#!/usr/bin/env python3
"""
MikroTik RouterOS API Client - 核心连接模块
"""

import socket
import select
from typing import List, Dict, Optional, Any


class MikroTikAPI:
    """MikroTik RouterOS API 客户端"""
    
    def __init__(self, host: str, username: str = 'admin', password: str = '', 
                 port: int = 8728, timeout: int = 5):
        """
        初始化 API 客户端
        
        Args:
            host: RouterOS 设备 IP 地址
            username: 用户名 (默认：admin)
            password: 密码 (默认：空)
            port: API 端口 (默认：8728, SSL 用 8729)
            timeout: 连接超时 (秒)
        """
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout
        self.sock: Optional[socket.socket] = None
        self.connected = False
    
    def connect(self) -> bool:
        """建立连接到 RouterOS"""
        try:
            self.sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
            self.sock.setblocking(0)  # 非阻塞模式（select 处理超时）
            self.connected = True
            return True
        except Exception as e:
            print(f"❌ 连接失败：{e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.connected = False
    
    def _send_word(self, word: str) -> None:
        """发送一个 API 命令字"""
        if not self.sock:
            raise ConnectionError("未连接到 RouterOS")
        
        data = word.encode('utf-8')
        length = len(data)
        
        # 编码长度前缀
        if length < 0x80:
            header = bytes([length])
        elif length < 0x4000:
            header = bytes([0x80 | (length >> 8), length & 0xFF])
        elif length < 0x200000:
            header = bytes([0xC0 | (length >> 16), (length >> 8) & 0xFF, length & 0xFF])
        elif length < 0x10000000:
            header = bytes([0xE0 | (length >> 24), (length >> 16) & 0xFF, 
                           (length >> 8) & 0xFF, length & 0xFF])
        else:
            header = bytes([0xF0, (length >> 24) & 0xFF, (length >> 16) & 0xFF,
                           (length >> 8) & 0xFF, length & 0xFF])
        
        self.sock.sendall(header + data)
    
    def _recv_word(self, timeout: float = 5.0) -> Optional[str]:
        """
        接收一个 API 词（word）
        
        RouterOS API 使用 length-prefixed 格式：
        - 第 1 位：长度标记
        - 后续字节：实际长度（根据标记位计算）
        - 最后：实际数据
        
        Returns:
            解码后的字符串，或 None（超时/错误）
        """
        if not self.sock:
            return None
        
        try:
            # 读取长度前缀（第 1 字节）
            self.sock.setblocking(0)
            ready = select.select([self.sock], [], [], timeout)
            if not ready[0]:
                return None
            
            first_byte = self.sock.recv(1)
            if not first_byte:
                return None
            
            length = first_byte[0]
            
            # 根据第 1 位计算实际长度
            if length & 0x80:
                if length & 0x40:
                    if length & 0x20:
                        if length & 0x10:
                            # 5 字节：11110xxx + 4 字节长度
                            length_bytes = self.sock.recv(4)
                            if len(length_bytes) < 4:
                                return None
                            length = ((length & 0x0F) << 24) | int.from_bytes(length_bytes, 'big')
                        else:
                            # 4 字节：1110xxxx + 3 字节长度
                            length_bytes = self.sock.recv(3)
                            if len(length_bytes) < 3:
                                return None
                            length = ((length & 0x07) << 16) | int.from_bytes(length_bytes, 'big')
                    else:
                        # 3 字节：110xxxxx + 2 字节长度
                        length_bytes = self.sock.recv(2)
                        if len(length_bytes) < 2:
                            return None
                        length = ((length & 0x1F) << 8) | length_bytes[1]
                else:
                    # 2 字节：10xxxxxx + 1 字节长度
                    second_byte = self.sock.recv(1)
                    if not second_byte:
                        return None
                    length = ((length & 0x3F) << 8) | second_byte[0]
            # else: 长度 < 0x80，直接使用
            
            # 读取实际数据
            if length > 0:
                data = b''
                while len(data) < length:
                    ready = select.select([self.sock], [], [], timeout)
                    if not ready[0]:
                        break
                    chunk = self.sock.recv(length - len(data))
                    if not chunk:
                        break
                    data += chunk
                
                return data.decode('utf-8', errors='ignore')
            
            return ''
            
        except Exception as e:
            print(f"⚠️ 接收词失败：{e}")
            return None
    
    def _recv_response(self, timeout: float = 5.0) -> List[Dict[str, Any]]:
        """
        接收完整的 API 响应
        
        RouterOS API 响应格式：
        - !re (记录/条目)
        - !done (完成)
        - !trap (错误)
        - !halt (停止)
        
        每个消息后跟多个 =key=value，以空字符串结束
        
        Returns:
            解析后的条目列表
        """
        results = []
        current_entry = {}
        message_type = None
        
        try:
            while True:
                word = self._recv_word(timeout)
                
                if word is None:
                    # 超时，返回已接收的数据
                    break
                
                if word == '':
                    # 空词表示当前消息结束
                    if message_type == '!re' and current_entry:
                        results.append(current_entry)
                        current_entry = {}
                    elif message_type in ('!done', '!trap', '!halt'):
                        # 完成/错误消息，返回结果
                        break
                elif word.startswith('!'):
                    # 消息类型
                    if message_type == '!re' and current_entry:
                        results.append(current_entry)
                        current_entry = {}
                    message_type = word
                elif word.startswith('='):
                    # =key=value 格式
                    if '=' in word[1:]:
                        key, value = word[1:].split('=', 1)
                        current_entry[key] = value
                
                # 减小后续超时
                timeout = 0.5
                
        except Exception as e:
            print(f"⚠️ 接收响应失败：{e}")
        
        return results
    
    def _parse_response(self, data: bytes) -> List[Dict[str, str]]:
        """
        解析 API 响应数据（向后兼容，已废弃）
        
        请使用 _recv_response() 代替
        """
        return self._recv_response()
    
    def login(self) -> bool:
        """登录到 RouterOS"""
        if not self.sock:
            return False
        
        try:
            # 发送登录命令
            self._send_word('/login')
            self._send_word(f'=name={self.username}')
            self._send_word(f'=password={self.password}')
            self._send_word('')  # 结束标记
            
            # 接收响应
            response = self._recv_response(timeout=3.0)
            
            # 检查是否有 !done 响应（登录成功标志）
            for item in response:
                if item.get('ret') == '!done':
                    return True
            
            # 如果没有 !done 但有数据，也算成功（兼容旧版本）
            if len(response) > 0:
                return True
            
            # 没有任何响应，可能是连接问题
            return False
            
        except Exception as e:
            print(f"❌ 登录失败：{e}")
            return False
    
    def run_command(self, command: str, args: Optional[List[str]] = None) -> List[Dict[str, str]]:
        """
        执行 API 命令
        
        Args:
            command: 命令路径 (如 '/system/resource/print')
            args: 额外参数列表 (如 ['=detail=', '=active='])
        
        Returns:
            解析后的响应数据列表（支持多条目）
        """
        if not self.connected:
            raise ConnectionError("未连接到 RouterOS")
        
        try:
            # 发送命令
            self._send_word(command)
            if args:
                for arg in args:
                    self._send_word(arg)
            self._send_word('')  # 结束标记
            
            # 接收并解析响应（使用新的解析器）
            return self._recv_response(timeout=5.0)
        except Exception as e:
            print(f"❌ 命令执行失败：{e}")
            return []
    
    def __enter__(self):
        """上下文管理器入口"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.disconnect()
