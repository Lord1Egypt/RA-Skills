# Motif Patterns — Path Recipes for Logo Designers

These are reusable path fragments distilled from the Simple Icons corpus. Combine them (as sub-paths of one `d` string) to compose most product logos on the 24×24 canvas.

> All snippets assume the standard `viewBox="0 0 24 24"` and are the **path `d` value only** (no wrapping `<path>` tag).

---

## Roundels (full disk, ring, dot)

**Full disk (radius 12, touches all 4 sides):**
```
M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0Z
```

**Ring (outer r=12, inner r=8) using nonzero fill and reverse-wound inner circle:**
```
M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0ZM12 4a8 8 0 1 1 0 16 8 8 0 0 1 0-16Z
```

**Center dot (r=2):**
```
M12 10a2 2 0 1 0 0 4 2 2 0 0 0 0-4Z
```

---

## Rounded squares (app-icon container feel)

**24×24 rounded square, radius ≈ 4:**
```
M4 0h16a4 4 0 0 1 4 4v16a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4V4a4 4 0 0 1 4-4Z
```

**Squircle-ish (r=6, more Apple-app-icon feel):**
```
M6 0h12c3.314 0 6 2.686 6 6v12c0 3.314-2.686 6-6 6H6c-3.314 0-6-2.686-6-6V6c0-3.314 2.686-6 6-6Z
```

---

## Letterforms (single-letter monogram)

Simple Icons has many single-letter marks (Visa "V", npm inner "N", Google "G"). Build letters as filled outlines — think of each character as a closed shape, not a stroke.

**Broad-stem "N" (touches top & bottom):**
```
M3 0h4l10 15V0h4v24h-4L7 9v15H3Z
```

**Broad-stem "H":**
```
M3 0h4v9h10V0h4v24h-4v-11H7v11H3Z
```

**Circle-inspired "O" ring** — reuse the ring snippet above.

**Wordmark caveat**: this skill emits **only symbol marks, not wordmarks**. For a wordmark request, degrade to the strongest single letter of the product name.

---

## Chevrons, arrows, play triangles

**Play triangle (media):**
```
M8 5v14l11-7Z
```

**Upward chevron:**
```
M2 16 12 6l10 10-2.5 2.5L12 11l-7.5 7.5Z
```

**Round-tripped sync arrows (two arcs + arrowheads):**
```
M4 12a8 8 0 0 1 14-5.3l2-2V12h-6l2.3-2.3A6 6 0 0 0 6 12ZM20 12a8 8 0 0 1-14 5.3l-2 2V12h6l-2.3 2.3A6 6 0 0 0 18 12Z
```

---

## Waveforms / spark / signal

**3-bar signal:**
```
M4 14h4v6H4Zm6-4h4v10h-4Zm6-6h4v16h-4Z
```

**Waveform (sinusoid slice):**
```
M0 12c3-8 6-8 9 0s6 8 9 0 6-8 6 0-2 12-6 12-6-4-9-12-6-12-4-4-4-6-4 6-4Z
```

**Spark / four-point star:**
```
M12 2 14 10 22 12 14 14 12 22 10 14 2 12 10 10Z
```

---

## Speech / chat bubbles

**Rounded rectangle bubble with tail:**
```
M4 3h16a3 3 0 0 1 3 3v9a3 3 0 0 1-3 3h-6l-6 5v-5H4a3 3 0 0 1-3-3V6a3 3 0 0 1 3-3Z
```

---

## Gears, sun, badges

**8-tooth gear (with center hole):**
```
M12 2l2 3 3-1 1 3 3 1-1 3 3 2-3 2 1 3-3 1-1 3-3-1-2 3-2-3-3 1-1-3-3-1 1-3-3-2 3-2-1-3 3-1 1-3 3 1ZM12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8Z
```

**16-ray sun** (short + long alternating rays, plus center disk).

---

## Shields, chevrons of protection (security / trust)

**Shield outline:**
```
M12 0 3 4v8c0 5.6 3.9 10.7 9 12 5.1-1.3 9-6.4 9-12V4Z
```

---

## Data / DB stacked cylinders

**3-disk stack:**
```
M4 5c0-2 3.6-4 8-4s8 2 8 4-3.6 4-8 4-8-2-8-4Zm0 6c1.8 1.2 4.6 2 8 2s6.2-.8 8-2v4c0 2-3.6 4-8 4s-8-2-8-4Zm0 7c1.8 1.2 4.6 2 8 2s6.2-.8 8-2v1c0 2-3.6 4-8 4s-8-2-8-4Z
```

---

## Combining motifs — best practices

1. **Rule of one visual idea** — a single dominant motif reads best at 16 px. Combining more than 2 motifs almost always fails the small-size readability check.
2. **Golden-ratio nesting** — inner shapes ≈ 0.618 × outer bounding box.
3. **Optical center** — Simple Icons prefers geometric center; adjust ±0.3u for arrows/triangles that need optical balance.
4. **Weight** — target 35 – 55% ink coverage of the 24×24 area. Below 25% feels thin at 16 px; above 65% muddies negative space.
5. **Corner treatment** — either all sharp OR all rounded; do not mix.
6. **Gap consistency** — if using the 0.5-unit gap technique, keep every gap exactly 0.5u.

---

## Anti-patterns

- Text stroked with `stroke-width`
- More than one `<path>` element
- Any `<g>`, `<rect>`, `<circle>` — even if `<path>` alternatives feel "harder"
- Padding around the mark (empty margin inside the 24×24)
- Multiple colors on the master (colored variants live under `color/`)
- Filters, gradients, transparency
