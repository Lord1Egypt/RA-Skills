#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
liken 存在性核实脚本（只核实"作品是否真实存在"，不做相似推荐；相似由 LLM 按品味维度推理）。

可用源（均免费无 key，已实测）：
  book  -> OpenLibrary   https://openlibrary.org/search.json
  music -> iTunes Search  https://itunes.apple.com/search?media=music
  movie -> Wikidata      https://www.wikidata.org/w/api.php (wbsearchentities)
  show  -> TVmaze        https://api.tvmaze.com/search/shows

已弃用（不可达，不要再调）：TasteDive（Cloudflare 拦截）、Google Books（429 限流）。

用法：
  py recommend.py book "<书名>"
  py recommend.py music "<歌名/艺人名>"
  py recommend.py movie "<电影名>"

输出 JSON 到 stdout；错误打到 stderr。代理：读 HTTPS_PROXY / HTTP_PROXY。
"""
import sys, os, json, argparse, urllib.request, urllib.parse

OPENLIBRARY = "https://openlibrary.org/search.json"
ITUNES = "https://itunes.apple.com/search"
WIKIDATA = "https://www.wikidata.org/w/api.php"
TVMAZE = "https://api.tvmaze.com/search/shows"


def _opener():
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not proxy:
        proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    if proxy:
        handler = urllib.request.ProxyHandler({"https": proxy, "http": proxy})
        return urllib.request.build_opener(handler)
    return urllib.request.build_opener()


def _get_json(url, timeout=20, data=None):
    opener = _opener()
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers={
        "User-Agent": "liken/0.2 (existence-check)",
        "Accept": "application/json",
    })
    with opener.open(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def check_book(name, limit=3):
    q = urllib.parse.urlencode({"q": name, "limit": limit,
                               "fields": "title,author_name,first_publish_year"})
    data = _get_json(f"{OPENLIBRARY}?{q}")
    docs = data.get("docs", [])[:limit]
    return {"source": "openlibrary", "exists": bool(docs),
            "hits": [{"title": d.get("title"),
                      "author": (d.get("author_name") or [None])[0],
                      "year": d.get("first_publish_year")} for d in docs]}


def check_music(name, limit=3):
    q = urllib.parse.urlencode({"term": name, "media": "music", "limit": limit})
    data = _get_json(f"{ITUNES}?{q}")
    res = data.get("results", [])[:limit]
    return {"source": "itunes-music", "exists": bool(res),
            "hits": [{"track": r.get("trackName"), "artist": r.get("artistName"),
                      "album": r.get("collectionName"),
                      "year": (r.get("releaseDate") or "")[:4]} for r in res]}


def check_movie(name):
    data = _get_json(WIKIDATA, data={
        "action": "wbsearchentities", "search": name,
        "language": "en", "format": "json", "type": "item", "limit": 5})
    hits = data.get("search", [])
    return {"source": "wikidata", "exists": bool(hits),
            "hits": [{"qid": h.get("id"), "label": h.get("label"),
                      "desc": h.get("description")} for h in hits]}


def check_show(name):
    q = urllib.parse.urlencode({"q": name})
    data = _get_json(f"{TVMAZE}?{q}")
    return {"source": "tvmaze", "exists": bool(data),
            "hits": [{"name": (d.get("show") or {}).get("name"),
                      "premiered": (d.get("show") or {}).get("premiered")} for d in data[:3]]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", help="book|music|movie|show")
    ap.add_argument("name")
    ap.add_argument("--limit", type=int, default=3)
    a = ap.parse_args()

    try:
        if a.mode == "book":
            out = check_book(a.name, a.limit)
        elif a.mode == "music":
            out = check_music(a.name, a.limit)
        elif a.mode == "movie":
            out = check_movie(a.name)
        elif a.mode == "show":
            out = check_show(a.name)
        else:
            print(f"[error] 未知模式: {a.mode}（支持 book|music|movie|show）", file=sys.stderr)
            sys.exit(2)
        out["query"] = a.name
        print(json.dumps(out, ensure_ascii=False, indent=2))
    except Exception as e:
        # 核实失败不阻断推荐流程：告诉上层"这次没核实到，按高把握处理并标待核实"
        print(json.dumps({"query": a.name, "exists": None,
                          "note": f"{type(e).__name__}: {e}",
                          "hint": "核实接口暂不可达，请只推高把握知名作品，存疑标待核实"},
                         ensure_ascii=False, indent=2))
        sys.exit(0)


if __name__ == "__main__":
    main()
