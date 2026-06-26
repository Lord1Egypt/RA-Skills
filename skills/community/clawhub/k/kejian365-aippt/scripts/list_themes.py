#!/usr/bin/env python3
"""List available PPT themes. Each theme line: THEME: id|name|style|scene|vip_flag"""

import argparse, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def _utf8_stdio():
    for a in ("stdout", "stderr"):
        s = getattr(sys, a)
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
        elif hasattr(s, "buffer"):
            setattr(sys, a, io.TextIOWrapper(s.buffer, encoding="utf-8", errors="replace", line_buffering=True))
_utf8_stdio()

from http_client import SkillHttpClient, SkillHttpError

BASE_URL = "https://kejian365.com/api"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--page",      type=int, default=1)
    p.add_argument("--page-size", type=int, default=100)
    args = p.parse_args()
    token = os.environ.get("KEJIAN365_AUTH_TOKEN", "")
    if not token:
        print("ERROR: 缺少账号凭证", flush=True); sys.exit(1)

    client = SkillHttpClient(auth_token=token, timeout=10)
    try:
        result = client.get(f"{BASE_URL}/aippt/v1/skill/themes",
                            {"page": args.page, "pageSize": args.page_size})
    except SkillHttpError as e:
        print(f"ERROR: {e}", flush=True)
        sys.exit(1)

    if result.get("rspCode") != "0000":
        print(f"ERROR: {result.get('rspDesc', '获取主题失败')}", flush=True)
        sys.exit(1)

    data = result.get("data") or {}
    rows = data.get("list") or data.get("rows") or []
    if not rows:
        print("ERROR: 主题列表为空，请检查账号权限或稍后重试", flush=True)
        sys.exit(1)

    print(f"COUNT: {len(rows)}", flush=True)
    for t in rows:
        tid   = t.get("theme_id", "")
        name  = t.get("theme_name", "")
        style = t.get("style", "")
        scene = t.get("scene", "")
        print(f"THEME: {tid}|{name}|{style}|{scene}", flush=True)

if __name__ == "__main__":
    main()
