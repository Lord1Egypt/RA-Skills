# Layout and Text Overflow

> **Applies to**: Mode A (Direct File Writing) + Mode B (MCP Tools)
> **See also**: [layout-integrity.md](layout-integrity.md) — the authoritative hard-rules document for ALL layout correctness (sizing, alignment, no-overlap, no-crooked). This file is a focused reference for **text/content overflow** specifically.
> **Also**: [screenshot-qa.md](../mcp/screenshot-qa.md) · [responsive.md](responsive.md)

---

## Why Overflow Is the Highest-Priority Defect

Text and content extending beyond their container or artboard is the most common and most visible design defect:

- Text gets clipped and becomes unreadable
- Mobile layouts break apart
- Generated code requires manual overflow fixes
- Creates an unprofessional, broken visual impression

Mobile screens (375–393px wide) are the most overflow-prone — handle with extra care.

---

## Core Principle: Responsive Layout Awareness

> **Inspired by Stitch** — Stitch automatically builds **responsive grids** when generating UI, ensuring layouts work at every screen size. The equivalent in Pencil: always use `fill_container` instead of fixed widths, use `gap` instead of margin hacks, and use `padding` to keep content away from edges.

---

## Prevention Strategy

### Text Elements

1. **Always set text width to fill its parent**

   ```javascript
   text=I(container, { type: "text", content: "Long text...", width: "fill_container" })
   ```

2. **Use the right text properties**
   - Text that should truncate (card titles, list items): set `maxLines`
   - Long paragraphs: let them wrap naturally within the container
   - Overly long headings: wrap or truncate with ellipsis

3. **Never** apply a fixed pixel width wider than the parent container on text nodes

### Container Frames

1. **Use auto-layout** (`layout: "vertical"` or `"horizontal"`) so children flow naturally

2. **Constrain child width to parent**

   ```javascript
   child=I(parent, { type: "frame", width: "fill_container", layout: "vertical" })
   ```

3. **Set padding on containers** to prevent content from touching edges

   ```javascript
   U("parentId", { padding: 16 })
   // Or per-side: paddingLeft, paddingRight, paddingTop, paddingBottom
   ```

4. **Use `gap` for spacing between children** — never use margin hacks

   ```javascript
   U("parentId", { layout: "vertical", gap: 12 })
   ```

### Mobile Screens (375–393px)

Mobile is the most overflow-prone context. Extra rules:

| Element | Requirement |
|---------|-------------|
| Screen frame | Width must exactly match the target width (e.g. 375px) |
| Direct children | `width: "fill_container"` + horizontal padding 16–20px |
| Text nodes | Always `width: "fill_container"`, never wider than ~335px (375 - 2×20) |
| Images | Constrain to container width or use `width: "fill_container"` |
| Horizontal scroll areas | Only use intentionally (e.g. carousels) — never by accident |

### Ref Component Instances

```javascript
// When an instance should fill its parent, set fill_container
card=I(container, { type: "ref", ref: "CardComponent", width: "fill_container" })
```

Verify that the component's internal layout can adapt to varying widths.

---

## Detection: Post-Build Verification

After completing each section, immediately run an overflow check:

```
pencil_snapshot_layout({
  filePath: "path/to/file.pen",
  parentId: "screenId",
  maxDepth: 3,
  problemsOnly: true
})
```

Returns nodes with layout problems:

| Problem Type | Meaning |
|-------------|---------|
| Clipped | Child node extends beyond parent container bounds |
| Overlapping | Sibling nodes unintentionally overlap |
| Overflow | Content is wider or taller than its container |

---

## Problem → Fix Quick Reference

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Text clipped horizontally | Text has a fixed width | `width: "fill_container"` or reduce font size |
| Text clipped vertically | Parent has a fixed height | Increase height, switch to auto-height, or set `maxLines` |
| Child wider than parent | Child uses a fixed width | Change to `width: "fill_container"` |
| Children overlapping | Parent frame has no layout | Add `layout: "vertical"` or `"horizontal"` |
| Content outside artboard | Width/padding too large | Reduce widths, verify all descendants fit within screen width |

---

## Common Fix Snippets

```javascript
// Text overflowing parent
U("textNodeId", { width: "fill_container" })

// Children overflowing frame
U("parentFrameId", { layout: "vertical", gap: 8 })
U("child1Id", { width: "fill_container" })
U("child2Id", { width: "fill_container" })

// Content touching screen edges
U("contentContainerId", { paddingLeft: 16, paddingRight: 16 })

// Long title truncated to single line
U("titleTextId", { maxLines: 1, width: "fill_container" })
```

---

## Pre-Completion Checklist

- [ ] Run `pencil_snapshot_layout` (`problemsOnly: true`) on every section?
- [ ] All text inside auto-layout parents using `width: "fill_container"`?
- [ ] Mobile screens have appropriate padding (16–20px)?
- [ ] Long titles/descriptions that need truncation have `maxLines` set?
- [ ] All child frames using `width: "fill_container"` (not fixed widths wider than parent)?
- [ ] Verified the full screen with `pencil_get_screenshot`?

---

## See Also

- [screenshot-qa.md](../mcp/screenshot-qa.md) — Full workflow for catching visual overflow via screenshots
- [responsive.md](responsive.md) — Mobile layout constraints and responsive patterns
