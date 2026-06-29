# GxpCode Skill — Parser: 四川药监局 工作通知
# 适用: yjj.sc.gov.cn 工作通知列表页
# DOM: <TABLE><TR><TD class="ListColumnClass5"><A href="...">标题</A>YYYY-MM-DD</TD></TR></TABLE>

import re


def parse(page, source_name: str, jurisdiction: str) -> list:
    entries = []

    for td in page.query_selector_all("td.ListColumnClass5"):
        a_el = td.query_selector("a")
        if not a_el:
            continue

        title = a_el.inner_text().strip()
        url = a_el.get_attribute("href") or ""

        if not title or not url:
            continue

        # 日期在 A 标签之后，TD 的 innerText 为 "标题\tYYYY-MM-DD"
        full_text = td.inner_text()
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", full_text)
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
