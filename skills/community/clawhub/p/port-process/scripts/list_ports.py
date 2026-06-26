#!/usr/bin/env python3
"""
列出所有正在使用的端口

支持 macOS 和 Linux 系统。

用法:
    python list_ports.py
    python list_ports.py --tcp
    python list_ports.py --udp
    python list_ports.py --verbose
    python list_ports.py --json
"""

import argparse
import json
import subprocess
import sys
import platform
import re


def run_command(cmd, shell=True):
    """运行命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)


def list_ports_macos(tcp_only=False, udp_only=False):
    """在 macOS 上列出端口"""
    ports = []
    
    # 使用 lsof
    cmd = "lsof -i -P -n"
    code, stdout, stderr = run_command(cmd)
    
    if code != 0:
        return ports
    
    for line in stdout.strip().split("\n"):
        if "LISTEN" not in line:
            continue
        
        parts = line.split()
        if len(parts) < 9:
            continue
        
        # 解析格式：COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
        command = parts[0]
        pid = parts[1]
        user = parts[2]
        name = parts[8]
        
        # 解析地址和端口，格式：*:8080 (LISTEN) 或 127.0.0.1:5432 (LISTEN)
        match = re.search(r'([*0-9.]+):(\d+)', name)
        if not match:
            continue
        
        address = match.group(1)
        port = int(match.group(2))
        
        # 确定协议
        proto = "TCP"
        if "UDP" in line or udp_only:
            proto = "UDP"
        
        # 过滤
        if tcp_only and proto != "TCP":
            continue
        if udp_only and proto != "UDP":
            continue
        
        ports.append({
            "port": port,
            "proto": proto,
            "address": address,
            "pid": int(pid),
            "user": user,
            "command": command
        })
    
    # 按端口排序
    ports.sort(key=lambda x: x["port"])
    return ports


def list_ports_linux(tcp_only=False, udp_only=False):
    """在 Linux 上列出端口"""
    ports = []
    
    # 尝试 ss
    cmd = "ss -tulpn 2>/dev/null"
    code, stdout, stderr = run_command(cmd)
    
    if code == 0 and stdout.strip():
        for line in stdout.strip().split("\n"):
            if line.startswith("Netid"):
                continue
            
            parts = line.split()
            if len(parts) < 5:
                continue
            
            proto = parts[0].upper()
            local_addr = parts[4]
            
            # 过滤协议
            if tcp_only and "TCP" not in proto:
                continue
            if udp_only and "UDP" not in proto:
                continue
            
            # 解析地址和端口
            match = re.search(r'([*0-9.]+):(\d+)', local_addr)
            if not match:
                continue
            
            address = match.group(1)
            port = int(match.group(2))
            
            # 提取进程信息
            pid = ""
            command = ""
            user = ""
            
            if len(parts) > 5:
                proc_info = " ".join(parts[5:])
                pid_match = re.search(r'pid=(\d+)', proc_info)
                if pid_match:
                    pid = pid_match.group(1)
                
                cmd_match = re.search(r'process="([^"]+)"', proc_info)
                if cmd_match:
                    command = cmd_match.group(1)
            
            ports.append({
                "port": port,
                "proto": proto,
                "address": address,
                "pid": int(pid) if pid else 0,
                "user": user,
                "command": command
            })
    
    if ports:
        ports.sort(key=lambda x: x["port"])
        return ports
    
    # 备选：使用 netstat
    cmd = "netstat -tulpn 2>/dev/null"
    code, stdout, stderr = run_command(cmd)
    
    if code == 0 and stdout.strip():
        for line in stdout.strip().split("\n"):
            if line.startswith("Active") or line.startswith("Proto"):
                continue
            
            parts = line.split()
            if len(parts) < 6:
                continue
            
            proto = parts[0].upper()
            local_addr = parts[3]
            
            # 过滤协议
            if tcp_only and "tcp" not in proto.lower():
                continue
            if udp_only and "udp" not in proto.lower():
                continue
            
            # 解析地址和端口
            match = re.search(r'([*0-9.]+):(\d+)', local_addr)
            if not match:
                continue
            
            address = match.group(1)
            port = int(match.group(2))
            
            ports.append({
                "port": port,
                "proto": proto,
                "address": address,
                "pid": 0,
                "user": "",
                "command": ""
            })
    
    ports.sort(key=lambda x: x["port"])
    return ports


def list_ports(tcp_only=False, udp_only=False):
    """跨平台列出端口"""
    system = platform.system()
    
    if system == "Darwin":
        return list_ports_macos(tcp_only, udp_only)
    elif system == "Linux":
        return list_ports_linux(tcp_only, udp_only)
    else:
        print(f"[!] 不支持的操作系统: {system}")
        return []


def main():
    parser = argparse.ArgumentParser(description="列出所有正在使用的端口")
    parser.add_argument("--tcp", action="store_true", help="仅显示 TCP 端口")
    parser.add_argument("--udp", action="store_true", help="仅显示 UDP 端口")
    parser.add_argument("--verbose", action="store_true", help="显示详细信息")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    ports = list_ports(args.tcp, args.udp)
    
    if args.json:
        print(json.dumps(ports, indent=2, ensure_ascii=False))
        return 0
    
    if not ports:
        print("✅ 没有发现监听端口")
        return 0
    
    print(f"\n📊 发现 {len(ports)} 个监听端口:\n")
    print("-" * 100)
    print(f"  {'端口':<8} {'协议':<6} {'地址':<15} {'PID':<8} {'进程'}")
    print("-" * 100)
    
    for p in ports:
        cmd_display = p["command"][:30] if p["command"] else "-"
        pid_display = str(p["pid"]) if p["pid"] else "-"
        print(f"  {p['port']:<8} {p['proto']:<6} {p['address']:<15} {pid_display:<8} {cmd_display}")
    
    print("-" * 100)
    
    if args.verbose:
        print("\n📋 详细信息:\n")
        for p in ports:
            print(f"  端口:     {p['port']}")
            print(f"  协议:     {p['proto']}")
            print(f"  地址:     {p['address']}")
            if p["pid"]:
                print(f"  PID:      {p['pid']}")
            if p["user"]:
                print(f"  用户:     {p['user']}")
            if p["command"]:
                print(f"  命令:     {p['command']}")
            print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
