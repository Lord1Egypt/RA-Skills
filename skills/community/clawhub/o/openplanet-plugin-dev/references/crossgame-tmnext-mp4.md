# Cross-game porting: TMNEXT (Trackmania 2020) <-> MP4 (Maniaplanet 4)

Verified while porting `tm-green-timer` (XertroV) so it runs on BOTH games
without changing TM2020 behaviour. Openplanet injects `TMNEXT` and `MP4`
preprocessor defines per game, so gate game-specific code with `#if` / `#elif`.

## When to use
A plugin compiles on TMNEXT but fails on MP4 (or misbehaves) because it
references a TMNEXT-only class/namespace. Classic culprits that do NOT exist on
MP4: `CTrackManiaMenus`, `NGameLoadProgress::EState`, `app.LoadProgress`.

## Verified SHARED members (exist on both via `CGameCtnApp`)
- `app.Switcher.ModuleStack` (MwFastBuffer<CGameSwitcher@>)
- `app.RootMap` (CGameCtnChallenge@) — null when no map is loaded
- `app.Editor` (CGameCtnEditor@)
- `app.CurrentPlayground` (CGamePlayground@)

Use these for cross-game logic; they compile on both builds. `CGameCtnApp` is
the common base class per the Openplanet docs, so `GetApp()` returns it on both.

## Pattern
```angelscript
#if TMNEXT
    // original TMNEXT-only code — keep byte-for-byte, do not touch
    if (S_PauseInMenu && (app.Switcher.ModuleStack.Length < 1 || cast<CTrackManiaMenus>(app.Switcher.ModuleStack[0]) !is null)) { ... }
    if (S_PauseWhileLoading && app.LoadProgress.State == NGameLoadProgress::EState::Displayed) { ... }
#elif MP4
    bool inMenu = app.Switcher.ModuleStack.Length < 1;
    bool inLoading = !inMenu && app.RootMap is null;
    if (S_PauseInMenu && inMenu) { tmpPauseReason = "in Menu"; return true; }
    if (S_PauseWhileLoading && inLoading) { tmpPauseReason = "Loading Screen"; return true; }
#else
    // same heuristic as MP4 for any other Openplanet game
    ...
#endif
```

## RULE: never change the TMNEXT branch
The user requires TM2020 behaviour to stay identical. Only ADD an `#elif MP4`
branch; do not edit the `#if TMNEXT` block. `CTrackManiaMenus` /
`NGameLoadProgress` must appear ONLY inside `#if TMNEXT` (Copilot-style reviews
will flag them if they leak into the MP4 branch).

## Menu/loading detection on MP4 (verified)
- `app.Switcher.ModuleStack.Length < 1`  -> in a MENU
- `!inMenu && app.RootMap is null`      -> map still LOADING
This replaces `cast<CTrackManiaMenus>` (menu) and `LoadProgress::EState::Displayed`
(loading), neither of which exists on MP4.

## Deprecated / legacy API fixes found while porting (apply on MP4)
- `nvg::LoadFont("x.ttf", true, true)` -> `nvg::LoadFont("x.ttf")`.
  (`fallbackIcons`/`fallbackArial` are deprecated; logs `DEPRECATED: nvg::LoadFont ...`.)
- `Time::Format(int(t), false, true, true)` (4 args) ->
  `Time::Format(uint64(t), false, true, true, false)` (5 args on MP4:
  time, fractions, forceMinutes, forceHours, short).
- `if (i == activeIndex)` where `i` is `uint`, `activeIndex` is `int` ->
  `if (int(i) == activeIndex)` (fixes `Signed/Unsigned mismatch` WARN).

## Font loading in dev-folder layout
`nvg::LoadFont("Exo-Bold.ttf")` resolves relative to the PLUGIN ROOT, not `src/`.
In a dev-folder plugin keep the font at `<Plugin>/Exo-Bold.ttf`, NOT
`<Plugin>/src/Exo-Bold.ttf` (the latter only works in a flattened `.op`).
Update `build.sh` to copy the font to the root of both dev and release outputs.

## Shipping: `.op` is a ZIP, not 7z
`build.sh release` calls `7z a ...`. If `7z` is absent the build silently
produces no `.op`. The `.op` file is a plain ZIP archive with the plugin's `.as`
files at the ROOT (plus info.toml, LICENSE, README, fonts). Build manually with
python when 7z is missing:
```python
import zipfile, os
out = 'green-timer-0.2.5.op'
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for name, path in [('GreenTimer.as', 'src/GreenTimer.as'),
                        ('Exo-Bold.ttf', 'Exo-Bold.ttf'),
                        ('info.toml', 'info.toml'),
                        ('LICENSE', 'LICENSE'),
                        ('README.md', 'README.md'),
                        ('nvg.as', 'src/nvg.as'), ('Main.as', 'src/Main.as'),
                        ('History.as', 'src/History.as')]:
        z.write(path, name)
# verify version inside: zipfile.ZipFile(out).read('info.toml')
```

## Verification recipe (no offline compiler)
AngelScript for MP4 has NO offline compiler. Prove a clean load by
kill+relaunch+greplog (see openplanet-compile-verify-loop). After a cross-game
port, ALSO statically check: extract the MP4 branch and grep for forbidden
TMNEXT-only symbols, and confirm every used `app.X` member exists in
`Openplanet4.json` (`ns.Game.CGameCtnApp.m[]`). A reusable checker lives at
`scripts/verify-mp4-branch.py` (under this skill).
