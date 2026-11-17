---
name: logos-and-vectors
description: >
  Make true scalable vector art (logos, icons, app glyphs, scalable illustrations) or convert a
  raster image into clean editable SVG. Use when the user says "make a logo", "I need an SVG",
  "vectorize this PNG", "turn this into a vector", "a flat icon set", "a scalable mark", or wants
  artwork that stays crisp at any size and opens in a design tool. The output is real SVG, not a
  flat PNG that looks vector-ish. For a raster poster, ad, or packaging with exact copy on it, use
  text-in-image instead.
---

# Logos and vectors

Produce genuine **SVG vector art**: paths, fills, and color regions that scale to any size and open editable in Illustrator, Figma, or the browser. Two jobs live here: *generate* a vector from a prompt, or *vectorize* an existing raster image into clean SVG. This is distinct from a normal image model, which only ever returns a flat raster (PNG/JPG) that cannot be rescaled or edited as paths.

## Inputs to collect

- **The job:** generate a new vector from a description, or convert an image you already have.
- **For generation:** what the mark/icon is, the style (flat, line, geometric, badge), and any **exact color set** to lock.
- **For conversion:** the source PNG/JPG (a clean, high-contrast, flat-color image vectorizes far better than a busy photo).
- **For a brand mark with words in it:** the exact text string. Vector models do not reliably set type, so pair with `text-in-image` for the legible wordmark (see Technique).
- Optional: background transparent vs a fill color.

## Models

All three carry the `op:vectorize` capability and use `taskType: vectorize`. Confirm each is `live` and inspect its schema via the `runware-models` + `runware-run` skills before calling. Never hardcode a stale choice.

- **Generate a vector: Recraft V4 Pro Vector** (`recraft:v4-pro@vector`), `io:text-to-image` + `op:vectorize`. Takes a `positivePrompt` and emits SVG directly. Best pick for new logos, icons, and scalable illustration with controllable line quality and color regions.
- **Raster to SVG: Recraft Vectorize** (`recraft:1@1`), `io:image-to-image` + `op:vectorize`. Converts a PNG/JPG to clean SVG with sharp edges and minimal artifacts. Default for converting existing flat artwork, logos, and icons.
- **Raster to SVG alternative: Picsart Image Vectorizer** (`picsart:1@1`), edge-aware tracing that separates flat color regions into compact, resolution-independent SVG. Try it as a second opinion when Recraft Vectorize over- or under-simplifies a source.

## Workflow

1. Resolve the model schema (`runware-run`) and confirm the fields below. All three use `taskType: vectorize`, not `imageInference`.
2. **Generate:** call `recraft:v4-pro@vector` with `positivePrompt`. Optionally lock color via `providerSettings.recraft.colors` / `backgroundColor`, and set `width`/`height` from the model's fixed 2K size set (both required together if either is sent).
3. **Convert:** upload the source under `inputs.image` (required) and call `recraft:1@1` or `picsart:1@1`.
4. Run **synchronously**. Vectorize is a fast image task with no async polling. `outputFormat` is `SVG` (the only value, and the default).
5. **Read the result:** the SVG comes back as `imageURL` (plus `imageUUID`). Open it to confirm it is real vector paths, not an SVG wrapper around an embedded bitmap.

## Technique

- **A vector is not a "vector-looking raster."** A regular image model can draw a flat, logo-style PNG, but it is still pixels: blurry when scaled, with no editable paths. These models output actual SVG geometry. If the user needs to resize, recolor, or hand off to a designer, you must use a vectorize model, not a styled raster.
- **Generate flat, then it vectorizes clean.** Prompt for simple, bold, flat-color shapes: "flat geometric logo", "minimal line icon", "two-color emblem". High contrast and few colors trace into tight paths. Photographic, gradient-heavy, or noisy descriptions produce messy, bloated SVGs.
- **Lock the palette.** On Recraft V4 Pro Vector, constrain color with `providerSettings.recraft.colors` (and `backgroundColor`) instead of naming hex codes in prose. It holds the brand palette far more reliably. This is the Recraft lever called out in `runware-prompting`.
- **Words belong to a typography model, not the vectorizer.** Vector models render shapes well and lettering poorly. For a wordmark or a logo with a tagline, generate the legible text with the `text-in-image` skill and compose it with the vector mark, rather than trusting the vectorizer to spell.
- **Clean source in, clean SVG out.** When converting, a flat high-contrast image (a screenshot of a flat logo, a scanned line drawing) vectorizes beautifully. A detailed photo produces thousands of stray paths. If a conversion is muddy, simplify or flatten the raster first, or generate fresh with Recraft V4 Pro Vector instead.
- **Two tracers, two opinions.** Recraft Vectorize and Picsart Image Vectorizer simplify differently. If one loses a detail or over-quantizes the colors, run the other on the same source and compare.

## Parameters that matter

- `taskType`: `vectorize` for all three (not `imageInference`). Pass it explicitly.
- `inputs.image`: required source for the raster-to-SVG models (`recraft:1@1`, `picsart:1@1`).
- `positivePrompt`: required for `recraft:v4-pro@vector` (1 to 10000 chars).
- `providerSettings.recraft.colors` / `backgroundColor`: palette and background control on Recraft V4 Pro Vector. Prefer this over hex-in-prose.
- `width` / `height`: optional on Recraft V4 Pro Vector, but only from the model's fixed 2K aspect-ratio set, and both must be sent together.
- `outputFormat`: `SVG` only (and the default). The result arrives as `imageURL`.
- Confirm every field against the live schema (`runware-run`) before calling. Never guess names.

## Quality bar

- The output is a real `.svg` of editable paths, not a raster embedded in an SVG tag. Open and scale it to verify it stays crisp.
- Color regions are clean and the palette matches what was requested (no muddy gradients where flat fills were asked for).
- A converted SVG keeps the source's recognizable shape with a sane path count, not thousands of stray slivers from a noisy input.
- Any text in the mark is correct and legible. If it is misspelled or fuzzy, redo the lettering via `text-in-image` and compose, do not ship the vectorizer's guess.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `text-in-image` (exact legible wordmarks to pair with a vector mark), `product-photography` (raster brand/product imagery, the non-vector sibling).
