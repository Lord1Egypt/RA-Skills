#!/usr/bin/env python3
"""Mint a fresh access link for the resident Go Next Move HTTP service.

This is the small, fast, one-shot command the agent runs (e.g. through an
OpenClaw elevated host bridge). It does not start or stop anything:

1. Sign a fresh token (default 5 hours) with the shared secret.
2. Read the resident service's current public tunnel URL from the state dir.
3. Print the full link `https://<tunnel-host>/?token=<token>`.

The token changes on every call; the tunnel URL is whatever the resident
service currently has. Both are obtained here in one step. To revoke every
previously issued link, pass `--rotate-secret`.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from skill_token import (  # noqa: E402
    DEFAULT_SECRET_PATH,
    DEFAULT_STATE_DIR,
    DEFAULT_TTL_SECONDS,
    load_or_create_secret,
    mint_token,
    rotate_secret,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Mint a fresh link for the resident Go Next Move service.")
    parser.add_argument("--ttl-hours", type=float, default=DEFAULT_TTL_SECONDS / 3600, help="Link validity in hours, default: 5")
    parser.add_argument("--secret-path", type=Path, default=DEFAULT_SECRET_PATH, help="Secret file path")
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR, help="State dir holding the tunnel URL")
    parser.add_argument("--rotate-secret", action="store_true", help="Rotate the secret first, invalidating all existing links")
    parser.add_argument("--json", action="store_true", help="Print a JSON object instead of just the link")
    args = parser.parse_args()

    if args.rotate_secret:
        secret = rotate_secret(args.secret_path)
    else:
        secret = load_or_create_secret(args.secret_path)

    tunnel_file = Path(args.state_dir) / "tunnel_url"
    if not tunnel_file.exists():
        sys.stderr.write(
            "未找到隧道地址。常驻服务可能没在运行。\n"
            "请先在宿主机启动：python3 scripts/launch_skill_server.py\n"
        )
        return 1
    base = tunnel_file.read_text(encoding="utf-8").strip()
    if not base:
        sys.stderr.write("隧道地址为空，常驻服务可能正在重连，请稍后重试。\n")
        return 1

    ttl_seconds = int(args.ttl_hours * 3600)
    token = mint_token(secret, ttl_seconds=ttl_seconds)
    link = f"{base}/?token={token}"

    if args.json:
        print(json.dumps({"link": link, "tunnel": base, "ttl_hours": args.ttl_hours}, ensure_ascii=False))
    else:
        print(link)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
