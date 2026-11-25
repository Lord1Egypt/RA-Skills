# PixelLab

Read this reference when a manifest selects `pixellab`, when choosing between
providers, or before any PixelLab account operation.

## Operational boundary

- Credential: `PIXELLAB_API_KEY` in `.env.local` beside the manifest or in the
  process environment. Never print or commit it.
- Status: production adapter. Generation and account workflows have live
  coverage.
- Cost unit: subscription generations. Copy the exact `pixelkiln plan` total
  into `--budget`; do not translate it into dollars.
- Account operations: balance, adopt, salvage, tag, and separately confirmed
  purge are supported, for characters as well as objects (salvage reviews a
  base with its states and loops as one group). Read `docs/RECOVERY.md`
  before using them.

## Generator choice

| Generator | Use it for | Measured cost |
|---|---|---:|
| `map` | One prop, icon, building, or landmark, up to 400×400 | 1 generation |
| `pixflux` | Closed palettes or full-bleed backgrounds up to 400×400 | 1 generation |
| `1dir` | Reference-guided work or several candidates | 10–25 generations |
| `tiles` | Ground variations or connected structures | 10–25 generations |
| `terrain` | A two-terrain Wang tileset for elevation (grass-to-water, floor-to-cliff), or a sidescroller platform set | Sidescroller **1** on standard and **15** with `terrainMode: "pro"`, measured (3 before PixelLab replaced that model in November 2026). Pro **15** at 32px, measured (a connected second set also billed 15). Pro **25** at 64px and standard **3** measured too; standard plans at 4, the top of PixelLab's quoted 1–4 |
| `imagePro` | A larger or non-square background/scene, or real style transfer; takes the style `palette` as a hard constraint | **10–25 generations** by canvas (64px billed 10; a flat 40 before October 2026) |
| `character` | A character in 4 or 8 directions, its poses (`state`), its loops (`animation`), bust `portrait`s, and `outfit` transfers onto a loop | 1 per standard base, 6 per pro-flash base at 64px (1 from a `reference`), 10–25 per pose or portrait (20–40 before the October 2026 cut), 1 per template loop per direction (2–4 as `skeleton-v3`), 20 per outfit (measured once, before the cut) |
| `objectPro` | A prop, creature, or vehicle that needs rotations, states, or loops but has no character rig | 6 per base (billed 6 at 32px, November 2026; 1 from a `reference`, unmeasured); states and animations assumed to match `character` pro-flash |
| `isometricTile` | One standalone isometric tile (a raised mesa, a cliff block), 16–64px | **1 generation, measured once** (32px `block`) |
| `uiAsset` | A UI panel, button, health bar, or other chrome, from precise `pieces` and/or named `elements` | **20 generations, measured once** (256×192, before the October 2026 cut); the borrowed canvas-tier estimate still predicts the 25 ceiling |
| `uiElement` | One UI element (button, slot, bar, dialogue box) from the prompt, 16px and up, with an optional concept image | 10–25 generations (a 32×32 call billed 10; 64 candidates at 32×32) |
| `vfx` | An animated effect (explosion, aura, lightning, status icons) from a `vfx` block: a `preset` or `recipe`, `parts`, an optional `sprite` to build around; cut into an ordered frame set. Or a `description` (+ `artist`: `lite`/`pro`, a local PNG `sprite`) for PixelLab's paid VFX artist | workbench **free** (a renderer, not a model); `description`: lite 1–5, pro 6–28 by sprite size, billed up to 2× the quote, which is what plan counts (a lite effect with no sprite billed its quote of 1, measured once) |
| `imageProFlash` | A styled still on the Pro Flash model (style image + `styleTraits`), 16–256px in multiples of 4; also the natural source for a Pro Flash character's south sprite | 5–9 generations, PixelLab's provisional quote |

A `pixflux` style's `outline`, `shading`, `detail` and (when stated) `view` are sent to
PixelLab, and it also takes `isometric: true`, `textGuidanceScale` (1 to 20) and
`backgroundRemoval: "complex"`; an asset may set `direction`, which only nudges, so state the
facing in the prompt too. Each new option changes the asset's hash only when set.

For an `animate-skeleton` revision of a character with a staff, sword, cape,
hat or tail, build a custom rig: `pixelkiln estimate-skeleton <sprite> --custom
--description "<what it is>" --action "<what it will do>" --out <file>` (1
generation, about a minute; ask first, it is a direct paid call outside the
budget). The file keeps the rig and its poses name the rig's joints. Check it
with `skeleton-preview` (props in yellow) before animating. Set
`writeMotionFrames` on the revision to have PixelLab write the motion from the
prompt instead of posing every frame. Keep the rig file once animated from:
joint names change between estimates.

A `portrait` cannot be pinned to a seed: sent one, PixelLab ignores the
character and draws a generic face (measured 3 of 3), so `portrait.seed` is
refused and the style's `seed` is never sent to it. The lock keeps the seed the
job reports, but it cannot redraw the portrait; to get a bust back, use
`history` and `restore`, never a regeneration. By default the
bust is attached to the parent's PixelLab character record; when the person
uses that character elsewhere, set `attach: false` rather than skipping the
portrait. To deliver only the bust and keep the parent's rotations out of the
game's art folder, put the style's `outDir` in a scratch folder and give the
portrait a `file` path that lands in the game's art folder, and confirm that
location with the person first because it writes outside the style's `outDir`.

`tiles` is not limited to top-down ground: `tileType` selects the projection
(`isometric` — the API default —, `oblique`, `hex`, `hex_pointy`, `octagon`,
or `square_topdown`), `tileSize` sets one tile's edge in pixels (16–128 — the
API's real ceiling; connectable sets via `tileFeature` have tighter per-shape
ranges, and square top-down roads are exactly 32), and `tileView` sets the
camera (`top-down`, `high top-down`, `low top-down`, or `side`). `outlineMode`
chooses `outline` (a dark border per tile — right for tiles meant to read as
discrete objects) or `segmentation` (no border, so a ground set tiles
seamlessly instead of quilting at every cell edge — this alone decided
whether a measured terrain set was usable). Isometric road sets (48 to
96px) trade off: `low top-down` with `segmentation` is seamless but a flat 3:1
diamond that reads as top-down; `high top-down` makes a 2:1 diamond, but with
`segmentation` it left grass fragments outside the slab on 17 of 18 tiles, and
with `outline` every tile has a border, so a map shows a grid. Paint a map with
a road set before choosing. `tileFeature` asks for a
connectable set instead of independent variations: `roads` for an
18-configuration path set, `tileset` for a 16-tile Wang corner set — describe
the transition itself in the prompt ("fairway grass to rough meadow"), not
one terrain — or `building` for a floor/wall/doorway construction kit.
Passing `styleImages` overrides `tileType`/`tileView` entirely and copies
tile shape and size from the reference instead, the only way to land new
tiles on an existing sheet's ground plane.

A second layer of `tiles` parameters controls shape and depth directly,
beyond the `tileView` presets: `tileHeight` sets a non-square tile's pixel
height explicitly (16–256, e.g. 128 for a 64×128 tile) when the geometry
computed from `tileType`/`tileView` isn't what's wanted; `tileViewAngle`
(0–90 degrees) is a continuous camera angle that overrides `tileView`
entirely (0 = side, 90 = top-down); `tileDepthRatio` (0–1) overrides the
depth/thickness the view would otherwise imply; `tileFlatTopPx` (2 or 4,
`isometric` only) picks the classic 2px diamond cap versus a modern 4px one;
and `obliqueLean` (0–1, `oblique` type and building walls only) sets the
shear per pixel of height — 0.5 is a classic ~27° cabinet lean, 1.0 the full
45° diagonal `oblique` defaults to.

`tileFeature: "building"` takes its own sub-parameters: `buildingWallTiles`
(1–3, default 2) sets wall height in tiles; `buildingLayout` picks `grid`
(paints each shaped piece individually — richer, and the default for
`isometric`) or `materials` (paints flat swatches and renders pieces from
them — more consistent, and the default for `square_topdown`/`oblique`);
`buildingWallDescription`, `buildingFloorDescription`, and
`buildingFloor2Description` (each up to 500 characters) name the wall
material, floor material, and upper-storey/roof surface explicitly rather
than relying on the main prompt being split correctly (`buildingFloor2Description`
defaults to the wall material when omitted); and `buildingWallAngle`
(5–90 degrees, `square_topdown` only) sets the wall storey's own camera
angle independent of the ground pitch.

`terrain` wraps PixelLab's separate `/create-tileset` endpoint, for exactly
the case `tiles`'s own `tileFeature: "tileset"` only approximates: two named
terrain levels — `lower` (the base, e.g. water, grass, lava) and `upper`
(the elevated one, e.g. sand, dirt, stone) — connected by a Wang corner set
that tiles seamlessly. This is the shape for elevation tiers in a map: a
coastline, a dungeon floor breaking into cracked stone, a cliff edge. Unlike
every other generator, its content is not one `prompt` string: `/create-tileset`
takes `lower_description` and `upper_description` as separate fields (plus
an optional `transition_description`), so a `terrain` asset's `prompt` uses
the same numbered convention `tiles` already asks for — `"1). deep ocean
water 2). golden sandy beach 3). wet sand with foam"` — split client-side
into the three fields before the call, with the style's `promptPrefix`/
`promptSuffix` wrapped around each one individually rather than the whole
string once.

A set is 16 tiles, or 25 in the tall layout: `terrainTransitionSize` 1 on
standard, or anything above 0.4 on Pro (so 0.5 is already 25 tiles). There
the step between levels is a wall and corners take a third "transition"
value. A set always resolves straight to a finished asset with one output
file per tile, never a candidate sheet to pick from, the same as a
connectable `tiles` set. `terrainTileSize` sets the tile edge (16 or 32 in
both modes, 64 needs `terrainMode: "pro"`, default 16).
`terrainTransitionSize` is 0, 0.25, 0.5, or 1 without `terrainShapeStyle`
(any value 0–1 with it, though above 0.5 switches to an extended 32-tile
layout pixelkiln does not model). Pro reads it as wall height: 0 flat, 0.25
a low bank, 0.5 or 1 a proper wall. `terrainView` picks `low top-down` or
`high top-down` (API default). The style's `outline`/`shading`/`detail`
apply here too.

`terrainMode: "standard"` (the default) is the classic Wang pipeline,
optionally with `terrainShapeStyle` (`square` or `round`) for a fixed
procedural boundary. `terrainMode: "pro"` rejects `terrainShapeStyle` and
shapes the border with its own controls, each refused outside the mode that
reads it:

- `terrainRaggedness` (0–1): boundary noise, half strength on tall sets.
- `terrainRoundness` (0–2): 0 square corners, 1 round, 2 cut at 45°. Pro or
  a shape style; above 1 needs Pro. Defaults 0.85 (Pro), 0.6 (shape style).
- `terrainBoundaryAmplitude` (0–0.3) and `terrainBoundarySeed` (integer):
  how far the border meanders, and which meander. Pro, or a shape style.
- `terrainStepSlope` (0–2): 0 a cliff to 2 a gentle slope. Pro at
  `terrainTransitionSize` 0.25 only.
- `terrainConnectDiagonals` (boolean): joins the two diagonal tiles'
  upper corners into one area. Pro only. With `terrainRoundness: 2` it is
  the fix for 45° paths and coastlines that break into one island per step.

`terrainSpreadX` and `terrainSlopeSize` are deprecated: PixelLab ignores
both now, so leave them out. Reference images, a forced palette, and the
remaining tunables (`tileStrength`, `tilesetAdherence`) are not modeled.

Changing any terrain setting marks the set stale. The Pro shape controls
are in `specHash`; the older ones (`terrainMode`, `terrainTransitionSize`,
`terrainRaggedness`, `terrainShapeStyle`, `terrainView`, the deprecated
pair) and the style's `promptPrefix`/`promptSuffix` are recorded on the
lock entry as `terrainSettings` instead, and `plan` names the one that
changed ("terrainTransitionSize changed from 0.25 to 0.5"). A setting is
compared as written: adding `terrainMode: "standard"` to a style that left
it out is a change, even though it is the default. A set generated before
this record existed has none and stays current until it is regenerated.

**Connected sets.** (How to export one, and `--merge-connected`, are in
[tiles.md](./tiles.md).) An asset's `connect` makes one of its terrains the very
terrain of another set in the same style, so ocean, sand, and grass paint on
one map: `"connect": { "lower": { "of": "coast", "terrain": "upper" } }` is
"this set's lower terrain is `coast`'s upper". The other set generates
first (the connected one is blocked until it is downloaded, and follows in
the next wave), PixelLab draws the shared terrain from its base tile, and
regenerating the other set makes this one stale. Sharing a terrain makes it
available, not blendable: two terrains with no set of their own between
them still meet with a hard (in PixelLab's map tool, black) edge, so plan a
set for every pair that touches. Connected sets share one style, and a style
fixes `terrainMode`, so a standard set cannot connect to a Pro one.

**Sidescroller sets.** `terrainOrientation: "sidescroller"` switches to
`/create-tileset-sidescroller`: a platform seen from the side. The prompt is
`"1). mossy stone bricks texture 2). green grass texture"`, the platform
body and the layer on top of it; the other side of every edge is empty air.
16 or 32px tiles, `terrainTransitionSize` (the top layer's height) 0, 0.25,
0.5, or 1, and none of the mode, view, or shape controls. It billed 3
generations for 16 tiles. A sidescroller set connects only its platform
(`lower`) terrain. PixelLab's Pro sidescroller (64px, taller top layers) is
web-app only.

Prompt each terrain as a short material ending on the word "texture" ("deep
ocean water texture", "plain smooth sand texture"). PixelLab's "Pro
Tilesets: Full Guide" shows that without it, Pro sometimes scatters rocks,
shells, or plants over the surface. Pro needs no long prompts. Put style
words in the style's `promptPrefix`/`promptSuffix` so they wrap each
terrain: color, season, and outline words ("autumn", "frosty", "bold black
outlines with cel shading", "four-color green palette") change the set the
most, so try two or three at a time. With `terrainTransitionSize` above 0.4
on Pro, the third numbered description is the wall itself ("crumbling
dungeon brick wall").

`1dir`'s own candidate mechanic (the size-tiered table above) normally
returns N variations of one prompt. `/create-1-direction-object` also takes
`item_descriptions`: N *distinct* described objects for the same canvas-tiered
price instead. An asset's `batch: { of: "<leader>", index: N }` field claims
a slot in another `1dir` asset's submission (the leader's own `prompt` is
implicitly slot 0); only the leader's `estimate()` prices the call, members
report zero so `--budget` never double-counts one call, and submitting fans
the leader's one job out to every member's own lock entry directly — a
member never calls the provider itself. Every sibling's spec hash includes
the *whole group's* ordered descriptions, so adding, removing, or editing
any one member marks every sibling stale together: PixelLab has no endpoint
to add one more item to an already-submitted batch, so a batch's membership
has to be decided before it's generated, not grown incrementally.
**Confirmed live** on a Tier 2 account: a 32px chest+potion+key batch billed
exactly 20 generations (the ordinary floor tier, unaffected by
`item_descriptions`), and `item_descriptions[0]` does own candidate slot 0 —
frame 0/1/2 came back as the chest/potion/key in exactly the declared order,
the rest of the 64 candidates being the model's ordinary per-slot variety,
not repeats. Only confirmed at this one size; the higher cost tiers are
unconfirmed. See `docs/GENERATORS.md#batch-several-distinct-objects-for-one-calls-cost`.

`imagePro` wraps PixelLab's Pro image tier, `/generate-image-v2` — the
`pixflux`-adjacent gap named in `pixellab-roadmap.md`: real style transfer
and non-square or larger canvases (16–792 wide, 16–688 tall; the exact
ceiling in a corner also depends on aspect ratio, e.g. 512×512 for square or
688×384 for 16:9), where `pixflux` tops out at 400×400 with no style
reference at all. Set the asset's `width`/`height` for anything other than
the style's default square. Unlike every other multi-candidate generator
here, it was a flat 40 generations at any size until PixelLab's October 2026
Pro price cut; it now tiers by canvas at 10/15/25 like the other Pro tools,
and a 64×64 call billed exactly 10 (`docs/ENDPOINTS.md`, "October 2026 Pro
price cut"). One call still returns
several candidates to pick from by the same size tiering as `1dir` (up to
42px: 64, 43–85px: 16, 86–170px: 4, above 170px: 1), reached through the
generic background-job endpoint the same way a `revision` is. The style's
`palette` goes out as the beta `target_palette` (PixelLab 0.4.130): every
pixel of every candidate lands on those 2–256 colours, at no extra cost.
`paletteName` (needs `palette`) names it, and `maxColors` (2–64) caps each
candidate's colours, with or without a palette. The same `target_palette`
now also goes out for `imageProFlash`, `objectPro` (bases, states, `pro`
animations), `1dir`, `tiles`, `uiAsset`, `uiElement`, Pro and Pro Flash
characters (bases, states, portraits, outfits), top-down Pro `terrain`, and
`interpolate`/`edit-animation` revisions, with `paletteName`/`maxColors`
accepted on those generators' styles. Standard characters and character
animations keep their `color_image` swatch, `pixflux` its own, and the
costs with a palette are measured for `imagePro`, `imageProFlash`, and `tiles`, and unmeasured elsewhere (see `docs/GENERATORS.md#target-palette`).
PixelLab's `smart` palette
mapping is not wrapped: it is "single images only", and this endpoint
returns a grid of candidates below 171px. Reference
images and a style image (`reference_images`, `style_image` +
`style_options`, up to 4 subject references plus one style reference) exist
on this endpoint but are not modeled yet. The completed job has been read
live (a 64×64 call billed 10); `pollImagePro` in `src/providers/pixellab.ts`
still reads it defensively.

`objectPro` wraps `/create-object-pro-flash` — the same base → state →
animation family `character` uses (`docs/CHARACTERS.md`), for PixelLab's
separate, skeleton-free "object" entity, distinct from the generic
`/objects` polling resource `1dir`/`map` already share. It reuses
`character`'s own `asset.state`/`asset.animation` authoring fields and
mirror handling verbatim rather than inventing parallel ones — an
`objectPro` asset's `state`/`animation` are validated identically, since an
object's state is a strict subset of a character's (no `paletteFromReference`/
`canvas` equivalent on the API, always inherits the parent's exact canvas)
and its animation is the same minus the template/skeleton concept objects
have none of: `template`, `subject`, `outline`, `shading`, `detail` on an
`objectPro` animation are rejected at resolve time rather than silently
dropped. `objectDirections` (1 or 8, default 8) is a real choice `character`
pro-flash does not offer (always 8); a 1-direction object's animation must
target `south` — passing any other direction, or `directions` at all to the
API for a 1-direction object, is what the endpoint itself 400s on.
Regenerating an already-animated direction is simpler than `character`'s
own "find and delete the prior take" dance: `/objects/{id}/animations` has
its own `replace_existing` flag, which PixelKiln always passes. **Cost: the
base is measured** (32px billed 6 and returned 8 files, November 2026) —
`objectProCost()` prices it identically to `character` pro-flash's own
measured formula (`proFlashCharacterCost`), since the request bodies are
near-identical minus `template_id`. States and `pro` animations are still
that assumption, pending a live check.
`objectPro`'s own place in `pixelkiln adopt` is not modeled yet. (N distinct
objects from one call, PixelLab's Object Creator "pack", is the `1dir`
`batch` field above.) `pixelkiln gallery --edit` offers "+ New state" and
"+ New animation" on a `character` or `objectPro` base/state's drawer, same
family, same manifest-only write "+ New revision" does — it writes the
`asset.state`/`asset.animation` fields above (minus `startFrame`/`endFrame`
and template `outline`/`shading`/`detail`, which need a manifest-relative
image the gallery does not offer) and leaves generation to `gen` or the
page's own budget, same as any other added asset.

`isometricTile` wraps a *third*, separate path to isometric content:
`/create-isometric-tile`, distinct from both `tiles`' own `tileType:
"isometric"` (a full connectable set) and `terrain`'s `/create-tileset`
(confirmed square-only — no isometric option exists there at all). It
generates one standalone tile, no candidates, no connectable set — the
shape for a per-tile elevation primitive (a raised mesa, a cliff block) when
a connected ground set is not what's needed. `isometricTileShape` controls
vertical thickness — `"thin tile"` (~15% canvas height), `"thick tile"`
(~25%), or `"block"` (~50%, the API default) — the most direct
height/elevation knob of any generator here. `isometricTileSize` is the
API's own tile grid (16 or 32, default 16), separate from `size` (the 16–64px
generation canvas; the endpoint's own guidance is that sizes above 24px
"often produce better quality results"). `outline` defaults to `"lineless"`
on this endpoint specifically (`tiles-pro`'s own default is `"outline"`),
with its own three-value enum (`"single color outline"`, `"selective
outline"`, `"lineless"`); `shading`/`detail` reuse the same enums `terrain`
does. **Cost: 1 generation flat, measured** — PixelLab's own OpenAPI response
example shows `{ type: "usd", usd: 0.02 }`, which reads as real-dollar
billing, but a real call against a live subscription account billed exactly
1 generation instead (`usage: { type: "generations", generations: 1 }`);
`costUnit` here is `"generations"` like every other generator, not `"usd"`.
Only one size/shape combination (32px, `"block"`) has actually been
measured, and the endpoint documents no size-tiering formula, so
`isometricTileCost()` assumes flat pricing across the 16–64px range rather
than guessing a tier. Style images, `init_image`/`init_image_strength`
(image-to-image), and `color_image` (native forced-palette) exist on this
endpoint and are not modeled yet; pixelkiln's own `palette`/`enforcePalette`
post-processing already works generically on the downloaded tile if a
closed palette is what's actually needed.

`uiAsset` wraps `/create-ui-asset`, the panel-layout UI endpoint. An earlier
OpenAPI path search ("ui-asset", "element", "split", "template") missed the
second UI endpoint, `/generate-ui-v2`, now wrapped as `uiElement` (below);
there is still no batch-icon, states, or nine-slice endpoint, whatever the
tutorials or the `delete_ui_asset` MCP tool's own description ("a UI panel
and, for a template, its split elements + their states") might suggest
about PixelLab's internal product model.
`width`/`height` default to 256×256 and are otherwise non-square capable
like `imagePro`, subject to the endpoint's own aspect-gated tiers (square up
to 512×512, 16:9 up to 688×384, 9:16 up to 384×688, 4:3 up to 600×448, 3:4 up
to 448×600); pixelkiln itself only enforces the loose 192–688px-per-side
floor/ceiling and leaves the exact aspect ceiling to the API. An asset's
`pieces` (exact `rounded_rect`/`circle`/`polygon` regions on a virtual 0–512
canvas, each with a unique `id`) and `elements` (named auto-positioned
scaffolds — `button`, `icon_button`, `toolbar`, `tab`, `panel`, `window`,
`health_bar`, `avatar`, `triangle`, `pentagon`, `hexagon`, `octagon`) combine
freely; omit both for a plain full-canvas panel. A style's `uiColorPalette`
string (e.g. `"brown and gold"`) is a free-text prompt-level hint sent as
`color_palette` — distinct from pixelkiln's own hex-array `palette`, which
still applies as local quantization afterward. **The result is always one
flat composited image**: `GET /ui-assets/{id}`'s response schema carries no
per-piece sub-image or bounding-box data at all, confirmed absent regardless
of how many `pieces` were requested, so there is nothing to crop apart even
though the request's own coordinates would make it possible in principle. A
themed variant of an existing panel (an empty vs. full health bar) needs no
dedicated "state" mechanism — it is a plain `revision` (image-to-image) of
the base panel, the same mechanism every other generator already has.
**Cost: confirmed live at one data point.** A real 256×192 call against a
Tier 2 account billed exactly 20 generations (balance 4979.8 → 4959.8),
matching the low end of the `create_ui_asset` MCP tool's then "20–40
generations" claim (PixelLab cut it to 10–25 in October 2026). No dedicated
cost branch exists, so pixelkiln still estimates it with the same
canvas-tier formula `1dir`/`tiles` use — which predicts the 25 ceiling
for every valid `uiAsset` size, since the 192px floor already clears
that formula's own top tier. The measured call disproves the formula for
this generator (it billed the floor price at an area where `1dir`/`tiles`
would bill the ceiling), but the estimate is left as-is, an intentional
over-read for `--budget`, until a second size is measured.

`uiElement` wraps `/generate-ui-v2` ("Generate UI (Pro)"): one element from
the prompt, no `pieces`/`elements` layout, sizes from 16×16 (up to 792 wide,
688 tall, aspect-gated upstream). A style's one `styleImages` entry becomes
the `concept_image` (design guidance); `uiColorPalette` is sent as
`color_palette`. Reach for it over `uiAsset` for icons, slots, and small
widgets under `uiAsset`'s 192px floor. A 32×32 call billed 10 and returned
64 candidates (November 2026); the plan borrows the 10/15/25 canvas tiers and
counts candidates by size (`uiElementCandidateCount`), and sizes other than
32px are unbilled.

`imageProFlash` wraps `/create-image-pro-flash`, the Pro Flash model as a plain
still: priced 5 up to 96px, 6 up to 208px, 9 beyond (PixelLab's own
provisional `/pro-flash/cost` quotes). Its lock entry keeps PixelLab's
`source_image_id`; a Pro Flash character or object base whose `reference` is
byte-for-byte that still's file is sent the id instead of the upload (same
price, no re-encode). The same model edits and inpaints through a revision's
`"engine": "pro-flash"` (`image-to-image`/`inpaint` only, 32–256px in multiples
of 4, no `strength`), at the Pro Flash tier instead of the Pro endpoints' 10–25.

Do not confuse pixelkiln's `map` generator with PixelLab's own "Map
Workshop": `map` returns one static prop, icon, or building in a single
generation. Its one scene concept is optional: a `map` asset's `scene` (`{
"image": "floor.png", "placement": { "oval": 0.3 } }`, or `rectangle`, or a
`mask` PNG the scene's size) draws the object into that picture, in its style,
still for one generation. The scene can be another asset's output; the object
is blocked until it exists and goes stale when it is redrawn. Whether the
result is the object alone or composited, and where an oval sits, are
unverified; look at the first result before a batch. Map Workshop (scene
composition — laying out a tile floor, placing characters and movable
objects, inpainting sections in place, exporting the result) is a distinct
PixelLab product surface this adapter does not model at all.

A `map` or `pixflux` prompt for anything smaller than a standard prop
(furniture, a hand-held item, a small decoration) tends to come back
oversized relative to the scale implied by the rest of a scene by default.
PixelLab's own tutorials hit this repeatedly and fixed it the same way every
time: add an explicit size qualifier to the prompt ("a small wooden chair",
not "a wooden chair"), rather than adjusting `size` after an oversized
result comes back.

A base can start from the author's own south-facing sprite (`reference` on
the asset; standard wants it at the style's size, v3 up to 256px, pro up
to 168px), and a standard humanoid base takes `proportions` (`chibi`,
`heroic`, or multipliers) on the style or the asset. A pro base can be
designed from a `concept` image (up to 1024px) and follow the look of
another generated character in the style (`styleCharacter`), which makes
that character a dependency the way a loop's parent is.

A `reference`, `concept`, or `styleCharacter` image's own canvas size sets
the output's apparent scale, not just its content: a reference cropped or
padded to a canvas larger than the target size reliably produces an
oversized character next to everything else at the intended size. Match the
reference's canvas to the base's `size` (or the other way around) before
submitting, not after a mismatched result comes back.

A v3 loop can start from a pose image (`startFrame`) or interpolate to one
(`endFrame`), take a `subject` when the character's own description would
mislead, and ask PixelLab to `enhancePrompt`; a template loop takes
`outline`, `shading`, and `detail` overrides instead. `keepFirstFrame`
defaults to `true` on a v3 loop: the parent's resting pose (or `startFrame`,
when set) becomes frame 0 for free, so a requested `frames: 6` delivers 7
files, not 6. Account for the `+1` when checking a loop's output count or
estimating its budget; set it `false` only when the caller will supply its
own first frame downstream.

`"mode": "skeleton-v3"` with a `template` poses that template onto the
character with PixelLab's skeleton video model instead of redrawing each
frame: the steadiest template loop, 2 to 4 generations and 3 to 5 minutes
per direction (plan budgets 4), beta, Tier 1 plans and up. Prefer it over a
plain template loop when identity drift matters and the account qualifies;
plain `template` stays the 1-generation option. It needs a base with a
stored 3D skeleton: a `v3` base has one (measured, 3 generations); a
`standard` base has none, so PixelLab answers a bare 500 and pixelkiln
refuses the loop at `plan`/`validate`, pointing at `mode: "template"`. `pro`
and `pro-flash` bases are not refused but are unverified.

`"mode": "skeleton-v3"` with **no** `template` animates the asset's `prompt`
as a sentence (`frames` 3 to 15, default 8; a v3 base): PixelLab writes it
into one 3D motion. Measured: 8 frames at 64px billed exactly 3 generations
and came back at 96×96, so the canvas can grow. The plan still budgets 4. One
request goes out per direction asset: the first direction of `directions`
leads, and each later one follows in the next wave, sent into the leader's
`animation_group_id` so every direction moves the same way (`animation.motionFrom`,
lock `motionShare`; a live append billed 3 and joined the group, deleting
one direction of a group is unverified, docs/CHARACTERS.md, "Loops from a
sentence"). The
`prompt` is required and gets no style prefix or suffix.

A named `template` loop (`walk`, `breathing-idle`, and similar) is trained
mostly on characters with empty hands, and reliably struggles once a
character holds an item — a weapon, a tool, anything gripped. For a
held-item character, skip the template and write a custom v3 loop with an
explicit prompt naming the held item and the motion (e.g. "knight holding a
sword, walking loop") instead of expecting the template to carry it.

PixelLab's own tutorials announce "Skeleton V3" as the quality jump for named
templates, and that is the `skeleton-v3` mode above, not a change to plain
`template`: the tutorial says the original templates were not recommended
for quality, and the new model is — "the movement is much more usable...
much more stable." For a body the skeleton fits, prefer `skeleton-v3` over
both a plain template and a custom v3 loop when the account is Tier 1+ and
2 to 4 generations a direction is acceptable; plain `template` stays the
1-generation option at its earlier quality. The held-item caveat above was
written about plain templates, and whether `skeleton-v3` shares it is
unmeasured. PixelLab has announced a further Skeleton V3 revision, so recheck
`animate_character`'s tool schema before assuming today's behaviour.

A pose-only `state` edit (a walk mid-step, a hurt pose) can turn the
character sideways or away from the camera by default, even on a prompt that
never mentions rotating — PixelLab's own tutorial hits this on a plain
"mid-walk state" prompt. State the facing explicitly (e.g. add "front-facing"
to the prompt) rather than assuming the parent's own camera angle carries
over automatically.

A loop costs per direction, and a sprite facing one way is the sprite facing
the opposite way flipped — this holds for the east/west pair and for both
diagonal pairs, south-east/south-west and north-east/north-west. Declare the
west loop and make the east one `{ "mirror": "bot.walk.west" }`: PixelKiln
flips it locally for nothing, in the wave after the source lands. South and
north sit on the mirror line itself, so flipping either just relabels the
same asset, not a new one — generate those two directly. Generate south,
south-east, east, north-east, and north, then mirror the other three: eight
directions of one loop are then 5 generations, not 8.

A game whose camera is a fixed isometric angle typically never shows a
character facing due south/east/north/west, only the four diagonals — in
that case, declare `south-east`, `north-east`, `north-west`, and
`south-west` only and skip the cardinal four entirely, rather than
generating all 8 and mirroring the rest. `isometric` on the base (drawing
every direction and loop in isometric perspective) is an independent choice
from this and does not by itself require or imply fewer directions; it is
the game's own camera that decides how many are worth generating.

A loop that needs headroom for an effect — recoil, a muzzle flash, a
projectile, anything that extends past the subject's silhouette — needs
empty canvas space near the subject before generating; a composition with no
margin is a common cause of a failed or clipped loop, and is worth ruling
out before rewriting the prompt. Bigger pose changes want more frames: a
simple loop (a walk, a static idle) reads fine at 6; a transition that
rotates or drops the subject (a fall, a knockdown) wants 8 or more. A
multi-stage action (windup, then attack, then recovery) is a chain of
loops, not one long one: take the final frame of one loop as the next
loop's `startFrame` and link them as separate manifest assets.

A loop's `startFrame` (or the `state` it is seeded from) should already
resemble the target action, not just be a valid pose of the character.
PixelLab's own tutorials show this going wrong concretely: prompting "walk
loop" from a mid-run pose forces the model to close the loop by running,
then walking, then running again, a much harder transition than starting
from a pose that already looks like the first step of a walk.

Write the loop `prompt` (and any `subject` override) as a full descriptive
sentence of the motion — pace, energy, what leads and what follows — rather
than a terse label like "attack": PixelLab's own tutorials treat this as the
single biggest lever on animation quality, on par with frame count. If an
agent drafts the prompt from a reference image, strip any technical framing
it invents (frame rates, frame-count ranges, export terms) before
submitting — PixelLab is never told the target frame rate, only the frame
count, and a stray "24fps" or "60 to 90 frames" fragment in the prompt does
not help.

In the committed environment benchmark, PixelLab followed complex building
prompts more closely and produced broader, more separable depth bands in scenic
backgrounds. Its 256px and 384px map objects were opaque despite the route's
transparency claim, so inspect alpha on one representative result before a
batch. Inspect scenic outputs for stray marks too: one untouched 384px attempt
contained a generated signature-like glyph.

An asset that declares `revision` against a PixelLab style calls `inpaint`
(masked), `image-to-image` (whole-image, no mask), `reduce-colors`
(palette quantize, `/reduce-colors`), `correct-pixelart` (edge/noise
cleanup, `/correct-pixelart`), `remove-background` (transparent cutout,
`/remove-background`, one image up to 400x400, 1 generation measured),
`normal-map` (`/normal-map`, lighting normals for a sprite or a loop sent as
one strip, 0.5 generation per call from the docs, a background job; refused
on a set of directions and in a style with `enforcePalette` or `quality`),
`animate` (`/animate-with-text-v3`),
`animate-pixminimax` (`/animate-pixminimax`, beta, tier 1 subscription or
higher), `animate-skeleton` (`/animate-with-skeleton-v3`, also beta/tier
1+ — poses the source frame-by-frame from a supplied 18-joint skeleton per
frame, via a committed `keypointsFile` rather than a text motion
description), `interpolate` (`/interpolation-v2`, in-betweens from the parent
to a required `lastFrame` keyframe), or `edit-animation` (`/edit-animation-v2`,
one edit across a whole frame set); `outpaint` is refused, since PixelLab has
no canvas-expansion endpoint. `reduce-colors`/`correct-pixelart`/
`remove-background` send no prompt (`remove-background` sends only its
optional `description` as a foreground hint) to PixelLab at all — they are mechanical, not described — and complete
synchronously with no background job, unlike every other PixelLab call this
adapter makes. `animate`/`animate-pixminimax`/`animate-skeleton` DO send the
asset's own prompt, as the motion description (`animate-skeleton` calls it
`action`, alongside a separate optional `description` field for appearance —
the skeleton carries the motion, the text only names it and what the subject
looks like), and produce an ordered **frame set** landing in candidate
review, not a single image — the one revision mode shape that isn't "one
image in, one image out." None of the animate/interpolate/edit-animation
endpoints' completed-job response shape has ever been observed;
`pollAnimateRevision` guesses defensively rather than assume one. Read
`docs/REVISIONS.md`'s PixelLab section before using any of these. A parent
written as a set (a character's directions, an animation's frames) goes to
`reduce-colors`, `correct-pixelart`, and `edit-animation` whole, in one call,
so every member shares one palette or edit; the other modes refuse a set
parent. `reduce-colors`/`correct-pixelart` cost is **confirmed live**: a flat
0.1 generations each (not the schema's dollar-denominated example), at least
at a 32×32 source — `animate`/`animate-pixminimax`/`interpolate`/
`edit-animation` remain schema-only and unexercised.
`animate-skeleton` has run live (8 frames billed exactly 3); its request
field names come from the `animate_with_skeleton_v3` MCP tool schema, a more
authoritative source than the OpenAPI document the others are taken from, and
the run found `description` is required. `estimate-skeleton` (auto-derive a reference image's own keypoints) is
wrapped too, but deliberately as a standalone `pixelkiln estimate-skeleton`
CLI command, never inside `submitRevision` — see
[pixellab-roadmap.md](./pixellab-roadmap.md)'s now-closed skeleton-driven-
animation entry for why composing two endpoints in one submission was
rejected.

`animate-pixminimax`'s `direction` + `enhancePrompt` combination has a
measured-in-practice gotcha, not just a schema quirk: PixelLab's own tutorial
states plainly that `enhancePrompt` can expand the motion description with
camera-relative language ("towards the camera") that fights the requested
world-facing `direction`, and the failure is direction-specific — cardinal
directions came out fine, an off-cardinal one (north-east) did not. When a
multi-directional PixMiniMax animation goes wrong at one or two directions
but not others, suspect the enhanced prompt's own wording before the model or
the `direction` value. The same tutorial states outright that PixMiniMax
"allows up to 40 frames," a second, independent (though still not
live-billed) confirmation of the ceiling above.

For effects, [vfx.md](./vfx.md) is the full reference: which source to
pick (this workbench, the paid artist, or the local pixelfx library), every
control, and how a game plays the result. The notes here are PixelLab's side.

Try `vfx` first for an effect: the workbench is free and re-renders the same
pixels. When presets and parts do not get there and the person would rather
describe the effect, a `vfx` `description` asks PixelLab's paid VFX artist
(`POST /vfx`) instead: it cannot be mixed with `preset`/`recipe`/`parts`/`fps`,
its `sprite` must be a local PNG up to 512px (no `character:` references), and
every regeneration is a new, re-billed effect. For an effect that follows an
animation, make the sprite a horizontal PNG strip and set `spriteFrames` (2 to
32, strip at most 1,024px wide) and optionally `spriteFps`; the lite quote
goes up by 1. Tell the person the price
before running it.
Generate one instead when the effect is a drawn object or a character's own
motion, such as a water hammer that bursts into a splash, a sword turning
into lightning, or a mage casting. PixelLab's "How to Make Animated Pixel
Art VFX" tutorial gives a pattern for that which maps onto what exists. Draw a sheet of different effects in
one `imagePro` call by listing one effect per frame in the prompt (64×64
returns 16 candidates), pick one, and animate it with `animate-pixminimax`.
Pin the ending with `lastFrame` when the motion should arrive somewhere: a
crystal cluster grown from a few hand-placed blue pixels, a splash after a
hammer strike, or the same sprite edited by a `"engine": "pro-flash"`
revision ("make it a lightning-enhanced version") so the clip transforms one
into the other. Describe motion, not appearance, and ask a loop to "return to
its original state at the end." Give a growing effect room: the tutorial
pads most sources onto a larger canvas first, which here means a hand-padded
`source` file, since a revision sends its parent at its own size. Then clean
up: `driftThreshold` or a `reduce-colors` revision over the frame set for
color flicker, `correct-pixelart` or `pixelkiln edit` for stray pixels, and
check a loop's last frame against its first for a duplicate.

Budget `animate-pixminimax` above what `plan` prints for long clips. The MCP
tool prices it by generation time (64×64 at 16 frames is 2, at 40 frames is
6), while pixelkiln's placeholder estimate gives 1 and 3. Tell the person the
plan may under-read before a long PixMiniMax run.

Parts of Pro Flash image editing are still outside this adapter: `edit`'s
reference-image method, palette correction, inpaint's output-method choice,
and inpainting with surrounding `context_image`. See
[pixellab-roadmap.md](./pixellab-roadmap.md) for the confirmed shape.

Six commands call PixelLab on loose files, outside the manifest and
lockfile. `pixelkiln unzoom --from <file> --out <file>` returns upscaled
pixel art to its native grid; run it before outside art becomes a
`reference` or `styleImages` entry (input at least 256×256, result opaque,
cost unmeasured). `pixelkiln pixelate --from <file> --out <file>` converts a
photo, painting, or render into pixel art with Image to Pixel Art Pro Flash:
PixelLab picks the output size, the result is opaque on near-white, an optional
`--description` steers the style, and it costs a flat 6 generations
(measured) after asking first. `pixelkiln normal-map --from <png> [--frames
N] [--convention opengl|directx]` writes a sprite's normal map, or a strip's
(N equal frames side by side, up to 32), for 0.5 generation after asking
first. `pixelkiln vfx --preset <name> --out <base>`
builds an animated effect (explosion, heal pillar, lightning strike, aura,
and more; `pixelkiln vfx presets` and `vfx parts` list them) with PixelLab's
VFX workbench, which is free and reached through PixelLab's MCP server. Add
`--part <name>` to layer parts, `--sprite <file|character:<id>:<dir>>` to
build around a character, and `--game-pack` for per-piece clips. It writes a
spritesheet, GIF, atlas JSON, and a `.vfx.json` record whose recipe
re-renders the same effect with `--recipe`. `pixelkiln vfx --lib pixelfx
--effect <category>/<name> --out <base>` renders one locally from the
pixelfx library instead, with no PixelLab call (see [vfx.md](./vfx.md)).
`pixelkiln vfx --description
<text> [--artist pro] [--sprite <png|gif> --sprite-frames <n> --sprite-fps <n>]
--out <base>` asks the paid VFX artist instead (a GIF or a PNG strip makes the
effect follow the animation), prints
the quote and its 2× ceiling, and asks first; with `--effect <id>` it changes
that saved effect in place. `pixelkiln talk visemes --from <portrait.png> --out <base>` draws a
portrait's mouth positions once (3 generations at 64px; asks first; the portrait needs a visible
mouth), after which `pixelkiln talk gif` and `talk plan --from <base>.talk.json --text <line>`
lip-sync any line for free. `pixelkiln font --description <text> --out <base>` writes a
`.ttf` and an 80-glyph atlas for PixelLab's documented 15 generations, and
asks first. `pixelkiln estimate-skeleton <image> --out <file>` starts an
`animate-skeleton` keypoints file, and `pixelkiln skeleton-preview <asset>`
draws its poses over the source for free. See `docs/CLI.md`, "PixelLab utilities".

For a style aimed at a specific look (a
retro/console feel or a
high-fidelity showcase asset) rather than a default, read
[pixellab-fidelity.md](./pixellab-fidelity.md) before choosing `size`,
`detail`, `shading`, or `outline`. For what PixelLab can do that this adapter
does not yet reach at all, read [pixellab-roadmap.md](./pixellab-roadmap.md)
before proposing new work. To pick which PixelLab endpoint to spend a live run
on, read the [validation
ledger](https://pixelkiln.griffen.codes/docs/endpoints#validation-ledger)
(`docs/ENDPOINTS.md`): it rates each endpoint by what has been measured and
what a wrong guess could cost.

For setup and current field constraints, use
the PixelKiln docs page `pixelkiln.griffen.codes/docs/pixellab`. When working in
the PixelKiln repository, `docs/PIXELLAB.md` and `docs/ENDPOINTS.md` are the
canonical local sources. The provider sources are the PixelLab site
(`pixellab.ai`) and its API reference (`api.pixellab.ai/v2/docs`).
