# Parallax backgrounds

PixelKiln has no parallax command or manifest field yet. This page is what the
research so far supports. The full note, with pictures and numbers, is at
https://pixelkiln.griffen.codes/docs/research-parallax.

## The route to try first

Compose each layer in the engine from separate silhouettes rather than cutting
layers out of one scene. Generate a few distant landforms per biome, one at a
time, each "fading to nothing at its foot, no ground plane, no sky, isolated
landform only, transparent background". In the game, lay them in overlapping
runs (each next one about 72% of the way across the last, random flips, never
the same twice in a row, a few pixels of jitter), in two tiers tinted toward a
dusk or haze colour, over a sky the engine draws. Nothing hidden has to be
invented, and a run can be as wide as the level. A game using PixelKiln ships
this; its numbers are in step 12 of the research note.

- Small, close rates for the tiers (0.85 and 0.92 of the camera) keep them
  together; wide spreads open bands of sky between them.
- Anchor the layers where they sit with parallax off and let them only rise,
  and fill the strip a rising layer uncovers with a thin band of distant
  ground, not sky, so nothing floats.
- A bounded level needs no loop: extend each run past both ends by the most
  that layer can drift.

## Generating whole layers

- PixelLab pixflux with ONE forced palette (`palette`) on every layer is the
  cheapest route that gives layers which agree: four layers for four
  generations. Opaque sky; the other layers with background removal, at most
  40,000 px each (400×100) to stay transparent. pixflux has no seamless
  option, so loop each layer afterwards.
- Retro Diffusion's `rd_plus__environment` draws a whole scene whatever the
  prompt says, so it is not a layer generator. Its `tileX` does wrap the
  drawing, but `removeBg` breaks the seam it made.
- Pixel-art background removal is all or nothing per pixel: a silhouette asked
  to fade at its foot comes back with a hard base. Plan a dithered fade, a
  ground strip or a treeline in front.

## Before generating

- A parallax background is several layers, not one scene. A single scenic
  picture has a focal point, and a repeating focal point is obvious. Put
  landmarks on a layer that does not repeat, and keep looping layers free of
  any single landmark.
- No benchmark background wraps horizontally as generated. Ask for seamless
  output where the provider has it (Retro Diffusion `tileX`), or loop the
  result afterwards and check the join.
- Keep the layers on one palette, one width and one horizon row. Far layers
  should sit closer to the sky colour and lower in contrast. PixelLab's scenes
  already do this; Retro Diffusion's and ComfyUI's benchmark scenes did not.

## Splitting a picture you already have

- A monocular depth model (Depth Anything V2 Small, Apache-2.0, about a second
  on a CPU) gives usable bands for an open landscape. Colour alone does not.
- It fails on a scene framed by tall near objects, and anything floating
  (smoke, clouds, a moon) must be cut out as its own sprite.
- Cut per pixel, not per column, so floating things keep their own layer.
- Whatever a near layer hid has to be invented when it moves. Say so before
  promising a clean result from a flat picture. PixelLab `inpaint_image` on
  the invented pixels gives a believable fill and leaves the rest untouched,
  at 10 to 25 generations a layer by canvas size.
- Do not reach for a layer-splitting model (Qwen-Image-Layered) for depth
  bands: it separated sky from everything else, kept near and far land in
  one layer, and took over half an hour a picture on a 12 GB card.
- For ground that recedes to a horizon, per-row (line) scrolling of the one
  picture needs no cutting at all, but it shears tall shapes.

## In the game

- Round the camera to whole pixels first, then derive each layer's offset from
  that. Rounding each layer separately moves layers while the camera is still.
- Factors of 1/2, 1/4 and 1/8 step on an even rhythm; 0.3 or 0.6 do not.
- Engine settings for a layer at a quarter of the camera's speed: Tiled
  `parallaxx: 0.25`; Godot `Parallax2D.scroll_scale = (0.25, 1)`; Phaser
  `setScrollFactor(0.25, 1)`; LDtk `parallaxFactorX: 0.75` with
  `parallaxScaling: false`. LDtk's factor is how much the layer follows the
  camera, and with scaling on it also shrinks the layer off the pixel grid.
  PixelKiln's LDtk export writes factor 0 today.
