#!/usr/bin/env python3
"""
search-agent-papers.py — 搜索 arXiv 最新的智能体方向论文并下载 PDF
用法: python3 search-agent-papers.py [output_dir] [max_papers]
"""

import urllib.request
import urllib.parse
import os
import sys
import re
import time
from datetime import datetime

output_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.getcwd(), "raw", "papers")
max_papers = int(sys.argv[2]) if len(sys.argv) > 2 else 5
os.makedirs(output_dir, exist_ok=True)

# arXiv API 搜索查询 — 智能体方向核心关键词
queries = [
    'all:"LLM agent"',
    'all:"agentic RL"',
    'all:"agent reinforcement learning"',
    'all:"tool-use" AND all:"large language model"',
    'all:"multi-agent" AND all:"reasoning"',
    'all:"autonomous agent" AND all:"planning"',
]

seen_titles = set()
papers = []

for q in queries:
    if len(papers) >= max_papers * 3:
        break
    url = f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(q)}&sortBy=submittedDate&sortOrder=descending&max_results=10"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (KarpathyWiki/1.0)"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read().decode("utf-8")
    except Exception as e:
        print(f"  [WARN] query failed: {q} -> {e}", file=sys.stderr)
        continue

    entries = data.split("<entry>")
    for entry in entries[1:]:
        if "<title>" not in entry:
            continue
        title = entry.split("<title>")[1].split("</title>")[0].strip()
        title = re.sub(r"\s+", " ", title)

        if title.lower() in seen_titles or len(title) < 20:
            continue

        try:
            published = entry.split("<published>")[1].split("</published>")[0].strip()[:10]
        except:
            published = "unknown"

        # 只保留 2025 年 4 月之后的论文（已有知识库覆盖更早的）
        if published < "2025-04-01":
            continue

        try:
            summary = entry.split("<summary>")[1].split("</summary>")[0].strip()
            summary = re.sub(r"\s+", " ", summary)
        except:
            summary = ""

        try:
            id_url = entry.split("<id>")[1].split("</id>")[0].strip()
            arxiv_id = id_url.split("/")[-1]
        except:
            arxiv_id = ""

        authors = []
        for author_block in entry.split("<author>")[1:]:
            try:
                name = author_block.split("<name>")[1].split("</name>")[0].strip()
                authors.append(name)
            except:
                break
        if len(authors) > 3:
            authors = authors[:3] + ["et al."]

        seen_titles.add(title.lower())
        papers.append({
            "title": title,
            "arxiv_id": arxiv_id,
            "published": published,
            "authors": ", ".join(authors),
            "summary": summary[:300],
        })

# 按日期排序，取最新的 max_papers 篇
papers.sort(key=lambda p: p["published"], reverse=True)
papers = papers[:max_papers]

if not papers:
    print("NO_NEW_PAPERS")
    sys.exit(0)

print(f"Found {len(papers)} new agent papers:")
print("=" * 60)

for i, p in enumerate(papers):
    print(f"\n--- Paper {i+1} ---")
    print(f"Title: {p['title']}")
    print(f"arXiv: {p['arxiv_id']}")
    print(f"Date: {p['published']}")
    print(f"Authors: {p['authors']}")
    print(f"Summary: {p['summary'][:200]}")

    if p["arxiv_id"]:
        arxiv_id = p["arxiv_id"]
        base_id = arxiv_id.split("v")[0]
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        filename = base_id.replace(".", "_").replace("/", "_")
        filepath = os.path.join(output_dir, f"{filename}.pdf")

        if os.path.exists(filepath):
            print(f"  [SKIP] Already exists: {filepath}")
        else:
            try:
                req = urllib.request.Request(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=60) as resp:
                    with open(filepath, "wb") as f:
                        f.write(resp.read())
                size = os.path.getsize(filepath)
                if size > 10000:
                    print(f"  [OK] Downloaded: {filepath} ({size//1024}KB)")
                else:
                    os.remove(filepath)
                    print(f"  [FAIL] Too small, removed: {filepath}")
            except Exception as e:
                print(f"  [FAIL] Download error: {e}", file=sys.stderr)

print(f"\nDone. Saved to {output_dir}")
