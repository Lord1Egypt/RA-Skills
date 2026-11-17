---
name: mystilink-router
description: >
  Chooses which Mystilink metaphysics skill to use (BaZi, Zi Wei, tarot, Liu Yao,
  western horoscope). Use when the user has not named a system, asks which method
  fits, or mixes several traditions in one request.
license: MIT
compatibility: "network optional for wiki API"
metadata:
  mystilink:
    system: shared
    default_locale: en
  hermes:
    tags: [metaphysics, router]
    category: mystilink
---

# Mystilink theory router

Pick **one** primary skill; do not run five systems “just in case.”

## When to use

- User did not specify a system
- User asks “which method should I use?”
- Request mixes incompatible frames

## Routing heuristics

| Need | Skill |
|------|--------|
| Birth date/time → long-term structure, ten gods | `mystilink-bazi` |
| Birth → twelve palaces / Zi Wei stars | `mystilink-ziwei` |
| Birth place + time → planets/houses/aspects | `mystilink-horoscope` |
| One concrete question, symbolic cards | `mystilink-tarot` |
| One concrete question, hexagram / moving lines | `mystilink-liuyao` |

Wiki aid:

```text
GET /api/v1/pages/shared.concept.choosing-a-system?locale=en
```

(If missing in locale, fallback `zh-Hans` or search `choosing`.)

## After routing

Load the chosen skill’s `SKILL.md` and follow it. Mention briefly why that system fits.
