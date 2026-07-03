#!/usr/bin/env python3
"""
IT运维工具箱 - 监控问题排查模块
功能:
  - 日志关键词/错误扫描（支持正则）
  - 系统异常检测（OOM、磁盘慢、CPU飙升历史）
  - 进程崩溃/重启检测
  - 网络连接异常排查
  - 性能瓶颈快速定位
  - 视频监控播放问题排查
  - 视频取流测试（RTSP/HTTP-FLV/HLS/RTMP）
  - 综合问题巡检报告
用法: python troubleshoot.py <command> [args...]
"""

import sys
import os
import re
import subprocess
import socket
import time
import json
import argparse
import glob
import urllib.request
import urllib.error
import base64
from datetime import datetime, timedelta
from collections import Counter, defaultdict

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
def dim(msg):   return color(msg, "2")

def section(title):
    print(f"\n{bold('═' * 60)}")
    print(f"  {bold(title)}")
    print(bold('═' * 60))

IS_WIN   = sys.platform == "win32"
IS_LINUX = sys.platform == "linux"
IS_MAC   = sys.platform == "darwin"

def run(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           shell=isinstance(cmd, str), errors="replace")
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", -1
    except Exception as e:
        return "", str(e), -1

# ─────────────────────────────────────────────
# 日志扫描
# ─────────────────────────────────────────────

# 常见错误模式
ERROR_PATTERNS = [
    (re.compile(r"error|exception|traceback|panic|fatal|critical", re.I), "错误/异常", "31"),
    (re.compile(r"warn(?:ing)?|deprecated", re.I),                       "警告",      "33"),
    (re.compile(r"out of memory|oom|killed process|oom-killer", re.I),   "内存不足",  "31"),
    (re.compile(r"disk full|no space left|disk quota", re.I),            "磁盘满",    "31"),
    (re.compile(r"connection refused|connection reset|timeout", re.I),   "连接异常",  "33"),
    (re.compile(r"authentication fail|permission denied|access denied", re.I), "认证/权限失败", "33"),
    (re.compile(r"segfault|segmentation fault|core dump", re.I),         "程序崩溃",  "31"),
    (re.compile(r"deadlock|lock wait timeout", re.I),                    "死锁/锁超时","33"),
]

def cmd_logscan(filepath, pattern=None, tail_lines=None, context=2):
    section(f"日志扫描: {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(err(f"文件不存在: {filepath}"))
        return
    except PermissionError:
        print(err(f"无权读取: {filepath}"))
        return

    if tail_lines:
        lines = lines[-tail_lines:]
        print(info(f"扫描最后 {tail_lines} 行，共 {len(lines)} 行"))
    else:
        print(info(f"共 {len(lines)} 行"))

    # 自定义pattern
    if pattern:
        rx = re.compile(pattern, re.I)
        matches = [(i, line.rstrip()) for i, line in enumerate(lines) if rx.search(line)]
        print(f"\n  {bold(f'匹配 [{pattern}] 的行: {len(matches)} 处')}")
        for idx, (lineno, text) in enumerate(matches[:100]):
            # 上下文
            start = max(0, lineno - context)
            end   = min(len(lines), lineno + context + 1)
            if idx > 0 and lineno - matches[idx-1][0] > context * 2 + 1:
                print(f"  {dim('  ─' * 10)}")
            for ci in range(start, end):
                prefix = color(f">{lineno+1:6}|", "33") if ci == lineno else f" {ci+1:6}|"
                print(f"  {prefix} {lines[ci].rstrip()}")
        if len(matches) > 100:
            print(warn(f"... 仅显示前100处，共 {len(matches)} 处"))
        return

    # 内置错误模式扫描
    stats = defaultdict(list)
    for i, line in enumerate(lines):
        for rx, label, _ in ERROR_PATTERNS:
            if rx.search(line):
                stats[label].append((i+1, line.rstrip()))
                break

    if not stats:
        print(ok("未发现明显错误/警告"))
        return

    for label, items in stats.items():
        c_code = next((c for rx, l, c in ERROR_PATTERNS if l == label), "33")
        print(f"\n  {color(f'[{label}]', c_code)} — {len(items)} 处")
        for lineno, text in items[:10]:
            # 截断过长行
            display = text[:120] + ("..." if len(text) > 120 else "")
            print(f"    {dim(f'L{lineno:>5}')}  {display}")
        if len(items) > 10:
            print(f"    {dim(f'... 仅显示前10条，共 {len(items)} 条')}")

    total = sum(len(v) for v in stats.values())
    print(f"\n  {warn(f'共发现 {total} 处异常/警告')}")

# ─────────────────────────────────────────────
# OOM (内存不足) 检测
# ─────────────────────────────────────────────

def cmd_oom():
    section("OOM (内存不足) 检测")
    if IS_WIN:
        # 查看系统事件日志中的内存不足事件
        out, _, _ = run("powershell -Command \"Get-EventLog -LogName System -Newest 200 | Where-Object {$_.Message -like '*memory*' -or $_.Message -like '*低内存*'} | Select-Object TimeGenerated,EntryType,Message | Format-List\"")
        if out:
            print(out)
        else:
            print(ok("近期系统日志中无内存相关告警"))
        return

    if IS_LINUX:
        # 从 dmesg 查 oom-killer
        out, _, rc = run("dmesg -T --level=err,crit,alert,emerg 2>/dev/null | grep -i oom | tail -30")
        if rc == 0 and out:
            print(f"  {err('发现 OOM Kill 记录:')}")
            for line in out.splitlines():
                print(f"  {line}")
        else:
            print(ok("dmesg 中未发现 OOM Kill 记录"))

        # syslog
        syslog_paths = ["/var/log/syslog", "/var/log/messages", "/var/log/kern.log"]
        for path in syslog_paths:
            if os.path.exists(path):
                out2, _, _ = run(f"grep -i 'oom\\|out of memory\\|oom-killer' {path} | tail -20")
                if out2:
                    print(f"\n  {warn(f'{path} 中的 OOM 记录:')}")
                    print(out2)
                break

# ─────────────────────────────────────────────
# 进程崩溃/重启检测
# ─────────────────────────────────────────────

def cmd_crashes():
    section("进程崩溃/重启检测")
    if IS_LINUX:
        # Systemd 服务失败记录
        out, _, _ = run("systemctl list-units --state=failed --no-legend --no-pager")
        if out:
            print(f"  {err('Systemd 失败的服务:')}")
            for line in out.splitlines():
                print(f"    {line}")
        else:
            print(ok("无 Systemd 服务失败"))

        # journalctl 崩溃记录
        out2, _, _ = run("journalctl -p err -n 50 --no-pager --output=short-iso 2>/dev/null")
        if out2:
            print(f"\n  {warn('最近50条错误级别日志:')}")
            for line in out2.splitlines()[:20]:
                print(f"  {line}")
            if out2.count("\n") > 20:
                print(dim("  ... (截断)"))

        # coredump
        out3, _, _ = run("coredumpctl list 2>/dev/null | tail -10")
        if out3 and "No coredumps" not in out3:
            print(f"\n  {err('Core Dump 记录:')}")
            print(out3)

    elif IS_WIN:
        # 查看应用程序错误事件
        out, _, _ = run("powershell -Command \"Get-EventLog -LogName Application -EntryType Error -Newest 20 | Select-Object TimeGenerated,Source,Message | Format-Table -AutoSize\"")
        if out:
            print(out)
        else:
            print(ok("近期无应用程序错误事件"))

# ─────────────────────────────────────────────
# 网络连接异常排查
# ─────────────────────────────────────────────

def cmd_netcheck():
    section("网络连接异常排查")

    # TCP 连接统计
    if IS_WIN:
        out, _, _ = run("powershell -Command \"netstat -ano | Select-String 'ESTABLISHED|TIME_WAIT|CLOSE_WAIT' | Measure-Object | Select-Object Count\"")
        out2, _, _ = run("netstat -ano | findstr ESTABLISHED")
    elif IS_LINUX:
        out2, _, _ = run("ss -tnp")
    else:
        out2, _, _ = run("netstat -tnp")

    if out2:
        lines = out2.splitlines()
        states = Counter()
        for line in lines:
            for state in ["ESTABLISHED","TIME_WAIT","CLOSE_WAIT","SYN_SENT","FIN_WAIT"]:
                if state in line:
                    states[state] += 1
                    break

        print(f"  {bold('TCP 连接状态统计:')}")
        for state, count in sorted(states.items(), key=lambda x: -x[1]):
            icon = ok if state == "ESTABLISHED" else (warn if state in ("TIME_WAIT","FIN_WAIT") else err)
            print(f"    {icon(state):<30} {count}")

        # CLOSE_WAIT 过多警告
        if states.get("CLOSE_WAIT", 0) > 50:
            print(warn(f"\n  CLOSE_WAIT 连接数 {states['CLOSE_WAIT']} 过多，可能存在连接泄漏（服务端未关闭连接）"))
        if states.get("TIME_WAIT", 0) > 500:
            print(warn(f"\n  TIME_WAIT 连接数 {states['TIME_WAIT']} 过多，考虑调整 tcp_fin_timeout 或启用 tcp_tw_reuse"))

    # DNS 解析测试
    print(f"\n  {bold('DNS 解析测试:')}")
    test_hosts = ["8.8.8.8", "114.114.114.114"]
    for host in test_hosts:
        try:
            start = time.time()
            socket.gethostbyaddr(host)
            elapsed = (time.time() - start) * 1000
            print(f"    {ok(host)} 响应 {elapsed:.1f}ms")
        except Exception:
            print(f"    {warn(host)} 反向解析失败（正常）")

    # 公网连通性
    print(f"\n  {bold('公网连通性检测:')}")
    targets = [("8.8.8.8", 53, "Google DNS"), ("114.114.114.114", 53, "阿里DNS"), ("1.1.1.1", 53, "Cloudflare")]
    for host, port, label in targets:
        try:
            start = time.time()
            sock = socket.create_connection((host, port), timeout=3)
            elapsed = (time.time() - start) * 1000
            sock.close()
            print(f"    {ok(label)}: {host}:{port}  {elapsed:.1f}ms")
        except Exception as e:
            print(f"    {err(label)}: {host}:{port}  {e}")

# ─────────────────────────────────────────────
# 性能瓶颈快速定位
# ─────────────────────────────────────────────

def cmd_perf():
    section("性能瓶颈快速定位")

    issues = []

    # ── CPU ──
    print(f"  {bold('[CPU]')}")
    if IS_WIN:
        out, _, _ = run("powershell -Command \"(Get-WmiObject -Class Win32_Processor).LoadPercentage\"")
        try:
            cpu_pct = float(out.strip())
        except Exception:
            cpu_pct = -1
    elif IS_LINUX:
        out, _, _ = run("top -bn1 | grep 'Cpu(s)'")
        m = re.search(r"(\d+\.?\d*)\s+id", out)
        cpu_pct = 100.0 - float(m.group(1)) if m else -1
    else:
        out, _, _ = run("top -l 1 | grep 'CPU usage'")
        m = re.search(r"(\d+\.?\d*)% user.*?(\d+\.?\d*)% sys", out)
        cpu_pct = float(m.group(1)) + float(m.group(2)) if m else -1

    if cpu_pct >= 0:
        bar = "█" * int(cpu_pct/5) + "░" * (20 - int(cpu_pct/5))
        icon = ok if cpu_pct < 70 else (warn if cpu_pct < 85 else err)
        print(f"    使用率: {icon(f'{cpu_pct:.1f}%')} [{bar}]")
        if cpu_pct > 85:
            issues.append(f"CPU使用率过高 ({cpu_pct:.1f}%)")
            # Top CPU进程
            if IS_WIN:
                out2, _, _ = run("powershell -Command \"Get-Process | Sort-Object CPU -Descending | Select-Object -First 5 Name,CPU | Format-Table\"")
            elif IS_LINUX:
                out2, _, _ = run("ps aux --sort=-%cpu | head -6")
            else:
                out2, _, _ = run("ps aux | sort -rk3 | head -6")
            print(f"    {warn('高CPU进程:')}")
            for line in out2.splitlines()[1:6]:
                print(f"      {line}")

    # ── 内存 ──
    print(f"\n  {bold('[内存]')}")
    if IS_WIN:
        out, _, _ = run("powershell -Command \"$os=Get-WmiObject Win32_OperatingSystem; [math]::Round(($os.TotalVisibleMemorySize-$os.FreePhysicalMemory)/$os.TotalVisibleMemorySize*100,1)\"")
        try: mem_pct = float(out.strip())
        except: mem_pct = -1
    elif IS_LINUX:
        out, _, _ = run("free | grep Mem")
        parts = out.split()
        if len(parts) >= 3:
            total, used = int(parts[1]), int(parts[2])
            mem_pct = used / total * 100
        else:
            mem_pct = -1
    else:
        mem_pct = -1

    if mem_pct >= 0:
        bar = "█" * int(mem_pct/5) + "░" * (20 - int(mem_pct/5))
        icon = ok if mem_pct < 75 else (warn if mem_pct < 90 else err)
        print(f"    使用率: {icon(f'{mem_pct:.1f}%')} [{bar}]")
        if mem_pct > 90:
            issues.append(f"内存不足 ({mem_pct:.1f}%)")

    # ── 磁盘 I/O ──
    print(f"\n  {bold('[磁盘]')}")
    if IS_LINUX:
        out, _, _ = run("iostat -x 1 2 2>/dev/null | tail -n +$(iostat -x 1 2 2>/dev/null | grep -n 'Device' | tail -1 | cut -d: -f1) | grep -v '^$\\|Device'")
        if out:
            print(f"    磁盘I/O等待:")
            for line in out.splitlines()[:5]:
                parts = line.split()
                if len(parts) > 10:
                    await_ms = parts[9] if len(parts) > 9 else "N/A"
                    util_pct = parts[-1] if parts else "N/A"
                    dev = parts[0]
                    try:
                        util = float(util_pct)
                        icon = ok if util < 70 else (warn if util < 90 else err)
                        print(f"      {dev:<12} await={await_ms}ms  util={icon(f'{util:.1f}%')}")
                        if util > 90:
                            issues.append(f"磁盘 {dev} I/O 过高 ({util:.1f}%)")
                    except Exception:
                        print(f"      {line}")
        else:
            out2, _, _ = run("df -h / | tail -1")
            print(f"    根分区: {out2}")
    else:
        out, _, _ = run("powershell -Command \"Get-PSDrive -PSProvider FileSystem | Where-Object {$_.Used} | Select-Object Name,@{n='Pct';e={[math]::Round($_.Used/($_.Used+$_.Free)*100,1)}} | Format-Table\"" if IS_WIN else "df -h")
        print(f"    {out.splitlines()[0] if out else 'N/A'}")

    # ── 总结 ──
    print(f"\n  {bold('── 问题汇总 ──')}")
    if issues:
        for issue in issues:
            print(f"  {err('！')} {issue}")
        print(f"\n  {warn(f'发现 {len(issues)} 个性能问题，请优先处理上述项目')}")
    else:
        print(f"  {ok('未发现明显性能瓶颈，系统运行正常')}")

# ─────────────────────────────────────────────
# 综合巡检报告
# ─────────────────────────────────────────────

def cmd_inspect():
    section("🔍 综合运维巡检报告")
    print(f"  生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  主机名  : {__import__('socket').gethostname()}")

    cmd_perf()
    cmd_netcheck()
    cmd_oom()
    cmd_crashes()

    print(f"\n{bold('═' * 60)}")
    print(f"  {ok('巡检完成')}")
    print(bold('═' * 60))

# ─────────────────────────────────────────────
# 视频监控播放问题排查
# ─────────────────────────────────────────────

def cmd_video(url=None, rtsp_url=None):
    """
    视频监控不能播放问题排查
    检测项：网络连通性、DNS解析、端口、RTSP/HTTP流可用性、流媒体协议握手
    支持输入 URL 或 rtsp:// 地址
    """
    section("视频监控播放问题排查")

    # 确定检测目标
    target_url = url or rtsp_url
    if not target_url:
        print(warn("请提供监控地址，例如:"))
        print("  python troubleshoot.py video --url http://192.168.1.100:8080/video")
        print("  python troubleshoot.py video --rtsp rtsp://admin:pass@192.168.1.100:554/stream")
        return

    parsed = _parse_url(target_url)
    if not parsed:
        print(err(f"无法解析地址: {target_url}"))
        return

    scheme   = parsed["scheme"]
    host     = parsed["host"]
    port     = parsed["port"]
    path     = parsed["path"]
    username = parsed["username"]

    print(f"  协议     : {scheme}")
    print(f"  目标主机 : {host}")
    print(f"  端口     : {port}")
    if path:
        print(f"  路径     : {path}")
    if username:
        print(f"  用户名   : {username}")

    issues = []
    passed = []

    # ── 1. DNS 解析 ──
    print(f"\n  {bold('[1/6] DNS 解析')}")
    try:
        ips = socket.getaddrinfo(host, None)
        resolved = sorted(set(r[4][0] for r in ips if ":" not in r[4][0]))
        if resolved:
            print(f"    {ok(f'解析成功: {', '.join(resolved)}')}")
            passed.append("DNS解析")
        else:
            print(f"    {warn('解析结果为空')}")
            issues.append("DNS解析异常")
    except socket.gaierror as e:
        print(f"    {err(f'DNS解析失败: {e}')}")
        issues.append("DNS解析失败 - 检查域名是否正确或使用IP直接访问")

    # ── 2. 网络连通性 (Ping) ──
    print(f"\n  {bold('[2/6] 网络连通性 (Ping)')}")
    if sys.platform == "win32":
        cmd = ["ping", "-n", "3", "-w", "2000", host]
    else:
        cmd = ["ping", "-c", "3", "-W", "2", host]
    out, _, rc = run(cmd)
    if rc == 0:
        # 提取延迟
        latency = _extract_ping_latency(out)
        if latency is not None:
            icon = ok if latency < 50 else (warn if latency < 200 else err)
            print(f"    {icon(f'Ping 通，延迟 {latency:.1f}ms')}")
            if latency > 200:
                issues.append(f"网络延迟较高 ({latency:.1f}ms)，可能导致视频卡顿")
            passed.append("Ping连通")
        else:
            print(f"    {ok('Ping 通')}")
            passed.append("Ping连通")
    else:
        print(f"    {err('Ping 不通 - 目标主机不可达')}")
        issues.append("目标主机不可达 - 检查IP地址、网络连接、防火墙")

    # ── 3. 端口可达性 ──
    print(f"\n  {bold('[3/6] 端口可达性')}")
    try:
        start = time.time()
        sock = socket.create_connection((host, port), timeout=5)
        elapsed = (time.time() - start) * 1000
        sock.close()
        print(f"    {ok(f'端口 {port} 开放，连接耗时 {elapsed:.1f}ms')}")
        passed.append(f"端口{port}")
    except socket.timeout:
        print(f"    {err(f'端口 {port} 连接超时 - 服务未启动或被防火墙阻止')}")
        issues.append(f"端口{port}不可达 - 检查监控服务是否启动、防火墙规则")
    except ConnectionRefusedError:
        print(f"    {err(f'端口 {port} 连接被拒绝 - 服务未监听此端口')}")
        issues.append(f"端口{port}被拒绝 - 监控服务未启动或未监听此端口")
    except OSError as e:
        print(f"    {err(f'端口 {port} 连接失败: {e}')}")
        issues.append(f"端口{port}连接失败: {e}")

    # ── 4. 协议层检测 ──
    print(f"\n  {bold('[4/6] 协议层检测')}")
    if scheme in ("rtsp", "rtsps"):
        _check_rtsp(host, port, path, username, parsed.get("password"), issues, passed)
    elif scheme in ("http", "https"):
        _check_http_stream(host, port, path, scheme, issues, passed)
    elif scheme in ("rtmp", "rtmps"):
        _check_rtmp(host, port, issues, passed)
    elif scheme in ("hls", "m3u8") or (path and (".m3u8" in path or "m3u8" in target_url)):
        _check_hls(host, port, path, scheme, issues, passed)
    elif scheme in ("onvif",):
        _check_onvif(host, port, issues, passed)
    else:
        # 尝试多种协议探测
        print(f"    {info('未指定协议，尝试探测常见监控端口...')}")
        _probe_common_ports(host, issues, passed)

    # ── 5. 带宽估算 ──
    print(f"\n  {bold('[5/6] 带宽/延迟评估')}")
    _check_bandwidth(host, issues)

    # ── 6. 常见问题对照 ──
    print(f"\n  {bold('[6/6] 常见问题对照')}")
    _print_video_troubleshooting_tips(issues)

    # ── 汇总 ──
    print(f"\n  {bold('── 排查结果汇总 ──')}")
    if issues:
        print(f"  {err(f'发现 {len(issues)} 个问题:')}")
        for i, issue in enumerate(issues, 1):
            print(f"    {i}. {err(issue)}")
    else:
        print(f"  {ok('未发现网络层面问题，视频无法播放可能的原因:')}")

    if passed:
        print(f"\n  {ok(f'通过项 ({len(passed)})')}: {', '.join(passed)}")

    if not issues:
        print(f"\n  {info('网络层面正常，建议检查:')}")
        print(f"    1. 浏览器/播放器是否支持该视频编码格式（H.264/H.265）")
        print(f"    2. 监控摄像头是否正常供电、镜头是否被遮挡")
        print(f"    3. 播放地址是否正确（路径、通道号）")
        print(f"    4. 监控设备的最大连接数是否已达上限")
        print(f"    5. 如果是 HTTPS，检查证书是否受信任")


def _parse_url(url):
    """解析 URL，支持 rtsp://user:pass@host:port/path 格式"""
    m = re.match(r"^(rtsp|rtsps|rtmp|rtmps|http|https|hls|onvif|m3u8)://"
                 r"(?:([^:]+)(?::([^@]+))?@)?"    # user:pass@
                 r"([^/:]+)"                       # host
                 r"(?::(\d+))?"                    # :port
                 r"(/.*)?$", url, re.I)
    if not m:
        return None
    scheme = m.group(1).lower()
    port_str = m.group(5)
    # 默认端口
    default_ports = {
        "rtsp": 554, "rtsps": 322, "rtmp": 1935, "rtmps": 1935,
        "http": 80, "https": 443, "hls": 80, "onvif": 80, "m3u8": 80,
    }
    return {
        "scheme": scheme,
        "username": m.group(2),
        "password": m.group(3),
        "host": m.group(4),
        "port": int(port_str) if port_str else default_ports.get(scheme, 80),
        "path": m.group(6) or "/",
    }


def _extract_ping_latency(output):
    """从 ping 输出中提取平均延迟"""
    # Windows: "平均 = 12ms" or "Minimum = 1ms, Maximum = 2ms, Average = 1ms"
    m = re.search(r"[Aa]verage[ =：]+(\d+)ms", output)
    if m:
        return float(m.group(1))
    # Linux: "rtt min/avg/max/mdev = 1.234/5.678/9.012/1.234 ms"
    m = re.search(r"rtt min/avg/max/mdev = [\d.]+/([\d.]+)", output)
    if m:
        return float(m.group(1))
    # Linux: "time=12.3 ms"
    m = re.search(r"time=([\d.]+)\s*ms", output)
    if m:
        return float(m.group(1))
    return None


def _check_rtsp(host, port, path, username, password, issues, passed):
    """RTSP 协议检测（发送 OPTIONS 请求）"""
    try:
        sock = socket.create_connection((host, port), timeout=5)
        # RTSP OPTIONS 请求
        request = f"OPTIONS rtsp://{host}{path} RTSP/1.0\r\n"
        request += f"CSeq: 1\r\n"
        request += f"User-Agent: WorkBuddy-OpsToolkit/1.0\r\n"
        if username:
            import base64
            cred = f"{username}:{password or ''}"
            b64 = base64.b64encode(cred.encode()).decode()
            request += f"Authorization: Basic {b64}\r\n"
        request += "\r\n"

        sock.sendall(request.encode())
        resp = b""
        sock.settimeout(5)
        try:
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                resp += chunk
                if b"\r\n\r\n" in resp:
                    break
        except socket.timeout:
            pass
        sock.close()

        resp_str = resp.decode("utf-8", errors="replace")
        first_line = resp_str.splitlines()[0] if resp_str.splitlines() else ""

        if "RTSP/1." in first_line:
            status_code = re.search(r"(\d{3})", first_line)
            if status_code:
                code = int(status_code.group(1))
                if code == 200:
                    # 解析支持的 methods
                    public = ""
                    for line in resp_str.splitlines():
                        if line.lower().startswith("public:"):
                            public = line.split(":", 1)[1].strip()
                            break
                    print(f"    {ok(f'RTSP 服务响应正常 (200)')}")
                    if public:
                        print(f"    {info(f'支持方法: {public}')}")
                    passed.append("RTSP协议")
                elif code == 401:
                    print(f"    {warn('RTSP 需要认证 (401) - 检查用户名密码')}")
                    issues.append("RTSP认证失败 - 用户名或密码错误")
                elif code == 404:
                    print(f"    {err('RTSP 通道不存在 (404) - 检查路径/通道号')}")
                    issues.append("RTSP路径错误 - 通道号或流路径不存在")
                elif code == 461:
                    print(f"    {err('RTSP 不支持请求方法 (461)')}")
                    issues.append("RTSP协议不兼容 - 摄像头不支持当前请求方法")
                else:
                    print(f"    {warn(f'RTSP 响应码: {code}')}")
                    issues.append(f"RTSP返回非200状态码: {code}")
        else:
            print(f"    {warn('收到响应但非标准RTSP协议')}")
            print(f"    {dim(f'响应头: {first_line[:100]}')}")
    except socket.timeout:
        print(f"    {err('RTSP 连接超时')}")
        issues.append("RTSP服务响应超时")
    except Exception as e:
        print(f"    {err(f'RTSP 检测失败: {e}')}")
        issues.append(f"RTSP检测异常: {e}")


def _check_http_stream(host, port, path, scheme, issues, passed):
    """HTTP/HTTPS 视频流检测"""
    try:
        url = f"{scheme}://{host}:{port}{path}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "WorkBuddy-OpsToolkit/1.0",
            "Range": "bytes=0-1023",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.status
            ct = resp.headers.get("Content-Type", "")
            cl = resp.headers.get("Content-Length", "")
            server = resp.headers.get("Server", "")

            print(f"    状态码     : {ok(str(code)) if code == 200 else warn(str(code))}")
            print(f"    Content-Type: {ct}")
            print(f"    Server     : {server}")

            # 判断是否为视频流
            stream_types = [
                "video/", "multipart/x-mixed-replace", "application/octet-stream",
                "application/mp4", "application/vnd.apple.mpegurl",
            ]
            is_stream = any(st in ct.lower() for st in stream_types)
            if is_stream:
                print(f"    {ok('检测到视频流响应')}")
                passed.append("HTTP视频流")
            elif "text/html" in ct.lower():
                print(f"    {warn('返回HTML页面而非视频流 - 地址可能不正确')}")
                issues.append("HTTP返回HTML而非视频流 - 播放地址/路径错误")
            elif code == 401:
                print(f"    {warn('需要认证 (401)')}")
                issues.append("HTTP认证失败 - 检查用户名密码或Token")
            elif code == 404:
                print(f"    {err('资源不存在 (404)')}")
                issues.append("视频流地址不存在 (404) - 检查路径和通道号")
            else:
                print(f"    {info(f'响应类型: {ct}')}")
                passed.append("HTTP连接")

    except urllib.error.HTTPError as e:
        print(f"    {err(f'HTTP 错误: {e.code} {e.reason}')}")
        if e.code == 401:
            issues.append("认证失败 - 用户名密码或Token不正确")
        elif e.code == 404:
            issues.append("视频地址不存在 (404)")
        else:
            issues.append(f"HTTP错误: {e.code}")
    except urllib.error.URLError as e:
        print(f"    {err(f'连接失败: {e.reason}')}")
        issues.append(f"HTTP连接失败: {e.reason}")
    except Exception as e:
        print(f"    {err(f'检测异常: {e}')}")


def _check_rtmp(host, port, issues, passed):
    """RTMP 协议检测（TCP握手检测）"""
    try:
        sock = socket.create_connection((host, port), timeout=5)
        print(f"    {ok(f'RTMP 端口 {port} 可连接')}")
        passed.append("RTMP端口")
        sock.close()
    except Exception as e:
        print(f"    {err(f'RTMP 连接失败: {e}')}")
        issues.append(f"RTMP连接失败: {e}")


def _check_hls(host, port, path, scheme, issues, passed):
    """HLS/m3u8 流检测"""
    try:
        url = f"https://{host}:{port}{path}" if scheme in ("hls", "https") else f"http://{host}:{port}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            if "#EXTM3U" in body or "#EXTINF" in body or "#EXT-X-" in body:
                print(f"    {ok('HLS m3u8 播放列表有效')}")
                # 解析 TS 分片数量
                ts_count = body.count("#EXTINF")
                print(f"    {info(f'分片数量: {ts_count}')}")
                if "#EXT-X-STREAM-INF" in body:
                    print(f"    {info('检测到多码率播放列表')}")
                passed.append("HLS流")
            else:
                print(f"    {warn('响应内容非标准m3u8格式')}")
                issues.append("m3u8文件格式异常")
    except Exception as e:
        print(f"    {err(f'HLS 检测失败: {e}')}")
        issues.append(f"HLS检测失败: {e}")


def _check_onvif(host, port, issues, passed):
    """ONVIF 协议检测"""
    try:
        url = f"http://{host}:{port}/onvif/device_service"
        req = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            print(f"    {ok(f'ONVIF 服务可用 (状态码: {resp.status})')}")
            passed.append("ONVIF服务")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print(f"    {warn('ONVIF 需要认证 (401)')}")
            issues.append("ONVIF认证失败")
        else:
            print(f"    {warn(f'ONVIF 响应: {e.code}')}")
    except Exception as e:
        print(f"    {info(f'ONVIF 服务不可用或非标准路径: {e}')}")


def _probe_common_ports(host, issues, passed):
    """探测常见监控端口"""
    probe_ports = {
        554: "RTSP",
        80: "HTTP-Web管理",
        443: "HTTPS-Web管理",
        8080: "HTTP-Alt",
        8443: "HTTPS-Alt",
        37777: "海康威视/DH-NVR",
        34567: "大华/DH-IPC",
        9000: "Hikvision-RTSP",
        8000: "通用HTTP监控",
        1935: "RTMP推流",
        8899: "海康RTSP备选",
    }
    print(f"    探测 {len(probe_ports)} 个常见监控端口...")
    found = []
    for port, label in probe_ports.items():
        try:
            sock = socket.create_connection((host, port), timeout=2)
            sock.close()
            found.append((port, label))
            print(f"    {ok(f'{port:5d}/tcp  OPEN  {label}')}")
        except Exception:
            pass

    if found:
        passed.append(f"发现{len(found)}个开放端口")
        print(f"\n    {info(f'发现 {len(found)} 个开放端口，以下为可能的访问方式:')}")
        for port, label in found:
            if port == 554:
                print(f"      RTSP:  rtsp://{host}:554/stream1")
            elif port == 37777:
                print(f"      海康:  http://{host}:{port}/ISAPI/Streaming/channels/101")
            elif port == 34567:
                print(f"      大华:  rtsp://{host}:554/cam/realmonitor?channel=1&subtype=0")
            elif port in (80, 8080):
                print(f"      Web:   http://{host}:{port}")
            elif port == 1935:
                print(f"      RTMP:  rtmp://{host}:1935/live/stream")
    else:
        print(f"    {warn('未发现常见监控端口开放')}")
        issues.append("常见监控端口均不可达 - 检查IP、网络和设备状态")


def _check_bandwidth(host, issues):
    """简单带宽评估（通过下载一小块数据估算）"""
    # 通过 TCP 连接延迟评估
    ports_to_try = [80, 443, 554, 8080, 37777, 34567, 9000, 8000]
    for port in ports_to_try:
        try:
            start = time.time()
            sock = socket.create_connection((host, port), timeout=3)
            elapsed = (time.time() - start) * 1000
            sock.close()
            print(f"    TCP连接延迟 ({port}): {elapsed:.1f}ms")
            if elapsed > 500:
                issues.append(f"连接延迟高 ({elapsed:.1f}ms)，视频可能卡顿")
            break
        except Exception:
            continue
    else:
        print(f"    {dim('所有常见端口不可达，无法评估延迟')}")


def _print_video_troubleshooting_tips(issues):
    """根据已发现问题，打印针对性排查建议"""
    has_network = any("不可达" in i or "不通" in i or "DNS" in i or "超时" in i for i in issues)
    has_auth    = any("认证" in i or "401" in i for i in issues)
    has_port    = any("端口" in i for i in issues)
    has_protocol= any("RTSP" in i or "HTTP" in i or "RTMP" in i for i in issues)

    print(f"\n  {bold('── 针对性排查建议 ──')}")

    if has_network:
        print(f"    {err('◆')} 网络问题:")
        print(f"       • 确认监控设备和本机在同一网络或VPN已连接")
        print(f"       • ping 目标IP，检查丢包率和延迟")
        print(f"       • 检查中间网络设备（交换机、路由器）")

    if has_port:
        print(f"    {err('◆')} 端口问题:")
        print(f"       • 确认监控服务已启动（NVR/DVR/IPC 在线）")
        print(f"       • 检查防火墙是否放行对应端口")
        print(f"       • 常用端口: RTSP=554, HTTP=80, 海康=37777, 大华=34567")

    if has_auth:
        print(f"    {warn('◆')} 认证问题:")
        print(f"       • 确认用户名密码正确（注意大小写）")
        print(f"       • 检查设备是否启用了IP白名单或MAC绑定")
        print(f"       • ONVIF设备可能需要单独开启ONVIF用户")

    if has_protocol:
        print(f"    {warn('◆')} 协议兼容问题:")
        print(f"       • RTSP: 确认路径正确（海康用 Streaming/channels，大华用 cam/realmonitor）")
        print(f"       • H.265编码需要播放器支持，尝试切换H.264")
        print(f"       • 部分设备需要先激活onvif/rtsp服务")

    if not issues:
        print(f"    {info('网络层正常，排查方向:')}")
        print(f"       • 检查视频编码是否被浏览器/播放器支持（H.265需Edge/Chrome最新版）")
        print(f"       • VLC播放器是最通用的测试工具，建议用VLC先验证流是否可用")
        print(f"       • 检查摄像头画面设置（分辨率、码率是否过高）")
        print(f"       • 确认设备最大并发连接数未超限")


# ─────────────────────────────────────────────
# 视频取流测试
# ─────────────────────────────────────────────

def cmd_stream(url=None, rtsp_url=None, duration=None):
    """
    视频取流测试：实际从摄像头拉取视频流并分析数据
    支持 RTSP / HTTP-FLV / HLS / RTMP 协议
    读取指定时长（默认5秒）的数据并分析码率、帧间隔等
    """
    section("视频取流测试")

    target_url = url or rtsp_url
    if not target_url:
        print(warn("请提供监控地址，例如:"))
        print("  python troubleshoot.py stream --rtsp rtsp://admin:pass@192.168.1.100:554/stream")
        print("  python troubleshoot.py stream --url http://192.168.1.100:8080/live/stream.flv")
        print("  python troubleshoot.py stream --url http://192.168.1.100:8080/live/stream.m3u8")
        print("  python troubleshoot.py stream --rtsp rtsp://admin:pass@192.168.1.100:554/stream --duration 10")
        return

    parsed = _parse_url(target_url)
    if not parsed:
        print(err(f"无法解析地址: {target_url}"))
        return

    scheme   = parsed["scheme"]
    host     = parsed["host"]
    port     = parsed["port"]
    path     = parsed["path"]
    username = parsed["username"]
    password = parsed.get("password")

    test_duration = duration if duration else 5

    print(f"  协议     : {scheme.upper()}")
    print(f"  目标地址 : {target_url}")
    print(f"  测试时长 : {test_duration} 秒")

    # ── 快速连通性检测 ──
    print(f"\n  {bold('[预检] 快速连通性')}")
    try:
        start = time.time()
        sock = socket.create_connection((host, port), timeout=5)
        elapsed = (time.time() - start) * 1000
        sock.close()
        print(f"    {ok(f'端口 {port} 可达 ({elapsed:.1f}ms)')}")
    except Exception as e:
        print(f"    {err(f'端口 {port} 不可达: {e}')}")
        print(f"    {warn('目标不可达，终止取流测试')}")
        return

    # ── 根据协议进行取流 ──
    print(f"\n  {bold('[取流] 开始拉取视频数据...')}")
    if scheme in ("rtsp", "rtsps"):
        _stream_rtsp(host, port, path, username, password, test_duration, target_url)
    elif scheme in ("http", "https"):
        # 根据路径后缀判断流类型
        if path.endswith(".flv"):
            _stream_http_flv(host, port, path, scheme, test_duration, target_url)
        elif path.endswith(".m3u8"):
            _stream_hls_test(host, port, path, scheme, test_duration, target_url)
        else:
            _stream_http_generic(host, port, path, scheme, test_duration, target_url)
    elif scheme in ("rtmp", "rtmps"):
        _stream_rtmp_test(host, port, test_duration, target_url)
    elif scheme in ("hls", "m3u8"):
        _stream_hls_test(host, port, path, "http", test_duration, target_url)
    else:
        print(f"    {warn(f'不支持的协议: {scheme}')}")
        print(f"    {info('支持: rtsp, http, https, rtmp, hls/m3u8')}")
        return


def _stream_rtsp(host, port, path, username, password, duration, full_url):
    """RTSP 取流测试：DESCRIBE + SETUP + PLAY，读取 RTP 数据"""
    issues = []
    try:
        sock = socket.create_connection((host, port), timeout=10)

        def _rtsp_request(method, extra_headers=""):
            """发送 RTSP 请求并返回响应"""
            req = f"{method} {full_url} RTSP/1.0\r\n"
            req += f"CSeq: 1\r\n"
            req += f"User-Agent: WorkBuddy-OpsToolkit/1.0\r\n"
            if username:
                cred = f"{username}:{password or ''}"
                b64 = base64.b64encode(cred.encode()).decode()
                req += f"Authorization: Basic {b64}\r\n"
            req += extra_headers
            req += "\r\n"
            sock.sendall(req.encode())
            time.sleep(0.5)

            resp = b""
            sock.settimeout(5)
            try:
                while True:
                    chunk = sock.recv(65536)
                    if not chunk:
                        break
                    resp += chunk
                    if b"\r\n\r\n" in resp:
                        # 只读取 header 部分，RTP 数据不等
                        break
            except socket.timeout:
                pass
            return resp.decode("utf-8", errors="replace")

        def _parse_rtsp_response(resp_str):
            """解析 RTSP 响应"""
            lines = resp_str.splitlines()
            headers = {}
            body_start = False
            body_lines = []
            first_line = lines[0] if lines else ""
            for line in lines[1:]:
                if body_start:
                    body_lines.append(line)
                    continue
                if line == "":
                    body_start = True
                    continue
                if ":" in line:
                    key, val = line.split(":", 1)
                    headers[key.strip().lower()] = val.strip()
            return first_line, headers, body_lines

        # Step 1: DESCRIBE
        print(f"    {info('DESCRIBE...')}")
        resp = _rtsp_request("DESCRIBE", "Accept: application/sdp\r\n")
        first_line, headers, body = _parse_rtsp_response(resp)

        if "200" not in first_line:
            if "401" in first_line:
                print(f"    {err('认证失败 (401) - 用户名或密码错误')}")
                sock.close()
                return
            elif "404" in first_line:
                print(f"    {err('流不存在 (404) - 检查路径/通道号')}")
                sock.close()
                return
            else:
                print(f"    {warn(f'DESCRIBE 返回: {first_line.strip()}')}")
                sock.close()
                return

        # 解析 SDP
        sdp_text = "\n".join(body)
        media_info = _parse_sdp(sdp_text)
        print(f"    {ok('DESCRIBE 成功 (200)')}")
        if media_info["video_codec"]:
            vc = media_info["video_codec"]
            print(f"    {info(f'视频编码: {vc}')}")
        if media_info["audio_codec"]:
            ac = media_info["audio_codec"]
            print(f"    {info(f'音频编码: {ac}')}")
        if media_info["resolution"]:
            res = media_info["resolution"]
            print(f"    {info(f'分辨率  : {res}')}")
        if media_info["control"]:
            ctrl = media_info["control"]
            print(f"    {info(f'媒体控制: {ctrl}')}")

        # Step 2: SETUP
        print(f"    {info('SETUP...')}")
        track_url = media_info.get("track_url", full_url + "/trackID=1")
        transport = "RTP/AVP;unicast;client_port=50000-50001"
        setup_resp = _rtsp_request("SETUP", f"Transport: {transport}\r\n")
        s_first, s_headers, _ = _parse_rtsp_response(setup_resp)

        if "200" not in s_first:
            print(f"    {err(f'SETUP 失败: {s_first.strip()}')}")
            sock.close()
            return

        session = s_headers.get("session", "").split(";")[0]
        transport_info = s_headers.get("transport", "")
        server_port = ""
        m = re.search(r"server_port=(\d+)-(\d+)", transport_info)
        if m:
            server_port = f"{m.group(1)}-{m.group(2)}"
        print(f"    {ok('SETUP 成功 (200)')}  Session: {session}")
        if server_port:
            print(f"    {info(f'服务端口: {server_port}')}")

        # Step 3: PLAY
        print(f"    {info('PLAY...')}")
        play_resp = _rtsp_request("PLAY", f"Session: {session}\r\nRange: npt=0.000-\r\n")
        p_first, p_headers, _ = _parse_rtsp_response(play_resp)

        if "200" not in p_first:
            print(f"    {err(f'PLAY 失败: {p_first.strip()}')}")
            sock.close()
            return

        # 获取 RTP-Info 中的 seq 和 clock
        rtp_info = p_headers.get("rtp-info", "")
        print(f"    {ok('PLAY 成功 (200) - 开始接收数据')}")

        # 读取数据流
        print(f"\n  {bold(f'[接收] 读取 {duration} 秒数据流...')}")
        total_bytes = 0
        packets = 0
        first_data_time = None
        last_data_time = None
        start_time = time.time()

        # 切换到数据接收模式，使用更大的超时
        sock.settimeout(3)
        while time.time() - start_time < duration:
            try:
                data = sock.recv(32768)
                if not data:
                    print(f"    {warn('连接已关闭')}")
                    break
                total_bytes += len(data)
                packets += 1
                now = time.time()
                if first_data_time is None:
                    first_data_time = now
                last_data_time = now
            except socket.timeout:
                if total_bytes == 0:
                    print(f"    {err('等待数据超时，无数据返回')}")
                    issues.append("RTSP PLAY 后无数据返回 - 流可能未正确建立")
                    break
                # 有数据的情况下超时可能是正常间隔
                continue
            except Exception as e:
                print(f"    {warn(f'读取异常: {e}')}")
                break

        sock.close()

        # 统计结果
        elapsed_real = last_data_time - first_data_time if first_data_time and last_data_time else 0
        _print_stream_stats(total_bytes, packets, elapsed_real, duration, issues, "RTSP")

    except socket.timeout:
        print(f"    {err('连接超时')}")
    except ConnectionRefusedError:
        print(f"    {err('连接被拒绝 - 服务未运行')}")
    except Exception as e:
        print(f"    {err(f'取流异常: {e}')}")


def _parse_sdp(sdp_text):
    """解析 SDP 内容提取媒体信息"""
    info = {
        "video_codec": "",
        "audio_codec": "",
        "resolution": "",
        "control": "",
        "track_url": "",
    }

    lines = sdp_text.strip().splitlines()
    in_video = False
    in_audio = False

    for line in lines:
        line = line.strip()
        if line.startswith("m=video"):
            in_video = True
            in_audio = False
            parts = line.split()
            # m=video 0 RTP/AVP 96
            info["video_codec"] = "RTP Payload: " + parts[-1] if len(parts) >= 4 else "unknown"
        elif line.startswith("m=audio"):
            in_audio = True
            in_video = False
            parts = line.split()
            info["audio_codec"] = "RTP Payload: " + parts[-1] if len(parts) >= 4 else "unknown"
        elif line.startswith("a=rtpmap:"):
            parts = line.split()
            if len(parts) >= 2:
                codec_name = parts[1]
                if in_video:
                    info["video_codec"] = codec_name.upper()
                elif in_audio:
                    info["audio_codec"] = codec_name.upper()
        elif line.startswith("a=control:"):
            ctrl = line.split(":", 1)[1].strip()
            if in_video and ctrl:
                info["track_url"] = ctrl
            info["control"] = ctrl
        elif line.startswith("a=fmtp:"):
            # 解析分辨率等参数 (H.264: sprop-parameter-sets 或 profile-level-id)
            fmtp = line
            if "sprop-parameter-sets" in fmtp.lower() or "profile-level-id" in fmtp.lower():
                if in_video and info["video_codec"]:
                    info["video_codec"] += " (H.264)"
        elif line.startswith("a=framesize:"):
            # a=framesize:96 1920-1080
            m = re.search(r"(\d+)-(\d+)", line)
            if m:
                info["resolution"] = f"{m.group(1)}x{m.group(2)}"

    # 更友好的编码名
    def _friendly_codec(raw):
        raw = raw.upper()
        if "H264" in raw or "H.264" in raw:
            return "H.264/AVC"
        if "H265" in raw or "H.265" in raw or "HEVC" in raw:
            return "H.265/HEVC"
        if "JPEG" in raw or "MJPG" in raw:
            return "MJPEG"
        if "AAC" in raw:
            return "AAC"
        if "PCMU" in raw or "G711" in raw:
            return "G.711u"
        if "PCMA" in raw:
            return "G.711a"
        if "OPUS" in raw:
            return "OPUS"
        return raw

    info["video_codec"] = _friendly_codec(info["video_codec"])
    info["audio_codec"] = _friendly_codec(info["audio_codec"])

    return info


def _stream_http_flv(host, port, path, scheme, duration, full_url):
    """HTTP-FLV 取流测试"""
    try:
        url = f"{scheme}://{host}:{port}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
        print(f"    {info('正在连接 HTTP-FLV 流...')}")

        start_time = time.time()
        total_bytes = 0
        packets = 0
        first_data_time = None
        last_data_time = None

        with urllib.request.urlopen(req, timeout=10) as resp:
            ct = resp.headers.get("Content-Type", "")
            print(f"    Content-Type: {ct}")

            if "flv" not in ct.lower() and "octet-stream" not in ct.lower() and "video" not in ct.lower():
                print(f"    {warn(f'Content-Type 不是视频流: {ct}')}")
            else:
                print(f"    {ok('Content-Type 确认为视频流')}")

            # 检查 FLV header
            header = resp.read(3)
            if header == b"FLV":
                print(f"    {ok('FLV 文件头校验通过')}")
            else:
                print(f"    {warn(f'非标准 FLV 头: {header.hex()}')}")

            total_bytes += len(header)
            packets = 1
            first_data_time = time.time()

            # 持续读取
            while time.time() - start_time < duration:
                try:
                    data = resp.read(8192)
                    if not data:
                        print(f"    {warn('流已结束')}")
                        break
                    total_bytes += len(data)
                    packets += 1
                    last_data_time = time.time()
                except Exception as e:
                    print(f"    {warn(f'读取中断: {e}')}")
                    break

        elapsed_real = (last_data_time or first_data_time) - first_data_time if first_data_time else 0
        _print_stream_stats(total_bytes, packets, elapsed_real, duration, [], "HTTP-FLV")

    except urllib.error.HTTPError as e:
        print(f"    {err(f'HTTP 错误: {e.code} {e.reason}')}")
    except Exception as e:
        print(f"    {err(f'FLV 取流失败: {e}')}")


def _stream_hls_test(host, port, path, scheme, duration, full_url):
    """HLS 取流测试：下载 m3u8 播放列表并尝试获取 TS 分片"""
    issues = []
    try:
        url = f"https://{host}:{port}{path}" if scheme == "https" else f"http://{host}:{port}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
        print(f"    {info('正在获取 HLS m3u8 播放列表...')}")

        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8", errors="replace")

            if "#EXTM3U" not in body:
                print(f"    {err('非标准 m3u8 格式')}")
                return

            # 判断是否为 Master Playlist（多码率）
            if "#EXT-X-STREAM-INF" in body:
                print(f"    {info('检测到 Master Playlist（多码率），选择第一个子流...')}")
                # 提取第一个子流 URL
                m = re.search(r"#EXT-X-STREAM-INF:.*?\n(.+)", body)
                if m:
                    sub_url = m.group(1).strip()
                    if not sub_url.startswith("http"):
                        base = url.rsplit("/", 1)[0]
                        sub_url = base + "/" + sub_url
                    print(f"    {info(f'子流地址: {sub_url}')}")
                    # 递归获取子流的 m3u8
                    req2 = urllib.request.Request(sub_url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
                    with urllib.request.urlopen(req2, timeout=10) as resp2:
                        body = resp2.read().decode("utf-8", errors="replace")
                else:
                    print(f"    {err('无法解析子流地址')}")
                    return

            # 解析 TS 分片 / fMP4 分片
            segment_urls = []
            init_url = None
            base_url = url.rsplit("/", 1)[0]
            for line in body.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    # 检测 fMP4 初始化段
                    if "#EXT-X-MAP" in line:
                        uri_m = re.search(r'URI="([^"]+)"', line)
                        if uri_m:
                            uri = uri_m.group(1)
                            init_url = uri if uri.startswith("http") else base_url + "/" + uri
                    continue
                # 非 # 开头且包含 / 或 . 扩展名的行视为分片地址
                if "/" in line or "." in line:
                    full = line if line.startswith("http") else base_url + "/" + line
                    segment_urls.append(full)

            if not segment_urls:
                print(f"    {warn('未找到媒体分片地址')}")
                print(f"    {info('可能为空播放列表或已过期')}")
                return

            print(f"    {ok(f'找到 {len(segment_urls)} 个媒体分片')}")
            if init_url:
                init_name = init_url.split("/")[-1]
                print(f"    {info(f'fMP4 初始化段: {init_name}')}")

            # 解析播放列表信息
            target_dur = None
            m = re.search(r"#EXT-X-TARGETDURATION:(\d+)", body)
            if m:
                target_dur = int(m.group(1))
                print(f"    {info(f'目标分片时长: {target_dur}s')}")

            # 下载前几个分片测试
            seg_dur = target_dur if target_dur else 2
            test_count = min(len(segment_urls), max(2, duration // seg_dur))
            print(f"\n  {bold(f'[接收] 下载前 {test_count} 个分片...')}")

            total_bytes = 0
            downloaded = 0
            segment_sizes = []
            start_time = time.time()

            # 如果有 fMP4 初始化段，先下载
            if init_url:
                try:
                    req_init = urllib.request.Request(init_url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
                    with urllib.request.urlopen(req_init, timeout=10) as init_resp:
                        init_data = init_resp.read()
                        total_bytes += len(init_data)
                        print(f"    初始化段: {len(init_data):>8,} bytes {ok('OK')}")
                except Exception as e:
                    print(f"    初始化段: {err(f'下载失败: {e}')}")

            for i, seg_url in enumerate(segment_urls[:test_count]):
                try:
                    req_seg = urllib.request.Request(seg_url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
                    with urllib.request.urlopen(req_seg, timeout=10) as seg_resp:
                        data = seg_resp.read()
                        size = len(data)
                        total_bytes += size
                        segment_sizes.append(size)
                        downloaded += 1

                        # 分片格式校验
                        ext = seg_url.rsplit("?", 1)[0].rsplit(".", 1)[-1].lower() if "." in seg_url.split("?")[0] else ""
                        if ext == "ts" and data[:1] == b"\x47":
                            status = ok
                            label = "TS Sync OK"
                        elif ext in ("m4s", "mp4") or data[:4] in (b"\x00\x00\x00\x1c", b"\x00\x00\x00\x20", b"\x00\x00\x00\x18", b"\x00\x00\x00\x24"):
                            status = ok
                            label = "fMP4 OK"
                        elif data[:3] == b"\x47":
                            status = ok
                            label = "TS Sync OK"
                        else:
                            status = info
                            label = f"格式: {ext or 'unknown'}"

                        print(f"    分片 {i+1}: {size:>8,} bytes {status(label)}")
                except Exception as e:
                    print(f"    分片 {i+1}: {err(f'下载失败: {e}')}")

            elapsed = time.time() - start_time

            # 统计
            print(f"\n  {bold('── 取流结果 ──')}")
            print(f"    下载分片 : {ok(f'{downloaded}/{test_count}')}")
            print(f"    总数据量 : {total_bytes:,} bytes ({total_bytes/1024/1024:.2f} MB)")

            if segment_sizes:
                avg_size = sum(segment_sizes) / len(segment_sizes)
                # 粗略码率估算（假设每分片 target_dur 秒）
                if target_dur:
                    bitrate_kbps = avg_size * 8 / (target_dur * 1000)
                    print(f"    平均分片 : {avg_size:,.0f} bytes")
                    print(f"    估算码率 : {bitrate_kbps:.0f} kbps ({bitrate_kbps/1000:.1f} Mbps)")
                print(f"    分片大小 : {min(segment_sizes):,} ~ {max(segment_sizes):,} bytes")
            print(f"    总耗时   : {elapsed:.1f}s")

            if downloaded == test_count:
                print(f"\n    {ok('HLS 取流测试通过，TS 分片可正常下载')}")
            elif downloaded > 0:
                print(f"\n    {warn(f'HLS 部分分片下载成功 ({downloaded}/{test_count})')}")
            else:
                print(f"\n    {err('HLS 取流测试失败，无法下载任何分片')}")

    except Exception as e:
        print(f"    {err(f'HLS 取流失败: {e}')}")


def _stream_http_generic(host, port, path, scheme, duration, full_url):
    """通用 HTTP 视频流取流测试（MJPEG / MJPEG-over-HTTP 等）"""
    try:
        url = f"{scheme}://{host}:{port}{path}"
        req = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
        print(f"    {info('正在连接 HTTP 视频流...')}")

        start_time = time.time()
        total_bytes = 0
        packets = 0
        first_data_time = None
        last_data_time = None
        boundary = None

        with urllib.request.urlopen(req, timeout=10) as resp:
            ct = resp.headers.get("Content-Type", "")
            print(f"    Content-Type: {ct}")

            # 检测 multipart 流边界
            if "multipart" in ct.lower():
                m = re.search(r'boundary="?([^";]+)"?', ct)
                if m:
                    boundary = m.group(1)
                    print(f"    {info(f'Multipart 边界: {boundary}')}")
                print(f"    {ok('检测到 MJPEG/Generic multipart 流')}")

            first_data_time = time.time()

            while time.time() - start_time < duration:
                try:
                    data = resp.read(8192)
                    if not data:
                        break
                    total_bytes += len(data)
                    packets += 1
                    last_data_time = time.time()
                except Exception:
                    break

        elapsed_real = (last_data_time or first_data_time) - first_data_time if first_data_time else 0
        _print_stream_stats(total_bytes, packets, elapsed_real, duration, [], "HTTP")

    except urllib.error.HTTPError as e:
        print(f"    {err(f'HTTP 错误: {e.code} {e.reason}')}")
    except Exception as e:
        print(f"    {err(f'HTTP 取流失败: {e}')}")


def _stream_rtmp_test(host, port, duration, full_url):
    """RTMP 取流测试（TCP 层面检测，RTMP 握手需二进制协议栈）"""
    print(f"    {info('RTMP 协议检测...')}")
    try:
        sock = socket.create_connection((host, port), timeout=5)

        # RTMP 握手: C0 (1 byte version) + C1 (1536 bytes timestamp + zero)
        c0 = bytes([3])  # RTMP version 3
        c1 = b"\x00" * 1536  # C1: timestamp(4) + zero(4) + random(1528)
        sock.sendall(c0 + c1)

        # 等待 S0 + S1 响应
        sock.settimeout(5)
        s0s1 = sock.recv(1 + 1536)
        if len(s0s1) >= 1 and s0s1[0] == 3:
            print(f"    {ok('RTSP S0+S1 握手成功 (version 3)')}")

            # 发送 C2
            c2 = s0s1[1:1+1536] if len(s0s1) > 1 else b"\x00" * 1536
            sock.sendall(c2)

            # 等待 S2
            s2 = sock.recv(1536)
            if len(s2) >= 1536:
                print(f"    {ok('RTMP 完整握手成功 (C0/C1/C2 + S0/S1/S2)')}")

                # 读取流数据
                print(f"\n  {bold(f'[接收] 读取 {duration} 秒数据流...')}")
                total_bytes = 0
                packets = 0
                first_data_time = time.time()

                sock.settimeout(3)
                while time.time() - first_data_time < duration:
                    try:
                        data = sock.recv(32768)
                        if not data:
                            break
                        total_bytes += len(data)
                        packets += 1
                    except socket.timeout:
                        if total_bytes == 0:
                            print(f"    {warn('握手成功但无数据返回')}")
                            print(f"    {info('RTMP 需要正确的 app/stream 路径，如 rtmp://host:1935/live/stream')}")
                            break
                        continue
                    except Exception as e:
                        break

                last_data_time = time.time()
                elapsed_real = last_data_time - first_data_time
                _print_stream_stats(total_bytes, packets, elapsed_real, duration, [], "RTMP")
            else:
                print(f"    {warn('S2 响应不完整')}")
        else:
            if s0s1:
                ver = s0s1[0]
                print(f"    {warn(f'RTMP 握手响应异常: version={ver}')}")
            else:
                print(f"    {err('RTMP 无响应')}")
        sock.close()

    except socket.timeout:
        print(f"    {err('RTMP 连接/握手超时')}")
    except ConnectionRefusedError:
        print(f"    {err('RTMP 连接被拒绝')}")
    except Exception as e:
        print(f"    {err(f'RTMP 取流失败: {e}')}")


def _print_stream_stats(total_bytes, packets, elapsed_real, duration, issues, protocol):
    """输出取流统计结果"""
    print(f"\n  {bold('── 取流结果 ──')}")
    print(f"    接收数据 : {total_bytes:,} bytes ({total_bytes/1024:.1f} KB)")
    print(f"    接收包数 : {packets}")
    print(f"    实际时长 : {elapsed_real:.1f}s / {duration}s")

    if total_bytes > 0 and elapsed_real > 0:
        bitrate_kbps = total_bytes * 8 / (elapsed_real * 1000)
        bitrate_mbps = bitrate_kbps / 1000
        print(f"    平均码率 : {bitrate_kbps:.0f} kbps ({bitrate_mbps:.2f} Mbps)")

        # 码率评估
        if bitrate_mbps < 0.5:
            print(f"    {info(f'码率较低，可能是子码流或静态画面')}")
        elif bitrate_mbps < 4:
            print(f"    {ok(f'码率正常（标清/子码率范围）')}")
        elif bitrate_mbps < 8:
            print(f"    {ok(f'码率正常（高清范围）')}")
        else:
            print(f"    {ok(f'码率较高（超高清或高帧率）')}")

        # 数据连续性检测
        if elapsed_real < duration * 0.5:
            print(f"    {warn(f'数据接收时长不足预期的一半，可能存在中断')}")
            issues.append(f"{protocol} 取流中断 - 数据接收不连续")
        else:
            print(f"    {ok(f'{protocol} 取流测试通过 - 数据连续接收')}")

        if packets > 0:
            avg_packet = total_bytes / packets
            print(f"    平均包大小: {avg_packet:.0f} bytes")
    elif total_bytes == 0:
        print(f"    {err('未接收到任何数据')}")
        issues.append(f"{protocol} 取流失败 - 无数据返回")

    if issues:
        print(f"\n  {warn(f'发现问题: {', '.join(issues)}')}")


# ─────────────────────────────────────────────
# RTSP 快捷取流（IP + 端口 + 用户名 + 密码）
# ─────────────────────────────────────────────

# 常见摄像头厂商 RTSP 路径模板
RTSP_PATH_TEMPLATES = {
    "hikvision": [
        "/Streaming/Channels/101",   # 主码流
        "/Streaming/Channels/102",   # 子码流
        "/Streaming/Channels/201",   # 第三码流
        "/h264/ch1/main/av_stream",  # 旧版海康
        "/h264/ch1/sub/av_stream",
    ],
    "dahua": [
        "/cam/realmonitor?channel=1&subtype=0",  # 主码流
        "/cam/realmonitor?channel=1&subtype=1",  # 子码流
        "/cam/realmonitor?channel=2&subtype=0",
        "/live/ch00_0.264",         # 旧版大华
        "/live/ch00_1.264",
    ],
    "uniview": [
        "/video1",                  # 宇视 主码流
        "/video2",                  # 宇视 子码流
        "/Living/ch1",              # 宇视备选
    ],
    "dhipc": [
        "/live/main",               # DHCP/通用IPC 主码流
        "/live/sub",                # 子码流
        "/ch0_0.264",
        "/ch0_1.264",
    ],
    "generic": [
        "/stream1",
        "/stream",
        "/live",
        "/video",
        "/media",
        "/h264",
        "/ch1",
        "/cam1",
    ],
}

# 品牌别名映射
BRAND_ALIASES = {
    "hikvision": ["hikvision", "hik", "海康", "海康威视"],
    "dahua": ["dahua", "大华"],
    "uniview": ["uniview", "宇视", "unv"],
    "dhipc": ["dhipc", "dhipc", "dhcp", "通用ipc", "generic"],
    "generic": ["generic", "通用", "其他"],
}


def _resolve_brand(brand_input):
    """将用户输入的品牌名映射到标准品牌名，返回品牌列表（或 None 表示全部）"""
    if not brand_input:
        return None  # 探测全部
    brand_lower = brand_input.lower().strip()
    for brand, aliases in BRAND_ALIASES.items():
        if brand_lower in aliases or brand_lower == brand:
            return [brand]
    # 未匹配到，当作 generic 处理
    return ["generic"]


def cmd_rtspstream(ip, port, user, password, path, duration, brand):
    """
    通过 IP/端口/用户名/密码 快捷获取 RTSP 流
    如果指定了 path，直接拼接 URL 取流
    如果未指定 path，依次探测常见厂商路径，找到可用的进行取流
    """
    section("RTSP 快捷取流")

    # 参数校验
    if not ip or not user:
        print(err("IP 和用户名为必填参数"))
        return

    # 构建 RTSP URL 前缀
    if password:
        url_prefix = f"rtsp://{user}:{password}@{ip}:{port}"
    else:
        url_prefix = f"rtsp://{user}@{ip}:{port}"

    print(f"  目标主机 : {ip}")
    print(f"  RTSP端口 : {port}")
    print(f"  用户名   : {user}")
    print(f"  密码     : {'****' if password else '(无)'}")
    if path:
        print(f"  指定路径 : {path}")
    print(f"  测试时长 : {duration} 秒")

    # ── 1. 连通性预检 ──
    print(f"\n  {bold('[1/3] 连通性预检')}")
    try:
        start = time.time()
        sock = socket.create_connection((ip, port), timeout=5)
        elapsed = (time.time() - start) * 1000
        sock.close()
        print(f"    {ok(f'端口 {port} 可达 ({elapsed:.1f}ms)')}")
    except (socket.timeout, TimeoutError):
        print(f"    {err(f'端口 {port} 连接超时 - 目标不可达')}")
        return
    except ConnectionRefusedError:
        print(f"    {err(f'端口 {port} 连接被拒绝 - RTSP 服务未启动')}")
        return
    except OSError as e:
        print(f"    {err(f'连接失败: {e}')}")
        return

    # Ping 延迟
    print(f"    Ping 检测...")
    if sys.platform == "win32":
        ping_cmd = ["ping", "-n", "2", "-w", "2000", ip]
    else:
        ping_cmd = ["ping", "-c", "2", "-W", "2", ip]
    out, _, rc = run(ping_cmd)
    if rc == 0:
        latency = _extract_ping_latency(out)
        if latency is not None:
            icon = ok if latency < 50 else (warn if latency < 200 else err)
            print(f"    {icon(f'延迟 {latency:.1f}ms')}")
        else:
            print(f"    {ok('Ping 通')}")
    else:
        print(f"    {warn('Ping 不通（可能禁ping，但不影响RTSP）')}")

    # ── 2. 路径探测 / 取流 ──
    print(f"\n  {bold('[2/3] RTSP 流探测')}")

    if path:
        # 用户指定了路径，直接取流
        full_url = url_prefix + path
        print(f"    使用指定路径: {path}")
        print(f"    完整 URL  : {full_url}")
        _stream_rtsp(ip, port, path, user, password, duration, full_url)
        return

    # 自动探测路径
    brands_to_try = _resolve_brand(brand)
    if brands_to_try:
        print(f"    品牌筛选: {', '.join(brands_to_try)}")
    else:
        print(f"    未指定品牌，将探测所有常见厂商路径...")

    # 收集所有待探测路径
    all_paths = []
    brand_order = ["hikvision", "dahua", "uniview", "dhipc", "generic"]
    if brands_to_try:
        # 用户指定了品牌，按品牌顺序探测
        for b in brand_order:
            if b in brands_to_try and b in RTSP_PATH_TEMPLATES:
                for p in RTSP_PATH_TEMPLATES[b]:
                    all_paths.append((b, p))
    else:
        # 全部探测
        for b in brand_order:
            if b in RTSP_PATH_TEMPLATES:
                for p in RTSP_PATH_TEMPLATES[b]:
                    all_paths.append((b, p))

    # 探测每个路径
    found_streams = []
    for brand_name, test_path in all_paths:
        full_url = url_prefix + test_path
        result = _probe_rtsp_path(ip, port, user, password, full_url, test_path, brand_name)
        if result:
            found_streams.append(result)

    if not found_streams:
        print(f"\n  {err('未找到可用的 RTSP 流路径')}")
        print(f"  {warn('可能原因:')}")
        print(f"    1. 用户名或密码不正确")
        print(f"    2. 摄像头品牌不在预设列表中（海康/大华/宇视/通用IPC）")
        print(f"    3. RTSP 服务未启用，需要在摄像头Web管理页面开启")
        print(f"    4. 端口不是默认的 554")
        print(f"  {info('你可以使用 --path 参数手动指定路径重试')}")
        print(f"  {info('例如: rtspstream --ip {ip} --port {port} --user {user} --pass **** --path /custom/path')}")
        return

    # ── 3. 汇总探测结果 ──
    print(f"\n  {bold('[3/3] 探测结果汇总')}")
    print(f"\n  {ok(f'找到 {len(found_streams)} 个可用流:')}")
    for i, (stream_url, stream_brand, stream_path, stream_status) in enumerate(found_streams, 1):
        print(f"    {i}. [{stream_brand:12s}] {stream_path}")
        print(f"       {dim(stream_url)}")
        if stream_status:
            print(f"       {info(stream_status)}")

    # 对第一个可用的流进行完整取流测试
    best = found_streams[0]
    best_url, best_brand, best_path, _ = best
    print(f"\n  {bold('── 对最佳匹配流进行取流测试 ──')}")
    print(f"    {info(f'选中: [{best_brand}] {best_path}')}")
    _stream_rtsp(ip, port, best_path, user, password, duration, best_url)


def _probe_rtsp_path(ip, port, user, password, full_url, path, brand_name):
    """
    快速探测单个 RTSP 路径是否可用
    返回 (url, brand, path, status_text) 或 None
    使用 DESCRIBE 请求检测，避免完整取流的耗时
    """
    try:
        sock = socket.create_connection((ip, port), timeout=5)

        request = f"DESCRIBE {full_url} RTSP/1.0\r\n"
        request += f"CSeq: 1\r\n"
        request += f"User-Agent: WorkBuddy-OpsToolkit/1.0\r\n"
        if user:
            cred = f"{user}:{password or ''}"
            b64 = base64.b64encode(cred.encode()).decode()
            request += f"Authorization: Basic {b64}\r\n"
        request += "Accept: application/sdp\r\n"
        request += "\r\n"

        sock.sendall(request.encode())
        resp = b""
        sock.settimeout(3)
        try:
            while True:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                resp += chunk
                if b"\r\n\r\n" in resp:
                    break
        except socket.timeout:
            pass
        sock.close()

        resp_str = resp.decode("utf-8", errors="replace")
        first_line = resp_str.splitlines()[0] if resp_str.splitlines() else ""

        if "200" in first_line:
            # 解析 SDP 获取媒体信息
            body_start = resp_str.find("\r\n\r\n")
            sdp = resp_str[body_start + 4:] if body_start >= 0 else ""
            media_info = _parse_sdp(sdp) if sdp.strip() else {}
            vc = media_info.get("video_codec", "")
            res = media_info.get("resolution", "")
            status_parts = []
            if vc:
                status_parts.append(f"编码={vc}")
            if res:
                status_parts.append(f"分辨率={res}")
            status = " ".join(status_parts) if status_parts else "可用"

            print(f"    {ok(f'[{brand_name:12s}] {path}')}")
            if status_parts:
                print(f"    {dim(f'              {status}')}")
            return (full_url, brand_name, path, status)
        elif "401" in first_line:
            # 401 说明路径存在但认证失败，只对第一个401打印提示
            return None
        elif "404" in first_line:
            return None
        else:
            # 其他状态码也跳过
            return None

    except socket.timeout:
        return None
    except Exception:
        return None

ROOTCAUSE_HINTS = {
    r"out of memory|oom|killed":       "内存不足 → 检查内存泄漏，考虑增加内存或限制进程内存",
    r"connection refused":             "服务未启动或端口被防火墙封禁 → 检查服务状态和防火墙规则",
    r"no space left|disk full":        "磁盘空间耗尽 → 清理日志文件、临时文件或扩容磁盘",
    r"too many open files|ulimit":     "文件描述符耗尽 → 调整 ulimit -n 或系统级 fs.file-max",
    r"timeout|timed out":              "网络或服务响应超时 → 检查网络延迟、服务负载和超时配置",
    r"permission denied|access denied":"权限不足 → 检查文件权限、SELinux/AppArmor 配置",
    r"segfault|segmentation fault":    "程序内存访问错误 → 收集 core dump，使用 gdb 分析",
    r"deadlock":                       "数据库/线程死锁 → 检查事务锁顺序，开启死锁检测日志",
    r"ssl|certificate":                "SSL证书问题 → 检查证书有效期、域名匹配和信任链",
    r"cpu.*100|load average.*[5-9]\d": "CPU过载 → 分析高CPU进程，考虑限流或横向扩展",
}

def cmd_hint(message):
    section("根因分析建议")
    print(f"  输入信息: {message}\n")
    matched = []
    for pattern, hint in ROOTCAUSE_HINTS.items():
        if re.search(pattern, message, re.I):
            matched.append(hint)

    if matched:
        print(f"  {bold('可能的根因及建议:')}")
        for i, hint in enumerate(matched, 1):
            print(f"  {i}. {ok('→')} {hint}")
    else:
        print(warn("未匹配到已知模式，建议:"))
        print("  1. 检查完整错误日志上下文")
        print("  2. 确认最近的变更（部署、配置修改）")
        print("  3. 使用 logscan 命令扫描相关日志文件")

# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────

def main():
    if sys.platform == "win32":
        os.system("")

    parser = argparse.ArgumentParser(description="IT运维工具箱 - 监控问题排查")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("logscan",  help="日志文件扫描")
    p.add_argument("filepath")
    p.add_argument("-p", "--pattern", default=None, help="自定义正则表达式")
    p.add_argument("-n", "--tail",    type=int, default=None, help="只看最后N行")
    p.add_argument("-c", "--context", type=int, default=2, help="上下文行数")

    sub.add_parser("oom",      help="OOM内存不足检测")
    sub.add_parser("crashes",  help="进程崩溃/重启检测")
    sub.add_parser("netcheck", help="网络连接异常排查")
    sub.add_parser("perf",     help="性能瓶颈快速定位")
    sub.add_parser("inspect",  help="综合巡检报告")

    p = sub.add_parser("hint",    help="根因分析建议")
    p.add_argument("message", help="错误信息描述")

    p = sub.add_parser("video",   help="视频监控播放问题排查")
    p.add_argument("--url",    help="监控HTTP地址 (http://host:port/path)")
    p.add_argument("--rtsp",   help="监控RTSP地址 (rtsp://user:pass@host:port/path)")

    p = sub.add_parser("stream",  help="视频取流测试")
    p.add_argument("--url",      help="监控HTTP地址 (http/https)")
    p.add_argument("--rtsp",     help="监控RTSP地址 (rtsp://user:pass@host:port/path)")
    p.add_argument("--duration", type=int, default=5, help="取流测试时长（秒），默认5秒")

    p = sub.add_parser("rtspstream", help="通过IP/端口/用户名/密码获取监控RTSP流")
    p.add_argument("--ip",       required=True,  help="摄像头IP地址")
    p.add_argument("--port",     type=int, default=554, help="RTSP端口，默认554")
    p.add_argument("--user",     required=True,  help="用户名")
    p.add_argument("--password", default="",      help="密码（默认空）")
    p.add_argument("--path",     default=None,     help="RTSP路径（不指定则自动探测常见路径）")
    p.add_argument("--duration", type=int, default=5, help="取流测试时长（秒），默认5秒")
    p.add_argument("--brand",    default=None,     help="摄像头品牌（hikvision/dahua/uniview/dhipc，不指定则全部探测）")

    args = parser.parse_args()
    dispatch = {
        "logscan":    lambda: cmd_logscan(args.filepath, args.pattern, args.tail, args.context),
        "oom":        cmd_oom,
        "crashes":    cmd_crashes,
        "netcheck":   cmd_netcheck,
        "perf":       cmd_perf,
        "inspect":    cmd_inspect,
        "hint":       lambda: cmd_hint(args.message),
        "video":      lambda: cmd_video(args.url, args.rtsp),
        "stream":     lambda: cmd_stream(args.url, args.rtsp, args.duration),
        "rtspstream": lambda: cmd_rtspstream(args.ip, args.port, args.user, args.password, args.path, args.duration, args.brand),
    }
    dispatch[args.cmd]()

if __name__ == "__main__":
    main()
