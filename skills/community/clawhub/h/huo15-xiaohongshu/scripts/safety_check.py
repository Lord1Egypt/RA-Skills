#!/usr/bin/env python3
"""抓取前做一次自检：Cookie 是否有效、是否会被风控拦、当前节奏是否合理。

用法：
    export XHS_COOKIE='...'
    python3 safety_check.py
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xhs_client import XHSClient, load_cookie_from_env, XHSError, BlockedByCaptcha, LoginRequired  # noqa: E402
from xhs_parser import extract_initial_state  # noqa: E402


def main() -> int:
    print("=== 火一五小红书抓取自检 ===\n")

    # 1. Cookie 检查
    try:
        cookie = load_cookie_from_env()
    except LoginRequired as e:
        print("❌", e)
        return 1
    cookie_count = len([c for c in cookie.split(";") if c.strip()])
    print(f"✓ Cookie 字段数：{cookie_count}（通常 10+）")
    for key in ("web_session", "a1", "webId", "xsecappid"):
        found = any(c.strip().startswith(key + "=") for c in cookie.split(";"))
        mark = "✓" if found else "⚠"
        print(f"   {mark} 包含 {key}" + ("" if found else "（缺失，部分接口可能不稳定）"))

    # 2. 访问首页看一下风控
    print("\n--- 访问 xiaohongshu.com 首页 ---")
    client = XHSClient(cookie=cookie, min_delay=1, max_delay=2, max_requests_per_session=5)
    try:
        resp = client.session.get("https://www.xiaohongshu.com/explore", timeout=10,
                                  headers=client._base_headers())
        if resp.status_code == 200:
            print(f"✓ HTTP 200 — 首页可达（{len(resp.text)} bytes）")
        else:
            print(f"⚠ HTTP {resp.status_code} — 可能已经被限制")
        state = extract_initial_state(resp.text)
        if state:
            print(f"✓ __INITIAL_STATE__ 解析成功（顶层 key {len(state)} 个）")
        else:
            print("⚠ 未找到 __INITIAL_STATE__ — HTML 结构可能变了，或页面被重定向")
    except XHSError as e:
        print(f"❌ {e}")
        return 1
    except Exception as e:
        print(f"❌ 网络错误：{e}")
        return 1

    # 3. 节奏建议
    print("\n--- 节奏建议 ---")
    print("  • 单次会话建议不超过 30 次请求（默认 max_requests_per_session=30）")
    print("  • 每次请求间隔 3~7 秒（默认 min_delay=3, max_delay=7）")
    print("  • 两次会话之间至少间隔 10~30 分钟")
    print("  • 一天内对同一账号不要超过 4~5 次脚本访问")
    print("  • 任何 460/461/403 或验证码提示，立即停手，进浏览器手动操作恢复")

    print("\n✓ 自检完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
