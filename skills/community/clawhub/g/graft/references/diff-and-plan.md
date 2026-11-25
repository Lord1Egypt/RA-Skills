# Diff and Plan — Comparing Tokens and Building the Change Plan

## Purpose

This reference defines how to compare the local project's current design tokens against the target `{domain}.json` taste profile, and how to format the resulting change plan for user review.

## Diff Logic

### Step 1 — Load the target taste profile

Read `{domain}.json`. The relevant sections are:
- `designMap` — all concrete token values
- `tasteDNA` — the reasoning behind each token choice (needed for change plan justification)

### Step 2 — Category-by-category comparison

For each token category, compare the local project's current values against the target's values. Not all categories will have mismatches — only include categories with actual differences in the change plan.

#### Colors

Compare these roles:
| Role | Local source | Target source |
|------|-------------|---------------|
| Page background | `:root { --background }` or `body { background }` | `designMap.colors.pageBackground` |
| Primary text | `:root { --foreground }` or `body { color }` | `designMap.colors.text[0]` |
| Secondary text | `--muted-foreground` or similar | `designMap.colors.text[1]` (if present) |
| Accent / primary | `--primary` or `--accent` | `designMap.colors.accents[0]` |
| Card background | `--card` or similar | `designMap.colors.backgrounds` (card role) |
| Border color | `--border` or similar | `designMap.colors.borders[0]` |

#### Typography

| Token | Local source | Target source |
|-------|-------------|---------------|
| Display font | `--font-display` or `fontFamily.sans` in Tailwind | `designMap.typography.families` (display role) |
| Body font | `--font-body` or `fontFamily.sans` | `designMap.typography.families` (body role) |
| Mono font | `--font-mono` or `fontFamily.mono` | `designMap.typography.families` (mono role) |
| Size scale | Various `font-size` values | `designMap.typography.sizeScale` |
| Weights | Various `font-weight` values | `designMap.typography.weights` |
| Line heights | Various `line-height` values | `designMap.typography.lineHeights` |

#### Spacing

| Token | Local source | Target source |
|-------|-------------|---------------|
| Base unit | Spacing scale pattern | `designMap.spacing.unit` |
| Section gaps | Section margin/padding values | `designMap.spacing.sectionGaps` |

#### Radii

| Token | Local source | Target source |
|-------|-------------|---------------|
| Default radius | `--radius` or `borderRadius` in Tailwind | `designMap.radii` (sorted by count) |

#### Shadows

| Token | Local source | Target source |
|-------|-------------|---------------|
| Shadow definitions | `--shadow-*` or `boxShadow` in Tailwind | `designMap.shadows` |

#### Motion

| Token | Local source | Target source |
|-------|-------------|---------------|
| Transition duration | `--transition-duration` or `transitionDuration` | `designMap.motion.dominantDuration` |
| Easing | `--easing` or `transitionTimingFunction` | `designMap.motion.dominantEasing` |

### Step 3 — Classify each mismatch

For each mismatch found:

1. **Is the difference significant?** A 1px radius difference may not matter. A color hue shift of >30° is significant. Use judgment but document the reasoning.

2. **Can the target value be adopted directly?** Some target values may not work in the local context (e.g., dark-mode colors applied to a light-mode project without dark-mode support).

3. **What taste principle justifies this change?** Find the relevant principle in `tasteDNA` and cite it. If no principle directly applies, the change may be cosmetic-only — still include it but note that it's a token match without taste reasoning.

## Change Plan Format

Produce the plan grouped by token category. Each change gets one row:

```markdown
## Change Plan — Grafting {domain} taste onto {project}

### Summary
- **X changes** across **Y files** in **Z token categories**
- Primary taste principle being applied: "{strongest principle trigger + decision}"

### Colors ({N} changes)
| File | Token/Property | Current | Proposed | Reasoning |
|------|---------------|---------|----------|-----------|
| `globals.css` | `--background` | `0 0% 100%` | `0 0% 4%` | Source uses near-black (#0A0A0B) page bg; dark environment is foundational to their depth-through-borders principle (borders at rgba(255,255,255,0.08) only work on dark surfaces) |

### Typography ({N} changes)
| File | Token/Property | Current | Proposed | Reasoning |
|------|---------------|---------|----------|-----------|
| `globals.css` | `--font-sans` | `Inter` | `Inter` | ✓ Already matches |

### [continue for each category with changes...]

### No Changes Needed
- [list categories where local tokens already match the target]

### Skipped (Token Boundary Violation)
- [list any proposed changes that were rejected by the token-boundary guard, with explanation]
```

## Rules for Change Plan Reasoning

1. **Every reasoning cell must cite a specific taste principle or measurement** from the target profile. "Looks better" is not a reason. "Matches source's tight-heading-rhythm pattern (1.1 line-height on all headings, source Step 2 Pattern #3)" is a reason.

2. **Use before/after values**, not just the proposed value: "Current 12px → Proposed 2px" is more useful than just "2px".

3. **Anti-slop check applies**: No "now it looks more modern/polished/clean." Always: "now the border-radius signals precision, matching {source}'s restraint principle (2px across 47 elements)."

4. **Flag uncertainty**: If a change might have unintended side effects (e.g., changing a primary color that's also used as a status indicator), note it: "⚠️ This color may also be used for success/active states — verify no semantic collision."

5. **Group changes logically**: Colors together, typography together. This lets the user approve/reject by category if they want partial application.

## After User Review

The user may:
1. **Approve all** → proceed to Phase 4 (Apply)
2. **Approve some, reject others** → apply only approved changes
3. **Reject all** → stop, no changes made
4. **Ask for modifications** → adjust the plan and re-present

Wait for explicit approval. Never auto-apply.
