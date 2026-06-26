---
name: ICCircle News
description: Fetch and aggregate semiconductor and chip industry news from IC技术圈 (iccircle.com) RSS feeds. Use when the user asks for 半导体新闻, 芯片行业资讯, IC技术圈动态, 芯片设计行业新闻, or semiconductor/chip industry news.
---

## Core Rules

1. **Execution**: Run `python3 <skill_dir>/scripts/agg_news.py` to fetch news.
2. **Output**: The script prints formatted news directly to stdout; capture and present to user.
3. **No arguments**: The script runs with predefined RSS sources and keywords; no extra parameters needed.
4. **Sources**: Aggregates from IC技术圈 (7 columns), VLSI Blogs, IT之家, 36氪.
5. **Presentation**: Preserve the formatted output structure with source headers, timestamps, and links.

## Data Storage

None. This skill executes a read-only script that fetches external RSS feeds.

## External Endpoints

| Service | URL | Purpose |
|---------|-----|---------|
| IC技术圈 | https://iccircle.com/feed | RSS feeds for 7 columns |
| VLSI Blogs | https://vlsiblogs.com/aggrss | RSS feeds for cadence and synopsys |
| IT之家 | https://www.ithome.com/rss/ | Tech news with keyword filtering |
| 36氪 | https://www.36kr.com/feed | Tech news with keywork filtering |
