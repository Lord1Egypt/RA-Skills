#!/usr/bin/env python3
"""
IT运维工具箱 - 网络诊断模块
支持: ping检测、DNS解析、域名查IP、HTTP/HTTPS检测、SSL证书检查、端口扫描、IP归属地
用法: python network_diag.py <command> [args...]
"""

import sys
import os
import subprocess
import socket
import ssl
import json
import urllib.request
import urllib.error
import datetime
import struct
import time
import argparse
import re

# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def color(text, code):
    """ANSI颜色，Windows也支持"""
    return f"\033[{code}m{text}\033[0m"

def ok(msg):   return color(f"✅ {msg}", "32")
def warn(msg): return color(f"⚠️  {msg}", "33")
def err(msg):  return color(f"❌ {msg}", "31")
def info(msg): return color(f"ℹ️  {msg}", "36")
def bold(msg): return color(msg, "1")

def section(title):
    print(f"\n{bold('═' * 50)}")
    print(f"  {bold(title)}")
    print(bold('═' * 50))

# ─────────────────────────────────────────────
# Ping 检测
# ─────────────────────────────────────────────

def cmd_ping(host, count=4):
    section(f"Ping 检测: {host}")
    if sys.platform == "win32":
        cmd = ["ping", "-n", str(count), host]
    else:
        cmd = ["ping", "-c", str(count), host]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        print(output)
        # 简单解析丢包率
        if "100%" in output or "100.0%" in output:
            print(err("全部丢包，目标主机不可达"))
        elif result.returncode == 0:
            print(ok("Ping 检测通过"))
        else:
            print(warn("Ping 检测存在异常"))
    except subprocess.TimeoutExpired:
        print(err("Ping 超时"))
    except FileNotFoundError:
        print(err("系统未找到 ping 命令"))

# ─────────────────────────────────────────────
# DNS 查询
# ─────────────────────────────────────────────

def cmd_dns(domain):
    section(f"DNS 查询: {domain}")
    try:
        results = socket.getaddrinfo(domain, None)
        ips = sorted(set(r[4][0] for r in results))
        for ip in ips:
            af = "IPv6" if ":" in ip else "IPv4"
            print(f"  {ok(af)}: {ip}")
        print(f"\n{ok(f'共解析到 {len(ips)} 个地址')}")
    except socket.gaierror as e:
        print(err(f"DNS解析失败: {e}"))

    # 尝试反向解析
    try:
        hostname = socket.gethostbyaddr(socket.gethostbyname(domain))[0]
        print(f"  {info('反向解析')}: {hostname}")
    except Exception:
        pass

# ─────────────────────────────────────────────
# 域名查 IP（精简版，专注输出 IP）
# ─────────────────────────────────────────────

def cmd_dnsip(domain):
    """根据域名查询解析到的 IP 地址，输出精简明了"""
    section(f"域名查IP: {domain}")
    try:
        results = socket.getaddrinfo(domain, None)
        ips = sorted(set(r[4][0] for r in results))
        if not ips:
            print(err(f"域名 {domain} 无解析结果"))
            return

        v4 = [ip for ip in ips if ":" not in ip]
        v6 = [ip for ip in ips if ":" in ip]

        if v4:
            print(f"\n  {bold('IPv4 地址:')}")
            for ip in v4:
                print(f"    {ok(ip)}")

        if v6:
            print(f"\n  {bold('IPv6 地址:')}")
            for ip in v6:
                print(f"    {ok(ip)}")

        # 尝试通过公共 DNS 对比（nslookup 风格）
        print(f"\n  {bold('DNS 服务器对比:')}")
        dns_servers = {
            "系统默认": None,
            "Google 8.8.8.8": "8.8.8.8",
            "阿里 223.5.5.5": "223.5.5.5",
            "腾讯 119.29.29.29": "119.29.29.29",
        }
        for label, dns_ip in dns_servers.items():
            try:
                if dns_ip:
                    cmd = ["nslookup", domain, dns_ip]
                else:
                    cmd = ["nslookup", domain]
                out, rc = run_nslookup(cmd)
                parsed = parse_nslookup(out)

                if parsed:
                    for p_ip in parsed:
                        af = "IPv6" if ":" in p_ip else "IPv4"
                        print(f"    {label:20s} → {p_ip} ({af})")
                else:
                    print(f"    {label:20s} → {warn('解析失败')}")
            except Exception:
                print(f"    {label:20s} → {warn('查询异常')}")

        # CDN 检测提示
        if len(v4) > 1:
            print(f"\n  {info(f'检测到 {len(v4)} 个 IPv4 地址，域名可能使用了 CDN 或 DNS 负载均衡')}")
        elif v4:
            # 检查是否为常见 CDN IP 段
            first_octet = int(v4[0].split(".")[0])
            cdn_ranges = {
                (1, 33): "腾讯云 CDN", (36, 37): "中国电信", (42, 43): "中国联通",
                (47,): "Akamai", (100, 104): "Cloudflare", (110,): "阿里云 CDN",
                (112, 120): "中国电信/联通/移动", (139,): "世纪互联",
                (172,): "Akamai/Cloudflare", (175, 176): "中国移动",
                (182, 183): "中国移动", (198,): "Cloudflare",
                (203,): "中国电信", (221,): "中国联通",
            }
            for ranges, name in cdn_ranges.items():
                if first_octet in ranges:
                    print(f"\n  {info(f'IP 段 {v4[0]} 可能属于: {name}')}")
                    break

    except socket.gaierror as e:
        print(err(f"DNS 解析失败: {e}"))

def run_nslookup(cmd):
    """执行 nslookup 命令"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, errors="replace")
        # 合并 stdout 和 stderr（Windows 上 nslookup 把应答输出到 stderr）
        combined = (result.stdout + "\n" + result.stderr) if result.stderr.strip() else result.stdout
        return combined, result.returncode
    except subprocess.TimeoutExpired:
        return "", -1
    except FileNotFoundError:
        return "", -1

def parse_nslookup(output):
    """解析 nslookup 输出中的 IP 地址"""
    ips = []
    lines = output.splitlines()
    in_answer = False
    for line in lines:
        line = line.strip()
        # 标记进入应答区域（遇到 Name: 或 名称:）
        if re.match(r"^Name:\s+", line, re.I) or line.startswith("名称:"):
            in_answer = True
            continue
        if not in_answer:
            continue
        # 匹配 "Addresses: 1.2.3.4" (Windows, 多IP时用复数)
        m = re.match(r"^Addresses?:\s*(\d+\.\d+\.\d+\.\d+)", line, re.I)
        if m:
            ips.append(m.group(1))
            continue
        # 匹配缩进的纯 IP 行（Windows 多IP后续行格式: "\t  1.2.3.4"）
        m = re.match(r"^(\d+\.\d+\.\d+\.\d+)$", line)
        if m:
            ips.append(m.group(1))
            continue
        # 遇到空行或新段则停止
        if not line:
            in_answer = False
    return ips

# ─────────────────────────────────────────────
# HTTP/HTTPS 检测
# ─────────────────────────────────────────────

def cmd_http(url, timeout=10):
    section(f"HTTP 检测: {url}")
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
        start = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = (time.time() - start) * 1000
            code = resp.status
            headers = dict(resp.headers)

            status_icon = ok(str(code)) if 200 <= code < 300 else warn(str(code))
            print(f"  状态码   : {status_icon}")
            print(f"  响应时间 : {elapsed:.1f} ms")
            print(f"  Content-Type: {headers.get('Content-Type', 'N/A')}")
            print(f"  Server   : {headers.get('Server', 'N/A')}")
            print(f"  最终URL  : {resp.url}")

            if elapsed < 500:
                print(ok("响应速度正常"))
            elif elapsed < 2000:
                print(warn(f"响应较慢: {elapsed:.0f}ms"))
            else:
                print(err(f"响应过慢: {elapsed:.0f}ms"))

    except urllib.error.HTTPError as e:
        print(err(f"HTTP错误: {e.code} {e.reason}"))
    except urllib.error.URLError as e:
        print(err(f"连接失败: {e.reason}"))
    except Exception as e:
        print(err(f"检测异常: {e}"))

# ─────────────────────────────────────────────
# SSL 证书检查
# ─────────────────────────────────────────────

def cmd_ssl(host, port=443):
    section(f"SSL 证书检查: {host}:{port}")
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                # 解析有效期
                not_after_str  = cert.get("notAfter", "")
                not_before_str = cert.get("notBefore", "")
                fmt = "%b %d %H:%M:%S %Y %Z"
                try:
                    not_after  = datetime.datetime.strptime(not_after_str, fmt)
                    not_before = datetime.datetime.strptime(not_before_str, fmt)
                    days_left  = (not_after - datetime.datetime.utcnow()).days
                except Exception:
                    not_after = not_before = None
                    days_left = None

                # 主题
                subject = dict(x[0] for x in cert.get("subject", []))
                issuer  = dict(x[0] for x in cert.get("issuer",  []))
                san     = [v for t, v in cert.get("subjectAltName", []) if t == "DNS"]

                print(f"  颁发给   : {subject.get('commonName', 'N/A')}")
                print(f"  颁发机构 : {issuer.get('organizationName', 'N/A')}")
                print(f"  生效日期 : {not_before_str}")
                print(f"  到期日期 : {not_after_str}")
                if days_left is not None:
                    if days_left > 30:
                        print(f"  剩余天数 : {ok(str(days_left) + ' 天')}")
                    elif days_left > 7:
                        print(f"  剩余天数 : {warn(str(days_left) + ' 天（即将到期）')}")
                    elif days_left > 0:
                        print(f"  剩余天数 : {err(str(days_left) + ' 天（紧急续期！）')}")
                    else:
                        print(f"  剩余天数 : {err('已过期！')}")
                if san:
                    print(f"  SAN域名  : {', '.join(san[:8])}{'...' if len(san)>8 else ''}")
                print(f"  TLS版本  : {ssock.version()}")
                print(ok("证书有效，连接正常"))
    except ssl.SSLCertVerificationError as e:
        print(err(f"证书验证失败: {e}"))
    except ssl.SSLError as e:
        print(err(f"SSL错误: {e}"))
    except socket.timeout:
        print(err("连接超时"))
    except Exception as e:
        print(err(f"检测异常: {e}"))

# ─────────────────────────────────────────────
# 端口扫描
# ─────────────────────────────────────────────

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 465: "SMTPS",
    587: "SMTP/TLS", 993: "IMAPS", 995: "POP3S", 1433: "MSSQL",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5672: "RabbitMQ",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt", 9200: "Elasticsearch",
    27017: "MongoDB", 2181: "ZooKeeper", 2379: "etcd",
}

def cmd_portscan(host, ports=None, timeout=1):
    if ports is None:
        ports = sorted(COMMON_PORTS.keys())
        section(f"常用端口扫描: {host} ({len(ports)}个端口)")
    else:
        section(f"端口扫描: {host} 端口 {ports}")

    open_ports = []
    closed_ports = []

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            svc = COMMON_PORTS.get(port, "unknown")
            if result == 0:
                open_ports.append((port, svc))
                print(f"  {ok('OPEN')}   {port:5d}/tcp  {svc}")
            else:
                closed_ports.append(port)
        except Exception:
            closed_ports.append(port)

    print(f"\n{bold('扫描结果')}:")
    print(f"  开放端口: {ok(str(len(open_ports)))} 个")
    print(f"  关闭/过滤: {len(closed_ports)} 个")

    danger_ports = {21: "FTP(明文传输)", 23: "Telnet(明文传输)", 3389: "RDP(暴露风险)"}
    for port, svc in open_ports:
        if port in danger_ports:
            print(warn(f"  安全提示: 端口 {port} ({danger_ports[port]}) 已开放，请注意安全"))

# ─────────────────────────────────────────────
# IP 归属地查询
# ─────────────────────────────────────────────

def cmd_ipinfo(ip=None):
    if ip is None:
        section("本机公网IP查询")
        url = "https://ipapi.co/json/"
    else:
        section(f"IP 归属地查询: {ip}")
        url = f"https://ipapi.co/{ip}/json/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WorkBuddy-OpsToolkit/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            print(f"  IP        : {data.get('ip', 'N/A')}")
            print(f"  归属城市  : {data.get('city', 'N/A')}, {data.get('region', 'N/A')}")
            print(f"  归属国家  : {data.get('country_name', 'N/A')} ({data.get('country', 'N/A')})")
            print(f"  ISP/运营商: {data.get('org', 'N/A')}")
            print(f"  时区      : {data.get('timezone', 'N/A')}")
            print(f"  经纬度    : {data.get('latitude', 'N/A')}, {data.get('longitude', 'N/A')}")
    except Exception as e:
        print(err(f"查询失败: {e}"))

# ─────────────────────────────────────────────
# 综合检测
# ─────────────────────────────────────────────

def cmd_check_all(host):
    """对目标主机做全面网络检测"""
    section(f"综合网络检测: {host}")
    cmd_ping(host, count=3)
    cmd_dns(host)
    cmd_http(f"https://{host}")
    cmd_ssl(host)
    cmd_portscan(host)

# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="IT运维工具箱 - 网络诊断")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    p = subparsers.add_parser("ping",     help="Ping检测")
    p.add_argument("host"); p.add_argument("-c", "--count", type=int, default=4)

    p = subparsers.add_parser("dns",      help="DNS解析")
    p.add_argument("domain")

    p = subparsers.add_parser("dnsip",    help="域名查IP（多DNS对比）")
    p.add_argument("domain")

    p = subparsers.add_parser("http",     help="HTTP/HTTPS检测")
    p.add_argument("url"); p.add_argument("-t", "--timeout", type=int, default=10)

    p = subparsers.add_parser("ssl",      help="SSL证书检查")
    p.add_argument("host"); p.add_argument("-p", "--port", type=int, default=443)

    p = subparsers.add_parser("port",     help="端口扫描")
    p.add_argument("host")
    p.add_argument("-p", "--ports", type=lambda s: [int(x) for x in s.split(",")], default=None)

    p = subparsers.add_parser("ipinfo",   help="IP归属地查询")
    p.add_argument("ip", nargs="?", default=None)

    p = subparsers.add_parser("all",      help="综合检测")
    p.add_argument("host")

    # 开启Windows ANSI颜色支持
    if sys.platform == "win32":
        os.system("")

    args = parser.parse_args()
    dispatch = {
        "ping":   lambda: cmd_ping(args.host, args.count),
        "dns":    lambda: cmd_dns(args.domain),
        "dnsip":  lambda: cmd_dnsip(args.domain),
        "http":   lambda: cmd_http(args.url, args.timeout),
        "ssl":    lambda: cmd_ssl(args.host, args.port),
        "port":   lambda: cmd_portscan(args.host, args.ports),
        "ipinfo": lambda: cmd_ipinfo(args.ip),
        "all":    lambda: cmd_check_all(args.host),
    }
    dispatch[args.cmd]()

if __name__ == "__main__":
    main()
