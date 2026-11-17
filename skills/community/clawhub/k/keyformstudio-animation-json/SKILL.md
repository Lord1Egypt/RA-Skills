---
name: keyformstudio-animation-json
version: 1.3.0
description: Generate and validate VASF JSON animations for import into Keyform Studio. Use when asked to create an animation JSON, a "vasf" file, a Keyform Studio animation, or to fix a JSON rejected by the importer.
license: MIT
homepage: https://github.com/Xiaohequ/keyformstudio-animation-json
---

# Generate VASF animation JSON

Produce ONE JSON file describing a 2D animation. The user imports it into
**Keyform Studio** (home ▸ "Import a JSON file" creates a new project; Studio ▸
Shapes ▸ "Import a VASF as instance…" inserts a skeleton into the current
project). The importer is strict and reports every problem in French with its
path.

`references/vasf-example.json` is a complete, importable animation that
exercises every feature below — copy its patterns.

## Top level

```json
{
  "version": 6,
  "name": "My animation",
  "canvas": {"width": 720, "height": 1280, "fps": 25, "background": "#14161C"},
  "theme": {"peau": "#FFE3C2"},
  "defs": {"main": {"type": "circle", "width": 56, "height": 56}},
  "groups": [{"name": "Head"}],
  "shapes": [ ... ],
  "skeleton": { ... }
}
```

| field | default | notes |
|---|---|---|
| version | required | `1`–`6`; use the highest extension you need |
| name | "Animation importée" | project name |
| canvas.width / height | 720 / 1280 | 16…4096 |
| canvas.fps | 25 | 5…60 |
| canvas.background | `#14161C` | scene background, or `"$alias"` |
| theme | — | v2 color palette: `{"alias": "#RRGGBB"}` |
| defs | — | v2 reusable primitive definitions |
| groups | — | v6 element groups |
| shapes | required, ≥ 1 | draw order = array order (first = background) |
| skeleton | — | presence switches the project to skeleton type |

Coordinates: origin top-left, x → right, y → **down**, positive degrees =
clockwise. Time in **seconds**, angles in **degrees**, colors `#RRGGBB` /
`#AARRGGBB`.

## Shape

```json
{
  "name": "Bloc", "type": "rect", "color": "#FF5C5C",
  "filled": true, "strokeWidth": 4, "width": 110, "height": 110,
  "start": 0, "end": 2, "x": 180, "y": 320,
  "rotation": 0, "scale": 1, "opacity": 1,
  "keyframes": [ ... ]
}
```

| field | default | notes |
|---|---|---|
| name | "Forme" | unique; duplicates are auto-renamed "X 2" |
| type | "rect" | `rect, circle, line, path, triangle, star, hexagon, cross, heart, arrow` |
| color | `#5B8DEF` | fill/stroke color |
| filled | true | `false` = outline only |
| strokeWidth | 4 | outline thickness (used when `filled=false`, always for `line`) |
| width / height | 110 | primitive size; ignored for `path` (derived from points) |
| points | — | `path` only: `[x, y]` pairs **around the shape center**, ≥ 2, auto-closed |
| start / end | 0 / latest other end, else 4 | visibility window in seconds; `end` > `start` |
| x / y | canvas center | base position of the shape center |
| rotation | 0 | base rotation, degrees |
| scale | 1 | base scale (0.05–4 recommended) |
| scaleX / scaleY | 1 | v2 axis factors — effective scale = `scale` × factor |
| pivot | `[0, 0]` | v2 `[dx, dy]` offset from the shape center, in shape units; rotation and scale turn around it (STATIC) |
| opacity | 1 | 0–1 |
| layers | — | v2 array of primitives (overrides the flat geometry fields) |
| cornerRadius | absent = auto | v5 explicit rectangle radius; `0` = square corners |
| roundTopLeft / roundTopRight / roundBottomRight / roundBottomLeft | true | v5 per-corner switches |
| ref | — | v2 name of a `defs` entry used as geometry defaults |
| bone | — | whole-shape binding shortcut (same as one `bind` entry) |
| cycle | — | v2 `{"repeat": N}` repeats the keyframe pattern |
| keyframes | — | see below |

### Shape keyframe

```json
{"t": 0, "x": 180, "y": 320, "rotation": 0, "scale": 1, "opacity": 1,
 "strokeWidth": 1, "easing": "easeInOut"}
```

- `t` seconds ≥ 0, sorted automatically; a keyframe past `end` extends it.
- `easing` = curve of the segment ARRIVING at this keyframe: `linear`,
  `easeIn`, `easeOut`, `easeInOut` (default), `step`, or a CSS chain
  `"cubic-bezier(x1, y1, x2, y2)"`.
- Any of `x, y, rotation, scale, opacity, strokeWidth` may be omitted and is
  carried from the previous keyframe (or the base pose). v2 adds `scaleX` /
  `scaleY`. `strokeWidth` here animates the stroke **factor** (visible stroke =
  `strokeWidth` × factor).
- Keyframes are poses: each property interpolates independently.

## Skeleton

```json
{
  "name": "Rat",
  "bones": [
    {"name": "Bras", "joint": [100, 320], "angle": 0, "length": 100},
    {"name": "Avant-bras", "parent": "Bras", "joint": [200, 420],
     "angle": 90, "length": 80, "z": 0, "ik": false, "bend": 1}
  ],
  "bind": {"Bloc": "Bras"},
  "keyframes": [
    {"bone": "Bras", "t": 0.5, "angle": -30, "easing": "easeInOut",
     "opacity": 0.5, "stretch": 1.2, "squash": 1}
  ]
}
```

| field | default | notes |
|---|---|---|
| name | "Squelette" | rig name |
| bones | required, ≥ 1 | **parents must be listed before their children** |
| bone.name | required | unique |
| bone.joint | required `[x, y]` | joint position in **world canvas coords**, at rest |
| bone.angle | 0 | **world** rest angle, degrees |
| bone.length | 80 | bone length, > 0 |
| bone.parent | none | parent bone NAME |
| bone.z | 0 | draw order of the pieces carried by this bone (−10…10) |
| bone.ik | false | IK chain ROOT: dragging the chain end solves every bone (2 bones = exact solver, more = CCD); the chain follows unique-child bones only |
| bone.bend | 1 | elbow side for 2-bone IK: +1 or −1 |
| bind | — | map **shape name → bone name**, or `"Shape/Layer" → bone` |
| cycle | — | v2 `{"repeat": N}` repeats ALL bone keyframes |
| keyframes | — | bone animation; may instead be embedded in each bone object |

### Bone keyframe

```json
{"bone": "Bras", "t": 0.5, "angle": -30, "easing": "easeInOut",
 "opacity": 0.5, "stretch": 1.2, "squash": 1, "move": [10, -5]}
```

- `bone` and `t` are required.
- `angle` = **absolute WORLD angle in degrees**, NOT a delta. A child whose
  world rest angle is 90° given `angle: 30` rotates −60°.
- `opacity` (0–1), `stretch` (along the bone, 1 = neutral), `squash`
  (perpendicular, 1 = neutral) are optional.
- `move` = `[dx, dy]` **world translation** of the joint from its rest
  position; children and bound pieces follow rigidly. Combines with `angle`.
- Bone keyframes do NOT carry: an omitted `opacity`/`stretch`/`squash`/`move`
  falls back to neutral (1/1/1/[0,0]). A keyframe carrying only `t` therefore
  resets them — always give `angle` to animate a bone.

## Format versions

Set `version` to the highest extension you use; a `version: 1` file stays valid
and the importer accepts 1 to 6.

- **v2** — `layers[]` packs several primitives into one shape (local pose per
  layer, `x`/`y` relative to the shape center; `x/y/rotation/scale/opacity` and
  `keyframes` remain the GROUP pose). `theme` palette with `"$alias"` colors.
  `cycle: {"repeat": N}` repeats the keyframe pattern (period = last − first
  time; end on the starting pose for a clean loop). `defs` + `ref` define
  geometry once. `scaleX`/`scaleY` are axis factors — a keyframe value of 1
  REPLACES the factor, it does not restore it. `pivot` is allowed on the SHAPE
  only, NEVER inside `layers[]` (rejected; rotation would fall back to the
  center). CSS easing `cubic-bezier(x1, y1, x2, y2)` with x1/x2 in [0,1];
  linear identity is (0.333, 0.333, 0.667, 0.667), NOT (0,0,1,1).
- **v3** — animated color per keyframe: `"color": "#hex"` on a single-layer
  shape, `"colors": {"LayerName": "#hex"}` on a layered shape (the reverse is
  rejected). Point morph: `"points": [[x,y]…]` or `"layerPoints":
  {"LayerName": [[x,y]…]}`; the path interpolates point by point, a shorter
  cloud is padded by repeating its last point, and the reference frame is the
  BASE `points` list (not each keyframe's bbox, or the morph drifts) — the
  FIRST keyframe must define the starting cloud (copy the base at `t: 0`).
  Bone `move` and IK as described above.
- **v4** — `"flipH": true` / `"flipV": true` per layer (or at shape level when
  flat) mirrors the layer CONTENT around its origin; keyframes are untouched.
- **v5** — `cornerRadius` plus the four `round*` switches, flat or inside
  `layers[]`.
- **v6** — element groups: root `"groups": [{"name": "Head", "color":
  "#FF8800", "visible": true, "collapsed": false, "x": 0, "y": 0,
  "rotation": 0, "scaleX": 1, "scaleY": 1}]` plus `"groupId": "Head"` on each
  member shape. `groupId` is the group NAME, resolved after creation, so JSON
  key order is free; an unknown name is an error. A group holds no keyframes
  and no bones (its span derives from its children); `visible: false` hides all
  its shapes. Groups are flat: no nesting, one group per shape. The static
  group transform IS rendered: it wraps each shape's pose and rotates/scales
  around the group's VISUAL CENTRE (mean of its children's rest positions), not
  the canvas origin; a neutral group renders exactly like ungrouped shapes.
- Bone objects may embed their own `keyframes` and `cycle` (the `bone` field is
  then implied). A bone with its own cycle is excluded from the global
  `skeleton.cycle`, so different bones can run different periods.

## Gotchas

- Draw order = `shapes` array order. `zIndex` is REJECTED on import.
- Unknown fields are REJECTED at every level (root, canvas, shape, bone) with
  the offending path — check spellings.
- Alpha in `#AARRGGBB` is REPLACED by the computed opacity, not multiplied.
  Animate `opacity` for fades.
- Path inside `layers[]`: `points` are recentered on the layer origin — place
  the path with the layer's `x`/`y` (e.g. a smile: `y` = vertical center of its
  bbox).
- Layer local pose (`x/y/rotation/scale/opacity` in `layers[]`) is static: only
  the group pose, layer COLORS and layer POINTS animate. `pivot` is not
  animatable. `ref` works at shape level only, not inside `layers[]`.
- No nested project instances.

## Workflow

1. **Design** — pick canvas, duration, shapes and timeline. Falling → `easeIn`,
   rising/relaunch → `easeOut`, hard stop → `step`, otherwise `easeInOut`.
   Squash & stretch: `scale`, or independent `scaleX`/`scaleY` (ground impact =
   `scaleX > 1` + `scaleY < 1`). Rotation around an edge → `pivot` on the shape
   (e.g. a door: `[-width/2, 0]`).
2. **Write** the JSON to a scratch path with a descriptive name. One root
   object only.
3. **Validate** — `python3 scripts/validate_vasf.py <file>.json`. Fix every
   error; re-read warnings (auto-rename, scale/axis factors outside 0.05–4,
   oversized pivot, elastic bezier y, morph starting after t ≈ 0).
4. **Deliver** the `.json` file itself. If the app rejects it, the "Import
   impossible" dialog lists the errors with paths — fix and resend.

## Animation tips

- Bouncing ball: alternate `easeIn` (fall) / `easeOut` (rise), squash on the
  ground with `scale` over 1–2 keyframes.
- Character: shapes at rest, bones at the joints, `bind` shape → bone; animate
  with world-angle bone keyframes (elbow at rest 100° → keyframe `angle: 150`).
- IK: enable `ik` on the chain ROOT (shoulder); `bend` picks the elbow side on
  2-bone chains.
- Stay readable: few shapes, short durations (2–8 s), 2–4 keyframes per
  property.
