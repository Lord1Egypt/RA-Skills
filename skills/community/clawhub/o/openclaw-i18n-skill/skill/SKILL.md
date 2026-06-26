---
name: openclaw-i18n
description: Internationalization and localization layer for OpenClaw. Auto-detects language, enforces correct diacritics, formats dates/currency per locale, and pipes output through a post-processing cleaner. Supports Romanian and German at launch.
homepage: https://github.com/bloommediacorporation-lab/openclaw-i18n-skill
metadata:
  {
    "openclaw":
      {
        "emoji": "🌍",
        "install":
          [
            {
              "id": "clawhub",
              "kind": "clawhub",
              "label": "Install via ClawHub",
              "source": "bloommediacorporation-lab/openclaw-i18n-skill",
            },
          ],
      },
    "pricing": "€5/month",
    "languages": ["ro", "de"],
    "trial": "7 days free",
  }
---

# openclaw-i18n — Internationalization Layer for OpenClaw

## What This Skill Does

OpenClaw is a powerful AI agent framework — but by default, models generate
output that often has wrong diacritics, mixed languages, or mechanically garbled
text when users communicate in non-English languages. This skill fixes that
with two layers:

**Layer 1 — SKILL.md:** Configures the agent to think and respond correctly
in the user's language. Language detection, diacritics enforcement, locale
formatting, cultural communication norms.

**Layer 2 — Post-Processor:** A Python script that mechanically cleans the
model's raw output before it reaches the user. This is the unique part — no
other ClawHub skill does this. It catches the specific mechanical errors that
models reliably produce on non-English text: missing diacritics, stray
Chinese/Russian characters, merged words, common typos.

---

## Language Detection

### How It Works
- Auto-detect user language from conversation context
- Signals: explicit language statements, user names, place references, writing
  style, diacritic usage
- Confidence scoring — if below 80%, ask the user to confirm

### Supported Languages
| Language | Code | Status | Diacritics | Launch |
|----------|------|--------|------------|--------|
| Romanian | ro   | Stable | ă â î ș ț | v1.0   |
| German   | de   | Stable | ü ö ä ß    | v1.0   |
| French   | fr   | Planned | à â ç é è ê ë î ï ô û ü | v1.1 |
| Spanish  | es   | Planned | á é í ó ú ñ ü ¿ ¡ | v1.1 |
| Italian  | it   | Planned | à è é ì ò ó ù | v1.2 |
| Portuguese | pt | Planned | à á â ã ç é ê í ó ô õ ú | v1.2 |

English (en) is always the fallback when detection fails.

### Configuration Commands
```
User:  "Set language to Romanian"  → sets active language to RO
User:  "Setează limba la română"  → same
User:  "Stelle Sprache auf Deutsch" → sets active language to DE
User:  "Reset language to auto-detect" → reverts to auto-detection
```

Configuration persists across sessions via OpenClaw memory tools.

---

## Output Rules

### Language Enforcement
- **Always respond in the detected or configured language**
- Never switch languages mid-response without explicit reason
- If a user writes in Romanian, respond in Romanian — never English
- If a user writes in German, respond in German — never English

### Character Rules
- **Never output Chinese, Russian, Arabic, or non-Latin characters** in
  non-intentional contexts. Stray characters that appear in Romanian or German
  output are model errors — the post-processor removes them.
- **Words are always separated by correct spaces** — never merge two words
  into one. Example: "sivei" should never appear as "știu" split wrongly.
- **Always use correct diacritics** for the active language

### Diacritics — Never Approximate
**Romanian:** ă â î ș ț — always correct, never write "s" instead of "ș" or
  "t" instead of "ț" in Romanian words.

**German:** ü ö ä ß — never substitute with "ue", "oe", "ae" unless user
  explicitly asks for old spelling.

### What NOT To Do
- No filler phrases: "Desigur!", "Absolut!", "With pleasure!"
- No language mixing: English sentence fragments in a Romanian response
- No transliteration of diacritics: never write "sch" for "ș" in Romanian
- No "obviously", "of course", "as you know" — condescending patterns

---

## Locale-Specific Formatting

### Romanian (RO)
| Element    | Format                          |
|------------|---------------------------------|
| Date       | 15 martie 2026                  |
| Currency   | 150 lei / 30 euro / 29,99 €   |
| Phone      | +40 734 270 188 / 0721 234 567 |
| Address    | Strada Victoriei nr. 10, București |

### German (DE)
| Element    | Format                          |
|------------|---------------------------------|
| Date       | 15. März 2026 / 15.03.2026     |
| Currency   | 29,99 € / 150 €                |
| Phone      | +49 30 12345678 / 0171 2345678 |
| Address    | Hauptstraße 10, 10115 Berlin   |

---

## Cultural Communication Norms

### German (DE) — Formal by Default
- Use **Sie** (capitalized) unless the user explicitly switches to **du**
- Formal address: "Sie" not "du", "Ihnen" not "dir"
- Titles: Herr, Frau, Dr. are relevant in professional contexts
- Email tone: structured, clear subject lines, bullet points appreciated
- When in doubt: over-formal beats casual

### Romanian (RO) — Warm but Professional
- First name basis is standard once rapport is established
- Direct communication — say what you mean
- Professional but not stiff — Romanians appreciate warmth
- Avoid: excessive formality, bureaucratic language, impersonal templates

---

## Post-Processor Integration

The `i18n_processor.py` script runs after the model generates output and
before it reaches the user. This is critical — it fixes mechanical errors
that slip through even when the model "knows" the correct form.

### What the Post-Processor Fixes (deterministic, high-confidence):
1. **Missing diacritics** in common words (RO: "vrau"→"vreau", DE: "Mueller"→"Müller")
2. **Stray non-Latin characters** — single Chinese/Russian chars inserted by M2.7
3. **Merged words** — obvious cases where two words lost their space
4. **Whitespace errors** — double spaces, trailing/leading spaces
5. **Common typos** — model-specific patterns that are consistent and fixable

### What the Post-Processor Does NOT Fix:
- Grammar errors requiring context understanding
- Wrong word choice (semantic errors)
- Stylistic improvements
- Sentence structure problems

### Integration Instructions
The agent should pipe output through the processor:

```python
from i18n_processor import process
cleaned = process(raw_output, language_code)
# send 'cleaned' to user
```

### Invoking from SKILL.md Context
When this skill is active, every model response should be treated as raw
output and passed through `process(response, detected_language)` before
delivery. The agent never sees this step — it's transparent to the user.

---

## Configuration Memory

Language preference is stored via OpenClaw memory tools:

- Key: `i18n_language` — the active language code (e.g., "ro", "de")
- Key: `i18n_mode` — "auto" or "manual"
- Key: `i18n_detection_confidence` — last confidence score (0.0–1.0)

When `i18n_mode` is "auto", the agent re-evaluates language on each session
start but respects manual overrides until reset.

---

## Quick Reference

| Command | Effect |
|---------|--------|
| "Set language to Romanian" | Lock to RO |
| "Setează limba la română" | Lock to RO |
| "Stelle Sprache auf Deutsch" | Lock to DE |
| "Reset language to auto-detect" | Back to auto |

| Symbol | Meaning |
|--------|---------|
| ă â î ș ț | Romanian diacritics |
| ü ö ä ß    | German diacritics |
| 🌐 | Language indicator |
| 🌍 | i18n skill active |

---

## Error Handling

If the post-processor encounters ambiguous text:
- **Do not change** if confidence < 95%
- Log the case for review
- Never risk a false positive that makes output worse

Rule: The cost of a missed diacritic is lower than the cost of a wrong one.
