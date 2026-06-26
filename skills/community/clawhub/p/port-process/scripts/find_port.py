#!/usr/bin/env python3
"""
查找占用指定端口的进程

支持 macOS 和 Linux 系统。

用法:
    python find_port.py <port> [port2] [port3...]
    python find_port.py 8080
    python find_port.py 8080 3000 5432
    python find_port.py 8080 --json
"""

import argparse
import json
import subprocess
import sys
import platform


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


def find_processes_by_port_macos(port):
    """在 macOS 上使用 lsof 查找进程"""
    cmd = f"lsof -ti :{port}"
    code, stdout, stderr = run_command(cmd)
    
    if code != 0 or not stdout.strip():
        return []
    
    pids = stdout.strip().split("\n")
    processes = []
    
    for pid in pids:
        pid = pid.strip()
        if not pid:
            continue
        
        # 获取进程详细信息
        cmd_ps = f"ps -p {pid} -o pid=,ppid=,user=,command="
        code_ps, stdout_ps, stderr_ps = run_command(cmd_ps)
        
        if code_ps == 0 and stdout_ps.strip():
            parts = stdout_ps.strip().split(None, 3)
            if len(parts) >= 4:
                processes.append({
                    "pid": int(parts[0]),
                    "ppid": int(parts[1]),
                    "user": parts[2],
                    "command": parts[3],
                    "port": port
                })
    
    return processes


def find_processes_by_port_linux(port):
    """在 Linux 上查找进程（尝试 ss, netstat, lsof）"""
    processes = []
    
    # 方法 1: 使用 ss
    cmd_ss = f"ss -tulpn 2>/dev/null | grep :{port}"
    code_ss, stdout_ss, stderr_ss = run_command(cmd_ss)
    
    if code_ss == 0 and stdout_ss.strip():
        for line in stdout_ss.strip().split("\n"):
            if f":{port}" in line:
                # 提取 pid，格式通常是 "pid=1234,process=xxx"
                import re
                pid_match = re.search(r'pid=(\d+)', line)
                if pid_match:
                    pid = pid_match.group(1)
                    cmd_ps = f"ps -p {pid} -o pid=,ppid=,user=,command="
                    code_ps, stdout_ps, stderr_ps = run_command(cmd_ps)
                    if code_ps == 0 and stdout_ps.strip():
                        parts = stdout_ps.strip().split(None, 3)
                        if len(parts) >= 4:
                            processes.append({
                                "pid": int(parts[0]),
                                "ppid": int(parts[1]),
                                "user": parts[2],
                                "command": parts[3],
                                "port": port
                            })
    
    if processes:
        return processes
    
    # 方法 2: 使用 lsof
    return find_processes_by_port_macos(port)


def find_processes_by_port(port):
    """跨平台查找占用端口的进程"""
    system = platform.system()
    
    if system == "Darwin":
        return find_processes_by_port_macos(port)
    elif system == "Linux":
        return find_processes_by_port_linux(port)
    else:
        print(f"[!] 不支持的操作系统: {system}")
        return []


def main():
    parser = argparse.ArgumentParser(description="查找占用指定端口的进程")
    parser.add_argument("ports", nargs="+", type=int, help="要查找的端口号")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    
    args = parser.parse_args()
    
    all_processes = []
    
    for port in args.ports:
        processes = find_processes_by_port(port)
        all_processes.extend(processes)
        
        if not args.json:
            if processes:
                print(f"\n🔍 端口 {port} 被以下进程占用:")
                print("-" * 80)
                for proc in processes:
                    print(f"  PID:     {proc['pid']}")
                    print(f"  PPID:    {proc['ppid']}")
                    print(f"  用户:    {proc['user']}")
                    print(f"  命令:    {proc['command'][:60]}{'...' if len(proc['command']) > 60 else ''}")
                    print()
            else:
                print(f"\n✅ 端口 {port} 没有被占用")
    
    if args.json:
        print(json.dumps(all_processes, indent=2, ensure_ascii=False))
    else:
        if all_processes:
            print(f"\n📊 总计找到 {len(all_processes)} 个进程")
        else:
            print("\n✅ 所有端口都没有被占用")
    
    return 0 if all_processes else 1


if __name__ == "__main__":
    sys.exit(main())
