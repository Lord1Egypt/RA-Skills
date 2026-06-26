# Layout Integrity — Hard Rules (MUST read before every `.pen` task)

> **Priority**: HIGHEST. Overrides style preferences.
> **Applies to**: ALL outputs — PPT slides, desktop UI, tablet, mobile, components, landing pages.
> **See also**: [overflow-prevention.md](overflow-prevention.md) · [pen-format.md](pen-format.md) · [screenshot-qa.md](../mcp/screenshot-qa.md)

"Looks reasonable" is not enough. Every artboard must be:

- **Bounded** — no content extends beyond the artboard rectangle.
- **Contained** — every child fits inside its parent's inner box (parent size − padding).
- **Non-overlapping** — sibling nodes never collide unintentionally.
- **Aligned** — items on the same row share a baseline / centerline; items in the same column share a left edge.
- **Balanced** — padding, gap, font size, and icon size follow a consistent scale.

---

## 1. Artboard Budget (do the math BEFORE writing)

Every artboard has fixed `width` × `height`. Before laying out, compute the **height budget**:

```
artboard_height = header_height + body_height + footer_height
body_height     = artboard_height − header_height − footer_height
```

### Typical budgets

| Artboard | Header | Footer | Body (auto) | Body padding (vertical) |
|---|---|---|---|---|
| PPT slide 1280×720 (content) | 64 | 40 | 616 | 32–40 |
| PPT slide 1280×720 (cover, full-bleed) | 0 | 0 | 720 | — (use `layout: "none"` for decoration only) |
| Desktop 1440×900 | 72 | — | 828 | 48–64 |
| Mobile 375×812 | 56 (status+nav) | 64 (tab bar) | 692 | 16–20 |

### Rules

- Body frame MUST be `"height": "fill_container"`. Never give it a fixed height.
- Fixed-height children inside the body (KPI row 140, image 200, etc.) PLUS gaps PLUS body vertical padding MUST sum `≤ body_height`.
- When uncertain, prefer `"fit_content"` on intermediate frames and set the outer body to `"fill_container"`.

### Width budget

```
usable_width = artboard_width − parent_horizontal_padding × 2
```

For a row of N cards with `gap = G`:

```
card_width = (usable_width − (N − 1) × G) / N
```

**Don't hand-pick pixel widths** — set each card to `"width": "fill_container"` and let auto-layout with `gap` do the math.

---

## 2. Auto-layout is the Default — `"layout": "none"` is the exception

| Situation | Layout |
|---|---|
| Any screen containing flowing content (list, form, cards, text blocks, PPT content slide) | `"vertical"` (or `"horizontal"` for row) |
| Cover slide / hero with decorative absolute shapes | `"none"` — but ALL children MUST stay inside the artboard rect (0 ≤ x, y; x + width ≤ artboard_width; y + height ≤ artboard_height). Decorative shapes MAY extend slightly beyond only if the parent has `"clip": true`. |
| Free-form illustration | `"none"` with `"clip": true` |

**Never** mix auto-layout children with absolute `x`/`y` — `x`/`y` are ignored inside an auto-layout parent and create mental-model drift.

---

## 3. Sizing Matrix (copy this into your head)

| Node role | width | height | Notes |
|---|---|---|---|
| Top-level artboard | number (1440 / 1280 / 375…) | number | Fixed |
| Artboard direct child (section) | `"fill_container"` | fixed (header/footer) OR `"fill_container"` (body) | |
| Row of cards / columns | `"fill_container"` | `"fit_content"` or fixed | Use `layout: "horizontal"` + `gap` |
| Each card in a row | `"fill_container"` | fixed OR `"fit_content"` | Cards of equal weight → equal fill |
| Card containing vertical list | `"fill_container"` | `"fit_content"` | |
| Body text / paragraph | `"fill_container"` + `textGrowth: "fixed-width"` | — | Mandatory |
| Heading | `"fill_container"` + `textGrowth: "fixed-width"` | — | Use `maxLines` if overflow risk |
| Inline label (next to icon in a row) | `"fit_content"` (no width) | — | Let the text shrink-wrap |
| Button / badge | `"fit_content"` | `"fit_content"` | `padding: [v,h]` defines size |
| Icon | number (12/14/16/18/20/24) | same number | Square, never stretched |
| Divider line | `"fill_container"` | `1` | |
| Avatar / thumbnail | number | same number | Square or aspect-locked |

---

## 4. Spacing Scale (use these, not arbitrary numbers)

```
Padding:   4 · 6 · 8 · 10 · 12 · 14 · 16 · 20 · 24 · 28 · 32 · 40 · 48 · 64
Gap:       2 · 4 · 6 · 8 · 10 · 12 · 14 · 16 · 20 · 24 · 32
Radius:    2 · 4 · 6 · 8 · 10 · 12 · 16 · 20 · 999
Icon size: 12 · 14 · 16 · 18 · 20 · 24
Font size: 11 · 12 · 13 · 14 · 15 · 16 · 18 · 20 · 24 · 28 · 32 · 40 · 48 · 64 · 72
```

Consistency beats creativity. Don't pick `padding: [13, 21]` — pick `[12, 20]`.

---

## 5. Alignment Rules

- Items in the same row: choose ONE of `alignItems: "center"` / `"start"` / `"end"` for the parent. Don't mix vertical positions in a row by hand.
- Items in the same column: parent controls `alignItems`. Text blocks default to start (left). Buttons in a form default to `justifyContent: "end"`.
- Card titles across a row: same `fontSize`, same `fontWeight`, same `fill`. Same goes for card body text.
- Icons next to text of size N: icon size ≈ N × 1.1 (rounded to scale). Text 14 → icon 16.
- Two columns of cards: both columns must have `"width": "fill_container"` OR both must be identically sized. Never `"fill_container"` + `480` side-by-side.

---

## 6. Buttons & Badges — Common Pitfalls

**Do**:

```json
{
  "type": "frame", "id": "btn01",
  "fill": "$--primary", "cornerRadius": 6,
  "padding": [10, 16], "gap": 6,
  "justifyContent": "center", "alignItems": "center",
  "children": [
    { "type": "icon_font", "id": "bi01", "width": 16, "height": 16, "iconFontName": "check", "iconFontFamily": "lucide", "fill": "$--primary-foreground" },
    { "type": "text", "id": "bt01", "content": "确认", "fontSize": 14, "fontWeight": "500", "fill": "$--primary-foreground", "fontFamily": "Inter", "lineHeight": 1.4 }
  ]
}
```

- No `width` / `height` on the button → it shrinks to fit content (correct).
- Horizontal padding ≥ vertical padding × 1.5 (keeps label room).
- Icon comes BEFORE text, `gap: 6` or `8`.
- Label text has NO `width: "fill_container"` inside a shrink-to-fit button — it would force button to stretch.

**Don't**:

- Fix `width: 80` with a 5-character label at fontSize 14 → clipping.
- Put button in auto-layout row without `alignItems: "center"` → crooked vertical alignment.
- Use full-width (`fill_container`) buttons unless the design explicitly demands it (forms, mobile CTAs).

---

## 7. PPT-Specific Rules (1280×720)

1. **Cover / closing slides** (`layout: "none"` allowed) — anchor all text blocks with explicit `x`/`y` AND `width` so they can't overflow:
   - Left margin: 96px. Right margin: ≥ 96px (text `width` ≤ 1088).
   - Top text baseline: ≥ 160px. Bottom baseline: ≤ 680px.
2. **Content slides** — MUST use `layout: "vertical"` with:
   - Header 64px (fixed) · Body `fill_container` · Footer 40px (fixed).
   - Body padding: `[32, 48]` or `[40, 48]` (top/bottom, left/right).
   - All inner rows: `width: "fill_container"`.
3. **KPI card rows** (4 cards): each card `width: "fill_container"`, `height: 120–140`, `gap: 20`. Never `gap: 16` with `padding: [_, 48]` — totals get awkward.
4. **Two-column body** (left / right): both columns `width: "fill_container"`, `height: "fill_container"`, `gap: 20`.
5. **Page numbers / footer** must be inside the footer frame, not floated. Use `justifyContent: "space_between"`.
6. **Slide Y-coordinates**: 0, 820, 1640, 2460 (720 + 100 gap).

---

## 8. Mobile Rules (375 / 393)

- Screen frame: exact target width.
- Direct children: `width: "fill_container"`, horizontal padding 16–20.
- Any text: `width: "fill_container"`, never wider than `screen_width − 2 × 16`.
- Tab bar / bottom nav: fixed height 64, `width: "fill_container"`, anchored via `justifyContent: "end"` on the screen OR as the last child of a `fill_container` body.
- Long lists must not push the screen taller than the artboard — content that exceeds should be implied-scrollable (design note only).

---

## 9. Detection — Automated Checks (Mode B)

Run AFTER every section, and again at final audit:

```
pencil_snapshot_layout({
  filePath: "...",
  parentId: "<artboardId>",
  maxDepth: 4,
  problemsOnly: true
})
```

Expected result at completion: **empty** (no Clipped / Overflow / Overlapping nodes).

Also run `pencil_get_screenshot` for each artboard and visually confirm:

- Nothing touches or crosses the artboard border.
- No text is cut mid-word.
- Rows of cards are equal width, equal height.
- Footer page numbers align to the right edge with the same inset as the header.

---

## 10. Manual Audit (Mode A) — Pre-completion Checklist

Go through EVERY artboard:

- [ ] Artboard has `layout: "vertical"` (or `"horizontal"`); only cover/hero uses `"none"` with `clip: true`.
- [ ] Header + footer have fixed height; body frame has `height: "fill_container"`.
- [ ] Every section frame inside body has `width: "fill_container"`.
- [ ] Every text inside an auto-layout parent has `width: "fill_container"` + `textGrowth: "fixed-width"`.
- [ ] Every row of cards: children use `width: "fill_container"`, same height.
- [ ] Sum of fixed-height children + gaps + vertical padding ≤ body computed height.
- [ ] No `x`/`y` on any child inside an auto-layout parent.
- [ ] In `layout: "none"` parents: every child satisfies `x ≥ 0`, `y ≥ 0`, `x + width ≤ parent_width`, `y + height ≤ parent_height` (decorative shapes with `clip: true` exempted).
- [ ] Icon sizes from the allowed scale (12/14/16/18/20/24). Buttons use `fit_content`.
- [ ] All colors via variables. No hex literals inside `fill` / `stroke.fill` (except within a documented gradient color list).
- [ ] Padding / gap / radius / font size / icon size all drawn from the spacing scale (§4).
- [ ] `read_lints` passes on the `.pen` file.

If any box is unchecked → fix, don't ship.

---

## 11. Problem → Fix Quick Reference

| Symptom | Root cause | Fix |
|---|---|---|
| Text clipped at right edge | Fixed-width text or missing `fill_container` | Add `width: "fill_container"` + `textGrowth: "fixed-width"` |
| Card row overflows right edge | Child cards have hardcoded widths summing > parent inner width | Switch each card to `"fill_container"`, tune `gap` |
| Body content visually exceeds artboard bottom | Body has fixed height, or children + gaps > artboard body height | Set body `height: "fill_container"`; reduce content or split slide |
| Button label wraps or clips | Button has fixed width smaller than label | Remove width; use `fit_content` + `padding: [v,h]` |
| Row items at different vertical positions | Parent missing `alignItems: "center"` | Add `alignItems: "center"` on the row frame |
| Columns misaligned left edges | Different `padding` on each column | Unify padding across columns |
| Gap looks inconsistent | Mixed `gap` values across siblings | Pick ONE value per layout level (usually 16 or 20) |
| Cover slide text floats off | `x`/`y` too large; no `width` set | Add `width: <bounded>` so text can wrap; keep x + width ≤ artboard width |
| Two-column layout where left is `fill_container`, right is fixed | Uneven balance, overflow risk | Both sides `fill_container` |

---

## 12. Golden Rules Card (memorize)

1. Body uses `height: "fill_container"`. Header/footer are fixed.
2. Every row child: `width: "fill_container"`.
3. Every text in auto-layout: `width: "fill_container"` + `textGrowth: "fixed-width"`.
4. Buttons/badges: `fit_content` + padding `[v, h]` + center align.
5. No `x`/`y` inside auto-layout. No `layout: "none"` for content.
6. Use the spacing scale (§4). No odd numbers.
7. Audit (§10) before declaring done.
