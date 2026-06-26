---
name: parsha-summary
slug: jewish-parsha-summary
version: 1.0.0
description: |
  Generate a weekly Torah portion (parsha) summary from Sefaria.
  Provides English summary with optional Hebrew text, verse count,
  and sample verses. Lightweight alternative to torah-scholar.
  Use when: user wants a quick parsha overview, weekly summary,
  or needs parsha content for a dvar Torah outline.
triggers:
  - parsha summary
  - weekly parsha
  - torah portion
  - parsha overview
  - this week's parsha
  - parsha summary
metadata:
  openclaw:
    emoji: 📜
---

# Parsha Summary

Quick weekly Torah portion summaries from Sefaria. Lightweight — no heavy commentary, just the text and a brief overview.

## Quick Start

```bash
# This week's parsha
parsha-summary

# Specific parsha
parsha-summary "Bereshit"

# Short summary (50 words)
parsha-summary --words 50

# With Hebrew text
parsha-summary --hebrew

# JSON output
parsha-summary --json
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `parsha-summary` | This week's parsha | `parsha-summary` |
| `parsha-summary <name>` | Specific parsha | `parsha-summary "Noach"` |
| `parsha-summary --words N` | Limit to N words | `parsha-summary --words 100` |
| `parsha-summary --hebrew` | Include Hebrew | `parsha-summary -H` |
| `parsha-summary --json` | JSON output | `parsha-summary -j` |

## Output Format

```
📖 Vayera
   Genesis.18.1-22.24
   106 verses

Abraham welcomes three angels who announce that Sarah will bear a son. Abraham pleads for Sodom. Lot is saved but his wife becomes a pillar of salt. Sarah gives birth to Isaac. Abraham is tested with the binding of Isaac (Akedah)...

📖 Sample verses:
   1. And the Lord appeared to him in the plains of Mamre: and he sat in the tent door in the heat of the day...
   2. And he lifted up his eyes and looked, and, lo, three men stood by him: and when he saw them, he ran to meet them from the tent door...
```

## Parsha Names

Accepted names (case-insensitive):
- Bereshit, Noach, Lech-Lecha, Vayera, Chayei Sara, Toldot, Vayetzei, Vayishlach, Vayeshev, Miketz, Vayigash, Vayechi
- Shemot, Vaera, Bo, Beshalach, Yitro, Mishpatim, Terumah, Tetzaveh, Ki Tisa, Vayakhel, Pekudei
- Vayikra, Tzav, Shemini, Tazria, Metzora, Achrei Mot, Kedoshim, Emor, Behar, Bechukotai
- Bamidbar, Naso, Beha'alotcha, Shelach, Korach, Chukat, Balak, Pinchas, Matot, Masei
- Devarim, Vaetchanan, Eikev, Re'eh, Shoftim, Ki Teitzei, Ki Tavo, Nitzavim, Vayelech, Ha'Azinu, Vezot Haberakhah

## Features

- Auto-detects this week's parsha via Hebcal
- Fetches text from Sefaria API
- Configurable summary length
- Optional Hebrew text inclusion
- JSON output for programmatic use

## Data Sources

- **Hebcal API** — Calendar data, parsha detection
- **Sefaria API** — Torah text (Hebrew + English)

## Limitations

- Requires internet for text fetch
- Summary is algorithmic (first N verses), not AI-generated
- Hebrew text truncated in non-JSON mode
