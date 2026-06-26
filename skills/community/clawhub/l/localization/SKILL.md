---
name: localization
description: Deep localization workflow—locale strategy, string extraction, ICU and placeholders, formatting, RTL and layout, translation QA, and continuous delivery with feature flags. Use when shipping multiple languages or fixing i18n bugs at scale.
---

# Localization (l10n) (Deep Workflow)

Localization is **engineering + content + QA**—not “send strings to translators.” Plan for **concatenation**, **plural/gender**, **context**, and **layout** early to avoid expensive rework.

## When to Offer This Workflow

**Trigger conditions:**

- New markets/languages; **translation** **backlog**
- Broken plurals, **overflow**, **RTL** layout bugs
- **Date/currency** errors; **sort** order issues

**Initial offer:**

Use **six stages**: (1) strategy & scope, (2) extraction & keys, (3) ICU & placeholders, (4) formatting & locale data, (5) layout & RTL, (6) QA & launch process. Confirm **TMS** (Phrase, Lokalise, etc.) and **release** cadence.

---

## Stage 1: Strategy & Scope

**Goal:** **Which** locales, **what** ships together, **quality** bar.

### Decisions

- **Locale** list vs **language** only; **regional** variants (pt-BR vs pt-PT)
- **Tier**: full UI vs partial; **legal** **must-have** strings
- **Fallback** chain: `es-MX` → `es` → `en`

**Exit condition:** **Scope** document and **priority** locales for launch.

---

## Stage 2: Extraction & Keys

**Goal:** **Stable** keys, **developer** context for translators.

### Practices

- **No** string concatenation across translations—**one** message id per sentence
- **Descriptions** for translators: **where** shown, **max length** hint if UI constrained
- **Namespaces** per feature; **avoid** reusing **ambiguous** English in multiple keys

### Workflow

- **Freeze** strings for release branches; **diff** notifications for **late** changes

**Exit condition:** **Naming** convention for keys; **PR** checklist for new strings.

---

## Stage 3: ICU & Placeholders

**Goal:** **Grammatically** correct in **all** target languages.

### Patterns

- **Plural**, **select**, **ordinal** rules via ICU MessageFormat (or platform equivalent)
- **Variables** named (`{userName}`), **reordered** per locale rules—**never** **positional** `%s` soup for user-visible text

### Pitfalls

- **Nested** plurals; **gender** agreement languages—**linguist** review when needed

**Exit condition:** **Lint** or **test** that **parses** ICU per message.

---

## Stage 4: Formatting & Locale Data

**Goal:** **Numbers, dates, currency, units** follow **locale**—not **manual** strings.

### Practices

- **Intl** APIs (JS), **babel** / **ICU** (other stacks); **timezone** policy explicit (UTC vs user local)
- **First day of week**, **calendars** where relevant

**Exit condition:** **Golden** tests for **format** snapshots per locale sample.

---

## Stage 5: Layout & RTL

**Goal:** UI **works** in **long** translations and **RTL**.

### Practices

- **Flexible** layouts; **truncate** with **tooltip** only when necessary—**German** **expands**
- **RTL**: **mirror** icons/direction; **bidirectional** text in **mixed** content
- **Vertical** space for **CJK** line breaks when needed

**Exit condition:** **Visual** QA checklist per **template**; **screenshots** in **worst-case** language often **de** or **fi** for length stress.

---

## Stage 6: QA & Launch

**Goal:** **Linguistic** + **functional** QA before **traffic**.

### Process

- **Pseudo-localization** in CI: **expand** strings, **accent**—catches truncation early
- **In-context** review (on-device) when possible
- **Smoke** tests per locale on **critical** paths post-deploy

---

## Final Review Checklist

- [ ] Locale scope and fallbacks defined
- [ ] Keys and translator context disciplined
- [ ] ICU for plurals/gender; no unsafe concatenation
- [ ] Intl formatting for numbers/dates/currency
- [ ] RTL and long-string layout verified
- [ ] QA process for each release train

## Tips for Effective Guidance

- **Concatenation** is the **#1** source of **untranslatable** bugs.
- **English** **plural** ≠ **other** languages—always **use** ICU.
- **Legal** copy may need **jurisdiction** review—flag early.

## Handling Deviations

- **Single** extra language: still use **ICU** and **Intl**—habits **scale**.
- **Community** translations: **glossary** and **style** guide **critical**.
