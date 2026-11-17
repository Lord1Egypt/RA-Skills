<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 8: Design System Foundation

## Purpose

Define the governed design system — the single source of truth for how the product looks, reads, and behaves. Covers design principles, color, typography, spatial system, iconography, voice & tone, and (conditionally) i18n/localization. All values expressed as design tokens.

---

## Depth Adaptation

| Depth | Design System Output |
|-------|---------------------|
| **Minimal** | Principles + core color palette + type scale + basic grid + essential tokens |
| **Standard** | Full system: all sections below with semantic + component token tiers |
| **Comprehensive** | Full system + extended token documentation + content model + governance rules |

---

## Steps

### Step 1: Design Principles

Define 4-6 principles that guide ALL design decisions:

```markdown
## Design Principles

| # | Principle | This Means... | This Does NOT Mean... |
|---|-----------|---------------|----------------------|
| 1 | {principle} | {concrete implication} | {common misinterpretation} |
| 2 | {principle} | {concrete implication} | {misinterpretation} |
```

**Good principles are:**
- Opinionated (not truisms like "be user-friendly")
- Actionable (help resolve design debates)
- Prioritized (when two conflict, which wins?)
- Traceable to research (each connects to a persona need or pain point)

### Step 2: Color System

```markdown
## Color System

### Palette (Global Tokens)
| Token | Value | Purpose |
|-------|-------|---------|
| `color.blue.500` | #2563EB | Primary brand |
| `color.blue.600` | #1D4ED8 | Primary hover |
| ... | ... | ... |

### Semantic Tokens (Alias Layer)
| Token | References | Purpose |
|-------|-----------|---------|
| `color.primary.default` | `color.blue.500` | Primary actions, links |
| `color.primary.hover` | `color.blue.600` | Primary hover state |
| `color.surface.default` | `color.neutral.50` | Page background |
| `color.surface.elevated` | `color.white` | Cards, modals |
| `color.text.primary` | `color.neutral.900` | Body text |
| `color.text.secondary` | `color.neutral.600` | Supporting text |
| `color.feedback.error` | `color.red.600` | Error messages |
| `color.feedback.success` | `color.green.600` | Success confirmation |
| `color.feedback.warning` | `color.amber.500` | Warning alerts |
| `color.feedback.info` | `color.blue.500` | Informational |

### Contrast Verification
| Pair | Ratio | WCAG | Status |
|------|-------|------|--------|
| text.primary on surface.default | {ratio} | AA (≥4.5:1) | ✅/❌ |
| text.secondary on surface.default | {ratio} | AA (≥4.5:1) | ✅/❌ |
| primary.default on surface.default | {ratio} | AA (≥3:1 for UI) | ✅/❌ |
```

### Step 3: Typography Scale

```markdown
## Typography

### Type Ramp
| Token | Size | Weight | Line Height | Use Case |
|-------|------|--------|-------------|----------|
| `typography.display.lg` | 48px | 700 | 1.1 | Hero headings |
| `typography.heading.lg` | 32px | 700 | 1.25 | Page titles |
| `typography.heading.md` | 24px | 600 | 1.3 | Section headings |
| `typography.heading.sm` | 20px | 600 | 1.4 | Subsections |
| `typography.body.lg` | 18px | 400 | 1.6 | Lead paragraphs |
| `typography.body.md` | 16px | 400 | 1.5 | Body text (default) |
| `typography.body.sm` | 14px | 400 | 1.5 | Secondary text |
| `typography.caption` | 12px | 400 | 1.4 | Labels, timestamps |

### Font Families
| Token | Value | Fallback Stack |
|-------|-------|---------------|
| `font.family.primary` | {font name} | {fallback fonts} |
| `font.family.mono` | {mono font} | {fallback} |

### Responsive Scaling
| Breakpoint | Scale Factor | Body Size |
|------------|-------------|-----------|
| Mobile | 1.0x | 16px |
| Tablet | 1.0x | 16px |
| Desktop | 1.125x | 18px (optional) |
```

### Step 4: Spatial System

```markdown
## Spatial System

### Base Unit
`spacing.base` = 8px (all spacing is a multiple of this)

### Spacing Scale
| Token | Value | Use Case |
|-------|-------|----------|
| `spacing.xs` | 4px | Tight gaps (icon-to-text) |
| `spacing.sm` | 8px | Compact spacing (within components) |
| `spacing.md` | 16px | Standard spacing (between elements) |
| `spacing.lg` | 24px | Section spacing |
| `spacing.xl` | 32px | Major section gaps |
| `spacing.2xl` | 48px | Page-level separation |
| `spacing.3xl` | 64px | Hero/feature spacing |

### Grid
| Property | Mobile | Tablet | Desktop |
|----------|--------|--------|---------|
| Columns | 4 | 8 | 12 |
| Gutter | 16px | 16px | 24px |
| Margin | 16px | 24px | 32px |
| Max width | 100% | 100% | 1280px |

### Breakpoints
| Token | Value | Context |
|-------|-------|---------|
| `breakpoint.sm` | 640px | Large mobile / small tablet |
| `breakpoint.md` | 768px | Tablet portrait |
| `breakpoint.lg` | 1024px | Tablet landscape / small desktop |
| `breakpoint.xl` | 1280px | Desktop |
| `breakpoint.2xl` | 1536px | Large desktop |
```

### Step 5: Iconography & Illustration

```markdown
## Iconography

### Icon System
| Property | Value |
|----------|-------|
| Style | {Outlined / Filled / Rounded} |
| Grid | {24x24px / 20x20px} |
| Stroke | {1.5px / 2px} |
| Corner radius | {consistent with UI radius tokens} |

### Sizing Scale
| Token | Size | Use Case |
|-------|------|----------|
| `sizing.icon.xs` | 12px | Inline indicators |
| `sizing.icon.sm` | 16px | Compact UI, table cells |
| `sizing.icon.md` | 20px | Standard buttons, nav |
| `sizing.icon.lg` | 24px | Feature icons, empty states |
| `sizing.icon.xl` | 32px | Hero features, illustrations |

### Usage Rules
1. Icons accompany labels (never standalone without tooltip/aria-label)
2. Directional icons (arrows, chevrons) mirror in RTL
3. Decorative icons are `aria-hidden="true"`
4. Interactive icons have minimum 44x44px touch target
5. Color inherits from text token (not hardcoded)
```

### Step 6: Voice & Tone

```markdown
## Voice & Tone

### Brand Voice (constant across contexts)
| Dimension | Position | Example |
|-----------|----------|---------|
| {Formal ↔ Casual} | {position} | {sample sentence} |
| {Serious ↔ Playful} | {position} | {sample sentence} |
| {Technical ↔ Simple} | {position} | {sample sentence} |

### Tone Shifts by Context
| Context | Tone Shift | Example |
|---------|-----------|---------|
| Success | Warm, brief | "Done. {Next step}." |
| Error | Empathetic, helpful | "We couldn't {action}. {What to try}." |
| Empty state | Encouraging, guiding | "{What would be here}. {How to add it}." |
| Loading | Calm, informative | "{What's happening}..." |
| Onboarding | Welcoming, minimal | "{What this is}. {One thing to try}." |
| Destructive action | Serious, clear | "{What will happen}. This can't be undone." |

### Microcopy Patterns
| Pattern | Structure | Example |
|---------|-----------|---------|
| Button label | {Verb} + {Object} | "Create Report" |
| Error message | {What happened} + {How to fix} | "Email format isn't valid. Try name@company.com" |
| Empty state | {What belongs here} + {How to start} | "No projects yet. Create your first one." |
| Confirmation | {Consequence} + {Action options} | "Delete this file? You can't undo this. [Delete] [Cancel]" |
| Success | {What happened} + {What's next} | "Report created. View it now?" |
| Tooltip | {What this does} — one sentence | "Filter results by date range" |

### Terminology Governance
| Term to Use | NOT This | Rationale |
|-------------|----------|-----------|
| {preferred} | {alternatives to avoid} | {why — consistency, clarity, audience} |
```

### Step 7: i18n / RTL / Localization (CONDITIONAL)

**Only if conditional feature is active.** Otherwise skip.

```markdown
## Internationalization & Localization

### Supported Locales
| Locale | Direction | Script | Text Expansion |
|--------|-----------|--------|---------------|
| en-US | LTR | Latin | Baseline |
| {locale} | {LTR/RTL} | {script} | {+N%} |

### Design Constraints for i18n
1. All text containers accommodate ≥35% expansion (longest target language)
2. Use CSS logical properties (`margin-inline-start` not `margin-left`)
3. Directional icons mirror in RTL (arrows, progress indicators)
4. Numbers and dates format per locale (never hardcode format)
5. Avoid text in images/icons (untranslatable)
6. String externalization: all UI text reference-able by key

### Locale-Aware Tokens
| Token | LTR | RTL | Notes |
|-------|-----|-----|-------|
| `spacing.inline.start` | left | right | Use logical properties |
| `spacing.inline.end` | right | left | Use logical properties |
```

### Step 8: Compile Token Specification

Consolidate all tokens from Steps 2-7 into a single token specification document following W3C Design Tokens Format:

- Group tokens by category (color, typography, spacing, sizing, etc.)
- Three tiers: Global → Semantic → Component
- Every token has: name, value, type, description
- Format suitable for tool consumption (Style Dictionary, Tokens Studio)

### Step 9: Present for Approval

Present the complete design system:
- Principles (do they resonate?)
- Color system with contrast verification
- Typography with scale
- Spatial system with grid
- Iconography rules
- Voice & tone with patterns
- Token specification overview
- i18n rules (if applicable)

---

## Gate

**Approval required before proceeding to Stage 9.**

User must confirm:
- Design principles are correct and prioritized
- Color system passes contrast checks
- Typography scale is appropriate
- Spatial system / grid is suitable
- Voice & tone matches the product's personality
- Token structure is clear and consumable
- i18n rules are complete (if applicable)

---

## Log

Update `uxd-state.md`:
- Completed Stages: add Stage 8 with date and artifacts (`07_Design_System/` folder)
- Current Stage: 9

Log major decisions (grid size, type scale, color palette source) in Decision Log as `UXD-D-NNN`.

---

## Transition

After gate approval:
```
Stage 8 complete. Design system foundation defined with {N} tokens.

Moving to Stage 9: Component Library Definition. I'll now define
every UI component — its variants, states, interactions, responsive
behavior, and accessibility requirements.
```

Load `design/component-library.md`.
