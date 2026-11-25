# Choosing resolution and fidelity on PixelLab

Read this reference before setting a style's `size`/`detail`/`shading`/
`outline` for a deliberate look — a retro console feel, or a high-fidelity
showcase asset — rather than an arbitrary default. It applies across every
PixelLab-backed generator: `map`, `pixflux`, `1dir`, `tiles`, and `character`.

## There is no GBA/NES/SNES preset to ask for

PixelLab ships none. Checked directly against the OpenAPI spec and PixelLab's
own docs site: no console name, no named retro preset, and no palette/color-
depth constraint tied to a console exists anywhere in the API or its
documentation. "Retro," "8-bit," "16-bit" appear only as free-text example
*prompt* wording, not as parameters. A "Game Boy style" or "GBA style" asset
is a convention pixelkiln has to define and apply consistently — a canvas
size, a `detail`/`shading`/`outline` choice, and where useful a post-hoc
palette reduction — not a flag PixelLab recognizes.

## The one real lever: canvas size trades frame/reference budget for detail

This is the closest thing to a hard rule PixelLab's own tooling exposes, and
it recurs across unrelated tools:

| Canvas size | Style-reference batch tool: max refs / outputs | Animate-with-text: frames | Interpolate: frames |
|---|---|---|---|
| 16–32px | up to 64 | 16 | 16 (measured to 64px) |
| 64px | 16 | 16 | 16 |
| 128px | 4 | 4 | 16 (reported; conflicts with animate-with-text's 4 at the same size — unresolved, see below) |
| 256px | 1 (single-image mode) | not demonstrated | ~8 (reported with uncertainty) |

Stated governing rule (PixelLab's own tutorial, verbatim): **"Smaller
resolution equals more style learning and bigger resolution equals more
precision."** Treat this as the master heuristic for any size choice, not
just the two tools it was said about.

**The 128px row disagrees between tools** — one PixelLab tutorial measured
animate-with-text at 4 frames and interpolate at 16 frames, both at 128×128.
Either the two tools genuinely have different frame/size curves, or one
figure is stale. Do not silently reconcile this; if it matters for a
budget-sensitive decision, treat both numbers as unconfirmed until checked
against the live API.

Two engine-specific data points worth the same treatment:

- `character` v3-engine loops report a higher, cheaper frame ceiling than the
  pro engine at the same canvas ("even at 256×256, we can generate eight
  animation frames, which we didn't have before even with the pro tools") —
  consistent with pixelkiln's documented `character` cost model, where v3
  scales `ceil(size²×8/65536)` and pro sits in the flat 10–25 tier regardless (20–40 before PixelLab's
  October 2026 cut).
  Prefer v3 over pro for a loop unless pro's quality is specifically needed.
- `portrait-character-pro` (not part of this adapter) renders sizes 128 and
  160 at "2K" internal resolution versus "1K" for 16–64, at a measured cost
  step (20 → 25 generations) — the one place PixelLab documents size-driven
  internal resolution as a fact rather than an inference.

## Detail, shading, and outline are not one enum family — they differ per endpoint

Do not assume a value that works on one generator works on another. Confirmed
directly against the OpenAPI spec (`components.schemas`), current as of this
writing:

| Generator | `detail` | `shading` | `outline` |
|---|---|---|---|
| `map` (map-objects) | `low detail` \| `medium detail` \| `high detail` | `flat` \| `basic` \| `medium` \| `detailed shading` | `single color outline` \| `selective outline` \| `lineless` (**no black-outline option**) |
| `pixflux` / `1dir` (pixflux, pixen, bitforge) | `low detail` \| `medium detail` \| `highly detailed` | `flat shading` \| `basic shading` \| `medium shading` \| `detailed shading` \| `highly detailed shading` | `single color black outline` \| `single color outline` \| `selective outline` \| `lineless` |
| `character`, standard/v3 | free string (soft guidance, model may ignore); v3 has **no `shading` field at all** | — | free string |
| `character`, pro / pro-flash | none — no text dial | none | none — style comes from a style image and `styleTraits` copy-toggles instead |
| `tiles` (create-tiles-pro) | none | none | `outlineMode`: `outline` \| `segmentation` only |

Notice `map`'s wording is `"high detail"`, while `pixflux`/`1dir`'s is
`"highly detailed"` — a different literal string, not a typo to normalize
away. Passing the wrong family's string is a real, easy-to-hit mistake.

Pixelkiln's own measured finding on `outlineMode` (docs/ENDPOINTS.md): the
API defaults `tiles` to `outline`, which quilts a ground set with a seam at
every cell edge; `segmentation` was the difference between a usable and
unusable terrain set. Set it deliberately for any `tiles` style meant to read
as continuous ground, never inherit the default.

**"Pro" is a quality/cost tier that spans many PixelLab tool families, not a
`character`-specific setting.** The table above already shows this
structurally — `character` pro/pro-flash drop every text dial in favor of a
style image — and PixelLab's own tutorials confirm the same pattern recurs
outside characters: a Pro background-generation tier, a Pro inpaint/edit
tier, and a Pro interpolate tier all exist, each swapping the cheaper
tool's text controls for a stronger, slower, more expensive model. When
scoping a new PixelLab-backed capability, expect a plain and a Pro variant
by default, not just for characters.

## Reference-image size sets the *output's* scale, not just its content

Already in [pixellab.md](./pixellab.md), repeated here because it is exactly
as much a fidelity-tier concern as a bug to avoid: a `reference`, `concept`,
or `styleCharacter` image's own canvas size sets the apparent scale of what
comes out. A reference padded to a larger canvas than the target reliably
produces an oversized result next to everything else at the intended size.
Decide the target size first, then build or crop every reference to match it
— for a whole matched set (a retro roster, a detailed showcase set), this
means every reference shares one canvas size, not just a similar look.

## A retro/low-fidelity recipe (pixelkiln's own convention, not PixelLab's)

1. Pick the smallest canvas that still reads as the subject — 16–32px for an
   icon or VFX element, 32–64px for a character or prop. Below 24px, an
   8-direction object stops reading as 8 distinct angles (PixelLab's own
   documented floor for `create-8-direction-object`).
2. `detail: "low detail"`, `outline: "single color outline"` or `"single
   color black outline"` (family-appropriate; see the table above),
   `shading: "flat shading"` or `"basic shading"`.
3. If animating, generate the model's normal frame count, then deliberately
   keep fewer of them than were generated — PixelLab's own tutorials treat a
   hand-picked subset as reading snappier and more "handmade," a retro trait
   in its own right, not a fallback for a bad generation.
4. For a genuinely constrained retro palette (a Game-Boy-style 4-shade look,
   an NES-like fixed count), `pixflux`'s `color_image` is pixelkiln's only
   generator-level palette lock today (see pixellab.md and
   docs/ENDPOINTS.md's "Lock a palette" recipe) — verified to hold exactly
   across 130 generations. `map`, `1dir`, and `character` accept no such
   lock. A post-generation reduce-to-N-colors pass exists on PixelLab
   (`reduce-colors`) but is not wired into this adapter; see
   [pixellab-roadmap.md](./pixellab-roadmap.md).
5. Never lead a prompt with the device or medium name. Measured: `"Original
   Game Boy DMG handheld sprite:"` as a prefix produced drawings of handheld
   consoles across an entire set. Put the medium after the subject, in the
   suffix, if at all — `promptSuffix` exists for exactly this.

### Game Boy Advance, specifically

The GBA's own hardware constraints are public and well documented, unlike
anything PixelLab publishes — use these as the actual target, not a vibe:

- Native screen: 240×160px. A `pixflux`/`map` background meant to fill the
  screen at native scale is 240×160, not a round number like 256×256.
- Sprites are tile-based in fixed hardware sizes: 8×8, 16×16, 32×32, 64×64
  (square) and 8×16, 16×8, 8×32, 32×8, 16×32, 32×16, 32×64, 64×32
  (rectangular). Pick a `character` or `map` `size` from this list, not an
  arbitrary value, if the goal is an authentic sprite size rather than just
  "small."
- Hardware palette is 15-bit (32,768 possible colors), but sprites are drawn
  from a 16-color or 256-color palette, not full 15-bit per pixel. A
  `pixflux` `color_image` swatch of 16 (or fewer) colors is the closer
  authentic target than an arbitrary small count.
- These are screen/hardware facts, not PixelLab settings — nothing here
  changes what `detail`/`shading`/`outline` value to pass. Keep those at the
  low/flat end per the general retro recipe above.

## A high-fidelity recipe

1. Use the largest canvas the generator and budget allow — 128–256px for a
   `pixflux`/`1dir` scene or portrait-scale asset, up to `character`'s
   v3/pro-flash ceiling of 256px for a hero character.
2. `detail: "highly detailed"`, `shading: "highly detailed shading"`,
   `outline: "lineless"` or `"selective outline"` (never a black outline,
   which reads as flatter and more graphic than a detailed render wants).
3. For a `character`, prefer `pro` or `v3` over `standard` — the fidelity
   lever for characters is the engine choice, not a text dial, since pro
   engines take no `detail`/`shading`/`outline` at all and standard's are
   only soft guidance.
4. For a matched set of many assets sharing one high-fidelity look
   (a full roster, a tileset family), generate one strong anchor first, then
   propagate it as a `styleImages`/`styleCharacter` reference across the
   rest, rather than repeating a style description in every prompt. A
   shipped-game case study credited exactly this sequence — one anchor image,
   then style-matched batch generation — with eliminating visual drift across
   an entire game's asset set. Keep the reference set small and tightly
   matched (5–10 images, not dozens) on pixel density, outline treatment,
   shading, and proportions; PixelLab's own tutorial states a small curated
   set outperforms a large uncurated one.
5. For a background or scene canvas, 320×180 (or the nearest size a
   generator allows, e.g. 320×176) is cited in PixelLab's own tutorials as
   "the closest ... to a very common aspect ratio for pixel art games" —
   a reasonable default when no other constraint decides the shape.
6. Sequence gameplay before art: validate mechanics with disposable
   placeholder sprites first, and only invest in a locked high-fidelity style
   once the core loop already works — the same case study built five
   throwaway static sprites before generating anything final.

## What this adapter still has no fidelity lever for

A dedicated post-generation "pixel correction" cleanup pass (strength-slider
noise/detail reduction, distinct from `image-to-pixelart`), and
`reduce-colors` (arbitrary post-hoc palette quantization with dithering) are
real PixelLab capabilities with no equivalent in this adapter today. Pro-tier
full-bleed background generation at custom aspect ratios (`generate-image-v2`)
is closed as the `imagePro` generator (`pixellab.md`). See
[pixellab-roadmap.md](./pixellab-roadmap.md).
