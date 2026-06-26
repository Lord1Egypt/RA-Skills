---
name: lowyat-forum-research
description: Research any topic by searching Lowyat forum (forum.lowyat.net), scraping relevant threads into Excel, and analyzing the results. Use this skill whenever the user wants to research, scrape, or extract opinions/recommendations from Lowyat forum. Triggers on keywords like "lowyat", "LYN", "forum research", or any Malaysian consumer research topic (e.g. renovation, gadgets, cars, property, food).
slug: lowyat-forum-research
display_name: Lowyat Forum Research & Analysis
owner: johnson
version: 1.0.0
tags:
  - lowyat
  - forum
  - malaysia
  - research
  - analysis
  - consumer-review
  - web-scraping
  - data-extraction
---

# Lowyat Forum Research Tool

End-to-end research pipeline: **Search → Scrape → Analyze**

## Workflow

### Step 1: Understand the user's research topic
- Ask clarifying questions if needed (e.g. what specifically they want to learn)
- Break the topic into 3-5 search keyword variations

### Step 2: Search for relevant threads
- Use `WebSearch` with `site:forum.lowyat.net <keywords>` to find threads
- Use `allowed_domains: ["forum.lowyat.net"]` to filter results
- Run multiple searches in parallel with different keyword angles
- Present the most relevant threads to the user with titles and URLs
- Let the user pick which threads to scrape, or recommend the best ones

### Step 3: Scrape the selected threads
- The scraper script (`datascraping.py`) should be in the project root
- Install Python dependencies:

```bash
pip install requests beautifulsoup4 html5lib openpyxl tqdm
```

Or if you have [uv](https://docs.astral.sh/uv/) installed:

```bash
uv sync
```

- Run the scraper for each thread:

```bash
python datascraping.py <TOPIC_URL>
```

- **IMPORTANT**: Do NOT include `/all` or `/+N` suffixes in the URL — just use the base topic URL (e.g. `https://forum.lowyat.net/topic/5411252`)
- To scrape multiple threads, run them **sequentially** (one at a time) to be respectful to the server. Only run up to 3 in parallel if the user explicitly asks for speed, using `&` and `wait`
- Output: `<topic_id>.xlsx` files with columns: `Name`, `Date`, `Comment`

### Step 4: Analyze the scraped data
- Read the scraped `.xlsx` files to understand the forum discussions
- Synthesize findings across all threads into a structured summary
- Organize insights by the user's research questions
- Include: consensus opinions, brand recommendations, price ranges, warnings, and specific user experiences
- Cite which thread/user said what when relevant

## Scraper Details

- Forum uses 20 posts per page, paginated via `/+N` URL suffix
- Scraper auto-detects total pages and crawls all of them
- Random 0.5–2s delay between page requests
- Saves incrementally after each page — safe to interrupt
- If `.xlsx` already exists, it resumes by appending

## Tips for good searches

- Use brand names: `site:forum.lowyat.net Toto toilet`
- Use Malay keywords too: `site:forum.lowyat.net kipas exhaust tandas`
- Add "recommendation" or "review": `site:forum.lowyat.net water heater recommendation`
- Search by location: `site:forum.lowyat.net bathroom shop KL Selangor`
- Try year filters for recency: `site:forum.lowyat.net smart toilet 2024 2025`

## Example usage

User: "I want to research mechanical keyboards on Lowyat"

1. Search with variations: `mechanical keyboard recommendation`, `cherry mx switch`, `keychron Malaysia`, `custom keyboard`
2. Present top threads to user
3. Scrape selected threads in parallel
4. Read the xlsx files and provide analysis: popular brands, price ranges, where to buy, common complaints

## Links

- **GitHub**: [github.com/superoo7/lowyat-forum-research](https://github.com/superoo7/lowyat-forum-research)
- **ClawHub**: [clawhub.ai/superoo7/lowyat-forum-research](https://clawhub.ai/superoo7/lowyat-forum-research)

## Disclaimer

Scraped data contains publicly available usernames, dates, and comments from forum.lowyat.net. This tool is intended for personal research purposes only. Users are responsible for how they store, share, and use the scraped data in compliance with applicable privacy laws and Lowyat forum's terms of service.
