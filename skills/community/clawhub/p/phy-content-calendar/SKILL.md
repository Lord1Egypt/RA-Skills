---
name: Content Calendar
description: Auto content calendar generator for social media. Takes your topic pillars and target platform, generates a 2-4 week posting calendar with style rotation (insight/story/data/contrarian/question/how-to/build-update), optimal day selection per platform, and draft outlines. Integrates with phy-content-compound to pull relevant content atoms for each scheduled post. Includes platform-specific best practices — LinkedIn (Tue-Thu, 3-4/week), Reddit (Mon-Thu, 2-3/week + daily comments), Twitter/X (daily, threads Wed/Thu), HackerNews (Mon-Wed, 1-2/week). Zero external dependencies.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - social-media
  - content-calendar
  - content-strategy
  - productivity
  - planning
  - scheduling
---

# phy-content-calendar — Auto Content Calendar

Stop deciding "what to post today." Generate a 2-week calendar with topic rotation, style variety, and platform-optimized scheduling.

```bash
# Generate a 2-week LinkedIn calendar
python3 ~/.claude/skills/phy-content-calendar/scripts/content_calendar.py \
  --pillars "dev tools" "AI" "startup growth" --platform linkedin

# 4-week Reddit calendar with content library integration
python3 ~/.claude/skills/phy-content-calendar/scripts/content_calendar.py \
  --pillars "security" "OpenClaw" "open source" --platform reddit \
  --weeks 4 --library ~/Desktop/content-ideas/

# Markdown table output (for Notion/docs)
python3 ~/.claude/skills/phy-content-calendar/scripts/content_calendar.py \
  --pillars "AI" "growth" "product" --platform twitter --format markdown
```

## Content Mix Strategy

Each week rotates through 7 content styles:

| Style | What | When to Use |
|-------|------|-------------|
| 💡 Insight | Non-obvious lesson or pattern | Best for LinkedIn/HN |
| 📖 Story | Personal experience with details | Universal |
| 📊 Data | Lead with number/stat/benchmark | LinkedIn, Twitter threads |
| 🔥 Contrarian | Challenge common belief | High engagement on all platforms |
| ❓ Question | Genuine discussion starter | Reddit, LinkedIn |
| 🔧 How-to | Step-by-step framework | LinkedIn, HN |
| 🚀 Build update | Progress on what you're shipping | Twitter, Reddit |

## Platform Schedules

| Platform | Best Days | Frequency | Best Time |
|----------|-----------|-----------|-----------|
| LinkedIn | Tue-Thu ⭐ | 3-4/week | 8-10 AM local |
| Reddit | Mon-Thu | 2-3/week + daily comments | 9 AM-12 PM ET |
| Twitter/X | Mon-Fri | 1-2/day | 9-12 AM, 5-7 PM |
| HackerNews | Mon-Wed | 1-2/week max | 9 AM-12 PM PT |

## Integration with Flywheel

```
content-calendar (plan what to post)
    → content-compound (find atoms for each post)
    → humanizer-audit (check AI signature)
    → platform-rules-engine (pre-flight)
    → post-forensics (analyze results)
    → feed back into next week's calendar
```

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
