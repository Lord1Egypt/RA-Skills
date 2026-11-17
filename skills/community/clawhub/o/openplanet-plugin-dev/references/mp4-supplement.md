## 🟢 ManiaPlanet 4 (MP4 / TM2) Supplement

> MP4 exposes a **stricter** ManiaScript API than TM2020. Openplanet loads the
> same `.op` for both games, but the symbol set at compile time is the game's own
> API — so TM2020-style code often fails on MP4 with `No matching symbol` /
> `is not a member of`. This supplement adds the MP4-specific gotchas, the
> desktop-driven launch loop, and the file-layout rules. Where it conflicts with
> a TM2020 pattern above, **this supplement wins for MP4**.
>
> The `#if TMNEXT` / `#elif MP4` block in *Preprocessor Directives* above is your
> primary guard: wrap TM2020-only code in `#if TMNEXT` and MP4-only code in
> `#elif MP4`. The `yield()`/`sleep(ms)` note in *Plugin Architecture* still
> applies — see the Performance section below for the MP4-specific lag trap.

### 🚀 Desktop Launch & Reload Loop (cua-driver)

The user opens the game from the Windows desktop with the computer-use driver
(cua-driver), not `start ""`. Use `launch_app` with the full exe path — it
launches hidden (no focus steal):

```
mcp__cua_driver__launch_app(path="C:\\Program Files (x86)\\ManiaPlanet\\ManiaPlanet.exe")
```

ManiaPlanet first shows a launcher/title window, then the main game window. It
lands **behind** other windows (z-index 0) — bring it forward with Alt-Tab if you
need to drive it. First boot takes 20–40s (Ubisoft Connect login, shader cache).
Poll `tasklist | grep -i maniaplanet` or `mcp__cua_driver__list_windows` if unsure.

⚠️ ManiaPlanet is a **non-UIA (DirectX) surface** — `get_window_state` returns no
elements. Drive it by pixel coordinates, or rely on `Openplanet.log` for
verification. Don't fight focus. Log path: `C:\Users\tomekdot\Openplanet4\Openplanet.log`.

**Reload after an edit (folder plugin, no full restart needed):**
1. Focus the game window.
2. Press **F3** → opens the Openplanet overlay.
3. THEN press **Ctrl+Shift+R** → reloads plugins.

`Ctrl+Shift+R` **alone does NOT work on MP4** — it only works after F3 opens the
overlay. Foreground hotkeys fail without UIAccess; drive them via cua-driver or
just restart the game. When in doubt, a full restart (kill + relaunch) is the most
reliable reload because the on-disk source is re-read from scratch.

### 📁 Folder Plugin vs `.op` Zip — READ THIS FIRST

- A **folder plugin** (`Plugins/<name>/` containing `Main.as`, `info.toml`, …) is
  read by Openplanet **directly from source** at game start. No build, no
  packaging. Edits take effect on next game launch (or `Ctrl+Shift+R` after F3).
  → This is the dev mode. Keep your plugin HERE.
- A **`.op` zip** is the distributed form. The running game holds it open for
  READ+WRITE, so you CANNOT overwrite it while the game runs. To update a `.op`:
  1. `taskkill /F /IM ManiaPlanet.exe`
  2. rebuild + copy fresh `.op` into `Openplanet4/Plugins/`
  3. relaunch + F3 → Ctrl+Shift+R
- Rule of thumb: develop as a folder in `Plugins/`. Only pack a `.op` when you
  ship. Do NOT pack during dev — it adds a rebuild step and risks a full-path zip
  entry that won't load.

### 🗂️ Plugin Folder Layout & Visibility

- **`Plugins/`** → standard menu (F3 → Plugins), checkbox toggle, Ctrl+Shift+R reloads.
- **`Plugins-Developer/`** → hidden "Developer" section, **NOT** in the normal menu.
  Don't leave plugins here if the user expects to see them in F3 → Plugins.
- **`Plugins-Archive/`** → skipped entirely by Openplanet. Use to disable TM2020-only
  plugins without deleting: `mv Plugins/<name> Plugins-Archive/<name>`.
- If a plugin is in BOTH `Plugins/` and `Plugins-Developer/`, it loads TWICE
  (duplicate compile errors). Keep it in exactly one place.

**Disabling gotchas:**
- `info.toml` `disabled = true` → **IGNORED**. Plugin still loads and shows red.
- `Settings.ini` `Plugin_<name>=false` → **IGNORED for folder plugins** (only works
  for `.op` zips that have a site ID from the Openplanet plugin manager).
- Reliable disable: move to `Plugins-Archive/`, or toggle via in-game UI (F3 →
  Plugins) which writes `Plugins-<name>=false` to `Openplanet4.json`.

### 🧹 Mass Cleanup Workflow (many red plugins)

1. **BACKUP FIRST:** `cp -r Plugins backup-<date>` and `cp -r Plugins-Developer backup-<date>/`.
2. Decide per-plugin: **PORT** (shallow TM2020 mismatches — UI/Time/Json/Text::Format
   only, e.g. `maniacalendar-dev`, `chase-mode-overlay`) vs **ARCHIVE** (deep TM2020-only:
   `Draw::`, `IO::`, `ExperimentalFeatures`, `PlaceGhostBlock`, `EMapElemColor`,
   `TrackGeneratorExtended`, `pursuit-*`, `green-*`, `drift-bar-dev`, `rounds-tracker-dev`,
   `pomodoro-plugin-dev`, `apeiron-galaxy-dev` TM2020 branch, `player-stats`, `green-timer`).
   Porting each is hours of rewrite — not worth it for unused plugins.
3. Move archived ones to `Plugins-Archive/`.
4. Verify: kill game → relaunch → `grep "ERR :" Openplanet.log | grep -oP "Plugins/[^/]+/"`
   should be EMPTY. Clear the log (`> Openplanet.log`) before a clean run.

Full command recipes: `Reference: plugin-cleanup-workflow` (below).

### 🐛 MP4-Only API Mismatches (the table)

Full verified list with exact replacement code (incl. the Hinnant ISO→timestamp
snippet) in `Reference: mp4-api-mismatches` (below). Note: `string::IndexOf` 1-arg and
`UI::TextColored`/`UI::Font` are already in the *Common Build Errors* table above —
this table covers the MP4-specific ones not listed there.

| TM2020-style code | MP4 error | Fix for MP4 |
|---|---|---|
| `UI::Combo(...)` | No matching symbol | Arrow selector: `UI::Button("◀") / UI::Text(shapes[idx]) / UI::Button("▶")` |
| `UI::Spacing()` | No matching symbol | `UI::Text("")` or `UI::Dummy(vec2(0,8))` |
| `UI::BulletText(s)` | No matching symbol | `UI::Text("• " + s)` |
| `UI::SetColumnWidth(n)` | No matching symbol | Remove (no table columns on MP4) or `UI::SetNextItemWidth(n)` |
| `Time::Parse(string)` | No matching signatures | `Time::Parse` does NOT take a string in MP4. Parse ISO 8601 yourself with `_DaysFromCivil` + `StampFromUTC`. `Time::ParseUTC(int64)` and `Time::Stamp` (field) DO exist. |
| `Time::FromUTC(Time::Info)` | No matching symbol | Does NOT exist in MP4. Build the Unix timestamp manually with `_DaysFromCivil` + `StampFromUTC`. |
| `UI::BeginTabBar(...)` / `UI::BeginMenuBar()` | 'Expression must be of boolean type, instead found void' | On MP4 these return `void`, NOT `bool`. Remove the `if (...)` wrapper — just call them, then `UI::EndTabBar()` / `UI::EndMenuBar()`. Keep the `{ }` balanced. |
| `Math::RandSeed(n)` | No matching symbol | Loop `Math::Rand(0, 1000000)` to advance RNG deterministically. |
| `Math::Rand()` (no args) | No matching signatures | `Math::Rand(0, 1000000)` (needs min,max). |
| `x.Type == Json::Type::Array` | 'Type' is not a member of 'Json::Value' | The `.Type` **property** is gone in MP4, but the `Json::Type` enum and the `.GetType()` **method** remain. Replace `x.Type` with `x.GetType()` (keep `Json::Type::Array`). Verified: `event-calendar-dev` uses `val.GetType() == Json::Type::String`. |
| `s.Substring(i,1)` | No matching symbol | `s.SubStr(i, 1)`. |
| `art.Article.BlockModel` / `art.BlockModel` | not a member | Inventory node `CGameCtnArticleNodeArticle` has `.Article` (a `CGameCtnArticle`). Block name via `art.Article.Name` (wstring → `string(...)`). `MwId` cannot be cast with `string(...)`; use `.Name`. |
| `map.PlaceBlock(bi, pos, Dir)` | Dir type mismatch | `PlaceBlock` needs `CGameEditorPluginMap::ECardinalDirections`. Wrap: `CGameEditorPluginMap::ECardinalDirections(int(dir))` (North=0,East=1,South=2,West=3 — same as `Dir`). |
| `Json::Array(a,b,c)` | No matching signatures | `Json::Array()` takes 0 args; build with `j.Add(Json::Value(x))`. |
| `Time::Stamp()` | non-function type int64 | `Time::Stamp` is a **field**, not a call → use `Time::Stamp` (no parens). |
| `EMapElemColor` / `EMapElemColorPalette` in `CGameEditorPluginMap` | not a data type | TM2020-only enums. Remove or guard with `#if TMNEXT`. |
| `CTrackManiaRaceInterface::MapCheckpointPos` | not a member | TM2020-only member; guard with `#if TMNEXT`. |

### ⚡ Performance / Lag Warnings (MP4)

Openplanet spams `Plugin <name> is laggy at X ms average!` when an entry point
blocks the script thread.

**`sleep(n)` instead of `yield()` in `Main()` loop** — `sleep` BLOCKS the thread for
`n` ms; Openplanet counts that blocked time as the plugin's execution time → laggy.
`yield()` hands control back without blocking, so the loop wakes each frame but the
per-iteration cost is tiny:

```angelscript
uint64 g_lastMapCheckTime = 0;
while (true) {
    uint64 now = Time::Now;
    if (g_lastMapCheckTime == 0 || now - g_lastMapCheckTime >= 1000) {
        g_lastMapCheckTime = now;
        CheckCurrentMap();   // light: only reads app.RootMap.IdName
    }
    yield();
}
```

**`GetApp().RootMap` polled too often** — accessing `.RootMap` copies the whole
`CGameCtnChallenge` object into the script context. Throttle to ~1000ms (maps don't
change mid-second). `apeiron-galaxy-dev` was laggy at 9–11ms at 250ms polling;
1000ms fixed it.

**`Net::HttpGet` (sync) inside `RenderMenu()`** — blocks per frame. Move to a
throttled background loop.

Verify: `grep "laggy" Openplanet.log` → EMPTY.

### 🖼️ UI Constraints on MP4 (no image API!)

**MP4 has no `UI::Image` and no `Images::` namespace.** You cannot load a URL picture
into an overlay. Fake thumbnails with a colored `BeginChild` accent bar; use recolored
`UI::Button` pills for category badges; detect category from title text. Full patterns
(category detection, newsletter card, meta-description extraction) in
`Reference: mp4-ui-rendering` (below).

Also NOT in the core MP4 API: `UI::GetCursorScreenPos()`, `UI::SetCursorPos()`,
`UI::IsItemHovered()`, `DrawList`, `nvg`. Build layout with `Dummy` + `SameLine` +
nested `BeginChild` instead. (`nvg::*` from the TM2020 patterns above does not exist
on MP4.) `UI::Button(label, vec2(0,0))` → `vec2(0,0)` means auto-size (good for pills).
Balance `UI::PushStyleColor` / `PopStyleColor` exactly (use `PopStyleColor(4)`).

### 🔧 Brace / Syntax Pitfalls

When you drop `if (` from `UI::BeginTabBar(...)` / `UI::BeginMenuBar()` (they return
`void` on MP4), you MUST keep the manual `{` you added closed, or you get
`Unexpected end of file` / `Expected ';'` / `Instead found identifier 'Main'`. After
any brace edit run:

```bash
python -c "s=open(r'Main.as','r',encoding='utf-8').read();print(s.count('{'),s.count('}'))"
```

Pairs must be equal (`python3` is NOT installed here — use `python`).

### 🧠 Oracle Technique & Verified Plugins

- **Oracle:** when unsure if an API exists on MP4, don't trust the abridged
  `Openplanet-ManiaScript-API.txt` (it omits e.g. `Json::Value` methods) and don't
  guess. Grep a plugin that already loads clean — `event-calendar-dev` is the best
  oracle (`grep -rn "Json::Type\|GetType\|Time::FromUTC" .../event-calendar-dev/`).
  This caught a wrong turn where `Json::Type` was wrongly rewritten to `Json::JsonType`.
- **`TM2TrackGen`** (from-scratch MP4 plugin, `C:\Users\tomekdot\Projects\TM2TrackGen\`):
  `info.toml` has NO `[game]` section (so it loads on MP4), reads block names from
  `editor.PluginMapType.Inventory` at runtime, and `ToCardinal(Dir)` wraps `PlaceBlock`.
- **`TrackGeneratorExtended`** is a DEEP TM2020 plugin (beyond color enums it uses
  `Permissions::OpenAdvancedMapEditor`, `CGameCtnEditorFree::ExperimentalFeatures`,
  `PlaceGhostBlock`, `RemoveGhostBlock`, `PlaceMacroblock_AirMode`,
  `CreateMacroblockInstance(...)` — none exist in MP4). Treat as TM2020-only or replace
  with `TM2TrackGen`.

### 📎 MP4 reference files in this skill

- `Reference: mp4-api-mismatches` (below) — full verified API-mismatch list with exact MP4-safe replacement code (incl. Hinnant ISO→timestamp snippet).
- `Reference: mp4-ui-rendering` (below) — UI/UX restyling constraints (no image API), newsletter-card + category-badge patterns, meta-description extraction.
- `Reference: plugin-cleanup-workflow` (below) — Plugins/ vs Plugins-Developer/ vs Plugins-Archive layout, disable gotchas, backup/merge/archive command recipes.
- `Reference: launch-commands` (below) — cua-driver launch recipes, kill/reload, log-grep, brace check.


---

