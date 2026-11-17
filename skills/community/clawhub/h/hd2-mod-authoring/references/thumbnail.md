# Dominator thumbnail (rebuild + verify)

The shipped thumbnail is `thumbnail.png` (2048×2048, the manifest `IconPath`).
`branding/dominator_base_thumbnail.jpg` is 1024×1024 and is the older pre-render
base — not the rebuild source. The rebuild source is the clean weapon cutout
`archive/dominator_render.png` (3840×2160 RGBA, weapon bbox x[570,3482]
y[543,1528], ~2.96:1 aspect; alpha>200 covers ~18% of the frame).

## When to rebuild vs tweak

- **Tweak** (add or reword one line of text): edit the shipped `thumbnail.png` in
  place. Do not regenerate.
- **Redesign** (operator asks to redo it — restructure boxes, add a features/specs
  panel): rebuild from `archive/dominator_render.png`, never from the jpg, and never
  as a side effect of a code/manifest edit. Generate the image with PIL against the
  real render cutout and the gold-on-dark brand, then verify it (below).

## Layout (redesigned 2026-10-06)

- Top-left panel — **FEATURES**: Arming Distance Toggle (via Weapon Wheel), Full
  Auto Fire Mode (via Weapon Wheel), Four WH40k Bolter Sound Effects, Shodan
  Editor Compatible.
- Top-right panel — **SPECS**: Heavy Armor Penetrating, Explosive, 380 m/s
  Velocity, 532 m Max Range, 325 Impact + 175 Explosive.
- Center: weapon hero. Bottom: `JAR-5 DOMINATOR` / `RECHAMBERED` title with
  flanking gold rules.

Both panels must be **identical in style** (same height, same gold border width,
same header + gold rule) and every line needs real vertical spacing. The earlier
version's two boxes ("BOLTER SOUND" top-left, "ARMING TOGGLE" top-right) had
mismatched fronts, and the Bolter Sound box's two lines sat directly on top of
each other. Match the panels and measure line spacing — do not hand-place text.

**A sub-annotation line must be visually attached to ITS OWN feature.** When a
feature carries a small qualifier ("Arming Distance Toggle" → "via Weapon
Wheel"), LEFT-INDENT the sub-line directly under its own title and give it an
explicit block gap before the next feature. Right-aligning the sub-line — or
stacking it only ~12 px above the next feature — makes it read as annotating the
feature BELOW it (the operator caught "you put 'via weapon wheel' on full
auto"). Lay out per-feature with explicit metrics — `title_h + GAP_SUB + sub_h +
GAP_BLOCK` — not a single shared line-height that lets the sub-line collide with
the next block. This cost two rebuilds (right-aligned, then too-close).

**Multiple sub-lines inflate the panel and can overflow the bottom border.**
Adding a second "via Weapon Wheel" pushed the last feature below the panel
edge. Tighten `GAP_SUB` (~4 px) and `GAP_BLOCK` (~16 px) when more than one
feature carries a qualifier, then verify the last line still has ~35 px of
breathing room above the panel border — measure text extent, do not trust a
count of drawn strings.

## Design tokens

- Gold `#E8B64A` (232,182,74); light gold `#F3D38A`; dim gold `#C4963A`.
- Background near-black `#0b0b0d` → `#070709`; body text near-white `#E8E6E0`.
- Fonts: `/usr/share/fonts/truetype/ibm-plex/IBMPlexSansCondensed-Bold.ttf`
  (title/headers) and `IBMPlexSansCondensed-SemiBold.ttf` (body). Condensed
  weights keep the longest feature ("Four WH40k Bolter Sound Effects") on one line.

## Verify a generated/edited image without vision

The running model may not support images (`view_image` then returns "Current
model does not support images", and it rejects `/tmp` paths regardless). Verify
programmatically instead of eyeballing:

- **Text present and placed** — `tesseract img.png stdout tsv` prints per-word
  bounding boxes (`left top width height conf text`); `--psm 11` for sparse
  layout, `--psm 6` for block text. Confirm every expected string appears once,
  at its expected region, with high conf. For a sub-annotation line, confirm it
  OCRs at a `top` directly below its OWN feature (roughly `parent_top + font +
  gap`), not right-aligned or within ~15 px of the NEXT feature's `top` — a
  right-aligned sub-line is a mis-attribution bug, not an overlap bug.
- **No squish / no wrap** — measure each line with PIL
  `ImageFont.truetype(path, size).getlength(text)` against the panel's inner
  width; shrink the font until the longest line fits on one line, and keep
  line height >= font size + ~20 px so lines never sit on top of each other.
- **No overlap** — after compositing, count gold text pixels inside the weapon
  band (must be ~0), and confirm both panels' borders land at the same top y via
  a numpy gradient/edge pass. A band where two text rows overlap shows up as a
  bright strip with no dark gap.

A passing check: every feature/spec/title string OCRs at its expected region, no
line wraps or overlaps, and both panels match in height and border.
