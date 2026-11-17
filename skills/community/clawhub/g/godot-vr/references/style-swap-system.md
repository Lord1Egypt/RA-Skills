# Runtime-swappable graphics styles (same scene, same object layout)

Pattern for adding N visual styles to a code-built scene and swapping at runtime
(controller button) while every object keeps its exact position, size, and
animation. Verified with 3 styles on a ~50-object scene: flat primitives →
higher-poly primitives with procedural ShaderMaterials → detailed
Blender-generated geometry.

## Registry (one array, typed entries)
Every style-able object registers at build time; one `_set_style(idx)` walk
applies everything (`match` on entry type, arrays indexed by `idx`):
- `{"t":"mi", "mi":MeshInstance3D, "meshes":[m0, m1, …]}` — mesh swap on the existing instance (same transform for all styles).
- `{"t":"mat", "mesh":Mesh, "mats":[…]}` — material swap only (same geometry).
- `{"t":"draw", "p":GPUParticles3D, "meshes":[…]}` — particle draw pass: the pass takes a **Mesh**, so register per-style meshes with the material set on the mesh.
- `{"t":"dual", "mi":MeshInstance3D, "alt":MeshInstance3D, "meshes":[…]}` — alternate **geometry with per-object transforms** (next section): for the alt's style, hide `mi` and show `alt`; for the others, set `mi.mesh = meshes[idx]` and swap visibility back.
Register via small helpers (`_reg_mi`, `_reg_mat`, `_reg_draw`, `_reg_dual`); keep every array the same length as the style count. Re-capture the styles you did **not** touch after any registry refactor — a registry change can silently regress them.

## Alternate geometry with per-object transforms: the hidden-twin instance
The shared instance's transform must stay identical across styles, so
per-object sizing (e.g. a canonical 3.0 m trunk scaled to each tree's height)
cannot live on the shared `MeshInstance3D`. Give each object a dedicated hidden
"alt" `MeshInstance3D` added to the **same parent**, sharing the imported/base
mesh, with its own node transform + `material_override` (overrides every
surface material — no per-mesh material surgery, no mesh duplication),
`visible=false` until its style activates.
- **Parent-hiding gotcha:** a hidden parent hides children regardless of their
  own `visible` flag. If the primary instance is hidden in the alt's style, the
  alt must be a **sibling** of the primary (copy position/rotation explicitly),
  not a child.
- **Align the alt's reference surface to the original:** compute the offset so
  the canonical geometry's top (terrain surface, water level) lands at the same
  world Y as the primitive's. A grid exported with its top at local y=0 placed
  at the origin replaces a 0.2-high cylinder that sat at y=-0.1 with its top
  at 0 — no offset needed; a cylinder-top replacement does need one.
- **Variety is cheap:** pick a random variant mesh + random Y-rotation per
  instance at build time (two rock GLBs, random `0..TAU` yaw) — one asset
  class, no cloned look.
- **Pool/water: a shallow basin, not a raised disc.** A water surface clearly
  above the ground plane (visible wall + gap underneath) reads as "a black
  disc floating in the air"; a wall flaring outward to the ground
  (`CylinderMesh` with `bottom_radius > top_radius`) reads as a cone that
  "tapers down to ground level at the edges" — the user rejects both. Correct
  shape: waterline ~2 cm **above** the ground plane (flat terrain is opaque —
  a waterline below it hides inside the terrain; 2 cm also clears Z-fighting
  against a y=0 terrain top), a **vertical** wall (equal top/bottom radii)
  running 10–15 cm below the groundline and hidden inside the terrain. Give
  every style's pool the same waterline Y. A true mirror water material (dark
  albedo, `metallic=1.0`, `roughness≈0.06`) looks like a black hole in a dark
  scene — keep a small cyan `emission` so it still reads as water.
- **Pool reflection: geometric mirror twins (user-confirmed in-visor) beat a probe for pools with rim objects.** A flat water surface only reflects content above the mirror plane — objects growing out of the pool (mushrooms, rocks) whose reflection would land outside the pool never appear in a probe cubemap or screen-space pass, while their glow survives — misread as "the glow reflects but the geometry doesn't". Recipe: a `_mirror_root` Node3D at (0, -2 cm, 0) with scale (1, -1, 1); for each in-pool object add a twin `MeshInstance3D` sharing the same mesh + material at the mirrored position below the waterline, so the object visibly continues underwater. Water: `TRANSPARENCY_ALPHA`, dark-teal albedo (≈`Color(0.05, 0.17, 0.21, 0.55)`), roughness ≈0.15 — the twin reads through the translucency (a different material model from the opaque metallic mirror in the godot-47-api notes; do not port the bright-albedo rule here). Verify from a standing eye-height close-up at ~45°, never the high overview.

## Blender side (detailed-geometry style)
Generate **canonical-sized** assets headlessly (see the `blender-headless`
skill + its 5.3 notes): one GLB per object class, fBm-displaced for organic
look, with UVs baked in (the Godot procedural shaders sample UVs). In Godot:
`preload` each GLB PackedScene once, extract the first `MeshInstance3D`'s
`Mesh` (instantiate → find the first mesh child → `get_mesh()` → free the
instance), share that Mesh across all instances of the class. Keep the
procedural ShaderMaterials **on top of** the Blender geometry via
`material_override` — geometry detail + procedural shading compose; replacing
them with plain GLB materials loses the per-instance seeded look. Ground/pool
become mesh swaps (terrain disc, rippling water), not just material swaps.
- **Bake the object transform before every export:** run
  `bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)` on
  the export target right before `export_scene.gltf`. The engine side extracts
  the *raw mesh* and ignores the node transform, so any position/rotation left
  on the Blender object drops out silently. `join` is the classic trigger: a
  joined object keeps its origin at the **first** source object's location, so
  a composite built away from the origin (a tuft cluster rooted at the first
  branch tip, an offset prism) lands misaligned in-engine — parts at the wrong
  tips or at the object origin. Bake every export target, not just the
  suspicious ones.
- **Clipping a bmesh grid to a circle leaves a stair-stepped rim.** For
  pool/water discs cut from a displaced grid, snap the boundary: project each
  boundary vertex radially onto the target radius, flatten its Z, and damp
  the ripple amplitude with a radial falloff over the outer band (e.g. from
  0.8 R to R) — otherwise the border renders jagged even at 64 segments.
- **`material_override` flattens all surfaces to one material** — where parts
  of one asset need different materials (bark branches + leaf tufts), export
  them as separate GLBs and register them as twin instances sharing the
  transform (same position/scale/yaw per tree).
- When one build step exports multiple targets, do not delete the other scene
  objects before export (a stray-cleanup loop silently kills the second
  target) — select per export with `use_selection=True`.

## Per-style environment
Meshes alone don't make a style: keep a per-style ENV table (fog density,
tonemap exposure, glow intensity + bloom, ambient energy, background color)
applied in the same `_set_style` walk. Deeper/darker styles: denser fog, lower
exposure and ambient. Check the floor is still readable in the screenshot —
"moody" and "the ground is pure black" are different things.

## Cycling input + verification
- Controller button: **edge-trigger** (`pressed_now and not pressed_prev`),
  ~0.3 s cooldown, one hand only — a level-triggered check cycles per frame
  while the button is held. A short SFX chime confirms the swap in-visor.
- The cycle wraps with `(_style + 1) % style_count`.
- Add a `--style N` boot arg that forces a style, and verify **each** style
  with the marker-arg screenshot: `timeout N <godot> --path . --xr-mode off
  `--style N --preview` → vision-check the PNG (geometry present, no
  white-out/blank, alt objects at the right heights).
- **When the screenshot can't verify an alignment** (one part occludes the
  other — e.g. canopies hiding branch tips), verify it geometrically instead:
  a headless Blender script imports both GLBs (after
  `read_factory_settings(use_empty=True)` so the startup-scene Cube doesn't
  pollute the report), clusters one asset's vertices, and prints each cluster
  center's distance to the nearest vertex of the reference asset. Deterministic
  proof — no vision judgment on hidden geometry.
