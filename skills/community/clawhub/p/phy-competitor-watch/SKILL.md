---
name: Competitor Watch
description: Competitor social media content strategy analyzer. Feed it a JSON file of any competitor's posts and get a full strategy breakdown — topic distribution, content style analysis (listicle/story/contrarian/how-to/data-driven/thread), posting schedule, top-performing content patterns, and exploitable gaps (topics and styles they DON'T cover). Works with any platform's exported data. No API keys needed. Zero external dependencies.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - social-media
  - competitive-intelligence
  - content-strategy
  - analytics
  - marketing
---

# phy-competitor-watch — Competitor Content Strategy Analyzer

Feed it a competitor's posts, get their entire content strategy decoded.

```bash
python3 ~/.claude/skills/phy-competitor-watch/scripts/competitor_watch.py \
  --file competitor_posts.json --name "Dan Koe"
```

## What It Analyzes

- **Topic distribution** — what they write about most (AI/ML, DevTools, StartupGrowth, etc.)
- **Content styles** — listicle, story, contrarian, how-to, data-driven, question-led, announcement, thread
- **Posting schedule** — which days they post, frequency per week
- **Top performers** — their best posts by engagement + what made them work
- **Gaps you can exploit** — topics and styles they DON'T cover

## Input Format

```json
[
  {"text": "Post content...", "platform": "linkedin", "date": "2026-03-01", "engagement": 5.2},
  {"text": "Another post...", "date": "2026-02-28", "engagement": 12.1}
]
```

## Collecting Competitor Data

Use `phy-twitter-scrape`, Reddit API exports, or manual collection. The tool works with any JSON array of posts.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
