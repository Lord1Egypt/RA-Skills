# Paperdoll layers

Read this reference when the person wants swappable outfits, hats, hair or
held items on a character, or when a manifest has an asset with `layer`.
PixelLab only. The full guide is `docs/PAPERDOLL.md`.

## What a layer is

- A `layer` asset, in a `character` style, draws its `prompt` over the frames
  of the assets named in `layer.of` (a base, its states, its loops) and writes
  one transparent PNG per source frame. A game draws the source frame, then
  the layer, at the same position.
- All frames go on one sheet and are repainted by one masked inpaint. That is
  what keeps the item the same across frames, so put every asset that must
  match in one layer's `of`. Two layers are two requests and will differ.
- Each layer is one request: 10, 15 or 25 generations by the sheet's size.
  `plan` prices every layer at 25; the lockfile records what was billed.
- It is `blocked` until every source is downloaded, and `stale` when a source
  is regenerated. Regenerating a base or a loop means redrawing every layer
  over it: say so, with the cost, before doing it.

## Choosing how to make an item

| Item | Use |
|---|---|
| Clothing, whole or one garment | `layer` with the default `region` (`body`) |
| Hats, helmets, hair, masks | `"region": "head"` and `padding` |
| Capes, packs, wings, anything worn | `"region": "around"` and `padding` |
| Swords, shields, tools, anything rigid in a hand | `layer.attach` (placed, not drawn) |

Do not inpaint a rigid held item. In measured runs an inpainted sword changed
hands mid-walk and an inpainted shield was drawn face-on in a side view.

## Before generating layers

- The base should be bare and bald with its arms away from the body. Describe
  proportions in the prompt ("adult human figure with adult proportions, slim,
  small head, long legs"); "mannequin" and "doll-like" gave a toddler at 64px.
- Underwear, if wanted, is its own layer drawn under everything. Keep the
  base bare.
- Set `"clean": true` on every loop first. Turning it on later makes the
  layers over that loop stale.
- Nothing in a layer may be cyan or teal: that is the colour skin is keyed
  to, and a layer drops it. `layer.key` changes the colour if an item needs it.

## Writing a layer

- The style's `promptPrefix` and `promptSuffix` are not applied. The prompt
  must stand alone.
- Say that it is a sheet of the same figure and that every one gets the
  **same** item. List its parts and colours. List what not to add.
- For one garment, say both halves: what it covers, and "only that: leave
  the legs, feet, hands, neck and head bare cyan".
- For anything that looks different from the front and the back (hair,
  helmets, packs, robes, capes), list the loops first in `of`, set `columns`
  to the loop's frame count so each loop is one row of the sheet, and say in
  the prompt which way each row faces. Without this some front-facing frames
  come back drawn from behind.
- The sheet must fit 512px a side. Six rows of a 64px figure fit with
  `padding` up to 10, not 12. A layer that does not fit fails before any
  request and names the sizes.
- After it downloads, look at every frame of every loop. One frame facing the
  wrong way is the usual fault. Regenerate with `gen --force --only <asset>`;
  the previous result stays in `pixelkiln history` and restores for free.

## Adjusting without paying

- One frame of a drawn layer wrong, the rest right: `pixelkiln redraw
  <layer> --frame <name>` (run it without `--frame` for the names, with
  `--dry-run` for the price). One small inpaint, 10 to 25 generations,
  outside the plan and `--budget`, so ask before running it. Do not
  regenerate the whole layer for one frame. Run `pixelkiln gen` afterwards:
  recolours of the layer are stale and rebuild free.
- Skin tones are free: derive the base and each loop with `hue-shift`,
  `"hue": [0, 45]` and a `brightness` under 1. Drawn layers go over them
  unchanged. A `grasp` layer holds fingers: derive it the same way with
  `reference` listing the base's frames, so only skin colours change.
- `layer.offset` moves a drawn layer by whole pixels: `[0, -2]` for every
  frame, or `{ "hero.walk.south": [0, -2], "*": [0, 0] }` per source asset.
  A changed offset is `recoverable`; `pixelkiln fetch` re-applies it at no
  cost. Use it for a hat that sits low, never regenerate for that.
- A colour variant of a drawn layer is a `derive` asset, not a new layer:
  `{ "derive": { "from": "hero.cape", "transform": "hue-shift", "degrees":
  -120, "hue": [320, 20] } }` recolours every frame for nothing. `hue` limits
  it to one range of colour so trim in another colour stays. Offer this
  before generating a second layer that differs only in colour.
- `pixelkiln pack --style <style>` puts the character and its layers on one
  sheet; the generic atlas's `layers` section pairs each layer frame with
  the frame it goes over and the offset to draw it at.
- `mask` and `keyed` replace the computed sheet inputs with PNGs the person
  supplies. Every intermediate file is in
  `.pixelkiln/layers/<style>/<asset>/`.

## Held items (`layer.attach`)

- Needs one sprite of the item per direction the frames face
  (`"item": "items/sword-{direction}.png"`) and an anchors file. It draws
  nothing and costs nothing to place.
- `pixelkiln anchors <asset>` writes the anchors file: one skeleton estimate
  per frame at 0.1 generation, outside the plan and `--budget`. State the
  frame count and cost before running it (`--dry-run` reports both). It is
  paid once per character; every item reads the same file, and re-running it
  only pays for new or changed frames.
- The item sprite must be drawn as held (leaning forward, handle down), or it
  stands straight up out of the hand. `tilt` and `lean` turn an upright one.
- `joint` picks the hand, `grip` the point held (`"center"` for a shield),
  `scale` resizes an item that came back too big, `depth` forces it in front
  of or behind the body, `offset` moves it on the hand.
- `"grasp": true` redraws the hand around the handle with one small inpaint.
  That makes the layer a paid one (priced like any layer) and it goes stale
  with its item, anchors and sources. Ask before adding it.
- "changed since its anchor was estimated" means a source frame changed: run
  `pixelkiln anchors <asset>` again.
