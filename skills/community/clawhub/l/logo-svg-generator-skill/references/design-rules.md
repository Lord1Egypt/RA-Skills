# Simple Icons Design Rules (Condensed)

Extracted from https://github.com/simple-icons/simple-icons/blob/develop/CONTRIBUTING.md and https://github.com/simple-icons/simple-icons/blob/develop/slugs.md — this is the source of truth for the `logo-svg-generator` skill.

## 1. Canonical SVG shape

Every master file MUST look like:

```xml
<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
  <title>Brand Name</title>
  <path d="…single compound path…"/>
</svg>
```

Rules:

| Rule | Enforcement |
|---|---|
| Root attributes exactly `role`, `viewBox`, `xmlns` (in that order) | HARD |
| `viewBox="0 0 24 24"` — always | HARD |
| Exactly one `<title>` with the brand's canonical name | HARD |
| Exactly one `<path>` element | HARD |
| No `<g> <rect> <circle> <ellipse> <polygon> <line> <defs> <style> <use> <mask> <clipPath>` | HARD |
| No `fill`, no `stroke`, no `class`, no `id`, no `data-*` on master | HARD |
| No `<!DOCTYPE>`, no `<?xml …?>`, no comments | HARD |
| One-line output, ≤ 3 decimal precision on numbers | HARD |

## 2. Canvas & composition

- **Canvas**: strictly 24 × 24 user-space units.
- **No padding**: the shape MUST touch at least two sides of the viewBox.
- **Center**: bounding box center should sit around (12, 12); acceptable window (11, 13) × (11, 13).
- **Aspect ratio**: never stretch — scale uniformly.
- **Symmetry**: horizontal or vertical axis symmetry is preferred if it fits the concept.

## 3. Stroke, fill, color

- **No strokes**. All lines are closed filled paths.
- **Single color** (monochrome) on the master.
- To imply layering / color regions, use the **0.5-unit gap** technique (see Google, Instagram, Mastercard examples): draw two shapes as sub-paths of the same path, leaving a 0.5-unit-wide negative gap between them.
- Overlap resolution uses the SVG default **`nonzero` fill-rule**: outer contour clockwise, inner contour (holes) counter-clockwise — automatic donut effect.
- Brand hex color is stored separately (not in the master SVG). It is only applied to `color/` variants (via `fill="#XXXXXX"` on the path).

## 4. Path anatomy — allowed commands

Prefer these commands, in rough order of frequency:

`M m` (moveto) · `L l H h V v` (lines) · `C c S s` (cubic bezier) · `Q q T t` (quadratic bezier) · `A a` (arc) · `Z z` (close)

Guidance:
- Prefer **relative** commands after the initial absolute `M`, so SVGO can compress well.
- Use `A` for circular / elliptical elements — never approximate a circle with dozens of L segments.
- Use compound sub-paths (multiple `M … Z` inside one `d`) for donuts, letterforms with counters, and multi-part marks.
- Target `d` length: **200 – 2000 characters** for simple/medium marks. Anything > 5000 chars usually means the concept is too detailed for a 24-unit canvas.

## 5. Naming — slug rules

Filename = `<slug>.svg` (all lowercase).

Transformations (in order):

1. Lowercase.
2. Replace `.` in-name with the literal string `dot` (e.g., `Node.js` → `nodedotjs`, `.NET` → `dotnet`).
3. Replace `+` with `plus` (e.g., `C++` → `cplusplus`).
4. Replace `&` with `and` (e.g., `AT&T` → `atandt`).
5. Convert Unicode accents to plain ASCII (`Citroën` → `citroen`).
6. Remove every remaining non-alphanumeric character (spaces, hyphens, punctuation).

## 6. Extracting an icon from a full logo

When the source material is a compound brand mark:

1. Discard the wordmark unless the brand IS a wordmark.
2. Discard tagline, subtitle, drop shadows, gradients, embosses.
3. Merge overlapping shapes → compound single path.
4. Rescale to 24×24 and touch ≥ 2 sides.
5. Recenter horizontally and vertically.
6. Reduce color to monochrome; if color layers are semantic, use the 0.5-unit gap trick.
7. Remove ® / ™ unless the brand style guide mandates it.

## 7. Multi-size output convention (this skill's addition)

Simple Icons itself ships only the 24×24 master; downstream users scale as needed. This skill produces convenience artefacts:

| Size | Purpose | Notes |
|---|---|---|
| 16 | favicon, small UI | may use simplified path (see `simplify_for_small.py`) |
| 24 | Simple-Icons master, table row icon | canonical |
| 32 | toolbar, list-view app icon | |
| 64 | grid tile, notification | |
| 128 | app icon (Windows classic) | |
| 256 | app icon | |
| 512 | app store / marketing | |

All sizes share the same 24×24 path; the SVG root gets `width="N" height="N"`. PNG rasters are produced via cairosvg / resvg / inkscape (whichever is available).

## 8. Compliance checker

Use `scripts/validate_svg.py` — it enforces every HARD rule above and fails the build if any is violated.
