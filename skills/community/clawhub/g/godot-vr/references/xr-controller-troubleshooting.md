# XR controller troubleshooting (Godot 4 / OpenXR, visor-side)

Use when the scene runs and the head tracks (you can look around) but the
**controllers don't show and you can't interact** in the headset. This is the
hard part of Godot VR: the head always works, so a clean headless run proves
nothing about controllers. You can't see the visor; you must infer state from
logs.

## The one decisive diagnostic

Add a per-frame log per `XRController3D`: its `global_position` and
`get_tracker_hand()`. Also query the OpenXR interface
(`XRServer.find_interface("OpenXR")`) and the hand trackers. Then judge which case
you're in — do this BEFORE changing anything, so you know which side to touch.
Dump the interface's `get_signal_list()` / `get_method_list()` first (4.7.2's
`OpenXRInterface` surface differs from older docs — see `references/godot-47-api.md`),
because some older checks do not exist in 4.7.2.

**When the logs run out — read the exact-version engine source, not the stable docs.**
Binding internals (tracker names, which profiles a runtime accepts, how an
`XRController3D` resolves its source) are not in the docs. Pull the version-matched
source and read the real function: `…/modules/openxr/openxr_interface.cpp`
(`find_tracker` = the registered tracker names; `_load_action_map` = which action-map
`.tres` loads, from project setting `xr/openxr/default_action_map`),
`…/scene/3d/xr/xr_nodes.cpp` (`XRNode3D::_bind_tracker` = exact-name match, no
auto-detect), all under
`https://raw.githubusercontent.com/godotengine/godot/<version-tag>/`. For the *runtime*
side, pull the runtime's own source (e.g. `mbucchia/Pimax-OpenXR` `action.cpp` /
`mappings.cpp`) to see exactly which interaction profiles and component paths it
validates — that is where an `XR_ERROR_PATH_UNSUPPORTED` rejection is decided.

- **Frozen position + `hand=0`** (pos stuck at whatever you set in code, every frame)
  → the node is NOT receiving a pose from the runtime. Not a visual/material bug.
- **`get_view_count()`** on the OpenXR interface (2 = stereo head is fine) — confirms
  the *head* path works even when the *controller* path is dead.
- **`is_hand_tracking_supported()` / `is_hand_interaction_supported()`** (bool) →
  whether the runtime exposes hand-tracking at all.
- **`XRServer.get_tracker("/user/hand_tracker/left")`** and `…/right` → if null, the
  runtime is NOT exposing hand-tracking; if non-null with `has_tracking_data == true`,
  it's exposing **optical hand-tracking**, not controllers.
- ⚠️ 4.7.2 `OpenXRInterface` has **no** `controller_connected` /
  `controller_disconnected` signals and **no** `get_active_interaction_profile()` —
  don't write code that connects the former or calls the latter (both runtime-error).

## The 3 cases (the diagnostic routes you)
| Case | Diagnostic signature | Where the fix lives |
|---|---|---|
| A — binding | session sees the controller (model/profile loads) but node pos stays frozen / `hand=0` | Godot action map / node linkage (code) |
| B — not exposed | no controllers, no hand tracker, `hand=0`, frozen pose, but `get_view_count()=2` | the **runtime** isn't handing controllers to the OpenXR session (runtime-side) |
| C — hand tracking | hand tracker present + `has_tracking_data` | runtime doing hand-tracking; switch code to hand-tracking, or disable hand-tracking in the runtime |

## Case A in detail — the two sub-fixes (runtime is correct, still `hand=0`)

On Pimax Crystal this is the common trap: after you've done the PimaxXR runtime fix
(case B), the PimaxXR log shows both controllers detected and mapped to
`/interaction_profiles/oculus/touch_controller` with **zero errors**, yet Godot still
reports `hand=0` / frozen `track pos` / invisible hands. That means the runtime is
fine and **case A** is what's left. Case A has **two independent sub-fixes** — both are
required; doing only one still leaves `hand=0`.

1. **Node binding — set `XRController3D.tracker` explicitly.** Godot 4.7 `XRController3D`
   binds via `xr_server->get_tracker(tracker_name)` with an **exact string match and no
   auto-detect**. `OpenXRInterface::find_tracker()` registers the two controller trackers
   under the names `"left_hand"` / `"right_hand"` (NOT the OpenXR path `/user/hand/left`,
   NOT the hand-tracker path `/user/hand_tracker/left`). So the code must do
   `controller.tracker = "left_hand"` (and `"right_hand"`). An **empty** `tracker` →
   `get_tracker("")` → null → the node never receives a pose → `get_has_tracking_data()`
   stays false, `hand=0`, frozen position. Also use `pose = "grip"` (not `"default"`).
   Verify with a one-time print of `tracker` + `pose` in `_ready` and the
   `hand=1`/`hand=2` + `tracking=true` line once the session starts.

2. **Action map — trim to the profiles the runtime recognizes.** Godot's stock
   `openxr_action_map.tres` ships **four** interaction profiles (generic, oculus, pico4,
   hand) plus an OpenXR 1.1 `grip_surface/pose` palm-pose path. The runtime validates
   *every* suggested profile, and a single unsupported path fails the whole
   `xrSuggestInteractionProfileBindings` call with `XR_ERROR_PATH_UNSUPPORTED` — so **no**
   controller binds, and you may not even see the error in the Godot Output (check the
   runtime's own log, e.g. PimaxXR's). For PimaxXR + Crystal (which only accepts
   `oculus/touch_controller`): edit `openxr_action_map.tres` so `interaction_profiles` is
   `[<the oculus profile SubResource>]` only, delete the other three profile sub-resources
   and **all** `grip_surface/pose` bindings (keep the oculus profile's remaining ~34
   bindings), then pin it in `project.godot`: `openxr/default_action_map="res://openxr_action_map.tres"`
   (the engine default already resolves to that path, but the pin is explicit and survives
   editor rewrites). Confirm your grab code's action names (`trigger`, `grip`,
   `trigger_click`, `grip_click`, `primary_click`, …) are all present in the surviving
   oculus profile.

**Order of attack:** runtime (case B) first, then **both** case A sub-fixes, then re-test
in the visor. The success signature: PimaxXR log shows `Using interaction profile:
/interaction_profiles/oculus/touch_controller` for both hands, Godot shows
`hand=1`/`hand=2` + `tracking=true` with `track pos` moving, and grab/throw responds.

## OpenXR runtime selection on Windows (confirmed mechanics)
- Active runtime = `HKLM\SOFTWARE\Khronos\OpenXR\1\ActiveRuntime` (REG_SZ = full path to
  the runtime's manifest `.json`). All installed = `…\1\AvailableRuntimes` (DWORD per
  manifest path). Read with `reg query`.
- **`XR_RUNTIME_JSON` env var (user OR machine) overrides the registry** — the loader
  checks it first. Check both (`reg query HKCU\Environment` and the SYSTEM
  `…\Session Manager\Environment` key) before assuming the registry governs.
- **Godot reads the runtime only at startup.** After switching, FULLY restart the
  editor (a running editor keeps the old session); a fresh `F5` game process re-reads it.
- **Verify which runtime Godot actually uses** via the Output line
  `OpenXR: Running on OpenXR runtime: …` — do not assume the switch took.
- Switch via the runtime's own UI (SteamVR → Developer → "Set SteamVR as OpenXR Runtime";
  **PimaxXR → PimaxXR Control Center**; the Pimax client's runtime selector) or by
  setting the registry value directly.

## Pimax Crystal / Crystal Super (inside-out) controllers
- Pimax Crystal is **inside-out** (no base stations); the headset tracks the
  controllers and the Pimax runtime owns that data. Crystal controllers report as
  **Oculus Touch** (Godot's default action map includes `oculus_touch` and the
  `generic_controller` fallback).
- **Runtime choice is NOT the fix for Pimax Crystal — the binding layer (case A,
  detailed above) is.** Verified in-visor on the same project: **both** Pimax
  OpenXR **0.1.0** (Pimax Play's built-in runtime) and PimaxXR (Unofficial)
  **0.4.4** (mbucchia/Pimax-OpenXR) work once the action map is trimmed and the
  trackers are set explicitly. The early "no hands" on PiOpenXR/SteamVR predated
  the case A fix, so the later runtime switch to PimaxXR was coincidental, not
  causal. SteamVR was never re-tested after the fix — still unverified (it may
  still not expose the Crystal controllers to the app's session).
- **Signature of case B on Pimax (confirmed):** head tracks (`get_view_count() = 2`),
  controllers visible in the runtime dashboard, but the app gets none:
  `is_hand_tracking_supported = false`, both `/user/hand_tracker/{left,right}` →
  `NO tracker`, `track pos` frozen, `hand=0`. ⚠️ On Pimax Crystal a **broken case A
  looks exactly like this too** — apply the case A fixes (trimmed action map +
  explicit trackers) before blaming the runtime: with those in place, **both** Pimax
  runtimes (built-in Pimax OpenXR 0.1.0 and PimaxXR 0.4.4) work in-visor.

### Optional — the PimaxXR (Unofficial) runtime
PimaxXR (mbucchia/Pimax-OpenXR) is a standalone **unofficial** third-party runtime
that **also** works with the Crystal (verified in-visor, alongside Pimax Play's
built-in Pimax OpenXR 0.1.0). It is **not required** once case A is fixed — the
built-in first-party runtime is the simpler default; keep PimaxXR as a fallback if
the built-in one ever regresses. Note: upstream marks the project **abandoned** — superseded by Pimax's own implementation in Pimax Play (last release 0.4.4, 2023); treat it as a legacy fallback only. If you do install it, it ships a **PimaxXR Control
Center** (Start Menu / desktop) used to toggle between PimaxXR and SteamVR:
1. Install the current release MSI (e.g. `PimaxXR-0.4.4.msi`) from
   `github.com/mbucchia/Pimax-OpenXR/releases`. Verify it (~3.4 MB, author
   `mbucchia@gmail.com`).
2. **PimaxXR Control Center** → set the active OpenXR runtime to **PimaxXR**.
3. Keep **Pimax Play** running (PimaxXR reads headset+controller tracking from it);
   quit SteamVR (no longer the runtime).
4. Fully restart Godot. The Output line should read
   `Running on OpenXR runtime: PimaxXR` (was `SteamVR/OpenXR …`), and the diagnostic
   should flip: hands `TRACKING`, `track pos` moving, `hand=1`/`2`.

**Enablers (do these too, but they are NOT the fix — recentering + non-Index
emulation alone did not work under SteamVR):** Pimax Play controller emulation =
**not Index** (Oculus Touch); recenter both Pimax Play and the runtime.

**Grip button may be dead** — a documented Pimax Crystal firmware bug in some apps.
Bind primary grab to the **trigger** (grip as fallback); grip non-response is
expected, not a code bug.

If PimaxXR is unavailable, secondary candidates (not independently validated):
SteamVR version rollback, or disabling a conflicting hand-tracking / Leap Motion
layer. But PimaxXR is the Pimax-blessed path — try it first.

## Benign noise (do not chase)
- `Object picking can't be used when stereo rendering` (`_process_picking`) — a one-time
  `WARN_PRINT_ONCE`; the viewport's built-in *mouse* object-picking is disabled under
  stereo. It does **not** affect controller raycast grabbing. Ignore it.
