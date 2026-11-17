#!/usr/bin/env python3
"""semantic-patrol.py v3 — Ollama 語義採集器（心跳驅動）：採集層。

v3 改動（2026-08-18 設計）：唔再定時爬！由心跳隨機喚醒：
- 無參數：蠕蟲模式（核心源 + 隨機探索源，全球覆蓋）
- --topic "XXX"：按 topic 爬 Google News search（中英雙源），用 Ollama 分析該 topic 新進展

topic 模式輸出 RESULT 行俾 agent 讀（心跳/對話時 agent 決定 ping 唔 ping 用戶）。

零雲端：Google News RSS + 本地 Ollama qwen3。
"""
import json
import os
import re
import random
import hashlib
import subprocess
import sys
import urllib.request
import urllib.parse
import argparse
import datetime
from concurrent.futures import ThreadPoolExecutor

BASE = os.environ.get("IDLE_PING_WS") or os.path.expanduser("~/.openclaw/workspace")
STATE = os.path.join(BASE, "curiosity", "state.json")
DIGEST = os.path.join(BASE, "curiosity", "news-digest.md")
MAX_NEWS_PER_RUN = 30  # 每次最多餵 30 條（2026-08-21 由 60 減半——Ollama 處理快啲）
FETCH_TIMEOUT = 8      # 每個源 timeout 8s（2026-08-21 由 15s 縮短——慢源 fail-fast，唔好拖死成個流程）

# 結構化輸出 schema（Ollama format 參數）——簡化版：qwen3 細模型對複雜 schema 唔穩定，
# 只要求 categories（name + points），links 由爬蟲 news-links.json 對應返（更準確）
SUMMARY_SCHEMA = {
    "type": "object",
    "properties": {
        "categories": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "points": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["name", "points"]
            }
        },
        "overall": {"type": "string"}
    },
    "required": ["categories", "overall"]
}

# 全球新聞源：覆蓋各大洲 + 唔出名嘅國家都有份
NEWS_SOURCES = [
    ("https://news.google.com/rss?hl=zh-HK&gl=HK&ceid=HK:zh-Hant", "香港"),
    ("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", "美國"),
    ("https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en", "英國"),
    ("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en", "印度"),
    ("https://news.google.com/rss?hl=id&gl=ID&ceid=ID:id", "印尼"),
    ("https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja", "日本"),
    ("https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko", "韓國"),
    ("https://news.google.com/rss?hl=th&gl=TH&ceid=TH:th", "泰國"),
    ("https://news.google.com/rss?hl=en-PH&gl=PH&ceid=PH:en", "菲律賓"),
    ("https://news.google.com/rss?hl=en-NG&gl=NG&ceid=NG:en", "尼日利亞"),
    ("https://news.google.com/rss?hl=en-ZA&gl=ZA&ceid=ZA:en", "南非"),
    ("https://news.google.com/rss?hl=en-KE&gl=KE&ceid=KE:en", "肯尼亞"),
    ("https://news.google.com/rss?hl=en-GH&gl=GH&ceid=GH:en", "加納"),
    ("https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-BR", "巴西"),
    ("https://news.google.com/rss?hl=es-MX&gl=MX&ceid=MX:es-419", "墨西哥"),
    ("https://news.google.com/rss?hl=es-AR&gl=AR&ceid=AR:es-419", "阿根廷"),
    ("https://news.google.com/rss?hl=es-CO&gl=CO&ceid=CO:es-419", "哥倫比亞"),
    ("https://news.google.com/rss?hl=es-PE&gl=PE&ceid=PE:es-419", "秘魯"),
    ("https://news.google.com/rss?hl=en-IL&gl=IL&ceid=IL:en", "以色列"),
    ("https://news.google.com/rss?hl=ar-EG&gl=EG&ceid=EG:ar", "埃及"),
    ("https://news.google.com/rss?hl=uk&gl=UA&ceid=UA:uk", "烏克蘭"),
    ("https://news.google.com/rss?hl=pl&gl=PL&ceid=PL:pl", "波蘭"),
    ("https://news.google.com/rss?hl=ro&gl=RO&ceid=RO:ro", "羅馬尼亞"),
    ("https://news.google.com/rss?hl=en-NZ&gl=NZ&ceid=NZ:en", "新西蘭"),
    ("https://news.google.com/rss?hl=en-PK&gl=PK&ceid=PK:en", "巴基斯坦"),
    ("https://hnrss.org/frontpage", "Hacker News"),
    ("https://feeds.bbci.co.uk/news/world/rss.xml", "BBC世界新聞"),
]

# 蠕蟲模式：核心源（每次必爬，保證覆蓋）+ 隨機探索源（四處鑽）
CORE_SOURCES = [
    ("https://news.google.com/rss?hl=zh-HK&gl=HK&ceid=HK:zh-Hant", "香港"),
    ("https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", "美國"),
    ("https://news.google.com/rss?hl=en-GB&gl=GB&ceid=GB:en", "英國"),
    ("https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja", "日本"),
    ("https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en", "印度"),
    ("https://news.google.com/rss?hl=en-NG&gl=NG&ceid=NG:en", "尼日利亞"),
    ("https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-BR", "巴西"),
    ("https://hnrss.org/frontpage", "Hacker News"),
]
WORM_SOURCES_PER_RUN = 4  # 每次再隨機抽幾多個探索源


# ============ 混合管道（2026-08-21 設計）============
CHANNELS_FILE = os.path.join(BASE, "curiosity", "channels.json")

DEFAULT_CHANNELS = {
    "channels": {
        "news": 25,
        "onthisday": 20,
        "randomwiki": 15,
        "misconceptions": 20,
        "arxiv": 10,
        "reddit": 10
    },
    "mix_probability": 0.2,
    "lastChannels": []
}

# ============ 全渠道自動化排程（2026-08-22 設計）============
# --mode auto：每個渠道按自己嘅 interval 到期先爬（唔會每小時爬晒全部），
# 爬完 Ollama 歸納 → 直接入倉（share-queue add，帶 channel 標籤）。
# 業界做法（news aggregator adaptive polling）：發布愈密 poll 愈密，發布愈疏 poll 愈疏。
AUTO_SCHEDULE = {
    "news":           {"interval_hours": 1,  "limit": 12, "max_store": 3},  # 時效性高，每小時
    "onthisday":      {"interval_hours": 24, "limit": 4,  "max_store": 4},  # 今日歷史一日不變，每日（指定 4 篇）
    "randomwiki":     {"interval_hours": 12, "limit": 4,  "max_store": 4},  # 冷知識唔急，每日兩次
    "misconceptions": {"interval_hours": 24, "limit": 8,  "max_store": 4},  # 迷思清單慢變，每日
    "arxiv":          {"interval_hours": 24, "limit": 8,  "max_store": 4},  # 論文每日更新，每日
    "reddit":         {"interval_hours": 12, "limit": 6,  "max_store": 3},  # TIL 每日兩次
}

# ============ Rotation mode（2026-08-22 設計：兩舊嘢合併）============
# 主題驅動全渠道：每晚心跳（主題工廠）諗 30 個主題入 topic-rotation.json；
# 每小時 crawler 讀 rotation[index]，用全部主題可搜渠道（news 中英 + arxiv + reddit）
# 搜呢個主題 → Ollama 歸納 → share-queue 入倉（channel=topic）→ index+1。
# 非主題渠道（onthisday/randomwiki/misconceptions）天生冇主題可言，保留做每日補底。
TOPIC_ROTATION_FILE = os.path.join(BASE, "curiosity", "topic-rotation.json")
BONUS_CHANNELS = {k: AUTO_SCHEDULE[k] for k in ("onthisday", "randomwiki", "misconceptions")}

# Cold-start fallback（2026-08-28 加）：用戶第一日夜晚主題工廠未行過 → topic-rotation.json 可能係空。
# 呢 30 條係通用主題，crawler 讀唔到 json 主題時用呢啲照爬，同時自動寫入 json（self-healing）。
DEFAULT_TOPICS = [
    "人工智能與未來科技", "太空探索與天文發現", "海洋生物與深海奧秘",
    "氣候變化與環境保護", "腦科學與記憶研究", "語言演化與文化",
    "恐龍與古生物學", "心理學與行為經濟學", "機器人與自動化",
    "新能源與電池技術", "虛擬實境與元宇宙", "音樂與大腦健康",
    "動物行為與智慧", "古代文明與考古發現", "食品安全與營養科學",
    "遊戲設計與玩家心理", "天文物理與黑洞", "生物演化冷知識",
    "醫學突破與新藥研發", "城市規劃與智慧交通", "機器學習與數據科學",
    "歷史冷知識與趣聞", "生態系統與生物多樣性", "航天工程與火箭技術",
    "基因編輯與生物科技", "迷因文化與網絡現象", "極地探索與冰川研究",
    "未來交通與超迴路", "人工智慧倫理與社會影響", "量子科技與密碼學",
]


def fetch_onthisday(month, day):
    """維基 On This Day：今日歷史事件（中英雙源，並行）→ [(title, link)]"""
    def grab(lang):
        out = []
        url = f"https://{lang}.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Patrol/1.0 (curiosity)"})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as r:
                data = json.load(r)
            for ev in data.get("events", [])[:7]:
                year = ev.get("year", "?")
                text = ev.get("text", "").strip()
                pages = ev.get("pages", []) or []
                pt = ""
                if pages:
                    pt = (pages[0].get("titles", {}).get("normalized", "")
                          or pages[0].get("title", ""))
                title = f"[{year}] {text}"
                if pt and pt not in text:
                    title += f"（{pt}）"
                link = f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(pt.replace(' ', '_'))}" if pt else ""
                out.append((title, link))
        except Exception as e:
            print(f"[semantic] onthisday 失敗({lang}): {e}")
        return out
    with ThreadPoolExecutor(max_workers=2) as ex:
        results = list(ex.map(grab, ("en", "zh")))
    items, seen = [], set()
    for batch in results:
        for t, l in batch:
            if t and t not in seen:
                seen.add(t)
                items.append((t, l))
    return items[:20]


def fetch_randomwiki(n=4):
    """維基隨機文章（中英交替，並行）→ [(title + extract, link)]"""
    def grab(i):
        lang = "zh" if i % 2 else "en"
        url = f"https://{lang}.wikipedia.org/api/rest_v1/page/random/summary"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Patrol/1.0 (curiosity)"})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as r:
                d = json.load(r)
            title = d.get("title", "")
            desc = d.get("description", "") or ""
            extract = d.get("extract", "")[:130]
            link = d.get("content_urls", {}).get("desktop", {}).get("page", "")
            if title:
                label = f"{title}" + (f" — {desc}" if desc else "")
                return (f"{label}: {extract}", link)
        except Exception as e:
            print(f"[semantic] randomwiki 失敗: {e}")
        return None
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(grab, range(n)))
    return [r for r in results if r]


def fetch_misconceptions(n=8):
    """拆迷思管道：維基 List of common misconceptions（隨機抽）+ Snopes RSS（並行）"""
    def grab_wiki():
        out = []
        try:
            url = ("https://en.wikipedia.org/w/api.php?action=parse"
                   "&page=List_of_common_misconceptions&prop=wikitext"
                   "&format=json&formatversion=2")
            req = urllib.request.Request(url, headers={"User-Agent": "OpenClaw-Patrol/1.0 (curiosity)"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.load(r)
            text = data.get("parse", {}).get("wikitext", "") or ""
            bullets = []
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("*") and len(line) > 60:
                    clean = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", line)
                    clean = re.sub(r"\{\{.*?\}\}", "", clean)
                    clean = re.sub(r"<ref.*?</ref>", "", clean, flags=re.S)
                    clean = re.sub(r"<[^>]+>", "", clean)
                    clean = re.sub(r"''+", "", clean)
                    clean = clean.lstrip("* ").strip()
                    if len(clean) > 60:
                        bullets.append(clean)
            random.shuffle(bullets)
            for b in bullets[:n]:
                out.append(("迷思: " + b[:170],
                            "https://en.wikipedia.org/wiki/List_of_common_misconceptions"))
        except Exception as e:
            print(f"[semantic] misconceptions 維基失敗: {e}")
        return out

    def grab_snopes():
        out = []
        try:
            req = urllib.request.Request("https://www.snopes.com/feed/",
                                         headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as r:
                data = r.read().decode("utf-8", "ignore")
            for entry in re.findall(r"<item>(.*?)</item>", data, re.S)[:5]:
                t = re.search(r"<title>(.*?)</title>", entry, re.S)
                l = re.search(r"<link>(.*?)</link>", entry, re.S)
                if t:
                    out.append(("Snopes: " + t.group(1).strip(),
                                l.group(1).strip() if l else "https://snopes.com"))
        except Exception as e:
            print(f"[semantic] misconceptions Snopes 失敗: {e}")
        return out

    with ThreadPoolExecutor(max_workers=2) as ex:
        futs = [ex.submit(grab_wiki), ex.submit(grab_snopes)]
        return futs[0].result() + futs[1].result()


def fetch_arxiv(n=8):
    """arXiv 最新論文（科普物理 + AI + 神經科學，並行）→ [(title + abstract, link)]"""
    cats = ["physics.pop-ph", "cs.AI", "q-bio.NC", "astro-ph.HE"]
    def grab(cat):
        out = []
        url = ("https://export.arxiv.org/api/query?search_query=cat:" + cat +
               "&sortBy=submittedDate&sortOrder=descending&max_results=3")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=12) as r:
                data = r.read().decode("utf-8", "ignore")
            for entry in re.findall(r"<entry>(.*?)</entry>", data, re.S)[:3]:
                t = re.search(r"<title>(.*?)</title>", entry, re.S)
                l = re.search(r"<id>(.*?)</id>", entry, re.S)
                s = re.search(r"<summary>(.*?)</summary>", entry, re.S)
                if t:
                    title = re.sub(r"\s+", " ", t.group(1)).strip()
                    summ = re.sub(r"\s+", " ", s.group(1)).strip()[:130] if s else ""
                    link = l.group(1).strip() if l else ""
                    out.append((f"[arXiv {cat}] {title}: {summ}", link))
        except Exception as e:
            print(f"[semantic] arxiv 失敗({cat}): {e}")
        return out
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(grab, cats))
    items = []
    for batch in results:
        items.extend(batch)
    return items


def fetch_reddit_til(n=6):
    """Reddit r/todayilearned 本週 top（Atom RSS；urllib 被 TLS fingerprint block → curl fallback）"""
    url = "https://www.reddit.com/r/todayilearned/top/.rss?t=week"
    data = ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"[semantic] reddit urllib 失敗({e})，試 curl")
        try:
            out = subprocess.run(
                ["curl", "-s", "-A", "Mozilla/5.0 (X11; Linux x86_64)", "--max-time", "15", url],
                capture_output=True, text=True, timeout=20)
            data = out.stdout
        except Exception as e2:
            print(f"[semantic] reddit 失敗: {e2}")
            return []
    if not data:
        return []
    items = []
    for entry in re.findall(r"<entry>(.*?)</entry>", data, re.S)[:n]:
        t = re.search(r"<title>(.*?)</title>", entry, re.S)
        l = re.search(r"<link[^>]*href=\"(.*?)\"", entry, re.S)
        if t:
            title = re.sub(r"&amp;", "&", t.group(1).strip())
            items.append(("TIL: " + title,
                          l.group(1) if l else "https://reddit.com/r/todayilearned"))
    return items


def fetch_arxiv_topic(topic, n=5):
    """arXiv API 按主題搜尋（relevance sort）→ [(title + abstract, link)]"""
    out = []
    url = ("https://export.arxiv.org/api/query?search_query=" +
           urllib.parse.quote(f'all:"{topic}"') +
           "&sortBy=relevance&sortOrder=descending&max_results=" + str(n))
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            data = r.read().decode("utf-8", "ignore")
        for entry in re.findall(r"<entry>(.*?)</entry>", data, re.S)[:n]:
            t = re.search(r"<title>(.*?)</title>", entry, re.S)
            l = re.search(r"<id>(.*?)</id>", entry, re.S)
            s = re.search(r"<summary>(.*?)</summary>", entry, re.S)
            if t:
                title = re.sub(r"\s+", " ", t.group(1)).strip()
                summ = re.sub(r"\s+", " ", s.group(1)).strip()[:120] if s else ""
                link = l.group(1).strip() if l else ""
                if title:
                    out.append((f"[arXiv] {title}: {summ}", link))
    except Exception as e:
        print(f"[semantic] arxiv topic 搜尋失敗: {e}")
    return out


def fetch_reddit_search(topic, n=6):
    """Reddit search.rss 按主題搜尋（Atom RSS；search.json 被 403 block → 用 RSS 版，
    urllib 被 TLS fingerprint block → curl fallback）→ [(title, link)]"""
    url = ("https://www.reddit.com/search.rss?q=" + urllib.parse.quote(topic) +
           "&sort=relevance&t=week")
    data = ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"[semantic] reddit search urllib 失敗({e})，試 curl")
        try:
            out = subprocess.run(
                ["curl", "-s", "-A", "Mozilla/5.0 (X11; Linux x86_64)", "--max-time", "15", url],
                capture_output=True, text=True, timeout=20)
            data = out.stdout
        except Exception as e2:
            print(f"[semantic] reddit search 失敗: {e2}")
            return []
    if not data:
        return []
    items = []
    for entry in re.findall(r"<entry>(.*?)</entry>", data, re.S)[:n]:
        t = re.search(r"<title>(.*?)</title>", entry, re.S)
        l = re.search(r"<link[^>]*href=\"(.*?)\"", entry, re.S)
        if t:
            title = re.sub(r"&amp;", "&", t.group(1).strip())
            if title:
                items.append(("Reddit: " + title,
                              l.group(1) if l else "https://reddit.com"))
    return items


def roll_channel():
    """按 channels.json 權重擲骰揀管道；mix_probability 機會揀多一條 mix。
    上次用過嘅管道權重 ×0.3（避免連續重複）。返回 (main, mix)"""
    try:
        with open(CHANNELS_FILE) as f:
            cfg = json.load(f)
    except Exception:
        cfg = DEFAULT_CHANNELS
    chans = cfg.get("channels", {})
    last = cfg.get("lastChannels", [])
    names = [n for n, w in chans.items() if w and w > 0]
    if not names:
        names = list(DEFAULT_CHANNELS["channels"].keys())
    weights = []
    for n in names:
        w = float(chans.get(n, 10))
        if last and n == last[-1]:
            w *= 0.3
        weights.append(max(w, 0.01))
    main = random.choices(names, weights=weights, k=1)[0]
    mix = ""
    if random.random() < cfg.get("mix_probability", 0.2):
        rest = [n for n in names if n != main]
        if rest:
            mix = random.choice(rest)
    last.append(main)
    cfg["lastChannels"] = last[-6:]
    with open(CHANNELS_FILE, "w") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return main, mix


def run_channel_mode(channel, topic, now, now_iso, today, state):
    """混合管道模式：--channel roll 擲骰，或者指定管道直接行"""
    main_chan = channel
    mix_chan = ""
    if channel == "roll":
        main_chan, mix_chan = roll_channel()
        print(f"[semantic] 擲骰: {main_chan}" + (f" + {mix_chan}" if mix_chan else ""))

    # xsearch：script 層冇 X API —— 輸出 marker，agent 要用 x_search tool 親自搜
    if main_chan == "xsearch":
        print("RESULT channel=xsearch")
        print("X_SEARCH_REQUIRED=1")
        print(f"TOPIC={topic or '（冇 topic，自由發揮）'}")
        print("OVERALL=請用 x_search tool 搜 X（query 用 TOPIC），自己整理 3-5 條有趣 post")
        state["lastSemanticPatrol"] = now_iso
        state["lastChannel"] = "xsearch"
        with open(STATE, "w") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        return

    fetch_map = {
        "news": (lambda: fetch_topic_headlines(topic) if topic else fetch_headlines()),
        "onthisday": (lambda: fetch_onthisday(now.month, now.day)),
        "randomwiki": (lambda: fetch_randomwiki(4)),
        "misconceptions": (lambda: fetch_misconceptions(8)),
        "arxiv": (lambda: fetch_arxiv(8)),
        "reddit": (lambda: fetch_reddit_til(6)),
    }
    items = []
    if main_chan in fetch_map:
        items += fetch_map[main_chan]()
    if mix_chan and mix_chan in fetch_map:
        items += fetch_map[mix_chan]()
    if not items:
        print(f"[semantic] channel '{main_chan}' 攞唔到內容，skip")
        return

    save_links(items)
    headlines = [t for t, _ in items][:MAX_NEWS_PER_RUN]
    label = main_chan + (f"+{mix_chan}" if mix_chan else "")
    resp = ollama_topic_summarize(f"管道[{label}]", headlines)
    cats, overall = parse_summary(resp)
    summary_line = overall or (cats[0]["name"] if cats else "（冇內容）")

    os.makedirs(os.path.dirname(DIGEST), exist_ok=True)
    digest_header = f"## {today}\n"
    digest_body = ""
    if os.path.exists(DIGEST):
        with open(DIGEST) as f:
            digest_body = f.read()
    if digest_header not in digest_body:
        digest_body += f"\n{digest_header}"
    with open(DIGEST, "a") as f:
        f.write(f"- {now_iso} | [{label}] {summary_line}\n")

    state["lastSemanticPatrol"] = now_iso
    state["lastSemanticSummary"] = summary_line
    state["lastChannel"] = label
    with open(STATE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"RESULT channel={label}")
    print(f"OVERALL={summary_line}")
    if mix_chan == "xsearch":
        print("X_SEARCH_REQUIRED=1")
        print(f"TOPIC={topic or '（冇 topic，自由發揮）'}")
    for c in cats:
        name = c.get("name", "")
        points = c.get("points", [])
        print(f"CAT={name}")
        for p in points:
            print(f"  - {p}")


def fetch_topic_headlines(topic):
    """按 topic 爬 Google News search RSS（中英雙源，並行 fetch），返回 [(title, link)]"""
    queries = [
        f"https://news.google.com/rss/search?q={urllib.parse.quote(topic)}&hl=zh-HK&gl=HK&ceid=HK:zh-Hant",
        f"https://news.google.com/rss/search?q={urllib.parse.quote(topic)}&hl=en-US&gl=US&ceid=US:en",
    ]

    def one(url):
        items = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as r:
                data = r.read().decode("utf-8", "ignore")
            for entry in re.findall(r"<item>(.*?)</item>", data, re.S)[:12]:
                t = re.search(r"<title>(.*?)</title>", entry, re.S)
                l = re.search(r"<link>(.*?)</link>", entry, re.S)
                if t:
                    title = t.group(1).strip()
                    if title:
                        items.append((title, l.group(1).strip() if l else ""))
        except Exception as e:
            print(f"[semantic] topic RSS 失敗: {e}")
        return items

    with ThreadPoolExecutor(max_workers=2) as ex:
        results = list(ex.map(one, queries))
    items, seen = [], set()
    for batch in results:
        for t, l in batch:
            if t not in seen:
                seen.add(t)
                items.append((t, l))
    return items[:40]


def ollama_topic_summarize(topic, headlines, known_context=""):
    """Ollama 只負責整理資訊（唔判斷）：輸出結構化 JSON（分類 + 要點 + 整體總結）。"""
    prompt = (
        f"你是資訊整理員。以下係關於「{topic}」嘅內容標題：\n"
        + "\n".join(f"{i+1}. {h}" for i, h in enumerate(headlines))
        + "\n\n請將以上標題整理成結構化摘要：\n"
          "1. 去重（相同事件合併）\n"
          "2. 按主題歸納成幾個類別（categories），每類 1-3 個要點（points）\n"
          "3. overall 用一句講「呢批內容涵蓋咩嘢」\n"
          "唔好判斷有冇趣、唔好評分、唔好篩選——純粹整理資訊，必須提及具體事件/人物/地點/國家名。"
    )
    payload = json.dumps({
        "model": "qwen3:1.7b", "prompt": prompt, "stream": False,
        "think": False, "format": SUMMARY_SCHEMA,
        "options": {"temperature": 0.3, "num_predict": 600},
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate", data=payload,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    return d.get("response", "")


def fetch_headlines():
    """返回 [(title, link)]——蠕蟲式：核心 8 源 + 隨機 4 源，全部並行 fetch（快好多）"""
    worm_pool = [s for s in NEWS_SOURCES if s not in CORE_SOURCES]
    sources = CORE_SOURCES + random.sample(worm_pool, min(WORM_SOURCES_PER_RUN, len(worm_pool)))

    def one(src):
        url, label = src
        items = []
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as r:
                data = r.read().decode("utf-8", "ignore")
            for entry in re.findall(r"<item>(.*?)</item>", data, re.S)[:3]:
                t = re.search(r"<title>(.*?)</title>", entry, re.S)
                l = re.search(r"<link>(.*?)</link>", entry, re.S)
                if t:
                    title = t.group(1).strip()
                    if title:
                        items.append((title, l.group(1).strip() if l else ""))
        except Exception as e:
            print(f"[semantic] RSS 失敗 {label} ({url}): {e}")
        return items

    with ThreadPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(one, sources))
    items, seen = [], set()
    for batch in results:
        for t, l in batch:
            if t not in seen:
                seen.add(t)
                items.append((t, l))
    return items[:80]


def save_links(items):
    """保存 title → link 對應（rolling 最近 500 條），俾 agent 篩選時攞 source。"""
    LINKS_FILE = os.path.join(BASE, "curiosity", "news-links.json")
    try:
        with open(LINKS_FILE) as f:
            links = json.load(f)
    except Exception:
        links = {}
    for t, l in items:
        if l:
            links[t] = l
    if len(links) > 500:
        links = dict(list(links.items())[-500:])
    with open(LINKS_FILE, "w") as f:
        json.dump(links, f, ensure_ascii=False, indent=1)


def news_hash(headlines):
    h = hashlib.md5()
    for t in headlines:
        h.update(t.encode("utf-8", "ignore"))
    return h.hexdigest()


def ollama_summarize(new_headlines, known_context=""):
    """Ollama 只負責整理資訊（唔判斷）：輸出結構化 JSON（分類 + 要點 + 整體總結）。"""
    prompt = (
        "你是資訊整理員。以下是來自全球各地（包括非洲、拉丁美洲、中東、東歐、"
        "南亞等平時少見嘅國家）嘅內容標題：\n"
        + "\n".join(f"{i+1}. {h}" for i, h in enumerate(new_headlines))
        + "\n\n請將以上標題整理成結構化摘要：\n"
          "1. 去重（相同事件合併）\n"
          "2. 按主題歸納成幾個類別（categories），每類 1-3 個要點（points）\n"
          "3. overall 用一句講「呢批內容涵蓋咩嘢」\n"
          "唔好判斷有冇趣、唔好評分、唔好篩選——純粹整理資訊，必須提及具體事件/人物/地點/國家名。"
    )
    payload = json.dumps({
        "model": "qwen3:1.7b", "prompt": prompt, "stream": False,
        "think": False, "format": SUMMARY_SCHEMA,
        "options": {"temperature": 0.3, "num_predict": 600},
    }).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate", data=payload,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.load(r)
    return d.get("response", "")


def recent_digest_context():
    """讀返最近 digest entries 做「已知世界」背景（learning progress 對照）。"""
    try:
        with open(DIGEST) as f:
            lines = [l.strip() for l in f.readlines() if l.strip().startswith("- ")]
        return "\n".join(lines[-12:])
    except Exception:
        return ""


def parse_summary(resp):
    """解析 Ollama 結構化 JSON 輸出 → (categories, overall)；失敗就 fallback 做單行文字。"""
    try:
        data = json.loads(resp)
        cats = data.get("categories", [])
        overall = data.get("overall", "")
        if cats or overall:
            return cats, overall
    except Exception:
        pass
    # JSON 被截斷（細模型 token 限制）時，嘗試救返完整 categories 部分
    try:
        cut = resp.rfind('"overall"')
        if cut > 0:
            partial = resp[:cut].rstrip()
            if partial.endswith(","):
                partial = partial[:-1]
            if partial.endswith("}"):
                partial = partial[:-1]
            partial += "}"
            data = json.loads(partial)
            cats = data.get("categories", [])
            if cats:
                return cats, ""
    except Exception:
        pass
    # fallback：舊格式（純文字）
    line = resp.strip().splitlines()[0] if resp.strip() else ""
    if line.startswith("{"):
        return [], "（Ollama 輸出未完成，摘要記錄不完整）"
    return [], re.sub(r"^整理[：:\s]*", "", line).strip()


def run_auto_mode(now, now_iso, today, state):
    """全渠道自動化入倉（cron 每小時觸發）：每渠道按 AUTO_SCHEDULE 到期先爬，
    爬完 Ollama 歸納 → 直接 share-queue add 入倉（帶 channel 標籤）。
    純機械，零 agent 判斷——出貨判斷仍由 idle-ping/curiosity-explore skill 負責。"""
    last_fetch = state.get("lastAutoFetch", {})
    fetch_map = {
        "news":           (lambda: fetch_headlines()),
        "onthisday":      (lambda: fetch_onthisday(now.month, now.day)),
        "randomwiki":     (lambda: fetch_randomwiki(4)),
        "misconceptions": (lambda: fetch_misconceptions(8)),
        "arxiv":          (lambda: fetch_arxiv(8)),
        "reddit":         (lambda: fetch_reddit_til(6)),
    }
    summary_lines = []
    for chan, cfg in AUTO_SCHEDULE.items():
        # 到期 check：冇記錄 → 即爬；有記錄 → 夠 interval 先爬
        last = last_fetch.get(chan, "")
        due = False
        if not last:
            due = True
        else:
            try:
                last_dt = datetime.datetime.strptime(last, "%Y-%m-%d %H:%M")
                if (now - last_dt).total_seconds() >= cfg["interval_hours"] * 3600:
                    due = True
            except Exception:
                due = True
        if not due:
            continue

        items = fetch_map[chan]()
        if not items:
            print(f"[auto] {chan} 攞唔到內容，skip")
            last_fetch[chan] = now_iso  # 記低，避免每小時都試一次（例如 source 死咗）
            continue

        items = items[:cfg["limit"]]
        save_links(items)
        headlines = [t for t, _ in items]
        resp = ollama_topic_summarize(f"管道[{chan}]", headlines)
        cats, overall = parse_summary(resp)

        # 入倉：每個 category 一條（topic 帶渠道前綴，summary 用第一點，link 嘗試 match）
        stored = 0
        for c in cats[:cfg["max_store"]]:
            name = c.get("name", "")
            points = c.get("points", []) or []
            if not name or not points:
                continue
            summary_text = points[0]
            link = ""
            for t, l in items:
                if l and (name in t or summary_text[:20] in t):
                    link = l
                    break
            cmd = [sys.executable, os.path.join(BASE, "scripts", "share-queue.py"), "add",
                   "--topic", f"[{chan}] {name}", "--summary", summary_text,
                   "--cat", name, "--channel", chan]
            if link:
                cmd += ["--link", link]
            try:
                subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                stored += 1
            except Exception as e:
                print(f"[auto] {chan} 入倉失敗: {e}")

        last_fetch[chan] = now_iso
        summary_lines.append(f"{chan}: {stored} 條入倉（{len(items)} 條料）")

    if summary_lines:
        state["lastAutoFetch"] = last_fetch
        with open(STATE, "w") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    print("RESULT auto=" + ("; ".join(summary_lines) if summary_lines else "全部渠道未到期"))


def next_rotation_topic():
    """讀 topic-rotation.json → (topic, index)；index 超出長度重置 0。
    2026-08-28：json 空／讀唔到 → fallback 去 DEFAULT_TOPICS（cold-start），並順手寫入 json。"""
    try:
        with open(TOPIC_ROTATION_FILE) as f:
            cfg = json.load(f)
    except Exception as e:
        print(f"[semantic] topic-rotation.json 讀取失敗: {e}（用內置主題）")
        cfg = None
    rotation = (cfg or {}).get("rotation", [])
    index = (cfg or {}).get("index", 0)
    if not rotation:
        # Cold-start：內置主題入 json（self-healing），聽日主題工廠會接管補充
        print("[semantic] topic-rotation.json 空——用內置 30 條通用主題並寫入 json（cold-start 修復）")
        _write_rotation(DEFAULT_TOPICS, 0)
        return DEFAULT_TOPICS[0], 0
    if index >= len(rotation):
        index = 0
    return rotation[index], index


def _write_rotation(rotation, index):
    """atomic write topic-rotation.json（fallback 用）。"""
    cfg = {
        "version": 2,
        "description": "主題輪換清單：夜晚主題工廠補充新主題，crawler 順住 rotation[index] 探索。",
        "rotation": rotation,
        "index": index,
        "updatedAt": datetime.date.today().isoformat(),
        "lastUsed": "",
    }
    tmp = TOPIC_ROTATION_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    os.replace(tmp, TOPIC_ROTATION_FILE)


def advance_rotation_index():
    """用後 index+1（到尾重置 0）+ lastUsed 更新，atomic write。"""
    try:
        with open(TOPIC_ROTATION_FILE) as f:
            cfg = json.load(f)
    except Exception:
        return
    rotation = cfg.get("rotation", [])
    index = cfg.get("index", 0)
    if rotation:
        if 0 <= index < len(rotation):
            cfg["lastUsed"] = rotation[index]
        index = (index + 1) % len(rotation)
        cfg["index"] = index
    cfg["updatedAt"] = datetime.date.today().isoformat()
    tmp = TOPIC_ROTATION_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    os.replace(tmp, TOPIC_ROTATION_FILE)


def crawl_bonus_channels(now, now_iso, state):
    """非主題渠道補底：onthisday/randomwiki/misconceptions 照 interval 到期先爬入倉。
    返回 summary lines list。"""
    last_fetch = state.get("lastAutoFetch", {})
    fetch_map = {
        "onthisday":      (lambda: fetch_onthisday(now.month, now.day)),
        "randomwiki":     (lambda: fetch_randomwiki(4)),
        "misconceptions": (lambda: fetch_misconceptions(8)),
    }
    lines = []
    for chan, cfg in BONUS_CHANNELS.items():
        last = last_fetch.get(chan, "")
        due = False
        if not last:
            due = True
        else:
            try:
                last_dt = datetime.datetime.strptime(last, "%Y-%m-%d %H:%M")
                if (now - last_dt).total_seconds() >= cfg["interval_hours"] * 3600:
                    due = True
            except Exception:
                due = True
        if not due:
            continue
        items = fetch_map[chan]()
        if not items:
            last_fetch[chan] = now_iso
            lines.append(f"{chan}: 攞唔到內容")
            continue
        items = items[:cfg["limit"]]
        save_links(items)
        headlines = [t for t, _ in items]
        resp = ollama_topic_summarize(f"管道[{chan}]", headlines)
        cats, overall = parse_summary(resp)
        stored = 0
        for c in cats[:cfg["max_store"]]:
            name = c.get("name", "")
            points = c.get("points", []) or []
            if not name or not points:
                continue
            summary_text = points[0]
            link = ""
            for t, l in items:
                if l and (name in t or summary_text[:20] in t):
                    link = l
                    break
            cmd = [sys.executable, os.path.join(BASE, "scripts", "share-queue.py"), "add",
                   "--topic", f"[{chan}] {name}", "--summary", summary_text,
                   "--cat", name, "--channel", chan]
            if link:
                cmd += ["--link", link]
            try:
                subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                stored += 1
            except Exception as e:
                print(f"[rotation] {chan} 入倉失敗: {e}")
        last_fetch[chan] = now_iso
        lines.append(f"{chan}: {stored} 條入倉（{len(items)} 條料）")
    if lines:
        state["lastAutoFetch"] = last_fetch
    return lines


def run_rotation_mode(now, now_iso, today, state):
    """主題驅動全渠道（cron 每小時）：讀 topic-rotation.json 攞當前主題，
    用全部主題可搜渠道（news 中英 + arxiv + reddit）搜呢個主題 → Ollama 歸納
    → share-queue 入倉（channel=topic）→ index+1。
    非主題渠道（onthisday/randomwiki/misconceptions）照 interval 到期補底。"""
    topic, idx = next_rotation_topic()
    if not topic:
        print("RESULT rotation=冇主題（topic-rotation.json 空？）")
        return

    print(f"[semantic] rotation 主題: {topic}")
    items = []
    items += fetch_topic_headlines(topic)   # news：Google News search 中英雙源
    items += fetch_arxiv_topic(topic)       # arxiv：論文搜尋
    items += fetch_reddit_search(topic)     # reddit：討論搜尋
    seen, deduped = set(), []
    for t, l in items:
        if t and t not in seen:
            seen.add(t)
            deduped.append((t, l))
    items = deduped

    stored = 0
    if items:
        save_links(items)
        headlines = [t for t, _ in items][:MAX_NEWS_PER_RUN]
        resp = ollama_topic_summarize(f"主題[{topic}]", headlines)
        cats, overall = parse_summary(resp)
        for c in cats[:4]:
            name = c.get("name", "")
            points = c.get("points", []) or []
            if not name or not points:
                continue
            summary_text = points[0]
            link = ""
            for t, l in items:
                if l and (name in t or summary_text[:20] in t):
                    link = l
                    break
            cmd = [sys.executable, os.path.join(BASE, "scripts", "share-queue.py"), "add",
                   "--topic", f"[主題] {name}", "--summary", summary_text,
                   "--cat", name, "--channel", "topic"]
            if link:
                cmd += ["--link", link]
            try:
                subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                stored += 1
            except Exception as e:
                print(f"[rotation] 入倉失敗: {e}")
    else:
        print(f"[semantic] rotation 主題 '{topic}' 全部渠道攞唔到內容")

    # 寫入 rolling digest（deep-explore/morning-report 有料跟）
    if items:
        summary_line = overall or (cats[0]["name"] if cats else "（冇內容）")
    else:
        summary_line = "（全部渠道攞唔到內容）"
    os.makedirs(os.path.dirname(DIGEST), exist_ok=True)
    digest_header = f"## {today}\n"
    digest_body = ""
    if os.path.exists(DIGEST):
        with open(DIGEST) as f:
            digest_body = f.read()
    if digest_header not in digest_body:
        digest_body += f"\n{digest_header}"
    with open(DIGEST, "a") as f:
        f.write(f"- {now_iso} | [主題:{topic}] {summary_line}\n")

    advance_rotation_index()
    bonus_lines = crawl_bonus_channels(now, now_iso, state)

    state["lastSemanticPatrol"] = now_iso
    state["lastSemanticSummary"] = f"[{topic}] {stored} 條入倉（{len(items)} 條料）"
    state["lastChannel"] = "topic"
    with open(STATE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

    msg = f"RESULT rotation={topic}: {stored} 條入倉（{len(items)} 條料）"
    if bonus_lines:
        msg += " | 補底: " + "; ".join(bonus_lines)
    print(msg)


def run_topic_mode(topic, now, now_iso, today, state):
    """按 topic 探索（心跳驅動）：爬 Google News search → Ollama 整理 → digest + stdout"""
    print(f"[semantic] topic 探索: {topic}")
    items = fetch_topic_headlines(topic)
    if not items:
        print(f"[semantic] topic '{topic}' 攞唔到內容，skip")
        return
    save_links(items)
    headlines = [t for t, _ in items]
    resp = ollama_topic_summarize(topic, headlines[:MAX_NEWS_PER_RUN])

    cats, overall = parse_summary(resp)
    summary_line = overall or (cats[0]["name"] if cats else "（冇內容）")

    os.makedirs(os.path.dirname(DIGEST), exist_ok=True)
    digest_header = f"## {today}\n"
    digest_body = ""
    if os.path.exists(DIGEST):
        with open(DIGEST) as f:
            digest_body = f.read()
    if digest_header not in digest_body:
        digest_body += f"\n{digest_header}"
    with open(DIGEST, "a") as f:
        f.write(f"- {now_iso} | [探索:{topic}] {summary_line}\n")

    state["lastSemanticPatrol"] = now_iso
    state["lastSemanticSummary"] = summary_line
    with open(STATE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    # stdout 俾 agent 讀——結構化輸出，agent 自己判斷有冇趣、值唔值得 ping 用戶
    print(f"RESULT topic={topic}")
    print(f"OVERALL={summary_line}")
    for c in cats:
        name = c.get("name", "")
        points = c.get("points", [])
        links = c.get("links", [])
        print(f"CAT={name}")
        for p, l in zip(points, links or [""] * len(points)):
            print(f"  - {p} ({l})" if l else f"  - {p}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default=None, help="news 管道用：按 topic 探索（Google News search）")
    parser.add_argument("--channel", default=None,
                        help="news|onthisday|randomwiki|misconceptions|arxiv|reddit|roll（roll=按權重隨機揀，20%% mix 兩管道）")
    parser.add_argument("--mode", default=None, help="auto=全渠道自動化入倉（每渠道按自己 interval）；rotation=主題驅動全渠道（cron 每小時）")
    args = parser.parse_args()

    now = datetime.datetime.now()
    now_iso = now.strftime("%Y-%m-%d %H:%M")
    today = now.strftime("%Y-%m-%d")

    try:
        with open(STATE) as f:
            state = json.load(f)
    except Exception:
        state = {}

    if args.mode == "rotation":
        run_rotation_mode(now, now_iso, today, state)
        return

    if args.mode == "auto":
        run_auto_mode(now, now_iso, today, state)
        return

    if args.channel:
        run_channel_mode(args.channel, args.topic, now, now_iso, today, state)
        return

    if args.topic:
        run_topic_mode(args.topic, now, now_iso, today, state)
        return

    headlines = fetch_headlines()
    if not headlines:
        print(f"[semantic] {now_iso} 攞唔到新聞，skip")
        return

    # 保留 title → link（驗證層：source 落地）
    items = headlines
    headlines = [t for t, _ in items]
    save_links(items)

    # dedup：只餵新新聞
    last_hash = state.get("lastNewsHash", "")
    cur_hash = news_hash(headlines)
    new_headlines = headlines
    if last_hash and cur_hash == last_hash:
        print(f"[semantic] {now_iso} 冇新新聞（同上次一樣），skip")
        state["lastSemanticPatrol"] = now_iso
        with open(STATE, "w") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        return

    known = recent_digest_context()
    resp = ollama_summarize(new_headlines[:MAX_NEWS_PER_RUN], known)

    cats, overall = parse_summary(resp)
    summary_line = overall or (cats[0]["name"] if cats else "（冇內容）")

    # 寫入 rolling digest（Ollama 整理 → 俾 agent 篩選）
    os.makedirs(os.path.dirname(DIGEST), exist_ok=True)
    digest_header = f"## {today}\n"
    digest_body = ""
    if os.path.exists(DIGEST):
        with open(DIGEST) as f:
            digest_body = f.read()
    if digest_header not in digest_body:
        digest_body += f"\n{digest_header}"
    with open(DIGEST, "a") as f:
        f.write(f"- {now_iso} | {summary_line}\n")

    # update state
    state["lastSemanticPatrol"] = now_iso
    state["lastNewsHash"] = cur_hash
    state["lastSemanticSummary"] = summary_line
    with open(STATE, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print(f"RESULT topic=蠕蟲")
    print(f"OVERALL={summary_line}")
    for c in cats:
        name = c.get("name", "")
        points = c.get("points", [])
        links = c.get("links", [])
        print(f"CAT={name}")
        for p, l in zip(points, links or [""] * len(points)):
            print(f"  - {p} ({l})" if l else f"  - {p}")


if __name__ == "__main__":
    main()
