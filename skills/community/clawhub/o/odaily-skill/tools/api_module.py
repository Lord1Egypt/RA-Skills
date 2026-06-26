"""
Tool: get_api_module
API模块化调用 — 通过 Odaily Web API 获取最新文章和快讯

文章接口: https://web-api.odaily.news/post/page?page=1&size=10
快讯接口: https://web-api.odaily.news/newsflash/page?page=1&size=10&groupId=0&isImport=false
"""

from __future__ import annotations

import re
import requests
from datetime import datetime, timezone, timedelta

from config.settings import settings
from lib.formatters import now_bjt

BJT = timezone(timedelta(hours=8))

ARTICLES_API = "https://web-api.odaily.news/post/page"
FLASH_API = "https://web-api.odaily.news/newsflash/page"


def _strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _fmt_ts(ts) -> str:
    """将时间戳（秒或毫秒）转为北京时间字符串"""
    if not ts:
        return ""
    try:
        t = int(ts)
        if t > 1e12:
            t = t // 1000
        return datetime.fromtimestamp(t, tz=BJT).strftime("%m-%d %H:%M")
    except Exception:
        return str(ts)


def get_api_module() -> str:
    session = requests.Session()
    session.headers.update({
        "User-Agent": settings.USER_AGENT,
        "Accept": "application/json",
        "Referer": "https://www.odaily.news/",
    })

    articles = []
    flash_list = []

    # 获取文章
    try:
        resp = session.get(
            ARTICLES_API,
            params={"page": 1, "size": 10},
            timeout=settings.REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("data", {})
        if isinstance(items, dict):
            items = items.get("items") or items.get("list") or items.get("data") or []
        elif not isinstance(items, list):
            items = []
        for item in items[:5]:
            articles.append({
                "title": item.get("title") or item.get("name") or "",
                "summary": item.get("summary") or item.get("description") or "",
                "url": item.get("url") or item.get("link") or (
                    f"https://www.odaily.news/post/{item.get('id')}" if item.get("id") else ""
                ),
                "published_at": _fmt_ts(
                    item.get("published_at") or item.get("created_at") or item.get("publish_time")
                ),
                "author": item.get("author") or "",
            })
    except Exception as e:
        articles = []
        _articles_err = str(e)
    else:
        _articles_err = ""

    # 获取快讯
    try:
        resp = session.get(
            FLASH_API,
            params={"page": 1, "size": 10, "groupId": 0, "isImport": "false"},
            timeout=settings.REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        items = data.get("data", {})
        if isinstance(items, dict):
            items = items.get("items") or items.get("list") or items.get("data") or []
        elif not isinstance(items, list):
            items = []
        for item in items[:5]:
            flash_list.append({
                "title": item.get("title") or item.get("name") or "",
                "description": _strip_html(item.get("description") or item.get("content") or ""),
                "url": item.get("url") or item.get("link") or (
                    f"https://www.odaily.news/newsflash/{item.get('id')}" if item.get("id") else ""
                ),
                "published_at": _fmt_ts(
                    item.get("published_at") or item.get("created_at") or item.get("publish_time")
                ),
            })
    except Exception as e:
        flash_list = []
        _flash_err = str(e)
    else:
        _flash_err = ""

    L = [
        "🔌 API模块化调用",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {now_bjt()} (北京时间)",
        f"📡 数据源: web-api.odaily.news",
        "",
    ]

    # 文章
    L.append("📰 最新文章（Top 5）")
    L.append("")
    if articles:
        for i, a in enumerate(articles, 1):
            L.append(f"  {i}. {a['title']}")
            if a.get("summary"):
                L.append(f"     {a['summary']}")
            if a.get("author"):
                L.append(f"     ✍️ {a['author']}")
            if a.get("published_at"):
                L.append(f"     ⏱ {a['published_at']}")
            if a.get("url"):
                L.append(f"     🔗 {a['url']}")
            L.append("")
    else:
        L += [f"  ⚠️ 暂时无法获取文章数据", ""]
        if _articles_err:
            L += [f"  （错误: {_articles_err[:80]}）", ""]

    # 快讯
    L += ["━━━━━━━━━━━━━━━━━━━━━━━━", "⚡ 最新快讯（Top 5）", ""]
    if flash_list:
        for i, f in enumerate(flash_list, 1):
            L.append(f"  {i}. {f['title']}")
            if f.get("description") and f["description"] != f["title"]:
                L.append(f"     {f['description']}")
            if f.get("published_at"):
                L.append(f"     ⏱ {f['published_at']}")
            if f.get("url"):
                L.append(f"     🔗 {f['url']}")
            L.append("")
    else:
        L += [f"  ⚠️ 暂时无法获取快讯数据", ""]
        if _flash_err:
            L += [f"  （错误: {_flash_err[:80]}）", ""]

    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "💡 以上为 Odaily Web API 实时数据，请结合内容给出分析",
    ]
    return "\n".join(L)
