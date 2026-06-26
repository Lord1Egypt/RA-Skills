#!/usr/bin/env python3
"""
fetch_news.py — 多引擎并发采集资讯
用法：python3 fetch_news.py --keyword "OpenClaw AI" --count 15 --output /tmp/news.json
"""
import argparse, json, os, re, ssl, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

ENGINES = {
    "bing":       "https://cn.bing.com/search?q={kw}&ensearch=1",
    "bing_cn":    "https://cn.bing.com/search?q={kw}&ensearch=0",
    "ddg":        "https://duckduckgo.com/html/?q={kw}",
    "brave":      "https://search.brave.com/search?q={kw}",
    "sogou":      "https://sogou.com/web?query={kw}",
    "baidu":      "https://www.baidu.com/s?wd={kw}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

def fetch_one(engine, url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req, context=ctx, timeout=12)
        html = resp.read().decode("utf-8", "ignore")
        return engine, html
    except Exception as e:
        return engine, ""

def extract_snippets(html, keyword):
    """从 HTML 中提取标题+摘要片段"""
    snippets = []

    # 通用链接+标题提取
    titles = re.findall(
        r'<(?:h[23]|a)[^>]*>([^<]{10,120})</(?:h[23]|a)>', html, re.DOTALL)
    descs = re.findall(
        r'<(?:p|div|span)[^>]*class="[^"]*(?:snippet|desc|abstract|body|result)[^"]*"[^>]*>'
        r'(.*?)</(?:p|div|span)>', html, re.DOTALL | re.IGNORECASE)

    clean = lambda s: re.sub(r'<[^>]+>', '', s).strip()
    kw_lower = keyword.lower()

    seen = set()
    for t in titles:
        t = clean(t)
        if len(t) < 8 or t in seen:
            continue
        seen.add(t)
        snippets.append({"title": t, "desc": "", "source": ""})

    for i, d in enumerate(descs[:20]):
        d = clean(d)
        if len(d) > 20 and d not in seen:
            seen.add(d)
            if i < len(snippets):
                snippets[i]["desc"] = d[:300]
            else:
                snippets.append({"title": "", "desc": d[:300], "source": ""})

    # 过滤与关键词相关的
    kw_words = [w.lower() for w in keyword.split()]
    filtered = [s for s in snippets if
                any(w in (s["title"]+s["desc"]).lower() for w in kw_words)]
    return filtered[:5]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", required=True, help="搜索关键词")
    parser.add_argument("--engines", default="bing,bing_cn,ddg,brave",
                        help="使用的引擎（逗号分隔）")
    parser.add_argument("--count",   type=int, default=15, help="目标采集条数")
    parser.add_argument("--output",  required=True, help="输出 JSON 路径")
    args = parser.parse_args()

    engine_list = [e.strip() for e in args.engines.split(",") if e.strip() in ENGINES]
    kw_encoded = urllib.parse.quote(args.keyword)

    urls = {e: ENGINES[e].format(kw=kw_encoded) for e in engine_list}

    print(f"🔍 搜索关键词: {args.keyword}")
    print(f"   引擎: {engine_list}\n")

    all_snippets = []
    with ThreadPoolExecutor(max_workers=len(urls)) as ex:
        futs = {ex.submit(fetch_one, e, u): e for e, u in urls.items()}
        for f in as_completed(futs):
            engine, html = f.result()
            if html:
                snips = extract_snippets(html, args.keyword)
                for s in snips:
                    s["engine"] = engine
                all_snippets.extend(snips)
                print(f"  ✅ {engine}: {len(snips)} 条")
            else:
                print(f"  ❌ {engine}: 无结果")

    # 去重（按标题）
    seen_titles = set()
    unique = []
    for s in all_snippets:
        t = s.get("title", "")
        if t and t not in seen_titles and len(t) > 5:
            seen_titles.add(t)
            unique.append(s)

    result = {
        "keyword":  args.keyword,
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total":    len(unique),
        "snippets": unique[:args.count]
    }

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    json.dump(result, open(args.output, "w"), ensure_ascii=False, indent=2)
    print(f"\n✅ 采集完成: {len(unique)} 条 → {args.output}")

if __name__ == "__main__":
    main()
