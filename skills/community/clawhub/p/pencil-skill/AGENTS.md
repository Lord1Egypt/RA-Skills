# Pencil Skill — Agent Guide

> This document guides AI agents in creating and editing `.pen` design files.
> For full rule details, examples, and edge cases, see individual files in `rules/`.

## Purpose & Scope

- This is a **guide document**, not a full rule compilation.
- Use it for fast orientation, then open each rule file for implementation details.
- Current rule count: **41** files across 8 categories.
- Source of truth: `rules/*.md`.

## Quick Start

1. Read current structure: `node scripts/read-tree.mjs <file.pen> --depth 2`
2. Search reusable components first: `node scripts/search-nodes.mjs <file.pen> --reusable`
3. Review variables/themes: `node scripts/get-variables.mjs <file.pen>`
4. Apply edits in batches: `node scripts/batch-design.mjs <file.pen> --ops ...`
5. Validate immediately: `node scripts/validate-pen.mjs <file.pen>`

## Standard Editing Workflow

```bash
# 1) Inspect
node scripts/read-tree.mjs assets/example-card.pen --depth 2

# 2) Find reusable parts
node scripts/search-nodes.mjs assets/example-card.pen --reusable

# 3) Edit
node scripts/batch-design.mjs assets/example-card.pen --ops '[{"op":"update","id":"title","props":{"content":"Updated"}}]'

# 4) Validate
node scripts/validate-pen.mjs assets/example-card.pen
```

## Critical Rules (Must Follow)

### Layout & Overflow
> Priority: **CRITICAL** · Prevent overlap, clipping, and broken responsive behavior.

| Rule | File | Summary |
|------|------|---------|
| Auto Layout Required | `rules/layout-auto-layout.md` | All container frames must specify the layout attribute. If layout: "none", children overlap with absolute coordinates, and the layout will be broken when content is ch... |
| Top-level canvas placement — no layer overlap | `rules/layout-canvas-placement.md` | All top-level nodes in root children (reusables, showcase frames, and utility canvases) must define explicit x and y coordinates and must not overlap each other. In .p... |
| Prevent overlap between elements | `rules/layout-no-overlap.md` | The most common causes of sibling elements overlapping in a three-column layout are overuse of fit_content, omission of gap, unverified width summation, and absolute c... |
| Prevent Text Overflow | `rules/layout-overflow.md` | Text nodes must have the textGrowth property specified. If you only have a fixed width and no textGrowth, long text will either spill out of the container or be trunca... |
| Responsive via Separate Frames | `rules/layout-responsive.md` | Since .pen does not have a CSS media query, the responsive version creates and expresses an independent frame for each resolution: 375 (mobile), 768 (tablet), and 1440... |
| Sizing Mode by Context | `rules/layout-sizing.md` | Depending on the role of the element, different size modes must be applied. The principle is that the screen frame is fixed px, section/row is fill_container, text blo... |
| Gap/Padding Only — No Spacer Frames | `rules/layout-spacing-consistency.md` | Never use empty frames (spacers) to create spacing. All spacing must be expressed using only the parent frame's gap or padding properties. Empty spacers increase child... |
| Z-Order via Children Order | `rules/layout-z-order.md` | In .pen, z-order is determined by the order of the children array. Children that come later render on top. Overlays, badges, modal backdrops, and similar layers must b... |

### Design Tokens
> Priority: **CRITICAL** · All reusable values must flow through variables and themes.

| Rule | File | Summary |
|------|------|---------|
| Token Naming Convention | `rules/token-naming.md` | All design tokens should use dot-separated naming in the $category.purpose.variant format. Raw names like $blue or meaningless names like $padding1 are forbidden. Prop... |
| No Hardcoded Values — Use Tokens | `rules/token-no-hardcode.md` | Use token references ($) for all design properties, including fill, fontSize, padding, gap, and cornerRadius. If you write literal values like "#3B82F6", 16, or "bold"... |
| Use Semantic Color Tokens | `rules/token-semantic-colors.md` | Color tokens must use semantic names like $color.primary, $color.surface, $color.foreground, not raw palette names like $color.blue500. Required semantic colors: backg... |
| Theme Axes Required (light/dark) | `rules/token-theme-required.md` | When declaring variables, you must define a themes axis and support at least light and dark modes. If only single values exist without themes, dark-mode migration beco... |
| Token Registration Workflow | `rules/token-workflow.md` | You must register tokens before getting started with design. Workflow: ① Register tokens with set-variables → ② Confirm registration with get-variables → ③ Reference $... |

### Anti-AI Aesthetic
> Priority: **HIGH** · Avoid generic AI-looking visual patterns and copycat styling.

| Rule | File | Summary |
|------|------|---------|
| Anti-AI Aesthetic Checklist | `rules/aesthetic-checklist.md` | After completing the design, it must pass the checklist below. If even one item fails, revise that item. |
| Avoid AI-looking Color Choices | `rules/aesthetic-color.md` | primary: #3B82F6 (Tailwind blue-500) and purple→blue linear gradients are already saturated defaults from AI design tools. Define brand-specific colors, use warm gray... |
| Real Content — No Filler Copy | `rules/aesthetic-content.md` | "Your Amazing Feature," "10K+ Users," repeating "Learn More" three times, and "Lorem ipsum" are all signals of content-less AI design. Use real service names, specific... |
| No Gratuitous Decoration | `rules/aesthetic-decoration.md` | Blurred gradient blobs in the background, lg shadow on every card, and meaningless pattern overlays are stereotypical decorations of AI-generated designs. Create visua... |
| Break AI Layout Patterns | `rules/aesthetic-layout.md` | The pattern of centering all elements and repeating three rows of cards with equal padding is typical of AI-generated design. Add variation to the visual flow by using... |
| Aesthetic Typography — Display + Body Pairing | `rules/aesthetic-typography.md` | It is a typical AI pattern to use Inter in all text and vary only the fontSize. Combine display fonts (Playfair Display, Fraunces, etc.) with body fonts (Source Sans 3... |

### Component System
> Priority: **HIGH** · Build reusable primitives and compose via ref + descendants + slot.

| Rule | File | Summary |
|------|------|---------|
| Atomic Design Hierarchy | `rules/component-atomic.md` | Components must be combined in the following hierarchy: Atom → Molecule → Organism → Template. Make Atoms (buttons, icons, badges) reusable first, combine them with re... |
| Component Slash Naming | `rules/component-naming.md` | Every reusable component is named two fields: id: slug without slash (btn-primary, card-default, nav-topbar) name: Figma standard slash naming ("Button/Primary", "Card... |
| Search Before Create | `rules/component-reuse-first.md` | Before creating a new component or element, you must search for existing reusables with search-nodes --reusable. If you already have btn-primary and create a new butto... |
| Declare Content Slots | `rules/component-slot.md` | Components whose content changes (cards, modals, list items, etc.) must declare their content area as slot. If you hard-code the title and description directly inside... |
| Variants as Separate Reusables | `rules/component-variant.md` | Variants with different styles, such as Primary/Secondary/Ghost variants of buttons, are implemented separately as reusable. It is prohibited to include conditional br... |

### Typography
> Priority: **MEDIUM** · Use readable scale, rhythm, and hierarchy for all text content.

| Rule | File | Summary |
|------|------|---------|
| Line Height by Text Size | `rules/typo-line-height.md` | Line height should vary by text size. As a rule: large display text tight (1.1), body text loose (1.6), captions medium (1.4). If all text uses lineHeight: 1.5, displa... |
| Font Pairing — Display + Body | `rules/typo-pairing.md` | Combining a Display font (hero/headings) with a Body font (body/UI) creates visual hierarchy and brand character. Using Inter everywhere is a common AI-pattern default... |
| Minimum 6-Step Type Scale | `rules/typo-scale.md` | Define type scale with at least 6 steps (xs, sm, base, lg, xl, 2xl, 3xl, 4xl, 5xl). Arbitrary values like 12, 15, 19, 23 lack proportional hierarchy and look visually... |
| Text Column Width & Alignment Rules | `rules/typo-text-rules.md` | Optimal readability for body text is about 65–75 characters per line. If widthMode: "fill_container" text stretches across full 1440px width, lines become too long to... |
| Font Weight by Role | `rules/typo-weight.md` | Font weights should be differentiated by role. Basic rule: body → 400, UI label/caption → 500, subheading/card title → 600, large heading/hero → 700. If everything is... |

### Color System
> Priority: **MEDIUM** · Enforce semantic color usage, accessibility, and dark mode parity.

| Rule | File | Summary |
|------|------|---------|
| WCAG 2.1 AA Contrast Ratio | `rules/color-accessibility.md` | Plain text requires a contrast ratio of 4.5:1 or higher compared to the background, and large text (18px bold or higher) requires a contrast ratio of 3:1 or higher. Wr... |
| Dark Mode — No Pure Black/White | `rules/color-dark-mode.md` | In dark mode, it is prohibited to use #000000 for background and #FFFFFF for text. Pure black and white combinations have too much contrast, which creates glare and le... |
| 60-30-10 Color Ratio | `rules/color-ratio.md` | Color distribution follows the 60-30-10 ratio. 60% neutral (background, surface), 30% secondary (section background, secondary UI), 10% primary accent (CTA button, lin... |
| 3-Layer Color System | `rules/color-semantic.md` | The color system is designed in three layers. ① Primitive (primary color palette: $palette.teal.500) → ② Semantic (role-based: $color.primary) → ③ Component (Component... |

### Spacing System
> Priority: **MEDIUM** · Keep spacing decisions consistent and token-driven.

| Rule | File | Summary |
|------|------|---------|
| 4pt/8pt Grid System | `rules/spacing-8pt-grid.md` | All gap, padding, and margin values must be multiples of 4. Allowed values: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96. Arbitrary odd values like gap: 13 or padding:... |
| Forbidden Spacing Patterns | `rules/spacing-forbidden.md` | The three patterns below are strictly forbidden: (1) empty frames as spacers, (2) arbitrary values not multiples of 4 (13, 30, 7, etc.), and (3) placing children direc... |
| Padding by Element Type | `rules/spacing-padding.md` | Padding should vary by element type. Small elements (buttons) need small padding, containers (cards) medium, sections large, and page-level containers largest. If ever... |
| Proximity — Varied Gap by Relationship | `rules/spacing-proximity.md` | Set small gaps between related elements, medium gaps between groups, and large gaps between sections. If you use gap: 16 everywhere, icon-label spacing looks the same... |

### Showcase & Style Guide
> Priority: **MEDIUM** · Use a pre-design process and finish with system-level QA checks.

| Rule | File | Summary |
|------|------|---------|
| Leverage Existing Design System | `rules/showcase-design-system.md` | Before starting design work, always search existing components with search-nodes --reusable and reuse them. If Button, Card, Nav, and others already exist, recreating... |
| Final Design Review Checklist | `rules/showcase-final-checklist.md` | After completing the design, you must pass the checklist below. If any item fails, fix it before submission. |
| Create Showcase Frame First | `rules/showcase-frame.md` | For a new project without an existing design system, create the showcase frame before building real pages. The showcase frame gathers the color palette, type scale, an... |
| Pre-Design Planning | `rules/showcase-pre-design.md` | Before starting design, define goals, audience, and tone, collect references, and establish a style guide. Skipping this step often produces generic AI-style design or... |

## 5 Critical Rules (Never Violate)

1. **`textGrowth` required** — Set `textGrowth` before using width/height behavior on text nodes.
2. **`ref` target must exist** — Every `ref` must point to an existing reusable component ID.
3. **No duplicate IDs** — Every node ID must be unique inside a `.pen` file.
4. **Validate after every edit** — Always run `node scripts/validate-pen.mjs` before finishing.
5. **Component reuse first** — Search existing reusable components before creating new ones.

## Property Aliases

- `fill` / `fills` — both accepted
- `stroke` / `strokes` — both accepted
- `effect` / `effects` — both accepted

## CLI Tools Reference

### Read Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `read-tree.mjs` | Print node tree structure | `node scripts/read-tree.mjs file.pen [--depth 2] [--id nodeId]` |
| `search-nodes.mjs` | Search nodes/components | `node scripts/search-nodes.mjs file.pen --type frame [--reusable] [--name regex]` |
| `get-variables.mjs` | View variables/themes | `node scripts/get-variables.mjs file.pen [--format json]` |
| `find-space.mjs` | Find empty-space coordinates | `node scripts/find-space.mjs file.pen --width 300 --height 200` |

### Write Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `batch-design.mjs` | Insert/update/delete/move/copy nodes | `node scripts/batch-design.mjs file.pen --ops "[...]"` |
| `replace-props.mjs` | Bulk property replacement | `node scripts/replace-props.mjs file.pen --match "{...}" --replace "{...}"` |
| `set-variables.mjs` | Add/update variables | `node scripts/set-variables.mjs file.pen --var "name=type:value"` |

### Validation Tool

| Script | Purpose | Usage |
|--------|---------|-------|
| `validate-pen.mjs` | Structural validation + lint | `node scripts/validate-pen.mjs file.pen` |

## Schema Quick Reference

| Node Type | Required Fields | Important Notes |
|-----------|------------------|-----------------|
| Root Document | `version`, `children` | `themes` and `variables` optional but recommended. |
| `frame` | `type`, `id` | Use `layout` (`vertical`/`horizontal`) for container behavior; supports `slot`. |
| `group` | `type`, `id` | Visual grouping only; avoid for layout logic. |
| `text` | `type`, `id`, `content` | Set `textGrowth` before fixed sizing behavior. |
| `rectangle` | `type`, `id` | Supports fill/stroke/effects; use tokens for values. |
| `ellipse` | `type`, `id` | Use tokens for size and color; keep naming semantic. |
| `line` | `type`, `id` | Prefer tokenized stroke thickness/color. |
| `polygon` | `type`, `id` | Keep geometry and style tokenized. |
| `path` | `type`, `id` | Validate path edits after any scripted change. |
| `icon_font` | `type`, `id` | Use supported families only (lucide, feather, Material Symbols, phosphor). |
| `ref` | `type`, `id`, `ref` | `ref` value must target an existing reusable component ID. |
| `note` / `prompt` / `context` | `type`, `id` | Use for annotations and guidance, not visual structure. |

## Batch Operation Reference

| Operation | Required Keys | Description |
|-----------|----------------|-------------|
| `insert` | `op`, `parentId`, `node` | Insert a new node into parent children. |
| `update` | `op`, `id`, `props` | Deep-merge patch into existing node. |
| `delete` | `op`, `id` | Remove node and descendants. |
| `move` | `op`, `id`, `toParentId` | Move node to another parent (`index` optional). |
| `copy` | `op`, `id`, `newId` | Duplicate node tree; ensure IDs remain unique. `toParentId` optional (defaults to `root`). |

## Validation Checklist

- [ ] Root has `version` and `children`
- [ ] No duplicate IDs
- [ ] No `/` in node IDs
- [ ] Every `ref` points to an existing reusable component
- [ ] `text` nodes with width/height behavior have `textGrowth`
- [ ] Variable references (`$...`) resolve to actual keys
- [ ] `node scripts/validate-pen.mjs <file.pen>` passes

## References

- Schema: `references/pen-schema.json`
- Types: `references/pen-types.ts`
- Mapping: `references/pen-to-tailwind.md`
- Patterns: `references/component-patterns.md`
- Example: `assets/example-card.pen`

---

Need full details for any rule? Open the corresponding file in `rules/`.
