# PixelLab coverage and remaining gaps

A catalog of PixelLab capabilities checked against PixelKiln: what this
adapter now covers, and what is still absent. It was built by reading all 31
tutorials on PixelLab's official YouTube channel (the original
26 — the 12 featured on pixellab.ai plus 14 more from the channel's "PixelLab
Tutorial" playlist, filtered to ~12 months back from that pass — plus 5 more
published since: "Level Up Your Game: Custom Sprite Animation Tutorial,"
"Pixel Art Animation Tutorial: Images Pro Flash, Skeleton V3 & PixMiniMax,"
"How to Reduce Colors Like a Pro!", "How to Make Animated Pixel Art VFX in
PixelLab" (https://www.youtube.com/watch?v=t8FIMv-8QpI), and "PixelLab Pro
Tilesets: Full Guide" (https://www.youtube.com/watch?v=MbkqpDUFkEg)) against
this adapter's actual source — and, for the newer passes, against PixelLab's
own MCP tool schemas (`create_image_pro_flash`, `edit_image_pro_flash`,
`inpaint_image_pro_flash`, `get_pro_flash_capabilities`, and for the last two
`create_topdown_tileset`, `create_sidescroller_tileset`, `create_tiles_pro`,
`create_map`, `animate_image_pixminimax`, `create_image_pro`, `vfx_workbench`,
and `search_knowledge`) plus the REST OpenAPI document's `/create-tileset`
and `/create-tileset-sidescroller` request schemas, where a tutorial's
framing needed checking against the live surface, the same standard the
original pass held itself to. The PixelLab 0.4.130 release notes (October 2026: Tileset
Pro, a target palette for Create Image Pro, VFX in the API, normal maps)
were checked the same way against the REST OpenAPI document.
Read this when scoping new PixelLab work, so effort goes toward a
confirmed gap with real demand rather than a guess. Nothing here is a
commitment to build it — it is what is missing, with the evidence for why it
might matter, so that decision can be made deliberately.

For which PixelLab endpoints PixelKiln already calls, and how much is measured
about each (so a live run can be chosen by risk), read the [validation
ledger](https://pixelkiln.griffen.codes/docs/endpoints#validation-ledger)
(`docs/ENDPOINTS.md`).

Each open entry names the PixelLab tool, why pixelkiln doesn't have it today,
and which tutorial(s) demonstrated real (not hypothetical) demand for it.

## Already closed since this catalog's research began

- **Sentence-driven skeleton-v3 loops** — a character loop with
  `mode: "skeleton-v3"`, no `template`, and a `prompt` animates the sentence
  on `/characters/animations` (`action_description`, 3 to 15 `frames`). Billed
  exactly 3 generations for 8 frames at 64px, frames back at 96×96; the plan
  budgets 4. See `docs/CHARACTERS.md`, "Loops from a sentence".
- **Shared motion across the directions of a sentence loop** — the first
  direction of `directions` is submitted as a new animation; each later one
  follows in the next wave with the leader's recorded `animation_group_id` and
  the group's `animation_name`, so every direction is drawn from one 3D motion
  (`animation.motionFrom`, lock `motionShare`). Adding a direction to a
  generated loop appends into its group, a regenerated leader marks followers
  stale, and a leader with no recorded group falls back to one request per
  direction. **A live append is verified** (adding `west` to a generated `south`
  loop billed 3, joined the leader's group, and moved with the same timing).
  Still unverified: that deleting one direction leaves the group and the
  others' motion intact.

- **Skeleton-v3 template loops** — `/characters/animations`'
  `mode: "skeleton-v3"` poses a template with the skeleton video model
  (2 to 4 generations and 3 to 5 minutes per direction, beta, Tier 1 and
  up). Now a character loop's `mode: "skeleton-v3"`; see
  `docs/CHARACTERS.md`. A template loop on a v3 character billed 3
  generations live (October 2026).

- **Masked inpainting and whole-image editing** — was the single largest gap
  found (routine in at least 6 of the 26 tutorials). Now the `revision` asset
  shape's `inpaint` and `image-to-image` modes; see `docs/REVISIONS.md`.
  Both are confirmed live at their floor size (20 generations each, response
  shape matched on the first try for both — though the two shapes differ,
  singular for one and array-wrapped for the other). `inpaint` is further
  confirmed at its ceiling size too (512×512, exactly 40 generations), and
  further confirmed to have a real middle (25-generation) tier — 288×288
  (82944px²) and 320×320 (102400px²) both billed 25 — just positioned far
  higher than the borrowed 1024px²/2048px² breakpoints assume: 40×40,
  128×128, and 256×256 (up to 65536px²) still billed 20, not 25, while
  352×352 (123904px²) already billed 40. Both breakpoints are now tightly
  bracketed: 20→25 in (65536px², 82944px²] (a 1.27x range), and 25→40 in
  (102400px², 123904px²] (a 1.21x range). `image-to-image` above its own
  floor remains completely unmeasured — see that doc's PixelLab section
  before relying on either endpoint's cost outside what's stated here.
- **`tiles` generator parameters** (`tileType`, `tileSize`, `tileView`,
  `tileFeature` including a building-kit construction set, `outlineMode`) —
  already implemented in code, was simply undocumented in
  [pixellab.md](./pixellab.md) until this pass. Not a gap; a docs fix.
- **Diagonal character mirroring** (southeast/southwest, northeast/northwest,
  not just east/west) — already implemented in code
  (`MIRRORED_DIRECTION` in `src/types.ts`), was undocumented. Not a gap.
- **Two-terrain elevation tilesets** (`/create-tileset`, the top-down family)
  — a real gap, not a docs fix: `tiles`'s own `tileFeature: "tileset"` draws
  one terrain's edges, not two named, connected terrain levels with their own
  transition prompt. Closed by the `terrain` generator; see
  `pixellab.md`. Reference images and `color_image` remain unmodeled.
- **Tileset Pro shape controls, connected sets, and sidescrollers**
  (PixelLab 0.4.130, October 2026). `terrain` styles take
  `terrainRoundness`, `terrainBoundaryAmplitude`/`terrainBoundarySeed`,
  `terrainStepSlope`, and `terrainConnectDiagonals`, each refused outside
  the mode that reads it. `terrainSpreadX`/`terrainSlopeSize` are
  deprecated, since PixelLab now documents both as "No effect". A Pro set at
  `terrainTransitionSize` 0.5 counts as 25 tiles. An asset's `connect` shares
  a terrain with another set in the same style: pixelkiln records each set's
  `metadata.terrain_ids`, sends the other set's id as `lower_base_tile_id` or
  `upper_base_tile_id`, blocks until that set is downloaded, and marks the
  connected set stale when the other is regenerated.
  `terrainOrientation: "sidescroller"` calls `/create-tileset-sidescroller`
  (platform body plus top layer). Its response is the top-down shape with
  `terrain_types` `["central","background"]` but `lower`/`upper` corners,
  lower being the platform. **Measured once**: a 16px set at transition 0.25
  billed exactly 3 generations. Estimates now follow PixelLab's quotes: Pro
  15 up to 32px and 25 at 64px, standard 4 (the top of its quoted 1 to 4),
  sidescroller 3. What is still open is in
  [Pro tilesets](#pro-tilesets-what-is-left-after-04130) below.
- **Older terrain fields as identity.** `terrainMode`,
  `terrainTransitionSize`, `terrainRaggedness`, `terrainShapeStyle`,
  `terrainView`, the deprecated `terrainSpreadX`/`terrainSlopeSize`, and
  the descriptions as sent (the prompt wrapped in the style's prefix and
  suffix) never entered `specHash`, and hashing them would have made every
  existing terrain entry stale at once. Closed without a migration: submit
  records them on the entry as `terrainSettings` (kept through history and
  `restore --generation`), and the plan marks a set stale naming each one
  that changed. An entry from before the record has none and stays current
  until it is next regenerated. The 0.4.130 fields stay hashed (when set).
- **Pro-tier full-bleed background generation** (`generate-image-v2`, PixelLab's
  Pro image tier) at arbitrary custom aspect ratios (not just square) —
  already measured at 40 generations in `docs/ENDPOINTS.md`, but `pixflux`
  wraps only the cheap 1-generation non-Pro endpoint. Demonstrated
  generating a 384×216 scene background in "How to Make Animated Pixel Art
  Scenes with PixelLab." Closed by the `imagePro` generator; see
  `pixellab.md`. Reference images and a style image
  (`reference_images`/`style_image`) remain unmodeled. The completed job's
  response shape has been read live (a 64×64 call billed 10).
- **A standalone single isometric tile** (`/create-isometric-tile`, a third,
  separate path to isometric content distinct from both `tiles`'
  `tileType: "isometric"` and `terrain`'s `/create-tileset`, which is
  confirmed square-only with no isometric option at all) — a real gap: no
  per-tile elevation primitive existed for a raised mesa or a cliff block
  outside a connected ground set. Found via direct API/schema investigation,
  not a tutorial (real downstream demand: a Godot game's terrain-verticality
  work). Closed by the `isometricTile` generator; see `pixellab.md`. Its
  `isometricTileShape` (thin/thick/block) is a direct thickness control
  `tiles`/`terrain` do not have. **Cost measured once, and it corrected a
  wrong assumption**: the endpoint's own OpenAPI response schema example is
  `{ type: "usd", usd: 0.02 }`, which reads as real-dollar billing, but a
  live call against a subscription account billed exactly 1 generation
  instead — `costUnit` is `"generations"` here, not `"usd"`. Only one
  size/shape combination (32px, `"block"`) has actually been measured; no
  size-tiering formula is documented the way `1dir`/`tiles` have one. Style
  images, `init_image`/`init_image_strength`, and `color_image` remain
  unmodeled.
- **Object Creator's rotation/state/animation family** (`/create-object-pro-flash`,
  a skeleton-free entity distinct from both `character` and the generic
  `/objects` polling resource `1dir`/`map` already use) — demonstrated in
  "Object Creator" and used throughout "GBA-Style Sprites" and "Build a Game
  with AI"; `map` (one generation, no direction/state concept) and `1dir`
  (one direction only) were the closest analogs, and neither modeled
  rotation, states, or animation for a plain object. Closed by the
  `objectPro` generator; see `pixellab.md`. It reuses `character`'s own
  `asset.state`/`asset.animation` authoring shapes and mirror handling
  rather than inventing parallel ones. **The base is measured**: a 32px
  base billed 6 and returned 8 files (November 2026), matching `character`
  pro-flash's formula, which the estimate assumes since the request bodies
  are near-identical minus `template_id`. States and `pro` animations remain
  that assumption pending a live check. Batch "pack" generation (N distinct objects from
  one call) is covered on `1dir` by its `batch` field — see below.
- **Pixel correction** (`/correct-pixelart`, a dedicated cleanup pass distinct
  from `image-to-pixelart` — the latter is documented, docs/ENDPOINTS.md, as
  being "for photographs and 3-D renders, not for reprocessing" pixel art)
  and **reduce colors** (`/reduce-colors`, palette-lock/quantize with an
  explicit color count or a lifted palette image, distinct from PixelKiln's
  internal `quantize()`, which only runs inside the `refine`/quality-gate
  pipeline against a manifest-declared palette) — both demonstrated
  repeatedly across this batch's character/animation tutorials as a
  near-mandatory cleanup step. Closed by the `revision` asset shape's
  `correct-pixelart` and `reduce-colors` modes; see
  `pixellab.md` and `docs/REVISIONS.md`. **Cost confirmed live**: a flat 0.1
  generations for each, on a 32×32 source, live against a Tier 2
  subscription account — the schema's own dollar-denominated `usage` example
  (`usd: 0.005`/`0.01`) did not predict this, exactly the kind of claim this
  catalog has repeatedly found wrong once measured (`isometricTile`,
  `objectPro`); PixelLab's own MCP tool descriptions claiming 0.1 generations
  were the correct source instead. Only confirmed at this one size — whether
  it holds at larger canvases is unconfirmed. **Batch/multi-frame input is
  now modeled too**: both endpoints are built to take several frames in one
  call so an animation or a character's eight directions share one
  consistent palette/cleanup pass, which is the actual differentiator the
  tutorials demonstrate. A revision whose parent is a set (directions, or
  `-frame-NN` files) now sends every member together and writes the result
  back under the same roles; see `docs/REVISIONS.md`'s "Revising a whole set
  at once." The price of a multi-frame call is unmeasured. Freshly confirmed by
  "How to Reduce Colors Like a Pro!": the real-world shape of this gap is
  project-wide, not per-asset — the tutorial applies one palette across a
  character's full 8-direction set, its states, each animation (per-frame,
  "apply to all frames" in one operation), a generated UI pack, a tileset,
  and a placed map object, in that order, specifically to keep an entire
  project visually consistent. `numColors`/`paletteImage` already cover the
  tutorial's other two reduction modes ("auto reduce colors" is pixelkiln's
  own omit-both default; "use palette" is `paletteImage`, including one
  imported from Lospec into the source editor's palette list before use) —
  and the batch/multi-frame piece above now covers the per-set step. What
  remains is the project-wide sweep: one revision per set, declared by hand,
  rather than one command that applies a palette across every asset.
- **Generic (non-character) animation and interpolation** (`/animate-with-text-v3`,
  `/animate-pixminimax`) — PixelLab's **Animate with text** tools work on
  *any* image, not just a `character`/`objectPro` asset. Demonstrated
  animating a treasure chest opening, a campfire's flames, a tree catching
  fire, a two-character combat scene, a day/night background transition, and
  chaining a sequence by feeding one animation's final frame back in as the
  next one's reference (repeatedly, in "Animate with Text," "Generate Pixel
  Animations," "New PixelLab Tool: Animate Between 2 Frames," and "How to
  Make Animated Pixel Art Scenes with PixelLab"). Closed by the `revision`
  asset shape's `animate` and `animate-pixminimax` modes; see
  `pixellab.md`. `lastFrame` covers both the "pin an ending pose" and the
  "chain from a prior animation's final frame" cases — it is just a
  manifest-relative image, which can be any earlier asset's own generated
  output file. **Both ran live in November 2026**: `animate` at 64×64 and 4 frames
  billed 1 (5 frames back, input included), `animate-pixminimax` billed 1 at 8
  frames and 2 at 16 (9 and 17 frames back), and the completed jobs were read
  correctly. `animate`'s cost borrows `character`'s measured v3-loop formula;
  `animate-pixminimax` follows PixelLab's published table. The frame list is
  still extracted defensively from several plausible field names. The dedicated
  **Interpolate** endpoint (`/interpolation-v2`, a separate "Pro" two-keyframe
  tool distinct from `last_frame` pinning on the animate endpoints above) is
  now wrapped too, as the `interpolate` revision mode (parent = start
  keyframe, required `lastFrame` = end keyframe), alongside
  `/edit-animation-v2` as `edit-animation` (one text edit across a whole
  frame set). Both ran live in November 2026 and billed 10 each (a 64×64
  `interpolate` returning 14 frames; an `edit-animation` of a 9-frame 64×64
  set), on the 10/15/25 Pro canvas tiers; the planner used to read them as 25
  and is calibrated. Larger canvases are unbilled.
  Real demonstrated demand for Interpolate: "Level Up Your Game: Custom
  Sprite Animation Tutorial" used it
  repeatedly, in Aseprite via PixelLab's own extension, as the fix for an
  animation a single `animate-with-text` attempt couldn't produce directly —
  a character knocked backward by a hit. One `animate-with-text` pass from
  the idle pose gave motion but no clean launched-backward pose; the fix was
  to stop asking for the whole animation at once, build the two key poses
  first with a plain single-image edit (an airborne "just hit" frame, then a
  "landed on the floor" frame, each edited from the previous one), and let
  Interpolate fill the motion between them (8 frames for the fall, 11 for the
  recovery back to idle, both with `enhancePrompt` on) — a "key poses first,
  then interpolate the gap" pattern worth carrying into any future wrapper,
  not just the raw endpoint (`docs/REVISIONS.md` carries it as the
  recommended use of `interpolate`; the endpoint itself has no
  `enhance_prompt` field, so that part of the tutorial's setup came from
  PixelLab's editor extension). Also newly confirmed, from "Pixel Art Animation
  Tutorial: Images Pro Flash, Skeleton V3 & PixMiniMax": PixelLab states
  outright that PixMiniMax allows "up to 40 frames," a second, independent
  (though still not live-billed) confirmation of the schema's 40-frame
  ceiling already assumed here. The same tutorial surfaces a real gotcha for
  `animate-pixminimax` + `direction` + `enhancePrompt`: the expanded prompt
  can add camera-relative language ("towards the camera") that fights the
  requested world-facing `direction`, breaking off-cardinal generations (a
  north-east loop came out wrong, cardinal ones did not) even though neither
  the model nor the `direction` value was at fault — worth a caveat wherever
  `enhancePrompt` is documented alongside `direction`.
- **Object Creator's "pack" generation** (one call → N *distinct* objects,
  each with its own per-item description, instead of N variations of one
  prompt) — demonstrated in "Object Creator" and used throughout
  "GBA-Style Sprites" and "Build a Game with AI." Turned out not to be a
  separate endpoint at all: `/create-1-direction-object`'s own
  `item_descriptions` field and `select-frames`'s already-plural `indices`
  field are the exact mechanism, on the same endpoint `1dir` already wraps —
  `client.ts`'s `create1Direction` even already sent `item_descriptions`
  before this pass, just never populated from anywhere in the manifest.
  Closed by the `1dir` asset shape's `batch` field (one leader, siblings
  claim slots via `{of, index}`); see `pixellab.md` and
  `docs/GENERATORS.md#batch-several-distinct-objects-for-one-calls-cost`.
  This is the one closed item in this catalog that isn't a new
  generator/revision-mode wrapper around a fresh endpoint — it's new
  manifest/pipeline plumbing (one submitted job, several independent lock
  entries) for a capability the client already halfway had. **Confirmed
  live** on a Tier 2 account: a 32px chest+potion+key batch billed exactly
  20 generations (the ordinary `1dir` floor tier, unaffected by
  `item_descriptions`), and `item_descriptions[0]` does own candidate slot
  0 — the returned frames 0/1/2 were exactly the chest, potion, and key in
  declared order, with the rest of the 64 candidates being the model's
  ordinary variety rather than repeats. Only confirmed at this one size;
  the cost table's higher tiers remain unconfirmed under
  `item_descriptions`.
- **UI elements and RPG UI kits** (`/create-ui-asset`, laying out `pieces`
  and named `elements` on a panel canvas) — demonstrated in "Create an RPG UI
  Set" and "Easiest way to create pixel art UI." Investigated directly
  against the live OpenAPI document rather than the tutorials' own framing,
  which turned out to overstate the surface: a look through the OpenAPI path list for "ui-asset",
  "element", "split", and "template" turned up one panel-creation
  endpoint (`/create-ui-asset`, + `GET`/`DELETE /ui-assets/{id}`) — no
  separate batch-icon endpoint, no states endpoint, no nine-slice endpoint,
  despite the tutorials describing all three. Closed by the `uiAsset`
  generator (plain panel generation only); see `pixellab.md` and
  `docs/GENERATORS.md#uiasset`. That search missed a second UI endpoint,
  `/generate-ui-v2` ("Generate UI (Pro)": one element from a description,
  16px and up, with an optional concept image and palette hint), found on a
  later full read of the path list and now wrapped as the `uiElement`
  generator; see `docs/GENERATORS.md#uielement`. A 32×32 call billed 10 and
  returned 64 candidates (November 2026). **Splitting into individual elements and
  nine-slice are not buildable at all**: `GET /ui-assets/{id}` returns one
  flat composited image with no per-piece sub-image or bounding-box data in
  its response schema, regardless of how many `pieces` the request declared.
  The `delete_ui_asset` MCP tool's own description ("a UI panel and, for a
  template, its split elements + their states") hints PixelLab's internal
  product model has a real split/states concept somewhere, but nothing in
  the public REST surface reaches it. **"States" needed no new mechanism**:
  a themed panel variant (an empty vs. full health bar) is just a plain
  `revision` (image-to-image) of the base panel, the same mechanism every
  other generator already has, so `character`'s dedicated `state` vocabulary
  was not reused or ported. The style-reference-driven icon-batch mode from
  the tutorials is a separate, still-unclosed gap — it does not fit this
  endpoint (one flat panel, not N distinct icons) any better than it fit
  `map`/`1dir`; the `1dir` `batch` field above is the closest existing
  analogue but was built for a different endpoint's `item_descriptions`, not
  this one. **Cost confirmed live, and it overturned the borrowed
  formula**: a real 256x192 call against a Tier 2 account billed exactly 20
  generations (balance 4979.8 → 4959.8), the low end of the `create_ui_asset`
  MCP tool description's then "20-40 generations" claim (10-25 since the
  October 2026 cut). No dedicated cost branch
  exists, so `uiAsset` still falls through to the same canvas-tier formula
  `1dir`/`tiles` use, which — given this generator's 192px floor — always
  predicts the 25 ceiling; the measured call billed the floor price at an
  area well past where that formula would bill the ceiling, so it does not
  actually describe `uiAsset`'s pricing. Left unpatched from one data point:
  over-reading stays the safe `--budget` direction, but a real call likely
  costs about half of what `pixelkiln plan` prints, pending a second size.
- **Skeleton-driven animation** (`POST /animate-with-skeleton-v3`, beta,
  tier 1+ subscription — pose a reference image frame-by-frame from a
  supplied 18-joint skeleton per frame, instead of a text motion
  description) — closed by the `revision` asset shape's `animate-skeleton`
  mode; see `pixellab.md` and `docs/REVISIONS.md#skeleton-driven-animation`.
  `POST /estimate-skeleton` (auto-derive a reference image's own keypoints)
  is wrapped too, but deliberately kept outside the manifest pipeline — a
  standalone `pixelkiln estimate-skeleton` CLI command, not a
  `resolveSpecs`/`estimate()`-time call — so `animate-skeleton`'s submission
  composes exactly one PixelLab endpoint, not two chained together. Both
  endpoints have since run live once (8 frames billed exactly 3), and the
  run found that `description` is required, which `plan` now enforces. **Correcting this catalog's own prior research**: this entry
  used to also claim a distinct "animation to animation" endpoint existed,
  for transferring an existing walk cycle's motion onto a different
  character. Checked against the live `animate_with_skeleton_v3` MCP tool
  schema: **there is no such endpoint.** The real composition is
  `estimate-skeleton` run once per frame of a source animation, then
  `animate-with-skeleton-v3` against a *different* reference image reusing
  those keypoints — a two-endpoint composition a person can now build by
  hand with the primitives above, not a primitive pixelkiln itself
  automates. Both endpoints have run live (see above); request field names
  came from the MCP tool schema, and the live run found `description` is required.
- **Remove background** (`/remove-background`, a transparent cutout of one
  image up to 400x400, `simple` or `complex` task, optional foreground text
  hint) — closed by the `revision` asset shape's `remove-background` mode.
  Cost is the measured 1 generation from docs/ENDPOINTS.md's utilities
  table; the `complex` task and the text hint have not been exercised live.
- **The legacy `/animate-with-skeleton`** (no `-v3`) is deliberately not
  wrapped: its live schema takes exactly 3 skeleton frames per call (other
  counts are a 422), plus view, direction, init-image and inpainting
  parameters, while v3 takes 3 to 15 frames. `animate-skeleton` covers the
  same job.

- **Fonts** (`/generate-font-pro`, an 80-glyph atlas plus a `.ttf` from a
  style description) — no tutorial demonstrated it in depth, so demand is
  unconfirmed beyond the endpoint's existence. Closed by `pixelkiln font`, a
  standalone command rather than a generator: a font has no style suffix,
  candidates, or image-shaped primary output for the lockfile to track. The
  documented price (15 since October 2026, 25 before) is unmeasured.
- **Unzoom** (`/unzoom`, recover the native grid of upscaled pixel art) —
  PixelLab's own API overview calls upscaled reference art "the most common
  cause of disappointing output" from every reference-taking endpoint.
  Closed by `pixelkiln unzoom`, a standalone command on a loose file, since
  the art it is for comes from outside the manifest. Its result is opaque
  (transparency is composited onto white first). Cost unmeasured.
- **Image to Pixel Art Pro Flash** (`/image-to-pixelart-pro-flash`, added in
  PixelLab 0.4.128, October 2026) — converts a photo, painting, or render
  into pixel art, choosing the output size itself. Closed by `pixelkiln
  pixelate`, a standalone command on a loose file like `unzoom`, since its
  input comes from outside the manifest. Billed a flat 6 generations live;
  the result is opaque on a near-white background (docs/ENDPOINTS.md,
  "Image to Pixel Art Pro Flash, measured").
- **Create VFX** (PixelLab 0.4.128, October 2026) — animated pixel-art
  effects (spells, hits, explosions, auras, weather). Offered only as the
  `vfx_workbench` MCP tool, with no REST endpoint as of October 2026, and free on a
  subscription because it renders a recipe rather than generating. Closed by
  `pixelkiln vfx`, which calls PixelLab's MCP server directly with the same
  API key. It starts from a preset, a saved effect, or a recipe file, adds
  parts, downloads the sheet, GIF, atlas, and optional game pack, and saves
  the recipe so the effect re-renders byte for byte (docs/ENDPOINTS.md, "VFX
  workbench (MCP only), measured"). Effects are also a manifest generator,
  `vfx`, planned, locked, and packed like every other asset (see
  docs/GENERATORS.md). Still open there: a sprite named by asset rather than
  by file, the game pack's per-piece clips, and the effect's anchor in the
  sheet formats. PixelLab 0.4.130 then put a second effects path in the
  REST API: `POST /vfx`, the website's VFX *artist*, which builds an effect
  from a plain-language description and saves it to My effects. It is paid:
  1 generation for a lite effect with no sprite or one up to 128px, up to 28
  for a pro effect around a 512px sprite, charged on delivery and never more
  than twice the quote. Closed as a `vfx` block's `description` (with
  `artist: "lite" | "pro"`) and `pixelkiln vfx --description`. Plans count
  twice the quote. **Measured once**: a lite effect with no sprite billed
  exactly its 1-generation quote, and its sheet (a 3×3 grid with an
  Aseprite-style atlas) cut into 8 correct frames (docs/ENDPOINTS.md). A
  sprite, the pro artist, and changes are unmeasured. Animated sprites (GIF
  or strips) are not sent yet.
- **Normal maps** (`POST /normal-map`, PixelLab 0.4.130) — a sprite's normal
  map for engine lighting, 8 to 512px, up to 32 frames as one strip so the
  light stays steady, `opengl` or `directx` convention, 0.5 generations.
  Closed by the `revision` asset shape's `normal-map` mode (a loop goes as
  one strip and comes back cut into frames; a character's directions are
  refused, since a strip would shape every direction from the first) and the
  standalone `pixelkiln normal-map` command. Styles with `enforcePalette` or
  `quality` refuse it so nothing palette-snaps a normal map. **Measured
  once**: an 8-frame 1304×26 strip billed exactly 0.5 and came back the same
  size with matching alpha. The revision mode then billed 0.5 on a 64×64
  sprite through `pixelkiln gen`.
- **Target palette for Create Image Pro** (`target_palette` on
  `/generate-image-v2`, PixelLab 0.4.130) — an `imagePro` style's `palette`
  is now sent as the colors every pixel must use, with `maxColors` (2 to 64
  per image) and `paletteName`. The beta `smart` mapping is left out because
  PixelLab documents it as single-image only and `imagePro` returns a grid of
  candidates below 171px. **Measured once**: a 64×64 call with the Game Boy
  palette billed exactly 10, and the picked candidate used only those four
  colours.
  **Rolled out** to the other wrapped tools that take it: `imageProFlash`,
  `objectPro` bases, states and `pro` animations, `1dir`, `tiles`, `uiAsset`,
  `uiElement`, Pro and Pro Flash character bases, states, portraits and
  outfits, top-down Pro `terrain`, and `interpolate`/`edit-animation`
  revisions, through one helper (`targetPaletteBody`). `paletteName` and
  `maxColors` are style fields on those generators, hashed only when set; an
  existing style `palette` keeps its hash and is simply sent on regeneration.
  **Measured live** with a Game Boy palette: `imageProFlash` (a 32×32 still, 5, only the four colours) and `tiles` (4 tiles at 16px, 10, every candidate in the palette), matching the plan, as `imagePro` did (10). **The other routes are mocked tests only, costs unmeasured.** **Not done**:
  standard character bases and every character animation (their verified
  `color_image` + `force_colors` swatch stays, and the schema does not say it
  combines), the standard terrain set (the field is "mode='pro' only"), the
  `v3` object animation (`pro` only), `/create-tileset-sidescroller` and the
  `animate*` revisions (no field), `pixelkiln pixelate` (no style), and the
  unwrapped `/create-8-direction-object`, `/generate-with-style-v2`,
  `/image-to-pixelart-pro`, `/animate-with-text-v2`, `/tilesets`.
- **October 2026 Pro price cut** — PixelLab 0.4.128 moved every Pro tool from
  20/25/40 to 10/15/25 generations. Cost estimates now use the new prices,
  and `imagePro` (`generate-image-v2`) is tiered instead of a flat 40: a
  64x64 call billed 10 live. Re-measured `inpaint-v3` calls (256, 288, 352,
  and 384px billed 10, 15, 25, 25) show the breakpoints did not move, despite
  the release notes putting 352-384px in the middle tier (docs/ENDPOINTS.md,
  "October 2026 Pro price cut").
- **Pro Flash for plain image create, edit, and inpaint** — a third image
  tier, distinct from `pixflux`/`map`'s 1-generation endpoints and
  `imagePro`'s `generate-image-v2` (a flat 40 then, 10–25 since October 2026), on the same model
  `character`/`objectPro` already use for their `pro-flash` engine
  (`gpt-image-2.5-flare`), confirmed against PixelLab's MCP tool schemas.
  Demonstrated in "Pixel Art Animation Tutorial: Images Pro Flash, Skeleton
  V3 & PixMiniMax": a styled character from a style image, re-edited
  repeatedly ("give him a winter outfit," then a thicker one from *that*
  result), then inpainted hair, shirt, and pants as separate masked passes.
  Closed by the `imageProFlash` generator (`create`, one style image +
  `styleTraits`, 16–256px in multiples of 4) and a revision's
  `"engine": "pro-flash"`, which sends `image-to-image` to `edit` (text
  method) and `inpaint` to `inpaint` (32–256px in multiples of 4, no
  `strength`). A still's `source_image_id` is recorded and reused when a Pro
  Flash character or object base's `reference` is that still's exact file
  (issue #145). Shape, via `get_pro_flash_capabilities` (a free quote, not
  billed):
  - `create`: native 16×16 (experimental, always grid-corrected), 24×24,
    32×32, 32×48, 64×64, 96×64, 96×96; custom (beta) 16–256 in steps of 4.
    One output, no reference images.
  - `edit`: native 32×32 up to 128×128, custom 32–256 step 4. Two
    `edit_methods`: `"text"` or `"reference"` (one `reference_image` that
    must fit the edit canvas natively). Canvas never grows.
  - `inpaint`: same sizes as `edit`; a rectangle or a same-size mask PNG
    (white = generate, black = preserve). Always crops to the mask.
  - Cost quotes (provisional): `create` 5 at 32 and 64px, 9 at 256px;
    `edit`/`inpaint` 5 at 64px, `inpaint` 6 at 128px; `character` and
    `object` at 64px `image: 5, rotations: 1, total: 6`, matching
    pixelkiln's measured `proFlashCharacterCost`. Only `create` has been billed
    live (a 32×32 still with a palette, 5); `edit` and `inpaint` have not.

  Still unmodeled: `edit`'s `"reference"` method, the
  `use_color_palette_correction` flag (snap the edit back to the source's
  palette), inpaint's three `output_methods` (`"New layer with changes"`,
  `"Modify current layer, only changes"`, `"Modify current layer"`), and
  `context_image` + a required `bounding_box`, which lets the model see up to
  3× the native canvas of surrounding context — the problem
  `docs/REVISIONS.md`'s "select a sub-region" workaround for `inpaint-v3`'s
  512px ceiling solves by hand today.
- **Portraits and outfit transfer** (`portrait-character-pro`,
  `transfer-outfit-v2`) — closed as the `character` asset kinds `portrait`
  (a bust of a base or state's south sprite) and `outfit` (an existing
  loop's frames re-clothed from a reference image); see
  `docs/CHARACTERS.md`. Both were live-measured: a 16px portrait billed 20,
  a 2-frame 92×92 outfit transfer billed 20.
- **`/create-8-direction-object`** is deliberately left unwrapped. `objectPro`
  already covers what it does (8 rotations from a prompt or a reference
  image, a `view`, a style image) on `/create-object-pro-flash` at roughly 6
  generations to its 20–40. Its one unique field, `style_object_id` (style
  from an existing 8-direction object's sprites), is not worth a second,
  pricier engine on its own.

## Pro tilesets: what is left after 0.4.130

"PixelLab Pro Tilesets: Full Guide" and the 0.4.130 release ("Tileset Pro
Update... Both top down and sidescroller has been updated! It also supports
connecting different tilesets") are now mostly covered; see the closed
`terrain` entries above. Checked against `/create-tileset` and
`/create-tileset-sidescroller`'s REST schemas, what remains:

- **Pro sidescrollers are web-app only.** The video's sidescroller is the
  Pro form at 16, 32, and 64px with top-layer height up to 100%.
  `/create-tileset-sidescroller` has no `mode` field, and its tile size is
  16 or 32. pixelkiln's sidescroller sets use whatever model that endpoint
  runs.
- **Wall-continuation twins export as duplicates.** The 25-tile layout has
  21 distinct corner combinations. Four tiles share corners with a twin and
  differ only in `pattern_4x4`, which pixelkiln records but cannot express in
  a four-bit Tiled/Godot corner mask.
- **Measured once:** a Pro 32px set billed exactly 15, and a second set
  connected to it through `lower_base_tile_id` billed exactly 15 and shared
  its sand (docs/ENDPOINTS.md). `terrainRoundness: 2` with
  `terrainConnectDiagonals` gave clean 45° edges. A second round confirmed
  Pro at 64px (exactly 25, and 25 tiles at transition 0.5), edge slope and
  an uneven boundary (15 at 32px), standard sets (3 each, under the planned
  4), and connecting through `upper_base_tile_id`. **Still open:** a
  standard set cannot connect to a Pro set, because connected sets share a
  style and a style fixes the mode. Sidescroller tile counts at transition
  sizes other than 0.25 are assumed to be 16. The one sidescroller call
  returned `metadata.transition_size: 0.0` although 0.25 was sent.
- **Prompting advice** lives in the skill reference: end each terrain on
  the word "texture", keep prompts short, and lead with color, season, and
  outline words.

## Generated effects with PixMiniMax

"How to Make Animated Pixel Art VFX in PixelLab" builds effects with
generation rather than the VFX workbench (`vfx`). It draws a sheet of
different effects in one Create Image Pro call, then animates each one with
PixMiniMax. Most of the steps already exist in pixelkiln. An `imagePro`
asset at 64×64 returns 16 candidates, and a prompt that lists one effect
per frame ("an orange fireball facing right, a white and cyan crescent
slash, ...") fills them. `animate-pixminimax` takes the pick as its parent,
`lastFrame` pins an ending (a full ice crystal grown from a few blue pixels,
a splash after a water hammer), and a `"engine": "pro-flash"` revision makes
that ending from the start frame (the video's plain sword, then a "lightning
enhanced version"). `driftThreshold` and a `reduce-colors` revision across
the frame set cover its frame-to-frame color flicker, and `correct-pixelart`
or `pixelkiln edit` covers its stray pixels. The video's frame counts (12,
16, 20, 24) are all multiples of 4, which PixMiniMax requires. What is
missing:

- **Several assets from one candidate sheet.** The video animates eight or
  more effects from two sheets. `pick` gives one `imagePro` asset one
  candidate, so each effect is either its own paid call or a hand-copied
  `source` file. `1dir`'s `batch` is the closest shape, but it fans one call
  out to declared descriptions, not to picks.
- **Padding the canvas before animating.** The video reframes most effects
  onto a larger canvas (64 to 80px) so a flame or splash has room to grow.
  A revision sends its parent at the parent's own size. The workaround is a
  hand-padded `source` file.
- **Trimming a loop's repeated frame.** The video deletes the last frame of
  a fireball loop because it repeats the first. `animate_image_pixminimax`
  says `get_image` returns `frame_count + 1` images with index 0 the input
  unchanged. Confirmed live (November 2026): an 8-frame clip came back as 9
  frames and a 16-frame clip as 17, with pixelkiln's frame extraction reading
  all of them, so the input frame is in the set. There is no manifest way to
  drop a frame.
- **The cost estimate used to under-read long clips (fixed).** The MCP tool
  prices PixMiniMax by generation time: 64×64 at 4, 8, 16, and 40 frames costs
  1, 1, 2, and 6 generations. pixelkiln's old placeholder,
  `ceil(width × height × frames / 65536)`, gave 1, 1, 1, and 3, and a live
  16-frame clip billed 2 against a plan of 1. The estimate (`pixMiniMaxCost`)
  now follows the published points and extrapolates above them; the 40-frame
  point has not been billed.
- **Joining two clips.** The video joins two orb animations end to end in
  Aseprite. pixelkiln has no frame-set concatenation; `lastFrame` can pin a
  clip's ending to another clip's frame file, but the two sets stay separate.

## Map Workshop (scene composition)

PixelLab's actual scene-building surface: lay out a tile floor, place
characters into the scene purely for in-canvas scale reference ("really
important... without it, it's very easy to accidentally generate furniture
that's way too big or way too small" — Create Interior Maps), in-paint
sections in place (with a documented two-tier cost: a "default" model at 1
credit, a "pro" model that costs more but handles complex prompts better),
place movable/duplicable objects distinct from permanent in-painting, extend
an existing tileset by anchoring one terrain slot to what's already there and
describing only the new terrain, and export the whole map (tilesets, full
composite, and every object as separate files). Demonstrated at length in
"Create Interior Maps," "PixelLab Map Workshop Tutorial," "How to Create
Destructible Environments in Seconds," and "Create a Full Side Scroller
Level." Zero pixelkiln analogue for the scene editor itself — and see
pixellab.md for the naming collision with pixelkiln's own unrelated `map`
generator. The one part the public API exposes, `/map-objects` style matching
(`background_image` + `inpainting`), is closed: a `map` asset's `scene` field
(issue #216).

One concrete, recurring gotcha worth carrying into any future implementation:
default/generic object prompts in Map Workshop reliably come out oversized
relative to the placed scale reference; appending an explicit size qualifier
("small") is the demonstrated fix, repeated across a table, a floor lamp, a
fridge, and a bed in "Create Interior Maps" alone.

PixelLab's own official Map-Workshop-to-Godot export ("Export Your PixelLab
Map to Godot in 3 Minutes") needs a third-party community plugin and manual
tile-size entry. PixelKiln's independent Godot exporter
(`pack --format godot`, `src/pipeline/tileset-export.ts`) already writes a
native Godot 4 `TileSet` resource directly, verified in CI — worth knowing if
Map Workshop parity is ever considered, since the export leg is arguably
already solved better here than in PixelLab's own reference flow.

## Animation-to-animation motion transfer

Transferring the motion of an *existing* walk cycle onto a newly described or
referenced character — demonstrated in "How to Make Walking Animations for
Pixel Art Characters in PixelLab." As corrected in the now-closed
skeleton-driven-animation entry above: this is not one endpoint, it is
`estimate-skeleton` run per frame of the source animation plus
`animate-with-skeleton-v3` against the new character's reference image
reusing those keypoints. Both primitives exist in this adapter now
(`animate-skeleton` revision mode, `pixelkiln estimate-skeleton`), so a
person can build this by hand today — chaining `estimate-skeleton` calls
across a source animation's frames into one keypoints file, then pointing an
`animate-skeleton` revision's `from` at a different character. What remains
a real gap is automating that chain as its own pixelkiln capability (one
command, not N manual `estimate-skeleton` calls plus hand-assembling the
result into a `SkeletonSetSchema` file) — worth scoping once the base
`animate-skeleton` mode has shipped and seen real use.

## Not PixelLab gaps at all — different products, no action implied

- **PixelLab's Game Builder** (hosted web IDE, its own chat agent, git-backed
  projects) and its **`agent_*` MCP tools** (`agent_list`/`agent_talk`/
  `agent_inspect`/`agent_feedback`/`agent_help`) manage a *separate* PixelLab
  product — "deploy your own agent," confirmed directly from the live tool
  schemas — unrelated to game-asset generation. Nothing to build here.
- Lip-sync/vocal-animation/talking-gif are named as out of scope in
  docs/PIXELLAB.md, with no in-flight work.
