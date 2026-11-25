# Prompt patterns

Use these as compositional patterns, replacing the product description with observed and confirmed facts. Deliver fully expanded prompts to the user; these patterns are not final user prompts.

## Shared product lock

A useful lock is concrete: “Use the supplied photo as the product reference. Preserve the exact [silhouette], [observed color], [visible surface], [lid/handle/strap geometry], and [label or logo placement]. Keep [component count]. Show only surfaces supported by the reference. Change the setting and lighting, not the SKU.”

If a front-only photo is supplied, favor front or slightly oblique compositions that do not expose unseen details. Do not request new rear ports, underside geometry, inside construction, or a newly opened lid. Preserve the supplied reference orientation when fidelity is critical.

## Six image roles

| Role | Useful composition | Suggested ratio | Facts to protect |
|---|---|---|---|
| Clean hero | One product, uncluttered light surface, soft contact shadow, fully visible | 1:1 | All supplied components; no invented accessories |
| Lifestyle 1 | Product in a plausible setting; restrained context, clear subject | 4:5 | Real use only; no unconfirmed durability or performance |
| Lifestyle 2 | A distinct context or tighter composition with the same lighting family | 4:5 | Same SKU and color; no unsupported scale reference |
| Detail | Crop into a feature already visible in the reference | 1:1 | Do not fabricate texture, seams, ports, or internal structure |
| Feature composition | Product plus generous space for one verified point | 4:5 | Approved copy only; omit numerical claims without evidence |
| Social creative | More expressive framing; room for a short headline | 4:5 or 9:16 | No invented sale, price, certification, review, or endorsement |

These are creative recommendations. Use the ratio choices actually available in the tool. Exact pixel dimensions should be checked on the exported file.

## Complete-prompt composition

Combine the following into one standalone prompt for each image:

1. Reference role and concrete product lock.
2. One image, its business role, scene, framing, and proposed ratio.
3. Light, surface, shadows, and restrained props.
4. Exact text policy, including the language when there is text.
5. The few exclusions relevant to that shot.

Example of prompt structure (replace bracketed content before delivering):

> Create one [role] image using the supplied photo as the product reference. Preserve [concrete product lock]. Place the product [composition] on [surface] against [background], with [lighting and shadows]. Use [approved props or none]. Keep [negative space/crop]. Suggested composition: [ratio]. [No added text / exact approved text and language]. Do not add [likely incorrect parts, claims, or accessories].

Do not append the same long negative-prompt list to every image. Clear positive instructions and reference fidelity usually matter more.

## Text and layout

For exact labels or prices, keep the product's original visible label and leave clean space for later typesetting. Give the user the final copy separately. If they want generated on-image text, specify the exact string and request proofreading; do not imply it is guaranteed.

A clean product card can communicate shape, finish, or arrangement without adding a claim. Replace an unsupported “100% waterproof” card with a visually grounded detail composition rather than a speculative functional scene.

## Targeted correction prompts

Write the correction around the actual defect. Supply the original product photo again when a reference is required.

**Product drift:** “Use the original supplied product photo as the identity reference. Restore its exact [changed feature]. Keep the current background, framing, and lighting. Change only the product area necessary to match the reference; add no new parts.”

**Label drift:** “Preserve the original product label's artwork, placement, shape, and proportions from the reference. Do not invent or rewrite label text. Keep the rest of the composition unchanged.” If exact restoration still fails, preserve/composite the original product instead of promising another generation will solve it.

**Clutter:** “Remove the surrounding [specific props]. Keep the product unchanged and fully visible. Retain the established lighting and a natural contact shadow. Add no text.”

**Unwanted lettering:** “Remove the added promotional lettering, leaving clean negative space. Preserve the product's original packaging and existing label. Do not remove the real product label.”

**Inconsistent set:** “Match the established [palette], [light direction], [surface], and [shadow softness] of the approved hero image. Keep the product identity from the original reference; do not copy a drifted product from another generated shot.”

## Batch brief shape

State: confirmed product facts; exact product lock; shared direction; numbered image roles; approved copy or no added text; and relevant exclusions. Request separate image files. Use the chosen tool's actual input limit, output assignments, and available ratios. If it only produces variations of a shared prompt, use one complete prompt per image instead. A single output grid is not a replacement for the requested files. Provider-specific modes and limits belong only in an optional guide for that provider.
