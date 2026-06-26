---
name: i18n
description: Deep internationalization workflow—string extraction, ICU messages, formats, pseudolocale testing, and developer workflow. Use when preparing software for translation before full localization (l10n).
---

# Internationalization (i18n) (Deep Workflow)

i18n is **engineering readiness** for multiple languages: extractable strings, ICU messages, locale-aware formatting, and tests—before full **localization** (translator workflow).

## When to Offer This Workflow

**Trigger conditions:**

- Planning first non-English locales
- Hard-coded UI strings across the codebase
- Incorrect date/number formatting outside default locale

**Initial offer:**

Use **six stages**: (1) inventory & scope, (2) extraction pipeline, (3) ICU & placeholders, (4) formatting APIs, (5) layout & overflow, (6) QA hooks). Confirm framework (i18next, FormatJS, rails-i18n, etc.).

---

## Stage 1: Inventory & Scope

**Goal:** Which surfaces ship first; pilot locales; avoid translating everything on day one.

---

## Stage 2: Extraction Pipeline

**Goal:** Stable message keys; CI lint to block new user-visible literals where policy requires; namespaces per feature.

---

## Stage 3: ICU & Placeholders

**Goal:** Plural and select rules; named variables; no string concatenation across translated fragments.

---

## Stage 4: Formatting APIs

**Goal:** `Intl` (or platform equivalent) for dates, numbers, currency; explicit timezone policy (UTC vs user local).

---

## Stage 5: Layout & Overflow

**Goal:** Flexible layouts for longer translations; pseudolocale in CI to catch truncation (e.g., `xx-ACME`).

---

## Stage 6: QA Hooks

**Goal:** Easy locale switching in staging; optional screenshot/visual tests for critical screens.

---

## Final Review Checklist

- [ ] Scope and pilot locales defined
- [ ] Extraction and linting in place
- [ ] ICU for plurals; no unsafe concatenation
- [ ] Intl formatting for numbers/dates
- [ ] Pseudolocale or stress language in QA

## Tips for Effective Guidance

- Pair with **localization** skill for translator workflow and TMS integration.

## Handling Deviations

- Games or marketing-heavy UIs: context comments for translators are critical.
