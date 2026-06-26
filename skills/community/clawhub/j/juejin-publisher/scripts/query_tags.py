#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_tags.py: 查询掘金标签 ID
Usage: python3 query_tags.py <关键词>
"""

import sys
import json
import urllib.request
import urllib.parse

API_URL = "https://api.juejin.cn/tag_api/v1/query_tag_list"

def search_tags(keyword):
    params = urllib.parse.urlencode({
        "key_word": keyword,
        "cursor": "0",
        "limit": "20",
    })
    url = f"{API_URL}?{params}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://juejin.cn/",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    tags = data.get("data", [])
    if not tags:
        print(f"未找到与 '{keyword}' 相关的标签")
        return

    print(f"\n🏷️  与 '{keyword}' 相关的掘金标签：\n")
    print(f"{'标签名称':<20} {'tag_id'}")
    print("-" * 50)
    for tag in tags:
        name = tag.get("tag_name", "")
        tid  = tag.get("id", "")
        print(f"{name:<20} {tid}")
    print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 query_tags.py <关键词>")
        sys.exit(1)
    search_tags(sys.argv[1])
