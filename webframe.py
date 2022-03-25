"""webframe的服务端"""

from socket import *
from select import *
import json
import sys,os
from setttings import *
class Application:
    def __init__(self):
        self.p = epoll()

        self.socked = socket()
        self.socked.setsockopt(SOL_SOCKET,SO_REUSEADDR,DEBUG)
        self.socked.bind((frame_ip,port))

        self.dict_io = {self.socked.fileno():self.socked}


    #处理客户段请求
    def start(self):
        self.socked.listen(5)

        #监听套套接字
        self.p.register(self.socked,EPOLLIN | EPOLLERR)

        while True:
            events = self.p.poll()

            for fd,event in events:
                if fd == self.socked.fileno():
                    con,addr = self.dict_io[fd].accept()
                    print("Connect from ,,,,,,,",addr)
                    self.p.register(con,EPOLLIN | EPOLLERR)
                    self.dict_io[con.fileno()]=con
                elif event & EPOLLIN:
                    data = self.dict_io[fd].recv(1024*1024)
                    if not data:
                        con.close()
                        self.p.unregister(fd)
                        del self.dict_io[fd]
                        continue
                    print(data.decode())

                    data ={"status":200,"data":"success"}
                    con.send(json.dumps(data).encode())







app = Application()

app.start()