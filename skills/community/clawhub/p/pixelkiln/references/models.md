# 3D models: texture fixes, the guide, and Blender

A model is a `.glb` file anywhere under a style's `outDir`. It is not a
manifest asset: it has no plan state, lockfile entry, cost, or `gen` step, and
nothing about it is written to the manifest or the lockfile. `pixelkiln model`
works on these files; the gallery shows the same ones in its **3D models**
section.

## The rule

The model as built is never written. Every change goes to an edited copy
beside it under the style's `edits/` folder:

```text
art/characters/models/knight.glb                     the model as built
art/characters/edits/models/knight.glb               the edited copy
art/characters/edits/models/knight.edit.json         what the copy is based on, per texture
art/characters/edits/models/knight.image-<n>.png     a texture exported for painting
art/characters/edits/models/knight.image-<n>.guide.png
art/characters/edits/models/knight.image-<n>.guide.txt
art/characters/edits/models/knight.image-<n>.pxo     layers, when painted in the gallery
art/characters/edits/models/knight.export.glb        what Blender (or another tool) exported
```

## Which file a game should load

```bash
pixelkiln model resolve knight           # one path, e.g. art/characters/edits/models/knight.glb
pixelkiln model resolve                  # every model: as built -> load (why)
pixelkiln model resolve --json           # styleId, file, load, from, edit, status, absolute
```

`resolve` names the edited copy when its status is `edited` or `unrecorded`,
and the model as built when there is no edit or the edit is `rebuilt-since`
(a note on stderr says so; tell the person, since their fixes are not in the
new build). Point a game's loader or build script at its output rather than
at the `edits/` folder. It reads only. `pack`, `mount`, and `export` do not
read models.

## Find what there is

```bash
pixelkiln model list            # text: meshes, bones, animations, every image and what it is for
pixelkiln model list --json     # the same, plus the edit's status and record
```

Each image is listed by index with its material and role (`base colour`,
`normal map`). Name a texture by index (`--image 8`), by material name
(`--image Helm`, its base colour texture), or `--image Helm:normal` for that
material's normal map. Name a model by its path, its file
name (`knight`), or the gallery id (`model:cast/models/knight.glb`).

An edit's `status` is `edited` (based on the model as it is now),
`rebuilt-since` (the model was rebuilt after the edit; tell the person before
building on it), or `unrecorded` (a file placed by hand, no record).

## Fix a texture by hand

```bash
pixelkiln model export knight --image Helm --no-open
# the person paints edits/models/knight.image-8.png
pixelkiln model import knight --image Helm
```

`export` writes the texture as PNG (decoding a JPEG one), starting from the
edited copy when there is one so earlier fixes carry on, plus the guide:

- `.guide.png`, transparent and the texture's size: each piece of the
  automatic unwrap outlined in its body region's colour and numbered. The
  person lays it on top as a layer and never paints on it.
- `.guide.txt`: the number, colour, and name of each region ("Left lower
  arm"), then every piece with its label ("Left lower arm, front"), pixel
  bounds, and meshes. Use it to answer "where on the texture is the left
  forearm?" or to point the person at a piece. `--json` on `export` returns
  the paths, piece count, and region names.

Regions come from the mesh: pieces are found from the texture coordinates,
and each is named after the bone with the most skin weight over it, or its
mesh when there is no skeleton. A piece's facing (front, back, left, right,
top, underside) is in the model's own frame, so "left" is the figure's left.

`import` refuses a PNG of a different size from the texture and writes the
copy with only that image replaced; meshes, normals, tangents, skins,
animations and the other images keep their bytes. `--from <png>` imports a
file from elsewhere. Without `--no-open`, `export` opens the texture in
`PIXELKILN_EDITOR` or the OS default, which an agent should not do unless
asked.

Do not paint the texture yourself unless the person asks for a specific,
checkable change. Hand fixes (streaks, pinholes, seams) are judgement calls
the person makes looking at the model. The gallery is better for that: its
editor shows the guide with names written in (on a layer of its own with a
protocol 5 editor build, which `pixelkiln tools status` reports) and the 3D
model beside the canvas, updating as they paint. Suggest
`pixelkiln gallery --edit` and leave `--edit` to them.

## Blender

```bash
pixelkiln model blender knight
# the person paints in Texture Paint, then File > Export > PixelKiln edit (.glb)
pixelkiln model adopt knight                 # changed base colour textures only
pixelkiln model adopt knight --mode whole    # the exported file as the edit
```

`blender` starts the person's Blender on the edited copy (or the model as
built) with an export item that writes `knight.export.glb`. It finds Blender
through `PIXELKILN_BLENDER`, then the usual install location; it never
installs it. It opens a window, so run it only when the person asks.

`adopt` defaults to `textures`: the base colour textures and normal maps that
changed in the export are matched to the model by material name and put into a copy of the
model as built. Blender re-encodes meshes and animations on export, so this
keeps them exactly as built. Use `--mode whole` only when the person changed
more than paint (geometry, weights, animation). `--from <glb>` adopts a file
from elsewhere. An export whose material names no longer match is refused;
`whole` is the way to take it.

## Normal maps

Normal maps are exported, imported, painted in the gallery, and adopted from
Blender the same way, recorded as `<material> normal map`. They are glTF
tangent-space maps in the OpenGL convention: `#8080ff` is flat, red leans the
surface right, green up. Painting one by hand is for repairs (flattening a
streak, filling a pinhole, softening a seam), judged in the gallery's 3D view
beside the editor, never for adding relief from scratch. Do not paint one
yourself.

## Normal map detail from PixelLab (spends generations)

```bash
pixelkiln model normal-map knight --dry-run                 # what it would send, and the price
pixelkiln model normal-map knight --yes --budget 0.5        # four views of the figure, 0.4 generation
pixelkiln model normal-map knight --source texture --image Cuirass --yes --budget 0.2
pixelkiln model normal-map knight --blend 2                 # again, stronger: answers are cached, free
```

This is the one model command that costs money. Run it only when the person
asked for normal map detail, show them the `--dry-run` price first, and pass
`--budget` at that price with `--yes`. Spending is never implied by "fix the
model".

It reads the painted light and dark as small bumps (PixelLab's surface
detail, with outline rounding and part shapes held at 0, since the mesh has
its shape already) and blends them onto the normal maps the model has, so the
baked relief stays. It writes the edited copy, recorded per map as
`pixellab normal-map (<source>)`.

Which source:

- `views` (default): the whole figure drawn from four sides (`--views` for
  others, up to eight; 0.1 generation each in lite mode), each picture's
  normals carried back onto every texture through the surface. Consistent
  across seams, coarser, and parts no view sees stay as they were. Best for a
  first pass on a character: one price covers every texture.
- `texture`: each normal map's base colour texture as laid out, in tiles of at
  most 512 px (a 1024 texture is four calls). Finer and complete, but
  neighbouring unwrap pieces are read separately and can leave a line along a
  seam. Use it for one material with fine engraving, by `--image`.
- `sprites`: the figure's own sprites, from `<model>.sprites/` (one
  `<direction>.png` each) or `--sprites`. Each is lined up with the model by
  matching colours, and only matching pixels are used. Run `--dry-run` first
  and read the per-sprite "lines up in colour" figures and notes, and look at
  `sprite-<direction>.fit.png`. Below about 50% the detail is patchy; low
  resolution sprites (80 px) give soft detail. It suits a model built to the
  sprites' proportions; on a mesh that was filled out differently (a chibi
  sprite, an adult mesh) prefer `views`, and say why. `--pose <animation>[@s]`
  poses the model to match sprites drawn in another stance.

What to expect: in testing on a knight, both added relief to gold trim and
embossing and little to plain cloth or fur; at `--blend 1` the change is
subtle. `--blend` (0–2) and `--replace` re-run from the cache at no cost, so
tune with those rather than by asking again. Runs re-tune, they do not stack:
each blends onto the map from before the first PixelLab run, and `--blend 0`
takes the detail off. The pictures sent, PixelLab's
answers, and `image-<n>.detail.png` (the detail alone) are in
`edits/models/<name>.normal-map/<source>/`; look at the detail picture and the
gallery's 3D view before calling it done.

In the gallery the same thing is **Normal map detail (PixelLab)** in the
model's drawer. It works only when the person started the gallery with
`--edit --budget <n>`; leave starting it that way to them.

## Not covered

Metallic-roughness, occlusion, and emissive images are listed but not offered
for painting. `normal-map` adds detail to a normal map the model has; it does
not add one to a material without one. There is no way to
declare the edited copy in the manifest (`resolve` is how a consumer finds it), and no step builds or regenerates a
model.
