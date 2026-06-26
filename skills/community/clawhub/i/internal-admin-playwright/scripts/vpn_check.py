#!/usr/bin/env python3
from __future__ import annotations

import socket
import sys
from pathlib import Path

import yaml


def load_whitelist(skill_root: Path) -> tuple[list[str], list[str]]:
    p = skill_root / "references" / "whitelist.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return data.get("allowed_hosts", []) or [], data.get("allowed_host_suffixes", []) or []


def check_reachable(host: str, port: int = 443, timeout: float = 3.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def main() -> int:
    skill_root = Path(__file__).resolve().parents[1]
    hosts, _ = load_whitelist(skill_root)
    if not hosts:
        print("[VPN检查] 白名单为空，无法检测")
        return 2

    # 优先检查 LOGIN_URL 对应主机
    import os
    from urllib.parse import urlparse
    login_url = os.getenv("LOGIN_URL", "")
    host = urlparse(login_url).hostname if login_url else None
    target = host or hosts[0]
    ok = check_reachable(target)
    if ok:
        print(f"[VPN检查] 可连通: {target}:443")
        return 0

    print(f"[VPN检查] 无法连通 {target}:443，请先连接 L2TP/IPsec VPN")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
