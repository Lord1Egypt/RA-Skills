# OpenplanetCore.json — the real source for built-in script namespaces

`Openplanet4.json` (written on launch) contains ONLY game Nod-class reflection.
It does NOT contain Openplanet's own script API (`IO::`, `Time::`, `UI::`,
`Json::`, `Math::`, `Text::`, `Net::`, `Audio::`, `Icons::`, `getExceptionInfo()`).
Those live in **`OpenplanetCore.json`** (also in the game dir). When a built-in
call fails to compile, grep THAT file — not the game reflection DB.

## Structure of OpenplanetCore.json

Top-level keys: `op`, `functions`, `classes`, `enums`, `funcdefs`, `props`.

- `functions[]` — free functions. Each has `ns` (namespace string), `name`,
  `decl` (full signature), `args[]`, `returntypedecl`. Fastest way to find a
  built-in: filter `functions` by `ns`.
- `classes[]` — class/struct defs (`name`, `ns`, `methods[]`, `props[]`).
  e.g. `Json::Value` is a class here.
- `enums[]` — enums with `ns`, `name`, `values{}`.
- `props[]` — namespace-level constants (e.g. `Math::PI`).

## Extraction recipes (run from the game dir)

```python
import json, io
d = json.loads(io.open(r"C:/Users/tomekdot/Openplanet4/OpenplanetCore.json",
                       encoding="utf-8").read())
funcs = d.get("functions", [])

def byns(ns):
    return [f.get("decl") for f in funcs if f.get("ns") == ns]

print("\n".join(byns("IO")))
print("\n".join(byns("Time")))
print("\n".join(byns("Json")))
```

To find a specific class (e.g. `Json::Value`) and its methods:
```python
for c in d.get("classes", []):
    if isinstance(c, dict) and c.get("name") == "Value" and c.get("ns") == "Json":
        for m in c.get("methods", []):
            print(m.get("decl"))
```

## Verified built-in signatures (this Openplanet build — 2026-07-27)

### IO (16 funcs — NO raw-text file writer exists)
- `string FromUserGameFolder(const string&in)`  ← Maps/Work paths
- `bool FileExists(const string&in)` / `uint64 FileSize` / `int64 File*Time`
- `void Delete(const string&in)` / `void Copy(path, target)` / `void Move(...)`
- `bool FolderExists(const string&in)`
- `void CreateFolder(const string&in path, bool recursive = true)`  ← NOT `CreateDirectory`
- `void DeleteFolder(const string&in path, bool recursive = false)`
- `string[]@ IndexFolder(const string&in path, bool recursive)`  ← NOT `DirectoryList`
- `void SetClipboard(const string&in text)`
- **NO `WriteFile` / `FileWrite` / `GetUserDir` / `DirectoryList` / `CreateDirectory`.**
  To persist raw text: `IO::SetClipboard` or emit JSON via `Json::ToFile`.
  To read text: no built-in — exchange via a JSON file (`Json::FromFile`).

### Time (11 funcs)
- `uint64 get_Now()` (use `Time::Now`)
- `string FormatString(const string&in format, int64 stamp = -1)`  ← strftime-style,
  e.g. `Time::FormatString("%Y-%m-%d_%H-%M-%S", int64(Time::Now))`
- `string Format(uint64 time, bool fractions = true, bool forceMinutes = true,
   bool forceHours = false, bool short = false)`  ← takes BOOL flags, NOT a format string
- `int64 ParseFormatString(const string&in format, const string&in stamp)`
- `Info Parse(int64 stamp = -1)` / `Info ParseUTC(int64 stamp = -1)`

### Json (6 funcs)
- `Value@ Object()` / `Value@ Array()` / `Value@ Parse(const string&in json)`
- `string Write(const Value@ value, bool pretty = false)`
- `Value@ FromFile(const string&in filename)`
- `void ToFile(const string&in filename, const Value@ value, bool pretty = false)`

`Json::Value` members: `GetType()`, `opIndex(int)`, `get_Length`, `Add(Json::Value@)`,
`Get(const string&in)`, `HasKey`, `Remove(int)`, `GetKeys()`. Implicit conversions
to int/float/bool/string exist so `int(value[c])` works. **NO `IsArray()`** — test
with `val.GetType() != Json::Type::Array` (enum: Unknown=0, String=1, Number=2,
Object=3, Array=4, Boolean=5, Null=6).

### UI (selected)
- `bool BeginCombo(label, current, flags)` / `void EndCombo()` /
  `bool Selectable(label, selected, flags)`  ← use instead of `UI::ListBox` (no ListBox)
- `bool BeginTable(id, columns, flags, ...)`  ← DOES exist on this build
- `BeginTabBar` / `BeginTabItem` / `BeginChild` / `EndChild` all exist
- `void PushStyleColor` / `PopStyleColor` / `PushStyleVar` / `PopStyleVar`

### Math / Text / Net / Audio
- Math: `Abs, Sin, Cos, Atan2, Pow, Sqrt, Floor, Ceil, Round, Min, Max, Clamp,
  Lerp, Distance, Dot, Cross, Rand(int,int), Rand(float,float), ToRad/ToDeg`.
- Text: `ParseInt/ParseFloat/ParseDouble`, `TryParse*`, `Format(const string&in, <type>)`
  (use `Text::Format("%d", int(v))`, never `tostring(uint)`), `EncodeBase64/DecodeBase64`.
- Net: `HttpGet/Post/...`, `UrlEncode/Decode`. Audio: `LoadSample/Play/Start`.

### Icons
`Icons::*` IS valid (FontAwesome subset) but only specific names compile. Verified
valid here: Wrench, Cube, Cubes, Th, PaintBrush, History, MousePointer, Clipboard,
VideoCamera, Eye, Crosshairs, ArrowDown, MapMarker, SearchPlus, SearchMinus, Eraser,
Plus, FolderOpen, List, FileCodeO, Clock, Exchange, Leaf, Repeat, Refresh, Undo,
Gamepad, Tree, Random, Search, Trash, Sitemap, Retweet, PuzzlePiece, Play, Pencil,
Link, Flask, FlagCheckered, Check, Bolt, BarChart, ArrowsAlt.
**INVALID on this build: `Icons::Save`, `Icons::Brush`** (use a valid icon or text-only).

## Pitfall: `char` / `string(uint)` are illegal
No `char` type and no `string(uint)` constructor. Build via `Text::Format("%d", int(v))`,
`I2S(uint)` helpers, or `SubStr` concatenation. Never `string(uint8)` or `char c = s[i]`.
