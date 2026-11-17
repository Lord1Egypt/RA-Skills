---
name: mystilink-horoscope
description: >
  Western natal astrology charting and reading for Mystilink. Computes planets,
  houses, and aspects from birth time and place, then interprets with Wiki terms.
  Use when the user asks about natal chart, horoscope, houses, aspects, or 占星.
license: MIT
compatibility: "python3; pip package pyswisseph; network optional for wiki API"
metadata:
  mystilink:
    system: horoscope
    default_locale: en
  hermes:
    tags: [metaphysics, astrology]
    category: mystilink
---

# Mystilink Horoscope (chart + read)

Combines **calculator** and **analyzer** for western natal charts.

## When to use

- Natal chart calculation or interpretation
- Birth datetime, timezone, latitude, longitude known or collectable

## When not to use

- Chinese systems only (BaZi / Zi Wei / Liu Yao) or tarot-only → other skills

## Locale

Wiki: `locale`/`lang`; **default `en`**; fallback `zh-Hans`.

## Workflow

### 1. Chart

```bash
python3 scripts/astro_chart_calculate.py \
  --datetime "YYYY-MM-DD HH:MM" \
  --timezone IANA \
  --lat LAT --lon LON \
  [--zodiac tropical|sidereal] [--true-solar-time] \
  --output json
```

Depends on `pyswisseph`.

### 2. Analyze

```text
GET /api/v1/search?q=ascendant&system=horoscope&locale=en
GET /api/v1/pages/horoscope.concept.natal-chart?locale=en
GET /api/v1/pages/horoscope.concept.aspects?locale=en
```

Read `references/overview.md` as needed. Keep chart data vs interpretation distinct; cite Wiki.

## Scripts note

Aligned with Mystilink product astro calculator.
