#!/usr/bin/env python3
"""
IT运维工具箱 - 服务状态检查模块
支持: Systemd服务、Docker容器、数据库连通性、Web服务健康检查
用法: python service_check.py <command> [args...]
"""

import sys
import os
import subprocess
import socket
import json
import time
import re
import argparse
import urllib.request
import urllib.error

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

def section(title):
    print(f"\n{bold('═' * 55)}")
    print(f"  {bold(title)}")
    print(bold('═' * 55))

IS_WIN   = sys.platform == "win32"
IS_LINUX = sys.platform == "linux"

def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           shell=isinstance(cmd, str))
        return r.stdout.strip(), r.stderr.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", -1
    except Exception as e:
        return "", str(e), -1

# ─────────────────────────────────────────────
# Systemd 服务检查 (Linux)
# ─────────────────────────────────────────────

def cmd_systemd(services=None):
    section("Systemd 服务状态检查")
    if IS_WIN:
        print(warn("Systemd 仅在 Linux 系统上可用"))
        return

    if services:
        svc_list = services
    else:
        # 获取所有active服务
        out, _, _ = run("systemctl list-units --type=service --state=active --no-pager --no-legend")
        svc_list = [line.split()[0] for line in out.splitlines() if line.strip()]

    if not svc_list:
        print(info("未指定服务，或无运行中的服务"))
        return

    print(f"  {'服务名':<35} {'状态':<10} {'激活状态'}")
    print(f"  {'─'*35} {'─'*10} {'─'*10}")

    for svc in svc_list:
        out, _, _ = run(["systemctl", "is-active", svc])
        active = out.strip()
        out2, _, _ = run(["systemctl", "is-enabled", svc])
        enabled = out2.strip()

        if active == "active":
            status_icon = ok("运行中")
        elif active == "inactive":
            status_icon = warn("已停止")
        elif active == "failed":
            status_icon = err("失败")
        else:
            status_icon = color(active, "33")

        enabled_icon = ok("开机启动") if enabled == "enabled" else info(enabled)
        print(f"  {svc:<35} {status_icon:<20} {enabled_icon}")

# ─────────────────────────────────────────────
# Windows 服务检查
# ─────────────────────────────────────────────

def cmd_win_services(services=None):
    section("Windows 服务状态检查")
    if not IS_WIN:
        print(warn("此功能仅在 Windows 上可用"))
        return

    if services:
        filter_names = ",".join(f'"{s}"' for s in services)
        cmd = f"powershell -Command \"Get-Service {' '.join(services)} | Select-Object Name,Status,StartType | ConvertTo-Json\""
    else:
        # 常见服务
        cmd = "powershell -Command \"Get-Service | Where-Object {$_.Status -eq 'Stopped' -and $_.StartType -eq 'Automatic'} | Select-Object Name,Status,StartType | ConvertTo-Json\""

    out, _, _ = run(cmd)
    try:
        items = json.loads(out) if out else []
        if isinstance(items, dict): items = [items]
        if not items:
            print(ok("所有自动启动服务均正常运行"))
            return
        print(f"  {'服务名':<40} {'状态':<12} {'启动类型'}")
        print(f"  {'─'*40} {'─'*12} {'─'*10}")
        for item in items:
            name = item.get("Name", "N/A")
            status = item.get("Status", "N/A")
            stype  = item.get("StartType", "N/A")
            if str(status) == "4":   # Running
                si = ok("运行中")
            elif str(status) == "1": # Stopped
                si = warn("已停止")
            else:
                si = info(str(status))
            print(f"  {name:<40} {si:<20} {stype}")
    except Exception:
        print(out)

# ─────────────────────────────────────────────
# Docker 容器检查
# ─────────────────────────────────────────────

def cmd_docker(show_all=False):
    section("Docker 容器状态")
    flag = "-a" if show_all else ""
    out, stderr, rc = run(f"docker ps {flag} --format \"{{{{json .}}}}\"")

    if rc != 0:
        if "not found" in stderr or "not recognized" in stderr:
            print(err("Docker 未安装或不在 PATH 中"))
        elif "permission denied" in stderr:
            print(err("权限不足，请使用 sudo 或将用户加入 docker 组"))
        elif "Cannot connect" in stderr:
            print(err("Docker Daemon 未启动，请执行: systemctl start docker"))
        else:
            print(err(f"Docker 命令执行失败: {stderr[:200]}"))
        return

    if not out:
        print(info("无运行中的容器" + ("（含已停止）" if show_all else "")))
        return

    containers = []
    for line in out.splitlines():
        try:
            containers.append(json.loads(line))
        except Exception:
            pass

    print(f"  {'容器名':<25} {'镜像':<30} {'状态':<15} {'端口'}")
    print(f"  {'─'*25} {'─'*30} {'─'*15} {'─'*20}")

    for c in containers:
        name   = c.get("Names", "N/A")[:24]
        image  = c.get("Image", "N/A")[:29]
        status = c.get("Status", "N/A")
        ports  = c.get("Ports", "")[:30]

        if "Up" in status:
            si = ok(status[:14])
        elif "Exited" in status:
            si = err(status[:14])
        elif "Paused" in status:
            si = warn(status[:14])
        else:
            si = info(status[:14])

        print(f"  {name:<25} {image:<30} {si:<25} {ports}")

    # 汇总
    running = sum(1 for c in containers if "Up" in c.get("Status",""))
    total   = len(containers)
    print(f"\n  {ok(f'运行中: {running}/{total} 个容器')}")

def cmd_docker_logs(container, tail=50):
    section(f"Docker 容器日志: {container} (最近 {tail} 行)")
    out, stderr, rc = run(["docker", "logs", "--tail", str(tail), "--timestamps", container])
    if rc != 0:
        print(err(f"获取日志失败: {stderr}"))
    else:
        print(out if out else info("(无日志输出)"))

# ─────────────────────────────────────────────
# 数据库连通性测试
# ─────────────────────────────────────────────

def test_tcp_connect(host, port, label, timeout=5):
    try:
        start = time.time()
        sock = socket.create_connection((host, port), timeout=timeout)
        elapsed = (time.time() - start) * 1000
        sock.close()
        print(f"  {ok(label)}: {host}:{port}  响应 {elapsed:.1f}ms")
        return True
    except socket.timeout:
        print(f"  {err(label)}: {host}:{port}  连接超时")
        return False
    except ConnectionRefusedError:
        print(f"  {err(label)}: {host}:{port}  连接被拒绝（服务未启动？）")
        return False
    except Exception as e:
        print(f"  {err(label)}: {host}:{port}  {e}")
        return False

DB_DEFAULT_PORTS = {
    "mysql":    3306,
    "postgres": 5432,
    "redis":    6379,
    "mongodb":  27017,
    "mssql":    1433,
    "oracle":   1521,
    "es":       9200,
    "kafka":    9092,
    "zk":       2181,
    "rabbitmq": 5672,
    "memcached":11211,
}

def cmd_dbconn(spec):
    """
    spec 格式: mysql://host:port 或 redis://host 或直接 host:port
    """
    section("数据库连通性测试")
    items = spec if isinstance(spec, list) else [spec]
    for item in items:
        m = re.match(r"^([a-z]+)://([^:]+)(?::(\d+))?$", item)
        if m:
            db_type = m.group(1)
            host    = m.group(2)
            port    = int(m.group(3)) if m.group(3) else DB_DEFAULT_PORTS.get(db_type, 80)
            label   = db_type.upper()
        elif ":" in item:
            host, port_str = item.rsplit(":", 1)
            port = int(port_str)
            label = "TCP"
        else:
            print(err(f"无法解析: {item}，格式应为 mysql://host:port 或 host:port"))
            continue
        test_tcp_connect(host, port, label)

# ─────────────────────────────────────────────
# Web 服务健康检查
# ─────────────────────────────────────────────

def cmd_healthcheck(endpoints, timeout=10):
    section("Web 服务健康检查")
    if isinstance(endpoints, str):
        endpoints = [endpoints]

    for ep in endpoints:
        if not ep.startswith(("http://", "https://")):
            ep = "http://" + ep
        try:
            start = time.time()
            req = urllib.request.Request(ep, headers={"User-Agent": "WorkBuddy-HealthCheck/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                elapsed = (time.time() - start) * 1000
                code = resp.status
                if 200 <= code < 300:
                    print(f"  {ok(str(code))}  {elapsed:6.0f}ms  {ep}")
                elif 300 <= code < 400:
                    print(f"  {warn(str(code))}  {elapsed:6.0f}ms  {ep} → {resp.url}")
                else:
                    print(f"  {err(str(code))}  {elapsed:6.0f}ms  {ep}")
        except urllib.error.HTTPError as e:
            print(f"  {err(str(e.code))}  N/A  {ep}  ({e.reason})")
        except urllib.error.URLError as e:
            print(f"  {err('ERR')}  N/A  {ep}  ({e.reason})")
        except Exception as e:
            print(f"  {err('ERR')}  N/A  {ep}  ({e})")

# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────

def main():
    if sys.platform == "win32":
        os.system("")

    parser = argparse.ArgumentParser(description="IT运维工具箱 - 服务检查")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("systemd",  help="Systemd服务状态 (Linux)")
    p.add_argument("services", nargs="*")

    p = sub.add_parser("winsvc",   help="Windows服务状态")
    p.add_argument("services", nargs="*")

    p = sub.add_parser("docker",   help="Docker容器列表")
    p.add_argument("-a", "--all",  action="store_true")

    p = sub.add_parser("dlogs",    help="Docker容器日志")
    p.add_argument("container")
    p.add_argument("-n", "--tail", type=int, default=50)

    p = sub.add_parser("dbconn",   help="数据库连通性测试")
    p.add_argument("specs", nargs="+", help="如: mysql://127.0.0.1:3306 redis://127.0.0.1")

    p = sub.add_parser("health",   help="Web服务健康检查")
    p.add_argument("endpoints", nargs="+")
    p.add_argument("-t", "--timeout", type=int, default=10)

    args = parser.parse_args()
    dispatch = {
        "systemd": lambda: cmd_systemd(args.services or None),
        "winsvc":  lambda: cmd_win_services(args.services or None),
        "docker":  lambda: cmd_docker(args.all),
        "dlogs":   lambda: cmd_docker_logs(args.container, args.tail),
        "dbconn":  lambda: cmd_dbconn(args.specs),
        "health":  lambda: cmd_healthcheck(args.endpoints, args.timeout),
    }
    dispatch[args.cmd]()

if __name__ == "__main__":
    main()
