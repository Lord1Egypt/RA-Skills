# Visual Verification

> **Applies to**: Mode B (MCP Tools)
> **See also**: [overflow-prevention.md](../references/overflow-prevention.md) · [image-reuse.md](image-reuse.md)

---

## Why Screenshot Verification Cannot Be Skipped

Layout and spacing problems in the node tree are invisible. Only the rendered output reveals them. The following issues are only discoverable through screenshots:

| Issue Type | In the Node Tree | In the Screenshot |
|------------|-----------------|-------------------|
| Wrong font weight | Values look correct | Text appears too thin or too bold |
| Inconsistent padding | Values differ slightly | Cards have visibly uneven whitespace |
| Color too close to background | Values are individually correct | Element "disappears" or is hard to read |
| Alignment drift | Coordinate values are close | Elements are visibly misaligned |
| Missing gap | gap/padding exists but direction is wrong | Two sections run directly into each other |
| Auto-layout direction wrong | layout property exists | Children stack in unexpected direction |
| Image aspect ratio wrong | fill type is correct | Image appears stretched or squished |

---

## Core Principle: Build in Sections, Verify in Sections

> **Inspired by Stitch** — AI-driven design should be **conversational and iterative**: verify, get feedback, and fix after each section — not build everything at once and check at the end. This mirrors Stitch's "real-time suggestions" and "conversational refinement" philosophy.

```
Build Header    → Screenshot Header    → Find issues → Fix → Confirm
Build Hero      → Screenshot Hero      → Find issues → Fix → Confirm
Build Features  → Screenshot Features  → Find issues → Fix → Confirm
Build Footer    → Screenshot Footer    → Find issues → Fix → Confirm
Complete        → Screenshot full page → Final review
```

**Never** build a full page and then screenshot only at the end.

---

## Verification Workflow

### Step 1 — Screenshot the Current Section

```
pencil_get_screenshot({
  filePath: "path/to/file.pen",
  nodeId: "sectionNodeId"
})
```

For the final full-screen verification:

```
pencil_get_screenshot({
  filePath: "path/to/file.pen",
  nodeId: "screenNodeId"
})
```

### Step 2 — Visual Analysis Checklist

After receiving the screenshot, check against each dimension:

**Alignment**
- [ ] Elements properly centered/left/right aligned?
- [ ] Multiple columns equal width? Grid items consistently spaced?

**Spacing**
- [ ] Adequate padding inside containers?
- [ ] Gaps between elements consistent? Following 8px grid?

**Typography**
- [ ] Text readable (sufficient size and contrast)?
- [ ] Headings visually distinct from body text?
- [ ] Any text clipped, overlapping, or overflowing?

**Color & Contrast**
- [ ] Colors sourced from design variables (not hardcoded)?
- [ ] Contrast sufficient for readability?
- [ ] Overall color scheme cohesive?

**Completeness**
- [ ] All expected elements present?
- [ ] Icons/images placed correctly?
- [ ] Any empty areas or rendering breaks?

### Step 3 — Layout Problem Detection

Run in parallel with the screenshot:

```
pencil_snapshot_layout({
  filePath: "path/to/file.pen",
  parentId: "sectionNodeId",
  maxDepth: 3,
  problemsOnly: true
})
```

Catches programmatic issues the screenshot may not make obvious:
- **Clipped**: Child node extends beyond parent container bounds
- **Overlapping**: Sibling nodes unintentionally overlap
- **Out of bounds**: Node positioned outside its parent

### Step 4 — Fix and Re-Verify

```
Issue found
  → pencil_batch_design (fix with U/R operations)
  → pencil_get_screenshot (confirm fix)
  → pencil_snapshot_layout (confirm no new issues introduced)
  → Continue to next section
```

**Never skip the re-verify step.**

---

## Screenshot Timing Reference

| Moment | What to Screenshot |
|--------|-------------------|
| After completing a section | The section's root frame |
| After fixing an issue | The affected area |
| When the full design is complete | The complete screen/artboard |
| After modifying an existing design | The changed section |
| After bulk property updates | At least one affected area |
| When comparing two variants | Both variants side by side |

---

## Final Full-Screen Review Checklist

Before submitting the final screenshot, confirm all items:

- [ ] Overall visual hierarchy makes sense?
- [ ] Sections clearly separated with visual distinction?
- [ ] Spacing consistent from top to bottom?
- [ ] Looks professional and polished?
- [ ] Mobile: all content within the 375px frame?
- [ ] No empty gaps or rendering breaks?
- [ ] Color scheme harmonious as a whole?
- [ ] Adequate whitespace?

---

## See Also

- [overflow-prevention.md](overflow-prevention.md) — Fix patterns for overflow issues
- [image-reuse.md](image-reuse.md) — Verify that copied assets are placed correctly
