---
name: numerology-reading
description: |
  Western-style numerology (Pythagorean-style)—life path and related numbers from birth date and name, with symbolic themes. Use when the user asks for life path number, angel numbers, name number, or “what does my birthday mean” in a numerology context. Entertainment and self-reflection only; not science, not medical/legal/financial advice.
metadata:
  openclaw:
    emoji: "🔢"
---

# Numerology Reading (Western)

## Overview

This skill supports **Western numerology** as commonly practiced online: reduce dates and names to **single digits (1–9)** and **master numbers (11, 22, 33)** where the tradition allows. Use it for **themes and prompts**, not destiny.

**Trigger keywords:** numerology, life path number, angel number, expression number, soul urge, birthday number, 生命灵数, 数字命理

---

## Core ideas (typical Pythagorean-style)

- **Life Path** — from **full birth date** (reduce to 1–9 or 11/22/33).  
- **Expression / Destiny** — from **full name** letters mapped to digits (A=1 … I=9 pattern varies slightly by system—**state which reduction you use**).  
- **Birthday number** — day of month reduced.  
- **Angel numbers** (e.g. 111, 222) — **popular culture** framing; avoid superstitious fear.

Always **show the math** when you compute (e.g. “1+9+9+0 = 19 → 1+9 = 10 → 1+0 = **1**”) so users can verify.

---

## When to use

- User wants a **number profile** from birthday or name.  
- User keeps seeing **repeating digits** and wants a **gentle symbolic** read—not a claim about the universe sending commands.

**Do not** use numbers to rank people’s worth, compatibility cruelty, or “lucky/unlucky” people.

---

## Assistant behavior

1. **Transparency** — Numerology is **not** validated by science; label as **reflective**.  
2. **Consistency** — Pick **one** letter-to-number table (classic Latin A–Z mapping) and stick to it; note Y as vowel/consonant only if you take a stance.  
3. **Master numbers** — If reducing, many systems preserve 11/22/33 before final reduction; **say which rule** you follow.  
4. **Inclusive** — Names with diacritics: normalize or state limitation.  
5. **Language** — Match the user’s language.

---

## Suggested output structure

```markdown
# Numerology snapshot

**Method**: [e.g. Pythagorean; master numbers preserved at step X]

## Inputs
- Birth date: …
- Name (if used): …

## Calculations (show steps)
- Life Path: … → **N**
- (Optional) Expression: … → **N**

## Themes (non-literal)
- [2–4 bullets tied to N as *cultural* meanings, not facts]

## Disclaimer
For entertainment and reflection only—not professional, medical, legal, or financial advice.
```

---

## References (general)

- Look for **educational** descriptions of “Pythagorean numerology” or “life path number”; treat pop sites as **varied**, not one standard.

