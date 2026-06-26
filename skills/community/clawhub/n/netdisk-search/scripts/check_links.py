#!/usr/bin/env python3
"""网盘链接有效性检测脚本"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import re

# ========== 网盘类型自动识别 ==========
DISK_PATTERNS = {
    "quark": r"pan\.quark\.cn",
    "baidu": r"pan\.baidu\.com",
    "aliyun": r"www\.alipan\.com|aliyundrive\.com",
    "xunlei": r"pan\.xunlei\.com",
    "115": r"115\.com|115cdn\.com",
    "tianyi": r"cloud\.189\.cn",
    "uc": r"drive\.uc\.cn",
    "mobile": r"caiyun\.139\.com|yun\.139\.com",
    "123": r"123pan\.com|123912\.com",
    "pikpak": r"mypikpak\.com",
    "mega": r"mega\.nz",
    " lanzou": r"lanzou[a-z]?\.com",
}

CLOUD_NAMES = {
    "quark": "夸克网盘", "baidu": "百度网盘", "aliyun": "阿里云盘",
    "ali": "阿里云盘", "alipan": "阿里云盘", "xunlei": "迅雷网盘",
    "115": "115网盘", "tianyi": "天翼云盘", "uc": "UC网盘",
    "mobile": "移动云盘", "123": "123网盘", "pikpak": "PikPak",
    "mega": "MEGA", "lanzou": "蓝奏云", "magnet": "磁力链接",
    "ed2k": "电驴链接", "others": "其他",
}

STATUS_ICON = {
    "ok": "✅", "bad": "❌", "locked": "🔒",
    "unsupported": "⚠️", "uncertain": "❓",
}


def detect_api(explicit=None):
    """探测 API 地址"""
    candidates = []
    if explicit:
        candidates.append(explicit)
    env = os.environ.get("NETDISK_API_URL")
    if env:
        candidates.append(env)
    candidates.append("http://localhost:8888")

    for url in candidates:
        try:
            req = urllib.request.Request(f"{url}/api/health", method="GET")
            resp = urllib.request.urlopen(req, timeout=3)
            if resp.status < 500:
                return url
        except Exception:
            continue
    return candidates[-1] if candidates else "http://localhost:8888"


def detect_disk_type(url):
    """从 URL 自动识别网盘类型"""
    for dtype, pattern in DISK_PATTERNS.items():
        if re.search(pattern, url):
            return dtype
    return "others"


def check_links(api_url, items, proxy_url=None):
    """调用 搜索 API 检测链接"""
    payload = {"items": items}
    if proxy_url:
        payload["proxy_url"] = proxy_url

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{api_url}/api/check/links",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"❌ API 错误 ({e.code}): {body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"❌ 连接失败: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="网盘链接检测")
    parser.add_argument("--url", action="append", help="待检测链接（可多次指定）")
    parser.add_argument("--file", help="从文件读取链接（每行一个）")
    parser.add_argument("--type", help="网盘类型（不指定则自动识别）")
    parser.add_argument("--password", default="", help="提取码")
    parser.add_argument("--proxy", help="代理地址（socks5://...）")
    parser.add_argument("--api", help="搜索 API 地址")
    parser.add_argument("--format", choices=["terminal", "json"], default="terminal")
    args = parser.parse_args()

    urls = list(args.url or [])
    if args.file:
        with open(args.file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    urls.append(line)

    if not urls:
        parser.print_help()
        print("\n❌ 请提供至少一个链接 (--url 或 --file)")
        sys.exit(1)

    # 构造检测请求
    items = []
    for url in urls:
        dtype = args.type or detect_disk_type(url)
        items.append({"disk_type": dtype, "url": url, "password": args.password})

    api_url = detect_api(args.api)

    if args.format == "terminal":
        print(f"🔗 检测 {len(items)} 个链接... (API: {api_url})")

    result = check_links(api_url, items, args.proxy)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Terminal 输出
    all_ok = True
    for r in result.get("results", []):
        state = r.get("state", "uncertain")
        icon = STATUS_ICON.get(state, "❓")
        url = r.get("url", "")
        summary = r.get("summary", "")
        dtype = r.get("disk_type", "")
        name = CLOUD_NAMES.get(dtype, dtype)
        print(f"{icon} [{name}] {url}")
        print(f"   {summary}")
        if state not in ("ok", "locked"):
            all_ok = False

    ok_count = sum(1 for r in result.get("results", []) if r.get("state") == "ok")
    total = len(result.get("results", []))
    print(f"\n📊 结果: {ok_count}/{total} 个链接有效")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
