# HTML → Editable PPTX Common Failure Modes / QA Heuristics

The most common problem with this type of conversion is not "generation failure" but **it generates, but details quietly break behind the scenes**.

## 1. Text Issues

### 1.1 Text box height insufficient / bottom overflow
Typical symptoms:
- Last line of a paragraph is clipped
- Text just barely touches the rounded corner or border
- Text looks fine in HTML but overflows after line-wrapping in PowerPoint

High-risk causes:
- PowerPoint font metrics differ from the browser
- Mixed Chinese and English text causes line-break position shifts
- Text box has fixed height, but content length is dynamic
- `fit: 'shrink'` / `resize` is unreliable — in many cases it only triggers after opening the PPT for editing

### 1.2 Large title pressing down text below
Typical symptoms:
- Insufficient vertical spacing between title, subtitle, and description
- Once the title wraps to two lines, it crowds the description below

High-risk causes:
- Title height assumed for single line
- Title font too large, or font fallback increases character width

### 1.3 Chip / pill / small card text gets clipped
Typical symptoms:
- Text is flush against the chip edge
- Insufficient top/bottom padding inside capsule shapes
- One or two extra characters in a small card title or body cause overflow

High-risk causes:
- Chip height is too small
- No explicit default padding set
- Text scaling is unreliable

## 2. Layout Issues

### 2.1 Vertical spacing drift between modules
Typical symptoms:
- Everything looks correct at the top, but modules start colliding toward the bottom
- One middle module gets slightly taller, pushing all subsequent modules downward

High-risk causes:
- Fixed-height stacking
- Content growth in one block without adjusting subsequent block coordinates

### 2.2 Arrow / connector bridges between left and right columns misalign
Typical symptoms:
- Arrow does not align to centerline
- Arrow direction is reversed
- Arrow is not visually centered

High-risk causes:
- Connection points hard-coded
- Column width adjustments not propagated to arrow coordinates

### 2.3 Borders, rounded corners, and shadows competing with content for space
Typical symptoms:
- Content is not technically out of bounds, but visually feels cramped
- Text is too close to the border, unlike a professional PPT

High-risk causes:
- Only checking "whether overflowing", not checking safe padding margins
- Rounded blocks have smaller usable area than rectangles

## 3. Font and Rendering Issues

### 3.1 Font fallback increases character width
Typical symptoms:
- Code uses PingFang / Microsoft YaHei, but the target machine does not have them
- PowerPoint auto-falls back to Calibri / Arial / other fonts, changing all line breaks

### 3.2 Line-height / paragraph spacing inconsistent with HTML
Typical symptoms:
- Looks loose in HTML, feels cramped in PPT
- Last line of a list overflows

High-risk causes:
- Browser CSS line-height ≠ PowerPoint paragraph model
- Default before/after paragraph spacing not explicitly controlled

## 4. Engine Known Limitations

### PptxGenJS
- `fit: 'shrink'` / `resize` does NOT mean perfect auto-scaling at generation time
- Text box margin, lineSpacing, and fontFace should all be explicitly specified where possible
- Complex HTML cannot be understood as browser layout — only semantic mapping is feasible

References:
- PptxGenJS README notes on `fit`
- GitHub issues: #544, #779, #991, #330

### python-pptx
- Weaker control over text wrapping and font metrics
- `word_wrap`, line spacing, top margin, and other behavior often differ

References:
- python-pptx issues: #709, #710, #162

## 5. Recommended QA Layer for the Skill

At minimum, check:
1. Whether estimated text line count exceeds box height
2. Whether title and subtitle risk collision
3. Whether bullet lists exceed safe height
4. Whether chip / small card text is near the clipping threshold
5. Whether total vertical stack height exceeds container height
6. Whether arrow direction and connection position conform to preset rules
7. Whether reliance on unstable mechanisms like `fit: 'shrink'` exists

## 6. Recommended QA Tiers

### A. Semantic pre-check (doable now)
Estimate risk from preset box sizes, font sizes, and copy length.

### B. Structural audit (doable now)
Check generated object coordinates, spacing, overflow, and overlap.

### C. Render verification (future enhancement)
Generate PPT thumbnails for hotspot checks, optionally with OCR / visual model.
