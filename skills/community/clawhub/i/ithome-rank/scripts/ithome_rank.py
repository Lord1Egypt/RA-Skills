#!/usr/bin/env python3
"""抓取 IT之家 日榜/周榜/月榜 热门文章"""
import requests, re, sys
from datetime import date

def fetch_rank(rank_type="日榜"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    r = requests.get("https://www.ithome.com/", headers=headers, timeout=15)
    r.encoding = "utf-8"
    html = r.text

    rank_start = html.find('<div id="rank"')
    if rank_start == -1:
        return []
    rank_end = html.find('</div>', html.find('</div>', html.find('</div>', rank_start) + 1) + 1) + 6
    rank_html = html[rank_start:rank_end]

    type_map = {"日榜": "1", "周榜": "2", "月榜": "3"}
    data_id = type_map.get(rank_type, "1")

    pattern = rf'id="d-{data_id}"[^>]*>(.*?)</ul>'
    match = re.search(pattern, rank_html, re.DOTALL)
    if not match:
        return []

    items_html = match.group(1)
    links = re.findall(
        r'<a[^>]*title="([^"]*)"[^>]*href="([^"]*)"[^>]*>',
        items_html
    )
    return links


def format_message(articles, rank_name="日榜"):
    today = date.today()
    month, day = today.month, today.day
    lines = [f"📰 IT之家{rank_name}热门 — {month}月{day}日"]
    lines.append("━" * 20)
    if not articles:
        lines.append("（暂无数据）")
    else:
        for i, (title, url) in enumerate(articles, 1):
            lines.append(f"{i}. 🔥 [{title}]({url})")
    lines.append("")
    lines.append("_来源：IT之家_")
    return "\n".join(lines)


if __name__ == "__main__":
    rank_type = sys.argv[1] if len(sys.argv) > 1 else "日榜"
    articles = fetch_rank(rank_type)
    print(format_message(articles, rank_type))