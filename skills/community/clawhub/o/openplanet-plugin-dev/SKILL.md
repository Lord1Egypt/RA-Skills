---
name: openplanet-plugin-dev
description: Create, debug, structure, and run Openplanet AngelScript plugins for Trackmania 2020 (TMNEXT) and ManiaPlanet 4 (TM2/MP4). Covers API quirks, AngelScript pitfalls, performance patterns, the launch/verify loop, MP4 API-mismatch fixes, and proven templates. Use when building, debugging, reviewing, or launching Openplanet plugins.
version: 3.0.0
metadata:
  openclaw:
    tags: [openplanet, trackmania, angelscript, plugin, game-modding]
---

# Openplanet Plugin Development

Core guide for Openplanet AngelScript plugins on **TM2020 (TMNEXT)** and
**ManiaPlanet 4 (MP4/TM2)**. Deep material lives in `references/` — load only
what the task needs (index at the bottom).

## Golden rules

1. **Verify API members against the reflection DB before writing code.**
   - **Game Nod classes** live in `<GameDir>/Openplanet4.json` under
     `ns.Game.<Class>.m[]` (entries `n`=name, `t`=type, `p`=parent). Walk it with
     the procedure in `references/static-verify-workflow.md`.
   - **Openplanet script namespaces** (`UI::`, `IO::`, `Time::`, `Json::`,
     `Math::`, `Text::`, `Net::`, `Audio::`, `Icons::`, `getExceptionInfo()`) are
     **NOT in `Openplanet4.json`**. They live in **`OpenplanetCore.json`** (same
     game dir) under `functions[]` (filter by `ns`), `classes[]`, `enums[]`.
     Extraction recipes + verified signatures: `references/openplanet-core-json.md`.
     **Before assuming a built-in exists (e.g. `IO::WriteFile`, `UI::ListBox`,
     `Time::Format(string)`), grep `OpenplanetCore.json`** — false assumptions
     here cost a full kill+relaunch recompile cycle each time.
   - MP4 game-class specifics: `references/mp4-api-verified.md` (editor) and
     `references/mp4-runtime-and-dev-memory.md` (in-race / playground).
   - **A class can appear in the DB with an EMPTY `m[]`** (e.g.
     `ns.Scene.CSceneVehicleVis` is `{"i":...,"s":3464}` with no members). That is
     not a lookup failure — it means the class has no scriptable named members and
     the only way in is raw `Dev::GetOffset*` / `Dev::SetOffset` against its byte
     size. Report that honestly instead of inventing member names.
2. **Target game matters.** TM2020 examples often DON'T compile on MP4 (missing
   UI overloads, missing members, wstring vs string). MP4 specifics:
   `references/mp4-api-verified.md`, `references/mp4-api-mismatches.md`,
   `references/mp4-supplement.md`, `references/mp4-ui-rendering.md`.
3. **Unsigned folder plugins need Developer signature mode.** Launch with
   `ManiaPlanet.exe /openplanet:developer` (or F3 → Developer → Signature Mode).
   Otherwise the log shows `Invalid file hash` + `not suitable for the current
   signature mode` and the plugin silently doesn't appear.
4. **Debug via the log, not the GUI.** Clear `Openplanet.log`, launch, wait
   ~50 s, then grep for `ERR :` / `compilation failed` / `Loaded plugin`.
   Full command recipes: `references/launch-and-verify.md`.
5. **A running game holds the compiled state.** After editing sources, kill the
   game (`taskkill /F /IM ManiaPlanet.exe`) and relaunch for a clean recompile —
   stale errors in the log mean the old build, not a failed patch.
6. **Null-safe editor access.** Route all `App.Editor` access through one
   gateway that re-checks every handle each frame; wrap each UI module in
   try/catch. Proven skeleton: `references/mapforge-architecture.md`.
7. **Cross-game (TMNEXT + MP4) plugins.** One plugin can target BOTH games via
   the predefined `TMNEXT` / `MP4` preprocessor defines (Openplanet injects them
   per-game; no `info.toml` flag needed). `CGameCtnApp` is the shared base, so
   `app.Switcher.ModuleStack`, `app.RootMap`, `app.Editor`, `app.CurrentPlayground`
   work on BOTH. Gate TMNEXT-only API (`cast<CTrackManiaMenus>`,
   `NGameLoadProgress::EState`, `app.LoadProgress`) behind `#if TMNEXT` and add an
   `#elif MP4` branch. **Keep TMNEXT and MP4 pause reasons/settings SEPARATE** —
   do NOT collapse `Pause In Menu` + `Pause While Loading` into one
   `inMenuOrLoading` check (Copilot flagged exactly this in the green-timer port:
   a combined `ModuleStack<1 || RootMap is null` with `return true` always reports
   "Loading Screen" and lets "menu" setting pause during load). Correct MP4 form:
   `bool inMenu = app.Switcher.ModuleStack.Length < 1;`
   `bool inLoading = !inMenu && app.RootMap is null;` then two separate `if`s.
   Deprecated calls to fix while porting: `nvg::LoadFont("x.ttf", true, true)` →
   `nvg::LoadFont("x.ttf")`; `Time::Format(int, bool, bool, bool)` →
   `Time::Format(uint64, bool fractions, bool forceMinutes, bool forceHours, bool short)`.
   Verified pattern, shared-member list, deprecated fixes, and the
   `nvg::LoadFont` root-path pitfall: `references/crossgame-tmnext-mp4.md`.
 8. **Never hardcode memory offsets you did not verify on THIS build.** `Dev::`
 read/write/hook is fully available on MP4, but offsets are build-specific.
 Discover them with a live correlation panel, freeze them behind a load-time
 self-check (re-read a known field and compare it to a reflected value), and
 fall back to read-only mode when the check fails — a bad `SetOffset` into a
 physics object crashes the game, not just the plugin. Procedure:
 `references/mp4-runtime-and-dev-memory.md` §6.
 9. **A plugin whose logic lives in a bundled native `.dll` is a REWRITE, not a
 port.** Unpack the `.op` (it is a ZIP) and check whether the `.as` files are
 just an `Import::GetLibrary` shell. If so, say that up front instead of
 promising a port — the offsets target a different executable and no sources
 ship in the package. Analysis recipe + verdict/brief template:
 `references/op-package-analysis-and-porting.md`.
 10. **Prefer dynamic, runtime-observed game state over static/parsed lists.**
 The user explicitly asks for this ("statyczne checkpointy → zrób dynamiczne").
 Example: bucket by the live `CurTriggerIndex` the driver actually crosses
 rather than a precomputed checkpoint table; it adapts to any map, multilap
 included. See `references/mp4-runtime-and-dev-memory.md` §7. Offer the static
 form as an explicitly-labelled *fallback* in the same module, never as the
 primary design — the user accepts "static if dynamic proves impossible", which
 is not the same as being handed static first.
 11. **In-plugin AngelScript beats any external process for reading game
 state.** When asked "can this be done in Python / .NET instead", the deciding
 fact is pointer acquisition: Openplanet hands you the live nod via `GetApp()`
 for free, so `Dev::GetOffset(nod, off)` is one line. An external Python
 `ctypes`/`pymem` or .NET process must first *find* that same object by scanning
 process memory — hours of work for something already solved. Answer with that
 comparison (a 3-row table works well), then keep Python for offline tooling:
 reflection-DB queries, code generation, Kanban seeding, and the static
 pre-flight gate. Do not accept "rewrite it in Python" as a way to avoid .NET
 when the real answer is "neither — it belongs in the plugin".
 12. **Stage delivery as Tier 1 (safe) then Tier 2 (memory writes).** Tier 1 =
 read-only reflection + teleport-style restore, ships immediately and cannot
 crash the game. Tier 2 = velocity/physics restore via `Dev::SetOffset`, gated
 behind a load-time offset self-check with automatic Tier-1 fallback. Ship and
 verify Tier 1 first; it also proves the nod chain before you build anything on
 top of it. A read-only telemetry tab is the cheapest possible proof that the
 whole context chain resolves — build it first and ask the user to confirm the
 numbers move before writing further modules.

## Project documentation convention (where knowledge lives)

For OpenPlanet plugin projects **on disk**, the user's preferred layout:

- **`IDEA.md` (project root) = project catalog only.** List *what each plugin/project
  does* (name → one-line description + module map). It is NOT a dumping ground for
  API knowledge or verified facts.
- **API knowledge → `README.md` + this skill's `references/`** (esp.
  `references/mp4-api-verified.md`). Put the verified member list, error→fix table,
  and the "no `MapForge.*` SDK / no Lua-C# / `MwFastBuffer` is a value type" facts in
  README (a summary) and in `references/`.
- Do **not** keep API facts in `IDEA.md`; keep `IDEA.md` a plain index so a future
  session finds projects fast without re-learning the API.

## Plugin skeleton (callback style)

```
MyPlugin/
├── info.toml        # metadata (see references/launch-and-verify.md §info.toml)
└── src/
    ├── Main.as      # Main(), Render(), RenderMenu(), OnDestroyed()
    ├── Core/        # context/gateway, module manager
    └── Modules/     # one feature per file
```

```angelscript
// Main.as — minimal
[Setting name="Show window"] bool S_ShowWindow = true;

void Main() { /* init; yield in loops */ }

void RenderMenu() {
    if (UI::MenuItem("\\$0f0" + Icons::Wrench + " MyPlugin", "", S_ShowWindow))
        S_ShowWindow = !S_ShowWindow;
}

void Render() {
    if (!S_ShowWindow) return;
    if (UI::Begin("MyPlugin", S_ShowWindow)) {
        // guard editor access every frame:
        auto app = cast<CGameCtnApp>(GetApp());
        auto editor = cast<CGameCtnEditorFree>(app.Editor);
        if (editor is null) UI::Text("Open the map editor.");
        else { /* modules */ }
    }
    UI::End();
}
```

`info.toml` minimum:

```toml
[meta]
name = "MyPlugin"
author = "you"
category = "Map Editing"
version = "1.0.0"

[script]
timeout = 5000
```

## Top MP4 compile-error killers (details in references/mp4-api-verified.md)

- `tostring(uint)` ambiguous → `Text::Format("%d", int(v))`
- no `char()` / char literals → byte math (`'A'`=65, `'Z'`=90)
- `MwFastBuffer` is a value type → never `Buf is null`
- ternary `cond ? x.Name : "?"` with `wstring Name` → `string(x.Name)` both branches
- `UI::InputInt3`, `UI::BeginTable`, `UI::Columns`, flag args on
  `CollapsingHeader`/`BeginTabBar` → don't exist; use `BeginChild`+`SameLine`
- no `string::ToLower` → manual byte compare helper

## Reference index (load on demand)

| File | When to load |
|---|---|
| `references/mp4-api-verified.md` | **Always for MP4 EDITOR work** — verified member list + error→fix table |
| `references/mp4-runtime-and-dev-memory.md` | **Always for MP4 IN-RACE work** (trainers, HUDs, telemetry, save-state) — playground nod chain, `CTrackManiaPlayer` / `CTrackManiaScriptPlayer` (~120 verified members incl. driver inputs, gear, rpm), the `CSceneVehicleVis` reflection gap (size 3464, no members), full `Dev::` read/write/hook surface, the offset-hunting procedure, and the dynamic-checkpoint pattern |
| `references/mp4-trainer-scaffold.md` | **Building an in-race trainer/HUD on MP4.** Session-verified nod chain (`GetApp → CurrentPlayground → GameTerminals[0].GUIPlayer → cast CTrackManiaPlayer → ScriptAPI`), 41 confirmed members with types, `ERaceState` values, the `CGameWaypointSpecialProperty` lives-in-`GameData`-not-`Game` trap, the dynamic `CurTriggerIndex` checkpoint pattern with multilap bucket formula + static scan fallback, the `Core/Modules` scaffold that compiles, and the de-risking build order (telemetry tab first as proof the chain resolves). |
| `references/op-package-analysis-and-porting.md` | User drops a compiled `.op` and asks "can this run on ManiaPlanet?" — unzip pitfalls, telling a script plugin from a native-DLL plugin, fingerprinting the DLL without a disassembler, recovering structs from the bridge, port-vs-rewrite verdict + the port-brief deliverable template |
| `references/mp4-api-mismatches.md` | More MP4 error→fix cases (time API, ISO 8601, session notes) |
| `references/mp4-supplement.md` | MP4/TM2 platform supplement (differences vs TM2020) |
| `references/mp4-ui-rendering.md` | MP4 UI limits (no images, layout primitives that work) |
| `references/api-quirks-and-pitfalls.md` | General AngelScript/Openplanet quirks (both games) |
| `references/patterns-performance-ui.md` | Performance, diagnostic UI, NanoVG, JSON persistence, public API namespace |
| `references/api-namespaces.md` | Namespace/function reference (UI, Time, Text, IO, Net, Json, nvg, Math…) |
| `references/launch-and-verify.md` | info.toml reference + launch/kill/reload/log-verify command recipes |
| `references/mapforge-architecture.md` | Proven MP4 editor-plugin skeleton (module registry + safe context) |
| `references/static-verify-workflow.md` | No-compiler static verification pass for .as + grid/array block-replication pattern. **When grepping for forbidden natives, strip `/* */` and `//` comments first** — a naive scan flags legitimate mentions *inside* comments (e.g. a doc line "no char() literals on MP4") as false positives. |
| `references/crossgame-tmnext-mp4.md` | **Cross-game TMNEXT+MP4 plugins** — `#if TMNEXT`/`#elif MP4` pattern, shared `CGameCtnApp` members (Switcher/RootMap/Editor/CurrentPlayground), MP4 menu/load detection, deprecated-API fixes, `.op`-is-zip build workaround, and the `nvg::LoadFont` root-path pitfall. Read BEFORE porting any TMNEXT plugin to MP4. |
| `scripts/verify-mp4-branch.py` | Static pre-load guard: extracts the `#elif MP4`/`#else` branch and checks it has no forbidden TMNEXT symbols and only `app.X` members present in `Openplanet4.json`. Run before the in-game kill+relaunch. |
| `references/openplanet-core-json.md` | **Source for Openplanet built-in namespaces** (`IO/Time/UI/Json/Math/Text/Net/Audio/Icons`). Where to find them (`OpenplanetCore.json`, not `Openplanet4.json`) + verified signatures that bit us (`IO::CreateFolder` not `CreateDirectory`, no `IO::WriteFile`, `Time::FormatString` not `Time::Format(string)`, `UI::ListBox` absent → use `BeginCombo`, `Json::Value` has no `IsArray`). |
| `scripts/hermes-verify-mapforge.sh` | Re-runnable ad-hoc load-check: greps `Openplanet.log` for clean `Loaded plugin` + zero `ERR :`/`compilation failed`, confirms 18 module files present & registered. Use after kill+relaunch to prove a clean compile (AngelScript has no offline compiler). |
| `scripts/static-preflight-plugin.py` | **Run BEFORE every kill+relaunch.** Generic static gate over a whole plugin tree: brace/paren balance, every `handle.Member` resolved against `Openplanet4.json` (walking the `p` parent chain), forbidden-native scan on comment-stripped source, `Icons::` allowlist, and module-registered-vs-defined cross-check. Adapt `ROOT`/`PLUGIN`/`HANDLE_TYPES` at the top. Two hard-won details baked in: handle regexes need a `(?<![\w.])` guard (else `s.` matches the tail of `m_modules.Length` and emits phantom errors), and you must prove the gate non-vacuous by injecting `UI::BeginTable` into a sandbox copy and asserting FAIL. |
| `references/plugin-standardization.md` | Naming/structure conventions |
| `references/openplanet-ui-menu-and-scaling.md` | Menu integration + UI scaling |
| `references/plugin-cleanup-recipes.md` | Removing features/plugins cleanly, visibility recipes |
| `references/feedback-map-uid.md` | ManiaPlanet feedback page map-UID extraction |
| `references/blockable-input-callbacks-mp4.md` | **Trainer hotkey input layer** — `BlockableInputCallbacks` on MP4: verified import surface (`RegisterCallback`/`UnregisterCallbacks`, `SetInputBlocked`, `VirtualKeyToKeyboardInput`), `KeyboardInput` F5=0x3F/F6=0x40/F8=0x42 enum values, `PadInput`/`InputDecision`, its `[script] module/exports/shared_exports` manifest shape, and the zero-dep `OnKeyPress` fallback |
| `references/openplanet-docs-dump.md` | Raw Openplanet docs dump (search only when the above fail) |
| `references/review-failure-ledger.md` | **Reviewing a finished plugin/PR/release.** Mechanism checklist of subtle runtime/state/lifecycle/UI/architecture/sync failures (UI containment, state desync, transactional mutation, architecture erosion, network mismatch). Use as a grading checklist, not a keyword linter. Imported from XertroV/openplanet-reviewer (CC0/Unlicense) — see header in file. |
| `references/review-evidence-precedents.md` | **Review evidence + concrete fault probes.** Evidence grades (Demonstrated / Confirmed source invariant / Hypothesis), real project-local precedents (`tm-bosslike`, `Map Together`, `Dips++`) with `path:line` fault fixtures, and the network fault-matrix. Load when a review branch needs a concrete probe or a precedent. Imported from XertroV/openplanet-reviewer (CC0/Unlicense) — see header in file. |
