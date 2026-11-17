---
name: mystilink-tarot
description: >
  Tarot draw and reading for Mystilink. Draws upright/reversed cards for a spread,
  then interprets with Wiki card pages. Use when the user asks about tarot, tarot
  spreads, major/minor arcana, or 塔罗.
license: MIT
compatibility: "node >= 18; network optional for wiki API"
metadata:
  mystilink:
    system: tarot
    default_locale: en
  hermes:
    tags: [metaphysics, tarot]
    category: mystilink
---

# Mystilink Tarot (draw + read)

Combines **drawer** and **interpreter**. Prefer a real random draw via script (or user-provided cards); do not invent draws silently.

## When to use

- Tarot question, spread, or card meanings
- User wants a draw or brings cards already drawn

## When not to use

- Birth-chart systems only → BaZi / Zi Wei / horoscope skills

## Locale

Wiki: `locale`/`lang`; **default `en`**.

## Workflow

### 1. Clarify question + spread

Default: three-card. Confirm before drawing if ambiguous.

### 2. Draw

```bash
node scripts/draw.mjs --spread three-card [--seed N]
# or stdin JSON: {"spread":"three-card","seed":42}
```

Stdout JSON: cards with `id`, `name`, `orientation` (`upright`|`reversed`), positions.

### 3. Read

For each card:

```text
GET /api/v1/search?q=The+Fool&system=tarot&locale=en
GET /api/v1/pages/<card.id>?locale=en
```

Use `references/overview.md` and `references/method-draw.md`. Tie each position to the question; cite Wiki.

## Ethics

Do not claim medical/legal certainty. One clear question per draw when possible.
