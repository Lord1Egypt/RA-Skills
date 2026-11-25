# Animated effects (VFX)

Read this reference when the person wants a spell, hit, explosion, aura,
shield, status icon, pickup sparkle, projectile, weather, or any other
animated effect, or when a manifest has an asset with a `vfx` block. The full
flag reference is `docs/CLI.md`, "vfx"; the manifest side is
`docs/GENERATORS.md`, "vfx".

## Pick the source first

There are four ways to get an effect. Ask what the effect must do before
choosing, in this order:

| The effect… | Use | Cost |
|---|---|---|
| must fit one sprite's shape (an aura on its outline, a shield around it, a strike that lands on it) | PixelLab workbench with `--sprite` | free on a subscription |
| stands on its own and is placed by a point (torch, explosion, hit spark, coin, projectile, rain) | pixelfx, `--lib pixelfx`; pixel-vfx-codex, `--lib codex`; or a workbench preset without a sprite | free; the local libraries need no account |
| should look different from a second camera (side-on or isometric) | pixel-vfx-codex with `--camera 2d` or `25d` | free |
| is easier to describe than to assemble, or must follow a walk or attack animation | PixelLab's paid artist, `--description` | lite 1–5 generations, pro 6–28, billed up to twice the quote |
| is a drawn object or a character's own motion (a sword turning into lightning, a mage casting) | generation, not `vfx`: an `imagePro` sheet, then an `animate-pixminimax` revision | see [pixellab.md](./pixellab.md) |

A person choosing by eye can browse both free catalogs at
<https://pixelkiln.griffen.codes/effects/catalog>; for the current lists,
run `pixelkiln vfx presets` and `pixelkiln vfx effects`.

Try the free sources first. Tell the person the price and get a yes before
the paid artist or any generation.

**Check what is available before promising a source.** The workbench needs
`PIXELLAB_API_KEY` and a subscription. pixelfx needs the library installed
(below). If the person has neither, say so and ask which to set up; do not
install anything unasked.

## The free sources, side by side

| | PixelLab workbench (default) | pixelfx (`--lib pixelfx`) | pixel-vfx-codex (`--lib codex`) |
|---|---|---|---|
| Runs | on PixelLab, over its MCP server | on this machine, in process | on this machine, in process |
| List | `pixelkiln vfx presets`, `pixelkiln vfx parts` | `pixelkiln vfx effects` (`--json` for every option and default) | `pixelkiln vfx effects --lib codex` (`--json` for parameter ranges) |
| Pick | `--preset <name>`, `--part <name>` (repeatable) | `--effect <category>/<name>` | `--effect <id>`, `--camera 2d\|25d\|3d` |
| Around a sprite | `--sprite <file \| URL \| character:<id>:<dir> \| object:<id>>` | no: every effect stands alone | no: every effect stands alone |
| Colors | sliders on pixellab.ai, pulled back with `--effect <id> --force` | `--palette "#102,#43a,#8cf,#fff"`, dark to bright | `--hue <degrees>` |
| Variation | part sliders | `--seed <n>` | `--param name=value`, `--tune name=value` |
| Speed | `--fps <n>`, 1–60 | `--fps <n>`, 1–60 (changes the frame count) | `--fps <n>`; each camera steps at its own rate (12, 20, 30) |
| Canvas | set by the preset and sprite | the effect's own; `--margin <px>` pads it | cropped to the effect and its pivot; `--margin <px>` pads it |
| Writes | `.png`, `.gif`, `.json`, `.vfx.json`, `-game.zip` with `--game-pack` | `.png`, `.json`, `.vfx.json` (no GIF) | `.png`, `.json`, `.vfx.json` (no GIF) |
| Saved where | the account's My effects, every run | nowhere but the files | nowhere but the files |
| In a manifest | yes, the `vfx` generator | not yet: loose files only | not yet: loose files only |

`--out <base>`, `--force`, `--dry-run` and `--json` mean the same for all
three. `--palette` and `--seed` are refused without `--lib pixelfx`;
`--camera`, `--hue`, `--param` and `--tune` are refused without `--lib codex`;
`--margin` works with either local library. `--preset`, `--part`, `--sprite`,
`--description` and `--game-pack` are refused with a local library.

## PixelLab workbench

```bash
pixelkiln vfx presets
pixelkiln vfx --preset explosion --part scorch_mark --out fx/explosion --game-pack
pixelkiln vfx --preset heal_pillar --sprite sprites/hero.png --out fx/hero-heal
pixelkiln vfx --effect <saved effect id> --out fx/explosion --force
```

- Start from exactly one of `--preset`, `--recipe`, or `--effect <id>`, or
  from `--part` alone. Parts are added on top, in order.
- The workbench renders a recipe; it does not generate. The same recipe
  gives the same pixels, and nothing is billed.
- With `--sprite`, the exported frames **include the sprite**. If the game
  animates that sprite itself, add `--game-pack`: the ZIP holds each layer
  as its own clip with a `manifest.json` of depth, frames and offset, so the
  game can draw its own sprite between the layers behind and in front.
- A recipe stores where the sprite stands, not its pixels. Re-rendering from
  a `.vfx.json` reuses the sprite path the record names; keep that file.
- Every run saves to My effects. When the person tunes the sliders on
  pixellab.ai, pull the change down with `--effect <id> --out <base>
  --force`; never rebuild it from the preset.
- The sprite does not have to be a character. A prop works the same way,
  as a local PNG or as `object:<id>` (both measured, November 2026). The
  preset places it: most stand it on a ground line, `shield_bubble` centres
  it. A preset's canvas does not shrink to a small sprite, so check the
  sheet before calling a 32px prop under a 96x128 strike good.
- "Took longer than 120s and was stopped; nothing was saved" is PixelLab
  timing out a render. Nothing is billed; run the same command again.
- "The pixel tools are busy" means another render is running on the account;
  the command retries on its own.

## pixel-vfx-codex (local)

```bash
npm i github:888wing/pixel-vfx-codex
pixelkiln vfx effects --lib codex
pixelkiln vfx --lib codex --effect fireball --camera 25d --param tailLength=1.6 --hue 40 --out fx/fireball
```

- 138 effects by 888wing and contributors (MIT), not on the npm registry and
  not a package with exports. Installing it is the person's call, as with
  pixelfx; without it the command exits 7 and prints the install line.
- Each effect is defined once in 3D and rendered through `--camera`: `2d`
  (default, 12 fps), `25d` (isometric, 20 fps) or `3d` (orbiting, 30 fps). The
  camera steps the effect at its own rate, so `--fps` above it repeats frames.
- Recolor with `--hue <degrees>`. There is no palette or seed: `--palette`
  and `--seed` are refused. An effect's own settings are `--param name=value`
  (`vfx effects --lib codex --json` lists them with ranges) and the shared
  knobs `--tune size=1.2,density=0.5`.
- It is days old (created November 2026, one author), and its package version
  stays 1.0.0 while its code changes. The record keeps a short hash of the
  engine; if a re-render says the hash differs, the pixels may too.
- Frames are cropped to the effect plus the pivot, so sizes vary from effect
  to effect: read the size from the command's output or the record, do not
  assume one. Diorama props and figures are not drawn.

## pixelfx (local)

```bash
npm i github:patch-gg/pixelfx
pixelkiln vfx effects
pixelkiln vfx --lib pixelfx --effect fire/torch --out fx/torch
pixelkiln vfx --lib pixelfx --effect explosions/small-explosion --palette "#102,#215,#43a,#8cf,#fff" --seed 3 --fps 12 --out fx/boom
```

- pixelfx (<https://github.com/patch-gg/pixelfx>, MIT) is not on the npm
  registry and is not a PixelKiln dependency. Without it the command exits 7
  and prints the install line. Installing a package changes the person's
  project: ask first, then run the line in the project root.
- `vfx effects` is the catalog: id, frame size, and length. Read it rather
  than guessing an id; a wrong id fails and lists the close ones.
- About 70 effects are marked "needs a character" (status effects, auras,
  whole attack moves). They are refused. For those, use the workbench with
  `--sprite`.
- To put one on a character or an object, the game draws it at
  `target − meta.anchor`, after the sprite (in front) or before it (behind).
  Frames are sized for a small character and are not scaled to the sprite;
  check the frame size in `vfx effects` against the sprite before choosing.
- Quote `--palette`: `#` starts a shell comment. A ramp of any length works;
  it is resampled to the steps the effect uses. An effect with no `palette`
  option refuses the flag.
- Lower `--fps` for fewer frames. A 5-second explosion at the default 30 fps
  is over 160 frames; 12 fps is usually enough for pixel art.
- If glow or particles are cut off at the canvas edge, add `--margin <px>`.
- The same recipe and library version write the same bytes. A record made
  with another version still renders, with a note that it may differ.
- Options the flags do not cover (`flip`, `angle`, `light`, and each
  effect's own, listed by `vfx effects --json`) go under `recipe.options`
  in a recipe file passed with `--recipe`.

## The paid artist

```bash
pixelkiln vfx --description "a blue lightning strike that leaves sparks" --out fx/zap --dry-run
pixelkiln vfx --description "a fiery trail behind the robot as it walks" --sprite sprites/walk.png --sprite-frames 8 --out fx/trail
```

- Run it with `--dry-run` first and report the quote and its ceiling (twice
  the quote). Pass `--budget` no higher than what the person approved.
- `--sprite` must be a local PNG up to 512px a side, a horizontal PNG strip
  with `--sprite-frames` (2–32, at most 1,024px wide), or a GIF. No URLs or
  `character:` references. Never rescale pixel art to fit; crop or pad.
- It cannot be mixed with `--preset`, `--recipe`, `--part`, or `--fps`.
- Every new description is a new, billed effect. To change one, pass
  `--effect <id>` with the same `--out`: the record beside it holds the
  conversation that prices the change as a change.
- Its record holds no recipe. For a free, repeatable copy afterwards, run
  `pixelkiln vfx --effect <id> --out <another base>`.

## What a run writes

- `<base>.png`: the spritesheet, frames in a row-major grid on transparency.
- `<base>.json`: an Aseprite-style atlas. `frames[i].frame` is each frame's
  rectangle in play order, `duration` is milliseconds per frame, and
  `meta.anchor` is the effect's pivot on a frame.
- `<base>.vfx.json`: the record. It names the source, the frame facts
  (`width`, `height`, `frames`, `fps`, `loop`, `anchor`), and the recipe.
  Commit it with the sheet.
- `pixelkiln vfx --recipe <base>.vfx.json --out <other base>` renders it
  again. The file says which source it came from, so no `--lib` is needed.
  Flags given with it override the recorded value.

Existing files are never replaced without `--force`. Look at what is there
before passing it.

## Putting an effect in a game

Tell the person these four things when handing an effect over:

1. **Frames.** Play `frames` in order, each for its `duration`.
2. **Position.** Draw a frame's top-left at `target − meta.anchor`. The
   target is the point the effect belongs to: feet for a spawn puff, a hand
   or muzzle for a shot, the contact point for a hit, a wall tile for a
   torch. A standalone effect works over a character, object, tile or UI
   alike.
3. **Loop or one-shot.** The record's `loop` says which. Free a one-shot
   after its last frame.
4. **Blending and order.** Frames are RGBA with straight alpha and the glow
   is already in the alpha, so use normal blending. Draw the effect after
   the thing it sits on; with a game pack, draw the "behind" clips first.

When the effect was built around a sprite and the sheet includes that
sprite, say so: the game should either swap the sprite for the clip while
it plays, or use the game pack's layers around its own sprite.

## In a manifest

Only PixelLab effects can be declared today. A `vfx` style takes assets
with a `vfx` block; `plan`, `gen`, the lockfile, `pack` and the gallery
treat the result as an ordered frame set.

```jsonc
{
  "styles": { "fx": { "generator": "vfx", "outDir": "art/fx" } },
  "assets": {
    "robot.zap": { "vfx": { "preset": "lightning_strike", "sprite": "art/chars/robot-south.png" } },
    "boom": { "vfx": { "preset": "explosion", "parts": [{ "name": "scorch_mark" }], "fps": 12 } },
    "zap.tuned": { "vfx": { "recipe": "fx/zap.vfx.json" } }
  }
}
```

- A `sprite` path may be another asset's output; the effect is blocked
  until that file exists and renders in a later wave.
- An effect goes stale when its preset, parts, fps, recipe content or sprite
  content changes. Slider changes made on pixellab.ai are invisible to
  `plan`: export them with `pixelkiln vfx --effect <id>` and point `recipe`
  at the record.
- A `description` in the block asks the paid artist; `plan` counts it at
  twice the quote.
- A pixelfx effect is not a manifest asset yet. Keep its sheet, atlas and
  `.vfx.json` together in the project and commit all three; a pixelfx
  record as a manifest `recipe` is refused.

## From code

```ts
import { loadPixelfx, listPixelfxEffects, makePixelfxVfx, renderPixelfx } from "pixelkiln"

const lib = await loadPixelfx()
const made = await makePixelfxVfx(lib, { effect: "fire/torch", fps: 12, options: { seed: 4 }, out: "fx/torch" })
const { frames, anchor } = renderPixelfx(lib, { effect: "pickups/coin-spin" })
```

`loadPixelfx()` throws a `capability` error when the library is missing.
`renderPixelfx()` returns one RGBA buffer per frame and writes nothing.
`makeVfx()` and `makeVfxWithArtist()` are the PixelLab equivalents. See
`docs/LIBRARY.md`, "Render effects".

## Before reporting an effect as done

- Look at the sheet. A sheet that is blank, clipped at an edge, or the wrong
  effect is not done, whatever the exit code.
- Report the frame size, frame count, fps, whether it loops, and the pivot,
  from the command's output or the record.
- Say which source made it and what it cost, and name the three files.
- Credit pixelfx when its effects ship: MIT, Copyright (c) 2026 Patch and
  Hugo Duprez (`docs/THIRD_PARTY.md`).
