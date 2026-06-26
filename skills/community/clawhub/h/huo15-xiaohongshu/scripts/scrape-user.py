#!/usr/bin/env python3
"""抓用户主页 + 主页列出的笔记预览。

    export XHS_COOKIE='...'
    python3 scrape-user.py --user-id 5f123abc... --out /tmp/user.json
    python3 scrape-user.py --url "https://www.xiaohongshu.com/user/profile/5f123abc..." \
        --out /tmp/user.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xhs_client import XHSClient, load_cookie_from_env, XHSError  # noqa: E402
from xhs_parser import parse_user_page, profile_to_dict  # noqa: E402


def _id_from_url(url: str) -> str:
    m = re.search(r"/user/profile/([0-9a-zA-Z]+)", url)
    return m.group(1) if m else ""


def main() -> int:
    ap = argparse.ArgumentParser(description="抓小红书用户主页")
    ap.add_argument("--user-id")
    ap.add_argument("--url")
    ap.add_argument("--out", "-o", default="")
    ap.add_argument("--save-html", default="")
    ap.add_argument("--min-delay", type=float, default=3.0)
    ap.add_argument("--max-delay", type=float, default=7.0)
    args = ap.parse_args()

    user_id = args.user_id or (_id_from_url(args.url) if args.url else "")
    if not user_id:
        print("必须提供 --user-id 或 --url", file=sys.stderr)
        return 2

    try:
        cookie = load_cookie_from_env()
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 2

    client = XHSClient(cookie=cookie, min_delay=args.min_delay, max_delay=args.max_delay)
    try:
        html = client.get_user_page(user_id)
    except XHSError as e:
        print(f"抓取失败：{e}", file=sys.stderr)
        return 1

    if args.save_html:
        Path(args.save_html).write_text(html, encoding="utf-8")

    profile = parse_user_page(html)
    if not profile:
        print("解析失败 — 可能 Cookie 失效或被风控。", file=sys.stderr)
        return 1

    data = profile_to_dict(profile)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}（昵称：{profile.nickname or '(未识别)'}，"
              f"主页笔记预览 {len(profile.recent_notes)} 条）")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
