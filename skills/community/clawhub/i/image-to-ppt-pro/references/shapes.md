# PPT Shape Recognition and Code Quick Reference

When analyzing images in Step 1, compare with this table to identify each graphic's shape type, record it, then directly use corresponding `pres.shapes.XXX` constant in Step 3.

---

## Recognition Process

Ask three questions for each graphic when viewing image:
1. **Outline**: Right angle? Rounded? Full circle? Polygon? Pointed corner?
2. **Symmetry**: Top-bottom symmetric? Left-right symmetric?
3. **Features**: Any缺口, arrow direction, protrusion, shadow?

---

## 1. Basic Shapes (Most Common)

| Visual Feature | Shape Name | pptxgenjs Constant |
|---------|---------|---------------|
| Right angle rectangle, four corners 90° | Rectangle | `pres.shapes.RECTANGLE` |
| Rectangle with rounded corners | Rounded Rectangle | `pres.shapes.ROUNDED_RECTANGLE` |
| Perfect circle or ellipse | Ellipse | `pres.shapes.OVAL` |
| Triangle, pointed corner up | Isosceles Triangle | `pres.shapes.ISOSCELES_TRIANGLE` |
| Triangle, right angle | Right Triangle | `pres.shapes.RIGHT_TRIANGLE` |
| Parallelogram, slanted right | Parallelogram | `pres.shapes.PARALLELOGRAM` |
| Trapezoid, narrow top wide bottom | Trapezoid | `pres.shapes.TRAPEZOID` |
| Hexagon | Hexagon | `pres.shapes.HEXAGON` |
| Pentagon (similar to arrow tag) | Pentagon | `pres.shapes.PENTAGON` |
| Octagon (stop sign shape) | Octagon | `pres.shapes.OCTAGON` |
| Diamond, four pointed corners | Diamond | `pres.shapes.DIAMOND` |

---

## 2. Arrow Shapes

| Visual Feature | Shape Name | pptxgenjs Constant |
|---------|---------|---------------|
| Thick arrow pointing right | Right Arrow | `pres.shapes.RIGHT_ARROW` |
| Thick arrow pointing left | Left Arrow | `pres.shapes.LEFT_ARROW` |
| Thick arrow pointing up | Up Arrow | `pres.shapes.UP_ARROW` |
| Thick arrow pointing down | Down Arrow | `pres.shapes.DOWN_ARROW` |
| Thick bidirectional arrow left-right | Left-Right Arrow | `pres.shapes.LEFT_RIGHT_ARROW` |
| Thick bidirectional arrow up-down | Up-Down Arrow | `pres.shapes.UP_DOWN_ARROW` |
| Thick four-directional arrow | Quad Arrow | `pres.shapes.QUAD_ARROW` |
| Curved arrow, turning right | Bent Arrow | `pres.shapes.BENT_ARROW` |
| U-shaped bend arrow | U-Turn Arrow | `pres.shapes.U_TURN_ARROW` |
| Thin line with arrow (connector) | See "Connectors" section below | — |

### Connectors (Thin line + arrow head)

```javascript
// Connector with arrow (more recommended than addShape LINE for flowcharts)
slide.addShape(pres.shapes.LINE, {
  x: 2.6, y: 1.37, w: 0, h: 0.35,      // Vertical: w=0,h>0; Horizontal: w>0,h=0
  line: {
    color: "888888",
    width: 1.5,
    endArrowType: "triangle",            // End arrow: triangle / open / stealth / diamond / oval / none
    beginArrowType: "none",             // Start arrow
  }
});
```

> **Recognition tip**: If arrow in image is **thin line with small triangle at end**, use connector + `endArrowType`; if **thick filled arrow shape**, use `RIGHT_ARROW` etc. shape constants.

---

## 3. Flowchart Specific Shapes

| Visual Feature | Flowchart Meaning | pptxgenjs Constant |
|---------|---------|---------------|
| Rounded rectangle | Start/End | `pres.shapes.ROUNDED_RECTANGLE` |
| Normal rectangle | Processing step | `pres.shapes.RECTANGLE` |
| Diamond | Decision/Branch | `pres.shapes.DIAMOND` |
| Parallelogram | Input/Output | `pres.shapes.PARALLELOGRAM` |
| Cylinder (looks like rectangle with ellipse top) | Database/Storage | `pres.shapes.CYLINDER` |
| Wavy rectangle (wave at bottom) | Document | `pres.shapes.WAVE` |
| Hexagon | Preparation step | `pres.shapes.HEXAGON` |

---

## 4. Annotation / Bubble Shapes

| Visual Feature | Shape Name | pptxgenjs Constant |
|---------|---------|---------------|
| Rectangle with small tail at bottom (speech bubble) | Rectangular Callout | `pres.shapes.RECTANGULAR_CALLOUT` |
| Rounded rectangle with tail | Rounded Rectangular Callout | `pres.shapes.ROUNDED_RECTANGULAR_CALLOUT` |
| Ellipse with tail | Oval Callout | `pres.shapes.OVAL_CALLOUT` |
| Cloud outline | Cloud Callout | `pres.shapes.CLOUD_CALLOUT` |

---

## 5. Star / Decorative Shapes

| Visual Feature | Shape Name | pptxgenjs Constant |
|---------|---------|---------------|
| Four-pointed star | 4-Point Star | `pres.shapes.STAR_4_POINT` |
| Five-pointed star | 5-Point Star | `pres.shapes.STAR_5_POINT` |
| Six-pointed star | 6-Point Star | `pres.shapes.STAR_6_POINT` |
| Explosion shape (sawtooth edge) | Explosion | `pres.shapes.IRREGULAR_SEAL_1` |
| Horizontal scroll | Horizontal Scroll | `pres.shapes.HORIZONTAL_SCROLL` |
| Vertical scroll | Vertical Scroll | `pres.shapes.VERTICAL_SCROLL` |

---

## 6. Lines (No shape, just line)

```javascript
// Line: Vertical w=0,h>0; Horizontal w>0,h=0; Diagonal w>0,h>0
slide.addShape(pres.shapes.LINE, {
  x: 1.0, y: 1.0, w: 3.0, h: 0,
  line: { color: "888888", width: 1.5 }
});
```

---

## 7. Shape Code Template

All shapes share following parameter structure, just replace `pres.shapes.XXX`:

```javascript
slide.addShape(pres.shapes.XXX, {
  x: 0,    // Left boundary (inches)
  y: 0,    // Top boundary (inches)
  w: 2,    // Width (inches)
  h: 0.5,  // Height (inches)
  fill: { color: "D8EAF5" },              // Fill color (hex, no #)
  line: { color: "A0C4E0", width: 1 },   // Border (width unit pt)
  // Only ROUNDED_RECTANGLE needs:
  rectRadius: 0.05,                       // Corner radius (inches, typical 0.03~0.1)
});

// ⚠️ Text layer must be separate addText, coordinates and dimensions exactly match shape
slide.addText("Text content", {
  x: 0, y: 0, w: 2, h: 0.5,             // ← Must exactly match shape x/y/w/h above
  fontSize: 11,
  color: "333333",
  fontFace: "Microsoft YaHei",
  align: "center",
  valign: "middle",
  margin: 0,                             // ← Must be 0, prohibit any padding
  wrap: true,                            // Text auto-wraps inside box
});
```

---

## ⚠️ Common Recognition Errors

| Shape Seen | Wrong Guess | Correct Answer |
|-----------|---------|---------|
| Rectangle with very small rounded corners | ROUNDED_RECTANGLE | May just be RECTANGLE, rectRadius not always needed |
| Thin line with arrow at end | RIGHT_ARROW (thick arrow shape) | LINE + endArrowType |
| Thick arrow shape with text inside | Text placed outside arrow | Text also overlaid on shape, coordinates same as shape |
| Flowchart diamond | RECTANGLE rotated | DIAMOND (use directly, no rotation needed) |
| Ellipse with text inside | Ellipse + separate text box | Text overlaid on ellipse, coordinates same |
