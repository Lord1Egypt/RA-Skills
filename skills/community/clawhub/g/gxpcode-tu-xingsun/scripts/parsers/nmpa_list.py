# GxpCode Skill — Parser: NMPA list pages
# 适用: 所有 NMPA yaopin + xxgk/fgwj 栏目
# 特征: 括号内日期 + title 即链接

import re


def parse(page, source_name: str, jurisdiction: str) -> list:
    """
    从 NMPA 列表页提取条目。
    innerText 格式:
      标题内容 (2026-06-26)
    """
    from . import _parse_body, _pair_links

    body = page.evaluate("() => document.body.innerText")
    entries = _parse_body(body, "括号内")
    entries = _pair_links(entries, page, "title", text_match_mode=False)
    return _build_items(entries, source_name, jurisdiction)


def _build_items(entries: list, source_name: str, jurisdiction: str) -> list:
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
