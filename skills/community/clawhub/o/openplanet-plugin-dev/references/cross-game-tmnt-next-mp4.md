# Cross-game plugin compatibility: TMNEXT + MP4

Verified facts for writing ONE Openplanet AngelScript plugin that compiles and
runs on BOTH Trackmania (2020) [TMNEXT] and Maniaplanet 4 [MP4]. (From the
`tm-green-timer` MP4 port, Aug 2026 — confirmed against `Openplanet4.json` and
`OpenplanetNext.json`, and a clean in-game load with 0 `ERR :`.)

## Preprocessor defines (Openplanet injects these per-game automatically)
- `TMNEXT` — current game is Trackmania (2020)
- `MP4`    — current game is Maniaplanet 4 (4.0 and 4.1)
- Also available: `MP40`, `MP41`, `UNITED`, `MP3`, `TURBO` (see Openplanet docs).
- No `info.toml` game flag is needed; the compiler selects the right branch.

```angelscript
#if TMNEXT
    // TMNEXT-only API here
#elif MP4
    // MP4-only API here
#else
    // fallback (treat like MP4)
#endif
```

## Common base class
`CGameCtnApp` is the base class for both games (Openplanet docs: "Openplanet
uses the base class CGameCtnApp"). On TMNEXT, `CGameManiaApp` DERIVES from
`CGameCtnApp`, so `GetApp()` returns a `CGameCtnApp` on both. Write shared code
against `CGameCtnApp` so it compiles everywhere.

## Members present on BOTH (safe to use unconditionally)
From `ns.Game.CGameCtnApp.m[]` in both reflection DBs:
- `Switcher`          : CGameSwitcher@   (`ModuleStack` : MwFastBuffer<CGameSwitcher@>)
- `Editor`            : CGameCtnEditor@
- `CurrentPlayground` : CGamePlayground@
- `RootMap`           : CGameCtnChallenge@
- `CurrentCampaign`   : CGameCtnCampaign@

## TMNEXT-only members (gate behind `#if TMNEXT`)
- `app.LoadProgress` (CGameLoadProgress@) + `NGameLoadProgress::EState::Displayed`
- `cast<CTrackManiaMenus>(app.Switcher.ModuleStack[0])` — NOTE: `CTrackManiaMenus`
  does NOT exist on MP4 (only `CGameCtnMenus` does, and even that isn't needed).

## MP4 menu/loading detection (no LoadProgress/Menu API)
On MP4 there is no `LoadProgress::EState` and no `CTrackManiaMenus`. Detect
"in menu" vs "loading" with the shared API. **KEEP THE TWO STATES SEPARATE** —
a combined `inMenuOrLoading` check collapses `Pause In Menu` and
`Pause While Loading` into one behavior and always reports "Loading Screen",
which Copilot flagged in the green-timer port. Correct form:
```angelscript
bool inMenu = app.Switcher.ModuleStack.Length < 1;          // empty stack = in a menu
bool inLoading = !inMenu && app.RootMap is null;            // stack non-empty but no map = loading
if (S_PauseInMenu && inMenu) { tmpPauseReason = "in Menu"; return true; }
if (S_PauseWhileLoading && inLoading) { tmpPauseReason = "Loading Screen"; return true; }
```
This goes in both the `#elif MP4` and `#else` branches.

## Deprecated / legacy calls to fix while porting (verified, 2026-08)
These compile but emit `DEPRECATED`/`WARN` lines in `Openplanet.log`; fixing
them yields a fully clean load (0 `ERR :` AND 0 `DEPRECATED`):
- `nvg::LoadFont("Exo-Bold.ttf", true, true)` → `nvg::LoadFont("Exo-Bold.ttf")`.
  The `fallbackIcons`/`fallbackArial` bools are deprecated; drop them (fallback
  fonts are now always included). Note: the ROOT-PATH pitfall below is separate —
  you still must place the font at the plugin root.
- `Time::Format(int(ms), false, true, true)` (4 args) →
  `Time::Format(uint64(ms), false, true, true, false)` (5 args). On MP4
  `Time::Format` signature is `(uint64 time, bool fractions, bool forceMinutes,
  bool forceHours, bool short)` — the original 4-arg TMNEXT form is missing the
  trailing `short` bool. Use `uint64(...)` cast so the same source compiles on
  both games. Fix all call sites (timer display + Saved Timers history).

## Font loading pitfall (`nvg::LoadFont`)
`nvg::LoadFont("Exo-Bold.ttf")` resolves the path RELATIVE TO THE PLUGIN ROOT,
NOT to `src/`. In a dev-folder layout the `.as` files live in `src/` but the
font must sit at the plugin root (next to `info.toml`) or it silently falls back
to the default font. In a packaged `.op`, everything is flattened to the root, so
a font in `src/` works there but NOT in the dev folder.
Fix: keep font files at the plugin root and copy them there in `build.sh`:
- release: add the font to the 7z list (`7z a $BUILD_NAME ./$pluginSrc/* ./Font.ttf ...`)
- dev: `cp -LR -v ./Font.ttf $_build_dest/`

## Verification for cross-game plugins (no offline compiler)
1. Verify each branch's natives against the matching reflection DB before writing.
2. Build the `.op` and/or copy the folder plugin into the game's `Plugins/` dir.
3. Run the game with `/openplanet:developer` (DeveloperMode=true in Settings.ini),
   kill + relaunch for a clean recompile, then grep `Openplanet.log` for
   `Loaded plugin '<Name>'` and 0 `ERR :` / `Script compilation failed`.
4. **Static scan the branch you cannot run:** extract the `#elif MP4` block and
   grep it against `Openplanet4.json` — confirm every `app.X` / `Switcher.X`
   member exists, and that NO TMNEXT-only token (`CTrackManiaMenus`,
   `NGameLoadProgress`, `LoadProgress`) leaks into that branch (strip `//`
   comments first, or a mention inside a comment will false-positive).
