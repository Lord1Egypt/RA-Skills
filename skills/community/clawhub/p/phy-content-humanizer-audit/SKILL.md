---
name: Content Humanizer Audit
description: AI content signature detector for social media posts. Measures 8 linguistic dimensions that LinkedIn's 360Brew and other platforms use to detect AI-generated content — lexical diversity, sentence length variance, transition word density, hedging ratio, contraction usage, personal pronoun density, question frequency, and specific data density. Not a humanizer that rewrites your text — an auditor that tells you exactly which signals are triggering detection so you fix only what's wrong. Research-backed (DivEye arXiv:2509.18880, LinkedIn 360Brew algorithm analysis, stylometric detection studies). Per-platform thresholds for LinkedIn (strictest), Reddit, Twitter/X, HackerNews. Zero external dependencies.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - social-media
  - content
  - linkedin
  - ai-detection
  - writing
  - marketing
  - authenticity
  - brand-voice
---

# phy-content-humanizer-audit — AI Content Signature Detector

LinkedIn's 360Brew algorithm penalizes AI-detected content with **30% less reach and 55% less engagement**. This tool tells you exactly which linguistic signals are triggering detection — so you fix only what's wrong instead of rewriting everything.

**Not a humanizer. An auditor.**

## The Problem

You draft a LinkedIn post (maybe with AI help), publish it, and reach tanks. Why?

LinkedIn's 360Brew uses an LLM to evaluate:
- **Lexical diversity** — AI repeats vocabulary patterns
- **Sentence rhythm** — AI maintains unnaturally consistent sentence lengths
- **Transition words** — AI overuses "Furthermore", "Moreover", "Additionally"
- **Hedging language** — AI says "arguably" and "it seems" instead of stating opinions
- **Formality** — AI avoids contractions ("do not" instead of "don't")
- **Impersonality** — AI rarely uses first-person pronouns
- **No questions** — AI makes statements, doesn't ask
- **Vagueness** — AI uses abstract language with no specific data

This tool measures all 8 dimensions, scores each 0-10, and tells you your **AI Signature %** — the probability a platform algorithm will flag your content as AI-generated.

## Quick Start

```bash
# Audit a LinkedIn post draft
echo "Your post text here" | python3 ~/.claude/skills/phy-content-humanizer-audit/scripts/content_humanizer_audit.py --platform linkedin

# Audit from file
python3 ~/.claude/skills/phy-content-humanizer-audit/scripts/content_humanizer_audit.py --file draft.txt --platform reddit

# Inline text
python3 ~/.claude/skills/phy-content-humanizer-audit/scripts/content_humanizer_audit.py --text "My post..." --platform twitter

# JSON output (for pipelines)
python3 ~/.claude/skills/phy-content-humanizer-audit/scripts/content_humanizer_audit.py --file draft.txt --format json
```

## The 8 Dimensions

| # | Dimension | What It Measures | Human Signal | AI Signal |
|---|-----------|-----------------|-------------|-----------|
| 1 | **Lexical Diversity (TTR)** | Vocabulary variety (type-token ratio) | TTR 0.55-0.80 | TTR 0.35-0.55 |
| 2 | **Sentence Length Variance** | Mix of short/long sentences (coefficient of variation) | CV > 0.4 | CV < 0.3 |
| 3 | **Transition Word Density** | "Furthermore", "Moreover" per 100 words | < 1.5/100w | > 3.0/100w |
| 4 | **Hedging Ratio** | "arguably", "it seems" per 100 words | < 1.0/100w | > 2.0/100w |
| 5 | **Contraction Usage** | "don't", "I've", "it's" per 100 words | > 1.5/100w | < 0.5/100w |
| 6 | **Personal Pronoun Density** | "I", "my", "we" per 100 words | > 3.0/100w | < 1.5/100w |
| 7 | **Question Frequency** | % of sentences that are questions | 10-25% | 0-5% |
| 8 | **Specific Data Density** | Numbers, dates, names per 100 words | > 2.0/100w | < 1.0/100w |

Each dimension scores 0-10 (10 = very human). Total /80, mapped to an **AI Signature %**.

## Platform Thresholds

| Platform | WARN above | FAIL above | Why |
|----------|-----------|-----------|-----|
| **LinkedIn** | 45% | 65% | 360Brew LLM actively detects AI. Strictest. |
| **HackerNews** | 50% | 70% | Technical audience spots AI quickly. |
| **Reddit** | 55% | 75% | Community policing + mod tools. Moderate. |
| **Twitter/X** | 60% | 80% | Short form = less surface for detection. |

## AI-Flagged Word List

The tool flags 37 words that are strong AI signals on social media:

> leverage, robust, crucial, delve, tapestry, holistic, synergy, paradigm, ecosystem, landscape, streamline, cutting-edge, game-changer, innovative, revolutionary, transformative, comprehensive, meticulous, nuanced, multifaceted, pivotal, seamless, foster, utilize, facilitate, endeavor, underscore, realm, navigate, embark, spearhead, harness, unveil, bolster, cornerstone, unparalleled, groundbreaking

Each found word adds 3% to your AI signature score.

## Example Output

### Human-written post (PASS)

```
==================================================================
  phy-content-humanizer-audit — AI Signature Report
==================================================================
  Platform : Linkedin
  Words    : 183
  AI Sig   : 10.5% ✅ PASS
  Human    : 74.0/80.0
  Threshold: WARN >45%, FAIL >65%
==================================================================

📊  Dimension Scores (0-10, higher = more human)

  Lexical Diversity (TTR)      ██████████ 10.0/10
  Sentence Length Variance     ██████████ 10.0/10
  Transition Word Density      ██████████ 10.0/10
  Hedging Ratio                ██████████ 10.0/10
  Contraction Usage            ██████████ 10.0/10
  Personal Pronoun Density     █████░░░░░  5.5/10
  Question Frequency           ████████░░  8.5/10
  Specific Data Density        ██████████ 10.0/10
```

### AI-generated post (FAIL)

```
==================================================================
  Platform : Linkedin
  AI Sig   : 100% 🔴 FAIL
  Human    : 22.0/80.0
==================================================================

  Transition Word Density      ██░░░░░░░░  2.6/10   (3.4/100w)
  Hedging Ratio                █░░░░░░░░░  1.1/10   (3.4/100w)
  Contraction Usage            ░░░░░░░░░░  0.0/10   (0.0/100w)
  Question Frequency           █░░░░░░░░░  1.0/10   (0%)
  Specific Data Density        ░░░░░░░░░░  0.0/10   (0.0/100w)

  🚫 14 AI-flagged words: comprehensive, crucial, cutting-edge,
     ecosystem, facilitate, harness, holistic, innovative, landscape,
     navigate, paradigm, revolutionary, robust, transformative
```

## How to Use the Fixes

The tool outputs your **top 3 fixes** ranked by impact:

```
💡  Top 3 Fixes to Lower AI Signature:

  1. Add contractions: change 'do not' → 'don't', 'I have' → 'I've'
  2. Add specific data: include a number, date, or tool name
  3. Remove AI words: comprehensive, crucial — replace with plain terms
```

Fix just those 3 things and re-run. Usually drops AI signature by 20-30%.

## CI / Pre-publish Gate

```bash
# Fail if AI signature > 65% (LinkedIn threshold)
echo "$POST_TEXT" | python3 content_humanizer_audit.py --platform linkedin
# Exit code: 0=PASS, 1=WARN, 2=FAIL
```

## Research Basis

| Source | Key Finding | How We Use It |
|--------|------------|---------------|
| DivEye (arXiv:2509.18880) | Human text has richer variability in lexical/structural unpredictability | TTR + sentence variance scoring |
| LinkedIn 360Brew (2026) | LLM-based feed ranking detects AI via lexical patterns, profile alignment | Platform-specific thresholds |
| Stylometric detection studies | AI shows lower sentence length variance, higher transition density | 8-dimension framework |
| LinkedIn algorithm data | 30% reach drop, 55% engagement drop for AI content | WARN/FAIL calibration |
| Consumer research | 52% reduce engagement with suspected AI content | Motivation for the tool |

## Technical Notes

- **Zero external dependencies** — pure Python 3.7+ stdlib
- **Sentence splitting** — regex-based, handles abbreviations
- **Windowed TTR** — sliding window of 100 tokens to normalize for text length
- **Exit codes** — 0 (PASS), 1 (WARN), 2 (FAIL) for CI integration
- **JSON output** — `--format json` for pipeline integration

## Companion Skills

| Skill | Relationship |
|-------|-------------|
| `phy-brand-voice-guard` | Brand-specific content rules (this tool = platform-universal AI detection) |
| `phy-post-forensics` | Analyzes why posts worked/failed (this tool = pre-publish prevention) |
| `phy-platform-rules-engine` | Platform-specific invisible rules (this tool = AI signature specifically) |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
