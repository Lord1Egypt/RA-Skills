# GxpCode Skill — Parser: FDA FOIA Electronic Reading Room
# 特征: HTML 表格，Company Name 列=标题，Record Date 列=日期

import re
from playwright.sync_api import Page


def parse(page: Page, source_name: str, jurisdiction: str) -> list:
    items = []

    tables = page.query_selector_all("table")
    target = None
    for tbl in tables:
        headers = [th.inner_text().strip() for th in tbl.query_selector_all("th")]
        if "Company Name" in headers and "Record Date" in headers:
            target = tbl
            break

    if not target:
        return items

    # 确定列索引
    headers = [th.inner_text().strip() for th in target.query_selector_all("th")]
    try:
        date_idx = headers.index("Record Date")
    except ValueError:
        date_idx = 0
    try:
        name_idx = headers.index("Company Name")
    except ValueError:
        name_idx = 1

    rows = target.query_selector_all("tbody tr") or target.query_selector_all("tr")
    for row in rows:
        cells = row.query_selector_all("td")
        if len(cells) <= max(date_idx, name_idx):
            continue

        title = cells[name_idx].inner_text().strip()
        if not title or len(title) < 3:
            continue

        date = cells[date_idx].inner_text().strip()

        url = ""
        link = cells[name_idx].query_selector("a[href]")
        if link:
            url = link.evaluate("el => el.href")

        items.append({
            "source": source_name,
            "jurisdiction": jurisdiction,
            "title": title,
            "url": url,
            "date": date,
            "summary": "",
            "source_type": "web",
            "confidence": "high",
        })
    return items
