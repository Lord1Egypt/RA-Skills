# GxpCode Skill — Parser: PIC/S publications table
# 特征: data-order 日期属性 + title 即链接

from . import _parse_data_order


def parse(page, source_name: str, jurisdiction: str) -> list:
    entries = _parse_data_order(page)
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
