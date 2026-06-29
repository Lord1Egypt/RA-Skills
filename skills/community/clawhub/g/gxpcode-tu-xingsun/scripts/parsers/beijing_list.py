# GxpCode Skill — Parser: 北京药监局 通知公告
# 适用: yjj.beijing.gov.cn 通知列表页
# DOM: <LI class="easysite-article-li"><P class="article-title xinwen"><A>标题</A></P><SPAN class="article-time xwdate fr">日期</SPAN></LI>

import re


def parse(page, source_name: str, jurisdiction: str) -> list:
    entries = []

    for li in page.query_selector_all("li.easysite-article-li"):
        a_el = li.query_selector("a")
        span_el = li.query_selector("span.article-time, span.xwdate")

        title = a_el.inner_text().strip() if a_el else ""
        url = a_el.get_attribute("href") if a_el else ""
        date_text = span_el.inner_text().strip() if span_el else ""

        if not title or not url:
            continue

        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", date_text)
        date = date_match.group(1) if date_match else date_text

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
