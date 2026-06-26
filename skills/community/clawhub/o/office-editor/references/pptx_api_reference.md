# python-pptx API Quick Reference

## Table of Contents

1. [Presentation Object](#presentation-object)
2. [Slide Objects](#slide-objects)
3. [Shape Objects](#shape-objects)
4. [TextFrame / Paragraph / Run](#textframe--paragraph--run)
5. [Table Object](#table-object)
6. [Chart Object](#chart-object)
7. [Picture Object](#picture-object)
8. [Units and Colors](#units-and-colors)
9. [Common Enums](#common-enums)

## Presentation Object

```python
from pptx import Presentation
```

| Property/Method | Description |
|-----------------|-------------|
| `Presentation()` | Create a new presentation |
| `Presentation(path)` | Open an existing file |
| `prs.save(path)` | Save to a file |
| `prs.slides` | Slide collection, supports `len()` and indexing |
| `prs.slide_layouts` | Slide layout collection |
| `prs.slide_masters` | Slide master collection |
| `prs.slide_width` | Slide width |
| `prs.slide_height` | Slide height |
| `prs.core_properties` | Core document properties such as title, author, and subject |

## Slide Objects

| Property/Method | Description |
|-----------------|-------------|
| `prs.slides.add_slide(layout)` | Add a slide |
| `slide.shapes` | Shape collection on the slide |
| `slide.shapes.title` | Title shape |
| `slide.placeholders` | Placeholder collection |
| `slide.placeholders[idx]` | Access a placeholder by index |
| `slide.notes_slide` | Notes slide |
| `slide.slide_layout` | Layout used by the current slide |

## Shape Objects

### SlideShapes

| Method | Description |
|--------|-------------|
| `shapes.add_textbox(left, top, width, height)` | Add a text box |
| `shapes.add_picture(image, left, top, width, height)` | Add an image |
| `shapes.add_shape(auto_shape_type, left, top, width, height)` | Add an auto shape |
| `shapes.add_table(rows, cols, left, top, width, height)` | Add a table |
| `shapes.add_chart(chart_type, x, y, cx, cy, chart_data)` | Add a chart |
| `shapes.add_connector(connector_type, begin_x, begin_y, end_x, end_y)` | Add a connector |
| `shapes.add_group_shape()` | Add a group shape |

### BaseShape

| Property | Description |
|----------|-------------|
| `shape.shape_id` | Shape ID |
| `shape.name` | Shape name |
| `shape.left` / `shape.top` | Position |
| `shape.width` / `shape.height` | Size |
| `shape.rotation` | Rotation angle |
| `shape.has_text_frame` | Whether it contains a text frame |
| `shape.text_frame` | Text frame object |
| `shape.text` | Text inside the shape, shorthand |
| `shape.has_table` | Whether it is a table |
| `shape.has_chart` | Whether it is a chart |

### AutoShape-Specific Properties

| Property | Description |
|----------|-------------|
| `shape.fill` | Fill formatting |
| `shape.fill.solid()` | Set solid fill |
| `shape.fill.background()` | Set no fill |
| `shape.fill.fore_color.rgb` | Fill foreground color |
| `shape.line` | Outline formatting |
| `shape.line.color.rgb` | Outline color |
| `shape.line.width` | Outline width |
| `shape.line.dash_style` | Outline dash style |

## TextFrame / Paragraph / Run

### TextFrame

| Property/Method | Description |
|-----------------|-------------|
| `tf.text` | Text content; setting it clears all paragraphs |
| `tf.paragraphs` | Paragraph collection |
| `tf.add_paragraph()` | Add a paragraph |
| `tf.clear()` | Clear all paragraphs |
| `tf.word_wrap` | Word wrapping |
| `tf.auto_size` | Auto sizing, uses `MSO_AUTO_SIZE` |
| `tf.margin_left/right/top/bottom` | Padding |
| `tf.vertical_anchor` | Vertical alignment, uses `MSO_ANCHOR` |

### _Paragraph

| Property/Method | Description |
|-----------------|-------------|
| `p.text` | Paragraph text |
| `p.runs` | Run collection |
| `p.add_run()` | Add a run |
| `p.alignment` | Horizontal alignment, uses `PP_ALIGN` |
| `p.level` | Indent level, `0-8` |
| `p.font` | Default paragraph font |
| `p.space_before` | Space before |
| `p.space_after` | Space after |
| `p.line_spacing` | Line spacing |

### _Run

| Property/Method | Description |
|-----------------|-------------|
| `run.text` | Text content |
| `run.font` | Font object |
| `run.hyperlink` | Hyperlink object |

### Font

| Property | Description |
|----------|-------------|
| `font.name` | Font name |
| `font.size` | Font size in points |
| `font.bold` | Bold |
| `font.italic` | Italic |
| `font.underline` | Underline |
| `font.color.rgb` | RGB color |
| `font.color.theme_color` | Theme color |

## Table Object

| Property/Method | Description |
|-----------------|-------------|
| `table.rows` | Row collection |
| `table.columns` | Column collection |
| `table.cell(row_idx, col_idx)` | Get a cell |
| `table.iter_cells()` | Iterate over all cells |
| `row.height` | Row height |
| `column.width` | Column width |
| `cell.text` | Cell text |
| `cell.text_frame` | Cell text frame |
| `cell.merge(other_cell)` | Merge cells |
| `cell.split()` | Split merged cells |
| `cell.is_merge_origin` | Whether the cell is the merge origin |
| `cell.is_spanned` | Whether the cell is covered by a merge |
| `cell.span_height` / `cell.span_width` | Span of the merged cell |
| `cell.fill` | Cell fill |
| `cell.vertical_anchor` | Vertical alignment |

## Chart Object

### ChartData Types

| Class | Use |
|-------|-----|
| `CategoryChartData` | Category charts such as bar, line, and pie |
| `XyChartData` | Scatter or XY charts |
| `BubbleChartData` | Bubble charts |

### Chart Properties

| Property/Method | Description |
|-----------------|-------------|
| `chart.chart_type` | Chart type |
| `chart.has_legend` | Whether the legend is shown |
| `chart.legend` | Legend object |
| `chart.category_axis` | Category axis |
| `chart.value_axis` | Value axis |
| `chart.plots` | Plot collection |
| `chart.series` | Series collection |

### Plot / DataLabels

| Property/Method | Description |
|-----------------|-------------|
| `plot.has_data_labels` | Whether data labels are shown |
| `plot.data_labels` | Data labels object |
| `data_labels.font` | Label font |
| `data_labels.number_format` | Number format |
| `data_labels.position` | Label position |

## Picture Object

| Property | Description |
|----------|-------------|
| `pic.left` / `pic.top` | Position |
| `pic.width` / `pic.height` | Size |
| `pic.crop_left/right/top/bottom` | Crop values |
| `pic.image` | Image object |
| `pic.image.content_type` | MIME type |
| `pic.image.blob` | Image binary data |

## Units and Colors

```python
from pptx.util import Inches, Pt, Cm, Emu
from pptx.dml.color import RGBColor

# Units
Inches(1)       # 1 inch = 914400 EMU
Pt(12)          # 12 points
Cm(2.54)        # 2.54 cm = 1 inch
Emu(914400)     # raw EMU unit

# Colors
RGBColor(0xFF, 0x00, 0x00)  # red
RGBColor(0x00, 0x80, 0xFF)  # blue
```

## Common Enums

| Enum | Import Path | Common Values |
|------|-------------|---------------|
| `PP_ALIGN` | `pptx.enum.text` | LEFT, CENTER, RIGHT, JUSTIFY |
| `MSO_ANCHOR` | `pptx.enum.text` | TOP, MIDDLE, BOTTOM |
| `MSO_AUTO_SIZE` | `pptx.enum.text` | NONE, SHAPE_TO_FIT_TEXT, TEXT_TO_FIT_SHAPE |
| `MSO_SHAPE` | `pptx.enum.shapes` | RECTANGLE, OVAL, ROUNDED_RECTANGLE, and more |
| `XL_CHART_TYPE` | `pptx.enum.chart` | COLUMN_CLUSTERED, LINE, PIE, BAR_CLUSTERED, and more |
| `XL_LEGEND_POSITION` | `pptx.enum.chart` | BOTTOM, LEFT, RIGHT, TOP |
| `XL_LABEL_POSITION` | `pptx.enum.chart` | INSIDE_END, OUTSIDE_END, CENTER |
| `MSO_THEME_COLOR` | `pptx.enum.dml` | ACCENT_1 through ACCENT_6, TEXT_1, TEXT_2 |
| `MSO_LINE_DASH_STYLE` | `pptx.enum.dml` | SOLID, DASH, DOT, DASH_DOT |
