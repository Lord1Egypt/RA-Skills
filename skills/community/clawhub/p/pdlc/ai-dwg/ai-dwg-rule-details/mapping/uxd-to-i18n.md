<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package (AI-UXD) → i18n-standards.md (UXD CLUSTER)

## Purpose

Transforms the **internationalization, RTL, and localization tokens** produced by AI-UXD (the i18n/RTL conditional generation) into a prescriptive `i18n-standards.md` steering file. This governs how the build workspace handles multiple locales, text direction, and localizable values, so AI-DLC v1 builds i18n-ready interfaces from day one instead of retrofitting localization later (an expensive and error-prone path).

**Output:** `rules/i18n-standards.md`

**Condition:** Generate IF `uxd-state.md` is present AND the UXP defines i18n/RTL/localization concerns (more than one locale OR multi-language mentioned — AI-UXD's i18n conditional generator). If single-locale, SKIP and note: "Single-locale product — i18n standards not generated."

**Cluster:** UX — belongs exclusively to the UXD input cluster.

---

## MANDATORY: Stage Sub-Role — UX Designer

During THIS activity, ALSO adopt the mindset of a **UX Designer** (with an accessibility/internationalization lens). ADDS a thinking dimension — does NOT replace your primary role.

### Behavioral Shifts
- Localization is structural — text length, direction, and formatting shape the layout, not just the strings
- RTL is a first-class mode — logical properties (start/end), not left/right, are mandatory
- Locale-dependent values (dates, numbers, currency) are tokens, not literals
- Externalized strings are non-negotiable — no hardcoded user-facing text

### Anti-Patterns for This Activity
- Do NOT hardcode left/right when RTL is in scope — mandate logical properties
- Do NOT assume English string lengths — preserve UXP's expansion allowances
- Do NOT drop locale-specific formatting rules (dates, numbers, currency, pluralization)

---

## Source Inputs

**Primary source:** AI-UXD → UXP, via `uxd-state.md` marker.

| UXP Source | What to Extract | Maps to Section |
|---|---|---|
| Locale list | Supported locales, default locale | Supported Locales |
| RTL / direction notes | Which locales are RTL, mirroring rules | RTL & Direction Rules |
| Localization tokens | Date/number/currency formats, pluralization, expansion allowance | Localization Tokens |
| Design system (spacing/type) | Text-expansion tolerance in layout | Layout Tolerance Rules |

### `uxd-state.md` Fields Used

| Field | Used For |
|-------|----------|
| `Locales` / `i18n` | Confirms i18n conditional ran (hard gate) |
| `Project ID` | Correlation key |

---

## Target Structure: i18n-standards.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD — i18n/RTL/localization tokens"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-UXD i18n/RTL | date: {generation-date} -->

# Internationalization (i18n) Standards

## Supported Locales
<!-- begin: UXP-sourced -->
| Locale | Direction | Default | Notes |
|--------|-----------|---------|-------|
| {locale} | {ltr/rtl} | {yes/no} | {region/format notes} |
<!-- end: UXP-sourced -->

## String Externalization Rules
| Rule ID | Rule |
|---------|------|
| I18N-01 | All user-facing text MUST be externalized to locale resource files. MUST NOT hardcode UI strings. |
| I18N-02 | Keys MUST be semantic (`checkout.button.pay`), not English-literal. |

## RTL & Direction Rules (IF any RTL locale)
| Rule ID | Rule |
|---------|------|
| I18N-RTL-01 | Layout MUST use logical properties (`margin-inline-start`), NEVER physical left/right. |
| I18N-RTL-02 | Icons/affordances with directional meaning MUST mirror in RTL per UXP. |

## Localization Tokens
<!-- begin: UXP-sourced -->
| Rule ID | Token / Format | Value | Locale Variance |
|---------|----------------|-------|-----------------|
| I18N-FMT-01 | date | {format} | {per-locale} |
| I18N-FMT-02 | number/currency | {format} | {per-locale} |
| I18N-FMT-03 | pluralization | {rule set} | {per-locale} |
<!-- end: UXP-sourced -->

## Layout Tolerance Rules
| Rule ID | Rule |
|---------|------|
| I18N-LAY-01 | UI MUST tolerate {expansion}% text expansion without truncation/overflow. |
```

---

## Transformation Rules

### Rule 1: Locale List & Formats Are VERBATIM
Copy supported locales, default, direction, and format tokens exactly.

### Rule 2: RTL Section Is Conditional
Generate RTL & Direction Rules only if at least one locale is RTL; otherwise omit with `<!-- no RTL locales in scope -->`.

### Rule 3: Externalization Is Always Mandatory (when i18n in scope)
String externalization rules are non-negotiable MUSTs whenever this file generates.

### Rule 4: Expansion Allowance Preserved
Carry the UXP's text-expansion tolerance into a concrete layout rule.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `uxd-to-voice-tone.md` | Per-locale tone constraints reconcile here; voice rules stay in content-guidelines. |
| `uxd-to-theming.md` | RTL relies on direction-agnostic tokens — keep theming token names logical. |
| `uxd-to-design-system.md` | Spacing/type tokens must accommodate expansion tolerance defined here. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| Single-locale product | SKIP; note "i18n standards not generated (single locale)" |
| Multiple locales, none RTL | Generate without RTL section |
| RTL in scope but no mirroring notes | Include I18N-RTL-01 (logical properties); flag missing mirroring detail |
| Locale formats unspecified | Mark format tokens `{TBD — confirm per locale}`; keep externalization rules |

---

## Output Validation

- [ ] Generated ONLY when i18n/multi-locale is in scope
- [ ] Locale list, direction, default copied verbatim
- [ ] RTL section present IFF an RTL locale exists
- [ ] String externalization rules present (mandatory)
- [ ] Localization format tokens carried (or explicit TBD)
- [ ] Provenance front-matter + projectId present
