# Tiles, terrain and engine exports

Read this reference when the person wants ground, a coastline, cliffs, roads,
a dungeon floor, or any set of tiles that must join, or wants a tileset in
Tiled, Godot or LDtk. The full detail is in `docs/TILES.md`; the generator
knobs are in [pixellab.md](./pixellab.md) and `docs/GENERATORS.md`; the flags
are in `docs/CLI.md`, "export".

## What a tileset is here

A set of tile images is not a tileset until something says which tile goes
next to which. PixelLab returns that with the images, and PixelKiln keeps it
in the lockfile entry (`providerMetadata.pixellab`) so nobody has to guess
from file names:

- a **corner** set names a terrain on each of a tile's four corners (NW, NE,
  SW, SE). Corner masks use bits 3, 2, 1, 0 for NW, NE, SW, SE, and a set bit
  means the set's first terrain.
- an **edge** set names one on each side (PixelLab's `tiles` with a
  `tileFeature` can return one). Edge masks use bits 0, 1, 2, 3 for N, E, S, W.
- a tile with no rule is a **stamp**: it goes in the atlas but no engine
  brush uses it.

Never infer a tile's rule from its file name or position. Read the lock entry,
or export `--format generic`, which keeps every rule PixelKiln does not map.

## Pick the generator

| The person wants… | Use | Notes |
|---|---|---|
| two surfaces that meet (water and sand, floor and cliff) | `terrain` | 16 tiles, or 25 with tall walls. Prompt: `1). lower 2). upper`, optionally `3). transition`. Square, top-down or side-on only. |
| a path or road network | `tiles` with `tileFeature: "roads"` | 18 tiles for the path configurations. |
| a rougher transition than `terrain` gives, or an isometric or hex set | `tiles` with `tileFeature: "tileset"` | 16-tile corner set; describe the transition itself in the prompt. |
| a floor, wall and doorway kit | `tiles` with `tileFeature: "building"` | May include stamp-only images. |
| several ground variations to pick from | `tiles`, no `tileFeature` | Normal review-and-pick; no rules, so it exports as a plain atlas. |
| one raised block or mesa | `isometricTile` | One standalone tile. It is not a set and `export` skips it. |
| a platform seen from the side | `terrain` with `terrainOrientation: "sidescroller"` | Prompt: `1). platform body 2). top layer`. |

Start with `terrain` for ground that meets other ground. Its response names
every tile's corners directly, and it costs the least of the set generators.

Prompt each terrain as a short material ending in "texture". Put style words in
the style's `promptPrefix`/`promptSuffix`; they wrap each terrain separately.
Terrain references, Pro shape controls and the rest are in
[pixellab.md](./pixellab.md).

## The usual run

```bash
pixelkiln doctor --dry-run
pixelkiln plan
pixelkiln gen --budget <approved-generations>
pixelkiln export --style ground --only coast --format tiled
```

A terrain set resolves straight to a finished asset: one file per tile, no
candidates to pick. Report the price from `plan` and get a yes before `gen`,
as for any paid work. Measured costs: a Pro set billed 15 at 32px, standard
1 to 3; a connected set bills like any other, so three sets cost three times
one.

Changing any terrain setting marks the set stale and `plan` names the setting.
Regenerating a set that others connect to marks those stale too, so ask before
redrawing a parent.

## Connected sets

Ocean, sand, grass and a path on one map need a set for every pair that
touches. Sets share a terrain through `connect`, keyed by the connecting set's
own side:

```jsonc
{
  "styles": { "ground": { "generator": "terrain", "outDir": "art/ground" } },
  "assets": {
    "coast":  { "prompt": "1). deep ocean water texture 2). plain smooth sand texture" },
    "meadow": { "prompt": "1). plain smooth sand texture 2). short green grass texture",
                "connect": { "lower": { "of": "coast", "terrain": "upper" } } },
    "forest": { "prompt": "1). short green grass texture 2). dark forest floor texture",
                "connect": { "lower": { "of": "meadow", "terrain": "upper" } } }
  }
}
```

"This set's lower terrain is `coast`'s upper." The parent generates first and
the child waits for it. Rules that trip people:

- Sharing a terrain makes it available, not blendable. Two terrains with no
  set of their own between them meet with a hard edge. Plan a set for every
  pair that touches.
- Connected sets share one style, so they share its `terrainMode`: a standard
  set cannot connect to a Pro one.
- A sidescroller set connects only its platform (`lower`).
- Cycles are refused.
- Write the same wording for the shared surface in both sets. It is how the
  merged tileset is named (below), and it keeps the art consistent.

## Export

```bash
pixelkiln export --style ground --only coast --format generic   # default
pixelkiln export --style ground --only coast --format tiled
pixelkiln export --style ground --only coast --format godot
pixelkiln export --style ground --only coast --format ldtk
pixelkiln export --style ground --format tiled --merge-connected
```

Files land in the style's `outDir` as `<asset>-tileset.png`,
`<asset>-tileset.<ext>` and `<asset>-tileset.pixelkiln.json` (the record of
inputs and output hashes). `--out <base>` names one result, `--columns <n>`
sets atlas columns.

| Format | Writes | What the engine gets |
|---|---|---|
| `generic` | `.json` | The lossless contract: atlas, every tile's rectangle, mask or corners, and the provider's raw rules. Use it for any engine without an exporter, and for anything below that is refused. |
| `tiled` | `.tsj` | An image tileset with a Wang set; ids in Tiled's own order. |
| `godot` | `.tres` | A `TileSet` with terrain peering bits on every tile. Corner sets use match-corners, edge sets match-sides. A tile that meets two terrains is written once per terrain (alternatives of one image), which is what lets either terrain's brush draw its own border. |
| `ldtk` | `.ldtk` | A whole project: tileset, an IntGrid layer plus an auto-rule layer, and a Preview level. Corner sets paint on a grid shifted half a tile. |

What export refuses, and what to do instead:

| Case | Use instead |
|---|---|
| six-edge hex masks | `generic` only. |
| `outline` or building images with no rule | `generic`; engine exporters will not invent placement. |
| Godot edge masks on an oblique tile | `generic` or `tiled`. Isometric edge sets export. |
| LDtk for hex, isometric, oblique, non-square tiles | `generic` or `tiled`; LDtk takes square tiles on an orthogonal grid. |
| tiles of different sizes | Engine formats need one cell size; `generic` does not. |

### Isometric sets

An isometric tile image is taller than its diamond (the sides of a block hang
below it), so the export finds the diamond from the art's alpha and writes it as
`footprint` in the generic file. Godot then gets the diamond as `tile_size`, a
`texture_origin` per tile that puts the image on its cell, and the diamond
layout; Tiled gets an isometric `grid` and a `tileoffset`. Filled-square tiles
have no diamond and get none of that. Edge-ruled isometric sets export to Godot
too: the north, east, south and west bits are the diamond's top-right,
bottom-right, bottom-left and top-left sides. When someone reports isometric
tiles sitting too high or spaced wrong, check `footprint` in the generic export
first. The geometry is described under "Isometric tiles" in `docs/TILES.md`.

A hand-edited set (`pixelkiln edit --only <asset> --style <style> --no-open`)
is exported tile by tile from its edits, and the record names those paths.
A changed output stops the next export instead of being overwritten; `--force`
re-baselines the whole bundle, so read the difference first.

Export never changes source PNGs or the lockfile.

### Building kits

`tileFeature: "building"` returns separate pieces (floor, walls, corners,
pillars, doorways, stairs, solid blocks) with a `composed` rule family, which no
engine exporter maps: export `generic` and place the pieces by cell and height.
`providerRules.parts` names each piece's index; `stack_stride_px` is one level.
Facts that held for the stone-hall kit, to check on another before relying on them:

- Every piece has its floor diamond in the same place, so a piece for cell
  (x, y) at level z is drawn with that point at `((x - y) * fw / 2, (x + y) *
  fh / 2 - z * stride)`, back to front by `x + y`, then z. Take the anchor from
  the floor piece: `footprint` is the diamond of the tile with the most opaque
  pixels, which in a kit is a wall.
- A solid block is two levels high and there is no half block: cut 16 rows from
  the middle of one.
- Stairs are pairs that climb a level between them (40 and 41, north), so a
  two-level rise is two pairs with the upper one on half blocks. The east
  pieces (42, 43) are a smooth ramp.
- Do not sink a full block to support stairs: its lower half shows below the
  floor.

`website/art/pixellab-isometric/compose-hall.py` is a working example (a three-tier
hall with a side room). Look at the render before calling a layout done: the
back walls hide anything behind them, so put doorways and ramps on the open
front, not in a wall that faces away.

### Merging connected sets

Without a flag each set exports as its own two-terrain tileset. In an engine
that is three separate brushes that do not know ocean, sand and grass share
surfaces. `--merge-connected` writes the whole group as one tileset with every
terrain:

- the group is every set linked by `connect`, in either direction. Naming one
  (`--only meadow`) exports all of them.
- every set must be generated. A missing one stops the export and is named.
- terrains that connect become one terrain, numbered in the order the group
  meets them, starting from the set that connects to nothing.
- each terrain is named from the first clause of the description in the set
  that defines it ("deep ocean water texture" gives `deep ocean water texture`
  up to 32 characters), so keep descriptions short and plain.
- the default file name joins the sets (`coast-meadow-forest-tileset`).
  Generic JSON gains `sets` and per-tile `corners`; Tiled gets one Wang set;
  Godot one terrain set; LDtk one value per terrain and a 16 by 12 Preview.
- refused: a group with a sidescroller set, or sets with different tile sizes
  or shapes.
- a `warning:` line under a set means some of its tiles have a role that is not
  in the lock's `terrainTiles`, so the export took their corners by position.
  Tell the user, and if the painted map puts the wrong tiles at the shores,
  regenerate that set. A single-set export prints the same warning.

The flag is opt-in on purpose. Without it, existing exports and their file
names do not move, and a game that loads `coast-tileset` keeps working. Do not
add the flag to someone's existing export command unasked; offer it when they
want one brush for several surfaces.

## What has been checked, and what has not

Tell the person when it matters:

- Godot painting: a headless Godot 4.7.2 in CI paints a square corner set, a
  square edge set, an isometric corner set, an isometric edge set and the real
  three-terrain coast set with `set_cells_terrain_connect(..., false)` (the
  editor's own setting) and compares every corner or side with the strokes. A
  road network painted from the real isometric road set ran unbroken with
  correct corners and T-junctions. To paint, fill the ground with the lowest
  terrain's plain tile first, then paint higher terrains on top; a script must
  pass `ignore_empty_terrains` as `false`. A higher terrain painted up to the
  map's edge gets a border of the first terrain there (a road off the side ends
  in a cap); Godot's solver does that, not the export, so paint one cell past
  the camera's edge. The first terrain fills to the edge cleanly.
- Godot isometric geometry: a 2x2 block of cells drawn in Godot 4.7.2 filled
  exactly the diamond lattice the cells predict, for the real 32px ground set.
- Godot: the `.tres` for a square corner set and an isometric set loads in a
  headless Godot 4.7.2 in CI, and a peering bit reads back.
- LDtk: a 16-tile corner set was opened by hand in LDtk 1.5.3. The preview
  drew correctly, LDtk's own rule matching reproduced the stored tiles, and
  painting redrew the right tiles. Edge sets are covered by tests only.
- Tiled: Tiled 1.12.2 loaded the `.tsj` for two single corner sets, a merged
  three-terrain coast, an isometric corner set and the isometric road (edge)
  set, and its own Wang tool painted each with no missing or wrong cells; the
  isometric `tileoffset` drew correctly. Checked by hand once (November 2026),
  not in CI.
- Merged exports: tested through the `export` command. A merged LDtk project
  (two connected sets from real art, three terrains) was opened in LDtk 1.5.3:
  the preview drew every border, LDtk's own rules reproduced all stored tiles,
  and painting redrew correctly. The merged Godot export paints in headless
  Godot. Painting two terrains that have no set between them leaves empty cells
  in LDtk, as expected. A merged Tiled export painted cleanly in Tiled 1.12.2.

Before the person relies on a format, suggest opening one file in the engine
and painting a few cells.

## Before reporting a tileset as done

- `pixelkiln plan` shows the asset `ok`, and `pixelkiln audit --check` passes.
- Look at the atlas PNG. Seams at the tile edges, a blank tile, or two
  surfaces that do not match their neighbours' wording means it is not done,
  whatever the exit code.
- Check the count: 16, 18 or 25 tiles as the generator promises. Report the
  tile size, the atlas size, the format and the three files written.
- For a connected group, list the terrains in order and name any pair that
  touches but has no set between them.
- State what was not checked (the engine, edge sets, a merged file).

## Pointers

- `docs/TILES.md`: stored state, the `terrain` shape, each format's mapping,
  Connected sets, and the deliberate limits.
- The website's `/tiles` page shows real output and the export commands.
- `docs/LIBRARY.md`, "Export generated tiles": `exportTileset()`, `connectedGroup()` and
  `exportMergedTilesets()` from code.
