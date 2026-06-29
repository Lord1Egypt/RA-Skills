---
description: Use this skill when you need to fetch IT之家 (ithome.com) daily/weekly/monthly
  hot/ranking articles and push them to a messaging channel (WeChat, QQ, DingTalk,
  Feishu, etc.). Suitable for scheduled daily hot-news push or on-demand article list
  retrieval. Also triggered by phrases like "IT之家日榜", "ithome热门", "抓取it之家排行", "每日科技新闻推送".
name: ithome-rank
---

## Prerequisites

- Python 3 with `requests` library installed
- Network access to `https://www.ithome.com/`
- (Optional) QwenPaw cron and channel-send capabilities for scheduled push

## Script Location

The Python script is expected at:
```
scripts/ithome_rank.py
```
relative to the workspace root.

---

## 1. Create the Python fetch script

Create `scripts/ithome_rank.py` with the following content:

```python
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

    # 先找到 rank 区域（避免匹配到页面中其他 id="d-X" 的元素）
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
```

**Why this approach (no browser):** The server likely doesn't have Chrome/Chromium installed, so `browser_use` will fail. Using `requests` to fetch the HTML directly is more reliable and faster.

**Key parsing detail:** The IT之家 homepage has **two** `id="d-1"` elements — the first is a software download section, the second (inside `<div id="rank">`) contains the actual rank articles. Always locate the `rank` div first before extracting the article list.

## 2. Run the script and get formatted output

```bash
# 日榜（默认）
python3 scripts/ithome_rank.py 日榜

# 周榜
python3 scripts/ithome_rank.py 周榜

# 月榜
python3 scripts/ithome_rank.py 月榜
```

**Expected output format (markdown):**
```
📰 IT之家日榜热门 — 6月17日
━━━━━━━━━━━━━━━━━━━━
1. 🔥 [标题](链接)
2. 🔥 [标题](链接)
...
_来源：IT之家_
```

The 日榜 returns 12 articles.

## 3. Push the result to a messaging channel

First query the target session:

```bash
qwenpaw chats list --agent-id <agent_id> --channel <channel>
```

Then send:

```bash
qwenpaw channels send \
  --agent-id <agent_id> \
  --channel <channel> \
  --target-user <user_id> \
  --target-session <session_id> \
  --text "$(python3 scripts/ithome_rank.py 日榜)"
```

## 4. (Optional) Set up daily scheduled push

```bash
qwenpaw cron create \
  --agent-id <agent_id> \
  --type agent \
  --schedule-type cron \
  --name "IT之家日榜推送" \
  --cron "0 9 * * *" \
  --channel wechat \
  --target-user <user_id> \
  --target-session <session_id> \
  --text "请运行命令 python3 scripts/ithome_rank.py 日榜 并将输出结果推送给我" \
  --timeout 120 \
  --timezone Asia/Shanghai \
  --mode final
```

## Failure Modes and Recovery

| Problem | Symptom | Fix |
|---------|---------|-----|
| No Chrome/Chromium | `browser_use` fails | Use `requests` approach instead (this skill's default) |
| Wrong content extracted | Gets 最会买/要知 download links | Ensure `rank` div is located first before extracting list |
| Network unreachable | `requests.get` times out | Check proxy / network settings |
| HTML structure changed | Regex doesn't match | Inspect page source and update regex