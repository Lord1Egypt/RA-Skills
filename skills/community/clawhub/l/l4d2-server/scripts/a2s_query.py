#!/usr/bin/env python3
"""
A2S (Valve Server Query) 查询脚本
查询 Source 引擎游戏服务器状态（L4D2、CS2 等）

用法:
    python3 a2s_query.py <host> [port] [--json]
    默认端口 27015
"""

import socket
import struct
import sys
import json
from datetime import datetime


def send_a2s_packet(sock, host, port, payload, challenge=None):
    """发送 A2S 数据包并接收响应"""
    if challenge:
        # 挑战码追加到数据包末尾
        payload = payload + challenge
    
    sock.settimeout(10.0)
    sock.sendto(payload, (host, port))
    
    response, _ = sock.recvfrom(4096)
    return response


def parse_a2s_info_response(data):
    """解析 A2S_INFO 响应"""
    if len(data) < 5:
        return None
    
    # 跳过头部 (4 bytes header + 1 byte type)
    offset = 5
    
    result = {}
    
    # Protocol version (1 byte)
    result['protocol'] = data[offset]
    offset += 1
    
    # Server name (null-terminated string)
    name_end = data.index(b'\x00', offset)
    result['name'] = data[offset:name_end].decode('utf-8', errors='replace')
    offset = name_end + 1
    
    # Map name (null-terminated string)
    map_end = data.index(b'\x00', offset)
    result['map'] = data[offset:map_end].decode('utf-8', errors='replace')
    offset = map_end + 1
    
    # Folder/game directory (null-terminated string)
    folder_end = data.index(b'\x00', offset)
    result['folder'] = data[offset:folder_end].decode('utf-8', errors='replace')
    offset = folder_end + 1
    
    # Game name (null-terminated string)
    game_end = data.index(b'\x00', offset)
    result['game'] = data[offset:game_end].decode('utf-8', errors='replace')
    offset = game_end + 1
    
    # App ID (2 bytes, little-endian)
    result['app_id'] = struct.unpack('<H', data[offset:offset+2])[0]
    offset += 2
    
    # Player count (1 byte)
    result['players'] = data[offset]
    offset += 1
    
    # Max players (1 byte)
    result['max_players'] = data[offset]
    offset += 1
    
    # Bot count (1 byte)
    result['bots'] = data[offset]
    offset += 1
    
    # Server type (1 byte: 'd' = dedicated, 'l' = listen, 'p' = SourceTV)
    result['server_type'] = chr(data[offset])
    offset += 1
    
    # Environment (1 byte: 'w' = Windows, 'l' = Linux)
    result['environment'] = chr(data[offset])
    offset += 1
    
    # Visibility (1 byte: 0 = public, 1 = private)
    result['visibility'] = data[offset]
    offset += 1
    
    # VAC secured (1 byte: 0 = unsecured, 1 = secured)
    result['vac'] = data[offset]
    offset += 1
    
    # Game version (null-terminated string)
    if offset < len(data):
        version_end = data.index(b'\x00', offset) if b'\x00' in data[offset:] else len(data)
        result['version'] = data[offset:version_end].decode('utf-8', errors='replace')
    
    return result


def query_server(host, port=27015):
    """查询服务器状态"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # A2S_INFO 请求包
        # Header: 0xFFFFFFFF (long) + 'T' (byte) + Source Engine Query (string)
        A2S_INFO = b'\xff\xff\xff\xffTSource Engine Query\x00'
        
        # 先发送请求，可能需要挑战码
        response = send_a2s_packet(sock, host, port, A2S_INFO)
        
        # 检查是否需要挑战码
        # 响应以 0x9A 开头表示需要挑战码
        if response[4] == 0x41:  # A2S_INFO_CHALLENGE response
            challenge = response[5:9]  # 提取挑战码
            response = send_a2s_packet(sock, host, port, A2S_INFO, challenge)
        
        # 解析响应
        if response[4] == 0x49:  # 'I' = A2S_INFO response
            info = parse_a2s_info_response(response)
            
            if info:
                info['host'] = host
                info['port'] = port
                info['query_time'] = datetime.now().isoformat()
                return info
        
        return {'error': 'Failed to parse server response', 'raw': response.hex()}
        
    except socket.timeout:
        return {'error': 'Connection timed out', 'host': host, 'port': port}
    except socket.error as e:
        return {'error': f'Socket error: {str(e)}', 'host': host, 'port': port}
    except Exception as e:
        return {'error': f'Query failed: {str(e)}', 'host': host, 'port': port}
    finally:
        sock.close()


def format_output(info, json_output=False):
    """格式化输出"""
    if json_output:
        return json.dumps(info, indent=2, ensure_ascii=False)
    
    if 'error' in info:
        return f"❌ 查询失败: {info['error']}"
    
    lines = [
        f"🖥️  服务器: {info.get('name', 'Unknown')}",
        f"📍 地址: {info['host']}:{info['port']}",
        f"🗺️  地图: {info.get('map', 'Unknown')}",
        f"👥 玩家: {info.get('players', 0)}/{info.get('max_players', 0)} ({info.get('bots', 0)} bots)",
        f"🎮 游戏: {info.get('game', 'Unknown')} (AppID: {info.get('app_id', 0)})",
        f"📦 版本: {info.get('version', 'Unknown')}",
        f"🔒 VAC: {'已启用' if info.get('vac') else '未启用'}",
        f"🌐 类型: {'Linux' if info.get('environment') == 'l' else 'Windows'} {info.get('server_type', '')}",
    ]
    
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print("用法: python3 a2s_query.py <host> [port] [--json]")
        print("示例: python3 a2s_query.py 192.168.1.100 27015")
        print("      python3 a2s_query.py 192.168.1.100 --json")
        sys.exit(0)
    
    host = sys.argv[1]
    port = 27015
    json_output = '--json' in sys.argv
    
    # 解析端口
    if ':' in host:
        host, port_str = host.split(':')
        port = int(port_str)
    elif len(sys.argv) > 2 and sys.argv[2].isdigit():
        port = int(sys.argv[2])
    
    info = query_server(host, port)
    print(format_output(info, json_output))


if __name__ == '__main__':
    main()