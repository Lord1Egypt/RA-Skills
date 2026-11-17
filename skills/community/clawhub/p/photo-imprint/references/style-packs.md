# Style packs

A style pack changes only rendering language. It must not change subject semantics, layer separation, composition, or final QA policy. The subject comes from the source photo and theme, never from a style reference.

## Current profiles

Bundled, approved initial references:

- `blue-lavender-watercolor` — Allen Tucker’s *Watercolor no. 73, Blue and Lavender* teaches transparent wash handling, edge control, cool value grouping, and selective dark anchors. It must not contribute seascape, shoreline, water-horizon, landscape, or compositional content.
- `highway-485-lithograph` — Allen Tucker’s *Highway 485* teaches sparse broken dry-crayon/contour construction, paper-white negative space, restrained dark accents, radical simplification, and limited hatching. It must not contribute roads, signs, poles, wires, landscape, or compositional content.

Both are independent style packs. Select one explicitly; do not blend them by default. Neither changes the reusable `travel-food-journal` preset’s existing `watercolor-journal` default.

Text-only profiles still awaiting approved references:

- `watercolor-journal` — loose observational line, transparent low-saturation watercolor, warm paper influence, and soft natural edges.
- `botanical-watercolor` — controlled graphite, translucent watercolor, delicate organic edges, sparse paper, and observational detail.
- `paper-collage` — cut or torn matte-paper layering, warm archival color, shallow depth, and intentional negative space.

These three profiles remain `reference_status: pending-selection`. Rendering can resolve from their text rules, but the warning must remain visible until an approved reference set is added.

## Reference sets

A style may use multiple references. Each reference must have named `technique_roles`, such as:

- contour construction;
- paint or material application;
- edge control;
- value grouping;
- surface texture;
- simplification.

Every active reference must also declare explicit `subject_exclusions`. Use the same approved set across a series. Do not copy the reference's subject, text, seals, ornaments, page content, or composition into the output.

## Storage and rights policy

Reference binaries stay out of version control until both conditions are approved:

1. item-level redistribution rights are verified through an authoritative institution or library page;
2. the image clearly demonstrates a reusable drawing method rather than only subject matter, historical atmosphere, or composition.

After approval, optimize each distributable derivative to:

- maximum long edge: 1600 px;
- preferred format: WebP;
- quality: 82–88;
- target size: 750 KB or less;
- enough retained detail to inspect line, edge, value, and texture behavior.

Record separate source metadata for every approved reference: title, creator, institution, object number, medium, date, official image URL, authoritative item record URL, exact item-level rights status and statement, license/rights URL, retrieval date, redistribution and bundling flags, source-download provenance, derivative settings/hash/bytes/dimensions, metadata stripping, technique roles, and subject exclusions. The derivative record must match the actual bundled bytes.

Do not treat “free to view” as permission. Public references require an explicit CC0, Public Domain Mark, or equivalent item-level reuse grant.

Private user-supplied references require two separate decisions:

1. **Local storage consent** — the file may remain in the private project workspace and must stay out of version control and delivery.
2. **External processing consent** — uploading or transmitting the file to an external image-generation service requires separate, explicit authorization naming that use. Local storage consent never implies external-processing consent.

If external processing is not explicitly authorized, use only local tooling or text rules. Record the applicable consent decision in the renderer receipt; never infer it from the presence of a local file.

## Adding a style pack

1. Add `profiles/styles/<id>.json` with style rules independent of subject matter.
2. Add zero or more approved entries to its `references` array.
3. Store each approved binary and its source metadata under `assets/style-packs/<id>/`.
4. Run `python3 bin/validate_skill.py`.
