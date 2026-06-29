# GxpCode Skill — Parser: FDA guidance tables
# 适用: FDA guidance snapshot, guidance list 等标准表格页
# 特征: HTML <table> 表格，标题在第一列，日期在最后一列

from playwright.sync_api import Page


def parse(page: Page, source_name: str, jurisdiction: str) -> list:
    """
    从 FDA 表格页提取条目。
    寻找标题含 "Guidance" 的表格，取第一列为 title，最后一列为 date。
    """
    items = []

    # 找到包含 Guidance 列的表格
    tables = page.query_selector_all("table")
    target_table = None
    for tbl in tables:
        headers = [th.inner_text().strip() for th in tbl.query_selector_all("th")]
        header_text = " ".join(headers)
        if "Guidance" in header_text and "Date" in header_text:
            target_table = tbl
            break

    if not target_table:
        # 回退：用第一个有 th 的表格
        for tbl in tables:
            if tbl.query_selector("th"):
                target_table = tbl
                break

    if not target_table:
        return items

    rows = target_table.query_selector_all("tbody tr")
    if not rows:
        rows = target_table.query_selector_all("tr")

    for row in rows:
        cells = row.query_selector_all("td")
        if len(cells) < 2:
            continue

        # 第一列 = title
        title = cells[0].inner_text().strip()
        if not title or len(title) < 10:
            continue

        # 找日期列（包含 MM/DD/YYYY 的单元格）
        date = ""
        for cell in cells:
            t = cell.inner_text().strip()
            import re
            if re.match(r"\d{2}/\d{2}/\d{4}", t):
                date = t
                break

        # 拿第一个链接作为 URL
        url = ""
        first_link = cells[0].query_selector("a[href]")
        if first_link:
            url = first_link.evaluate("el => el.href")

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
