# Design System Components

> **Applies to**: Mode A (Direct File Writing) + Mode B (MCP Tools)
> **See also**: [design-tokens.md](design-tokens.md) · [codegen-workflow.md](codegen-workflow.md)

---

## Core Principle: Reuse Over Rebuild

> **Inspired by Stitch** — Great design systems are built on **component thinking**: identify reusable UI elements, organize them into a shared component library, and maintain consistency through instance inheritance rather than redundant rebuilds. Stitch treats this as a fundamental workflow assumption.

Rebuilding existing components from scratch causes:

- Design inconsistencies (subtle padding, color, font-weight differences)
- Design system updates failing to propagate to manually rebuilt elements
- Code generation producing duplicate, non-DRY components
- File size bloat from redundant nodes

---

## Workflow: Discover and Use Components

### Step 1 — List All Reusable Components

**Run this at the start of every design task**:

```
pencil_batch_get({
  filePath: "path/to/file.pen",
  patterns: [{ reusable: true }],
  readDepth: 2,
  searchDepth: 3
})
```

Example result:

```json
{
  "id": "btn-primary",
  "name": "Button",
  "type": "frame",
  "reusable": true,
  "children": [
    { "id": "btn-label", "type": "text", "content": "Button" }
  ]
}
```

### Step 2 — Identify the Right Component

Evaluate reusability along these dimensions:

| Dimension | How to Judge |
|-----------|-------------|
| **Name match** | Button / Card / Input / NavBar / Avatar, etc. |
| **Structure match** | Need a card with image + title + description? Find a component with that structure. |
| **Variant match** | Design system may have multiple variants (Button Primary / Secondary) |

### Step 3 — Insert as a Ref Instance

Use the component's `id` as the `ref` value:

```javascript
btn=I("parentFrameId", { type: "ref", ref: "btn-primary", width: "fill_container" })
```

This creates a connected instance. Edits to the main component automatically update all instances.

### Step 4 — Customize via Descendants

Override specific properties on descendant paths:

```javascript
// Change button label text
U(btn+"/btn-label", { content: "Submit" })

// Deep nested path
U(btn+"/icon-container/icon", { iconFontName: "check" })
```

### Step 5 — Replace Slot Content

When a component has placeholder/slot areas, use Replace to swap content:

```javascript
newContent=R(btn+"/content-slot", { type: "text", content: "Custom content" })
```

---

## When to Create a New Component

Only create a new component from scratch when:

1. After checking `reusable: true`, **no similar component exists**
2. The existing component is **structurally different** (not just a color or text change)
3. You are building a **brand-new design system** (empty file)

When creating, set `reusable: true` to enable future reuse.

---

## Pre-Design Checklist

- [ ] Ran `pencil_batch_get` with `{ reusable: true }` to list all components?
- [ ] Checked whether these exist: buttons, inputs, cards, navbars, headers, footers, modals, badges, avatars, table rows?
- [ ] Inserting as `ref` instances (not rebuilding the structure)?
- [ ] Customizing instances via `U()` on descendant paths (not replacing the whole component)?

---

## Common Design System Components Quick Reference

| Need | Search for names containing |
|------|-----------------------------|
| Button | button, btn, cta |
| Text input | input, field, text-field |
| Card | card, tile, panel |
| Navigation | nav, navbar, sidebar, menu |
| Header | header, topbar, appbar |
| Footer | footer, bottom-bar |
| Modal/Dialog | modal, dialog, sheet |
| Badge/Tag | badge, tag, chip, label |
| Avatar | avatar, profile-pic |
| Table row | row, table-row, list-item |
| Icon | icon, symbol |
| Checkbox/Radio | checkbox, radio, toggle, switch |
| Select/Dropdown | select, dropdown, picker |
| Tabs | tab, tab-bar, segment |

---

## See Also

- [design-tokens.md](design-tokens.md) — Use variables when styling component instances
- [codegen-workflow.md](codegen-workflow.md) — Map reusable components to shadcn/ui
- [codegen-mapping.md](codegen-mapping.md) — Pencil component → shadcn/ui mapping table
