# GxpCode Skill — Parser: 广东药监局 政务公开
# 适用: mpa.gd.gov.cn 政务公开列表页
# DOM: <li><h4><a href="...">标题</a><span class="time">[ 2026-05-26 ]</span></h4></li>

import re


def parse(page, source_name: str, jurisdiction: str) -> list:
    entries = []

    for li in page.query_selector_all("li"):
        a_el = li.query_selector("a[href*='content']")
        if not a_el:
            continue

        title = a_el.inner_text().strip()
        url = a_el.get_attribute("href") or ""

        if not title or not url:
            continue

        span_el = li.query_selector("span.time")
        date_text = span_el.inner_text().strip() if span_el else ""

        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", date_text)
        date = date_match.group(1) if date_match else ""

        entries.append({
            "title": title,
            "url": url,
            "date": date,
        })

    return _build_items(entries, source_name, jurisdiction)


def _build_items(entries: list, source_name: str, jurisdiction: str) -> list:
    items = []
    for e in entries:
        items.append({
            "source": source_name,
            "jurisdiction": jurisdiction,
            "title": e["title"],
            "url": e["url"],
            "date": e.get("date", ""),
            "summary": "",
            "source_type": "web",
            "confidence": "high",
        })
    return items
