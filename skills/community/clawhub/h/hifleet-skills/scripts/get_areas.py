#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取区域清单（海区、贸易区），供用户按名称选择区域后使用 areaId 查询区域船舶。
可选配置环境变量 `HIFLEET_API_KEY`（传 `api_key` 时 `includeBound` 才生效）。
可选 `HIFLEET_API_BASE`（默认 https://api.hifleet.com，无末尾斜杠）。

用法:
  python get_areas.py [--include-bound]
  无参数时仅返回区域列表；--include-bound 时返回边界 WKT（需 `api_key` 有效）。

Security: 仅向 HIFLEET_API_BASE 下 position/areas/token 发起 GET；标准库 only。
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request


def api_base():
    return (os.environ.get("HIFLEET_API_BASE") or "https://api.hifleet.com").rstrip("/")


def get_api_key():
    return os.environ.get("HIFLEET_API_KEY")


def get_areas(api_key: str = None, include_bound: bool = False) -> dict:
    params = {}
    if api_key:
        params["api_key"] = api_key
    if include_bound:
        params["includeBound"] = "true"
    url = api_base() + "/position/areas/token" + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main():
    parser = argparse.ArgumentParser(description="获取区域清单（海区、贸易区）")
    parser.add_argument(
        "--include-bound",
        action="store_true",
        help="是否返回边界 WKT（仅 api_key 有效时生效）",
    )
    args = parser.parse_args()

    api_key = get_api_key() if args.include_bound else None
    if args.include_bound and not api_key:
        print("使用 --include-bound 时请配置 HIFLEET_API_KEY", file=sys.stderr)
        sys.exit(1)

    try:
        data = get_areas(api_key=api_key, include_bound=args.include_bound)
    except Exception as e:
        print("请求失败: %s" % e, file=sys.stderr)
        sys.exit(1)

    if data.get("result") != "ok":
        print(json.dumps(data, ensure_ascii=False, indent=2), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
