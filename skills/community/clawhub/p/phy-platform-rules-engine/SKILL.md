---
name: Platform Rules Engine
description: Social media pre-flight checker. Scans any draft post against 30+ platform-specific invisible rules and outputs PASS/WARN/FAIL per rule with exact fix suggestions. Like a linter for content. Covers Reddit (90/10 self-promo ratio, shadowban triggers, link-to-comment tracking), LinkedIn (360Brew AI detection, 60% external link penalty, engagement bait NLP filter, engagement pod detection), Twitter/X (150x author-reply multiplier, 30-min velocity window, link depression since March 2026, bookmark 10x signal), and HackerNews (Show HN format rules, tutorial downrank, clickbait title editing by dang). Research-backed with specific algorithm data. Zero external dependencies.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - social-media
  - content
  - reddit
  - linkedin
  - twitter
  - hackernews
  - pre-publish
  - content-quality
---

# phy-platform-rules-engine — Social Media Pre-Flight Checker

Each social platform has invisible rules. Break them and you get shadowbanned, de-ranked, or ignored — without knowing why. This tool scans your draft post against 30+ platform-specific rules before you publish.

**Like a linter, but for social media posts.**

## Quick Start

```bash
# Check a Reddit post
echo "Your post text" | python3 ~/.claude/skills/phy-platform-rules-engine/scripts/platform_rules.py --platform reddit

# Check a LinkedIn post from file
python3 ~/.claude/skills/phy-platform-rules-engine/scripts/platform_rules.py --file draft.txt --platform linkedin

# Check a Twitter/X thread
python3 ~/.claude/skills/phy-platform-rules-engine/scripts/platform_rules.py --text "My tweet..." --platform twitter

# Check a HackerNews submission
python3 ~/.claude/skills/phy-platform-rules-engine/scripts/platform_rules.py --text "Show HN: ..." --platform hackernews

# JSON output
python3 ~/.claude/skills/phy-platform-rules-engine/scripts/platform_rules.py --file draft.txt --platform linkedin --format json
```

## Rules by Platform

### Reddit (7 rules)

| ID | Rule | What It Catches | Severity |
|----|------|----------------|----------|
| R001 | Self-promo in opening | Product mention in first paragraph → instant downvotes | HIGH |
| R002 | Self-promotion ratio | >10% promotional content violates 90/10 rule | HIGH |
| R003 | External link in body | Reddit tracks link-to-comment ratio; >10% → spam flag | MEDIUM |
| R004 | Post length | <50 words = low effort; >500 = TL;DR needed | LOW |
| R005 | No discussion prompt | No question = no comments = no algorithm boost | MEDIUM |
| R006 | Clickbait language | Community actively downvotes hype/clickbait | MEDIUM |
| R007 | Cross-posting signal | "Also posted on LinkedIn" → mass-distribution flag | HIGH |

### LinkedIn (8 rules)

| ID | Rule | What It Catches | Severity |
|----|------|----------------|----------|
| L001 | External link penalty | Links in body → **60% less reach** (LinkedIn 2026) | HIGH |
| L002 | Engagement bait | "Comment YES", "Tag a friend" → NLP filter penalizes | HIGH |
| L003 | AI content signals | 37 AI-flagged words → 360Brew **30% less reach** | HIGH |
| L004 | Hashtag count | >5 hashtags looks spammy; 0 = no categorization | MEDIUM |
| L005 | Hook strength | First 150 chars determine "See more" clicks → dwell time | HIGH |
| L006 | Post length | <30 words = low dwell time | MEDIUM |
| L007 | Long paragraphs | >40 words/paragraph = poor mobile readability | MEDIUM |
| L008 | Engagement pod signals | Pod references → aggressive detection in 2026 | HIGH |

### Twitter/X (6 rules)

| ID | Rule | What It Catches | Severity |
|----|------|----------------|----------|
| X001 | External link depression | Links → **near-zero engagement** for non-Premium (since March 2026) | HIGH |
| X002 | Thread hook strength | Weak thread hook = rest of thread never distributed | HIGH |
| X003 | Character count | >280 chars = truncated (non-Premium) | HIGH |
| X004 | Link placement strategy | Tip: author reply with link = **150x multiplier** | HIGH |
| X005 | Bookmark potential | No save-worthy content = misses **10x bookmark boost** | MEDIUM |
| X006 | No engagement prompt | No question = no replies = misses **27x reply multiplier** | MEDIUM |

### HackerNews (7 rules)

| ID | Rule | What It Catches | Severity |
|----|------|----------------|----------|
| HN001 | Clickbait title | Moderator (dang) will edit your title | HIGH |
| HN002 | ALL CAPS | Excessive capitalization → title edit | MEDIUM |
| HN003 | Show HN missing URL | Show HN requires a URL | HIGH |
| HN004 | Show HN content type | Show HN is for runnable things, not blog posts | HIGH |
| HN005 | Tutorial content | Tutorials explicitly downranked by moderators | MEDIUM |
| HN006 | Self-promotion | Self-promo outside Show HN → flagged | HIGH |
| HN007 | Technical depth | Low technical depth → poor reception on HN | MEDIUM |

## Algorithm Data Behind the Rules

| Platform Signal | Source | Data |
|----------------|--------|------|
| LinkedIn external link penalty | LinkedIn 360Brew 2026 | ~60% less reach |
| LinkedIn AI content penalty | LinkedIn 360Brew 2026 | 30% less reach, 55% less engagement |
| Twitter/X reply multiplier | X algorithm source code | Reply = 27x, Author reply = 150x, Bookmark = 10x, Like = 1x |
| Twitter/X link penalty | X algorithm March 2026 | Non-Premium: near-zero engagement with links |
| Twitter/X half-life | X algorithm analysis | Tweet loses 50% visibility every 6 hours |
| Reddit timing impact | Upvote.net 1000-post study | 730% difference based on posting time alone |
| Reddit self-promo | Reddit sitewide rules | 90/10 ratio across total account history |
| HN tutorial downrank | HN moderator policy | Tutorials "gratify intellectual curiosity less" |

## Example Output

### Bad Reddit post (HIGH RISK)
```
  Score    : 20/100 🔴 HIGH RISK
  Rules    : 2 PASS, 3 WARN, 2 FAIL

  🔴 [R001] Self-promo in opening — FAIL
     → Move product mention to a reply comment. Lead with value first.
  🔴 [R007] Cross-posting signal — FAIL
     → Remove cross-posting references. Each platform should feel native.
```

### Bad LinkedIn post (HIGH RISK)
```
  Score    : 5/100 🔴 HIGH RISK
  Rules    : 3 PASS, 2 WARN, 3 FAIL

  🔴 [L001] External link penalty — FAIL (60% less reach)
  🔴 [L002] Engagement bait detection — FAIL (NLP filter)
  🔴 [L003] AI content signals — FAIL (8 AI words found)
```

### Clean LinkedIn post (CLEAR)
```
  Score    : 100/100 ✅ CLEAR
  Rules    : 8 PASS, 0 WARN, 0 FAIL
```

## Technical Notes

- **Zero external dependencies** — pure Python 3.7+ stdlib
- **Exit codes**: 0 (CLEAR), 1 (warnings only), 2 (has failures)
- **JSON output**: `--format json` for pipeline integration
- **37 AI-flagged words**: same database as phy-content-humanizer-audit
- **10 engagement bait patterns**: regex-based, matches LinkedIn's NLP filter targets

## Companion Skills

| Skill | Relationship |
|-------|-------------|
| `phy-content-humanizer-audit` | Deep 8-dimension AI signature analysis (this tool = quick rule check) |
| `phy-post-forensics` | Post-publish analysis (this tool = pre-publish prevention) |
| `phy-content-compound` | Content atom library (use rules engine before publishing atom combinations) |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
