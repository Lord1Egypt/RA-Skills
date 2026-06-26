"""
HuggingFace Daily Papers 抓取脚本
用法：
    python hf_papers.py [日期YYYY-MM-DD]
    不传日期则默认昨天
输出：
    hf_results.json
"""

import json
import os
import re
import sys
import time
import requests
from datetime import date, timedelta

HF_TOKEN = os.environ.get("HF_TOKEN", "")
if not HF_TOKEN:
    print("ERROR: HF_TOKEN environment variable is not set.")
    print("Get your token at: https://huggingface.co/settings/tokens")
    print('Then run: $env:HF_TOKEN = "hf_xxx"  (Windows PowerShell)')
    print('Or:      export HF_TOKEN="hf_xxx"    (macOS/Linux/Git Bash)')
    sys.exit(1)
HF_API = "https://huggingface.co"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

YESTERDAY = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
TARGET_DATE = sys.argv[1] if len(sys.argv) > 1 else YESTERDAY

print(f"[HF Papers] Target date: {TARGET_DATE}")

list_url = f"{HF_API}/api/daily_papers"
params = {"date": TARGET_DATE, "limit": 30, "sort": "publishedAt"}

print("[1/2] Fetching HF Daily Papers list...")
try:
    resp = requests.get(list_url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    papers_list = resp.json()
except Exception as e:
    print(f"FAIL: Could not fetch list: {e}")
    sys.exit(1)

if not papers_list:
    print("WARNING: No papers found. Try RFC 3339 date format (YYYY-MM-DD).")
    papers_list = []

print(f"   Got {len(papers_list)} papers")

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

results = []
total = len(papers_list)

for i, paper_entry in enumerate(papers_list, 1):
    paper_obj = paper_entry.get("paper") or paper_entry
    paper_id = paper_obj.get("id", "")
    if not paper_id:
        continue

    title = paper_entry.get("title") or paper_obj.get("title", "Unknown")
    summary = clean_text(paper_entry.get("summary") or paper_obj.get("summary", ""))
    ai_summary = clean_text(paper_entry.get("ai_summary") or paper_obj.get("ai_summary", ""))
    upvotes = paper_entry.get("upvotes", 0)

    submitted_raw = paper_entry.get("submittedOnDailyBy") or paper_entry.get("submittedBy") or {}
    submitted_by = submitted_raw.get("fullname") or submitted_raw.get("name") or ""

    org_raw = paper_entry.get("organization") or paper_obj.get("organization") or {}
    org_name = org_raw.get("fullname") or org_raw.get("name") or ""

    github_repo = paper_entry.get("githubRepo") or paper_obj.get("githubRepo") or ""
    keywords = paper_entry.get("ai_keywords") or paper_obj.get("ai_keywords") or []

    hf_link = f"https://huggingface.co/papers/{paper_id}"
    arxiv_link = f"https://arxiv.org/abs/{paper_id}"

    print(f"   [{i}/{total}] {paper_id} -- {title[:55]}...")

    results.append({
        "paperId": paper_id,
        "title": title,
        "votes": upvotes,
        "submittedBy": submitted_by,
        "organization": org_name,
        "link": hf_link,
        "arxivLink": arxiv_link,
        "summary": summary[:2000],
        "aiSummary": ai_summary[:500],
        "githubRepo": github_repo,
        "keywords": keywords[:10],
    })

    time.sleep(0.25)

output_path = "hf_results.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nDone! Saved {len(results)} papers to {output_path}")
