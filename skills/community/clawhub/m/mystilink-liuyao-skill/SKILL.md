---
name: mystilink-liuyao
description: >
  Liu Yao (six-line) casting and reading for Mystilink. Forms hexagrams from six
  casts, then interprets with Wiki method pages and Zhouyi chapters. Use when the
  user asks about Liu Yao, 六爻, moving lines, or hexagram casting.
license: MIT
compatibility: "node >= 18; network recommended for wiki + classics"
metadata:
  mystilink:
    system: liuyao
    default_locale: en
  hermes:
    tags: [metaphysics, liuyao]
    category: mystilink
---

# Mystilink Liu Yao (cast + read)

Combines **caster** and **interpreter**. One matter, one cast. Classic text lives in Wiki `classics/yijing`—fetch by chapter/passage; do not paste invented jingwen.

## When to use

- Six-line casting, moving lines, shi/ying, or hexagram reading for a concrete matter

## When not to use

- Pure BaZi / Zi Wei / natal / tarot without Liu Yao → other skills

## Locale

Wiki: `locale`/`lang`; **default `en`**. Classics often fall back to `zh-Hans`.

## Workflow

### 1. One clear matter

Refuse multi-topic shotgun casting.

### 2. Cast

```bash
node scripts/cast.mjs [--seed N]
# or pass throws: node scripts/cast.mjs --throws "3,2,3,3,2,3"
# values 0–3 coins heads count → line type per product rules in script help
```

Stdout JSON: six lines bottom→top, moving flags, original/resulting hexagram keys when available.

### 3. Read

```text
GET /api/v1/pages/liuyao.method.six-casts?locale=en
GET /api/v1/pages/liuyao.rule.ben-zhi-bian?locale=en
GET /api/v1/pages/liuyao.table.64-gua?locale=en
# Then classics chapter for the hexagram name, e.g.:
GET /api/v1/pages/shared.work.yijing.gua.01-qian?locale=zh-Hans
```

Use `references/overview.md`. Prefer Wiki **references** / `cites` links to local Zhouyi passages.

## Scripts note

Casting helper mirrors product coin→line semantics in simplified form for agents.
