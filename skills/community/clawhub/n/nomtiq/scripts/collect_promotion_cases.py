#!/usr/bin/env python3
"""
每2小时收集 nomtiq 类似产品的推广案例
结果追加到 promotion-cases/YYYY-MM-DD.md
"""
import subprocess
import json
import sys
import os
from datetime import datetime

WORKSPACE = "/Users/mac/.openclaw/workspace"
OUTPUT_DIR = f"{WORKSPACE}/skills/nomtiq/promotion-cases"
HUB = f"{WORKSPACE}/skills/search-hub/scripts/hub.py"

QUERIES = [
    "openclaw skill clawhub new launch promotion community",
    "restaurant finder app AI personal taste launch growth",
    "小红书 OpenClaw skill 推广 用户增长",
    "Show HN openclaw skill food recommendation",
]

def search(query):
    try:
        result = subprocess.run(
            ["python3.13", HUB, "search", query, "-t", "text", "-l", "3"],
            capture_output=True, text=True, timeout=30
        )
        data = json.loads(result.stdout)
        return data.get("results", [])
    except Exception as e:
        return []

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%H:%M")
    output_file = f"{OUTPUT_DIR}/{today}.md"
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    lines = [f"\n## {now} 收集\n"]
    
    for query in QUERIES:
        results = search(query)
        if not results:
            continue
        lines.append(f"\n### 搜索：{query}\n")
        for r in results:
            title = r.get("title", "")
            url = r.get("url", "")
            snippet = r.get("snippet", "")[:120]
            if title and url:
                lines.append(f"- [{title}]({url})\n  {snippet}\n")
    
    if len(lines) > 1:
        with open(output_file, "a") as f:
            f.writelines(lines)
        print(f"✅ 已追加到 {output_file}")
    else:
        print("无新结果")

if __name__ == "__main__":
    main()
