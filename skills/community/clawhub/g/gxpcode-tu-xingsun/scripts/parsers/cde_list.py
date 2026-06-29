# GxpCode Skill — Parser: CDE list pages
# 适用: CDE-指导原则, CDE-征求意见, CDE-政策法规, CDE-政策解读
# 特征: 行模式日期 + text:【查看详情】链接

import re

LINK_TEXT = "【查看详情】"


def parse(page, source_name: str, jurisdiction: str) -> list:
    """
    从 CDE 列表页提取条目。
    DOM 结构: div.listWrapper > div.news_content_box
    innerText 格式:
      2026.06 01
      法规标题
      【查看详情】
      >
    """
    from . import _parse_body, _pair_links

    body = page.evaluate("() => document.body.innerText")
    entries = _parse_body(body, "行模式")
    entries = _pair_links(entries, page, LINK_TEXT, text_match_mode=True)
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
