---
name: pencil-design-skill
description: Design UIs in Pencil (.pen files) and generate production-ready code from them. Triggers on any task involving .pen files, UI prototyping, design system authoring, design-to-code conversion, or Pencil MCP tool usage.
metadata:
  author: CaoPipeline
  version: "3.2.0"
---

# Pencil Design Skill

Design production-quality UIs in Pencil and generate clean code. Two modes:

- **Mode A — Direct file writing**: write `.pen` JSON via `write_to_file` / `replace_in_file`. Always read [`references/pen-format.md`](references/pen-format.md) **before** writing any `.pen` file.
- **Mode B — MCP tool-based**: when Pencil MCP is connected, use `pencil_batch_design`, `pencil_batch_get`, etc. See [MCP tools](#mcp-tool-quick-reference) below.

## When to Use

- Creating/editing `.pen` files (UI screens, components, design systems)
- Converting Pencil designs to React/Vue/Svelte + Tailwind v4 + shadcn/ui code
- Syncing design tokens between Pencil variables and code (`@theme` blocks)

---

## Critical Rules (MUST follow)

1. **Read `pen-format.md` first** before writing any `.pen` file (Mode A) — contains all node types, variables, layout rules, default templates.
2. **Confirm style first** — if user did not specify a style, ask via `ask_followup_question` using the menu in [`styles/style-picker.md`](styles/style-picker.md). Never silently default to Shadcn Dark.
3. **Enforce file split** — count requested artboards before designing:
   - ≤ 3: proceed
   - 4: ask user (keep together vs split)
   - ≥ 5: MUST ask user for split strategy (1/file, 3/file, or 4/file). See [File split policy](#file-split-policy).
4. **Always use variables** — never hardcode colors / radius / fonts. Use `"$--background"`, not `"#09090b"`. If a variable doesn't exist, create it.
5. **Layout integrity is non-negotiable (HIGHEST PRIORITY)** — applies to ALL outputs (PPT slides, web, mobile, components). No content may extend beyond its parent or the artboard. No overlaps. No crooked / misaligned elements. See [`references/layout-integrity.md`](references/layout-integrity.md) + [`references/overflow-prevention.md`](references/overflow-prevention.md). Summary:
   - Every top-level artboard MUST use `"layout": "vertical"` or `"horizontal"` (NOT `"none"`) whenever it holds flowing content. Only use `"none"` for intentional absolute-positioned decoration (cover / hero slides), and in that case every child MUST stay within the artboard rect.
   - Every text node inside an auto-layout parent: `"width": "fill_container"` + `"textGrowth": "fixed-width"`.
   - Every child frame whose content may grow: `"width": "fill_container"` and/or `"height": "fit_content"`. Never fix a width larger than the parent's inner width (parent width − horizontal padding).
   - Artboards have **fixed width + fixed height**; sum of header + body (`fill_container`) + footer MUST equal artboard height. Body area content must never exceed its computed height.
   - Horizontal rows of cards: use `gap` + `width: "fill_container"` on each card. Never hand-pick fixed pixel widths that don't divide evenly.
   - Buttons / badges: use `"fit_content"` (padding `[v,h]`) + `"justifyContent": "center"` + `"alignItems": "center"`. Never fix a width smaller than the label.
   - Absolutely no hand-computed `x`/`y` for content blocks inside an auto-layout parent.
6. **Default UI language is Simplified Chinese** — all user-facing text in `.pen` files uses 简体中文 unless user explicitly requests otherwise. Technical terms / brand names may stay English.
7. **Multi-artboard layout** — when ≥ 2 artboards exist in one file, **default direction is HORIZONTAL** (画板横向排列，x 递增，100 px gap). Each top-level frame needs `x` and `y`.
   - **Default (horizontal)**: y = 0 for all; x = 0, `W+100`, `2(W+100)`, … Example for 1440×900: x = 0, 1540, 3080, 4620.
   - **Vertical (only when user explicitly asks)**: x = 0 for all; y = 0, `H+100`, `2(H+100)`, … Example for 1440×900: y = 0, 1000, 2000, 3000. For PPT (1280×720): y = 0, 820, 1640, 2460.
   - **Always ask the user before designing** (in both English and Chinese), unless they have already specified a direction:
     > Your request has **N** artboards. Arrange them: 您的请求包含 **N** 个画板，排列方向：
     > 1. Horizontal (default) / 横向排列（默认）
     > 2. Vertical / 竖向排列
8. **Icon font family** — always `"iconFontFamily": "lucide"`. No other families.
9. **Reuse assets** — before generating images/logos, search existing nodes (Mode B uses `pencil_batch_get`). Copy & resize, do not regenerate. See [`mcp/image-reuse.md`](mcp/image-reuse.md).
10. **Build section by section in Mode B** — screenshot + layout-check after each section, fix issues before moving on. See [`mcp/screenshot-qa.md`](mcp/screenshot-qa.md).
11. **Mandatory pre-completion layout audit** — before declaring any `.pen` task done, run the [Layout Integrity Checklist](references/layout-integrity.md#pre-completion-checklist). In Mode B: `pencil_snapshot_layout` with `problemsOnly: true` for every artboard must return empty. In Mode A: manually verify each artboard against the checklist.
12. **Code generation requires `frontend-design` skill** if available — load it for aesthetic direction.

---

## File Split Policy

A single `.pen` file must NEVER contain more than 4 artboards (causes performance issues).

When ≥ 4 artboards are requested, ask the user (in both English and Chinese):

> Your request includes **N** artboards. Please choose a splitting strategy:
> 您的请求包含 **N** 个画板。请选择拆分方式：
>
> 1. One artboard per file / 每个画板一个文件
> 2. Max 3 artboards per file / 每个文件最多 3 个画板
> 3. Max 4 artboards per file / 每个文件最多 4 个画板
> 4. No split (not recommended) / 不拆分（不推荐）

Naming: `feature-01.pen`, `feature-02.pen`, … or by logical groups (`feature-onboarding.pen`).

---

## Quick Templates

### Single artboard (Shadcn Dark default)

```json
{
  "version": "2.8",
  "children": [
    {
      "type": "frame", "id": "scrn1", "name": "页面",
      "theme": { "Mode": "Dark" },
      "clip": true, "width": 1440, "height": 900,
      "fill": "$--background", "layout": "vertical",
      "children": [ ... ]
    }
  ],
  "themes": { "Mode": ["Light", "Dark"] },
  "variables": { ...copy from pen-format.md "Shadcn Dark Zinc Variables"... }
}
```

### Multiple artboards — default HORIZONTAL (x 递增, 100 px gap)

```json
{ "type": "frame", "id": "scrn1", "x": 0,    "y": 0, "width": 1440, "height": 900, ... },
{ "type": "frame", "id": "scrn2", "x": 1540, "y": 0, "width": 1440, "height": 900, ... },
{ "type": "frame", "id": "scrn3", "x": 3080, "y": 0, "width": 1440, "height": 900, ... }
```

### Multiple artboards — VERTICAL (only when user picks it, y 递增, 100 px gap)

```json
{ "type": "frame", "id": "scrn1", "x": 0, "y": 0,    "width": 1440, "height": 900, ... },
{ "type": "frame", "id": "scrn2", "x": 0, "y": 1000, "width": 1440, "height": 900, ... },
{ "type": "frame", "id": "scrn3", "x": 0, "y": 2000, "width": 1440, "height": 900, ... }
```

Common screen sizes: Desktop `1440×900` / `1920×1080` · Tablet `768×1024` · Mobile `375×812` / `393×852`.

---

## Default Styles

> Named style specs (Vercel / Linear / Stripe / Notion / Raycast / Supabase / Airtable / Apple) are distilled from <https://getdesign.md/>.

| Trigger | Style file | Notes |
|---|---|---|
| User chose a named style | `styles/style-<name>.md` | Read only the matching file (vercel / linear / stripe / notion / raycast / supabase / airtable / apple) |
| User skipped / chose "default" | Shadcn Dark Zinc | Variables block lives in `pen-format.md`. Dark surfaces `#09090b` / `#18181b`, light text `#fafafa`, subtle borders `#27272a`. |
| PPT / slide deck | [`ppt/presets-ppt.md`](ppt/presets-ppt.md) | 1280×720, blue gradient header, white body |

---

## Workflow Summary

### Mode A — Direct file writing
```
1. Confirm style (Rule 2)         -> ask user OR read styles/style-<name>.md
2. Read pen-format.md             -> mandatory for first .pen task in session
3. Read layout-integrity.md       -> mandatory for EVERY .pen task (Rule 5, 11)
4. Plan layout & artboard count   -> apply file split policy if ≥ 4
   If ≥ 2 artboards, ask arrangement direction (Rule 7) — default HORIZONTAL
5. Write .pen with variables block and auto-layout (NEVER layout:"none" for content)
6. read_lints to validate JSON
7. Manual Layout Integrity Checklist pass (Rule 11) — fix before declaring done
```

### Mode B — MCP tool-based
```
1. Confirm style + load frontend-design skill if available
2. pencil_get_editor_state        -> get .pen schema, current state
3. pencil_batch_get reusable=true -> discover existing components (REUSE > recreate)
4. pencil_get_variables           -> read tokens; pencil_set_variables to create new
5. pencil_find_empty_space        -> place new artboards
6. pencil_batch_design             -> build ONE section at a time
7. pencil_get_screenshot + pencil_snapshot_layout(problemsOnly:true) -> verify each section
8. Fix issues -> re-screenshot -> re-check (verify loop)
9. Final full-file layout audit (Rule 11) -> problemsOnly MUST be empty before declaring done
```

---

## MCP Tool Quick Reference

See [`mcp/mcp-tools.md`](mcp/mcp-tools.md) for the full tool table and Mode B call order.

---

## Code Generation (Pencil → React + Tailwind v4 + shadcn/ui)

**Always do**: TypeScript · React 19 (`ref` as prop, no `forwardRef`) · semantic Tailwind classes (`bg-primary`, never `bg-[#3b82f6]`) · `@theme { --color-* / --radius-* }` blocks · Lucide icons · CVA + `cn()` for variants · OKLCH in tokens.

**Never do**: arbitrary values (`bg-[#fff]`, `rounded-[6px]`, `p-[24px]`) · `tailwind.config.ts` (v4 uses CSS) · `forwardRef` · hardcoded artboard widths in components (use `w-full max-w-7xl`).

Detailed mapping: [`references/codegen-workflow.md`](references/codegen-workflow.md) + [`references/codegen-mapping.md`](references/codegen-mapping.md).

---

## Reference Files (read on demand)

### Always-read (mandatory)

| File | When |
|------|------|
| [`pen-format.md`](references/pen-format.md) | Before writing any `.pen` file |
| [`layout-integrity.md`](references/layout-integrity.md) | Before writing any `.pen` file — hard rules preventing overflow, misalignment, crooked layouts |

### Style references (read 1, after style is selected)

> Source for named style specs: <https://getdesign.md/>

| Style | File |
|-------|------|
| Style picker / menu | [`style-picker.md`](styles/style-picker.md) |
| Vercel | [`style-vercel.md`](styles/style-vercel.md) |
| Linear | [`style-linear.md`](styles/style-linear.md) |
| Stripe | [`style-stripe.md`](styles/style-stripe.md) |
| Notion | [`style-notion.md`](styles/style-notion.md) |
| Raycast | [`style-raycast.md`](styles/style-raycast.md) |
| Supabase | [`style-supabase.md`](styles/style-supabase.md) |
| Airtable | [`style-airtable.md`](styles/style-airtable.md) |
| Apple | [`style-apple.md`](styles/style-apple.md) |
| PPT preset | [`presets-ppt.md`](ppt/presets-ppt.md) |

### Topic references (read on demand)

| File | Topic |
|------|-------|
| [`layout-integrity.md`](references/layout-integrity.md) | **MUST-READ.** Hard rules for all UI / PPT — sizing, auto-layout, no-overflow, no-overlap, no-crooked-alignment, artboard budget math |
| [`overflow-prevention.md`](references/overflow-prevention.md) | Text `fill_container` rules, mobile constraints, fix patterns |
| [`design-tokens.md`](references/design-tokens.md) | Variable system, theming, Tailwind v4 mapping |
| [`component-reuse.md`](references/component-reuse.md) | `ref` instances, `descendants` overrides |
| [`image-reuse.md`](mcp/image-reuse.md) | Search-before-generate, copy vs regenerate |
| [`screenshot-qa.md`](mcp/screenshot-qa.md) | Section-by-section verification (Mode B) |
| [`responsive.md`](references/responsive.md) | Artboard sizes → Tailwind breakpoints |
| [`codegen-workflow.md`](references/codegen-workflow.md) | Full design-to-code workflow |
| [`codegen-mapping.md`](references/codegen-mapping.md) | Tailwind / shadcn quick mapping tables |

> **Output rule**: user-facing design files must always be saved as `<name>.pen` (never `.pen.json` — that suffix is reserved for skill-internal storage).

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hardcoded `#3b82f6` in `.pen` | Use `"$--primary"` |
| Omitting `layout` on frame | Set `"layout": "vertical"` or `"horizontal"` (default is horizontal) |
| Using `"layout": "none"` on a content artboard | Switch to `"vertical"`; reserve `"none"` for intentional absolute decoration (cover backgrounds only) |
| Fixed-width text in auto-layout | Use `"width": "fill_container"` + `"textGrowth": "fixed-width"` |
| Card/content wider than parent inner width | Use `"width": "fill_container"` on every row child; size cards via `gap` on parent |
| Body height overflowing artboard (header + body > artboard) | Use `height: "fill_container"` on the body frame, fixed heights only for header/footer |
| Button with hardcoded width smaller than label | Use `"fit_content"` + `padding: [v, h]` + `justifyContent: "center"` |
| Hand-computed `x`/`y` inside auto-layout parent | Let auto-layout position children; use `gap`/`padding` instead |
| Text touching artboard edges | Apply horizontal padding (desktop 40–64px, tablet 24–32px, mobile 16–20px) |
| Long descriptive IDs | Use 5-char codes: `"btn01"`, `"crd1a"` |
| `bg-[#fff]` in code | Use `bg-background`, `text-foreground` |
| `tailwind.config.ts` | Use CSS `@theme` (Tailwind v4) |
| English UI text | Default to Simplified Chinese |
| Silently using Shadcn Dark | Always ask user for style first (Rule 2) |
| Cramming 5+ artboards in one file | Apply file split policy (Rule 3) |
| Skipping final layout audit | Run Layout Integrity Checklist before declaring done (Rule 11) |

