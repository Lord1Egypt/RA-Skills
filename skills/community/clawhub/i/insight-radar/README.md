# Insight Radar (洞察雷达)

> **Dual-purpose news intelligence system**: AI self-evolution + strategic news briefings.

[![ClawHub](https://img.shields.io/badge/ClawHub-Published-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-2.0.0-green)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT--0-lightgrey)](LICENSE)

---

## What It Does

**For Your AI**: Scans news daily, records events to `news-log/`, and selectively extracts **concepts** and **thinking patterns** to the knowledge base when they meet high quality bars.

**For You**: Generates CORE-analyzed news briefings — not summaries, but **strategic intelligence** with actionable insights personalized to your context.

---

## Quick Start

### 1. Install Dependencies

```bash
clawhub install kedoupi/core-prism
clawhub install kedoupi/news-source-manager
```

### 2. Configure News Categories

Run `news-source-manager` to set up your interests, or let it auto-initialize with defaults on first run. Categories are stored in `~/.openclaw/workspace/memory/news-sources.json`.

### 3. Run It

```
"Run insight-radar for today's news."
```

**Automated daily briefing**: Add to your `HEARTBEAT-news.md` or set up a cron/scheduled trigger.

---

## How It Works

```
1. Load Config (news-source-manager)
   ↓
2. Search News (broad scan + smart follow-up)
   ├── English: "{category} news {month} {year}"
   ├── Chinese: "{类别} 新闻 {year}"
   └── AI evaluates coverage gaps → 0-2 targeted follow-ups per category
   ↓
3. CORE Analysis (via core-prism)
   ├── [C] Core Logic    [O] Opportunity
   └── [R] Risk          [E] Execution (personalized via USER.md)
   ↓
4. Generate Briefing (4 sections)
   ├── Core News (3-5 items with CORE analysis)
   ├── Strategic Briefing (cross-news patterns + So What?)
   ├── Cognitive Digest (news-log + candidate concepts/patterns)
   └── Blind Spot Questions (3-5 challenges)
   ↓
5. Write to Knowledge Base (3-tier architecture)
   ├── Layer 1: news-log/YYYY-MM-DD.md  (every run)
   ├── Layer 2: concepts.md             (weekly, high bar)
   └── Layer 3: thinking-patterns.md    (monthly, highest bar)
   ↓
6. (Optional) Write to Feishu Bitable
   ↓
7. Deliver Briefing (personalized via USER.md)
```

### Search Strategy

**Broad scan + smart follow-up** (not fixed search templates):

- Step 2a: 1 English + 1 Chinese search per category (broad coverage)
- Step 2b: AI checks results against category keywords, generates 0-2 targeted follow-up searches for uncovered sub-domains
- Total: 6-12 WebSearch calls for 3 categories

### Knowledge Base: 3-Tier Architecture

| Layer | File | Entry Bar | Frequency |
|-------|------|-----------|-----------|
| News Log | `news-log/YYYY-MM-DD.md` | Every analyzed news item | Daily |
| Concepts | `concepts.md` | Truly novel cognitive frameworks (not event records) | Weekly 1-3 |
| Thinking Patterns | `thinking-patterns.md` | Same pattern observed 3+ times across different news | Monthly 1-2 |

---

## Sample Output

See [references/example-output.md](references/example-output.md) for a complete example.

---

## Configuration

| Priority | Source | Purpose |
|----------|--------|---------|
| 1 | `memory/news-sources.json` | News categories (managed by news-source-manager) |
| 2 | `HEARTBEAT-news.md` | Feishu/external database config |
| 3 | `USER.md` | Personalize [E] Execution dimension |
| 4 | Defaults | AI/Tech category, no database, generic second-person |

---

## File Structure

```
insight-radar/
├── SKILL.md                        # Main skill definition
├── README.md                       # This file
└── references/
    ├── example-output.md           # Sample briefing format
    ├── category-config.md          # Category configuration guide
    └── category-recommendations.md # Recommended categories and sources
```

---

## Troubleshooting

**"No news found"**: Check if WebSearch is available. The skill auto-expands time range as fallback.

**"CORE analysis is shallow"**: Ensure `core-prism` skill is installed. Claude Opus recommended.

**"Briefing too long for Feishu"**: Skill auto-splits into 2 messages.

---

## License

MIT-0 (No Attribution Required)

---

## Credits

Created by **Tangyuan** for daily intelligence workflows.

**Dependencies**: [core-prism](https://clawhub.ai/kedoupi/core-prism), [news-source-manager](https://clawhub.ai/kedoupi/news-source-manager)
