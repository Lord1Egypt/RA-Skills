# MP4 API Mismatches — Verified Error List & Fixes

Captured while porting 3 red TM2020 plugins to ManiaPlanet 4 (MP4). Every entry
below was hit in a real `Openplanet.log` compile and the fix was confirmed to
remove the error. Read the error line as:
`C:/Users/.../Plugins/<name>/<file>.as (LINE, COL) :  ERR : <message>`

## Quick error → fix index

| Error message (truncated) | Real fix on MP4 |
|---|---|
| `No matching symbol 'UI::Combo'` | Arrow-button selector (◀ / ▶ with `UI::Text`) |
| `No matching symbol 'UI::Spacing'` | `UI::Text("")` or `UI::Dummy(vec2(0,8))` |
| `No matching symbol 'UI::BulletText'` | `UI::Text("• " + s)` |
| `No matching symbol 'UI::SetColumnWidth'` | Delete the call (no column-width API) |
| `'Expression must be of boolean type, instead found void'` on `if (UI::BeginTabBar(...))` / `if (UI::BeginMenuBar())` | These return `void` in MP4 — drop the `if`, keep `UI::EndTabBar()`/`EndMenuBar()` (mind braces, see pitfall) |
| `No matching signatures to 'Time::Parse(const string&)'` | `Time::Parse` takes no string; use the `_DaysFromCivil`/`StampFromUTC` snippet below |
| `No matching symbol 'Time::FromUTC'` | Does not exist; build timestamp manually (snippet below) |
| `No matching signatures to 'Text::Format(const string, int, int, int)'` | `Text::Format` takes ONE arg after the format (`Text::Format("%d", x)`); concatenate the rest |
| `'MapCheckpointPos' is not a member of 'CTrackManiaRaceInterface'` | TM2020-only; default `g_TotalCheckpoints = 1` or guard `#if TMNEXT` |
| `No matching signatures to 'string::IndexOf(const string, int)'` | `string::IndexOf` takes ONE arg. For `s.IndexOf(needle, from)` use `s.SubStr(from).IndexOf(needle) + from` |
| `'Type' is not a member of 'Json::Value'` (on `x.Type`) | Use `x.GetType()` (method), keep `Json::Type::Array`/`::Object`/`::String` enums |
| `No matching signatures to 'Math::RandSeed(...)'` / `Math::Rand()` | `Math::Rand(0, 1000000)` (needs min,max). For a seed, loop `Math::Rand(0,1000000)` N times |
| `No matching symbol 's.Substring'` | `s.SubStr(i, len)` |
| `not a member` on `art.Article.BlockModel` / `art.BlockModel` / `art.CursorBlockModel` | `CGameCtnArticleNodeArticle` → `.Article` (a `CGameCtnArticle`); block name is `art.Article.Name` (wstring → `string(...)`) |
| type mismatch on `PlaceBlock(bi, pos, Dir)` | wrap dir: `CGameEditorPluginMap::ECardinalDirections(int(dir))` (N=0,E=1,S=2,W=3) |
| `No matching signatures to 'Json::Array(a,b,c)'` | `Json::Array()` 0-arg + `.Add(Json::Value(x))` |
| `non-function type int64` on `Time::Stamp()` | `Time::Stamp` is a field, not a call → drop the parens |
| `Identifier 'EMapElemColor' / 'EMapElemColorPalette' is not a data type` | TM2020-only enums; define local enums OR guard with `#if TMNEXT` |
| `No matching symbol 'Permissions::OpenAdvancedMapEditor'` | TM2020-only |
| `'ExperimentalFeatures' is not a member of 'CGameCtnEditorFree'` | TM2020-only |
| `'NextMapElemColor' / 'MapElemColorPalette' is not a member of 'CGameEditorPluginMap'` | TM2020-only |
| `No matching symbol 'PlaceGhostBlock'` / `RemoveGhostBlock` / `PlaceMacroblock_AirMode` | TM2020-only |
| `No matching signatures to 'CreateMacroblockInstance(..., EMapElemColor&, ...)'` | TM2020 signature; MP4 variant takes no color arg |

## ISO 8601 → Unix timestamp (MP4-safe, no Time::FromUTC)

Drop-in replacement for `Time::Parse(iso)`. Handles `YYYY-MM-DDTHH:MM:SS`
(optional `Z` / `+HH:MM` ignored). Returns milliseconds.

```angelscript
// Hinnant's days_from_civil algorithm (MP4-safe, no Time::FromUTC)
int _DaysFromCivil(int y, int m, int d) {
    y -= m <= 2 ? 1 : 0;
    int era = (y >= 0 ? y : y - 399) / 400;
    int yoe = y - era * 400;
    int doy = (153 * (m + (m > 2 ? -3 : 9)) + 2) / 5 + d - 1;
    int doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    return era * 146097 + doe - 719468;
}

int64 StampFromUTC(int Y, int M, int D, int h, int mi, int s) {
    int days = _DaysFromCivil(Y, M, D);
    return int64(days) * 86400 + int64(h) * 3600 + int64(mi) * 60 + int64(s);
}

int64 ParseIsoToMs(const string &in iso) {
    if (iso.Length < 19) return 0;
    int Y  = Text::ParseInt(iso.SubStr(0, 4));
    int M  = Text::ParseInt(iso.SubStr(5, 2));
    int D  = Text::ParseInt(iso.SubStr(8, 2));
    int h  = Text::ParseInt(iso.SubStr(11, 2));
    int mi = Text::ParseInt(iso.SubStr(14, 2));
    int s  = Text::ParseInt(iso.SubStr(17, 2));
    return StampFromUTC(Y, M, D, h, mi, s) * 1000;
}
```

## Verify-in-loop

1. `taskkill /F /IM ManiaPlanet.exe`
2. patch source / rebuild `.op` (or edit extracted `Plugins/<name>/` folder directly)
3. `> Openplanet4/Openplanet.log`  (clear, so old timestamps don't fool you)
4. relaunch game (`python tools/debug_launch.py --wait 90` for TM2TrackGen, or start ManiaPlanet.exe)
5. `grep "ERR :" Openplanet4/Openplanet.log | grep -i <pluginname>`

A stale `.op` held by the running game will re-show the SAME old errors even after
you patched the source — that is the file lock, not a broken patch. Kill the game.

---

## Session additions (2nd pass)

### The "known-good plugin" oracle technique

When unsure whether an API exists on MP4, **don't trust the abridged API txt** and
don't guess — grep a plugin that already loads clean on MP4. `event-calendar-dev`
is the best oracle in this install:

- `grep -rn "Time::FromUTC\|Json::Type\|GetType" .../event-calendar-dev/` told us
  `Json::Type` (via `.GetType()`) and `Time::FromUTC` usage patterns are valid.
- This caught a wrong turn: an earlier edit changed `Json::Type` → `Json::JsonType`
  (wrong), but grepping `event-calendar-dev` showed `Json::Type::String` is correct.
  Always confirm against a working plugin before committing a fix.

### Brace-matching pitfall (void UI calls)

Changing `if (UI::BeginTabBar("X")) { ... UI::EndTabBar(); }` to the MP4-safe
`UI::BeginTabBar("X"); { ... UI::EndTabBar(); }` requires keeping the manual `{`
you added CLOSED. The safe edit:

```
// BEFORE (TM2020)
if (UI::BeginTabBar("MainTabs")) {
    if (UI::BeginTabItem(...)) { ... }
    UI::EndTabBar();
}
// AFTER (MP4) — keep the { and its matching }
UI::BeginTabBar("MainTabs"); {
    if (UI::BeginTabItem(...)) { ... }
    UI::EndTabBar();
}
```

If you drop the `if` but forget to re-add the `{`, you get `Unexpected end of file`
or `Expected ';'` / `Instead found identifier 'Main'` because the trailing
`UI::End()` / namespace close gets mis-scoped. After ANY brace edit, run a balance
check: `python -c "s=open('Main.as',encoding='utf-8').read();print(s.count('{'),s.count('}'))"`
— they must be equal. (`python3` is NOT on this machine; use `python`.)

### Disabling a plugin — the `info.toml` trap

Writing `disabled = true` under `[meta]` in `info.toml` is **IGNORED** by
Openplanet — the plugin still loads (and still shows red if broken). To stop a
TM2020-only plugin from loading on MP4:

- Move the folder: `mv Plugins/<name> Plugins-Archive/<name>` (Openplanet never
  loads from `Plugins-Archive/`). This is how `TrackGeneratorExtended` (deep
  TM2020-only) was retired in favour of the MP4-native `TM2TrackGen`.
- Or disable via the Openplanet UI (F3 → Plugins), which writes
  `Plugins-<name>=false` into `Openplanet4.json` / `Settings.ini`.

### Reference: mp4-ui-rendering

