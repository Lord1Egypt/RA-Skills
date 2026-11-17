<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-UXD
generatedVersion: "{version}"
source: "{upstream-doc-path}"
generatedOn: "{ISO-date}"
ownership: hybrid
---

# Multi-Brand Theming Architecture

## Theme Contexts

| Context | Type | Description |
|---------|------|-------------|
| Base (Light) | Default | Light mode, primary brand |
| Dark | Color Mode | Dark mode override |
| {Brand A} | Brand | Brand-specific overrides |
| {Brand B} | Brand | Brand-specific overrides |
| {Brand A + Dark} | Composed | Brand A in dark mode |

---

## Token Inheritance Model

```
Global Tokens (raw values — never change per theme)
       │
       ▼
Semantic Tokens (base / default theme)
       │
       ├── Dark Mode Override (changes surface/text/border semantics)
       │
       ├── Brand A Override (changes primary/accent hues)
       │       │
       │       └── Brand A + Dark (both overrides composed)
       │
       └── Brand B Override
               │
               └── Brand B + Dark
```

**Rules:**
1. Component tokens ALWAYS reference semantic tokens (never global)
2. A "theme" = a set of semantic token overrides
3. Unoverridden tokens inherit from base
4. Themes compose: Brand + Mode = both override sets applied
5. Conflicts: Mode override wins on surface/text; Brand wins on primary/accent

---

## Color Mode: Dark

### Override Table

| Semantic Token | Light (Base) | Dark Override | Rationale |
|---------------|-------------|--------------|-----------|
| `color.surface.default` | `color.neutral.50` | `color.neutral.900` | Dark background |
| `color.surface.elevated` | `color.white` | `color.neutral.800` | Lighter than bg (inverted elevation) |
| `color.surface.sunken` | `color.neutral.100` | `color.neutral.950` | Darker than bg |
| `color.text.primary` | `color.neutral.900` | `color.neutral.50` | Light text on dark |
| `color.text.secondary` | `color.neutral.600` | `color.neutral.400` | Muted but readable |
| `color.text.disabled` | `color.neutral.400` | `color.neutral.600` | Reduced prominence |
| `color.border.default` | `color.neutral.200` | `color.neutral.700` | Visible on dark surface |
| `color.primary.default` | `color.{hue}.500` | `color.{hue}.400` | Lighter for dark contrast |

### Dark Mode Design Rules
1. Elevation = lighter surface (not shadow) — shadows invisible in dark
2. Never use pure black (#000000) — use `color.neutral.900` or darker
3. Reduce saturation slightly on large colored surfaces
4. Primary hue shifts lighter (+1 step) for contrast on dark surfaces
5. Focus rings remain visible (test against dark background)

---

## Brand Override: {Brand A}

### Brand Identity

| Property | Value |
|----------|-------|
| Brand name | {name} |
| Primary hue | {color family + hex} |
| Accent hue | {if different from primary} |
| Typography | {brand font or "inherit base"} |
| Border radius | {brand personality: rounded/sharp or "inherit base"} |
| Logo | {reference/link} |

### Override Table

| Token | Base Value | {Brand A} Override | Rationale |
|-------|-----------|-------------------|-----------|
| `color.primary.default` | {base} | {brand value} | Brand primary color |
| `color.primary.hover` | {base} | {brand value} | Brand hover |
| `color.primary.active` | {base} | {brand value} | Brand active |
| `font.family.primary` | {base} | {brand font or same} | Brand typography |
| `radius.md` | {base} | {brand value or same} | Brand personality |

### What Does NOT Change Per Brand
- Spacing system (consistency)
- Shadow system (functional)
- Z-index (structural)
- Typography scale (only family may change, not sizes)
- Component structure (only colors/fonts change)
- Accessibility requirements (non-negotiable)
- Icon system style (operational, not decorative)

---

## Brand Override: {Brand B}

{Same structure as Brand A — repeat the override table}

---

## Theme Switching Behavior

| Aspect | Decision |
|--------|----------|
| **Detection** | `prefers-color-scheme` media query (system preference) |
| **User override** | Manual toggle in settings / UI |
| **Persistence** | Stored in `localStorage` / user preferences |
| **Priority** | User preference > System preference > Default (light) |
| **Transition** | {Instant / Smooth 200ms opacity} |
| **Initial load** | Stored → System → Light (waterfall) |
| **Flash prevention** | Inline script in `<head>` sets class before render |

---

## Contrast Verification (Per Theme)

| Theme | Pair | Ratio | Standard | Pass |
|-------|------|:-----:|----------|:----:|
| Light | text.primary on surface.default | {N}:1 | ≥4.5 AA | ✅/❌ |
| Light | text.secondary on surface.default | {N}:1 | ≥4.5 AA | ✅/❌ |
| Dark | text.primary on surface.default | {N}:1 | ≥4.5 AA | ✅/❌ |
| Dark | text.secondary on surface.default | {N}:1 | ≥4.5 AA | ✅/❌ |
| {Brand A} Light | text on surface | {N}:1 | ≥4.5 AA | ✅/❌ |
| {Brand A} Dark | text on surface | {N}:1 | ≥4.5 AA | ✅/❌ |

**Every combination must pass.** Failing combinations must have their override tokens adjusted.

---

## Implementation Notes for AI-DWG

When AI-DWG consumes this specification:
- Generate CSS custom properties with theme class selectors (`.theme-dark`, `.theme-brand-a`)
- Generate token files per theme context for Style Dictionary / build tool
- Add `design-system.md` steering section on theme switching implementation
- Include the contrast-verification requirement in `frontend-standards.md`
