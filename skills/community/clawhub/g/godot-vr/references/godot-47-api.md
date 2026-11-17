# Godot 4.7.2 API forms that work (verified at runtime)

Exact names/shapes confirmed against a running 4.7.2 build. The "obvious" 3.x-era
form appears only as the thing that FAILS — use the stated form.

## Environment (glow = bloom) + fog
- `glow_enabled`, `glow_intensity`, `glow_bloom`, `glow_hdr_threshold` (~0.9); blend `Environment.GLOW_BLEND_MODE_ADDITIVE`; tonemap `Environment.TONE_MAPPER_ACES`; overall brightness via `tonemap_exposure`.
- Fog: `fog_enabled`, `fog_density`, `fog_light_color`.
- HDR emission on a `StandardMaterial3D`: `emission_enabled=true`, `emission` (Color), `emission_energy_multiplier > 1.0` (2.5–4.0 for strong bloom). There is **no** `SHADING_MODE_GLOW` / `TRANSPARENCY_ADD` in 4.7 — do not reach for them.

## GPUParticles3D
- `draw_pass_1` / `draw_pass_2` take a **Mesh**, not a Material: build a `SphereMesh`, set its `.material`, then assign the mesh to `draw_pass_1`. (Assigning a bare `Material` is a type error.)
- `emission_shape` + `emission_shape_scale`; `process_material` is a `ParticleProcessMaterial`.

## Physics / RigidBody3D
- Damping is `linear_damp` and `angular_damp` (NOT `_damping`); `gravity_scale`; velocity is `linear_velocity` (NOT `velocity`).
- World raycast: `direct_space_state` is a **property** on `World3D` (not a method) → `get_world_3d().direct_space_state.intersect_ray(PhysicsRayQueryParameters3D.create(from, to))`. `intersect_ray` takes the single `PhysicsRayQueryParameters3D`, not two `Vector3`s.
- `RayCast3D` node: `target_position`, `enabled`, `collision_mask`; `is_colliding()`, `get_collider()`, `force_raycast_update()`.

## RandomNumberGenerator
- Has `randf()`, `randf_range()`, `randi_range()`, `seed`. **No `.pick()`** — pick manually: `arr[rng.randi_range(0, arr.size()-1)]`.

## Audio
- Use `AudioStreamPlayer3D` (NOT `SoundPlayer3D`). Build `AudioStreamWAV` in code for procedural chimes.

## XR
### Session state (OpenXR interface from `XRServer.find_interface("OpenXR")`)
- `get_session_state()` (enum), `is_initialized()`, signals `session_begun` / `session_stopping`. **No `is_session_started()`.** Drive a `_xr_active` bool from the two signals.

### OpenXRInterface diagnostic surface (4.7.2 — dump before coding)
- **No** `controller_connected` / `controller_disconnected` signals, and **no**
  `get_active_interaction_profile()` method — do not connect the former or call the
  latter (both runtime-error in 4.7.2). Real signals include `session_begun`,
  `session_stopping`, `session_focussed`, `session_visible`, `play_area_changed`,
  `pose_recentered`, `user_presence_changed`.
- Hand-tracking queries (no-arg): `is_hand_tracking_supported()`,
  `is_hand_interaction_supported()`, `get_view_count()`; plus `get_hand_joint_*()`
  (position/rotation/radius/flags/linear+angular velocity). `get_hand_tracking_source()`
  takes **1 argument** (hand side) — calling it with no args errors.
- **Dumping the interface:** iterate `get_signal_list()` / `get_method_list()` and read
  each entry's `"name"` — in 4.7.2 that value is a **`String`**, so convert with
  `str(x)`, NOT `x.string()` (`.string()` on a String errors: "Nonexistent function
  'string' in base 'String'").

### XRController3D
- Props: `tracker` (String), `pose` (String: use `"grip"` or `"aim"`), `show_when_tracked` (bool).
- ⚠️ **No auto-detect: an empty `tracker` never binds** (`get_tracker("")` → null → frozen pose, invisible hands). Set `tracker="left_hand"`/`"right_hand"` explicitly — verified in-visor on Pimax Crystal on both Pimax runtimes (plus the trimmed action map; see `references/xr-controller-troubleshooting.md`). `pose="default"` is **unreliably bound** → controllers silently stop tracking — never use it.
- Methods: `is_button_pressed()`, `get_input()`, `get_float()`, `get_vector2()`, `get_tracker_hand()` (returns unknown/0 when the node isn't linked to a tracked controller).
- **No** `tracking` prop, **no** `TrackingType` enum, **no** `get_supported_controls()`.

### Scene structure
```
Main (root, main.gd)
└─ XROrigin3D            # XR root
   ├─ XRCamera3D         # extends Camera3D
   ├─ XRController3D "LeftHand"   (tracker="left_hand", pose="grip", show_when_tracked=true)
   └─ XRController3D "RightHand"  (tracker="right_hand", pose="grip", show_when_tracked=true)
```

## Spatial shaders (procedural materials, 4.7)
Written against the 4.7 spatial-shader reference + compile errors that actually fired:
- **`shader_type spatial;` must be the first line of the code string.** If it is missing Godot renders the material as a no-op default white — **no error, no warning in the log**. The only reliable detector is a pixel sample (build a tiny rig that prints `get_viewport().get_texture().get_image().get_pixel(x, y)` for a known-albedo sphere).
- Fragment built-ins in 4.7: `VIEW` (NOT `V`), `NORMAL` (view-space), `VERTEX` (**view space** in the fragment stage — model+view already applied; **object space** only in the vertex stage). 4.7 has **NO `WORLD_MATRIX`** (`SHADER ERROR: Unknown identifier`) — `MODEL_MATRIX` is the model→world uniform, but it applies to *object-space* positions only. True world coords for noise, two verified forms (either makes the pattern sit still when the head moves — verified in-visor):
  - the documented recipe, in the fragment: `vec3 wp = (INV_VIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;` (inverse-view × view-space = world) — or
  - a varying: `varying vec3 v_local;` + `v_local = VERTEX;` in `vertex()` (where `VERTEX` IS object space), then `vec3 wp = (MODEL_MATRIX * vec4(v_local, 1.0)).xyz;` in the fragment.
  **WRONG:** `MODEL_MATRIX * VERTEX` in the fragment — it multiplies the model matrix into a VIEW-space position; the noise pattern crawls/rotates as the head moves, synchronized across every object sharing the shader. Also wrong: sampling raw `VERTEX` straight into `_fbm3(VERTEX * k)` in the fragment — `VERTEX` there is view space, same crawl.
- **Not in 4.7** (compile error or type error): `SHEEN`, `SHEEN_TINT`, `IRIDESCENCE`, `IRIDESCENCE_IOR`, `SSS_RADIUS`, `AOMAP`, `CLEARCOAT_GLOSS`, and the function `saturate()`.
- Working forms: `AO` (out float) for ambient occlusion; `CLEARCOAT_ROUGHNESS` (out float, 0=mirror — the inverse of the old gloss); `RIM_TINT` is an **out float** (0=white rim, 1=albedo rim), not vec3; `clamp(x, 0.0, 1.0)` instead of `saturate(x)`.
- SSS: `SSS_STRENGTH` alone does little — pair with `SSS_TRANSMITTANCE_COLOR` (**vec4**) + `SSS_TRANSMITTANCE_DEPTH`. `BACKLIGHT` (inout vec3) is the documented cheap-SSS approximation (nice on foliage).
- Iridescence: no built-in — manual thin-film: `vec3 irid = 0.5 + 0.5 * cos(TAU * (fres * 1.8 + vec3(0.0, 0.33, 0.67)) + seed);` mixed into ALBEDO/EMISSION by fresnel.
- Shader compile failures print `SHADER ERROR: …` + `ERROR: Shader compilation failed` but the scene keeps running with white fallback materials — grep for `SHADER ERROR` in every GPU run, not just `SCRIPT ERROR`.

## ArrayMesh (imported GLB meshes)
- `surface_get_arrays(s)` returns an **Array** with one entry per array type — `.size()` is the number of array types (13), **not** a byte count. Vertex count: `surface_get_arrays(i)[ArrayMesh.ARRAY_VERTEX].size() / 12`.
- `surface_get_array(s, type)` does **not** exist in 4.7 (runtime "Nonexistent function") — the plural form above is the only per-surface accessor.

## Reflection (ReflectionProbe, 4.7.2)
- A realtime `ReflectionProbe` can give TRUE geometry reflections on a small glossy surface in a dark scene (screen-space reflections on the same scene produced no visible scene reflection there; only light specular highlights showed). Place it just above the reflective surface — it only mirrors content ABOVE its own height — with `max_distance` ≥ scene radius; all materials pick it up automatically, so only the glossy surface shows the effect. Limit: a pool with objects at/inside the rim (mushrooms, rocks) needs the geometric mirror-twin recipe instead (see `references/style-swap-system.md`) — the cubemap never shows rim objects whose reflection would land outside the pool, and the partial result is easy to misread as "glow reflects but geometry doesn't".
- **No `cube_map_size` or `decay` in 4.7.2** (Godot 3-era names) — assigning either throws "Invalid assignment of property or key", and a GDScript runtime error **aborts the rest of the enclosing function** (code after the failing line — including `add_child` — never runs). Valid properties (verified by `get_property_list()`): `update_mode, intensity, blend_distance, max_distance, size, origin_offset, box_projection, interior, enable_shadows, cull_mask, reflection_mask, mesh_lod_threshold, ambient_mode, ambient_color, ambient_color_energy`. There is also no `cubemap` property in 4.7 — the captured texture is not exposed to script.
- Enumerating unknown node APIs: a standalone `-s` SceneTree script printing `get_property_list()` / `get_method_list()` (pass the script a native `C:/...` path — MSYS `/tmp/...` fails with "File not found").
- **Mirror-material PBR pitfall:** with `metallic = 1.0` the reflected image is multiplied by the albedo — a near-black "deep water" albedo blacked out every non-emissive reflection (only emissive objects survived). Use a BRIGHT albedo for a tinted mirror (e.g. `Color(0.30, 0.65, 0.70)` for cyan water); roughness ~0.05–0.1 keeps it sharp.

## Windowed screenshots on a machine with an OpenXR runtime installed
The runtime (e.g. Pimax) can initialize even with no headset on; then Godot logs `OpenXR: No viewport was marked with use_xr, there is no rendered output!` every frame and the **window stops rendering — the screenshot is a solid background color**. Fix: add `--xr-mode off` to the run (`--xr-mode` takes `default|off|on`; the Vulkan backend cannot init/uninit OpenXR at runtime, so it must be a startup flag). Also verify process hygiene after every non-headless run: the command must finish on its own (`RUN_DONE` marker in the log) and `tasklist | grep -ic godot` must be 0 — a windowed Godot left open blocks the user's machine.

## Error → fix table (fired during the real build)
| Symptom | Cause | Fix |
|---|---|---|
| parse error assigning to `draw_pass_1` | assigned a `Material` | assign a `Mesh` with `.material` set |
| `is_session_started()` not found | wrong method | `get_session_state()` enum + `session_begun`/`session_stopping` signals |
| `.pick()` not found | no such method | `arr[rng.randi_range(0, arr.size()-1)]` |
| `direct_space_state()` / 2-Vector3 `intersect_ray` | wrong shape | property + `PhysicsRayQueryParameters3D.create(a,b)` |
| `get_supported_controls()` not found | no such method | drop it; log `tracker` instead |
| connecting `controller_connected` / calling `get_active_interaction_profile()` | don't exist in 4.7.2 `OpenXRInterface` | use `is_hand_tracking_supported()` / `get_view_count()` / `XRServer.get_tracker()` instead |
| `.string()` on a `String` ("Nonexistent function 'string'") | list entries' `name` is a String in 4.7.2 | `str(x)` |
| `surface_get_array(s, type)` not found | no such method in 4.7 | `surface_get_arrays(s)[ArrayMesh.ARRAY_VERTEX]` (Array, not bytes) |
| "Invalid assignment of property or key 'cube_map_size'" (or 'decay') on a ReflectionProbe | Godot 3-era names; also aborts the rest of the enclosing function | 4.7.2 ReflectionProbe properties (see Reflection section) |
| `EMISSION_SHAPE_*` / `_damping` / `velocity` names | 3.x-era names | 4.7 names above |
| `SHADER ERROR: Unknown identifier 'WORLD_MATRIX'` | no such spatial-shader uniform in 4.7 | world in the fragment: `INV_VIEW_MATRIX * VERTEX` (documented recipe) or `MODEL_MATRIX * v_local` from a varying (see Spatial shaders) |

## Verification commands (point `GODOT` at your console exe)
```bash
GODOT="C:/path/to/Godot_v4.7.x-stable_win64_console.exe"
# import
"$GODOT" --headless --import --path "C:/path/to/<proj>" > imp.log 2>&1
# run (OpenXR OFF for verification) — expect a startup self-test print
"$GODOT" --headless --path "C:/path/to/<proj>" > run.log 2>&1
# screenshot (NON-headless, marker arg the scene looks for) → saves PNG, quits
timeout 120 "$GODOT" --path "C:/path/to/<proj>" --preview > prev.log 2>&1
# check
grep -c "SCRIPT ERROR" run.log
grep -iE "SCRIPT ERROR|Parse Error|Failed to load" run.log | sort | uniq -c
```
