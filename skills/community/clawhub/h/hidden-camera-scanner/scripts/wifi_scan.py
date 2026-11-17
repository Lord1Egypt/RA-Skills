#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hidden-camera-scanner · wifi_scan.py
局域网扫描（纯 Python 实现，免 nmap）：发现联网设备并标记疑似监控摄像头 / NVR（反偷拍排查阶段①）。

合规定位：目的是帮助用户保护自身隐私、发现针对自己的非法偷拍设备。
  - 只做被动的设备发现与 TCP 端口探测，不登录任何设备、不利用漏洞、不访问摄像头视频流；
  - 仅扫描你本人已连接、有权限的网络；扫描会主动发探测包，运行前须确认范围并获得授权；
  - 扫到监控厂商设备 ≠ 有人在偷拍，需结合场景与人工排查确认。

实现与依赖：
  - 全部为 Python 标准库（subprocess ping + socket 端口探测 + ARP 表解析），零第三方硬依赖；
  - netaddr（可选）：`pip install netaddr`，启用 IEEE OUI 厂商识别；缺失时厂商为空、仅靠端口判定，
    此时能力等同 bash 版回退路径；
  - 无需 root；不需要 nmap（nmap 版能力见 wifi_scan.sh，OS 指纹/服务版本探测本技能未用到）。

用法：
  python3 wifi_scan.py [--subnet 192.168.1.0/24] [--ports 554,8554,...]
                       [--out result.json] [--no-portscan] [--timeout 1.0]

输出：JSON 到 stdout；--out 时同时写入文件；人类可读摘要到 stderr。
平台：macOS / Windows(原生 Python) / Linux(Termux)。Python 版本 >= 3.8。
"""

import argparse
import concurrent.futures as cf
import json
import re
import socket
import subprocess
import sys
import platform
import os

# 监控厂商关键字（匹配 OUI 组织名，小写比较；见 references/vendors_ports.md）
SURVEIL_KEYWORDS = [
    "hikvision", "海康", "hangzhou hikvision", "dahua", "大华", "reolink", "axis",
    "ezviz", "萤石", "imou", "乐橙", "uniview", "宇视", "tp-link", "tplink", "小米",
    "xiaomi", "d-link", "foscam", "yi tech", "小蚁", "amcrest", "wyze", "lorex",
    "swann", "tend", "wansview", "tenvis", "geovision", "奇偶", "vivotek",
    "mobotix", "hanwha", "bosch", "panasonic", "sony", "netatmo", "nest",
]
PORT_MEANING = {
    "554": "RTSP 视频流", "8554": "RTSP 备用", "3702": "ONVIF 设备发现",
    "80": "HTTP 管理界面", "8080": "HTTP 管理界面", "443": "HTTPS 管理界面",
    "8000": "海康威视 ISAPI/SDK", "34567": "大华私有协议", "37777": "大华私有协议",
    "8899": "大华/通用私有", "23": "Telnet(高危)", "21": "FTP", "1900": "UPnP/SSDP",
    "9999": "厂商私有", "49152": "厂商私有",
}
HIGH_PORTS = {"554", "8554", "3702", "8000", "34567", "37777"}

IS_MACOS = platform.system() == "Darwin"
IS_WIN = platform.system() == "Windows"

e = sys.stderr


def log(msg):
    print(msg, file=e)


# ---------- 子网探测 ----------

def detect_local_ip():
    """探测本机在默认路由网卡上的 IPv4。"""
    if IS_MACOS:
        try:
            iface = subprocess.run(
                ["route", "-n", "get", "default"], capture_output=True, text=True, timeout=5
            ).stdout
            m = re.search(r"interface:\s+(\S+)", iface)
            if m:
                out = subprocess.run(
                    ["ipconfig", "getifaddr", m.group(1)], capture_output=True, text=True, timeout=5
                ).stdout.strip()
                if out:
                    return out
        except Exception:
            pass
    elif IS_WIN:
        try:
            out = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway} "
                 "| Select-Object -First 1).IPv4Address.IPAddress"],
                capture_output=True, text=True, timeout=15,
            ).stdout.strip()
            if re.match(r"^\d+\.\d+\.\d+\.\d+$", out):
                return out
        except Exception:
            pass
    else:  # Linux / Termux
        try:
            out = subprocess.run(
                ["ip", "route", "get", "1.1.1.1"], capture_output=True, text=True, timeout=5
            ).stdout
            # 形如 "1.1.1.1 via 192.168.31.1 dev wlan0 src 192.168.31.98"
            m = re.search(r"src\s+(\d+\.\d+\.\d+\.\d+)", out)
            if m:
                return m.group(1)
        except Exception:
            pass
    # 通用兜底：UDP socket 连外网地址看本地源地址（不发包）
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        s.connect(("8.8.8.8", 53))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return ""


# ---------- 主机发现（并发 ping） ----------

def ping_args():
    if IS_MACOS:
        return ["ping", "-c", "1", "-t", "1"]
    if IS_WIN:
        return ["ping", "-n", "1", "-w", "1000"]
    return ["ping", "-c", "1", "-W", "1"]


def ping_one(ip):
    try:
        r = subprocess.run(ping_args() + [ip], capture_output=True, timeout=4)
        return ip if r.returncode == 0 else None
    except Exception:
        return None


def ping_sweep(subnet):
    o = subnet.split("/")[0].split(".")
    targets = ["{}.{}.{}.{}".format(o[0], o[1], o[2], i) for i in range(1, 255)]
    live = []
    log(f"▶ ping 探活 254 个地址（并发）...")
    with cf.ThreadPoolExecutor(max_workers=64) as pool:
        for res in pool.map(ping_one, targets):
            if res:
                live.append(res)
    return live


# ---------- ARP 表（MAC 地址） ----------

def collect_arp():
    """返回 {ip: mac}，跨平台解析。"""
    arp = {}
    try:
        if IS_WIN:
            out = subprocess.run(["arp", "-a"], capture_output=True, text=True, timeout=10).stdout
            # "  192.168.31.1  3c-84-6a-11-22-33  动态"
            for m in re.finditer(r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})\b", out):
                ip, mac = m.group(1), m.group(2).lower().replace("-", ":")
                if not ip.startswith(("224.", "239.", "255.")):
                    arp[ip] = mac
        else:
            if IS_MACOS:
                out = subprocess.run(["arp", "-a", "-n"], capture_output=True, text=True, timeout=10).stdout
                for m in re.finditer(r"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-fA-F:]{17})", out):
                    arp[m.group(1)] = m.group(2).lower()
            else:
                out = subprocess.run(["ip", "neigh", "show"], capture_output=True, text=True, timeout=10).stdout
                for line in out.splitlines():
                    f = line.split()
                    if "lladdr" in f:
                        arp[f[0]] = f[f.index("lladdr") + 1].lower()
    except Exception:
        pass
    return arp


# ---------- 厂商识别（netaddr OUI，可选） ----------

def _dig(info, *path):
    """从 dict 或 netaddr DictDotLookup 中按路径安全取值。"""
    cur = info
    for p in path:
        if cur is None:
            return None
        try:
            cur = cur[p]
        except Exception:
            try:
                cur = getattr(cur, p)
            except Exception:
                return None
    return cur


def vendor_from_mac(mac):
    if not mac:
        return ""
    try:
        from netaddr import EUI
        info = EUI(mac).info
        org = _dig(info, "org") or _dig(info, "OUI", "org") or _dig(info, "IAB", "org") or ""
        return str(org).strip()
    except ImportError:
        return ""
    except Exception:
        return ""


# ---------- 端口探测（并发 TCP connect） ----------

def probe_port(ip, port, timeout):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return (ip, port)
    except Exception:
        return None


def port_scan(live_ips, ports, timeout):
    open_hits = []
    tasks = [(ip, p) for ip in live_ips for p in ports]
    log(f"▶ TCP 端口探测 {len(live_ips)} 台设备 × {len(ports)} 个监控相关端口（并发）...")
    with cf.ThreadPoolExecutor(max_workers=128) as pool:
        futs = [pool.submit(probe_port, ip, p, timeout) for ip, p in tasks]
        for f in cf.as_completed(futs):
            r = f.result()
            if r:
                open_hits.append(r)
    return open_hits


# ---------- 主流程 ----------

def main():
    ap = argparse.ArgumentParser(description="纯 Python 局域网扫描（免 nmap，反偷拍阶段①）")
    ap.add_argument("--subnet", default="", help="扫描子网，如 192.168.1.0/24（默认自动探测）")
    ap.add_argument("--ports", default="554,8554,3702,80,8080,443,8000,34567,37777,8899,23,21,1900,9999,49152",
                    help="逗号分隔的探测端口")
    ap.add_argument("--out", default="", help="JSON 结果同时写入此文件")
    ap.add_argument("--no-portscan", action="store_true", help="跳过端口探测，仅发现设备")
    ap.add_argument("--timeout", type=float, default=0.8, help="TCP 连接超时秒数（默认 0.8）")
    args = ap.parse_args()

    local_ip = detect_local_ip()
    if not args.subnet:
        if not local_ip:
            log("无法确定本机 IP，请用 --subnet 指定（如 192.168.1.0/24）")
            sys.exit(1)
        subnet = "{}.{}.{}.0/24".format(*local_ip.split("."))
    else:
        subnet = args.subnet
    log(f"▶ 扫描子网: {subnet}（本机 {local_ip or '未知'}）")

    live = ping_sweep(subnet)
    log(f"▶ 探活设备: {len(live)} 台")

    arp = collect_arp()

    open_hits = [] if args.no_portscan else port_scan(live, [p.strip() for p in args.ports.split(",") if p.strip()], args.timeout)

    # 汇总
    hosts = {}

    def add(ip):
        if ip not in hosts:
            hosts[ip] = {"ip": ip, "mac": arp.get(ip, ""), "vendor": "", "vendor_suspect": False,
                         "open_ports": [], "flags": []}
        return hosts[ip]

    for ip in live:
        add(ip)
    for ip, port in open_hits:
        h = add(ip)
        if port not in h["open_ports"]:
            h["open_ports"].append(str(port))

    try:
        import netaddr  # noqa
        has_netaddr = True
    except ImportError:
        has_netaddr = False

    for h in hosts.values():
        h["vendor"] = vendor_from_mac(h["mac"]) if has_netaddr else ""
        v = h["vendor"].lower()
        if any(k in v for k in SURVEIL_KEYWORDS):
            h["vendor_suspect"] = True
            h["flags"].append("厂商命中监控关键字")
        for p in sorted(h["open_ports"], key=int):
            meaning = PORT_MEANING.get(p, "未知服务")
            if p in HIGH_PORTS:
                h["flags"].append(f"开放高危监控端口 {p}({meaning})")
            else:
                h["flags"].append(f"开放端口 {p}({meaning})")

    isolation = len(hosts) <= 2
    result = {
        "scan_type": "wifi",
        "subnet": subnet,
        "tool": "python-native" + ("+netaddr" if has_netaddr else ""),
        "client_isolation_suspected": isolation,
        "host_count": len(hosts),
        "hosts": sorted(hosts.values(), key=lambda x: tuple(int(x) for x in x["ip"].split("."))),
    }
    out = json.dumps(result, ensure_ascii=False, indent=2)
    print(out)
    if args.out:
        with open(args.out, "w") as f:
            f.write(out)
        log(f"▶ JSON 已写入: {args.out}")

    # 人类可读摘要（stderr）
    log("\n=== Wi-Fi 扫描摘要 ===")
    log(f"子网: {subnet} | 工具: {result['tool']} | 发现设备: {len(hosts)} 台")
    if isolation:
        log("⚠️ 疑似客户端隔离：仅发现极少设备，无法扫描其他联网设备 → 建议转人工排查（阶段④）")
    if not has_netaddr:
        log("提示: 未安装 netaddr，厂商识别不可用（pip install netaddr 可启用 IEEE OUI 库）")
    sus = [h for h in hosts.values() if h["flags"]]
    if not sus:
        log("未标记可疑设备（不代表安全：蜂窝/其他 Wi-Fi/纯本地存储的摄像头不可见）")
    for h in sus:
        log(f"  可疑 {h['ip']}  MAC {h['mac'] or '?'}  厂商[{h['vendor'] or '未知'}]")
        for fl in h["flags"]:
            log(f"    - {fl}")
    log("提示：以上仅为设备发现结果，发现监控厂商设备不等于偷拍，需结合场景与人工排查确认。")


if __name__ == "__main__":
    main()
