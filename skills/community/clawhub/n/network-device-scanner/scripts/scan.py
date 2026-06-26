#!/usr/bin/env python3
"""
Network Device Scanner - 局域网设备扫描器
扫描局域网内活跃设备及其开放端口

此工具仅用于扫描用户自有网络，用于网络管理和设备发现。
"""

import subprocess
import socket
import re
import ipaddress
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Optional, Set

# 扫描端口列表
PORTS = [21, 22, 23, 53, 80, 135, 139, 443, 445, 554, 8000, 8080, 8443, 9000, 37777]
NETWORK = "172.16.10.0/24"
TIMEOUT = 0.3  # 端口扫描超时(秒)


@dataclass
class Device:
    ip: str
    mac: str = ""
    ports: List[int] = None
    device_type: str = "unknown"
    
    def __post_init__(self):
        if self.ports is None:
            self.ports = []


def get_arp_table() -> Set[str]:
    """获取ARP表中的IP地址 (Linux/通用)"""
    ips = set()
    
    # 方法1: 读取 /proc/net/arp (Linux)
    if os.path.exists('/proc/net/arp'):
        try:
            with open('/proc/net/arp', 'r') as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 4:
                        ip = parts[0]
                        mac = parts[3]
                        if ip.startswith('172.16.10.') and mac != '00:00:00:00:00:00':
                            ips.add(ip)
        except Exception as e:
            print(f"/proc/net/arp read error: {e}", file=sys.stderr)
    
    # 方法2: 使用 arp 命令 (如果可用)
    try:
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=10)
        # 匹配 172.16.10.x 地址
        pattern = r'172\.16\.10\.(\d+)'
        for line in result.stdout.splitlines():
            match = re.search(pattern, line)
            if match:
                ip = f"172.16.10.{match.group(1)}"
                # 检查不是广播地址
                if 'ff-ff-ff-ff-ff-ff' not in line.lower():
                    ips.add(ip)
    except FileNotFoundError:
        pass  # arp 命令不存在
    except Exception as e:
        print(f"ARP command error: {e}", file=sys.stderr)
    
    return ips


def ping_sweep() -> Set[str]:
    """Ping 扫描发现局域网设备"""
    ips = set()
    
    # 方法1: 使用 fping (更高效)
    try:
        result = subprocess.run(
            ['fping', '-g', '172.16.10.0/24', '-a'],
            capture_output=True, text=True, timeout=30
        )
        for line in result.stdout.splitlines():
            if line.strip().startswith('172.16.10.'):
                ips.add(line.strip())
    except FileNotFoundError:
        pass
    
    # 方法2: 使用 nmap (如果可用)
    if not ips:
        try:
            result = subprocess.run(
                ['nmap', '-sn', '-PR', '172.16.10.0/24', '-oG', '-'],
                capture_output=True, text=True, timeout=60
            )
            pattern = r'Host: (172\.16\.10\.\d+)'
            for match in re.finditer(pattern, result.stdout):
                ips.add(match.group(1))
        except FileNotFoundError:
            pass
    
    # 方法3: 简单的 ping 扫描 (备用)
    if not ips:
        print("Using basic ping sweep...", flush=True)
        def ping_ip(ip: str) -> Optional[str]:
            try:
                subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                             capture_output=True, timeout=2)
                return ip
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(ping_ip, f"172.16.10.{i}"): i for i in range(1, 255)}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    ips.add(result)
    
    return ips


def get_mac_for_ip(ip: str) -> str:
    """获取指定IP的MAC地址"""
    # 方法1: 从 /proc/net/arp 读取 (Linux)
    if os.path.exists('/proc/net/arp'):
        try:
            with open('/proc/net/arp', 'r') as f:
                for line in f:
                    parts = line.split()
                    if len(parts) >= 4 and parts[0] == ip:
                        mac = parts[3].upper()
                        if mac != '00:00:00:00:00:00':
                            return mac.replace(':', '-')
        except:
            pass
    
    # 方法2: 使用 arp 命令
    try:
        result = subprocess.run(['arp', '-a', ip], capture_output=True, text=True, timeout=5)
        pattern = r'([0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2}-[0-9a-f]{2})'
        match = re.search(pattern, result.stdout, re.IGNORECASE)
        if match:
            return match.group(1).lower()
    except:
        pass
    
    return ""


def scan_port(ip: str, port: int) -> Optional[int]:
    """扫描单个端口"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    try:
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            return port
    except:
        pass
    return None


def scan_ports(ip: str) -> List[int]:
    """扫描IP的开放端口"""
    open_ports = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(scan_port, ip, port): port for port in PORTS}
        for future in as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)
    return sorted(open_ports)


def identify_device(mac: str, ports: List[int]) -> str:
    """根据MAC前缀和开放端口识别设备类型"""
    mac_upper = mac.upper() if mac else ""
    port_str = ",".join(map(str, ports))
    
    # 端口识别规则
    if "445" in port_str and "135" in port_str:
        return "Windows电脑 (SMB/远程管理)"
    elif "22" in port_str and "80" in port_str:
        return "Linux服务器 (SSH/Web)"
    elif "3389" in port_str:
        return "Windows电脑 (RDP)"
    elif "554" in port_str or "37777" in port_str:
        return "监控摄像头 (RTSP)"
    elif "8000" in port_str:
        return "Web服务器"
    elif "80" in port_str or "8080" in port_str or "443" in port_str or "8443" in port_str:
        return "Web服务器/设备"
    
    # MAC前缀识别规则
    if not mac_upper:
        return "未知设备"
    
    mac_prefixes = {
        "E4-68-A3": "小米路由器",
        "40-31-3C": "小米设备 (智能电视/IoT)",
        "00-1D-0C": "小米设备",
        "C8-": "小米设备",
        "DC-2E-97": "小米设备",
        "30-9C-23": "Windows电脑",
        "24-DF-6A": "Windows电脑",
        "00-1E-58": "Dell设备",
        "00-25-9E": "Dell设备",
        "00-FF-EE": "Dell设备",
        "AC-DC-0E": "Dell设备",
        "F8-E4-3B": "Dell电脑",
        "00-14-22": "Dell电脑",
        "00-1B-21": "Intel设备",
        "00-0C-29": "VMware虚拟机",
        "00-50-56": "VMware虚拟机",
        "00-1C-14": "VMware虚拟机",
    }
    
    # 精确匹配
    if mac_upper in mac_prefixes:
        return mac_prefixes[mac_upper]
    
    # 前缀匹配
    for prefix, device in mac_prefixes.items():
        if prefix.endswith('-'):
            if mac_upper.startswith(prefix[:-1]):
                return device
        elif mac_upper.startswith(prefix):
            return device
    
    return "未知设备"


def scan_network() -> List[Device]:
    """扫描局域网设备"""
    print("Scanning...", flush=True)
    
    # 从ARP表获取已知IP
    known_ips = get_arp_table()
    
    # 如果ARP表为空，尝试ping扫描
    if not known_ips:
        print("ARP table empty, trying ping sweep...", flush=True)
        known_ips = ping_sweep()
    
    # 额外扫描一些常见IP (可配置)
    additional_ips = os.environ.get('SCAN_EXTRA_IPS', '172.16.10.234').split(',')
    for ip in additional_ips:
        if ip.strip():
            known_ips.add(ip.strip())
    
    # 去重并转为列表
    known_ips = list(set(known_ips))
    print(f"Found {len(known_ips)} IPs: {', '.join(sorted(known_ips))}", flush=True)
    
    results = []
    
    # 扫描每个IP的端口
    for ip in known_ips:
        open_ports = scan_ports(ip)
        
        if open_ports:
            mac = get_mac_for_ip(ip)
            device_type = identify_device(mac, open_ports)
            
            device = Device(
                ip=ip,
                mac=mac,
                ports=open_ports,
                device_type=device_type
            )
            results.append(device)
    
    # 按IP排序
    results.sort(key=lambda x: ipaddress.IPv4Address(x.ip))
    
    return results


def main():
    """主函数"""
    devices = scan_network()
    
    # 输出格式: IP|MAC|Ports|DeviceType
    for device in devices:
        port_list = ",".join(map(str, device.ports))
        print(f"{device.ip}|{device.mac}|{port_list}|{device.device_type}")


if __name__ == "__main__":
    main()
