#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auto_discover.py — 官方政策源自动发现
从种子官方页抓取并收录合法的政策子链接到 data/sources.json。
注意: 官方站(ontario.ca/canada.ca)可能拦截直连 urllib; 优先建议用 skill 的 web_fetch。
本脚本提供CLI直连, 若失败请改用 web_fetch 抓取后的HTML喂入, 或由代理人工运行 discover。
"""
import json, os, re, sys, time, urllib.request
from urllib.parse import urljoin

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(BASE, "data", "sources.json")

SEEDS = [
    "https://www.ontario.ca/page/ontario-immigrant-nominee-program-oinp",
    "https://www.ontario.ca/page/2026-ontario-immigrant-nominee-program-updates",
    "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry.html",
    "https://investsudbury.ca/why-sudbury/newcomers/rcipfcip/",
]
ALLOWED = [
    r"^https://www\.ontario\.ca/page/.*(immigra|oinp|workforce|nominee)",
    r"^https://www\.ontario\.ca/laws/regulation/.*",
    r"^https://www\.canada\.ca/en/immigration-refugees-citizenship/.*",
    r"^https://investsudbury\.ca/why-sudbury/newcomers/.*",
]
MAX_PER_SEED = 15  # 防爆量限速

def load():
    if os.path.exists(SOURCES):
        with open(SOURCES, encoding="utf-8") as f:
            return json.load(f)
    return {"version": "1.0", "sources": []}

def save(d):
    with open(SOURCES, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[-] fetch fail {url}: {e}", file=sys.stderr)
        return ""

def ok(url):
    return any(re.match(p, url, re.I) for p in ALLOWED)

def main():
    data = load()
    existing = {s["url"] for s in data.get("sources", [])}
    new = []
    for seed in SEEDS:
        html = fetch(seed)
        if not html:
            continue
        links = re.findall(r'href=["\'](.*?)["\']', html)
        count = 0
        for ln in links:
            full = urljoin(seed, ln).split("#")[0].rstrip("/")
            if full in existing or not ok(full):
                continue
            if count >= MAX_PER_SEED:
                break
            existing.add(full)
            cat = "OINP" if "ontario.ca" in full else ("IRCC" if "canada.ca" in full else "RCIP")
            slug = full.rstrip("/").split("/")[-1].replace("-", " ").title()
            key = re.sub(r"[^a-z0-9]", "-", slug.lower())[:40] or f"src{len(existing)}"
            data["sources"].append({"key": key, "name": slug, "url": full, "category": cat, "watch": True, "auto_discovered": True})
            new.append(full)
            count += 1
        time.sleep(1)  # 节流
    if new:
        save(data)
        print(f"[+] 新增 {len(new)} 个官方源:")
        for u in new:
            print("   -", u)
    else:
        print("[=] 无新增 (已达最新/被拦截)")

if __name__ == "__main__":
    main()
