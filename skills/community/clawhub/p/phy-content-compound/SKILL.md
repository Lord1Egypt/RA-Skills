---
name: Content Compound
description: Content atom library builder for social media creators. Scans a directory of your past content (markdown, text files) and extracts reusable "content atoms" — claims, data points, anecdotes, frameworks, contrarian takes, and questions. Tags each with topic keywords and source attribution. When given a new topic, retrieves the most relevant atoms from your personal library and generates a post outline. Like Zettelkasten but automated — every post you write makes the next one easier. Solves the 77% creator burnout problem by eliminating "blank page" starts. Research-backed (Zettelkasten serendipity effect, Justin Welsh 730-day content library, content atomization hub-and-spoke model). Zero external dependencies.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - social-media
  - content
  - writing
  - productivity
  - knowledge-base
  - zettelkasten
  - content-creation
  - anti-burnout
---

# phy-content-compound — Content Atom Library Builder

77% of social media creators report burnout. The #1 cause: starting from a blank page every time. You've already written the best version of your ideas — in past posts, comments, threads. The problem is you can't find and recombine them.

This tool scans your past content, extracts reusable "content atoms," and retrieves the most relevant ones when you need to write about a new topic. **Every post you write makes the next one easier.**

## Quick Start

```bash
# Build atom library from your content directory
python3 ~/.claude/skills/phy-content-compound/scripts/content_compound.py ~/Desktop/content-ideas/

# Build library + query for a topic
python3 ~/.claude/skills/phy-content-compound/scripts/content_compound.py ~/posts/ --topic "developer tools"

# Query specific atom type
python3 ~/.claude/skills/phy-content-compound/scripts/content_compound.py ~/posts/ --topic "AI" --type data_point

# Get top 10 results
python3 ~/.claude/skills/phy-content-compound/scripts/content_compound.py ~/posts/ --topic "security" --top 10

# JSON output
python3 ~/.claude/skills/phy-content-compound/scripts/content_compound.py ~/posts/ --topic "growth" --format json
```

## The 6 Atom Types

| Type | Icon | What It Captures | Detection Pattern |
|------|------|-----------------|-------------------|
| **data_point** | 📊 | Specific numbers, percentages, metrics | Sentences with digits + units (%, $, K, M, x) |
| **claim** | 💡 | Strong assertions, thesis statements | "The key insight is...", "Turns out...", "The reality is..." |
| **anecdote** | 📖 | Personal stories and experiences | "I built...", "We shipped...", "Last month I..." |
| **framework** | 🔧 | Structured lists, step-by-step models | 3+ consecutive bullet points or numbered items |
| **contrarian** | 🔥 | Challenges to conventional wisdom | "Stop...", "Don't...", "Everyone is wrong about..." |
| **question** | ❓ | Thought-provoking discussion drivers | Sentences ending with "?" (>25 chars) |

## How It Works

```
Your content files (.md, .txt)
    ↓
[Extract atoms] — regex-based sentence classification
    ↓
[Tag keywords] — context-window keyword extraction
    ↓
[Build library] — 6 atom types, source attribution, line numbers
    ↓
[Query topic] — keyword overlap scoring + text presence matching
    ↓
[Generate outline] — Hook (contrarian/data) → Body (claims+data+proof) → CTA (question)
```

## Example Output

```
==================================================================
  phy-content-compound — Content Atom Library
==================================================================
  Files scanned  : 14
  Total atoms    : 591
==================================================================

📊  Atoms by Type:

  📊 data_point      485 atoms
  🔧 framework        90 atoms
  ❓ question           7 atoms
  📖 anecdote           4 atoms
  💡 claim              3 atoms
  🔥 contrarian         2 atoms

🔍  Top atoms for: "developer tools security"

  1. 📊 [data_point] (relevance: 5.0)
     "55 automated audit checks, maps to OWASP Agentic Top 10"
     — Source: skills-marketplace-guide.md:112

  2. 📖 [anecdote] (relevance: 3.5)
     "I spent a week mapping every platform, scanning for security"
     — Source: skills-marketplace-guide.md:7

📝  Suggested Outline for: "developer tools security"

  1. HOOK: Lead with data (55 automated audit checks...)
  2. BODY: Core argument + supporting data + personal proof
  3. CTA: Close with a genuine question
```

## The Compounding Effect

| Library Size | Serendipity | Writing Speed |
|-------------|-------------|---------------|
| 0-50 atoms | Low — still building | Same as blank page |
| 50-100 atoms | **Emerging** — old atoms surface relevant connections | 15-20% faster |
| 100-500 atoms | **Strong** — most new topics have 3-5 relevant atoms | 30-50% faster |
| 500+ atoms | **Compound** — new posts are mostly recombination | 50-70% faster |

Based on Zettelkasten research: the "serendipity effect" kicks in at 50-100 well-connected notes.

## Content Pipeline Integration

This tool is the **final piece of the social media flywheel**:

```
COMPOUND (find your best past atoms)
    → Write draft
    → HUMANIZER (remove AI signals)
    → RULES ENGINE (pre-flight platform check)
    → Post
    → FORENSICS (analyze what worked)
    → feedback into COMPOUND (grows your atom library)
```

Each cycle makes the next one better. The library grows, retrieval improves, writing gets faster.

## Research Basis

| Source | Key Insight | How We Use It |
|--------|------------|---------------|
| Zettelkasten method | Atomic notes + serendipity at 50-100 notes | 6 atom types, keyword linking |
| Justin Welsh 730-day library | 5 styles × 5 topics = 75+ ideas; performance grading | Engagement hint tagging |
| Content atomization (MarTech) | Hub-and-spoke: 1 idea → dozens of derivatives | Atom extraction + recombination |
| NLP text segmentation | Regex-based sentence classification + entity extraction | Atom type detection patterns |

## Technical Notes

- **Zero external dependencies** — pure Python 3.7+ stdlib
- **Supported file types**: `.md`, `.txt` (recursive scan)
- **Skips**: `.git/`, `node_modules/`, `__pycache__/`, `venv/`
- **Keyword extraction**: Context-window TF approach (no external NLP library)
- **Scoring**: Keyword overlap × 2 + text presence × 1.5 + engagement bonus
- **Engagement hints**: Inferred from filename patterns (e.g., "viral", "top", "hit")

## Companion Skills

| Skill | Relationship |
|-------|-------------|
| `phy-content-humanizer-audit` | Check AI signature before publishing atom-based posts |
| `phy-post-forensics` | Analyze which atom combinations drove engagement → feed back into library |
| `phy-platform-rules-engine` | Pre-flight check before posting on any platform |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
