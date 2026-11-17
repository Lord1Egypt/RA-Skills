<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Design Tokens Specification

> Aligned with [W3C Design Tokens Format Module (2025.10)](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/)

## Token Architecture

```
┌─────────────────────────────────────────┐
│ TIER 1: Global Tokens                    │  Raw values — the palette
│ color.blue.500, spacing.16, font.inter   │
├─────────────────────────────────────────┤
│ TIER 2: Semantic / Alias Tokens          │  Purpose — references Tier 1
│ color.primary.default → color.blue.500   │
├─────────────────────────────────────────┤
│ TIER 3: Component Tokens                 │  Scoped — references Tier 2
│ button.bg.default → color.primary.default│
└─────────────────────────────────────────┘
```

### Naming Convention

`{category}.{item}.{sub-item}.{state}`

| Segment | Examples |
|---------|----------|
| Category | `color`, `spacing`, `typography`, `sizing`, `radius`, `shadow`, `motion`, `breakpoint`, `z` |
| Item | `primary`, `surface`, `text`, `border`, `feedback`, `heading`, `body` |
| Sub-item | `default`, `hover`, `active`, `disabled`, `error`, `success` |
| State (Tier 3) | Component-specific states |

---

## Color Tokens

### Tier 1: Global (Raw Palette)

| Token | Value | Type |
|-------|-------|------|
| `color.{hue}.50` | {value} | color |
| `color.{hue}.100` | {value} | color |
| `color.{hue}.200` | {value} | color |
| `color.{hue}.300` | {value} | color |
| `color.{hue}.400` | {value} | color |
| `color.{hue}.500` | {value} | color |
| `color.{hue}.600` | {value} | color |
| `color.{hue}.700` | {value} | color |
| `color.{hue}.800` | {value} | color |
| `color.{hue}.900` | {value} | color |

### Tier 2: Semantic (Purpose)

| Token | References | Description |
|-------|-----------|-------------|
| `color.primary.default` | `color.{hue}.500` | Primary brand, CTAs, links |
| `color.primary.hover` | `color.{hue}.600` | Primary hover |
| `color.primary.active` | `color.{hue}.700` | Primary pressed |
| `color.surface.default` | `color.neutral.50` | Page background |
| `color.surface.elevated` | `color.white` | Cards, modals |
| `color.surface.sunken` | `color.neutral.100` | Inputs, code blocks |
| `color.text.primary` | `color.neutral.900` | Body text |
| `color.text.secondary` | `color.neutral.600` | Supporting text |
| `color.text.disabled` | `color.neutral.400` | Disabled elements |
| `color.text.inverse` | `color.white` | On dark backgrounds |
| `color.border.default` | `color.neutral.200` | Dividers, card borders |
| `color.border.strong` | `color.neutral.400` | Emphasized borders |
| `color.border.focus` | `color.primary.default` | Focus indicators |
| `color.feedback.error` | `color.red.600` | Error states |
| `color.feedback.success` | `color.green.600` | Success |
| `color.feedback.warning` | `color.amber.500` | Warning |
| `color.feedback.info` | `color.blue.500` | Informational |

---

## Typography Tokens

| Token | Value | Type | Description |
|-------|-------|------|-------------|
| `font.family.primary` | {value} | fontFamily | Primary typeface |
| `font.family.mono` | {value} | fontFamily | Code / monospace |
| `typography.display.lg` | {composite} | typography | Hero headings |
| `typography.heading.lg` | {composite} | typography | Page titles |
| `typography.heading.md` | {composite} | typography | Section headings |
| `typography.heading.sm` | {composite} | typography | Subsections |
| `typography.body.lg` | {composite} | typography | Lead text |
| `typography.body.md` | {composite} | typography | Default body |
| `typography.body.sm` | {composite} | typography | Secondary text |
| `typography.caption` | {composite} | typography | Labels, meta |

---

## Spacing Tokens

| Token | Value | Type | Description |
|-------|:-----:|------|-------------|
| `spacing.xs` | 4px | dimension | Tight (icon gaps) |
| `spacing.sm` | 8px | dimension | Compact (within components) |
| `spacing.md` | 16px | dimension | Standard (between elements) |
| `spacing.lg` | 24px | dimension | Section spacing |
| `spacing.xl` | 32px | dimension | Major gaps |
| `spacing.2xl` | 48px | dimension | Page sections |
| `spacing.3xl` | 64px | dimension | Hero areas |

---

## Sizing Tokens

| Token | Value | Type | Description |
|-------|:-----:|------|-------------|
| `sizing.icon.xs` | 12px | dimension | Inline indicators |
| `sizing.icon.sm` | 16px | dimension | Compact UI |
| `sizing.icon.md` | 20px | dimension | Default icons |
| `sizing.icon.lg` | 24px | dimension | Feature icons |
| `sizing.icon.xl` | 32px | dimension | Empty states |
| `sizing.avatar.sm` | 24px | dimension | Inline avatars |
| `sizing.avatar.md` | 32px | dimension | List items |
| `sizing.avatar.lg` | 48px | dimension | Profile headers |
| `sizing.touch-target` | 44px | dimension | Minimum touch area |

---

## Radius Tokens

| Token | Value | Type | Description |
|-------|:-----:|------|-------------|
| `radius.none` | 0px | dimension | Sharp corners |
| `radius.sm` | 4px | dimension | Inputs, small |
| `radius.md` | 8px | dimension | Cards, buttons |
| `radius.lg` | 12px | dimension | Modals |
| `radius.xl` | 16px | dimension | Feature cards |
| `radius.full` | 9999px | dimension | Pills, circles |

---

## Shadow Tokens

| Token | Value | Type | Description |
|-------|-------|------|-------------|
| `shadow.none` | none | shadow | Flat |
| `shadow.sm` | 0 1px 2px rgba(0,0,0,0.05) | shadow | Subtle lift |
| `shadow.md` | 0 4px 6px rgba(0,0,0,0.07) | shadow | Cards |
| `shadow.lg` | 0 10px 15px rgba(0,0,0,0.1) | shadow | Modals |
| `shadow.xl` | 0 20px 25px rgba(0,0,0,0.12) | shadow | Overlays |
| `shadow.focus` | 0 0 0 3px {color.primary/30%} | shadow | Focus ring |

---

## Breakpoint Tokens

| Token | Value | Type | Description |
|-------|:-----:|------|-------------|
| `breakpoint.sm` | 640px | dimension | Mobile → Tablet |
| `breakpoint.md` | 768px | dimension | Tablet portrait |
| `breakpoint.lg` | 1024px | dimension | Tablet → Desktop |
| `breakpoint.xl` | 1280px | dimension | Desktop |
| `breakpoint.2xl` | 1536px | dimension | Large desktop |

---

## Z-Index Tokens

| Token | Value | Type | Description |
|-------|:-----:|------|-------------|
| `z.base` | 0 | number | Default stacking |
| `z.dropdown` | 100 | number | Dropdowns, popovers |
| `z.sticky` | 200 | number | Sticky headers |
| `z.overlay` | 300 | number | Overlay backdrop |
| `z.modal` | 400 | number | Modal dialogs |
| `z.toast` | 500 | number | Toast notifications |
| `z.tooltip` | 600 | number | Tooltips (topmost) |

---

## Token Count Summary

| Category | Count |
|----------|:-----:|
| Color (Global) | {N} |
| Color (Semantic) | {N} |
| Typography | {N} |
| Spacing | {N} |
| Sizing | {N} |
| Radius | {N} |
| Shadow | {N} |
| Breakpoint | {N} |
| Z-Index | {N} |
| **Total** | **{N}** |

---

## Consumption Guide

### For Developers (via Style Dictionary / Tokens Studio)
- Export format: JSON (W3C Design Tokens Format)
- Platform targets: CSS custom properties, SCSS variables, JS/TS constants
- Build command: `{tool-specific command}`

### For Designers (via Figma / tool)
- Sync mechanism: {Tokens Studio plugin / manual / API}
- Variable modes: {light, dark, brand-A, brand-B}

### For AI-DWG
- AI-DWG reads this file and generates `design-system.md` steering
- Tokens inform `frontend-standards.md` enforcement rules

### For AI-GCE
- AI-GCE derives "no hardcoded values" enforcement from this spec
- Every dimension in code must reference a token, not a literal
