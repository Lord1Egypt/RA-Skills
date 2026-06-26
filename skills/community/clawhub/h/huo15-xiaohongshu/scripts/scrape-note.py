#!/usr/bin/env python3
"""抓单条笔记详情。

用法：
    export XHS_COOKIE='a=b; c=d; ...'   # 登录后复制浏览器 Cookie
    python3 scrape-note.py --note-id 64abc... --out /tmp/note.json
    python3 scrape-note.py --url "https://www.xiaohongshu.com/explore/64abc...?xsec_token=xxx" \
        --out /tmp/note.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).parent))

from xhs_client import XHSClient, load_cookie_from_env, XHSError  # noqa: E402
from xhs_parser import parse_note_page, note_to_dict  # noqa: E402


def _parse_url(url: str):
    """从 URL 抽取 note_id / xsec_token。"""
    m = re.search(r"/explore/([0-9a-zA-Z]+)", url)
    note_id = m.group(1) if m else ""
    qs = parse_qs(urlparse(url).query)
    xsec = (qs.get("xsec_token") or [""])[0]
    xsec_src = (qs.get("xsec_source") or ["pc_feed"])[0]
    return note_id, xsec, xsec_src


def main() -> int:
    ap = argparse.ArgumentParser(description="抓单条小红书笔记")
    ap.add_argument("--note-id")
    ap.add_argument("--url")
    ap.add_argument("--xsec-token", default="")
    ap.add_argument("--xsec-source", default="pc_feed")
    ap.add_argument("--out", "-o", default="", help="JSON 输出路径，省略则 stdout")
    ap.add_argument("--save-html", default="", help="同时保存原始 HTML（调试用）")
    ap.add_argument("--min-delay", type=float, default=3.0)
    ap.add_argument("--max-delay", type=float, default=7.0)
    args = ap.parse_args()

    note_id, xsec, xsec_src = args.note_id or "", args.xsec_token, args.xsec_source
    if args.url:
        parsed_id, parsed_xsec, parsed_src = _parse_url(args.url)
        note_id = note_id or parsed_id
        xsec = xsec or parsed_xsec
        xsec_src = parsed_src or xsec_src

    if not note_id:
        print("必须提供 --note-id 或 --url", file=sys.stderr)
        return 2

    try:
        cookie = load_cookie_from_env()
    except Exception as e:
        print(str(e), file=sys.stderr)
        return 2

    client = XHSClient(cookie=cookie, min_delay=args.min_delay, max_delay=args.max_delay)
    try:
        html = client.get_explore_page(note_id, xsec_token=xsec, xsec_source=xsec_src)
    except XHSError as e:
        print(f"抓取失败：{e}", file=sys.stderr)
        return 1

    if args.save_html:
        Path(args.save_html).write_text(html, encoding="utf-8")

    note = parse_note_page(html, note_id=note_id)
    if not note:
        print("解析失败 — HTML 里没找到 __INITIAL_STATE__，可能 Cookie 失效或被风控。", file=sys.stderr)
        if not args.save_html:
            print("加 --save-html /tmp/raw.html 查看原始页面。", file=sys.stderr)
        return 1

    data = note_to_dict(note)
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}（标题：{note.title[:40] or '(空)'}）")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
