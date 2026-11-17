<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Design System

## 1. Design Principles

| # | Principle | This Means... | This Does NOT Mean... |
|---|-----------|---------------|----------------------|
| 1 | {principle} | {concrete implication for design decisions} | {common misinterpretation} |
| 2 | {principle} | {implication} | {misinterpretation} |
| 3 | {principle} | {implication} | {misinterpretation} |
| 4 | {principle} | {implication} | {misinterpretation} |

**Priority:** When principles conflict, higher-numbered principles yield to lower-numbered.

---

## 2. Color System

### 2.1 Global Palette

| Token | Value | Swatch |
|-------|-------|--------|
| `color.{hue}.50` | {value} | |
| `color.{hue}.100` | {value} | |
| `color.{hue}.500` | {value} | |
| `color.{hue}.900` | {value} | |

### 2.2 Semantic Color Tokens

| Token | References | Purpose |
|-------|-----------|---------|
| `color.primary.default` | `color.{hue}.500` | Primary actions, links, active elements |
| `color.primary.hover` | `color.{hue}.600` | Primary hover state |
| `color.primary.active` | `color.{hue}.700` | Primary pressed state |
| `color.surface.default` | `color.neutral.50` | Page background |
| `color.surface.elevated` | `color.white` | Cards, modals, popovers |
| `color.surface.sunken` | `color.neutral.100` | Input fields, code blocks |
| `color.text.primary` | `color.neutral.900` | Headings, body text |
| `color.text.secondary` | `color.neutral.600` | Labels, placeholders, captions |
| `color.text.disabled` | `color.neutral.400` | Disabled text |
| `color.text.inverse` | `color.white` | Text on colored backgrounds |
| `color.border.default` | `color.neutral.200` | Card borders, dividers |
| `color.border.focus` | `color.primary.default` | Focus rings |
| `color.feedback.error` | `color.red.600` | Error states |
| `color.feedback.success` | `color.green.600` | Success confirmation |
| `color.feedback.warning` | `color.amber.500` | Warnings |
| `color.feedback.info` | `color.blue.500` | Informational |

### 2.3 Contrast Verification

| Pair | Ratio | Standard | Status |
|------|:-----:|----------|:------:|
| `text.primary` on `surface.default` | {N}:1 | ≥4.5:1 (AA) | ✅/❌ |
| `text.secondary` on `surface.default` | {N}:1 | ≥4.5:1 (AA) | ✅/❌ |
| `primary.default` on `surface.default` | {N}:1 | ≥3:1 (UI AA) | ✅/❌ |
| `text.inverse` on `primary.default` | {N}:1 | ≥4.5:1 (AA) | ✅/❌ |
| `border.default` on `surface.default` | {N}:1 | ≥3:1 (UI AA) | ✅/❌ |

---

## 3. Typography

### 3.1 Font Families

| Token | Value | Fallback Stack |
|-------|-------|---------------|
| `font.family.primary` | {font} | {system fallbacks} |
| `font.family.mono` | {mono font} | {fallbacks} |

### 3.2 Type Ramp

| Token | Size | Weight | Line Height | Letter Spacing | Use Case |
|-------|:----:|:------:|:-----------:|:--------------:|----------|
| `typography.display.lg` | 48px | 700 | 1.1 | -0.02em | Hero headings |
| `typography.display.md` | 36px | 700 | 1.15 | -0.01em | Feature titles |
| `typography.heading.lg` | 32px | 600 | 1.25 | 0 | Page titles |
| `typography.heading.md` | 24px | 600 | 1.3 | 0 | Section headings |
| `typography.heading.sm` | 20px | 600 | 1.4 | 0 | Subsections |
| `typography.body.lg` | 18px | 400 | 1.6 | 0 | Lead paragraphs |
| `typography.body.md` | 16px | 400 | 1.5 | 0 | Default body |
| `typography.body.sm` | 14px | 400 | 1.5 | 0.01em | Secondary text |
| `typography.caption` | 12px | 400 | 1.4 | 0.02em | Labels, meta |
| `typography.overline` | 11px | 600 | 1.5 | 0.08em | Category labels |

---

## 4. Spatial System

### 4.1 Base Unit
`spacing.base` = **8px**

### 4.2 Spacing Scale

| Token | Value | Use Case |
|-------|:-----:|----------|
| `spacing.xs` | 4px | Icon-to-text, tight inline |
| `spacing.sm` | 8px | Within components |
| `spacing.md` | 16px | Between elements |
| `spacing.lg` | 24px | Between sections |
| `spacing.xl` | 32px | Major separations |
| `spacing.2xl` | 48px | Page sections |
| `spacing.3xl` | 64px | Hero / feature areas |

### 4.3 Grid

| Property | Mobile (4-col) | Tablet (8-col) | Desktop (12-col) |
|----------|:--------------:|:--------------:|:----------------:|
| Columns | 4 | 8 | 12 |
| Gutter | 16px | 16px | 24px |
| Margin | 16px | 24px | 32px |
| Max width | 100% | 100% | {N}px |

### 4.4 Breakpoints

| Token | Value | Context |
|-------|:-----:|---------|
| `breakpoint.sm` | 640px | Mobile → Tablet |
| `breakpoint.md` | 768px | Tablet portrait |
| `breakpoint.lg` | 1024px | Tablet → Desktop |
| `breakpoint.xl` | 1280px | Desktop |
| `breakpoint.2xl` | 1536px | Large desktop |

---

## 5. Iconography

| Property | Value |
|----------|-------|
| Style | {Outlined / Filled / Rounded} |
| Grid | {24x24px} |
| Stroke | {1.5px} |
| Corner radius | {matches `radius.sm`} |
| Color | Inherits from text token |

### Sizing Scale

| Token | Size | Use Case |
|-------|:----:|----------|
| `sizing.icon.xs` | 12px | Inline indicators |
| `sizing.icon.sm` | 16px | Compact UI |
| `sizing.icon.md` | 20px | Default (buttons, nav) |
| `sizing.icon.lg` | 24px | Feature icons |
| `sizing.icon.xl` | 32px | Empty states, features |

### Usage Rules
1. Icons always have a text label OR `aria-label`
2. Decorative icons use `aria-hidden="true"`
3. Directional icons (arrows, chevrons) mirror in RTL
4. Touch targets: minimum 44×44px regardless of icon size
5. Color inherits parent text color — never hardcode

---

## 6. Border Radius

| Token | Value | Use Case |
|-------|:-----:|----------|
| `radius.none` | 0px | Sharp edges (tables, code blocks) |
| `radius.sm` | 4px | Inputs, small elements |
| `radius.md` | 8px | Cards, buttons |
| `radius.lg` | 12px | Modals, large containers |
| `radius.xl` | 16px | Feature cards |
| `radius.full` | 9999px | Pills, avatars, circular |

---

## 7. Elevation / Shadow

| Token | Value | Use Case |
|-------|-------|----------|
| `shadow.none` | none | Flat elements |
| `shadow.sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift (dropdowns) |
| `shadow.md` | `0 4px 6px rgba(0,0,0,0.07)` | Cards |
| `shadow.lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, popovers |
| `shadow.xl` | `0 20px 25px rgba(0,0,0,0.12)` | Top-level overlays |
| `shadow.focus` | `0 0 0 3px {color.primary.default/30%}` | Focus ring |

---

## Cross-References

| Artifact | Connection |
|----------|-----------|
| Design Tokens (detailed) | `Design_Tokens.md` — full token spec with all tiers |
| Component Library | Components reference these tokens |
| Accessibility Baseline | Contrast ratios verified here |
| Voice & Tone | See `Voice_Tone_Guidelines.md` |
| Multi-Brand Theming | See `Multi_Brand_Theming.md` (if active) |
