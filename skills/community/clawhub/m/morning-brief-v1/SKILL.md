\---

name: morning-brief
description: "Use when user asks for a morning brief, daily briefings, or what's happening in the world. Fetches news from trusted international RSS feeds."
---

# Morning Brief

This skill pulls the latest headlines from a reliable international RSS feed and presents a concise list of news titles. It is ideal for a quick, up-to-date snapshot of global events at the start of your day.

## Usage

```bash
# Run the script:
python3 scripts/fetch\\\_clean\\\_headlines.py
```

\## 🟢 Information Presentation Protocol (信息展示铁律)

When reporting news, RSS feeds, or script outputs that contain URLs/links, you MUST preserve the original Markdown links exactly as provided by the tool.

\*\*NEVER strip, summarize, or remove the URLs.\*\*

Output format must strictly be: `- \\\[Headline Title](Original URL)` so that user can click and read the details.

\## Translate all headlines into Chinese, write a brief that you would like to see.

The script will prompt for a feed URL or use the default, then prints headlines per line. Optionally use `--limit N`.

## Requirements

* Python 3.8+
* `requests` and `beautifulsoup4` packages.

