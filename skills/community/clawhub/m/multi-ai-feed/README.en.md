# Multi-Platform AI Feed / multi-ai-feed

---

## Introduction

Ask once and get the trending AI content from all five platforms — Kuaishou, WeChat Official Accounts, Bilibili, WeChat Channels and Xiaohongshu. Topics are clustered automatically, compared across platforms, and delivered as a single visual daily report, with an actionable intelligence investigation guide for each platform's hot topics.

**Core Value**

- **Five platforms in one pass**: No more asking about each platform separately and stitching the answers together by hand — describe what you need once and get the full picture.
- **Tell a global trend from a platform-local one**: See how many items each topic has on each platform and how many platforms it covers, so you can instantly tell real cross-platform buzz from a single-community spike.
- **Ranking that fits each platform**: Bilibili is ranked by likes; Kuaishou, Official Accounts, Channels and Xiaohongshu are ranked by engagement (likes + shares + comments) — never scored on a metric the API does not return.
- **Topics grouped automatically**: Directions such as AI tutorials, large models and AI art are decided by that day's actual content, with no categories to set up in advance.
- **Intelligence guidance you can act on**: Every platform's TOP topics come with a matched investigation mode, a search engine combination and credibility labels, ready to be verified.
- **One report that accumulates over time**: Daily reports are named by date and stored locally, so you can revisit any past day's cross-platform AI trends.

**Who It's For**

- 🤖 **AI content researchers** — Grasp the AI hot topics across all five platforms with a single daily question, instead of browsing each platform.
- 📊 **Industry intelligence analysts** — Judge whether a trend is genuine via cross-platform coverage, then verify key claims with the investigation guide.
- 🎬 **Content creators / operators** — Spot rising topic directions and decide which platform to publish them on first.
- 📈 **Brand / marketing leads** — Track how the same topic performs differently per platform to inform content and distribution strategy.

---

## Features

### Core Capabilities

- **Freely combine platforms**: Query all five, just one, or any subset — plain Chinese/English platform names are accepted.
- **Trending content discovery**: High-engagement items are selected by each platform's primary metric, with the top-ranked works shown per category.
- **Intelligent topic clustering**: The day's hot topic directions are identified and grouped automatically, entirely driven by the actual content.
- **Cross-platform topic comparison**: Counts each topic's items per platform and its platform coverage, surfacing genuinely global trends fast.
- **AI intelligence investigation**: Matches each platform's TOP topics to an investigation mode and search engine combination, then outputs a structured guide with credibility labels.
- **Custom keyword targeting**: Supports one global keyword set, or different keyword sets per platform, to cover niche directions precisely.
- **Visual daily report**: A single page containing the cross-platform overview, the cross-platform topic comparison and one section per platform, with platform filter tabs and each platform's own brand color.
- **Cover images that actually load**: A built-in local image proxy works around the hotlink protection on some platforms' cover images.
- **Daily subscription**: Once enabled, a report is produced automatically at 17:00 every day, using the platform scope and keywords you chose when subscribing.

---

## API Key Acquisition & Security

- This skill requires the environment variable `REDFOX_API_KEY`.
- `REDFOX_API_KEY` is provided by [RedFoxHub](https://redfox.hk/settings/api-keys?source=clawhub) (`https://redfox.hk`).
- Please register at [RedFoxHub](https://redfox.hk?source=clawhub) to obtain your `REDFOX_API_KEY`.
- Configure the `REDFOX_API_KEY` environment variable on your device before using this skill.
- Before providing a key, confirm its source, scope of use, validity period, and whether it can be reset or revoked.
- Never hardcode or expose the key in plaintext in code, prompts, logs, or output files.

---

## How to Use

Just describe what you need in plain language — no commands to memorize.

### Common Phrases

| Intent | Example Phrasing | Result |
| ------ | ---------------- | ------ |
| Latest all-platform report | "Generate today's multi-platform AI daily report" | Queries all five platforms and outputs the cross-platform overview, topic comparison and per-platform investigation guides |
| Only a few platforms | "Just show me AI trends on Bilibili and Xiaohongshu" | Queries the specified platforms; the report contains only those sections |
| A single platform | "Generate the Kuaishou AI daily report" | Single-platform query, equivalent to that platform's dedicated report |
| A specific past day | "Check the all-platform AI trends for 2026-08-30" | Retrieves that date's trending content and topic distribution |
| A date range | "Show me last week's all-platform AI hits" | Queries by date range and aggregates the trending content within it |
| One direction across platforms | "Find trending AI art content across all platforms" | Uses your keywords for targeted queries on all five platforms |
| Different direction per platform | "Bilibili for RAG and fine-tuning, Xiaohongshu for AI tutorials, Official Accounts for long-form large-model pieces" | Assigns separate keyword sets per platform and runs them all at once |
| Compare a topic's distribution | "How hot is the large-model topic on each platform" | Outputs that topic's item count per platform and its platform coverage |
| Enable daily subscription | "Subscribe me to the multi-platform AI daily report" | Auto-generates at 17:00 daily, accumulating reports locally |
| Cancel subscription | "Cancel my multi-platform AI daily report subscription" | Turns off daily auto-generation |
| Check subscription status | "Which platforms am I subscribed to for the AI report" | Shows the subscribed platform scope, keywords and run time |

### Sample Output

After the report is generated, you receive a structured conversational report, roughly as follows (illustrative):

**Multi-Platform AI Feed · 2026-08-31 Daily Report**

Covering 5 platforms · 620 items scanned · 18 topic clusters · 2.846M total engagement

**Cross-Platform Overview**

| Platform | Clusters | Items | Top Metric | Total Engagement |
|----------|----------|-------|------------|------------------|
| Kuaishou | 4 | 200 | 4.8K engagement | 963K |
| Official Accounts | 3 | 86 | 4.9K engagement | 421K |
| Bilibili | 4 | 200 | 3.6K likes | 887K |
| Channels | 3 | 74 | 4.3K engagement | 315K |
| Xiaohongshu | 4 | 60 | 4.3K engagement | 260K |

**Cross-Platform Topic Comparison**

| Topic | Kuaishou | Official Accounts | Bilibili | Channels | Xiaohongshu | Coverage |
|-------|----------|-------------------|----------|----------|-------------|----------|
| AI Art | 52 | 18 | 61 | — | 23 | 4/5 |
| Large Models | 34 | 27 | 45 | 19 | — | 4/5 |

**Global trends**: AI Art and Large Models each cover 4 platforms, making them the day's global trends; Channels has no AI Art content yet, which is an opening for differentiated positioning.

Each platform's category overview, emerging momentum signals, key creators, TOP topic investigation reports and cross-platform recommendations follow in turn.

---

## Use Cases

| Scenario | Role | Example Query | Benefit |
| -------- | ---- | ------------- | ------- |
| Daily cross-platform AI trend tracking | AI researcher / operator | "Generate today's multi-platform AI daily report" | Grasp all five platforms' AI hits and topic distribution at once, without checking each separately |
| Judging whether a trend is genuine | Industry intelligence analyst | "Is the AI Agent topic being discussed everywhere" | Distinguish global trends from platform-local spikes via coverage counts |
| Matching topics to platforms | Content creator | "Which platform is hottest for AI art right now" | Identify the high-momentum platform for that direction and prioritize publishing there |
| Niche direction mining | Content operator | "Find all-platform hits about ComfyUI and Stable Diffusion" | Focus on a specific track with custom keywords to support topic decisions |
| Differentiated per-platform research | Brand / marketing lead | "Bilibili for technical angles, Xiaohongshu for tutorials, Official Accounts for deep long-form" | Collect separately for each platform's content ecosystem, avoiding mixed-up yardsticks |
| Competitor & topic verification | Industry analyst | "Check recent all-platform trends about large models and do an intelligence analysis" | Get a structured report with investigation modes, engine combinations and credibility labels |
| Historical review | Content operator | "Check last Wednesday's all-platform AI trends" | Revisit past reports and compare how topic momentum changed over time |
| Long-term automatic accumulation | Team lead | "Subscribe to the multi-platform AI daily report" | Auto-generated at 17:00 daily and accumulated locally into a searchable archive |

---

## Important Data Notes

- **Update times differ by platform**: Kuaishou and Bilibili update the previous day's content at 15:00 daily; Official Accounts, Channels and Xiaohongshu update at 16:00 daily.
- **Today's data is not available**: Before the update time, the latest queryable date is the day before yesterday; after it, the latest queryable date is yesterday. When you ask for a date that has not been updated yet, you are told the latest available date and asked to confirm first — no quota is spent querying a date that has no data.
- **Multi-platform queries use a shared date**: Because update times differ, querying several platforms at once uses the latest date on which all of them have updated, preventing empty results from some platforms.
- **Official Accounts cannot be filtered by date**: That data service does not support time filtering, so it returns the most recently indexed articles; the date you specify only affects the date label on the report, not the returned content.
- **Channels has no external links**: WeChat Channels works cannot be opened outside the app, so titles appear as plain text in the report with no detail link.
- **AI-related content only**: All five platform data services index AI-related content only — this is not the platforms' full inventory.
- **Subscription run time**: Runs at 17:00 daily, later than every platform's update time, so all five have published that day's data.

---
