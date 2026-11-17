# In the Cards · 牌间

**Lenormand Interpreter**

> [简体中文](README.zh-CN.md) · [繁體中文](README.zh-TW.md)

An [Agent Skills](https://agentskills.io) compatible Lenormand interpreter. It reads the meaning between cards, saves each interpretation as structured data, and generates polished A4 PDFs, web pages, social cards, or long images. It accepts freeform spreads and prompts from [Stargazer’s Oracle](https://lenor.star-oracle.app/), without depending on a single platform.

```
Please help me install this skill: https://github.com/locoda/in-the-cards-lenormand-skill
```

## Design

Every product shares a unified visual language inspired by two sources:

- **[Kami](https://github.com/tw93/Kami)** — warm parchment background (#f5f4ed), ink-blue accent (#1B365D), Chiron Sung HK serif typography. Clean, literary, minimal.
- **Geometric Silence** — a custom 36-card Lenormand deck in architectural blueprint style. Muted sage green (#7A8B7A) linework on cream (#F5F0E8), with dusty rose (#C4A0A0) accents. Swiss International Style meets scientific specimen plates. No mystical ornament — pure geometric abstraction.

Together they create a reading experience that feels scholarly, warm, and quietly beautiful.

## Features

- **6 spread types**: 1-card Yes/No · 2-card pair · 3-card linear · 5-card linear · 9-card Box Spread (3×3) · A-or-B choice
- **Bilingual**: Auto-detects Chinese or English prompts; all output matches the prompt language
- **Combination-first reading**: Systematic combination methodology — adjacent card pair chains with modifier type system (Noun+Modifier model). Each card modifies its neighbor according to its modifier type; 8 negative modifiers automatically darken the tone. Neutral, honest, no empty reassurance.
- **4 product types from one reading**: A4 PDF (default) · self-contained web page · 1080×1440 social card carousel · full-page PNG long image
- **Persistent readings**: Saved as structured JSON + human-readable Markdown; regenerate into any product format anytime
- **Seed-based HTML**: Copy + fill HTML skeletons — no fragile from-scratch construction
- **Geometric Silence deck**: 36 original SVG cards in architectural blueprint style
- **Chiron font pair**: Chiron Sung HK (昭源宋體) serif + Chiron Hei HK (昭源黑體) sans, loaded from Google Fonts CDN with CN mirror fallback

## Preview

Product showcase: [牌间 / In the Cards](https://skills.1mether.me/in-the-cards/)

## Install

Tell your agent:

> Install the In the Cards Lenormand skill from GitHub: https://github.com/locoda/in-the-cards-lenormand-skill

Or clone manually into your agent's skills directory:

```bash
git clone https://github.com/locoda/in-the-cards-lenormand-skill.git ~/your-agent/skills/in-the-cards-lenormand/
```

Requires: Node.js + Puppeteer (auto-installs Chromium on first PDF/social card render).

Existing installs may keep the legacy `stargazer-interpreter` folder name; new installs use `in-the-cards-lenormand`.

## Usage

### First-time reading

Paste a Lenormand spread or compatible Stargazer prompt — the agent runs Phase 1 (parse) + Phase 2 (interpret + save), then generates an A4 PDF by default.

```
User: Interpret this spread

You are a traditional Lenormand reader. Read for me...
---
Question: How will my career change in the next 3 months?
Date: 2026-06-20
Spread: 3-card linear
1. Clover
2. Child
3. Snake
```

### Generate a different product

```
User: Generate social cards from the latest reading
User: Generate web page from reading #2
```

### Request multiple products

```
User: Interpret this spread, generate PDF and social cards
[Lenormand spread or Stargazer prompt...]
```

### Three-phase workflow

```
Lenormand Prompt
(Stargazer-compatible)
    │
    ▼
[Phase 1] Parse → structured card data
    │
    ▼
[Phase 2] Interpret → save reading (JSON + MD)
    │
    ▼
[Phase 3] Generate products from saved reading
           ├── A4 PDF (default)
           ├── Web Page
           ├── Social Card (1080×1440 carousel)
           └── Long Image (full-page PNG)
```

## Structure

```
├── SKILL.md                         # Main instructions
├── README.md                        # English docs
├── README.zh-CN.md                  # Simplified Chinese docs
├── README.zh-TW.md                  # Traditional Chinese docs
├── assets/
│   ├── seed-a4-pdf.html             # A4 PDF HTML skeleton
│   ├── seed-social-card.html        # 1080×1440 social card skeleton
│   └── seed-web-page.html           # Web page skeleton
├── cards/
│   └── card-01-rider.svg ...        # 36 Geometric Silence SVG cards
├── references/
│   ├── lenormand-cards.md           # 36-card database (MIT), modifier types, methodology
│   ├── spread-parsing.md            # Prompt parsing rules
│   ├── design-system.md             # Shared fonts, colors, card slugs
│   ├── reading-schema.md            # JSON schema for persisted readings
│   └── template-a4-pdf.md           # A4 PDF chapter & page balance rules
└── scripts/
    ├── generate-pdf.js              # HTML → A4 PDF (Puppeteer)
    ├── render-social-cards.js       # HTML → 1080×1440 PNGs (Puppeteer)
    ├── render-long-image.js         # HTML → full-page PNG (Puppeteer)
    ├── validate.js                  # Product validation (static + Puppeteer)
    └── manage-readings.js           # Reading index CLI
```

> **Website & previews** are maintained in the separate [`locoda/skill-showcase`](https://github.com/locoda/skill-showcase) repository: [牌间 / In the Cards](https://skills.1mether.me/in-the-cards/).

## License

MIT

## Credits & References

**Typography**
- [Chiron Sung HK (昭源宋體)](https://github.com/chiron-fonts/chiron-sung-hk) — variable serif, SIL OFL 1.1
- [Chiron Hei HK (昭源黑體)](https://github.com/chiron-fonts/chiron-hei-hk) — variable sans, SIL OFL 1.1

**Design**
- [Kami](https://github.com/tw93/Kami) — visual style inspiration, MIT
- Geometric Silence — original card deck design

**Data**
- [Stargazer’s Oracle](https://lenor.star-oracle.app/) — online Lenormand platform
- [lenormand-oracle](https://github.com/jintianbaihe/lenormand-oracle) — 36-card bilingual dataset, MIT
- Combination modifier system — original synthesis based on public-domain Lenormand tradition