# GxpCode Skill — Parser: 江苏药监局 公告通告
# 适用: da.jiangsu.gov.cn 公告通告列表页
# DOM: <table><tr><td><a class="bt_link" href="/art/...">标题</a></td><td><font>日期</font></td></tr></table>

import re
from urllib.parse import urljoin

BASE_URL = "https://da.jiangsu.gov.cn"


def parse(page, source_name: str, jurisdiction: str) -> list:
    entries = []

    rows = page.evaluate("""() => {
        const links = document.querySelectorAll('a.bt_link');
        const results = [];
        links.forEach(a => {
            if (!a.href) return;
            const tr = a.closest('tr');
            const font = tr ? tr.querySelector('font') : null;
            results.push({
                title: a.textContent.trim().replace(/^·\\s*/, ''),
                url: a.href,
                date: font ? font.textContent.trim() : ''
            });
        });
        return results;
    }""")

    for r in rows:
        title = r["title"]
        url = r["url"]
        if not title or not url:
            continue

        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", r.get("date", ""))
        date = date_match.group(1) if date_match else ""

        if not url.startswith("http"):
            url = urljoin(BASE_URL, url)

        entries.append({"title": title, "url": url, "date": date})

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
