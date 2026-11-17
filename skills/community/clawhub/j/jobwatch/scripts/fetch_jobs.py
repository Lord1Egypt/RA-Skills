#!/usr/bin/env python3
"""感知层：从各家 ATS 官方 API / RSS 抓岗位列表，输出标准化 SourceItem 数组。

支持的信源类型（config.json sources[].kind）：
- greenhouse  boards-api.greenhouse.io（如 Anthropic、DeepMind）
- ashby       api.ashbyhq.com/posting-api（如 OpenAI）
- lever       api.lever.co/v0/postings
- rss         任意 RSS/Atom feed（url 字段），适合博客/公告类信源

SourceItem: {source, company, doc_id, title, location, detail_url, updated_at, content_hash}
新增信源类型 = 加一个 fetch_ 函数 + 注册进 FETCHERS，下游完全不动。
"""
import hashlib
import json
import sys
import time
import xml.etree.ElementTree as ET

from common import CONFIG, http, http_json


def _hash(*parts):
    return hashlib.sha256("|".join(p or "" for p in parts).encode()).hexdigest()[:16]


def _item(src, jid, title, location, url, updated, posted=""):
    return {
        "source": src["id"], "company": src["company"],
        "doc_id": f"{src['id']}:{jid}", "title": title or "",
        "location": location or "", "detail_url": url or "",
        "updated_at": updated or "", "posted_at": posted or "",
        "content_hash": _hash(title, location, updated),
    }


def fetch_greenhouse(src):
    data = http_json(f"https://boards-api.greenhouse.io/v1/boards/{src['board']}/jobs")
    return [_item(src, j["id"], j.get("title"), (j.get("location") or {}).get("name"),
                  j.get("absolute_url"), j.get("updated_at"), j.get("first_published"))
            for j in data.get("jobs", [])]


def fetch_ashby(src):
    data = http_json(f"https://api.ashbyhq.com/posting-api/job-board/{src['board']}")
    return [_item(src, j["id"], j.get("title"), j.get("location"),
                  j.get("jobUrl") or j.get("applyUrl"), j.get("publishedAt"),
                  j.get("publishedAt"))
            for j in data.get("jobs", []) if j.get("isListed") is not False]


def fetch_lever(src):
    data = http_json(f"https://api.lever.co/v0/postings/{src['board']}?mode=json")
    return [_item(src, j.get("id"), j.get("text"),
                  (j.get("categories") or {}).get("location"),
                  j.get("hostedUrl"), str(j.get("createdAt", "")))
            for j in (data if isinstance(data, list) else [])]


def fetch_rss(src):
    """通用 RSS/Atom（stdlib 解析）。适合博客、公告页信源。"""
    status, body = http(src["url"], timeout=45)
    if status >= 300:
        raise RuntimeError(f"RSS HTTP {status} for {src['url']}")
    root = ET.fromstring(body)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items = []
    for e in root.iter("item"):  # RSS 2.0
        link = (e.findtext("link") or "").strip()
        items.append(_item(src, _hash(link), e.findtext("title"), "",
                           link, e.findtext("pubDate")))
    for e in root.iter("{http://www.w3.org/2005/Atom}entry"):  # Atom
        link_el = e.find("a:link", ns)
        link = link_el.get("href") if link_el is not None else ""
        items.append(_item(src, _hash(link), e.findtext("a:title", "", ns), "",
                           link, e.findtext("a:updated", "", ns)))
    return items




def fetch_gcareers(src):
    """Google Careers（SPA、无公开 API）：Firecrawl 渲染搜索结果页后解析岗位链接。

    GDM 的工程岗不走 Greenhouse 而走 Google Careers，故需此信源。
    解析只依赖 jobs/results/<数字id>- 的 URL 模式，对页面改版有较强容忍度。
    无 FIRECRAWL_API_KEY 时降级 Jina Reader。config 字段：query（搜索词）、pages（默认 2）。
    """
    import re
    import urllib.parse
    from enrich_jd import firecrawl_scrape, jina_reader

    q = urllib.parse.quote(src.get("query", src["company"]))
    items, seen = [], set()
    for page in range(1, int(src.get("pages", 2)) + 1):
        url = ("https://www.google.com/about/careers/applications/jobs/results/"
               f"?q={q}&page={page}")
        md = None
        last_err = None
        for fn in (firecrawl_scrape, jina_reader):
            try:
                md = fn(url)
                break
            except Exception as e:  # noqa: BLE001
                last_err = e
        if md is None:
            raise RuntimeError(f"gcareers scrape failed: {last_err}")
        found = 0
        for m in re.finditer(
                r"\[([^\]]{4,120})\]\((https://www\.google\.com/about/careers/"
                r"applications/jobs/results/(\d+)-[^)\s]*)\)", md):
            title = re.sub(r"\s+", " ", m.group(1)).strip(" *_")
            link, jid = m.group(2), m.group(3)
            if jid in seen or title.lower() in ("learn more", "apply", "share"):
                continue
            seen.add(jid)
            found += 1
            items.append(_item(src, jid, title, "", link, ""))
        if found == 0:  # 空页 = 到底了
            break
    return items


FETCHERS = {"greenhouse": fetch_greenhouse, "ashby": fetch_ashby,
            "lever": fetch_lever, "rss": fetch_rss, "gcareers": fetch_gcareers}


def fetch_all():
    """Returns (items, errors). One source failing doesn't kill the others (失败隔离)."""
    items, errors = [], []
    for src in CONFIG["sources"]:
        if "REPLACE_ME" in json.dumps(src):
            errors.append({"source": src.get("id", "?"), "stage": "fetch",
                           "error": "source not configured (REPLACE_ME placeholder) — "
                                    "finish onboarding: probe boards with discover_board.py "
                                    "and write real sources into config.json"})
            continue
        try:
            items.extend(FETCHERS[src["kind"]](src))
        except Exception as e:  # noqa: BLE001
            errors.append({"source": src["id"], "stage": "fetch", "error": str(e)[:300]})
        time.sleep(0.2)
    return items, errors


if __name__ == "__main__":
    items, errors = fetch_all()
    json.dump({"items": items, "errors": errors}, sys.stdout, ensure_ascii=False, indent=1)
    print(f"\n# {len(items)} items, {len(errors)} errors", file=sys.stderr)
