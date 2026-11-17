#!/usr/bin/env python3
"""从苹果系统更新目录 (sucatalog) 中解析最新 Command Line Tools 安装包的 CDN 直链。

用法:
    python3 find_clt_packages.py [--catalog-index 15] [--all]

输出: 每行一个产品 (PostDate | 产品Key | 主包URL)，加 --all 列出全部历史版本。
"""
import argparse
import plistlib
import re
import subprocess
import sys
import tempfile
import urllib.request

# 已知可用的 sucatalog 地址（macOS 版本 -> 完整版本链）
CATALOG_URLS = {
    "15": "https://swscan.apple.com/content/catalogs/others/index-15-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog",
    "14": "https://swscan.apple.com/content/catalogs/others/index-14-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog",
    "13": "https://swscan.apple.com/content/catalogs/others/index-13-12-10.16-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog",
}


def fetch(url: str) -> bytes:
    """优先走 shell 环境(可能带代理)，失败则回退 urllib。"""
    try:
        r = subprocess.run(
            ["curl", "-sL", "--retry", "3", "--connect-timeout", "15", url],
            capture_output=True, timeout=180,
        )
        if r.returncode == 0 and len(r.stdout) > 10000:
            return r.stdout
    except Exception:
        pass
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog-index", default="15", help="macOS 主版本号，如 15")
    ap.add_argument("--all", action="store_true", help="列出全部 CLT 产品而非仅最新")
    args = ap.parse_args()

    url = CATALOG_URLS.get(args.catalog_index)
    if not url:
        print(f"错误: 未内置 macOS {args.catalog_index} 的 sucatalog 地址，请手动确认目录 URL", file=sys.stderr)
        return 2

    data = fetch(url)
    try:
        cat = plistlib.loads(data)
    except Exception as e:
        print(f"错误: 目录解析失败 ({e})。下载大小 {len(data)} 字节，可能是网络问题返回了错误页", file=sys.stderr)
        return 2

    products = cat.get("Products", {})
    results = []
    for key, prod in products.items():
        pkgs = prod.get("Packages", []) or []
        for p in pkgs:
            u = p.get("URL", "")
            if "CLTools_Executables.pkg" in u:
                post = str(prod.get("PostDate", ""))
                results.append((post, key, pkgs))
                break

    if not results:
        print("错误: 目录中未找到 CLTools_Executables.pkg 产品", file=sys.stderr)
        return 1

    results.sort(reverse=True)
    show = results if args.all else results[:1]
    for post, key, pkgs in show:
        total = sum(p.get("Size", 0) for p in pkgs)
        print(f"# PostDate: {post} | Product: {key} | 总大小约 {total/1024/1024:.0f} MB")
        for p in pkgs:
            print(p["URL"])
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
