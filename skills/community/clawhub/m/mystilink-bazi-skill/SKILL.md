---
name: mystilink-bazi
description: >
  BaZi (Four Pillars) charting and reading for Mystilink. Computes pillars, luck
  cycles, and annual pillars from birth data, then interprets with Wiki theory
  (ten gods, day master, combinations). Use when the user asks about BaZi, Four
  Pillars, 八字, day master, ten gods, dayun, or liunian.
license: MIT
compatibility: "python3; network optional for wiki.mystilink.com API"
metadata:
  mystilink:
    system: bazi
    default_locale: en
    wiki_api: /api/v1
  hermes:
    tags: [metaphysics, bazi]
    category: mystilink
  openclaw:
    requires: {}
---

# Mystilink BaZi (chart + read)

Combines **calculator** and **analyzer**: produce a chart from birth data, then interpret using Mystilink Wiki—do not invent classic quotations.

## When to use

- User wants BaZi / Four Pillars charting or reading
- Birth civil date (and preferably time, place, gender for luck cycles) is available or can be collected

## When not to use

- Question is only Zi Wei, tarot, Liu Yao, or western astrology → use the matching skill or `mystilink-router`
- User only wants calendar conversion with no BaZi framing

## Locale

Wiki calls: `locale` or `lang` query. **Omit → `en`**. Untranslated pages fall back to `zh-Hans` (`usedLocaleFallback`).

## Workflow

### 1. Collect profile (JSON)

```json
{
  "name": "string",
  "gender": "male|female",
  "birth_date": "YYYY-MM-DD",
  "birth_time": "HH:MM",
  "birth_place": "string",
  "birth_place_latitude": 0,
  "birth_place_longitude": 0,
  "birth_place_timezone": "Asia/Shanghai"
}
```

### 2. Chart (scripts)

From this skill directory:

```bash
python3 scripts/bazi_calculate.py --date YYYY-MM-DD --hour H [--minute M] [--timezone IANA] [--longitude E]
python3 scripts/bazi_dayun_calculate.py --date YYYY-MM-DD --gender male|female [--count 8]
python3 scripts/bazi_liunian_calculate.py --year YYYY [--day-stem 甲] [--pillars-json '...']
```

Stdout is JSON (product-aligned rules). On failure, non-zero exit.

### 3. Analyze

1. Identify day master (day stem) and ten-gods structure from chart JSON  
2. Pull theory via Wiki API (prefer English unless user locale known):

```text
GET /api/v1/search?q=day+master&system=bazi&locale=en
GET /api/v1/pages/bazi.concept.ri-zhu?locale=en
GET /api/v1/pages/bazi.concept.shishen?locale=en
```

3. Read `references/overview.md` and other files under `references/` only as needed  
4. Answer the user’s question; separate **chart facts** from **interpretation**  
5. Keep Wiki `provenance` / cite Mystilink Wiki when using knowledge pages  

### 4. Output shape

- Chart summary (four pillars, day master)  
- Luck / annual notes if computed  
- Interpretation tied to the question  
- Optional Wiki page ids used  

## Scripts note

Python CLIs are copied from Mystilink product BaZi calculators for standalone skill install. They are the operational reference for chart math in this skill.
