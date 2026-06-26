#!/usr/bin/env python3
"""
Valve RCON (Remote Console) 客户端
通过 RCON 协议执行游戏服务器命令

用法:
    python3 rcon_cmd.py <host> <port> <password> <command>
    python3 rcon_cmd.py 192.168.1.100 27015 mypassword "status"

注意: L4D2 的 RCON 端口通常与游戏端口相同 (默认 27015)
"""

import socket
import struct
import sys


# RCON 数据包类型
SERVERDATA_AUTH = 3
SERVERDATA_AUTH_RESPONSE = 2
SERVERDATA_EXECCOMMAND = 2
SERVERDATA_RESPONSE_VALUE = 0


def create_packet(packet_id, packet_type, body):
    """创建 RCON 数据包
    
    数据包结构:
    - 4 bytes: 包大小 (不包含这4字节)
    - 4 bytes: 包ID
    - 4 bytes: 包类型
    - n bytes: 包体 (body + null + null)
    """
    body_bytes = body.encode('ascii') + b'\x00\x00'
    payload = struct.pack('<II', packet_id, packet_type) + body_bytes
    return struct.pack('<I', len(payload)) + payload


def read_packet(sock, timeout=30.0):
    """读取 RCON 响应数据包"""
    sock.settimeout(timeout)
    
    # 读取大小 (4 bytes)
    size_data = b''
    while len(size_data) < 4:
        chunk = sock.recv(4 - len(size_data))
        if not chunk:
            return None, None, None
        size_data += chunk
    
    size = struct.unpack('<I', size_data)[0]
    
    # 读取剩余数据
    data = b''
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            break
        data += chunk
    
    if len(data) < 8:
        return None, None, None
    
    packet_id = struct.unpack('<I', data[:4])[0]
    packet_type = struct.unpack('<I', data[4:8])[0]
    body = data[8:].rstrip(b'\x00').decode('utf-8', errors='replace')
    
    return packet_id, packet_type, body


def send_command(host, port, password, command, timeout=30.0):
    """通过 RCON 发送命令并获取响应"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        # 连接服务器
        sock.connect((host, port))
        
        # 发送认证包
        auth_packet = create_packet(1, SERVERDATA_AUTH, password)
        sock.sendall(auth_packet)
        
        # 读取认证响应（可能有多个包，包括空响应）
        auth_success = False
        for _ in range(10):
            packet_id, packet_type, body = read_packet(sock, timeout)
            if packet_type == SERVERDATA_AUTH_RESPONSE:
                if packet_id == -1:
                    return {'success': False, 'error': '认证失败（密码错误）'}
                auth_success = True
                break
        
        if not auth_success:
            return {'success': False, 'error': '认证响应异常'}
        
        # 发送命令
        cmd_packet = create_packet(2, SERVERDATA_EXECCOMMAND, command)
        sock.sendall(cmd_packet)
        
        # 发送空命令标记结束（获取完整响应的技巧）
        empty_packet = create_packet(3, SERVERDATA_EXECCOMMAND, "")
        sock.sendall(empty_packet)
        
        # 读取响应
        full_response = ""
        for _ in range(50):
            packet_id, packet_type, body = read_packet(sock, timeout)
            if packet_id is None:
                break
            if packet_id == 3:  # 空包响应，表示命令输出结束
                break
            if packet_id == 2:
                full_response += body
        
        return {
            'success': True,
            'command': command,
            'response': full_response.strip(),
            'host': host,
            'port': port
        }
        
    except socket.timeout:
        return {'success': False, 'error': '连接超时'}
    except socket.error as e:
        return {'success': False, 'error': f'网络错误: {str(e)}'}
    except Exception as e:
        return {'success': False, 'error': f'执行失败: {str(e)}'}
    finally:
        sock.close()


def main():
    if len(sys.argv) < 5:
        print("用法: python3 rcon_cmd.py <host> <port> <password> <command>")
        print("示例: python3 rcon_cmd.py 192.168.1.100 27015 mypassword status")
        print("      python3 rcon_cmd.py 192.168.1.100 27015 mypassword \"changelevel c5m1_waterfront\"")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    password = sys.argv[3]
    command = ' '.join(sys.argv[4:])
    
    result = send_command(host, port, password, command)
    
    if result['success']:
        print(f"✅ 命令执行成功: {result['command']}")
        print(f"📝 响应:\n{result['response']}")
    else:
        print(f"❌ 执行失败: {result['error']}")


if __name__ == '__main__':
    main()