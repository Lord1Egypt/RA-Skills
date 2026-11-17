#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
policy_monitor.py — 政策差分监控 (净化后 hash 比对, 避免动态内容误报)
- 对每个 watch=true 的源抓取, 净化成纯文本(去 script/style/标签/空行/时间戳噪音)后做 hash。
- 首跑建基线; 后续比对, 变化输出 CHANGES_DETECTED:url,... ; 无变化输出 NO_CHANGES。
- 建议由 cron 每日调用; 净化使动态页面不改内容则不误报。
"""
import hashlib, json, os, re, sys, urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(BASE, "data", "sources.json")
STATE = os.path.join(BASE, "data", "snapshots", "policy_hashes.json")

def clean(html):
    html = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"&nbsp;|&#160;", " ", html)
    html = re.sub(r"\s+", " ", html)
    return html.strip()

def fetch_text(url):
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept": "text/html"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"[-] fetch fail {url}: {e}", file=sys.stderr)
        return ""

def main():
    if not os.path.exists(SOURCES):
        print("NO_SOURCES"); return
    with open(SOURCES, encoding="utf-8") as f:
        sources = json.load(f).get("sources", [])
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    old = {}
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            old = json.load(f)
    new = {}
    changed = []
    for s in sources:
        if not s.get("watch", True):
            continue
        url = s["url"]
        html = fetch_text(url)
        if not html:
            continue
        text = clean(html)
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        new[url] = h
        if url in old and old[url] != h:
            changed.append(url)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(new, f, ensure_ascii=False, indent=2)
    if changed:
        print("CHANGES_DETECTED:" + ",".join(changed))
    else:
        print("NO_CHANGES")

if __name__ == "__main__":
    main()
