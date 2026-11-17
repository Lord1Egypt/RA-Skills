<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: UX Design Package (AI-UXD) → theming.md (UXD CLUSTER)

## Purpose

Transforms the **multi-brand theming and dark-mode token architecture** produced by AI-UXD (`design/multi-brand-theming.md`) into a prescriptive `theming.md` steering file. This governs how themes (brands, color modes) are structured and switched in the build workspace, so AI-DLC v1 implements a token-driven theming system that matches the designed inheritance model rather than hardcoding per-theme styles.

**Output:** `rules/theming.md`

**Condition:** Generate IF `uxd-state.md` is present AND the UXP contains multi-brand theming OR color-mode (dark/light) tokens. (This is AI-UXD's conditional Stage 10 — if it did not run, SKIP and leave base theming rules in `design-system.md` DS-THM-01/04.)

**Cluster:** UX — belongs exclusively to the UXD input cluster.

---

## MANDATORY: Stage Sub-Role — UX Designer

During THIS activity, ALSO adopt the mindset of a **UX Designer** (brand-designer/design-systems lens). ADDS a thinking dimension — does NOT replace your primary role.

### Behavioral Shifts
- Theming is token inheritance, not a second stylesheet — global → semantic → theme overrides
- Dark mode is a token layer, not inverted colors — preserve the designed dark token set verbatim
- A theme is a named override map — each theme references the same semantic token names
- Mode/brand switching is a contract — preserve the switching mechanism the UXP defined

### Anti-Patterns for This Activity
- Do NOT compute dark-mode values — copy the UXP's dark token set exactly
- Do NOT collapse brand themes into one — each brand keeps its override set
- Do NOT duplicate base token definitions — reference `design-system.md`; this file is theming-only

---

## Source Inputs

**Primary source:** AI-UXD → UXP, via `uxd-state.md` marker.

| UXP Document | What to Extract | Maps to Section |
|---|---|---|
| Multi-brand theming (`design/multi-brand-theming.md`) | Brand list, per-brand token overrides | Brand Themes |
| Color-mode tokens | Light/dark (and any additional mode) token sets | Color Modes |
| Token inheritance model | global → semantic → theme layering | Theme Architecture |
| Switching behavior | How theme/mode is selected, persisted, defaulted | Switching Rules |

### `uxd-state.md` Fields Used

| Field | Used For |
|-------|----------|
| `Multi-Brand` / `Color Modes` | Confirms Stage 10 ran (hard gate) |
| `Token Format` | Output token format (W3C / Style Dictionary / custom) |
| `Project ID` | Correlation key |

---

## Target Structure: theming.md

```markdown
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "AI-UXD — design/multi-brand-theming.md"
generatedOn: "{generation-date}"
ownership: generated
projectId: "{project-id}"
---

<!-- AI-DWG generated | source: AI-UXD Multi-Brand Theming | date: {generation-date} -->

# Theming Rules

> Base tokens live in `design-system.md`. This file governs how themes override them.

## Theme Architecture
| Rule ID | Rule |
|---------|------|
| THM-ARCH-01 | Themes MUST override only SEMANTIC tokens, never global primitives. |
| THM-ARCH-02 | Inheritance order: global → semantic → theme. MUST NOT skip layers. |

## Color Modes
<!-- begin: UXP-sourced -->
| Rule ID | Mode | Token | Value | Note |
|---------|------|-------|-------|------|
| THM-MODE-01 | dark | `--color-surface` | {value} | MUST respect prefers-color-scheme |
| ... | ... | ... | ... | ... |
<!-- end: UXP-sourced -->

## Brand Themes (IF multi-brand)
<!-- begin: UXP-sourced -->
| Rule ID | Brand | Overridden Token | Value |
|---------|-------|------------------|-------|
| THM-BRD-01 | {brand} | `--color-primary` | {value} |
| ... | ... | ... | ... |
<!-- end: UXP-sourced -->

## Switching Rules
| Rule ID | Rule |
|---------|------|
| THM-SW-01 | Theme/mode selection MUST be {mechanism}; default = {default}. |
| THM-SW-02 | Selection MUST persist via {persistence}; MUST honor system preference on first load. |
```

---

## Transformation Rules

### Rule 1: Token Values Are VERBATIM
Dark-mode and per-brand token values are copied exactly — never computed or inverted.

### Rule 2: Inheritance Model Preserved
Reproduce the global → semantic → theme layering exactly as designed.

### Rule 3: No Base-Token Duplication
Reference `design-system.md` for primitives; this file lists only overrides.

### Rule 4: Switching Mechanism Carried
Persist the UXP-defined selection/persistence/default behavior as MUST rules.

---

## Interaction with Other Mappings

| Related Mapping | Relationship |
|---|---|
| `uxd-to-design-system.md` | Base tokens + `DS-THM-01/04` live there; multi-theme overrides live here. If Stage 10 did not run, only DS-THM-01/04 exist and this file is skipped. |
| `uxd-to-i18n.md` | RTL may interact with theming (logical properties) — keep token names direction-agnostic. |

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| UXP present, Stage 10 NOT run (single brand, single mode) | SKIP; base theming stays in `design-system.md` DS-THM-01/04 |
| Dark mode only, no multi-brand | Generate Color Modes; omit Brand Themes |
| Multi-brand, no dark mode | Generate Brand Themes; omit Color Modes |
| Theme overrides a global primitive (anti-pattern in UXP) | Flag as a UXP finding; do not propagate the anti-pattern |

---

## Output Validation

- [ ] Generated ONLY when multi-brand and/or color modes exist
- [ ] Token values copied verbatim (not computed)
- [ ] Inheritance order (global→semantic→theme) preserved
- [ ] No base-token duplication (references `design-system.md`)
- [ ] Switching/persistence/default rules present
- [ ] Provenance front-matter + projectId present
