#!/usr/bin/env python3
"""
MikroTik 设备扫描器 - 通过 API 端口扫描发现设备

扫描局域网中开放 8728 端口（MikroTik API）的设备
"""

import socket
import struct
import time
import subprocess
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


class MikroTikScanner:
    """MikroTik 设备扫描器（通过 API 端口扫描）"""
    
    # MikroTik API 端口
    API_PORT = 8728
    API_SSL_PORT = 8729
    
    # MikroTik OUI 前缀（用于从 ARP 获取 MAC）
    MIKROTIK_OUIS = [
        '00:0C:42', '4C:5E:0C', 'D4:CA:6D',
        '78:8B:77', '84:D1:54', 'B8:69:F4',
        '48:8F:5A', 'CC:2D:E0', '08:55:31',
        '90:09:D0', 'FE:F5:CF'
    ]
    
    def __init__(self, timeout: float = 1.0, max_threads: int = 50):
        """
        初始化扫描器
        
        Args:
            timeout: 单个 IP 扫描超时（秒）
            max_threads: 最大并发线程数
        """
        self.timeout = timeout
        self.max_threads = max_threads
        self.discovered_devices: List[Dict] = []
    
    def get_local_subnets(self) -> List[str]:
        """获取本地所有 /24 网段"""
        subnets = []
        try:
            result = subprocess.run(['ip', '-o', 'addr', 'show'], 
                                   capture_output=True, text=True, timeout=5)
            
            for line in result.stdout.split('\n'):
                if 'inet ' in line and '/' in line:
                    parts = line.split()
                    for part in parts:
                        if '/' in part and '.' in part:
                            ip, prefix = part.split('/')
                            if int(prefix) <= 24:  # 支持 /24 及更大的网段
                                iface = parts[1] if len(parts) > 1 else ''
                                if iface not in ['lo', 'docker0'] and not iface.startswith('br-'):
                                    octets = ip.split('.')
                                    if int(prefix) == 24:
                                        subnet = f"{octets[0]}.{octets[1]}.{octets[2]}.0/{prefix}"
                                    else:
                                        # 对于更大的网段，计算网络地址
                                        network = self._get_network(ip, int(prefix))
                                        subnet = f"{network}/{prefix}"
                                    if subnet not in subnets:
                                        subnets.append(subnet)
        except Exception as e:
            print(f"⚠️ 获取本地网段失败：{e}")
        
        return subnets
    
    def _get_network(self, ip: str, prefix: int) -> str:
        """计算网络地址"""
        ip_int = struct.unpack('!I', socket.inet_aton(ip))[0]
        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        network = ip_int & mask
        return socket.inet_ntoa(struct.pack('!I', network))
    
    def get_local_ips(self) -> List[str]:
        """获取本机所有 IP 地址"""
        ips = []
        try:
            result = subprocess.run(['hostname', '-I'], 
                                   capture_output=True, text=True, timeout=5)
            ips = result.stdout.strip().split()
        except:
            pass
        return ips
    
    def get_arp_macs(self) -> Dict[str, str]:
        """从 ARP 表获取 IP 到 MAC 的映射"""
        mac_map = {}
        local_ips = self.get_local_ips()
        
        try:
            result = subprocess.run(['ip', 'neigh'], 
                                   capture_output=True, text=True, timeout=5)
            
            for line in result.stdout.split('\n'):
                parts = line.split()
                if len(parts) >= 5 and parts[1] == 'dev':
                    ip = parts[0]
                    if ip in local_ips:
                        continue
                    
                    mac = ''
                    for i, part in enumerate(parts):
                        if part == 'lladdr':
                            mac = parts[i+1].upper() if i+1 < len(parts) else ''
                            break
                    
                    if mac and mac != '00:00:00:00:00:00':
                        mac_map[ip] = mac
        except Exception as e:
            print(f"⚠️ 读取 ARP 表失败：{e}")
        
        return mac_map
    
    def scan_ip(self, ip: str, arp_macs: Dict[str, str]) -> Optional[Dict]:
        """
        扫描单个 IP 的 API 端口
        
        Args:
            ip: 目标 IP 地址
            arp_macs: ARP 表中的 MAC 地址映射
        
        Returns:
            设备信息字典，如果端口未开放则返回 None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            
            # 尝试普通 API 端口
            result = sock.connect_ex((ip, self.API_PORT))
            
            if result == 0:
                # 端口开放
                mac = arp_macs.get(ip, 'Unknown')
                is_mikrotik = mac != 'Unknown' and any(mac.startswith(oui) for oui in self.MIKROTIK_OUIS)
                
                device = {
                    'ip': ip,
                    'mac': mac,
                    'port': self.API_PORT,
                    'identity': 'Unknown',
                    'model': 'Unknown',
                    'version': '',
                    'source': 'api_port',
                    'is_mikrotik': is_mikrotik
                }
                
                # 尝试获取设备信息（如果 MAC 匹配 MikroTik）
                if is_mikrotik:
                    try:
                        # 简单 API 连接测试
                        from client import MikroTikAPI
                        api = MikroTikAPI(ip, 'admin', '', timeout=2)
                        if api.connect():
                            # 尝试登录（空密码）
                            if api.login():
                                result = api.run_command('/system/identity/print')
                                if result:
                                    device['identity'] = result[0].get('name', 'Unknown')
                                
                                result = api.run_command('/system/resource/print')
                                if result:
                                    device['version'] = result[0].get('version', '')
                                
                                api.disconnect()
                    except:
                        pass
                
                sock.close()
                return device
            
            # 尝试 SSL API 端口
            sock.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((ip, self.API_SSL_PORT))
            
            if result == 0:
                mac = arp_macs.get(ip, 'Unknown')
                is_mikrotik = mac != 'Unknown' and any(mac.startswith(oui) for oui in self.MIKROTIK_OUIS)
                
                device = {
                    'ip': ip,
                    'mac': mac,
                    'port': self.API_SSL_PORT,
                    'identity': 'Unknown',
                    'model': 'Unknown',
                    'version': '',
                    'source': 'api_ssl_port',
                    'is_mikrotik': is_mikrotik
                }
                
                sock.close()
                return device
            
            sock.close()
            return None
            
        except Exception as e:
            return None
    
    def scan_subnet(self, subnet: str, arp_macs: Dict[str, str]) -> List[Dict]:
        """
        扫描单个子网
        
        Args:
            subnet: 子网地址（如 '192.168.1.0/24'）
            arp_macs: ARP 表中的 MAC 地址映射
        
        Returns:
            发现的设备列表
        """
        devices = []
        
        # 生成子网中的所有 IP
        network, prefix = subnet.split('/')
        prefix = int(prefix)
        
        network_bytes = struct.unpack('!I', socket.inet_aton(network))[0]
        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        network_masked = network_bytes & mask
        broadcast = network_masked | (~mask & 0xFFFFFFFF)
        
        # 计算 IP 数量
        ip_count = broadcast - network_masked - 1
        
        print(f"   扫描：{subnet} ({ip_count} 个 IP)")
        
        # 生成 IP 列表
        ips = []
        for ip_int in range(network_masked + 1, broadcast):
            ip = socket.inet_ntoa(struct.pack('!I', ip_int))
            if ip not in self.get_local_ips():  # 排除本机 IP
                ips.append(ip)
        
        # 并发扫描
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(self.scan_ip, ip, arp_macs): ip for ip in ips}
            
            completed = 0
            for future in as_completed(futures):
                ip = futures[future]
                try:
                    device = future.result()
                    if device:
                        devices.append(device)
                        status = "✅" if device['is_mikrotik'] else "⚠️"
                        print(f"     {status} {ip}:{device['port']} (MAC: {device['mac']})")
                except Exception as e:
                    pass
                
                completed += 1
                if completed % 50 == 0:
                    print(f"     进度：{completed}/{len(ips)}")
        
        return devices
    
    def scan(self) -> List[Dict]:
        """
        执行完整扫描（API 端口 + ARP 表补充）
        
        Returns:
            发现的设备列表
        """
        all_devices = {}
        
        # 获取本地网段
        subnets = self.get_local_subnets()
        if not subnets:
            print("⚠️ 无法获取本地网段")
            return []
        
        print(f"📡 扫描 {len(subnets)} 个本地网段:")
        for subnet in subnets:
            print(f"   - {subnet}")
        print()
        
        # 获取 ARP 表中的 MAC 地址
        print("🔍 读取 ARP 表获取 MAC 地址...")
        arp_macs = self.get_arp_macs()
        print(f"   获取到 {len(arp_macs)} 个 MAC 地址\n")
        
        # 方法 1: 扫描 API 端口（主要方式）
        print("🔍 方法 1: 扫描 API 端口 (8728/8729)...")
        for subnet in subnets:
            devices = self.scan_subnet(subnet, arp_macs)
            for dev in devices:
                mac = dev.get('mac', '')
                if mac and mac != 'Unknown':
                    all_devices[mac] = dev
                else:
                    all_devices[dev['ip']] = dev
        
        # 方法 2: ARP 表补充（仅用于获取 MAC 地址，不显示未启用 API 的设备）
        print("\n🔍 方法 2: 读取 ARP 表补充 MAC 地址...")
        for ip, mac in arp_macs.items():
            if ip in [d['ip'] for d in all_devices.values()]:
                # 更新已发现设备的 MAC 地址
                for dev in all_devices.values():
                    if dev['ip'] == ip and dev.get('mac') == 'Unknown':
                        dev['mac'] = mac
        
        self.discovered_devices = list(all_devices.values())
        return self.discovered_devices
    
    def format_results(self) -> str:
        """格式化扫描结果 - 只显示 API 可用的设备"""
        if not self.discovered_devices:
            return "  (未发现设备)"
        
        # 只显示 API 可用的设备
        api_devices = [d for d in self.discovered_devices if d.get('port') not in ['N/A', None]]
        
        if not api_devices:
            return "  (未发现启用 API 的 MikroTik 设备)"
        
        lines = []
        lines.append(f"\n✅ MikroTik 设备 ({len(api_devices)}):\n")
        
        for i, device in enumerate(api_devices, 1):
            identity = device.get('identity', 'Unknown')
            ip = device.get('ip', 'N/A')
            mac = device.get('mac', '')
            version = device.get('version', '')
            port = device.get('port', 8728)
            
            lines.append(f"  [{i}] {identity}")
            lines.append(f"      IP: {ip}:{port}")
            if mac and mac != 'Unknown':
                lines.append(f"      MAC: {mac}")
            if version:
                lines.append(f"      RouterOS: {version}")
            lines.append("")
        
        lines.append(f"共发现 {len(api_devices)} 个设备")
        
        return "\n".join(lines)


def scan_network() -> str:
    """扫描网络中的 MikroTik 设备"""
    scanner = MikroTikScanner(timeout=1.0, max_threads=50)
    scanner.scan()
    return scanner.format_results()


if __name__ == '__main__':
    print(scan_network())
