# GxpCode Skill — Parser: JSCDI JS onclick list
# 特征: onclick 属性中的日期和链接 + 内链拼接

from . import _parse_onclick


def parse(page, source_name: str, jurisdiction: str) -> list:
    source_url = page.url
    entries = _parse_onclick(page, source_url)
    items = []
    for e in entries:
        title = e.get("title", "")
        url = e.get("url", "")
        if not title or not url:
            continue
        items.append({
            "source": source_name,
            "jurisdiction": jurisdiction,
            "title": title,
            "url": url,
            "date": e.get("date", ""),
            "summary": "",
            "source_type": "web",
            "confidence": "high",
        })
    return items
