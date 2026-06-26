# PPTX Export Strategy - Progressive Approach

## Goal
Export HTML slides to editable PPTX, balancing editability vs. visual fidelity.

## Export Priority Matrix

### ✅ Tier 1: Native PPTX (Fully Editable)
Export as PowerPoint native elements for maximum editability.

| HTML Element | PPTX Element | Notes |
|--------------|--------------|-------|
| `<h1>-<h6>` | TextBox | Font size mapped from CSS |
| `<p>` | TextBox paragraph | Preserve alignment, color |
| `<ul>/<ol>` | TextBox with bullets | Manual bullet insertion |
| `<table>` | Table | Cell text, borders |
| `<div>` (solid bg) | Rectangle shape | Background color only |
| `<img>` | Picture | Native image insertion |
| `<svg>` → PNG | Picture | Rasterize SVG first |

### ⚠️ Tier 2: Degraded Export (Editable with Style Loss)
Simplify visual effects but preserve content editability.

| CSS Effect | Degradation Strategy |
|------------|----------------------|
| Gradient background | Use primary color or first gradient stop |
| Box shadow | Omit or use simple border |
| Text shadow | Omit |
| `opacity < 1` | Multiply alpha into RGB |
| Custom fonts | Fallback to system fonts (Arial, Calibri) |
| `transform: rotate()` | Omit rotation |

### ❌ Tier 3: Image Export (Not Editable)
Complex elements that cannot be natively represented.

| Element Type | Reason | Solution |
|--------------|--------|----------|
| Complex CSS compositions | Multiple effects layered | Screenshot entire slide |
| Canvas/WebGL graphics | Dynamic rendering | Screenshot element |
| CSS filters (blur, etc.) | No PPTX equivalent | Screenshot element |
| Embedded videos | PPTX limited support | Screenshot + placeholder |

---

## Implementation Plan

### Phase 1: DOM Analysis (MVP)
Parse HTML structure and classify elements.

**Input**: HTML slide
**Output**: Element tree with classifications

```python
class Element:
    type: str  # 'text', 'shape', 'image', 'table', 'complex'
    bounds: Rect  # x, y, width, height
    styles: dict  # CSS properties
    children: List[Element]
    export_tier: int  # 1, 2, or 3
```

### Phase 2: Layout Calculation
Convert relative CSS layout to absolute PPTX positions.

**Approach**:
1. Use Playwright to get `getBoundingClientRect()` for each element
2. Convert pixels to inches (96 DPI)
3. Handle nested elements (parent offset)

### Phase 3: Native Export
Export Tier 1 & 2 elements as native PPTX objects.

**Core transformations**:
- `color: #00ffcc` → `RGBColor(0, 255, 204)`
- `font-size: 36px` → `Pt(36)`
- `text-align: center` → `alignment = PP_ALIGN.CENTER`

### Phase 4: Image Fallback
Screenshot Tier 3 elements and insert as images.

### Phase 5: Merge & Polish
Combine native + image layers on each slide.

---

## Element Mapping Rules

### Text
```html
<h1 style="font-size: 48px; color: #00ffcc; text-align: center">
  Title
</h1>
```
↓
```python
txBox = slide.shapes.add_textbox(left, top, width, height)
p = txBox.text_frame.paragraphs[0]
p.text = "Title"
p.font.size = Pt(48)
p.font.color.rgb = RGBColor(0, 255, 204)
p.alignment = PP_ALIGN.CENTER
```

### Background Rectangle
```html
<div style="background: #4472C4; width: 300px; height: 200px">
</div>
```
↓
```python
shape = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, left, top, width, height
)
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(68, 114, 196)
```

### Table
```html
<table>
  <tr><th>Header</th></tr>
  <tr><td>Data</td></tr>
</table>
```
↓
```python
table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
table = table_shape.table
table.cell(0, 0).text = "Header"
table.cell(1, 0).text = "Data"
```

---

## Hybrid Export Mode

User can choose export mode:

| Mode | Use Case | Editability | Visual Fidelity |
|------|----------|-------------|-----------------|
| `--image` (default) | Pixel-perfect archive | ❌ None | ⭐⭐⭐⭐⭐ |
| `--native` | Editable slides | ✅ Full text | ⭐⭐⭐ |
| `--hybrid` | Balance both | ✅ Text editable | ⭐⭐⭐⭐ |

**Hybrid mode**:
1. Export text, shapes, tables natively
2. Screenshot complex visual effects as background layer
3. Overlay native text on top

---

## Limitations & Trade-offs

### Cannot Preserve
- CSS animations (PPTX has limited animation API)
- Custom web fonts (unless embedded, complex)
- Gradients with transparency
- Complex shadows/filters

### Can Approximate
- Gradient → dominant color
- Shadow → simple border
- Opacity → blended RGB

### Perfect Fidelity
- Solid colors
- Basic shapes
- Text with system fonts
- Tables
- Images

---

## Testing Strategy

### Test Cases
1. **Text slide**: Title + body → verify font/color/alignment
2. **Background slide**: Solid bg color → verify PPTX background
3. **Shape slide**: Rectangle with border → verify shape properties
4. **Table slide**: Data table → verify cell text
5. **Complex slide**: Gradient + shadow → verify fallback to image

### Validation
```python
def test_text_export():
    html = '<h1 style="font-size: 48px; color: #00ffcc">Test</h1>'
    pptx = export(html, mode='native')
    slide = pptx.slides[0]
    assert len(slide.shapes) == 1
    assert slide.shapes[0].text_frame.paragraphs[0].text == "Test"
```

---

## Next Steps

1. **Prototype DOM parser**: Use BeautifulSoup + Playwright to extract element tree
2. **Implement Tier 1 export**: Text, basic shapes, tables
3. **Add hybrid mode**: Mix native + screenshot layers
4. **User testing**: Validate with real slide decks
5. **Iterate**: Expand supported elements based on feedback