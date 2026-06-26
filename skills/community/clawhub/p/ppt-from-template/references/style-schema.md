# Style Schema

The `style.yaml` file captures the complete visual identity extracted from a reference PDF, including per-layout element definitions.

## Example

```yaml
source: 培训课模板.pdf
pages_analyzed: 6
slide_size: "16:9"            # 10" x 5.625"

# ── Global Colors ──
colors:
  primary: "2040E0"
  secondary: "E8A020"
  accent: "E02020"
  background: "0A0A0A"
  text_primary: "FFFFFF"
  text_body: "E8A020"
  text_muted: "D4A574"

# ── Global Typography ──
typography:
  title:    { size: 44, weight: bold, font: "Arial Black" }
  subtitle: { size: 28, weight: bold, font: "Arial" }
  body:     { size: 22, weight: bold, font: "Arial" }
  caption:  { size: 14, weight: normal, font: "Arial" }

# ── Layouts with Element Definitions ──
layouts:
  - type: cover
    source_page: 1
    background:
      type: solid              # solid | image | gradient
      color: "0A0A0A"
    elements:
      - id: title
        type: text
        role: title            # title | subtitle | body | label | tagline
        x: 0.6                # inches from left
        y: 0.4
        w: 5.0
        h: 1.2
        style:
          fontSize: 48
          fontFace: "Arial Black"
          color: "FFFFFF"
          bold: true
          align: left

      - id: keyword_tags
        type: tag_group        # special: row of filled rectangles with text
        x: 6.2
        y: 0.55
        items_per_row: 3
        tag_w: 1.15
        tag_h: 0.55
        gap: 0.15
        style:
          fill: "2040E0"
          fontSize: 16
          color: "FFFFFF"
          bold: true

      - id: divider
        type: line
        x: 0.6
        y: 2.0
        w: 8.8
        style:
          color: "E8A020"
          width: 1.5

      - id: hero_title
        type: text
        role: title
        x: 0.6
        y: 2.3
        w: 8.8
        h: 2.5
        style:
          fontSize: 56
          fontFace: "Arial Black"
          color: "E8A020"
          bold: true

      - id: tagline
        type: text
        role: tagline
        x: 0.6
        y: 4.8
        w: 8.8
        h: 0.5
        style:
          fontSize: 18
          color: "D4A574"

  - type: content
    source_page: 5
    background:
      type: solid
      color: "0A0A0A"
    elements:
      - id: title_block
        type: shape
        shape: rectangle
        x: 4.5
        y: 0.3
        w: 3.5
        h: 0.8
        style:
          fill: "E8A020"

      - id: title_text
        type: text
        role: title
        x: 4.5
        y: 0.3
        w: 3.5
        h: 0.8
        style:
          fontSize: 32
          fontFace: "Arial Black"
          color: "0A0A0A"
          bold: true
          align: center
          valign: middle

      - id: left_image
        type: image
        role: illustration      # illustration | photo | mockup | icon | decorative
        x: 0.3
        y: 1.5
        w: 3.8
        h: 3.5
        placeholder: true       # AI should generate or user provides
        description: "Phone mockup or product screenshot"

      - id: numbered_list
        type: numbered_list
        x: 4.5
        y: 1.5
        w: 5.1
        item_h: 0.7
        max_items: 5
        style:
          number_color: "E02020"
          number_size: 22
          text_color: "E8A020"
          text_size: 20
          bold: true

  - type: section
    source_page: 7
    background:
      type: image
      description: "Full-bleed photo with dark overlay"
      overlay_color: "000000"
      overlay_opacity: 40
    elements:
      - id: main_text_1
        type: text
        role: title
        x: 0.5
        y: 1.2
        w: 9.0
        h: 1.5
        style:
          fontSize: 52
          fontFace: "Arial Black"
          color: "E8A020"
          bold: true
          align: center

      - id: main_text_2
        type: text
        role: subtitle
        x: 0.5
        y: 3.0
        w: 9.0
        h: 1.5
        style:
          fontSize: 52
          fontFace: "Arial Black"
          color: "E8A020"
          bold: true
          align: center

  - type: detail
    source_page: 10
    background:
      type: solid
      color: "0A0A0A"
    elements:
      - id: left_panel
        type: image
        role: mockup
        x: 0.0
        y: 0.0
        w: 2.5
        h: 5.625
        placeholder: true
        description: "Phone or device mockup, full height"

      - id: title
        type: text
        role: title
        x: 3.0
        y: 0.4
        w: 6.5
        h: 0.8
        style:
          fontSize: 36
          fontFace: "Arial Black"
          color: "FFFFFF"
          bold: true

      - id: step_list
        type: step_list
        x: 3.0
        y: 1.6
        w: 6.5
        item_h: 1.2
        max_items: 3
        style:
          number_color: "E02020"
          number_size: 28
          title_color: "FFFFFF"
          title_size: 24
          subtitle_color: "D4A574"
          subtitle_size: 16

  - type: closing
    source_page: 37
    background:
      type: solid
      color: "0A0A0A"
    elements:
      - id: quote
        type: text
        role: title
        x: 0.6
        y: 0.6
        w: 8.8
        h: 2.0
        style:
          fontSize: 40
          fontFace: "Arial Black"
          color: "FFFFFF"
          bold: true

      - id: divider
        type: line
        x: 0.6
        y: 3.0
        w: 8.8
        style:
          color: "E8A020"
          width: 1.5

      - id: left_text
        type: text
        role: body
        x: 0.6
        y: 3.4
        w: 4.5
        h: 1.0
        style:
          fontSize: 36
          color: "D4A574"
          bold: true

      - id: vertical_divider
        type: line
        x: 5.8
        y: 3.4
        w: 0
        h: 1.0
        direction: vertical
        style:
          color: "E8A020"
          width: 2

      - id: cta
        type: text
        role: body
        x: 6.1
        y: 3.4
        w: 3.5
        h: 1.0
        style:
          fontSize: 28
          color: "E02020"
          bold: true

      - id: footer
        type: text
        role: caption
        x: 0.6
        y: 4.8
        w: 8.8
        h: 0.4
        style:
          fontSize: 14
          color: "D4A574"
          align: center

# ── Decorations ──
decorations:
  card_style: none
  card_shadow: false
  accent_bar: none
  icon_style: none
  divider: thin_golden_line
  keyword_tags: filled_blue_rectangles
  text_style: ultra_bold_impact
```

## Element Types

| Type | Description | Key Properties |
|------|-------------|----------------|
| `text` | Text box | role, fontSize, color, bold, align, valign |
| `image` | Image placeholder | role (illustration/photo/mockup/icon/decorative), placeholder, description |
| `video` | Video placeholder | role, description, thumbnail_description |
| `shape` | Shape (rectangle, oval, line) | shape, fill, line, transparency |
| `line` | Divider line | color, width, direction (horizontal/vertical) |
| `numbered_list` | Numbered items | number_color, text_color, item_h, max_items |
| `step_list` | Steps with title + subtitle | number/title/subtitle styles, item_h |
| `tag_group` | Row of filled tag rectangles | items_per_row, tag_w, tag_h, gap, fill |
| `icon_group` | Row/grid of icons with labels | cols, icon_size, icon_style |
| `chart` | Chart placeholder | chart_type (bar/line/pie), description |
| `table` | Table placeholder | rows, cols, header_style, cell_style |

## Element Roles

| Role | Typical Usage |
|------|--------------|
| `title` | Main heading (36-56pt, bold) |
| `subtitle` | Secondary heading (24-32pt) |
| `body` | Body text (16-22pt) |
| `label` | Small label/tag (12-16pt) |
| `tagline` | Slogan or motto (14-18pt) |
| `caption` | Footer, source citation (10-14pt) |
| `illustration` | Conceptual or decorative image |
| `photo` | Realistic photo |
| `mockup` | Device/product mockup |
| `icon` | Small icon in circle/square |
| `decorative` | Background decoration, no content |

## Background Types

| Type | Properties |
|------|-----------|
| `solid` | `color` (hex) |
| `image` | `description`, `overlay_color`, `overlay_opacity` |
| `gradient` | `color_start`, `color_end`, `direction` (horizontal/vertical/diagonal) |

## Position & Size

All values in **inches** relative to slide origin (top-left = 0,0).
- 16:9 slide: 10.0" wide × 5.625" tall
- x, y = top-left corner of element
- w, h = width and height
