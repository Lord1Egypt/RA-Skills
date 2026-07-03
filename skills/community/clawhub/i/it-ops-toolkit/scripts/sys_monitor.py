#!/usr/bin/env python3
"""
IT运维工具箱 - 系统监控模块
支持: CPU、内存、磁盘、进程、系统信息、网络接口、远程服务器监控
用法: python sys_monitor.py <command> [args...]
依赖: 纯标准库（跨平台）；远程监控依赖系统 ssh 命令
"""

import sys
import os
import platform
import subprocess
import time
import argparse
import socket
import json
import re
import shlex
from datetime import datetime, timedelta

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def color(text, code):
    return f"\033[{code}m{text}\033[0m"

def ok(msg):    return color(f"✅ {msg}", "32")
def warn(msg):  return color(f"⚠️  {msg}", "33")
def err(msg):   return color(f"❌ {msg}", "31")
def info(msg):  return color(f"ℹ️  {msg}", "36")
def bold(msg):  return color(msg, "1")
def green(msg): return color(msg, "32")
def yellow(msg):return color(msg, "33")
def red(msg):   return color(msg, "31")

def section(title):
    print(f"\n{bold('═' * 55)}")
    print(f"  {bold(title)}")
    print(bold('═' * 55))

def fmt_bytes(n):
    for unit in ["B","KB","MB","GB","TB"]:
        if n < 1024: return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"

def progress_bar(pct, width=30):
    filled = int(width * pct / 100)
    bar = "█" * filled + "░" * (width - filled)
    if pct < 70:   c = "32"
    elif pct < 85: c = "33"
    else:          c = "31"
    return color(f"[{bar}]", c) + f" {pct:5.1f}%"

# ─────────────────────────────────────────────
# 检测平台
# ─────────────────────────────────────────────

IS_WIN   = sys.platform == "win32"
IS_LINUX = sys.platform == "linux"
IS_MAC   = sys.platform == "darwin"

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           shell=isinstance(cmd, str))
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except Exception as e:
        return "", str(e), -1

# ─────────────────────────────────────────────
# 系统概览
# ─────────────────────────────────────────────

def cmd_sysinfo():
    section("系统信息概览")
    p = platform.uname()
    print(f"  主机名   : {bold(p.node)}")
    print(f"  操作系统 : {p.system} {p.release} {p.version[:50]}")
    print(f"  架构     : {p.machine} / {p.processor[:40] if p.processor else 'N/A'}")
    print(f"  Python   : {sys.version.split()[0]}")

    # 运行时间
    if IS_WIN:
        out, _, _ = run("powershell -Command \"(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime\"")
        print(f"  运行时间 : {out.splitlines()[0] if out else 'N/A'}")
    elif IS_LINUX:
        out, _, _ = run("uptime -p")
        print(f"  运行时间 : {out}")
    elif IS_MAC:
        out, _, _ = run("uptime")
        print(f"  运行时间 : {out}")

    # 时间
    print(f"  当前时间 : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  时区     : {time.tzname[0]}")

# ─────────────────────────────────────────────
# CPU 监控
# ─────────────────────────────────────────────

def _get_cpu_win():
    out, _, _ = run("powershell -Command \"Get-WmiObject -Class Win32_Processor | Select-Object LoadPercentage,Name,NumberOfCores,NumberOfLogicalProcessors | ConvertTo-Json\"")
    try:
        data = json.loads(out)
        if isinstance(data, list): data = data[0]
        return {
            "total": float(data.get("LoadPercentage", 0)),
            "name": data.get("Name", "N/A"),
            "cores": data.get("NumberOfCores", "N/A"),
            "logical": data.get("NumberOfLogicalProcessors", "N/A"),
        }
    except Exception:
        return None

def _get_cpu_linux():
    out, _, _ = run("grep -c ^processor /proc/cpuinfo")
    logical = out.strip()
    out2, _, _ = run("top -bn1 | grep 'Cpu(s)'")
    pct = 0.0
    m = re.search(r"(\d+\.?\d*)\s+id", out2)
    if m: pct = 100.0 - float(m.group(1))
    out3, _, _ = run("cat /proc/cpuinfo | grep 'model name' | head -1")
    name = out3.split(":")[1].strip() if ":" in out3 else "N/A"
    return {"total": pct, "name": name, "logical": logical, "cores": "N/A"}

def cmd_cpu(interval=1):
    section("CPU 使用率")
    if IS_WIN:
        data = _get_cpu_win()
    elif IS_LINUX:
        data = _get_cpu_linux()
    else:
        # macOS
        out, _, _ = run("sysctl -n machdep.cpu.brand_string")
        out2, _, _ = run("top -l 1 | grep 'CPU usage'")
        pct_m = re.search(r"(\d+\.?\d*)% user", out2)
        sys_m = re.search(r"(\d+\.?\d*)% sys",  out2)
        pct = (float(pct_m.group(1)) if pct_m else 0) + (float(sys_m.group(1)) if sys_m else 0)
        data = {"total": pct, "name": out, "logical": "N/A", "cores": "N/A"}

    if not data:
        print(err("获取CPU信息失败"))
        return

    print(f"  型号     : {data['name']}")
    print(f"  物理核心 : {data['cores']}  逻辑核心: {data['logical']}")
    print(f"  总体使用 : {progress_bar(data['total'])}")

    # 负载均值 (Linux/macOS)
    if not IS_WIN:
        out, _, _ = run("cat /proc/loadavg" if IS_LINUX else "sysctl -n vm.loadavg")
        parts = out.split()[:3]
        if parts:
            print(f"  负载均值 : {' | '.join(f'{x}' for x in parts)} (1/5/15分钟)")

    pct = data["total"]
    if pct < 70:   print(ok("CPU负载正常"))
    elif pct < 85: print(warn(f"CPU负载偏高: {pct:.1f}%"))
    else:          print(err(f"CPU负载过高: {pct:.1f}%，请检查高占用进程"))

# ─────────────────────────────────────────────
# 内存监控
# ─────────────────────────────────────────────

def cmd_mem():
    section("内存使用情况")
    if IS_WIN:
        out, _, _ = run("powershell -Command \"Get-WmiObject -Class Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory | ConvertTo-Json\"")
        try:
            data = json.loads(out)
            total = int(data["TotalVisibleMemorySize"]) * 1024
            free  = int(data["FreePhysicalMemory"])  * 1024
            used  = total - free
            pct   = used / total * 100
        except Exception:
            print(err("获取内存信息失败")); return
    elif IS_LINUX:
        out, _, _ = run("cat /proc/meminfo")
        m = {}
        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                m[parts[0].rstrip(":")] = int(parts[1]) * 1024
        total    = m.get("MemTotal", 0)
        free     = m.get("MemFree",  0)
        buffers  = m.get("Buffers",  0)
        cached   = m.get("Cached",   0)
        available= m.get("MemAvailable", free + buffers + cached)
        used     = total - available
        pct      = used / total * 100 if total else 0
    else:
        out, _, _ = run("vm_stat")
        page = 4096
        pages = {}
        for line in out.splitlines():
            m = re.match(r"(.+):\s+(\d+)", line)
            if m: pages[m.group(1).strip()] = int(m.group(2)) * page
        used  = pages.get("Pages active", 0) + pages.get("Pages wired down", 0)
        free  = pages.get("Pages free", 0)
        total = used + free + pages.get("Pages inactive", 0)
        pct   = used / total * 100 if total else 0

    print(f"  总内存   : {fmt_bytes(total)}")
    print(f"  已使用   : {fmt_bytes(used)}   {progress_bar(pct)}")
    print(f"  可用     : {fmt_bytes(total - used)}")

    if pct < 75:   print(ok("内存使用正常"))
    elif pct < 90: print(warn(f"内存使用偏高: {pct:.1f}%"))
    else:          print(err(f"内存不足: {pct:.1f}%，请检查内存泄漏或增加内存"))

# ─────────────────────────────────────────────
# 磁盘监控
# ─────────────────────────────────────────────

def cmd_disk():
    section("磁盘使用情况")
    if IS_WIN:
        out, _, _ = run("powershell -Command \"Get-PSDrive -PSProvider FileSystem | Select-Object Name,Used,Free | ConvertTo-Json\"")
        try:
            drives = json.loads(out)
            if isinstance(drives, dict): drives = [drives]
            print(f"  {'盘符':<6} {'总大小':>10} {'已用':>10} {'可用':>10} {'使用率':>8}  状态")
            print(f"  {'─'*6} {'─'*10} {'─'*10} {'─'*10} {'─'*8}  ──")
            for d in drives:
                used = int(d.get("Used") or 0)
                free = int(d.get("Free") or 0)
                total = used + free
                pct = used / total * 100 if total else 0
                name = d.get("Name", "?") + ":"
                status = ok("正常") if pct < 80 else (warn("偏高") if pct < 90 else err("紧张"))
                print(f"  {name:<6} {fmt_bytes(total):>10} {fmt_bytes(used):>10} {fmt_bytes(free):>10} {pct:>7.1f}%  {status}")
        except Exception:
            print(err("解析磁盘信息失败"))
    else:
        out, _, _ = run("df -h")
        print(out)

# ─────────────────────────────────────────────
# 进程监控
# ─────────────────────────────────────────────

def cmd_top(n=15, sort_by="cpu"):
    section(f"Top {n} 进程 (按{sort_by.upper()}排序)")
    if IS_WIN:
        prop = "CPU" if sort_by == "cpu" else "WorkingSet"
        out, _, _ = run(f"powershell -Command \"Get-Process | Sort-Object {prop} -Descending | Select-Object -First {n} Name,Id,CPU,WorkingSet | ConvertTo-Json\"")
        try:
            procs = json.loads(out)
            if isinstance(procs, dict): procs = [procs]
            print(f"  {'PID':>6} {'CPU(s)':>8} {'内存':>10}  进程名")
            print(f"  {'─'*6} {'─'*8} {'─'*10}  ──")
            for p in procs:
                cpu_s = p.get("CPU") or 0
                mem   = int(p.get("WorkingSet") or 0)
                print(f"  {p.get('Id',0):>6} {cpu_s:>8.1f} {fmt_bytes(mem):>10}  {p.get('Name','N/A')}")
        except Exception:
            print(err("获取进程列表失败"))
    elif IS_LINUX:
        sort_flag = "-k3" if sort_by == "cpu" else "-k4"
        out, _, _ = run(f"ps aux --sort=-{'%cpu' if sort_by=='cpu' else '%mem'} | head -n {n+1}")
        print(out)
    else:
        out, _, _ = run(f"ps aux | sort -r{'-k3' if sort_by=='cpu' else '-k4'} | head -n {n+1}")
        print(out)

# ─────────────────────────────────────────────
# 网络接口
# ─────────────────────────────────────────────

def cmd_netif():
    section("网络接口信息")
    if IS_WIN:
        out, _, _ = run("powershell -Command \"Get-NetIPAddress | Where-Object {$_.AddressFamily -ne 'IPv6'} | Select-Object InterfaceAlias,IPAddress,PrefixLength | ConvertTo-Json\"")
        try:
            items = json.loads(out)
            if isinstance(items, dict): items = [items]
            for i in items:
                print(f"  {i.get('InterfaceAlias','N/A'):<25} {i.get('IPAddress','N/A')}/{i.get('PrefixLength','N/A')}")
        except Exception:
            print(err("获取网络接口失败"))
    else:
        out, _, _ = run("ip addr" if IS_LINUX else "ifconfig")
        # 简化输出
        for line in out.splitlines():
            if re.match(r"^\d+:|^[a-z]", line) or "inet " in line:
                print(f"  {line}")

# ─────────────────────────────────────────────
# 全面扫描
# ─────────────────────────────────────────────

def cmd_full():
    cmd_sysinfo()
    cmd_cpu()
    cmd_mem()
    cmd_disk()
    cmd_top(10)
    cmd_netif()

# ─────────────────────────────────────────────
# 远程服务器监控（通过 SSH）
# ─────────────────────────────────────────────

def _ssh_exec(host, user, port, cmd_str, timeout=15, key=None):
    """
    通过系统 ssh 命令执行远程命令，返回 (stdout, stderr, returncode)。
    支持密钥文件和密码认证（密码通过 SSH_ASKPASS 环境变量传递）。
    """
    ssh_bin = "ssh"
    if IS_WIN:
        # Windows 常见 ssh 路径
        for candidate in [
            r"C:\Windows\System32\OpenSSH\ssh.exe",
            r"C:\Program Files\OpenSSH\ssh.exe",
            "ssh",
        ]:
            if os.path.isfile(candidate) or candidate == "ssh":
                ssh_bin = candidate
                break

    ssh_args = [
        ssh_bin,
        "-o", "StrictHostKeyChecking=no",
        "-o", "ConnectTimeout=8",
        "-o", "BatchMode=yes",
        "-p", str(port),
        f"{user}@{host}",
        cmd_str,
    ]

    if key:
        ssh_args.insert(-2, "-i")
        ssh_args.insert(-2, key)

    try:
        r = subprocess.run(ssh_args, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "SSH connection timed out", -1
    except FileNotFoundError:
        return "", "ssh command not found", -1
    except Exception as e:
        return "", str(e), -1


def _ssh_exec_json(host, user, port, cmd_str, timeout=15, key=None):
    """远程执行命令并解析 JSON 输出"""
    out, stderr, rc = _ssh_exec(host, user, port, cmd_str, timeout, key)
    if rc != 0:
        return None, stderr
    try:
        return json.loads(out), None
    except Exception as e:
        return None, f"JSON parse error: {e}"


def _remote_sysinfo(host, user, port, key=None):
    """远程系统信息"""
    section(f"系统信息概览 [{bold(user+'@'+host)}]")
    # 检测远程 OS 类型
    out, stderr, rc = _ssh_exec(host, user, port,
        "uname -s 2>/dev/null || echo WINDOWS", timeout=10, key=key)
    if rc != 0:
        print(err(f"SSH 连接失败: {stderr or '无法连接'}"))
        return None

    remote_os = out.strip()
    is_linux_remote = remote_os == "Linux"
    is_mac_remote   = remote_os == "Darwin"

    # 主机名
    out, _, _ = _ssh_exec(host, user, port, "hostname", timeout=5, key=key)
    print(f"  主机名   : {bold(out.strip()) if out else 'N/A'}")

    # OS 版本
    if is_linux_remote:
        out, _, _ = _ssh_exec(host, user, port,
            "cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | head -1 | cut -d'\"' -f2 || uname -r", timeout=5, key=key)
        print(f"  操作系统 : {out.strip()}")
    elif is_mac_remote:
        out, _, _ = _ssh_exec(host, user, port, "sw_vers -productVersion 2>/dev/null", timeout=5, key=key)
        print(f"  操作系统 : macOS {out.strip()}")
    else:
        out, _, _ = _ssh_exec(host, user, port, "ver 2>/dev/null || systeminfo | findstr /B /C:\"OS\" | head -1", timeout=10, key=key)
        print(f"  操作系统 : {out.strip()[:60]}")

    # 架构
    out, _, _ = _ssh_exec(host, user, port, "uname -m", timeout=5, key=key)
    print(f"  架构     : {out.strip()}")

    # 运行时间
    out, _, _ = _ssh_exec(host, user, port, "uptime -p 2>/dev/null || uptime", timeout=5, key=key)
    print(f"  运行时间 : {out.strip()[:60]}")

    # 当前时间
    out, _, _ = _ssh_exec(host, user, port, "date '+%Y-%m-%d %H:%M:%S %Z' 2>/dev/null || date", timeout=5, key=key)
    print(f"  服务器时间: {out.strip()}")

    return remote_os


def _remote_cpu(host, user, port, key=None):
    """远程 CPU 监控"""
    section(f"CPU 使用率 [{bold(user+'@'+host)}]")

    # 使用统一脚本：输出 JSON 格式的 CPU 信息
    script = r"""
python3 -c "
import subprocess, re, json
try:
    import json
except:
    pass
out = subprocess.check_output('grep -c ^processor /proc/cpuinfo 2>/dev/null || echo 0', shell=True).decode()
logical = out.strip()
out2 = subprocess.check_output('top -bn1 | grep \"Cpu(s)\" 2>/dev/null', shell=True).decode()
pct = 0.0
m = re.search(r'(\d+\.?\d*)\s+id', out2)
if m: pct = round(100.0 - float(m.group(1)), 1)
out3 = subprocess.check_output('cat /proc/cpuinfo 2>/dev/null | grep \"model name\" | head -1', shell=True).decode()
name = out3.split(':')[1].strip() if ':' in out3 else 'N/A'
out4 = subprocess.check_output('cat /proc/loadavg 2>/dev/null', shell=True).decode().strip()
load = out4.split()[:3] if out4 else []
print(json.dumps({'pct': pct, 'name': name, 'logical': logical, 'load': load}))
" 2>/dev/null
"""
    out, stderr, rc = _ssh_exec(host, user, port, script.strip(), timeout=15, key=key)

    if rc != 0:
        # 回退方案：用 grep + awk
        script_fallback = (
            "echo CPU_INFO_START; "
            "grep -c '^processor' /proc/cpuinfo 2>/dev/null || echo 'N/A'; "
            "grep 'model name' /proc/cpuinfo 2>/dev/null | head -1 | cut -d: -f2 | xargs || echo 'N/A'; "
            "top -bn1 2>/dev/null | grep 'Cpu(s)' | awk -F'id,' '{print 100 - $2}' | awk '{print int($1)}' || echo '0'; "
            "cat /proc/loadavg 2>/dev/null | awk '{print $1,$2,$3}' || echo 'N/A'; "
            "echo CPU_INFO_END"
        )
        out, stderr, rc = _ssh_exec(host, user, port, script_fallback, timeout=15, key=key)

        if rc != 0 or "CPU_INFO_START" not in out:
            print(err(f"获取远程CPU信息失败: {stderr[:100]}"))
            return

        # 解析回退输出
        lines = out.splitlines()
        data_lines = []
        capture = False
        for line in lines:
            if "CPU_INFO_START" in line:
                capture = True
                continue
            if "CPU_INFO_END" in line:
                capture = False
                continue
            if capture:
                data_lines.append(line.strip())

        if len(data_lines) >= 4:
            logical = data_lines[0]
            name    = data_lines[1]
            pct     = float(data_lines[2]) if data_lines[2].replace('.','').isdigit() else 0
            load    = data_lines[3].split()
        else:
            print(err("解析远程CPU数据失败"))
            return
    else:
        try:
            # 提取 JSON（可能在输出中夹杂其他内容）
            json_match = re.search(r'\{[^}]+\}', out)
            if not json_match:
                print(err("解析远程CPU数据失败")); return
            data = json.loads(json_match.group())
            pct    = float(data.get("pct", 0))
            name   = data.get("name", "N/A")
            logical= data.get("logical", "N/A")
            load   = data.get("load", [])
        except Exception as e:
            print(err(f"JSON解析失败: {e}")); return

    print(f"  型号     : {name}")
    print(f"  逻辑核心 : {logical}")
    print(f"  总体使用 : {progress_bar(pct)}")
    if load:
        print(f"  负载均值 : {' | '.join(f'{x}' for x in load)} (1/5/15分钟)")

    if pct < 70:   print(ok("CPU负载正常"))
    elif pct < 85: print(warn(f"CPU负载偏高: {pct:.1f}%"))
    else:          print(err(f"CPU负载过高: {pct:.1f}%"))


def _remote_mem(host, user, port, key=None):
    """远程内存监控"""
    section(f"内存使用情况 [{bold(user+'@'+host)}]")
    out, stderr, rc = _ssh_exec(host, user, port, "cat /proc/meminfo", timeout=10, key=key)
    if rc != 0:
        print(err(f"获取远程内存信息失败: {stderr[:100]}"))
        return

    m = {}
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            m[parts[0].rstrip(":")] = int(parts[1]) * 1024

    total     = m.get("MemTotal", 0)
    free      = m.get("MemFree",  0)
    buffers   = m.get("Buffers",  0)
    cached    = m.get("Cached",   0)
    available = m.get("MemAvailable", free + buffers + cached)
    used      = total - available
    pct       = used / total * 100 if total else 0

    # Swap
    swap_total = m.get("SwapTotal", 0)
    swap_free  = m.get("SwapFree", 0)
    swap_used  = swap_total - swap_free
    swap_pct   = swap_used / swap_total * 100 if swap_total else 0

    print(f"  物理内存")
    print(f"    总计   : {fmt_bytes(total)}")
    print(f"    已使用 : {fmt_bytes(used)}   {progress_bar(pct)}")
    print(f"    可用   : {fmt_bytes(available)}")

    if swap_total > 0:
        print(f"\n  Swap")
        print(f"    总计   : {fmt_bytes(swap_total)}")
        print(f"    已使用 : {fmt_bytes(swap_used)}   {progress_bar(swap_pct)}")
        if swap_pct > 50:
            print(warn(f"Swap 使用率 {swap_pct:.1f}%，可能存在内存压力"))

    if pct < 75:   print(ok("内存使用正常"))
    elif pct < 90: print(warn(f"内存使用偏高: {pct:.1f}%"))
    else:          print(err(f"内存不足: {pct:.1f}%"))


def _remote_disk(host, user, port, key=None):
    """远程磁盘监控"""
    section(f"磁盘使用情况 [{bold(user+'@'+host)}]")
    out, stderr, rc = _ssh_exec(host, user, port, "df -h --output=target,size,used,avail,pcent 2>/dev/null | tail -n +2 || df -h | tail -n +2", timeout=10, key=key)
    if rc != 0:
        print(err(f"获取远程磁盘信息失败: {stderr[:100]}"))
        return

    print(f"  {'挂载点':<20} {'总大小':>8} {'已用':>8} {'可用':>8} {'使用率':>6}  状态")
    print(f"  {'─'*20} {'─'*8} {'─'*8} {'─'*8} {'─'*6}  ──")
    warn_count = 0
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 5:
            target, size, used, avail, pcent = parts[0], parts[1], parts[2], parts[3], parts[4]
            pct_num = int(pcent.rstrip('%'))
            status = ok("正常") if pct_num < 80 else (warn("偏高") if pct_num < 90 else err("紧张"))
            print(f"  {target:<20} {size:>8} {used:>8} {avail:>8} {pcent:>6}  {status}")
            if pct_num >= 85:
                warn_count += 1

    if warn_count > 0:
        print(warn(f"\n  {warn_count} 个分区使用率超过 85%，请关注磁盘空间"))
    else:
        print(ok("所有分区使用率正常"))


def _remote_top(host, user, port, n=10, sort_by="cpu", key=None):
    """远程 Top 进程"""
    section(f"Top {n} 进程 [{bold(user+'@'+host)}] (按{sort_by.upper()}排序)")
    sort_key = "%cpu" if sort_by == "cpu" else "%mem"
    cmd = f"ps aux --sort=-{sort_key} | head -n {n+1}"
    out, stderr, rc = _ssh_exec(host, user, port, cmd, timeout=10, key=key)
    if rc != 0:
        print(err(f"获取远程进程列表失败: {stderr[:100]}"))
        return
    print(out)


def _remote_netif(host, user, port, key=None):
    """远程网络接口"""
    section(f"网络接口信息 [{bold(user+'@'+host)}]")
    out, stderr, rc = _ssh_exec(host, user, port,
        "ip -4 addr show 2>/dev/null | grep -E '^[0-9]+:|inet ' || ifconfig 2>/dev/null | grep -E '^[a-z]|inet '",
        timeout=10, key=key)
    if rc != 0:
        print(err(f"获取远程网络信息失败: {stderr[:100]}"))
        return
    for line in out.splitlines():
        print(f"  {line}")


def _remote_docker(host, user, port, key=None):
    """远程 Docker 容器状态"""
    section(f"Docker 容器状态 [{bold(user+'@'+host)}]")
    out, stderr, rc = _ssh_exec(host, user, port,
        "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' 2>&1", timeout=15, key=key)

    if rc != 0:
        if "not found" in stderr or "not recognized" in stderr:
            print(warn("远程主机未安装 Docker"))
        elif "permission denied" in stderr.lower():
            print(warn("权限不足，请使用 root 或 docker 组用户"))
        elif "Cannot connect" in stderr:
            print(err("远程 Docker Daemon 未启动"))
        else:
            print(err(f"远程Docker查询失败: {stderr[:150]}"))
        return

    if not out or "CONTAINER ID" not in out:
        print(info("无运行中的容器"))
        return

    print(out)

    # 统计
    running = out.count("Up")
    total   = len(out.splitlines()) - 1  # 减去 header
    print(ok(f"运行中: {running}/{total} 个容器"))


def _remote_uptime(host, user, port, key=None):
    """远程运行时间摘要（轻量级快速检查）"""
    out, stderr, rc = _ssh_exec(host, user, port,
        "echo '---HOST---'; hostname; echo '---UPTIME---'; uptime; echo '---LOAD---'; cat /proc/loadavg 2>/dev/null; echo '---DATE---'; date '+%Y-%m-%d %H:%M:%S %Z'",
        timeout=10, key=key)

    if rc != 0:
        print(err(f"无法连接 {user}@{host}: {stderr or '连接失败'}"))
        return False

    host_out = "N/A"
    uptime_out = "N/A"
    load_out = ""
    date_out = "N/A"

    current_key = ""
    for line in out.splitlines():
        if "---HOST---" in line:   current_key = "host"
        elif "---UPTIME---" in line: current_key = "uptime"
        elif "---LOAD---" in line:  current_key = "load"
        elif "---DATE---" in line:  current_key = "date"
        elif current_key == "host" and line.strip(): host_out = line.strip()
        elif current_key == "uptime" and line.strip(): uptime_out = line.strip()
        elif current_key == "load" and line.strip():   load_out = line.strip()
        elif current_key == "date" and line.strip():   date_out = line.strip()

    load_str = f"  负载均值 : {load_out}" if load_out else ""
    print(f"  主机 {bold(host_out):<25} 运行: {uptime_out[:40]}")
    print(load_str)
    print(f"  服务器时间: {date_out}")
    return True


# ── 远程综合监控 ──

def cmd_remote_full(host, user, port=22, key=None):
    """远程全面系统监控"""
    section(f"远程服务器综合监控 [{bold(user+'@'+host)}]")
    # 先测试连通性
    print(info("正在连接远程服务器..."))
    start = time.time()
    out, stderr, rc = _ssh_exec(host, user, port, "echo ok", timeout=10, key=key)
    elapsed = (time.time() - start) * 1000

    if rc != 0:
        print(err(f"SSH 连接失败 ({elapsed:.0f}ms): {stderr or '未知错误'}"))
        print(info("请检查: 1) 主机地址和端口 2) SSH 密钥配置 3) 防火墙规则"))
        return

    print(ok(f"SSH 连接成功 ({elapsed:.0f}ms)"))

    _remote_sysinfo(host, user, port, key)
    _remote_cpu(host, user, port, key)
    _remote_mem(host, user, port, key)
    _remote_disk(host, user, port, key)
    _remote_top(host, user, port, 10, "cpu", key)
    _remote_netif(host, user, port, key)
    _remote_docker(host, user, port, key)


def cmd_remote_batch(hosts_file=None, hosts=None, key=None):
    """批量远程服务器健康检查"""
    section("批量远程服务器健康检查")

    # 解析主机列表
    server_list = []
    if hosts:
        for spec in hosts:
            # 支持格式: user@host:port 或 user@host
            m = re.match(r"^([^@]+)@([^:]+)(?::(\d+))?$", spec)
            if m:
                server_list.append({"user": m.group(1), "host": m.group(2), "port": int(m.group(3) or 22)})
            else:
                print(warn(f"无法解析主机格式: {spec}，应为 user@host:port"))

    if hosts_file:
        if not os.path.exists(hosts_file):
            print(err(f"主机列表文件不存在: {hosts_file}"))
        else:
            with open(hosts_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    m = re.match(r"^([^@]+)@([^:]+)(?::(\d+))?$", line)
                    if m:
                        server_list.append({"user": m.group(1), "host": m.group(2), "port": int(m.group(3) or 22)})

    if not server_list:
        print(err("未提供任何主机，请通过 --hosts 或 --file 指定"))
        print(info("格式: user@host:port（端口可选，默认22）"))
        return

    print(f"  共 {len(server_list)} 台服务器\n")
    print(f"  {'主机':<30} {'状态':<8} {'延迟':>6}  {'系统信息'}")
    print(f"  {'─'*30} {'─'*8} {'─'*6}  {'─'*30}")

    results = {"ok": 0, "fail": 0, "warn": 0}

    for srv in server_list:
        addr = f"{srv['user']}@{srv['host']}"
        start = time.time()
        out, stderr, rc = _ssh_exec(srv["host"], srv["user"], srv["port"],
            "hostname && uptime -p 2>/dev/null || uptime && cat /proc/loadavg 2>/dev/null | awk '{print $1,$2,$3}'",
            timeout=10, key=key)
        elapsed = (time.time() - start) * 1000

        if rc != 0:
            print(f"  {addr:<30} {err('FAIL'):<18} {elapsed:.0f}ms  {stderr[:40]}")
            results["fail"] += 1
        else:
            info_text = out.splitlines()[1].strip() if len(out.splitlines()) > 1 else out.splitlines()[0].strip()
            print(f"  {addr:<30} {ok(' OK'):<18} {elapsed:.0f}ms  {info_text[:40]}")
            results["ok"] += 1

    ok_count = results["ok"]
    fail_count = results["fail"]
    total_count = len(server_list)
    print(f"\n  {bold('汇总')}: {ok(f'正常 {ok_count}')}, {err(f'失败 {fail_count}')}, 共 {total_count} 台")

    if results["fail"] > 0:
        print(warn(f"  {results['fail']} 台服务器连接异常，请检查网络和SSH配置"))

# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────

def main():
    if sys.platform == "win32":
        os.system("")

    parser = argparse.ArgumentParser(description="IT运维工具箱 - 系统监控")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # 本地监控命令
    sub.add_parser("info",  help="系统信息概览")
    sub.add_parser("cpu",   help="CPU使用率")
    sub.add_parser("mem",   help="内存使用情况")
    sub.add_parser("disk",  help="磁盘使用情况")
    p = sub.add_parser("top",   help="Top进程列表")
    p.add_argument("-n", type=int, default=15)
    p.add_argument("--sort", choices=["cpu","mem"], default="cpu")
    sub.add_parser("netif", help="网络接口信息")
    sub.add_parser("full",  help="全面系统扫描")

    # 远程监控命令
    p = sub.add_parser("remote",    help="远程服务器全面监控")
    p.add_argument("host",       help="远程主机地址 (user@host:port 或 user@host)")
    p.add_argument("-k", "--key",  default=None, help="SSH 私钥文件路径")

    p = sub.add_parser("rinfo",     help="远程系统信息")
    p.add_argument("host",       help="远程主机地址")
    p.add_argument("-k", "--key",  default=None, help="SSH 私钥文件路径")

    p = sub.add_parser("rcpu",      help="远程CPU监控")
    p.add_argument("host",       help="远程主机地址")
    p.add_argument("-k", "--key",  default=None, help="SSH 私钥文件路径")

    p = sub.add_parser("rmem",      help="远程内存监控")
    p.add_argument("host",       help="远程主机地址")
    p.add_argument("-k", "--key",  default=None, help="SSH 私钥文件路径")

    p = sub.add_parser("rdisk",     help="远程磁盘监控")
    p.add_argument("host",       help="远程主机地址")
    p.add_argument("-k", "--key",  default=None, help="SSH 私钥文件路径")

    p = sub.add_parser("rtop",      help="远程Top进程")
    p.add_argument("host",       help="远程主机地址")
    p.add_argument("-n", type=int, default=10)
    p.add_argument("--sort", choices=["cpu","mem"], default="cpu")
    p.add_argument("-k", "--key",  default=None, help="SSH 私钥文件路径")

    p = sub.add_parser("rnetif",    help="远程网络接口")
    p.add_argument("host",       help="远程主机地址")
    p.add_argument("-k", "--key",  default=None, help="SSH 私钥文件路径")

    p = sub.add_parser("rdocker",   help="远程Docker容器状态")
    p.add_argument("host",       help="远程主机地址")
    p.add_argument("-k", "--key",  default=None, help="SSH 私钥文件路径")

    p = sub.add_parser("batch",     help="批量服务器健康检查")
    p.add_argument("--hosts", nargs="+", default=None, help="主机列表 (user@host:port)")
    p.add_argument("--file",  default=None, help="主机列表文件路径（每行一台）")
    p.add_argument("-k", "--key",   default=None, help="SSH 私钥文件路径")

    args = parser.parse_args()

    def parse_host(spec):
        """解析 user@host:port 格式"""
        m = re.match(r"^([^@]+)@([^:]+)(?::(\d+))?$", spec)
        if not m:
            print(err(f"主机格式错误: {spec}，应为 user@host:port"))
            sys.exit(1)
        return m.group(2), m.group(1), int(m.group(3) or 22)

    def get_key():
        return getattr(args, "key", None)

    def do_remote(fn):
        h, u, p = parse_host(args.host)
        fn(h, u, p, get_key())

    dispatch = {
        "info":   cmd_sysinfo,
        "cpu":    cmd_cpu,
        "mem":    cmd_mem,
        "disk":   cmd_disk,
        "top":    lambda: cmd_top(args.n, args.sort) if hasattr(args, "n") else cmd_top(),
        "netif":  cmd_netif,
        "full":   cmd_full,
        # 远程命令
        "remote": lambda: do_remote(cmd_remote_full),
        "rinfo":  lambda: do_remote(_remote_sysinfo),
        "rcpu":   lambda: do_remote(_remote_cpu),
        "rmem":   lambda: do_remote(_remote_mem),
        "rdisk":  lambda: do_remote(_remote_disk),
        "rtop":   lambda: (lambda: (
            (lambda h, u, p: _remote_top(h, u, p, args.n, args.sort, get_key()))
            (*parse_host(args.host))
        ))(),
        "rnetif": lambda: do_remote(_remote_netif),
        "rdocker":lambda: do_remote(_remote_docker),
        "batch":  lambda: cmd_remote_batch(hosts_file=args.file, hosts=args.hosts, key=get_key()),
    }
    dispatch[args.cmd]()

if __name__ == "__main__":
    main()
