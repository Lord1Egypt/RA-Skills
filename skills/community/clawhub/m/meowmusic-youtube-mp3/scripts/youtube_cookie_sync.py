#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
import tempfile
import urllib.request


def export_cookies(cookie_txt, browser, profile):
    browser_spec = browser if not profile else f"{browser}:{profile}"
    cmd = [
        "yt-dlp",
        "--cookies-from-browser", browser_spec,
        "--cookies", cookie_txt,
        "--skip-download",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    ]
    print("+", " ".join(cmd))

    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        if os.path.exists(cookie_txt) and os.path.getsize(cookie_txt) > 100:
            print("cookie 已导出，忽略本地 yt-dlp 校验失败，继续上传...")
            return
        raise


def push_cookies(server, token, cookie_txt):
    with open(cookie_txt, "r", encoding="utf-8") as f:
        content = f.read()

    data = json.dumps({"content": content}).encode("utf-8")
    req = urllib.request.Request(
        server.rstrip("/") + "/api/admin/youtube-cookie/update",
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token,
        },
    )
    with urllib.request.urlopen(req) as resp:
        print(resp.read().decode("utf-8", "replace"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browser", default="chrome", help="浏览器类型，如 chrome / edge / firefox")
    parser.add_argument("--profile", default="Default", help="浏览器 Profile，如 Default / Profile 1 / Profile 2")
    parser.add_argument("--server", default=os.environ.get("MEOW_SERVER_URL", "http://127.0.0.1:2233"))
    parser.add_argument("--token", default=os.environ.get("MEOW_BEARER_TOKEN", ""))
    args = parser.parse_args()

    if not args.token:
        print("缺少 token：请传 --token 或设置环境变量 MEOW_BEARER_TOKEN", file=sys.stderr)
        sys.exit(1)

    with tempfile.TemporaryDirectory() as td:
        cookie_txt = os.path.join(td, "youtube-cookies.txt")
        export_cookies(cookie_txt, args.browser, args.profile)

        if not os.path.exists(cookie_txt) or os.path.getsize(cookie_txt) <= 100:
            print("cookie 文件导出失败", file=sys.stderr)
            sys.exit(1)

        push_cookies(args.server, args.token, cookie_txt)
        print("cookie sync ok")


if __name__ == "__main__":
    main()
