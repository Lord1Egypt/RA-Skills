---
name: handmade-editorial-poster
description: "Create one high-end handmade editorial poster per supplied photo using a paper-textured, minimal illustrated-cover aesthetic. Invoke for requests such as 'make handmade posters from these photos' or 'turn these photos into minimalist editorial covers'; never make a collage or photorealistic edit."
---

# Handmade Editorial Poster

Turn every supplied source photo into its own standalone poster: a small handmade visual poem, recognizably derived from the photo but radically simplified into an art-publication cover.

## Natural-language activation

The user does not need to type this skill's name. Treat these as activation cues when photos are supplied or clearly referenced: `make handmade posters from these photos`, `turn these photos into minimalist editorial covers`, `create one illustrated poster per photo`, `photo-to-paper art posters`, `make an art-book cover from this photo`, `one photo one poster`.

Do not activate for requests to preserve photography, create a collage, make an ad, or generate a generic cartoon unless the user explicitly changes the visual brief.

## Core contract

- Process photos one at a time. Generate and return one output per source photo; never combine photos into a collage, contact sheet, diptych, or shared composition.
- Match poster orientation to source: portrait source -> `9:16`; landscape source -> `16:9`. If square or ambiguous, default to `9:16` unless the user specifies otherwise.
- Preserve the most recognizable subject, silhouette/proportions, key pose or gesture, important object, and central subject-object relationship. Remove nonessential detail.
- Keep the illustrated subject small and centered in the lower half, approximately 10–20% of the canvas. Leave generous negative space.
- Derive no more than four dominant colors from the source. Use restrained, bold acrylic-like flat shapes over visibly warm white, off-white, or pale natural paper.
- Require physical handmade character: imperfect drawn contours, rough paper grain, visible brush marks, and slightly irregular organic edges. Reject smooth digital vectors, watercolor, wax/crayon, glossy 3D, commercial cartoons, or product-ad aesthetics.
- Typography is optional. Add only a small, credible editorial element using verified user-provided text; otherwise omit it. Never invent factual captions.

## Execution path

1. With native image generation/editing, pass one source photo as the reference and generate its standalone poster using [Prompt library](references/prompt-library.md).
2. With an external image provider, use its documented image-reference/upload field. Preserve source order and create a fresh job for every photo.
3. Without image capability, do not claim an image was generated. Deliver one ready-to-paste English prompt per source photo and identify its matching reference.

Read [Platform adapters](references/platform-adapters.md) only when selecting an integration pattern.

## Quality gate

Before returning each result, inspect the generated image and confirm: exactly one source maps to exactly one poster; aspect ratio is correct; no source photo is embedded; the subject remains recognizable; negative space dominates; four or fewer apparent dominant colors are used; paper/brush/line imperfection is tangible; and any text is sparse, legible, verified, and integrated. If needed, retry with a named correction. Stop at the platform's practical retry allowance and report any remaining deviation.
