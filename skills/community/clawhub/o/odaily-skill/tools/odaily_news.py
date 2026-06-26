"""
Tool: get_today_watch
今日必关注 — 从 Odaily RSS 文章 + 快讯中挑选最值得关注的内容并附信息源
"""

from __future__ import annotations

from lib.odaily_client import OdailyClient
from lib.formatters import now_bjt


def get_today_watch(limit: int = 10) -> str:
    client = OdailyClient()
    articles = client.get_hot_articles(limit=limit)
    flash = client.get_flash_news(limit=20)

    L = [
        "📌 今日必关注",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"⏰ {now_bjt()} (北京时间)",
        "",
    ]

    if articles:
        L.append("📰 重点文章")
        L.append("")
        for i, a in enumerate(articles, 1):
            L.append(f"  {i}. {a['title']}")
            if a.get("summary"):
                L.append(f"     {a['summary']}")
            if a.get("published_at"):
                L.append(f"     ⏱ {a['published_at']}")
            if a.get("url"):
                L.append(f"     🔗 {a['url']}")
            L.append("")
    else:
        L += ["⚠️ 暂时无法获取文章数据", ""]

    if flash:
        L += ["━━━━━━━━━━━━━━━━━━━━━━━━", "⚡ 重要快讯", ""]
        for f in flash:
            L.append(f"  • {f['title']}")
            if f.get("description") and f["description"] != f["title"]:
                L.append(f"    {f['description']}")
            if f.get("published_at"):
                L.append(f"    ⏱ {f['published_at']}")
            if f.get("url"):
                L.append(f"    🔗 {f['url']}")
            L.append("")
    else:
        L += ["⚠️ 暂时无法获取快讯数据", ""]

    L += [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "💡 请基于以上内容，筛选出今日最值得关注的事件，并给出简要分析和判断",
    ]
    return "\n".join(L)


# 保持向后兼容
def get_odaily_headlines(limit: int = 10, category: str = "all") -> str:
    return get_today_watch(limit=limit)
