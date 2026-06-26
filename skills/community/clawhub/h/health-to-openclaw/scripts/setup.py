#!/usr/bin/env python3
"""
Generate a QR code for pairing the Health Sync iOS app with this OpenClaw instance.
Reads gateway token from ~/.openclaw/openclaw.json automatically.
Auto-detects VPS vs local and chooses the right IP.
"""

import argparse
import json
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
DEFAULT_PORT = 18789


def read_gateway_token() -> str:
    if not OPENCLAW_CONFIG.exists():
        sys.exit("❌ 未找到 ~/.openclaw/openclaw.json，请先安装并配置 OpenClaw。")
    config = json.loads(OPENCLAW_CONFIG.read_text())
    token = config.get("gateway", {}).get("auth", {}).get("token", "")
    if not token:
        sys.exit("❌ openclaw.json 中没有 gateway token，请先运行 'openclaw gateway' 初始化。")
    return token


def get_lan_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_public_ip() -> str | None:
    for service in ["https://api.ipify.org", "https://checkip.amazonaws.com"]:
        try:
            with urllib.request.urlopen(service, timeout=4) as r:
                return r.read().decode().strip()
        except Exception:
            continue
    return None


def is_vps() -> bool:
    """True if LAN IP looks like a cloud private IP and public IP is different."""
    lan = get_lan_ip()
    pub = get_public_ip()
    if not pub:
        return False
    # On a VPS, LAN IP is typically 10.x or 172.x (private) while public IP differs
    is_private_lan = (
        lan.startswith("10.") or
        lan.startswith("172.") or
        lan == "127.0.0.1"
    )
    return is_private_lan and lan != pub


def check_port_open(host: str, port: int, timeout: float = 3.0) -> bool:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except Exception:
        return False


def ensure_gateway_running(bind_mode: str = "lan"):
    """Start/restart gateway in the specified bind mode."""
    print(f"→ 启动 OpenClaw gateway（bind={bind_mode}）...", flush=True)
    try:
        subprocess.Popen(
            ["openclaw", "gateway", "--bind", bind_mode, "--force"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(2)
    except FileNotFoundError:
        print("  警告: 未找到 openclaw 命令，请确保已安装并在 PATH 中。")
    except Exception as e:
        print(f"  警告: gateway 启动失败 ({e})")


def qr_terminal(data: str, compact: bool = False):
    """Print QR code as ASCII/UTF-8. Works in any terminal, including SSH on VPS."""
    # Try qrencode (brew/apt install qrencode)
    for mode in (["ansiutf8"] if not compact else ["ansi"]):
        try:
            result = subprocess.run(
                ["qrencode", "-t", mode, "-m", "1", data],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(result.stdout)
                return
        except FileNotFoundError:
            break

    # Try Python qrcode (pip install qrcode)
    try:
        import qrcode  # type: ignore
        qr = qrcode.QRCode(border=1)
        qr.add_data(data)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
        return
    except ImportError:
        pass

    # Auto-install and retry
    print("→ 正在安装 qrcode 库...", flush=True)
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "qrcode", "-q"],
            check=True, capture_output=True
        )
        import qrcode  # type: ignore
        qr = qrcode.QRCode(border=1)
        qr.add_data(data)
        qr.make(fit=True)
        qr.print_ascii(invert=True)
    except Exception:
        print("  (QR 码生成失败，请使用下方备用 JSON 手动配置)")


def firewall_hint(ip: str, port: int):
    print(f"\n⚠️  VPS 防火墙配置（如果手机无法连接）：")
    print(f"   Linux iptables:  sudo iptables -A INPUT -p tcp --dport {port} -j ACCEPT")
    print(f"   Ubuntu ufw:      sudo ufw allow {port}/tcp")
    print(f"   Oracle Cloud:    控制台 → VCN → Security List → 添加入站规则 TCP {port}")
    print(f"   确认后可用以下命令测试连通性（在另一台机器上）：")
    print(f"   curl http://{ip}:{port}/api/status\n")


def main():
    parser = argparse.ArgumentParser(description="生成 iOS 配对 QR 码")
    parser.add_argument("--host", help="手动指定 IP 或域名（如 VPS 有自定义域名）")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--local", action="store_true", help="强制使用局域网 IP（忽略 VPS 检测）")
    parser.add_argument("--compact", action="store_true", help="生成较小的 QR 码")
    parser.add_argument("--no-gateway", action="store_true", help="跳过 gateway 启动")
    args = parser.parse_args()

    print("\n🍎 Apple Health Sync — 配对 iOS App\n")

    # 1. Read token
    token = read_gateway_token()

    # 2. Detect environment
    if args.host:
        host = args.host.rstrip("/")
        if not host.startswith("http"):
            host = f"http://{host}"
        url = f"{host}:{args.port}"
        bind_mode = "lan"
        on_vps = False
    elif args.local:
        ip = get_lan_ip()
        url = f"http://{ip}:{args.port}"
        bind_mode = "lan"
        on_vps = False
    else:
        on_vps = is_vps()
        if on_vps:
            pub = get_public_ip()
            if not pub:
                print("⚠️  无法获取公网 IP，回退到局域网 IP。")
                pub = get_lan_ip()
            print(f"📡 检测到 VPS 环境，使用公网 IP: {pub}")
            url = f"http://{pub}:{args.port}"
            bind_mode = "lan"
        else:
            ip = get_lan_ip()
            print(f"🏠 检测到本地环境，使用局域网 IP: {ip}")
            url = f"http://{ip}:{args.port}"
            bind_mode = "lan"

    # 3. Start gateway
    if not args.no_gateway:
        ensure_gateway_running(bind_mode)

    # 4. Check connectivity
    host_check = url.replace("http://", "").split(":")[0]
    if check_port_open(host_check, args.port):
        print(f"✅ Gateway 可访问: {url}")
    else:
        print(f"⚠️  Gateway 暂时不可达: {url}")
        if on_vps:
            firewall_hint(host_check, args.port)
        else:
            print("   请确认 OpenClaw gateway 已启动：openclaw gateway --bind lan\n")

    # 5. Build QR payload
    payload = json.dumps({"url": url, "token": token}, separators=(",", ":"))

    # 6. Print QR
    print(f"\n服务地址: {url}")
    print(f"Token:    {'*' * 8}{token[-4:]}\n")
    print("扫描下方 QR 码完成配置（iOS App → 扫码自动配置）：\n")
    qr_terminal(payload, compact=args.compact)
    print(f"\n备用 JSON（手动输入）:\n{payload}\n")
    print("扫码后 App 自动连接，无需手动填写任何信息。\n")


if __name__ == "__main__":
    main()
