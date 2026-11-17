<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 10: Multi-Brand Theming

## Purpose

Define the token architecture for supporting multiple brands, color modes (dark/light), or both. This stage adds a theming layer on top of the design system foundation, enabling the same component library to render differently per brand or context.

---

## CONDITIONAL — Executes IF:
- Product serves >1 brand (white-label, partner brands)
- Product requires color modes (dark mode, high-contrast mode)
- Brief explicitly mentions theming requirements

If none of these conditions are met → skip to Stage 11.

---

## Depth Adaptation

| Depth | Theming Output |
|-------|---------------|
| **Minimal** | Dark/light mode token override table only |
| **Standard** | Full theme architecture: base + brand/mode overrides + switching logic |
| **Comprehensive** | Full architecture + per-brand guidelines + theme testing matrix |

---

## Steps

### Step 1: Identify Theming Requirements

| Dimension | Options | This Product |
|-----------|---------|-------------|
| Brand variants | Single / Multi-brand / White-label | {answer} |
| Color modes | None / Light+Dark / Light+Dark+High-Contrast | {answer} |
| User control | System preference / Manual toggle / Both | {answer} |
| Scope | Full theme / Partial (colors only) | {answer} |

### Step 2: Define Token Inheritance Architecture

```
┌─────────────────────────────────────┐
│ TIER 1: Global Tokens (raw values)  │  ← color.blue.500 = #2563EB
├─────────────────────────────────────┤
│ TIER 2: Semantic Tokens (purpose)   │  ← color.primary.default → color.blue.500
├─────────────────┬───────────────────┤
│ LIGHT MODE      │ DARK MODE         │  ← Override semantic → different globals
│ surface = white │ surface = gray.900│
│ text = gray.900 │ text = gray.50    │
├─────────────────┼───────────────────┤
│ BRAND A         │ BRAND B           │  ← Override primary → different hue
│ primary = blue  │ primary = green   │
└─────────────────┴───────────────────┘
```

**Inheritance rules:**
1. Component tokens reference semantic tokens (never global directly)
2. Semantic tokens resolve differently per theme context
3. A theme = a set of semantic token overrides
4. Unoverridden tokens inherit from the base/default theme
5. Themes compose: Brand A + Dark Mode = Brand A's dark override set

### Step 3: Define Mode Contexts

For each color mode:

```markdown
## Color Modes

### Light Mode (Default)
| Semantic Token | Resolves To | Purpose |
|---------------|-------------|---------|
| `color.surface.default` | `color.white` | Page background |
| `color.surface.elevated` | `color.white` + shadow | Cards, modals |
| `color.text.primary` | `color.neutral.900` | Body text |
| `color.text.inverse` | `color.white` | Text on dark surfaces |

### Dark Mode
| Semantic Token | Resolves To | Purpose |
|---------------|-------------|---------|
| `color.surface.default` | `color.neutral.900` | Page background |
| `color.surface.elevated` | `color.neutral.800` | Cards, modals (lighter than bg) |
| `color.text.primary` | `color.neutral.50` | Body text |
| `color.text.inverse` | `color.neutral.900` | Text on light surfaces |

### Dark Mode Design Principles
1. Surface hierarchy reverses: elevated = lighter (not darker + shadow)
2. Shadows are invisible in dark mode — use surface color steps instead
3. Primary colors may need lightness adjustment for contrast
4. Reduce saturation slightly for large colored surfaces
5. Never use pure black (#000) as background — use very dark gray
```

### Step 4: Define Brand Overrides (if multi-brand)

For each brand variant:

```markdown
## Brand: {Name}

### Brand Identity
| Property | Value |
|----------|-------|
| Primary hue | {color family} |
| Logo | {reference} |
| Typography override | {if brand has custom font — otherwise inherits base} |
| Personality shift | {any tone/voice adjustment} |

### Token Overrides
| Token | Base Value | Brand Override | Reason |
|-------|-----------|---------------|--------|
| `color.primary.default` | {base} | {brand value} | Brand color |
| `font.family.primary` | {base} | {brand font or same} | Brand identity |
| `radius.md` | {base} | {brand value or same} | Brand personality (rounded vs sharp) |

### What Does NOT Change Per Brand
- Spacing system (consistency across brands)
- Icon style (operational, not brand-decorative)
- Component structure (only colors/fonts change)
- Accessibility requirements (non-negotiable)
```

### Step 5: Define Theme Switching Behavior

| Trigger | Behavior |
|---------|----------|
| System preference (OS setting) | Detect `prefers-color-scheme` → apply matching mode |
| User manual toggle | Store preference → persist across sessions |
| Conflict resolution | User preference > system preference |
| Transition | Instant (no animation) or smooth (200ms opacity) — decide |
| Initial load | Apply stored preference → fall back to system → fall back to light |

### Step 6: Contrast Re-Verification

Re-run contrast checks from Stage 8 for EACH theme context:

| Theme | Pair | Ratio | WCAG | Status |
|-------|------|-------|------|--------|
| Light | text.primary on surface.default | {ratio} | AA | ✅/❌ |
| Dark | text.primary on surface.default | {ratio} | AA | ✅/❌ |
| Brand A Light | ... | ... | ... | ... |
| Brand A Dark | ... | ... | ... | ... |

**Every combination must pass.** If it doesn't, adjust the override tokens.

### Step 7: Present for Approval

Present:
- Token inheritance architecture (diagram)
- All theme contexts defined
- Override tables per brand/mode
- Contrast verification results
- Switching behavior decision
- What is fixed vs. what varies

---

## Gate

**Approval required before proceeding to Stage 11.**

User must confirm:
- Theme architecture is sound (inheritance makes sense)
- All mode/brand combinations pass contrast
- Switching behavior is appropriate
- Override scope is clear (what changes, what doesn't)

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 10 with date and artifact (`09_Multi_Brand_Theming.md`)
- Current Stage: 11

---

## Transition

After gate approval:
```
Stage 10 complete. Theming architecture defined with {N} theme contexts.

Moving to Stage 11: Accessibility Baseline. I'll now consolidate
all accessibility requirements into a governed baseline document.
```

Load `validate/accessibility-baseline.md`.
