---
name: graft
description: >-
  Apply a previously extracted design taste profile to a local project. Given a
  {domain}.json from a prior /extract run and the user's own project, diffs the
  project's current design tokens against the target taste, proposes a change plan
  with per-line reasoning, and — on explicit approval — applies token-level edits
  only. Never touches content, copy, layout structure, or business logic. Operates
  on design tokens exclusively: color values, spacing scale, border-radius, shadows,
  typography (font-family, weight, size, line-height), and transition/easing values.
  Triggers on '/graft <domain>', '/graft <path-to-json>', 'make my project feel like X',
  'apply the taste I extracted to my project', 'replace my color theme with X's',
  'port the design from X to my project'. If no prior extract exists for the
  referenced domain, tells the user to run /extract first.
compatibility: >-
  Works in any environment. No MCP or browser needed — operates entirely on local
  files. Requires a {domain}.json from a prior /extract run.
metadata:
  version: "1.0.0"
  author: Built from PRD
  license: MIT
---

# Graft — Apply Extracted Design Taste to a Local Project

This skill takes a previously extracted taste profile (`{domain}.json` from `/extract`) and applies it to the user's own local project. It's designed for the common case of an AI-coded ("vibe coded") project that works functionally but has generic/inconsistent design defaults (Inter font, purple gradient, arbitrary radii, default shadows) and needs its visual taste replaced with a deliberate one.

## When to activate

Trigger this skill when the user wants to apply a previously extracted design taste to their project:

- Explicit: `/graft <domain>` or `/graft <path-to-json>`
- Natural language: "make my project feel like linear.app", "apply the taste I extracted", "replace my color theme with X's", "port the design from X to my project"
- Follow-up after extract: "now apply it", "use those tokens in my project"

If no `{domain}.json` exists for the referenced domain, tell the user: "I need a taste profile to graft from. Run `/extract <url>` first to generate one, then try `/graft <domain>` again." Alternatively, offer to run `/extract` as a sub-step (with permission, since it invokes a separate skill).

Do NOT activate for: "redesign my project" (too broad — graft is token-level only), "build a new project like X" (use extract + manual design, not graft), "fix my CSS" (debugging, not taste application).

---

## Hard Boundary — Token-Level Only

**This is non-negotiable. Read `references/token-boundary-guard.md` before any editing.**

`graft` operates on **design tokens only**:

### ✅ Token-level (allowed)
- Color values (hex, rgb, hsl, CSS custom properties)
- Spacing values (margin, padding, gap — the values, not the properties)
- Border-radius values
- Box-shadow / border values
- Typography: font-family, font-weight, font-size, line-height, letter-spacing
- Transition/animation: duration, easing, delay values

### ❌ NOT token-level (forbidden)
- Rewriting copy, text content, or microcopy
- Changing component structure, layout (flexbox/grid direction), or DOM hierarchy
- Adding, removing, or restructuring HTML/JSX elements
- Touching business logic, data fetching, state management, or routing
- Deleting or renaming files outside of style/token config files
- Adding new components or removing existing ones
- Changing responsive breakpoints or layout strategies

### Guard step

Before writing ANY change, classify each proposed edit:
1. Is it modifying a **value** (color, size, weight, radius, shadow, easing)? → ✅ Allowed
2. Is it modifying a **property** or **structure** (adding `display: flex`, changing `grid-template-columns`, wrapping in a new div)? → ❌ Refused
3. Is the file a **style/token config** file (CSS, Tailwind config, theme file)? → ✅ Likely allowed
4. Is the file a **component/logic** file with inline styles mixed in? → ⚠️ Prefer extracting to CSS variables over editing inline. Flag for user review.

If ANY proposed edit fails this classification, remove it from the change plan and note why.

---

## Workflow

### Phase 1 — Inventory the Local Project

**Read:** `references/inventory-project.md`

Scan the project for its current design tokens. Detect the stack:

1. **Look for centralized token sources:**
   - `globals.css`, `global.css`, `index.css`, `variables.css`, `theme.css`
   - CSS files with `:root` or `--` custom properties
   - `tailwind.config.js`, `tailwind.config.ts`, `tailwind.config.mjs`
   - Theme files: `theme.ts`, `theme.js`, `tokens.json`
   - shadcn: `components.json` + `globals.css` with HSL variables
   - CSS-in-JS: `styled-components` ThemeProvider, `emotion` theme objects

2. **Extract current token values** using the same categories as `/extract` Step 1:
   - Colors (backgrounds, text, accents, borders)
   - Typography (families, sizes, weights, line-heights)
   - Spacing (scale, section gaps)
   - Radii
   - Shadows
   - Motion (transitions, easings)

3. **Ask user to confirm** if the detected stack is ambiguous:
   > "I detected [plain CSS / Tailwind / CSS-in-JS / shadcn]. Is that correct, or is there a different token source I should look at?"

### Phase 2 — Diff Against Target

**Read:** `references/diff-and-plan.md`

Load the target `{domain}.json`. For each token category:

1. Compare current project value(s) against target value(s)
2. For every mismatch, don't just note the numbers — **state the reasoning** from the target's Taste DNA

Example diff:
> Your border-radius is `12px` everywhere; target uses `2px` on 47/47 interactive elements. The source taste principle is "precision-over-softness" — 2px signals engineering tooling rather than consumer friendliness. **Recommend**: adopt `2px` for buttons and inputs, `4px` max for cards.

### Phase 3 — Change Plan (Dry Run)

**Always show this before any edit. Nothing is written yet.**

Produce an itemized plan grouped by token category:

```
## Change Plan — Grafting {domain} taste onto {project}

### Colors
| File | Token/Property | Current | Proposed | Reasoning |
|------|---------------|---------|----------|-----------|
| globals.css | --color-bg | #ffffff | #0A0A0B | Source uses near-black bg; dark page background creates the low-contrast-text-on-dark environment that their depth principle depends on |
| globals.css | --color-accent | #7c3aed | #4F46E5 | Source restricts accent to CTAs only at HSL(239, 84%, 67%); lower saturation than your current purple signals restraint |

### Typography
| File | Token/Property | Current | Proposed | Reasoning |
|------|---------------|---------|----------|-----------|
| globals.css | --font-display | 'Inter' | 'Inter' | ✓ Already matches — no change needed |
| globals.css | --font-size-h1 | 3rem | 3rem / 1.1 lh | Line-height tightening from 1.5 to 1.1 — source's "tight heading rhythm" pattern |

### [more categories...]

### Skipped (outside token boundary)
- Component X uses inline `style={{ borderRadius: 12 }}` — recommend extracting to CSS variable rather than editing JSX inline
- Layout grid in `page.tsx` uses `grid-cols-3` — this is structural, not a token change
```

Present this to the user and **wait for explicit approval** before proceeding.

### Phase 4 — Apply (After Approval Only)

Apply changes with these preferences:

1. **Prefer centralized files** — edit CSS custom properties in `globals.css`, Tailwind config `theme.extend`, or theme objects. This keeps changes auditable and reversible.

2. **If no centralized token layer exists**, offer to create one:
   > "Your project doesn't have centralized CSS custom properties. I can create them in `globals.css` and update your components to reference them. This is a slightly larger change — want me to proceed?"
   Get separate confirmation for this.

3. **Never scatter edits** across many component files if a centralized option exists.

4. **Preserve existing structure** — don't reorganize CSS files, don't reorder properties, don't change formatting conventions.

### Phase 5 — Report

After applying changes, summarize:

1. **Files modified** — list each file and what changed
2. **Token categories touched** — colors, typography, spacing, radii, shadows, motion
3. **Strongest taste principle applied** — one-line callback to the source taste DNA
4. **What was skipped** — any proposed changes that were outside the token boundary or that the user declined
5. **Anti-slop check** — confirm the report itself passes the grep test (see `references/anti-slop-wordlist.md`)

Example summary line:
> "Your project now uses {domain}'s 2px radius system and restrained single-accent palette. The strongest signal change: border-radius went from mixed 8/12/16px to uniform 2px across 23 elements, matching the source's precision-over-softness principle."

NOT: "Your project now looks more modern and polished." (This would fail the anti-slop check.)

---

## Known Limitations

- **Inline styles**: Projects with heavily inlined styles (e.g., `style={{ color: 'red' }}` scattered through JSX) cannot be safely grafted without first extracting tokens to CSS variables. The skill will flag this and propose the extraction as a prerequisite step.
- **CSS-in-JS complexity**: Styled-components/emotion theme objects can be deeply nested. The inventory phase may miss tokens buried in complex theme structures — the user should verify the detected tokens are complete.
- **Partial application**: If the source taste profile has tokens the target project doesn't use (e.g., source has a mono font, project has no code blocks), those tokens are noted as "not applicable" rather than force-applied.
- **Reversibility**: Changes to centralized token files are easy to revert (`git diff`/`git checkout`). Scattered inline edits are harder to undo — another reason the skill prefers centralized files.
- **No visual verification**: The skill cannot take a screenshot of the local project to verify the grafted result looks correct. The user should preview the result and report any issues.
