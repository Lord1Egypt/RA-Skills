# Page Types Catalog

Extracted from the 40-slide H3C template. Use these patterns as building blocks.

## 1. Cover Page (Layout 6: 节标题)

**When**: First slide, section dividers.

```
Title:   centered, 36-48pt bold RED2
Subtitle: centered, 14-16pt DARK
Tagline:  centered, 10pt LIGHT
Author:   centered, 9pt LIGHT, near bottom
```

Position reference: title Y≈1.2-1.5", subtitle Y≈2.2", tagline Y≈3.2"

---

## 2. Left Text + Right Card (Layout 3)

**When**: Main content with supporting visual/data on the right.

```
Left column:  x=0.5", w=4.2"
  - Section header: 13pt bold RED3
  - Body bullets: 10pt DARK, spacing 4pt
  - Can have 2 sections vertically

Right card:   x=5.1", w=4.4"
  - Rounded rect, fill=BG, border=BORDER
  - Card title: 11pt bold RED, with divider line below
  - Card content: 10-11pt, generous spacing
```

Template examples: Slides 7, 12

---

## 3. Three-Column Cards (Layout 3)

**When**: 3 parallel concepts/features to compare.

```
Card 1: x=0.5",  w=2.85"
Card 2: x=3.5",  w=2.85"
Card 3: x=6.5",  w=2.85"

Each card:
  - Rounded rect, fill=BG, border=BORDER
  - Red header bar: full width, h=0.38", RED fill, white text 12pt bold centered
  - Bullet content: 10pt, left-aligned, 0.2" indent from card edge
```

---

## 4. Data Card Wall (Layout 3)

**When**: Multiple KPI numbers or stats to showcase.

```
Grid: 3 columns × 2 rows (or 2×2, 2×3)

Each cell:
  - Number: 10pt bold #4B4948
  - Label: 8-9pt #4B4948 below number
  - Optional icon to the left of number

Grid start: y=1.5"
Cell size: ~1.6" wide × 0.8" tall
```

Template example: Slide 8 (19,000+ / 13,700+ / 443.51亿元 etc.)

---

## 5. Timeline / Milestones (Layout 3)

**When**: Development history, roadmap, phases.

```
Vertical timeline (right card):
  For each milestone:
    - Date badge: RED rect, 0.8"×0.28", white text 8-9pt bold centered
    - Title: 11pt bold DARK, right of badge
    - Description: 8pt LIGHT, below title
    - Vertical spacing: 0.75-0.85" per item

Horizontal timeline (full width):
  - Red line spanning width
  - Circle/rect nodes at intervals
  - Labels above/below alternating
```

---

## 6. Comparison Table (Layout 3)

**When**: Feature comparison, product vs product.

```
Header row: RED fill, white text 9-10pt bold centered
Data rows:  alternating WHITE / BG
Border:     BORDER on all cells
Row height: 0.34-0.38"

Column 0 (labels): left-aligned, RED text, bold
Column 1+: center-aligned, DARK text

Position: start at y=1.1-1.2", span full width (0.5" to 9.5")
```

---

## 7. Four-Quadrant Matrix (Layout 3)

**When**: 2×2 categorization, SWOT, positioning.

```
Top-left:     x=0.5",  y=1.2", w=4.2", h=1.8"
Top-right:    x=5.1",  y=1.2", w=4.4", h=1.8"
Bottom-left:  x=0.5",  y=3.2", w=4.2", h=1.8"
Bottom-right: x=5.1",  y=3.2", w=4.4", h=1.8"

Each quadrant:
  - Title: 14pt bold RED (or one RED, three DARK for emphasis)
  - Body: 10pt DARK
  - Optional BG fill on cards
```

Template example: Slide 23

---

## 8. Full-Width Content (Layout 3)

**When**: Large diagram, org chart, single focused message.

```
Content area: x=0.5", y=1.1", w=9.0", h=3.8"
Single text block or embedded chart/image.
```

Template examples: Slides 25, 29, 31 (chart slides)

---

## 9. Left Image + Right Text (Layout 3)

**When**: Product photo, screenshot, illustration with description.

```
Image area:  x=0.5",  y=1.1", w=3.8", h=3.8"
Text area:   x=4.7",  y=1.1", w=4.8", h=3.8"
  - Title: 20pt bold or 14pt bold RED
  - Body: 10-11pt, line spacing 1.2
```

Template example: Slide 7 (left photo + right text)

---

## 10. Process Flow (Layout 3)

**When**: Step-by-step workflow, funnel, pipeline.

```
Horizontal flow:
  - 3-5 rounded rects in a row
  - Arrow connectors between them
  - Each box: title + 2-3 bullet points
  - Box width: ~1.6-2.0"
  - Row y: centered vertically ≈ 2.0-3.5"

Vertical flow:
  - Steps stacked with downward arrows
  - Left-aligned, indented descriptions
```

---

## 11. Quote / Key Message Page (Layout 6 or 3)

**When**: Ending slide, key takeaway, executive summary.

```
Large quote:  24-30pt bold, centered or left-aligned
Attribution:  10pt LIGHT below
Accent:       RED horizontal line above or below the quote
```

---

## 12. Analogy Cards (Layout 3, right card)

**When**: Drawing parallels, showing precedents.

```
Inside right card:
  For each analogy:
    - Rounded rect: WHITE with BORDER (normal) or RED fill (highlight)
    - Title: 12pt bold centered
    - Description: 9pt LIGHT centered below
    - Spacing: 0.95" per card vertically
```

---

## 13. Two-Column Numbered Cards (Layout 3)

**When**: Two parallel concepts, A vs B, product vs product overview.

**Source**: Learned from 两栏模板 Slide 1.

```
Card width:  4.15"    Card height: 3.2"
Left card:   x=0.60"  Right card:  x=5.25"
Gap:         0.50"
Card top:    1.6"

Number circle: 0.65" diameter, RED fill, white 20pt bold centered
  Position: card left + 0.15", card top − 0.25" (floats above card)

Title: 16pt bold RED, y = card_top + 0.55", indent 0.25" from card edge
Divider: BORDER line at card_top + 1.0", spans card width − 0.4"
Body: 11pt DARK, y = card_top + 1.15", indent 0.25"
```

Helper: `tb.two_col_numbered_cards(slide, [{num, title, body}, ...])`

---

## 14. Stacked Numbered Bars (Layout 3)

**When**: Two key points stacked vertically, each with a number + title + description.

**Source**: Learned from 两栏模板 Slide 4.

```
Bar width:   8.50"    Bar height: 1.75"
Bar x:       0.75"    Gap: 0.30"
Bar 1 top:   1.30"    Bar 2 top: 3.35"

Number: 28pt bold RED, left side (x + 0.2", 0.8" wide)
Title:  16pt bold DARK, x + 1.2", y + 0.2"
Body:   11pt MID, x + 1.2", y + 0.65"
```

Helper: `tb.two_row_numbered_bars(slide, [{num, title, body}, ...])`

---

## 15. Label Tab Rows (Layout 3)

**When**: Two items with prominent category labels, label-then-detail style.

**Source**: Learned from 两栏模板 Slide 5.

```
Row width:   8.50"    Row height: 1.75"
Row x:       0.75"    Gap: 0.30"

Label tab: 2.6" × 0.85", RED fill, white 14pt bold centered
  Position: row_x − 0.15" (overlaps left edge), vertically centered in row

Body text: starts at row_x + tab_w + 0.1", 11pt DARK
  Width: row_w − tab_w − 0.3"
```

Helper: `tb.two_row_label_tabs(slide, [{label, body}, ...])`

---

## 16. Circle Avatar Cards (Layout 3)

**When**: Team/department showcase, role-based comparison, person profiles.

**Source**: Learned from 两栏模板 Slide 3.

```
Card width:  4.15"    Card height: 2.8"
Left card:   x=0.60"  Right card:  x=5.25"
Card top:    2.0"

Circle: 1.2" diameter, RED3 fill, centered above card
  y = card_top − 0.6" (overlaps top edge)
  Contains: 11pt bold WHITE text (role/icon label)

Title: 16pt bold RED, y = card_top + 0.75"
Body:  11pt DARK, y = card_top + 1.2"
```

Helper: `tb.two_col_circle_cards(slide, [{icon_text, title, body}, ...])`

---

## 17. Left Text + Right Stacked Cards (Layout 3)

**When**: Narrative argument on left, supporting points as mini-cards on right.

**Source**: Combined pattern (original Left Text + Right Card + stacked bars).

```
Left column:  x=0.6", w=4.0"
  Title: 14pt bold RED3, y=1.2"
  Body:  11pt DARK, y=1.65", h=3.0" (multi-paragraph OK)

Right column: x=5.0"
  Mini card: 4.6" × 1.55", BG fill + BORDER
  Card 1: y=1.2"    Card 2: y=3.05"   Gap=0.30"
  Number: 22pt bold RED, left side (0.6" wide)
  Title:  13pt bold DARK, right of number
  Body:   10pt MID, below title
```

Helper: `tb.left_text_right_stacked_cards(slide, left_title, left_body, [{num, title, body}, ...])`

---

## 18. Three-Column Vertical Cards (Layout 3)

**When**: Three parallel concepts, features, or services to compare side by side.

**Source**: Learned from 三栏模板 Slide 4.

```
Card width:  2.85"    Card height: 3.7"
Card 1: x=0.50"   Card 2: x=3.70"   Card 3: x=6.90"
Gap: 0.35"         Card top: 1.2"

Title: 14pt bold RED, y = card_top + 0.15", indent 0.15"
Divider: BORDER line at card_top + 0.8"
Body: 10pt DARK, y = card_top + 0.95", fill remaining height
```

Helper: `tb.three_col_vertical_cards(slide, [{title, body}, ...])`

---

## 19. Three-Row Numbered Bars (Layout 3)

**When**: Three key points stacked vertically with numbered emphasis.

**Source**: Learned from 三栏模板 Slide 1.

```
Bar width:   8.80"    Bar height: 1.15"
Bar x:       0.60"    Gap: 0.20"

Number circle: 0.50" diameter, RED fill, white 18pt bold centered
  Position: left side, vertically centered
Title: 14pt bold DARK, x + 0.85", y + 0.10"
Body:  10pt MID, x + 0.85", y + 0.45"
```

Helper: `tb.three_row_numbered_bars(slide, [{num, title, body}, ...])`

---

## 20. Three-Row Label Bars (Layout 3)

**When**: Three items with left-side category labels, like a mini-spec sheet.

**Source**: Learned from 三栏模板 Slide 6.

```
Label: 1.20" × 1.15", RED fill, white 14pt bold centered
Body area: 7.60" wide, BG fill + BORDER
Row x: 0.50"   Gap: 0.15" (tight stacking)
```

Helper: `tb.three_row_label_bars(slide, [{label, body}, ...])`

---

## 21. Three-Column Icon Cards (Layout 3)

**When**: Three features/services with icon badges and descriptions.

**Source**: Learned from 三栏模板 Slide 7 (adapted to H3C colors).

```
Card width:  2.85"    Card height: 3.7"
Same positions as #18

Icon circle: 0.70" diameter, RED fill, centered in card top
  Contains: 11pt bold WHITE text (short label or emoji stand-in)
Title: 13pt bold RED, centered, y = card_top + 1.1"
Body: 10pt DARK, y = card_top + 1.55"
```

Helper: `tb.three_col_icon_cards(slide, [{icon_text, title, body}, ...])`

---

## Choosing the Right Page Type

**Four-Column Layout Variants (from 四栏模板)**:

### 22. Four-Column Numbered Circles (Layout 3)

**When**: Four items arranged horizontally with numbered emphasis.

**Source**: Learned from 四栏模板 Slide 1.

```
Column width: 2.1"     Gap: 0.35"
Columns: x=0.50, 2.95, 5.40, 7.85"

Number circle: 0.6" diameter, RED fill, centered in column
Title: 12pt bold RED, centered above circle
Body: 10pt DARK, below circle
```

Helper: `tb.four_col_numbered_circles(slide, [{num, title, body}, ...])`

---

### 23. Four-Column Tall Cards (Layout 3)

**When**: Four parallel features/services with icon + title + body.

**Source**: Learned from 四栏模板 Slide 3.

```
Card: 2.1" × 3.3"    Gap: 0.35"
Icon circle: 0.6" diameter, RED fill, top center of card
Title: 12pt bold RED, centered
Divider: below title
Body: 9pt DARK
```

Helper: `tb.four_col_tall_cards(slide, [{title, body}, ...])`

---

### 24. Four-Row Badge Bars (Layout 3)

**When**: Four items with left badge/label + description (like PEST analysis).

**Source**: Learned from 四栏模板 Slide 4 & 6.

```
Badge: 1.5" × 0.5", RED fill, white 11pt bold centered
Title: 12pt bold DARK, right of badge
Body: 10pt MID, below title
Row height: 0.9"    Gap: 0.15"
```

Helper: `tb.four_row_badge_bars(slide, [{badge, title, body}, ...])`

---

### 25. Four-Column Ascending Steps (Layout 3)

**When**: Four progressive stages or levels, ascending from left to right.

**Source**: Learned from 四栏模板 Slide 5.

```
Column width: 2.1"    Gap: 0.35"
Step Y offset: 0.6" per column (rightmost is highest)
Card height: grows with step (1.2" to 2.1")
Dot: 0.12" RED circle below each card
Title: 12pt bold RED    Body: 9pt DARK
```

Helper: `tb.four_col_ascending_steps(slide, [{title, body}, ...])`

---

### 26. Timeline Horizontal Ascending (Layout 3)

**When**: Company history, product roadmap, multi-year milestones.

**Source**: Learned from 时间线流程图 Slide 1.

```
Three nodes ascending left-to-right:
  Node 1: x=1.5", y=3.5"  Node 2: x=4.2", y=2.7"  Node 3: x=6.9", y=1.9"

Year badge: 1.0" × 0.32", RED fill, white bold text
Vertical line: 0.02" wide, 1.2" tall, BORDER color
Title: 14pt bold DARK    Body: 10pt MID
Base bar: 9.0" × 0.5" at y=4.6", BG fill
```

Helper: `tb.timeline_horizontal_ascending(slide, [{year, title, body}, ...])`

---

### 27. Process Flow Arrows (Layout 3)

**When**: Three-step workflow, pipeline, sequential process.

**Source**: Learned from 时间线流程图 Slide 2.

```
Three arrow shapes at y=3.0", 2.5" wide, gap=0.5"
Number: 16pt bold WHITE centered in arrow
Vertical line up to content area
Title: 13pt bold RED    Body: 10pt DARK
```

Helper: `tb.process_flow_arrows(slide, [{num, title, body}, ...])`

---

### 28. Process Three Stage (Layout 3)

**When**: Three major phases/milestones with prominent numbering.

**Source**: Learned from 时间线流程图 Slide 3.

```
Three columns, 2.8" wide, gap=0.55"
Large number card: 2.0" × 1.3" at bottom, RED fill, 32pt bold WHITE
Dot: 0.2" RED circle at top of vertical line
Vertical line: BORDER, connects dot to number card
Title: 16pt bold RED    Body: 10pt DARK
```

Helper: `tb.process_three_stage(slide, [{num, title, body}, ...])`

---

## Choosing the Right Page Type (Final)

| Content Type | Recommended Page Type |
|---|---|
| Opening / section break | Cover Page |
| Narrative + supporting data | Left Text + Right Card |
| 3 parallel concepts | Three-Column Cards |
| KPI numbers | Data Card Wall |
| History / roadmap | Timeline |
| Product comparison | Comparison Table |
| 2×2 categorization | Four-Quadrant Matrix |
| Large visual / chart | Full-Width Content |
| Screenshot + explanation | Left Image + Right Text |
| Workflow / steps | Process Flow |
| Key takeaway | Quote / Key Message |
| Historical parallels | Analogy Cards |
| **A vs B parallel comparison** | **Two-Column Numbered Cards** |
| **Two key points, stacked** | **Stacked Numbered Bars** |
| **Category label + detail** | **Label Tab Rows** |
| **Team / role showcase** | **Circle Avatar Cards** |
| **Argument + supporting points** | **Left Text + Right Stacked Cards** |
| **3 parallel features (tall cards)** | **Three-Column Vertical Cards** |
| **3 key points, stacked** | **Three-Row Numbered Bars** |
| **3 categories with labels** | **Three-Row Label Bars** |
| **3 features with icons** | **Three-Column Icon Cards** |
| **4 items with numbers** | **Four-Column Numbered Circles** |
| **4 parallel features (tall)** | **Four-Column Tall Cards** |
| **4 rows with badges** | **Four-Row Badge Bars** |
| **4 ascending steps** | **Four-Column Ascending Steps** |
| **Timeline with years** | **Timeline Horizontal Ascending** |
| **3-step process flow** | **Process Flow Arrows** |
| **3-stage milestone** | **Process Three Stage** |
