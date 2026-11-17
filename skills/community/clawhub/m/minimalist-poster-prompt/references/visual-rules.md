# Visual Rules — Minimal Zine Poster

This file contains the detailed rendering rules for the Standard Mode Prompt
Compiler. Load this file before writing any image-generation prompt.

## First-Principles Prompt Fields

Every Standard Mode prompt must answer these rendering questions in this order:

### 1. Canvas

What is the output frame and base surface?

- Tall vertical 3:5 phone-poster.
- Full-frame aged paper.
- No border, no mockup.

### 2. Attention Geometry

Where does the eye go and how much is empty?

- 70%-90% plain paper.
- One visual cluster occupying about 8%-25%.
- Placed center, upper-middle, lower-middle, lower-left, or upper-right.
- No edge-hugging.

### 3. Image Anchor

What is the one imageable subject?

- Convert the user's theme into one object, fragment, photo crop, specimen,
  cutout, silhouette, old printed illustration, texture window, or small
  conceptual relation.

### 4. Anchor Treatment

What material process makes the anchor belong to paper?

- Grayscale photos and paper fragments may use low contrast, photocopy
  softness, torn edge, softened edge, halftone, scanline, risograph grain,
  xerox wear, ink bleed, or slight misregistration.
- Do not apply low saturation or low contrast to the chosen color anchor.

### 5. Typography System

How does text behave visually?

- Small serif/typewriter/monospaced type.
- One short readable phrase.
- Optional tiny date/location/weather and signature.
- Semi-legible microtext or fragmented letters.
- Text can drift, press against the image edge, blur, or misregister.

### 6. Color Logic

What is the restrained accent strategy?

- Paper tones plus gray/black support one unmistakably high-chroma anchor.
- Prefer cobalt or ultramarine; rotate through cyan, violet, magenta-pink,
  lemon yellow, pear green, orange, or tomato red.
- The color may be the subject, a flat silhouette, an irregular cutout, a
  substantial block, a partial-color photo region, or bold fragmented type.
- It must not be reduced automatically to a tiny dot or hairline.

### 7. Reproduction Texture

What print/scanning process defines the whole image?

- Flat orthographic scanned-paper appearance.
- Matte absorbent paper.
- Diffuse light.
- Low-to-medium contrast.
- No hard shadow.
- No 3D depth.

### 8. Emotional Temperature

What should the viewer feel before identifying the object?

- Quiet, poetic, nostalgic, sparse, diary-like, archival, distant,
  memory-like.
- Japanese/Korean indie zine or minimal editorial mood.

### 9. Hard Avoids

What must not appear?

- Full-bleed scene.
- Commercial headline.
- Product ad.
- Logo/CTA.
- Glossy mockup.
- Clean UI white.
- Cinematic lighting.
- 3D.
- Neon.
- Cute cartoon.
- Fashion editorial drama.
- Dense scrapbook.
- Too many colors.
- Long clean text.

## Standard Color Engine

This section defines the color strategy for Standard Mode.

- Default to one visibly saturated, opaque chromatic ink anchor. Use wording
  such as `fully saturated cobalt-blue risograph ink`, `opaque ultramarine
  cutout`, `vivid pear-green flat silhouette`, or `clean tomato-red printed
  block`.
- Keep the paper, grayscale photo, microtext, and secondary marks subdued.
  Preserve saturation in the color anchor even when adding grain, halftone,
  ink bleed, or misregistration.
- The high-chroma area should occupy roughly 0.8%-2.5% of the whole canvas or
  15%-35% of the small visual cluster. It must remain visible when the image
  is viewed as a thumbnail.
- Color can carry the subject itself. Prefer a colored tree, fruit, shell,
  flower, geometric cutout, window, poster fragment, or image panel over a
  gray object with one colored registration tick.
- For a single image, use a substantial color anchor by default. For batches,
  at least 60% of images must use a colored subject, cutout, or block; the
  remaining images may use dots, hairlines, or colored type for rhythm.
- Do not use `near-monochrome`, `no strong accent`, `pale accent`, `muted
  accent`, `faded accent`, or `pastel accent` unless the user explicitly
  requests monochrome, muted, or pastel output.
- Do not describe the entire image as low saturation. Apply `low contrast` and
  `muted grayscale` only to paper, photos, and secondary ink.
- Use only one main high-chroma hue per image. A tiny secondary hue is allowed
  only when it supports the subject and does not make the poster commercially
  colorful.

## Standard Prompt Shape (Detailed)

Write the final Standard Mode prompt as four compact paragraphs:

**Paragraph 1 — Canvas + Paper + Negative Space + Cluster:**

Describe the vertical 3:5 aged-paper canvas, the 70%-90% negative space, the
single visual cluster's size (8%-25%), and its position on the canvas. Example
wording: `Vertical 3:5 aged-paper poster, full-frame, no border. About 85% of
the canvas is plain off-white paper. One small visual cluster sits
lower-center, occupying roughly 15% of the frame.`

**Paragraph 2 — Subject + Anchor + Treatment:**

Name the one imageable subject derived from the user's theme, its anchor type
(photo, cutout, silhouette, block, specimen, etc.), and the material treatment
(xerox, halftone, torn edge, risograph grain, ink bleed, etc.). Do not apply
low saturation to the color anchor. Example wording: `A single small cobalt-blue
risograph-printed leaf sits at the lower-center, edges softened by photocopy
wear, slight ink bleed on the stem. The leaf itself is fully saturated.`

**Paragraph 3 — Typography + Accent + Print Defects:**

State the exact high-chroma hue, its material form, and its approximate visual
share. Describe the typography behavior and the print/scan texture. Example
wording: `Small typewriter text in near-black serif, one short phrase "august
rain" pressed against the upper edge of the leaf, semi-legible microtext
scattered faintly. The cobalt-blue ink anchor occupies about 1.5% of the canvas
and 25% of the visual cluster. Risograph grain, scan noise, and paper fibers
across the whole image.`

**Paragraph 4 — Flat Scan Mood + Avoid-List:**

Describe the flat scanned-paper mood and list what must not appear. Example
wording: `Flat orthographic scanned-paper appearance, matte absorbent paper,
diffuse light, no hard shadow, quiet archival memory mood, Japanese indie zine
aesthetic. Avoid: full-bleed scene, commercial headline, glossy mockup, 3D
rendering, cinematic lighting, neon, cute cartoon, dense scrapbook, long clean
text.`

## Reminders

- This structure is more important than reciting every rule.
- Prefer a concrete, imageable prompt over a long style essay.
- Keep in-image text short — image models distort long text.
- If the recipe becomes too dense, simplify typography or color treatment
  first.
- The color anchor must survive at thumbnail scale.
