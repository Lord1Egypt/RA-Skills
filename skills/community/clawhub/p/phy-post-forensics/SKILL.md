---
name: Post Forensics
description: "Why did this post work?" structural analyzer for social media. Takes a batch of your posts + engagement data, extracts 12 linguistic/structural features per post, groups by performance tier (top/middle/bottom), and tells you exactly which content patterns correlate with YOUR best vs worst posts. Generates a data-backed content blueprint. Not an analytics dashboard — a forensic structural analyzer that separates content quality from distribution luck. Research-backed (Buffer 52M+ posts study, LinkedIn 360Brew data, Stanford CS229 Reddit prediction, Upvote.net 1000-post study). Zero external dependencies.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - social-media
  - content
  - analytics
  - engagement
  - linkedin
  - reddit
  - twitter
  - content-strategy
---

# phy-post-forensics — "Why Did This Post Work?"

You post 50 times. 3 go viral. 47 die. Analytics tells you "what happened" (likes, views). This tool tells you **why** — which structural elements in your content drove engagement.

## The Problem

Every analytics tool shows lagging indicators: impressions, likes, comments. None of them tell you:
- Which **hook type** correlates with your best posts?
- Do your top posts have more **specific numbers**?
- Does **sentence rhythm** (mixing short + long) predict engagement?
- Are your worst posts missing **personal voice** (first-person pronouns)?

This tool extracts 12 structural features per post, groups by performance tier, and outputs: *"Your top posts share X, Y, Z. Your bottom posts all lack them."*

## Quick Start

```bash
# Analyze posts from JSON file
python3 ~/.claude/skills/phy-post-forensics/scripts/post_forensics.py --file my_posts.json

# Pipe from stdin
cat posts.json | python3 ~/.claude/skills/phy-post-forensics/scripts/post_forensics.py

# JSON output (for pipelines)
python3 ~/.claude/skills/phy-post-forensics/scripts/post_forensics.py --file posts.json --format json
```

## Input Format

```json
[
  {
    "text": "I built 101 OpenClaw skills in 30 days. Here's what happened...",
    "platform": "linkedin",
    "engagement_rate": 8.5,
    "impressions": 15000,
    "date": "2026-03-18"
  },
  {
    "text": "Another post...",
    "platform": "reddit",
    "engagement_rate": 1.2,
    "impressions": 500
  }
]
```

Required: `text`, `engagement_rate`. Optional: `platform`, `impressions`, `date`.

## The 12 Features Extracted

| # | Feature | What It Measures | Why It Matters |
|---|---------|-----------------|----------------|
| 1 | **Hook Type** | First line classification: number_lead, question, contrarian, story_open, challenge, statement | Hook determines "stop scrolling" moment |
| 2 | **Word Count** | Total words | Platform sweet spots vary (LinkedIn ~100-200, Twitter ~50-100) |
| 3 | **Sentence Count** | Number of sentences | More sentences ≠ better, but structure matters |
| 4 | **Sentence Length CV** | Coefficient of variation of sentence lengths | High CV = mixed rhythm (human). Low CV = monotone (AI) |
| 5 | **Question Count** | Questions in body text | Questions drive comments and dwell time |
| 6 | **Specific Numbers** | Count of data points (%, $, metrics, years) | Posts with data get 3-4x more reach (LinkedIn 2026 data) |
| 7 | **Personal Pronoun Density** | I/my/we per 100 words | Personal voice = trust and engagement |
| 8 | **List Formatting** | Bullets or numbered lists present | Scannability drives dwell time |
| 9 | **Paragraph Count** | Number of visual breaks | Short paragraphs = mobile-friendly |
| 10 | **CTA Type** | Call-to-action classification: question, action, share, comment, none | CTAs drive comments, comments drive distribution |
| 11 | **Sentiment** | Positive / neutral / negative keyword analysis | Positive content drives more shares |
| 12 | **Specificity Score** | Proper nouns + numbers + tool names per 100 words | Specific > generic (3-4x reach difference) |

## How Analysis Works

1. **Extract** 12 features from every post
2. **Tier** posts by engagement: top 25%, middle 50%, bottom 25%
3. **Compare** feature distributions across tiers
4. **Generate insights**: which features differentiate top from bottom
5. **Output blueprint**: actionable content template based on YOUR data

## Example Output

```
==================================================================
  phy-post-forensics — Content Forensics Report
==================================================================
  Posts analyzed : 8
  Top tier       : 2 posts (avg 11.05% engagement)
  Bottom tier    : 2 posts (avg 0.40% engagement)
  Spread         : Top posts get 27.6x more engagement
==================================================================

🔍  Key Insights (8 patterns found):

  1. 🔴 [HIGH] Specific Data Points
     Top posts: 5.5 numbers/post
     Bottom:    0.0 numbers/post
     → Include specific numbers — posts with data get 3-4x reach

  2. 🔴 [HIGH] Specificity Score
     Top posts: 18.9/100w
     Bottom:    2.6/100w
     → Name specific tools, companies, projects — not generic advice

  3. 🔴 [HIGH] Hook Type
     Top posts: Mostly 'contrarian' (50%)
     Bottom:    Mostly 'challenge' (50%)
     → Lead with contrarian hooks — they correlate with your best posts

📋 YOUR CONTENT BLUEPRINT:
  HOOK: Challenge conventional wisdom: 'Stop doing X. Here's why.'
  LENGTH: ~74 words, 14 sentences
  DATA: Include ~5 specific numbers/metrics
  VOICE: Personal — aim for 2+ first-person pronouns per 100 words
  CTA: End with a clear next step the reader can take
```

## Research Basis

| Source | Key Finding | How We Use It |
|--------|------------|---------------|
| Buffer 52M+ posts (2026) | Dwell time > likes; specificity = 3-4x reach | Specificity scoring + feature correlation |
| LinkedIn 360Brew data | Document posts = 596% more engagement than text; first 150 chars critical | Hook type classification |
| Reddit 1000-post study | Posting time = 730% diff; question titles underperform by 16% | Context notes in output (distribution vs content) |
| Stanford CS229 | Text features + sentiment predict Reddit post popularity | 12-feature extraction framework |
| LinkedIn 2026 benchmarks | 6.60% engagement for docs, 2-4% for text; 3-5 weekly optimal | Platform-aware recommendations |

## Collecting Your Post Data

### LinkedIn
Export from LinkedIn Analytics → Content tab → CSV export, then convert to JSON format.

### Reddit
```bash
# Use Reddit user history API
curl "https://www.reddit.com/user/USERNAME/submitted.json?limit=100" | python3 -c "
import json, sys
data = json.load(sys.stdin)
posts = [{'text': p['data']['title'] + ' ' + p['data'].get('selftext', ''),
          'platform': 'reddit',
          'engagement_rate': p['data']['upvote_ratio'] * 100,
          'impressions': p['data']['score']}
         for p in data['data']['children']]
json.dump(posts, sys.stdout, indent=2)
"
```

### Manual
Create a JSON file with your posts and approximate engagement rates.

## Technical Notes

- **Zero external dependencies** — pure Python 3.7+ stdlib
- **Minimum 3 posts** for meaningful analysis (8+ recommended)
- **Tier grouping**: top 25%, middle 50%, bottom 25% by engagement_rate
- **Insight generation**: only surfaces patterns with meaningful deltas (not noise)
- **JSON output**: `--format json` for pipeline integration

## Companion Skills

| Skill | Relationship |
|-------|-------------|
| `phy-content-humanizer-audit` | Checks AI signature before posting (this tool = analyzes after posting) |
| `phy-platform-rules-engine` | Checks platform-specific rules (this tool = analyzes content quality) |
| `phy-content-compound` | Builds content atom library (this tool = informs which atoms work best) |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
