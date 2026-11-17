---
name: mystilink-ziwei
description: >
  Zi Wei Dou Shu charting and reading for Mystilink. Builds a twelve-palace chart
  with major stars and optional Si Hua, then interprets with Wiki theory. Use when
  the user asks about Zi Wei, 紫微, twelve palaces, or Si Hua.
license: MIT
compatibility: "python3; pip package zhdate; network optional for wiki API"
metadata:
  mystilink:
    system: ziwei
    default_locale: en
  hermes:
    tags: [metaphysics, ziwei]
    category: mystilink
---

# Mystilink Zi Wei (chart + read)

Combines **calculator** and **analyzer**.

## When to use

- Zi Wei Dou Shu chart or palace/star reading
- Birth datetime, timezone, and gender available (or collectable)

## When not to use

- BaZi-only, tarot, Liu Yao, or western natal without Zi Wei framing → other skills / router

## Locale

Wiki: `locale`/`lang`; **default `en`**; fallback `zh-Hans`.

## Workflow

### 1. Profile

Need: local datetime, IANA timezone, gender (`male`|`female`). Optional: longitude, Si Hua year, midnight-zi rule.

### 2. Chart

```bash
python3 scripts/ziwei_chart_calculate.py \
  --datetime "YYYY-MM-DD HH:MM" \
  --timezone Asia/Shanghai \
  --gender female \
  [--si-hua] [--year YYYY] [--longitude E] [--midnight-zi] \
  --output json
```

Depends on `zhdate` (`pip install zhdate`).

### 3. Analyze

```text
GET /api/v1/search?q=life+palace&system=ziwei&locale=en
GET /api/v1/pages/ziwei.concept.ming-gong?locale=en
GET /api/v1/pages/ziwei.concept.sihua?locale=en
```

Use `references/overview.md` as needed. Separate chart facts from reading. Cite Wiki provenance.

## Scripts note

Chart script is aligned with Mystilink product Zi Wei calculator.
