# Controlled revisions

Read this reference when an asset declares `revision`.

- Treat the parent and child as separate assets. `revision.from` names the
  parent, in the child's own style unless `revision.fromStyle` names another, so
  a chain can generate with one provider and refine with another. A `quality`
  profile gates its own style; put it on the last style of a chain.
- Run `pixelkiln plan --only <child>` first. If it reports `blocked`, do not try
  to submit the child or work around the gate.
- A generated parent must be current and downloaded. When the parent has a
  quality profile, its named human approval must be current. Never approve it
  on the user's behalf.
- An inpaint mask must be a PNG and match the available parent dimensions.
- Start image-to-image strength around `0.2`–`0.4`; explain that the exact
  effect belongs to the model and graph.
- On PixelLab, `"engine": "pro-flash"` sends an `image-to-image` or `inpaint`
  revision to the Pro Flash edit/inpaint endpoints instead of the Pro ones:
  5 generations up to 96px, 6 up to 208px, 9 beyond (provisional quotes),
  against 10–25. The parent must be 32–256px per side in multiples of 4, and
  `strength` is refused. Other modes reject `engine`.
- `remove-background` (PixelLab, one image up to 400x400, `removalTask`
  `simple` or `complex`, optional `description` hint) cuts the background out
  to transparency and leaves a locked palette intact; 1 generation measured.
  It refuses a set parent.
- `normal-map` (PixelLab `/normal-map`, 8–512px per side, PNG only,
  optional `convention` `opengl` or `directx`) makes lighting data, not art:
  0.5 generation per call, unmeasured. A loop's frames go as one strip
  (`frames: N`, up to 32) so the light stays steady, and come back cut into
  the parent's `-frame-NN` files; a character's directions are refused (one
  revision per direction instead). It is refused in a style with
  `enforcePalette` or `quality`, since snapping or grid repair would wreck
  the normals: put it in a plain style and point at the parent with
  `fromStyle`. A mirror of a normal map is refused too. For a loose file,
  `pixelkiln normal-map --from <png> [--frames N]` asks before spending.
- `reduce-colors` and `correct-pixelart` send no prompt to the provider — the
  asset's `prompt` stays a manifest-only label. `numColors`/`paletteImage`
  are mutually exclusive; a `paletteImage` has no size relationship to the
  parent, unlike a mask. Cost is confirmed live: a flat 0.1 generations each
  on a 32×32 source (against the schema's own dollar-denominated example);
  unconfirmed whether that holds at larger canvases.
- When the parent is a set (a character's directions, an animation's
  `-frame-NN` files), `reduce-colors`, `correct-pixelart`, and
  `edit-animation` send every member in one call and write the result back
  under the same roles — the way to put a whole loop or all eight directions
  on one shared palette. Every other mode refuses a set parent at plan time.
  A leftover member file from an older generation blocks the revision; tell
  the user which file to remove rather than deleting art yourself.
- `animate` and `animate-pixminimax` DO send the asset's `prompt`, as the
  motion description, and produce an ordered **frame set** — the one
  revision shape that lands in candidate review (`pixelkiln pick`) rather
  than going straight to downloadable output, same as a character loop.
  `lastFrame` pins where the motion ends (any manifest-relative image,
  including another asset's own generated output — that's how to chain one
  animation's final frame into the next). `animate` caps at 16 frames;
  `animate-pixminimax` (beta, tier 1+) allows up to 40 and adds `direction`.
  Neither endpoint's cost or completed-response shape is measured against a
  live account. `direction` + `enhancePrompt` together have a real gotcha:
  the enhanced prompt can add camera-relative language that fights the
  requested world-facing `direction`, breaking an off-cardinal direction
  while cardinal ones in the same batch generate fine — suspect the enhanced
  prompt's wording, not the model, when only some directions of a
  multi-directional set come out wrong.
- `animate-skeleton` (PixelLab, beta, tier 1+) poses the parent from a
  committed `keypointsFile`: the parent's current pose plus 3–15 per-frame
  poses. It needs `direction`; `prompt` names the motion and the optional
  `description` says what the subject looks like. Bootstrap the file with
  `pixelkiln estimate-skeleton <image> --out <file>` (a direct call, outside
  any budget, like `balance`; square 16–256px images only), which writes the
  estimated pose plus `--frames` copies (default 4) to edit. Joint labels are
  PixelLab's 18 names, each once per pose. After every edit, run
  `pixelkiln skeleton-preview <asset>` (local, free) and look at the sheet:
  the starting pose must match the sprite, or every frame degrades silently. Plan cost
  interpolates PixelLab's documented anchors (3 frames = 2, 8 = 3, 15 = 4);
  like the other animate modes it lands in candidate review and is
  unmeasured live.
- `interpolate` needs `lastFrame` (the end keyframe; the parent is the
  start) and lets the model pick the frame count. Suggest it for motion one
  `animate` pass can't produce cleanly: build the key poses first as
  `image-to-image` revisions, then interpolate between them.
  `edit-animation` applies one prompt across a whole frame set (a cape added
  to every frame of a walk); its frame ceiling falls with frame size (16 up
  to 64px, 9 up to 80px, 4 up to 256px). Both land in candidate review and
  are unmeasured; their plan cost borrows the 10/15/25 Pro tiers.
- Both PixelLab and ComfyUI can back a `revision`, not just ComfyUI.
  PixelLab's `reduce-colors`/`correct-pixelart` calls its own
  `/reduce-colors`/`/correct-pixelart` endpoints synchronously (no background
  job); everything else in this file about the dependency gate, hashing, and
  candidate review applies identically regardless of provider. ComfyUI
  cannot back `animate`, `animate-pixminimax`, `animate-skeleton`,
  `interpolate`, or `edit-animation` at all (`supportsRevision` refuses them) — its revision
  path always writes a single output image, and an animation is a frame
  set; that's a structural gap, not a missing binding.
- A filtered child resolves its parents for safety but does not generate them.
  Generate, fetch, refine, and approve the parent explicitly, then re-plan.
- PixelKiln rechecks parent and mask bytes immediately before submission. A
  changed input must stop the run before provider work begins.
- In candidate review, compare the source beside every output. Reject
  silhouette or layout drift before post-processing.
- `pixelkiln gallery --edit` can create a revision directly from a parent's
  drawer ("+ New revision" under "Revisions from this asset"), once the parent
  has usable pixels: on a PixelLab sprite `image-to-image`, `inpaint` (a
  paint-over-the-sprite mask editor that writes the mask PNG into the project),
  `animate`, `animate-pixminimax`, `interpolate` (another same-size sprite as
  the ending keyframe), `reduce-colors`, `correct-pixelart`, or
  `remove-background`, or `normal-map`; on a PixelLab frame set (or a
  character's directions) `edit-animation`, `reduce-colors`, or
  `correct-pixelart`, plus `normal-map` on a loop (never in a style with
  `enforcePalette` or `quality`); on ComfyUI
  `image-to-image` or `inpaint`; on other providers `image-to-image`. On a
  single PixelLab sprite, "+ Skeleton animation" creates an `animate-skeleton`
  revision: poses from a project file, pasted JSON, or "Estimate poses" (one
  confirmed, un-budgeted PixelLab call), edited in a drag-to-edit pose editor
  over the sprite, written into the project on save. "Edit poses" on an
  existing `animate-skeleton` record reopens the editor on its keypoints file.
  Only `outpaint` is not offered; no provider implements it.
- Before an outside image becomes a `styleImages` or `reference` path,
  suggest `pixelkiln unzoom --from <file>`: upscaled pixel art (every art
  pixel a block of screen pixels) degrades every reference-taking PixelLab
  endpoint, and the result is opaque, so a cut-out needs its background
  removed again.
- ComfyUI needs explicit bindings for a revision: its workflow needs
  `sourceImage`; inpaint also needs `maskImage`; declared strength needs a
  `strength` binding. It has no binding for `numColors`/`paletteImage`/
  `dithering` — those reject at validation on ComfyUI; PixelLab needs no
  bindings at all.
- The bundled `comfyui/pixel-art-xl-img2img@1.0.0` recipe is square-only. Its
  live three-strength fortress smoke preserved the footprint but missed the
  requested snow, lost alpha, and produced thousands of colors. Do not call it
  production-ready or a quality preset.

Commit parent inputs, masks, outputs, lock lineage, and quality companions.
Do not commit ComfyUI's recreated input cache.
