---

name: image-to-ppt-pro
description: |
Replicate any image (PPT screenshots, slide photos, design mockups) into fully editable .pptx files with pixel-perfect restoration of layout, colors, text, and graphic elements.

Trigger this skill immediately when users say any of the following:

* "Generate/create PPT from image/screenshot"
* "Turn this image into an editable slide"
* "Replicate/restore this PPT page"
* "Generate PPT identically"
* "Convert screenshot to pptx"
* Upload PPT screenshots or slide images and request editable output

## Even if users don't explicitly say "identical", trigger this skill whenever they upload images and want .pptx output.

# PPT Replicator Skill

Complete workflow for replicating images into editable `.pptx` files.

## Dependencies

```bash
npm install -g pptxgenjs
pip install Pillow numpy pytesseract --break-system-packages -q
# LibreOffice + pdftoppm (from poppler-utils)
```

---

## Workflow Overview

```
Step -1  Image Type Classification  ← Required! Determines Strategy A or B
    ↓
    ├─── Strategy A: Pure Code Replication      (Images with flat geometric shapes)
    │     Step 0    Perspective Correction      ← Required for photos; skip for screenshots
    │     Step 1    Data Extraction             ← Colors + OCR text + shape recognition
    │     Step 2    Visual Planning             ← Define regions, record coordinates
    │     Step 3    Code Implementation         ← Code each block
    │     Step 3.5  Pre-flight Check            ← ★ Paper verification before execution
    │     Step 4    Generate pptx
    │     Step 5    Visual QA + Correction Loop (max 3 iterations)
    │     Step 6    Delivery
    │
    └─── Strategy B: Mathematical Approximation (Images with 3D/lighting/curves that can be geometrically decomposed)
          Step 0    Perspective Correction      ← Required for photos; skip for screenshots
          Step 1    Data Extraction             ← Colors + OCR text + layer decomposition
          Step B2   Layer Planning              ← Decompose complex graphics into overlay layers
          Step B3   Code Implementation         ← Transparency + math coordinates + multi-shape overlay
          Step 3.5  Pre-flight Check            ← ★ Paper verification before execution
          Step 4    Generate pptx
          Step 5    Visual QA + Correction Loop (max 3 iterations)
          Step 6    Delivery
```

**Core difference between paths**: Strategy A directly replicates flat graphics; Strategy B doesn't pursue pixel-perfect replication but uses geometric overlays + transparency + math coordinates to approximate complex visuals, trading visual fidelity for **100% editability**.

**Value of Step 3.5**: After writing the script, perform paper verification before execution to intercept out-of-bounds, overlaps, and text overflow issues, significantly reducing Step 5 correction iterations.

---

## ⚠️ Global Golden Rules (Every line of code must follow)

### Rule 1: Text margin must be 0

All `addText` calls, whether for titles, body text, or node text, **must** include `margin: 0`.

```javascript
// ✅ Correct
slide.addText("text", { x:1, y:1, w:3, h:0.5, margin: 0, ... });

// ❌ Wrong: Missing margin: 0, pptxgenjs default padding causes text position offset
slide.addText("text", { x:1, y:1, w:3, h:0.5, ... });
```

### Rule 2: Text box coordinates must exactly match shape coordinates

For text inside shapes, the text box's `x/y/w/h` must be **exactly identical** to the underlying shape, with no offset.

```javascript
// ✅ Correct: Shape and text coordinates are identical
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:1.4, y:0.95, w:2.4, h:0.42, ... });
slide.addText("text", { x:1.4, y:0.95, w:2.4, h:0.42, margin:0, align:"center", valign:"middle" });

// ❌ Wrong: Text box doesn't match shape coordinates, causes text offset or overflow
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:1.4, y:0.95, w:2.4, h:0.42, ... });
slide.addText("text", { x:1.5, y:1.0,  w:2.2, h:0.35, ... });
```

### Rule 3: Text box dimensions locked, no auto-expansion allowed

Text box `w` and `h` must be explicitly set to match the corresponding shape dimensions. If text doesn't fit, **reduce font size or adjust line breaks**, never rely on text box auto-expansion.

### Rule 4: Drawing order must be background → foreground

1. Background color
2. Large background rectangles (header, footer, content area base)
3. Content graphics (node shapes, connection lines, decorations)
4. Text inside graphics (add text immediately after each shape, don't wait for all shapes)

### Rule 5: Text direction must match original image

**Judge text direction first** when viewing the image, then write code:

|Condition|Text Direction|Code|
|-|-|-|
|Text box **width > height**, text reads left→right normally|Horizontal (default)|No direction attribute needed|
|Text box **height > width × 3**, text top→bottom, each character **upright**|Vertical (Chinese)|`vert: "eaVert"`|
|Entire text block rotated 90° or 270°|Rotated horizontal|`rotate: 270` (or 90)|

**⚠️ Two wrong approaches for vertical text:**

```javascript
// ❌ Wrong: Using narrow text box as vertical, text becomes horizontal stacked
slide.addText("Group Data Platform", { x:0, y:1, w:0.3, h:2.0, ... });
// Result: Text horizontal, insufficient width, characters overlap

// ❌ Wrong: Using rotate for Chinese vertical, characters lie on side
slide.addText("Group Data Platform", { x:0, y:1, w:0.3, h:2.0, rotate: 270, ... });
// Result: Entire text block tilted, characters lying sideways

// ✅ Correct: vert: "eaVert" for upright Chinese vertical
slide.addText("Group Data Platform", {
  x: 0, y: 1, w: 0.4, h: 2.0,   // w sufficient for single character width (~0.3-0.5")
  fontSize: 14, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei",
  align: "center", valign: "middle",
  margin: 0,
  vert: "eaVert",                 // ← Key attribute for Chinese vertical
});
```

---

## Step -1: Image Type Classification (Required)

**After viewing image, answer these two questions to determine the path.**

---

### Classification 1: Strategy A?

**All conditions met → Use Strategy A**:

|Condition|Description|
|-|-|
|All graphics are flat basic shapes|Rectangles, rounded rectangles, diamonds, ellipses, lines, arrows|
|No lighting gradients, no transparency layers|Each element solid fill, clear color boundaries|
|No curve-arranged elements|All elements arranged in rows/columns or flowcharts|

**Typical scenarios**: Flowcharts, architecture diagrams, org charts, data tables. Proceed directly to Step 0, no need to inform user.

---

### Classification 2: Strategy B?

**Any of these signals present, but can be geometrically decomposed → Use Strategy B**:

|Complex visual signal (any)|And can be geometrically decomposed (all must satisfy)|
|-|-|
|3D perspective / isometric graphics|Graphics can be approximated with triangles, ellipses, rectangles|
|Glow / fan-shaped beams / gradient backgrounds|Layering differences can simulate depth with transparency|
|Decorative elements arranged along circular arcs|Can calculate coordinates with parametric equations|
|Multi-layer stacked 3D effects|Can use "large shape + white cover" to achieve cutout rings|

**Decision mnemonic**: "Flatten" the graphic in your mind—if after flattening it can be reconstructed with triangles + ellipses + rectangles + transparency combinations, use Strategy B.

**Typical scenarios**: Circular supply chain platform diagrams, funnel + glow combinations, dashboard schematics.

Inform user:

> "This image contains [specific description], will use 'Mathematical Approximation' strategy: overlay geometric shapes + simulate lighting layers with transparency, all elements fully editable, visual fidelity ~75-85% (abandoning pixel-level lighting details, preserving overall visual structure)."

---

## Strategy B: Mathematical Approximation (Detailed Steps)

**Core idea**: Don't pursue pixel-perfect replication, decompose complex visual graphics into several "geometric layers", use transparency differences to simulate lighting layers, use parametric equations to calculate coordinates of curve-arranged elements, trading for 100% editability.

**Practical verification**: For complex circular supply chain platform diagrams, can actually achieve:

* Fan-shaped beams → 5 triangles with different transparencies
* 3D cylinder → 3-4 nested ellipses + white ellipse cutout
* Arc decorative ring → 52 small rectangles arranged by parametric equations
* 3D tower → 9 rectangle columns with different heights + transparencies
* All code generated, zero images, 100% editable

---

### Step B2: Layer Planning

When viewing image, decompose complex graphics **from bottom to top** into geometric layers, each corresponding to an approximation method:

|Layer|Original Effect|Approximation Method|
|-|-|-|
|L1|Background glow / fan beams|N triangles, same color different transparencies, expanding from center outward|
|L2|Circular platform base color|Large ellipse (semi-transparent) + small white ellipse (cutout inner ring)|
|L3|Decorative elements along arc|Small rectangles, coordinates calculated with ellipse parametric equations|
|L4|Central column / tower structure|Rectangle group, center highest and darkest, gradually shorter and more transparent toward sides|
|L5|Leader lines pointing to labels|Polyline (vertical line + horizontal line, two LINE segments拼接)|
|L6|All text labels|addText, coordinates precisely matching original positions|

**Layer Record Table** (fill before writing code):

|Layer|Description|Shape Type|Count|Color|Transparency Range|Key Dimensions|
|-|-|-|-|-|-|-|
|L1|Background fan beams|triangle|5|F4CACA|55-78%|Cover corresponding fan sector|
|L2|Large ellipse platform|ellipse×3|3|F8DADA|20-38%|cx=5.5 rx=3.5 ry=1.0|
|L3|Arc decorative ring|rectangle|52|D85D5D|0%|0.08×0.15"|
|L4|Central tower|rectangle|9|B50E17|0-92%|w=0.05"|
|L5|Leader lines|line×2|N groups|888888|0%|—|
|L6|Text labels|text|N|A64F4F|0%|Positioned by OCR|

---

### Step B3: Code Implementation (Three Core Techniques)

#### Technique 1: Transparency Control (Simulate Lighting Layers)

`transparency` is the most core parameter in Strategy B, range 0 (fully opaque) ~ 100 (fully transparent). **Larger values are more transparent**, opposite of intuition, requires special attention.

```javascript
// ── Fan-shaped beams: multiple triangles, same color, different transparencies ──────────────────────────
// Closer to center = less transparent (smaller value), farther out = more transparent (larger value)

slide.addShape(pres.shapes.TRIANGLE, {   // Central triangle, 22% opaque
  x: 3.5, y: 1.0, w: 3.0, h: 4.0,
  fill: { color: "F4CACA", transparency: 78 },
  line: { color: "F4CACA", width: 0 },   // ← Must be width:0, otherwise hard edges
});
slide.addShape(pres.shapes.TRIANGLE, {   // Left triangle, 34% opaque
  x: 1.5, y: 1.5, w: 3.0, h: 3.5,
  fill: { color: "F4CACA", transparency: 66 },
  line: { color: "F4CACA", width: 0 },
});
slide.addShape(pres.shapes.TRIANGLE, {   // Outermost triangle, 45% opaque
  x: 0.0, y: 1.5, w: 3.0, h: 3.5,
  fill: { color: "F4CACA", transparency: 55 },
  line: { color: "F4CACA", width: 0 },
});

// ── Multi-layer ellipse overlay + white cutout (circular platform) ─────────────────────────────────────
slide.addShape(pres.shapes.OVAL, {       // Large ellipse, platform base color
  x: 1.5, y: 3.0, w: 7.0, h: 2.0,
  fill: { color: "F8DADA", transparency: 20 },
  line: { color: "F8DADA", width: 0 },
});
slide.addShape(pres.shapes.OVAL, {       // White ellipse, covers inner ring → forms ring shape
  x: 2.5, y: 3.2, w: 5.0, h: 1.4,
  fill: { color: "FFFFFF", transparency: 0 },
  line: { color: "FFFFFF", width: 0 },
});
slide.addShape(pres.shapes.OVAL, {       // Thin ring outline
  x: 2.3, y: 3.15, w: 5.4, h: 1.5,
  fill: { color: "F5CACA", transparency: 38 },
  line: { color: "D85D5D", width: 1.5 },
});
```

**Transparency Quick Reference**:

|transparency value|Visual Effect|Typical Use|
|-|-|-|
|0|Fully opaque (solid)|Main structure, accent colors|
|20-30|Slightly transparent, color saturated|Platform base color, main areas|
|40-55|Semi-transparent, layered feel|Mid-layer glow|
|60-75|Quite transparent, outline still clear|Outer glow|
|85-92|Very transparent, nearly invisible|Far beams, decorative columns|

---

#### Technique 2: Math Coordinate Calculation (Elements arranged along ellipse path)

```javascript
// ── N small rectangles evenly arranged along ellipse path (arc decorative ring) ─────────────────────────────
// cx/cy = ellipse center (inches), rx/ry = horizontal/vertical radius (inches)
// ew/eh = width/height of each small element (inches)

const cx = 5.5,  cy = 4.5;   // Ellipse center
const rx = 3.2,  ry = 0.6;   // Ellipse radius
const N  = 52;                // Total elements
const ew = 0.08, eh = 0.15;  // Small rectangle dimensions

for (let i = 0; i < N; i++) {
  const theta = (2 * Math.PI * i) / N;          // Even angles, 0 → 2π
  const x = cx + rx * Math.cos(theta) - ew / 2; // Element top-left x
  const y = cy + ry * Math.sin(theta) - eh / 2; // Element top-left y
  const color = i % 3 === 0 ? "D85D5D" : "EE8D8D"; // Alternating colors

  slide.addShape(pres.shapes.RECTANGLE, {
    x, y, w: ew, h: eh,
    fill: { color },
    line: { color, width: 0 },
  });
}
```

**Center and radius estimation method**:

* `cx` = Ellipse horizontal center (inches) = center pixel x ÷ image width px × 10
* `cy` = Ellipse vertical center (inches) = center pixel y ÷ image height px × 5.625
* `rx` = Ellipse horizontal radius (inches) = radius pixels ÷ image width px × 10
* `ry` = Ellipse vertical radius (inches) = radius pixels ÷ image height px × 5.625

---

#### Technique 3: Gradient Column Structure (Center highest and darkest, gradually shorter and more transparent toward sides)

```javascript
// ── Central tower: 9 columns, center highest and most solid, gradually shorter and more transparent toward sides ─────────────────────
const baseY  = 3.93;  // Column bottom y (inches, shared by all columns)
const colW   = 0.05;  // Column width (inches)

// [x coordinate, height, transparency]  Center column transparency=0 (solid)
const columns = [
  [4.944, 0.82, 92],
  [5.034, 1.00, 92],
  [5.124, 1.18, 92],
  [5.214, 1.55, 92],
  [5.304, 2.15,  0],   // ← Center main column, fully opaque
  [5.349, 2.36,  0],   // ← Second highest column, fully opaque
  [5.484, 1.55, 92],
  [5.574, 1.00, 92],
  [5.664, 0.82, 92],
];

columns.forEach(([x, h, transp]) => {
  const color = transp === 0 ? "B50E17" : "D76666";
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x - colW / 2,
    y: baseY - h,       // Column grows upward from bottom
    w: colW,
    h,
    fill: { color, transparency: transp },
    line: { color, width: 0 },
  });
});
```

---

#### Polyline Leaders (L-shaped, connecting graphics to text labels)

```javascript
// ── Leader = vertical segment + horizontal segment, two LINE segments拼接 ──────────────────────────────
// anchorX/Y = Leader start point on graphic
// labelX/Y  = Label position

const anchorX = 1.25, anchorY = 4.12;
const labelY  = 2.70, labelX  = 1.00;

// Vertical line: from start point up to label height
slide.addShape(pres.shapes.LINE, {
  x: anchorX, y: labelY, w: 0, h: anchorY - labelY,
  line: { color: "888888", width: 0.75 },
});
// Horizontal line: from vertical top horizontally to label
slide.addShape(pres.shapes.LINE, {
  x: labelX, y: labelY, w: anchorX - labelX, h: 0,
  line: { color: "888888", width: 0.75 },
});
```

---

### Strategy B QA Focus

After Step 5 generates preview image, **in addition to Strategy A general checks**, additionally check:

|Check Item|Judgment Criteria|
|-|-|
|Transparency layers natural|Glow naturally attenuates from center outward, no abrupt jumps|
|Triangles have hard edges|Triangle edges show dark outline (is `line.width` 0)|
|Ellipse path elements closed and even|Arc decorative ring fully closed, no obvious uneven spacing|
|Cutout effect clean|White cover ellipse edges aligned, no color gaps showing|
|Column structure symmetrical|Tower left-right symmetrical about central axis|
|Leader corner continuous|Vertical line endpoint and horizontal line start coordinates precisely connected|

---

## Step 0: Perspective Correction (Required for photos, skip for screenshots)

**Judgment**: Edges not parallel, shot from side, corners not right angles → Must correct.

```python
# scripts/correct_perspective.py
from PIL import Image
import numpy as np

def order_points(pts):
    pts = np.array(pts, dtype="float32")
    s, diff = pts.sum(axis=1), np.diff(pts, axis=1).flatten()
    return np.array([pts[np.argmin(s)], pts[np.argmin(diff)],
                     pts[np.argmax(s)], pts[np.argmax(diff)]], dtype="float32")

def _find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
    A = np.matrix(matrix, dtype=float)
    B = np.array(pb).reshape(8)
    return np.array(np.dot(np.linalg.inv(A.T * A) * A.T, B)).reshape(8)

def perspective_correct(src_path, corners, dst_path, w=1920, h=1080):
    img = Image.open(src_path)
    src = order_points(corners)
    dst = np.array([[0,0],[w-1,0],[w-1,h-1],[0,h-1]], dtype="float32")
    img.transform((w,h), Image.PERSPECTIVE, _find_coeffs(dst,src), Image.BICUBIC).save(dst_path)
    print(f"✓ Correction complete → {dst_path}")

perspective_correct(
    src_path="/mnt/user-data/uploads/your_photo.jpg",
    corners=[[120,85],[1800,60],[1820,980],[100,1000]],  # ← Replace after viewing image with view tool
    dst_path="/home/claude/corrected.jpg"
)
```

```bash
python scripts/correct_perspective.py
# Use view tool to confirm corrected.jpg has straight edges before continuing
```

> All subsequent steps use `corrected.jpg` after correction.

---

## Step 1: Data Extraction (Three items: colors + text + shapes)

### 1-A Color Extraction (Program runs)

```python
# scripts/extract_colors.py
import sys
from PIL import Image

def sample(img, x1, y1, x2, y2, n=8):
    x1,y1,x2,y2 = int(x1)+5,int(y1)+5,int(x2)-5,int(y2)-5
    if x2<=x1 or y2<=y1: x2,y2=x1+1,y1+1
    xs=[x1+(x2-x1)*i//(n-1) for i in range(n)]
    ys=[y1+(y2-y1)*i//(n-1) for i in range(n)]
    cols=[img.getpixel((x,y))[:3] for x in xs for y in ys]
    r=sorted(c[0] for c in cols)[len(cols)//2]
    g=sorted(c[1] for c in cols)[len(cols)//2]
    b=sorted(c[2] for c in cols)[len(cols)//2]
    return f"{r:02X}{g:02X}{b:02X}"

img_path = sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/uploads/your_image.jpg"
img = Image.open(img_path).convert("RGB")
W, H = img.size

print(f"Image size: {W} × {H} px")
print(f"Coordinate conversion: x\" = px_x × {10/W:.5f}   y\" = px_y × {5.625/H:.5f}")
print(f"                      w\" = px_w × {10/W:.5f}   h\" = px_h × {5.625/H:.5f}\n")

regions = {
    "Background":     (W*.4,  H*.4,  W*.6,  H*.6),
    "Header":         (W*.01, H*.01, W*.99, H*.13),
    "Title Text":     (W*.03, H*.02, W*.65, H*.11),
    "Content Area":   (W*.05, H*.18, W*.95, H*.82),
    "Footer":         (W*.01, H*.87, W*.99, H*.99),
}
print(f"{'Region':<12} {'hex':<8}  Sampling range (px)")
print("-" * 52)
for name,(x1,y1,x2,y2) in regions.items():
    print(f"{name:<12} #{sample(img,x1,y1,x2,y2)}    ({int(x1)},{int(y1)})→({int(x2)},{int(y2)})")
print("\n# Single point sampling: r,g,b=img.getpixel((x,y))[:3]; print(f'{r:02X}{g:02X}{b:02X}')")
```

```bash
python scripts/extract_colors.py /mnt/user-data/uploads/your_image.jpg
```

**Record all hex values**, copy directly in Step 3, no visual estimation.

---

### 1-B Text Extraction (OCR)

```python
# scripts/extract_text.py
import sys, subprocess
from PIL import Image

def ensure_deps():
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        return pytesseract
    except Exception:
        print("Installing tesseract-ocr...")
        subprocess.run(["apt-get","install","-y","-q",
                        "tesseract-ocr","tesseract-ocr-chi-sim"], check=True)
        subprocess.run([sys.executable,"-m","pip","install","pytesseract",
                        "--break-system-packages","-q"], check=True)
        import pytesseract
        return pytesseract

def ocr(img, x1, y1, x2, y2, scale=2, lang="chi_sim+eng"):
    crop=img.crop((int(x1),int(y1),int(x2),int(y2)))
    crop=crop.resize((crop.width*scale,crop.height*scale),Image.LANCZOS)
    raw=tess.image_to_string(crop,lang=lang).strip()
    return "\n".join(l for l in raw.splitlines() if l.strip())

tess=ensure_deps()
img_path=sys.argv[1] if len(sys.argv)>1 else "/mnt/user-data/uploads/your_image.jpg"
img=Image.open(img_path).convert("RGB")
W,H=img.size

print("=== Full Image Scan ===")
print(tess.image_to_string(img,lang="chi_sim+eng").strip())

regions={"Header":(W*.02,H*.01,W*.88,H*.13),"Footer Left":(W*.02,H*.87,W*.38,H*.99),
         "Footer Center":(W*.38,H*.87,W*.72,H*.99),"Footer Right":(W*.72,H*.87,W*.98,H*.99)}
print("\n=== Region Extraction ===")
for name,(x1,y1,x2,y2) in regions.items():
    print(f"\n[{name}] {repr(ocr(img,x1,y1,x2,y2))}")
print("\n# Custom: ocr(img, x1, y1, x2, y2, scale=2)")
```

```bash
python scripts/extract_text.py /mnt/user-data/uploads/your_image.jpg
```

> OCR uses **image as final authority**, mainly for quickly obtaining long text and numbers, avoiding manual typing errors.

---

### 1-C Shape Recognition + Text Direction Recognition (Visual, compare with references/shapes.md)

**Open `references/shapes.md`**, compare and identify each graphic and text label, record to table:

|ID|Position Description|Shape Constant|Arrow|Fill Color|Border Color|Inner Text|Text Direction|
|-|-|-|-|-|-|-|-|
|S1|Header background|`RECTANGLE`|No|8B1A1A|Same as fill|—|—|
|S2|Left flow node 1|`ROUNDED_RECTANGLE`|No|D8EAF5|A0C4E0|"Start"|Horizontal|
|S3|Node 1→Node 2 connector|`LINE`|Yes, triangle|888888|—|—|—|
|T1|Left area label|`RECTANGLE`|No|Dark blue|—|"Group Data Platform"|**Vertical**|
|…|…|…|…|…|…|…|…|

**Text direction judgment (confirm one by one when viewing image):**

```
Observe each text label:
  Text box width > height       → Horizontal (default, no vert needed)
  Text box height > width × 3   → Vertical, characters upright → use vert: "eaVert"
  Entire text block tilted 90°/270°    → Rotated horizontal → use rotate: 270
```

**Special attention to these common vertical labels** (narrow strip text on left/right sides of images are almost always vertical):

* Hierarchy area labels: "Group Data Platform", "Data Consumption", "Data Lake", "Data Source", etc.
* Right side vertical description strips: "Data Services", "Data Governance and Control", etc.

**Connector arrow judgment**:

* Thin line with solid/hollow small triangle at end → `LINE` + `endArrowType: "triangle"` or `"open"`
* Thick filled arrow shape → `RIGHT_ARROW` / `DOWN_ARROW` etc. shape constants
* Pure connector without arrow → `LINE`, don't set `endArrowType`

---

## Step 2: Visual Layout Planning

**Eyes on image**, divide slide into large regions, record inch coordinates for each block using conversion formula.

Coordinate system: Top-left origin, unit inches. Slide = 10" × 5.625".

**Conversion formula** (coefficients printed in Step 1-A, use directly):

```
x" = pixel_x  × (10    / image width px)
y" = pixel_y  × (5.625 / image height px)
w" = pixel_w × (10    / image width px)
h" = pixel_h × (5.625 / image height px)
```

**Region Record Table** (fill before writing code):

|Region|x"|y"|w"|h"|Notes|
|-|-|-|-|-|
|Header|0|0|10|0.65|Top edge aligned|
|Footer|0|5.0|10|0.625|Bottom edge aligned|
|Left content area|0.2|0.75|…|…|Estimate|
|…|…|…|…|…|…|

---

## Step 3: Code Implementation

> Each element's color from Step 1-A, text from Step 1-B, shape constant from Step 1-C, coordinates from Step 2. **No reliance on memory or guesswork**, all values have clear sources.

After writing each region, immediately mentally compare with original image before continuing to next block.

### Script Template

```javascript
// create_slide.js
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
let slide = pres.addSlide();

// ── Layer 1: Background ──────────────────────────────────────────────────────────
slide.background = { color: "FFFFFF" };  // ← Background color from Step 1-A

// ── Layer 2: Large background rectangles ───────────────────────────────────────────────────

// Header
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.65,
  fill: { color: "8B1A1A" }, line: { color: "8B1A1A", width: 0 }
});
// Header text (coordinates exactly match header, margin: 0)
slide.addText("[Step 1-B OCR result]", {
  x: 0, y: 0, w: 10, h: 0.65,
  fontSize: 22, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei",
  align: "left", valign: "middle",
  margin: 0,   // ← Rule 1: must be 0
});

// Footer
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 5.0, w: 10, h: 0.625,
  fill: { color: "8B1A1A" }, line: { color: "8B1A1A", width: 0 }
});
slide.addText("[Step 1-B OCR result]", {
  x: 0, y: 5.0, w: 10, h: 0.625,
  fontSize: 13, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei",
  align: "left", valign: "middle",
  margin: 0,
});

// ── Layer 3: Content graphics + Layer 4: Graphic text (alternate drawing, add text immediately after each shape) ──

// Example: Flow node
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {  // ← Shape constant from Step 1-C
  x: 1.4, y: 0.95, w: 2.4, h: 0.42,
  fill: { color: "D8EAF5" },
  line: { color: "A0C4E0", width: 1 },
  rectRadius: 0.05
});
slide.addText("Node text", {
  x: 1.4, y: 0.95, w: 2.4, h: 0.42,  // ← Rule 2: exactly matches shape above
  fontSize: 11, color: "333333",
  fontFace: "Microsoft YaHei",
  align: "center", valign: "middle",
  margin: 0,  // ← Rule 1
  wrap: true,
});

// Example: Connector (with arrow)
slide.addShape(pres.shapes.LINE, {
  x: 2.6, y: 1.37, w: 0, h: 0.25,    // Vertical line: w=0,h>0
  line: {
    color: "888888", width: 1.5,
    endArrowType: "triangle",          // ← Step 1-C: use triangle/open if arrow present, omit if no arrow
  }
});

pres.writeFile({ fileName: "/mnt/user-data/outputs/output.pptx" });
console.log("Done!");
```

```bash
NODE_PATH=/home/claude/.npm-global/lib/node_modules node create_slide.js
```

---

## Step 3.5: Pre-flight Check (Required before execution, do not skip)

> **Core principle**: Don't execute immediately after writing script. Do paper verification first—"render" script coordinates in mind, compare with original image, fix issues on the spot, then submit for execution. This step intercepts most overlap, out-of-bounds, and text overflow issues before execution.

---

### Check A: Automated Out-of-bounds + Overlap Scan

Run `scripts/preflight.py`, automatically parse all element coordinates in script and report issues:

```bash
python scripts/preflight.py create_slide.js
```

Output explanation:

* `❌ Out of bounds`: Elements with `x+w > 10` or `y+h > 5.625` → **Must fix before execution**
* `⚠️ Suspected overlap`: Non-parent-child rectangle intersections between two elements → Manual confirmation if reasonable
* `📋 Coordinate summary`: All elements sorted by y, convenient for comparing region proportions with original image

**Any ❌ out of bounds must be fixed and re-run until no ❌ before entering Step 4.**

---

### Check B: Text Capacity Manual Verification

For **all `addText`** in script, verify one by one if text fits.

#### Horizontal Text

```
Required width = character count × (fontSize / 72 × 1.1) inches
Required height = line count × (fontSize / 72 × 1.5) inches
Requirement: w ≥ required width, h ≥ required height
```

**Quick reference (fontSize = 12pt)**:

|Content|Min w|Min h|
|-|-|-|
|4 Chinese characters, single line|0.74"|0.25"|
|6 Chinese characters, single line|1.10"|0.25"|
|4 Chinese characters, two lines|0.74"|0.45"|
|10 English characters|0.80"|0.25"|

#### Vertical Text (`vert: "eaVert"`)

```
Required width = fontSize / 72 × 1.4 inches (single column character width)
Required height = character count × (fontSize / 72 × 1.3) inches
Requirement: w ≥ required width, h ≥ required height
```

**Quick reference (fontSize = 14pt)**:

|Vertical characters|Min w|Min h|
|-|-|-|
|4 chars|0.27"|1.05"|
|6 chars|0.27"|1.57"|
|8 chars|0.27"|2.10"|

**Text doesn't fit → Fix before execution**: Reduce `fontSize`, expand `w`/`h`, or use `breakLine` for manual line breaks.

---

### Check C: Region-by-Region Proportion Verification (Compare with original image)

Use coordinate summary table from `preflight.py` output, compare with original image for proportion verification:

```
1. Horizontally slice original image into major horizontal regions (header, content area, footer…)
2. Visually estimate each region's percentage of total slide height
3. Compare with corresponding element's h/5.625 in summary table, see if close to visual percentage
4. Regions with deviation > 15% need re-estimation of y and h

Focus on right-side truncation check:
  → Rightmost element's x+w ≤ 9.8" (leave 0.2" safety margin)
  → When right side has vertical label bar, confirm its x doesn't exceed 10 - label width
```

---

### Check D: Parent-Child Container Relationship Verification

For nested regions (large background box containing multiple child elements), check all child elements are within parent box range:

```
Child element requirements:
  child.x        ≥ parent.x
  child.x + child.w ≤ parent.x + parent.w
  child.y        ≥ parent.y
  child.y + child.h ≤ parent.y + parent.h
```

Most common violation: Last column of nested grid `x+w` exceeds parent box right boundary. Fix method:

```javascript
// Recalculate grid column width, ensure last column doesn't exceed bounds
const cellW = (parentW - padLeft - padRight) / cols;
const cellX = (i) => parentX + padLeft + i * cellW;
```

---

### Pass Criteria

All satisfied before entering Step 4:

|Item|Pass Criteria|
|-|-|
|✅ No out of bounds|preflight.py has no ❌ output|
|✅ Text fits|All text boxes w/h satisfy capacity calculation|
|✅ Region proportions reasonable|Each region height deviation from original visual ≤ 15%|
|✅ Child elements within parent|All nested elements don't exceed parent box boundary|
|✅ Overlaps confirmed|preflight.py ⚠️ warnings all manually confirmed reasonable|

Fix unpassed items directly in script, **re-run preflight.py after fix**, until all pass.

---

## Step 4: Implementation Methods for Various Element Types

### 4.1 Various Nodes (Shape + text must have identical coordinates)

```javascript
// Rectangle node (processing step)
slide.addShape(pres.shapes.RECTANGLE, { x:1.0, y:1.0, w:2.0, h:0.5,
  fill:{color:"F5F5F5"}, line:{color:"AAAAAA",width:1} });
slide.addText("Processing Step", { x:1.0, y:1.0, w:2.0, h:0.5,
  fontSize:11, color:"333333", fontFace:"Microsoft YaHei",
  align:"center", valign:"middle", margin:0, wrap:true });

// Diamond node (decision branch)
slide.addShape(pres.shapes.DIAMOND, { x:1.0, y:2.0, w:2.0, h:0.6,
  fill:{color:"FFF2CC"}, line:{color:"CCAA00",width:1} });
slide.addText("Yes?", { x:1.0, y:2.0, w:2.0, h:0.6,
  fontSize:11, color:"333333", fontFace:"Microsoft YaHei",
  align:"center", valign:"middle", margin:0, wrap:true });

// Ellipse node (start/end)
slide.addShape(pres.shapes.OVAL, { x:1.2, y:0.3, w:1.6, h:0.45,
  fill:{color:"D5E8D4"}, line:{color:"82B366",width:1} });
slide.addText("Start", { x:1.2, y:0.3, w:1.6, h:0.45,
  fontSize:11, color:"333333", fontFace:"Microsoft YaHei",
  align:"center", valign:"middle", margin:0 });
```

### 4.2 Connectors (Choose arrow type based on Step 1-C)

```javascript
// Connector with arrow (solid triangle at end)
slide.addShape(pres.shapes.LINE, { x:2.0, y:1.5, w:0, h:0.3,
  line:{ color:"888888", width:1.5, endArrowType:"triangle" } });

// Connector with arrow (open arrow at end)
slide.addShape(pres.shapes.LINE, { x:2.0, y:1.5, w:0, h:0.3,
  line:{ color:"888888", width:1.5, endArrowType:"open" } });

// Pure connector without arrow
slide.addShape(pres.shapes.LINE, { x:2.0, y:1.5, w:0, h:0.3,
  line:{ color:"CCCCCC", width:1 } });
```

> `endArrowType` options: `"triangle"` (solid), `"open"` (hollow), `"stealth"` (stealth), `"diamond"`, `"oval"`, `"none"`

### 4.3 Dual-Theme Nodes (Main title + subtitle)

```javascript
slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x:0.55, y:1.62, w:4.1, h:0.55,
  fill:{color:"E8E0F0"}, line:{color:"C0A8D8",width:1}, rectRadius:0.05 });
slide.addText([
  { text:"Main Title", options:{ breakLine:true } },
  { text:"Subtitle description, can be smaller", options:{ fontSize:7.5, color:"666666" } }
], { x:0.55, y:1.62, w:4.1, h:0.55,
  fontSize:10, color:"444444", fontFace:"Microsoft YaHei",
  align:"center", valign:"middle", margin:0, wrap:true });
```

### 4.4 Annotation Bubbles

```javascript
slide.addShape(pres.shapes.RECTANGULAR_CALLOUT, { x:1.0, y:0.5, w:2.5, h:0.6,
  fill:{color:"FFFDE7"}, line:{color:"CCAA00",width:1} });
slide.addText("Annotation text", { x:1.0, y:0.5, w:2.5, h:0.6,
  fontSize:10, color:"333333", fontFace:"Microsoft YaHei",
  align:"center", valign:"middle", margin:0, wrap:true });
```

### 4.5 Mixed Style Text (Links + normal)

```javascript
slide.addText([
  { text:"Link text", options:{ color:"1155CC", underline:{style:"sng"} } },
  { text:" and ",    options:{ color:"333333" } },
  { text:"Another link", options:{ color:"1155CC", underline:{style:"sng"} } },
  { text:" is description.", options:{ color:"333333" } }
], { x:5.55, y:3.3, w:4.2, h:0.35,
  fontSize:12, fontFace:"Microsoft YaHei", margin:0 });
```

### 4.6 Vertical Text Labels (Standard for sidebar area labels)

**Applicable scenarios**: Narrow strip area labels on left or right side of image, such as "Group Data Platform", "Data Lake", "Data Services", etc.

```javascript
// ── Vertical text: vert: "eaVert" (each character upright, read top to bottom) ───────────────────

// Vertical label with background (most common form)
slide.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0.65, w: 0.4, h: 3.5,        // Width ~0.35-0.5", height fills area
  fill: { color: "1F4E79" }, line: { color: "1F4E79", width: 0 }
});
slide.addText("Group Data Platform", {
  x: 0, y: 0.65, w: 0.4, h: 3.5,        // ← Exactly matches shape
  fontSize: 14, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei",
  align: "center", valign: "middle",
  margin: 0,
  vert: "eaVert",                         // ← Chinese vertical, characters upright
});

// Pure vertical text without background
slide.addText("Data Services", {
  x: 9.2, y: 1.0, w: 0.35, h: 2.0,
  fontSize: 12, color: "2E75B6",
  fontFace: "Microsoft YaHei",
  align: "center", valign: "middle",
  margin: 0,
  vert: "eaVert",
});
```

**Dimension rules**:

* `w` (width) = Single character width + small margin, approximately `fontSize / 72 * 1.4` (inches)

  * fontSize 12pt → w ≈ 0.28", suggest 0.35"
  * fontSize 14pt → w ≈ 0.33", suggest 0.4"
  * fontSize 16pt → w ≈ 0.38", suggest 0.45"
* `h` (height) = Actual height of corresponding region, converted from image

---

### 4.7 Correct Handling of Compressed Horizontal Labels

**Applicable scenarios**: Horizontal region labels at top or bottom of image (such as "Data Consumption", "Data Source"), text is normal horizontal but text box is narrow.

```javascript
// ── Correct: Horizontal labels need sufficient width, don't compress to achieve vertical effect ──────────────────────

// ❌ Wrong: Width too narrow, text forced to wrap into "vertical column", actually horizontal compression
slide.addText("Data Consumption", {
  x: 0, y: 0, w: 0.3, h: 0.8,    // w too narrow, each character auto-wraps
  fontSize: 16, ...
});

// ✅ Correct: Give sufficient width to accommodate all text, if space insufficient reduce font size
slide.addText("Data Consumption", {
  x: 0, y: 0, w: 0.8, h: 0.8,    // w sufficient for horizontal text
  fontSize: 14, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei",
  align: "center", valign: "middle",
  margin: 0,
  wrap: false,                     // ← Prohibit wrapping, ensure single line display
});

// ✅ If region really narrow must wrap, use breakLine for manual line break control
slide.addText([
  { text: "Data", options: { breakLine: true } },
  { text: "Consumption" }
], {
  x: 0, y: 0, w: 0.45, h: 0.8,
  fontSize: 14, bold: true, color: "FFFFFF",
  fontFace: "Microsoft YaHei",
  align: "center", valign: "middle",
  margin: 0,
});
```

**Horizontal vs Vertical Quick Reference**:

|Original Effect|Characters upright?|Correct approach|
|-|-|-|
|Text left to right, normal reading|✅ Upright|Horizontal, no `vert` needed|
|Text top to bottom, each character upright|✅ Upright|Vertical, add `vert: "eaVert"`|
|Entire text block rotated (horizontal but on side)|❌ On side|Add `rotate: 270`|
|Text wraps into column but characters horizontal (compressed)|✅ Upright but squeezed|Horizontal + manual `breakLine` + appropriate `w`|

```javascript
const slideW = 10, slideH = 5.625;

// Horizontal center
const x = (slideW - w) / 2;

// Node bottom center (connector start point)
const lineX = nodeX + nodeW / 2;
const lineY = nodeY + nodeH;

// n elements evenly spaced (total range rangeW, start x0, each width itemW)
const gap = (rangeW - n * itemW) / (n + 1);
const itemX = (i) => x0 + gap + i * (itemW + gap);
```

---

## Step 5: Visual QA + Correction Loop (Required, max 3 iterations)

### Generate Preview Image

```bash
python /mnt/skills/public/pptx/scripts/office/soffice.py \
  --headless --convert-to pdf /mnt/user-data/outputs/output.pptx

rm -f /home/claude/slide-*.jpg
pdftoppm -jpeg -r 150 /home/claude/output.pdf /home/claude/slide
ls -1 /home/claude/slide*.jpg
```

Use `view` tool to view preview image, **compare side-by-side with original image**, execute following two-phase checks.

---

### Phase 1: Layout Compliance

|Check Item|Judgment Criteria|
|-|-|
|Text out of box|Text exceeds graphic boundary or truncated|
|Text box exceeds graphic|Text box dimensions larger than underlying shape, text appears outside shape|
|**Vertical text correct**|Sidebar label characters upright (`eaVert`); horizontal compressed text not mistakenly made vertical|
|**Horizontal text compressed**|Horizontal label `w` sufficient, text not overlapping or misaligned due to insufficient width|
|Elements unexpectedly overlapping|Text covered by graphics, or graphics block other text|
|Connector arrow direction|Arrow direction matches original image (start/end reversed?)|
|Arrangement orderly|Peer elements aligned, evenly spaced, no obvious misalignment|
|Spacing reasonable|Adjacent element spacing ≥ 0.1", no edge touching|
|Page margins|Content distance from slide edge ≥ 0.2" (header/footer excepted)|

### Phase 2: Fidelity to Original Image

|Check Item|Judgment Criteria|
|-|-|
|🎨 Colors|Background, graphic fill, text color match original image|
|🔷 Shape types|Rectangle/rounded/diamond/ellipse etc. match original image|
|📏 Proportions|Element width/height ratios, region proportions match original image|
|↔️ Arrow types|Solid/hollow/thick arrow shapes match original image|
|🔤 Font size hierarchy|Title/body/annotation font size relationships match original image|
|↔️ Alignment|Text left/center/right alignment matches original image|

---

### Correction Loop Control (Strictly Enforced)

```
Correction counter = 0

LOOP:
  Generate preview → Phase 1 check → Phase 2 check

  if no issues → Deliver, end

  if correction counter >= 3:
    Deliver directly, note: "Completed 3 correction rounds, following issues unresolved: [list]"
    End

  Modify create_slide.js corresponding lines
  Regenerate pptx and preview
  Correction counter += 1
  → Continue LOOP
```

**Explain each round**: ① Layout issues found ② Fidelity issues found ③ Which code modified ④ Round N/3

---

## Step 6: Common Errors and Fixes

|Error Phenomenon|Cause|Fix|
|-|-|-|
|Vertical label characters on side|Used `rotate: 270` instead of `vert`|Use `vert: "eaVert"` instead|
|Vertical label characters overlapping|Text box `w` too narrow without `vert`|Add `vert: "eaVert"`, set `w` to 0.35-0.5"|
|Horizontal label text wraps into column|Text box `w` too narrow, text forced to wrap|Increase `w` for single line, or use `breakLine` for manual line break control|
|Horizontal label added `vert` causing chaos|Misjudged as vertical|Remove `vert`, ensure `w` wide enough|
|Text position offset|Forgot `margin: 0`|Add `margin: 0` to all addText|
|Text exceeds graphic boundary|Text box dimensions don't match shape|Align text box x/y/w/h exactly with shape|
|Text expanded text box|Didn't set `wrap: true` and fixed dimensions|Add `wrap: true`, appropriately reduce font size|
|Arrow direction reversed|`endArrowType` on wrong side|Swap `begin/endArrowType`, or adjust x/y/w/h direction|
|Color display wrong|Added `#` before hex|Remove `#`: `"FF0000"` ✅|
|Garbled/Chinese characters as blocks|Font not set|Add `fontFace: "Microsoft YaHei"`|
|ROUNDED_RECTANGLE corner has white edge|Text box covers corner|Text box same coordinates as shape + `margin:0`|
|Diamond text crooked|valign not set|Add `align:"center", valign:"middle"`|
|Color sampling deviation|Sampled border/shadow pixels|Move sampling coordinates to region center, 10px from edge|

### Strategy B Specific

|Error Phenomenon|Cause|Fix|
|-|-|-|
|Triangle/shape has obvious hard edge outline|`line.width` not set to 0|Add `line: { color: same as fill, width: 0 }`|
|Glow layers reversed (outer dark inner light)|`transparency` value order wrong|Outer `transparency` smaller (more opaque) → swap values|
|Arc decorative ring not closed|N value insufficient or angle range wrong|Confirm `theta` from 0 to `2 * Math.PI`, appropriately increase N|
|Arc element position not on ellipse|cx/cy/rx/ry estimation wrong|Recalculate center and radius from pixel coordinates|
|Cutout white ellipse has color gap|White ellipse coverage insufficient|Slightly expand white ellipse w/h, ensure complete inner ring coverage|
|Column structure asymmetrical|x coordinate calculation error|Use center column as benchmark, mirror symmetric offset left-right|
|Leader corner has gap|Vertical and horizontal line endpoint coordinates not continuous|Vertical line start y = horizontal line y; horizontal line start x = vertical line x|

---

## References

* pptxgenjs API: `references/pptxgenjs-cheatsheet.md`
* Shape recognition and constants quick reference: `references/shapes.md`
