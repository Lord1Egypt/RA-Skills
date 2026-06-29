# GxpCode Skill — Parser: NIFDC 标准物质通知公告列表页
# 适用: www.nifdc.org.cn 标准物质与菌毒种/通知公告
# DOM: <ul><li><a href="..." title="...">标题</a><span>(日期)</span></li></ul>
# 分页: index_N.html, 首页为 index.html

import re
from urllib.parse import urljoin


def parse(page, source_name: str, jurisdiction: str) -> list:
    entries = []

    # 列表容器: .list > ul > li
    list_ul = page.query_selector(".list ul")
    if not list_ul:
        return _build_items(entries, source_name, jurisdiction, "https://www.nifdc.org.cn")

    for li in list_ul.query_selector_all("li"):
        a_el = li.query_selector("a")
        span_el = li.query_selector("span")
        if not a_el:
            continue

        href = a_el.get_attribute("href") or ""
        title = (a_el.get_attribute("title") or a_el.inner_text()).strip()
        date_text = span_el.inner_text().strip() if span_el else ""

        # 日期格式: (2026-06-09)
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", date_text)
        date = date_match.group(1) if date_match else ""

        if not title or not href:
            continue

        entries.append({
            "title": title,
            "url": href,
            "date": date,
        })

    return _build_items(entries, source_name, jurisdiction, "https://www.nifdc.org.cn")


def _build_items(entries: list, source_name: str, jurisdiction: str, base_url: str) -> list:
    items = []
    for e in entries:
        # 将相对路径 URL 转为绝对路径
        abs_url = urljoin(base_url, e["url"])
        items.append({
            "source": source_name,
            "jurisdiction": jurisdiction,
            "title": e["title"],
            "url": abs_url,
            "date": e.get("date", ""),
            "summary": "",
            "source_type": "web",
            "confidence": "high",
        })
    return items
