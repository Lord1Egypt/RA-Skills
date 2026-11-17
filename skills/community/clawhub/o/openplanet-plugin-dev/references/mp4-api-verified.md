# MP4 AngelScript verified API facts (from the MapForge build, July 2026)

These were hit compiling a real ManiaPlanet 4 plugin and confirmed against the
reflection DB Openplanet writes to `Openplanet4/Openplanet4.json` on launch
(`ns.Game.<ClassName>.m[]` — each entry has `n`=member name, `t`=type). Treat
that JSON as ground truth: grep it before trusting any member name. All of these
produce COMPILE ERRORS if you use the TM2020 form.

| You wrote | MP4 reality | Correct form |
|---|---|---|
| `char(c)` / `uint('A')` char literal | `char` type and char-literal casts do NOT exist | bytes as `uint`; A-Z = 65..90; append `input.SubStr(i,1)` to build strings |
| `Map.Blocks is null` / `Map.AnchoredObjects is null` | `MwFastBuffer<T>` is a **value type**, never a handle | guard only `if (Map is null)`, then `i >= Map.Blocks.Length` |
| `tostring(uintValue)` | `tostring(uint)` is AMBIGUOUS (uint→int and uint→float both match) | `Text::Format("%d", int(v))` — cast to int first; wrap in `I2S(uint)` |
| `s.ToLower()` / `string::ToLower` | no such method on MP4 | manual `LCByte` A-Z→a-z compare; use a `ContainsCI(haystack, needle)` helper |
| `UI::InputInt3(label, int3)` | does NOT exist (`UI::InputFloat3` DOES) | three `UI::InputInt("X",x); UI::SameLine();` for Y, Z |
| `UI::BeginTable(id, cols, flags)` | returns `void` on MP4; table API unreliable | `UI::BeginChild` + `UI::SameLine` panels, or scrollable `BeginChild` list |
| `UI::Columns(n)` / `UI::NextColumn()` | unreliable/absent on MP4 | `BeginChild` + `SameLine` |
| `UI::CollapsingHeader(label, UI::TreeNodeFlags::X)` | single `string` arg only | `UI::CollapsingHeader(label)` |
| `UI::BeginTabBar(id, UI::TabBarFlags::X)` | `string id` only | `UI::BeginTabBar(id);` |
| `b.IsClip` on `CGameCtnBlock` | member does NOT exist (only `IsGround`) | show IsGround only |
| `it.IVariant` on `CGameCtnAnchoredObject` | member does NOT exist (`Scale` DOES) | use `Scale`; drop `IVariant` |
| `CGameCursorBlock::ECardinalDir(d)` | enum is `ECardinalDirEnum` | `CGameCursorBlock::ECardinalDirEnum(d)` |
| `ctx.PluginMapType.CursorBlockModel = model` | `CGameCtnBlockInfo` has no value `opAssign` | cannot set directly; `IO::SetClipboard(model.Name)` or use editor input |
| `it.ItemModel.CollectionId.GetName()` | `CollectionId` is `UnnamedEnum` (no GetName) | show `it.ItemModel.Name` only |
| `cond ? obj.Name : "?"` when `Name` is `wstring` | `wstring` vs `string` → no common ternary type; `string("?")` alone still ambiguous | `cond ? string(obj.Name) : string("?")` (cast wstring branch to string). Plain `+` auto-converts wstring, so non-ternary `UI::Text("x "+obj.Name)` is fine. `CGameCtnBlockInfo.Name` is `wstring` on MP4. |
| `CGameCtnBlockInfo.Name` type | it is `wstring` (not `string`) on MP4 | use `string(b.BlockModel.Name)` when you need a string |
| plain folder plugin refuses to load | needs developer signature mode | launch `ManiaPlanet.exe /openplanet:developer` |

## Members CONFIRMED present on MP4 (safe to use)
- `CGameCtnBlock`: `CoordX/Y/Z` (uint), `BlockDir` (ECardinalDirections), `IsGround`, `BlockInfoVariantIndex`, `MobilIndex`, `WaypointSpecialProperty` (CGameWaypointSpecialProperty@), `BlockModel` (CGameCtnBlockInfo@), `Coord` (nat3)
- `CGameCtnAnchoredObject`: `BlockUnitCoord` (nat3), `AnchorTreeId` (MwId, has GetName()), `AbsolutePositionInMap` (vec3), `Yaw/Pitch/Roll` (float, radians), `Scale` (float), `ItemModel` (CGameItemModel@), `WaypointSpecialProperty`
- `CGameCursorBlock`: `Coord` (nat3), `Dir` (ECardinalDirEnum), `AdditionalDir` (EAdditionalDirEnum)
- `CGameEditorPluginMap`: `CursorBlockModel` (readable), `GetBlockModelFromName(name)` → CGameCtnBlockInfo@, `Blocks` (MwFastBuffer<CGameCtnBlock@>), `AutoSave()`
- `CGameCtnChallenge`: `EdChallengeId` (string), `Size` (nat3), `Blocks`, `AnchoredObjects`, `AuthorNickName` (wstring), `MapName` (wstring)
- `CGameWaypointSpecialProperty`: `Tag` (string), `Order` (uint)
- Helpers that exist: `ExploreNod(label, nod)`, `IO::SetClipboard`, `Math::Rand(min,max)` (both args), `Math::ToRad/ToDeg`, `Text::Format`

## Verified MUTATION API (CGameEditorPluginMap) — the only valid edit surface

Editor++ (TM2020) and old skill references hallucinate `CGameCtnEditorBase.AddBlock`,
`ItemNew`, `AddItem` — **these do NOT exist on MP4**. All map mutation goes through
`CGameEditorPluginMap` (reachable as `Editor.PluginMapType`, typed as the parent class).
`EditorContext.PluginMapType` is `CGameEditorPluginMap@`.

| Action | Verified call | Notes |
|---|---|---|
| Undo / Redo | `pm.Undo()` / `pm.Redo()` → bool | no args |
| Place block by NAME+coord | `pm.GetBlockModelFromName(str)` → CGameCtnBlockInfo@; `pm.PlaceBlock(model, int3, ECardinalDirections)` → bool | model from name works — no cursor setter needed |
| Preview placement | `pm.CanPlaceBlock(model, int3, ECardinalDirections, bool OnGround, uint Variant)` → bool | |
| Remove block | `pm.RemoveBlock(int3 Coord)` → bool | by coordinate, not handle |
| Remove item | `pm.RemoveItem(CGameCtnEditorScriptSpecialProperty@)` → bool | **fragile**: `Items` buffer is `CGameCtnEditorScriptAnchoredObject@`, type mismatch; resolve via `cast<CGameCtnEditorScriptSpecialProperty>(it.WaypointSpecialProperty)`, often null on MP4 |
| Bulk delete | `RemoveAllBlocks()`, `RemoveAllObjects()`, `RemoveAllTerrain()`, `RemoveAll()` | no args |
| Copy/paste | `CopyPaste_Copy/Cut/Remove/SelectAll/ResetSelection()`, `CopyPaste_Symmetrize()` → bool | |
| Validate / test | `Validate()`, `TestMapFromStart()`, `TestMapFromCoord(int3, ECardinalDirections)`, `TestMapWithMode(wstring)` | |
| Save | `SaveMap(wstring FileName)` | plain string accepted via implicit conversion |
| Camera (writable) | `CameraVAngle`, `CameraHAngle`, `CameraToTargetDistance`, `CameraTargetPosition` (vec3), `CameraPosition` (vec3) | floats/vec3 |
| Modes (writable) | `PlaceMode` (EPlaceMode), `EditMode` (EditMode), `UndergroundMode` (bool), `BlockStockMode` (bool) | |

Enum values (verified):
- `ECardinalDirections` (on `CGameEditorPluginMap`): `North, East, South, West` = 0..3.
- `EPlaceMode`: Unknown, Terraform, Block, Macroblock, Skin, CopyPaste, Test, Plugin, CustomSelection, OffZone, BlockProperty, Path, GhostBlock, Item, Light.
- `EditMode`: Unknown, Place, FreeLook, Erase, Pick, SelectionAdd, SelectionRemove.

Value types are constructible: `int3(x,y,z)`, `nat3(x,y,z)`, `vec3(x,y,z)`.

## Reflection-DB grep recipe
```
python -c "import json,io; d=json.load(io.open(r'C:/Users/tomekdot/Openplanet4/Openplanet4.json',encoding='utf-8')); c=d['ns']['Game']['CGameCtnBlock']['m']; print('\n'.join('%s  %s'%(m['n'],m['t']) for m in c))"
```

## Items, variants, terrain, map metadata (verified 2026-07-27)
- `pm.Items` -> `MwFastBuffer<CGameCtnEditorScriptAnchoredObject@>` (editable wrapper).
  Each item exposes: `AbsolutePositionInMap` (vec3), `Yaw`/`Pitch`/`Roll` (float),
  `Scale` (float), `ItemModel` (`CGameItemModel@`).
- `RemoveItem(CGameCtnEditorScriptSpecialProperty@ Item) -> bool`.
- **NO `PlaceItem` / `GetItem` / `AddItem` exist anywhere.** Cannot create new items
  programmatically — only iterate/modify/remove existing. "Scatter new items" must be
  done via blocks (`PlaceBlock`) instead.
- `CGameCtnBlock` variant fields: `BlockInfoVariantIndex` (uint), `MobilVariantIndex` (uint).
  `CGameCtnBlock.Coord` (nat3), `Dir` (`ECardinalDirections`), `BlockModel`, `Skin`, `IsGround`.
- `CGameCtnBlockInfo` flags present: `IsTerrain` (bool), `IsRoad` (bool), `Name` (wstring).
  Does NOT expose `IsGround`/`IsSkinnable`/`IsDeco`/`IsWall`/`IsPlatform`/`Variants`.
- Skinnability: use `pm.IsBlockModelSkinnable(CGameCtnBlockInfo@) -> bool`,
  `pm.GetBlockModelSkin(model, uint) -> wstring`, `pm.SetBlockSkin(CGameCtnBlock@, wstring) -> void`.
- `pm.SaveMap(wstring FileName) -> void` (FULL path; creates file). `pm.AutoSave()`, `pm.Validate()` (no args).
- Terrain: `pm.PlaceTerrainBlocks(CGameCtnBlockInfo@, int3 Start, int3 End) -> bool`;
  `pm.RemoveTerrainBlocks(int3 Start, int3 End) -> bool`;
  `pm.GetBlockGroundHeight(CGameCtnBlockInfo@, int X, int Z, ECardinalDirections) -> uint`.
- Reach map: `pm.Map` -> `CGameCtnChallenge`: `Blocks`, `AnchoredObjects`, `Size` (nat3),
  `MapName`, `AuthorLogin`, `AuthorNickName`, `Comments`.
- `Time::` / `IO::` / `UI::` / `Json::` are Openplanet BUILT-INS, NOT in the Nadeo
  reflection DB. The REAL signatures (verified in OpenplanetCore.json, 2026-07-27)
  differ from older skill notes — use these:
  - IO: `FromUserGameFolder(string)->string`, `FromAppFolder`, `FromDataFolder`,
    `FromStorageFolder`, `FileExists`, `FileSize`, `FolderExists`, `CreateFolder(path, bool recursive=true)`,
    `DeleteFolder`, `Delete`, `Copy`, `Move`, `IndexFolder(path, bool recursive)->string[]@`,
    `SetClipboard(string)`. **NO `WriteFile` / `FileWrite` / `GetUserDir` / `DirectoryList` /
    `CreateDirectory`** — there is NO raw-text file writer in this OP build.
  - Time: `Time::Now` (uint64), `Time::FormatString(string fmt, int64 stamp=-1)->string`
    (strftime-style, e.g. "%Y-%m-%d_%H-%M-%S"). `Time::Format(uint64, bool...)` exists but
    takes bools, NOT a format string.
  - Json: `Json::Parse(string)->Value@`, `Json::ToFile(string, const Value@, bool pretty)`,
    `Json::FromFile(string)->Value@`, `Json::Object()`, `Json::Array()`.
  - UI: `BeginCombo(label, current)->bool` + `EndCombo()` + `Selectable(label, bool)`,
    `BeginTable(id, columns, flags)`, `BeginTabBar`/`BeginTabItem`. **NO `UI::ListBox` /
    `UI::CollapsingHeader(label, flags)`** (older notes were wrong).
  - Icons: `Icons::*` IS valid (FontAwesome subset) but ONLY specific names compile —
    verified-valid examples: Wrench, Cube, Cubes, Th, PaintBrush, History, MousePointer,
    Clipboard, VideoCamera, Eye, Crosshairs, ArrowDown, MapMarker, SearchPlus, SearchMinus,
    Eraser, Plus, FolderOpen, List, FileCodeO, Clock, Exchange, Leaf, Repeat, Refresh,
    Undo, Gamepad, Tree, Random, Search, Trash, Sitemap, Retweet, PuzzlePiece, Play, Pencil,
    Link, Flask, FlagCheckered, Check, Bolt, BarChart, ArrowsAlt. **INVALID: `Icons::Save`,
    `Icons::Brush`** (use text-only or a valid one).
  - `string(uint)` and `char` are ILLEGAL. Build strings via `Text::Format("%d", int(v))`
    or `SubStr` concatenation; never `string(uint8)`.
  - `MwFastBuffer<T@>` is a VALUE type — you CANNOT take a handle `@` to it.
    Write `MwFastBuffer<CGameCtnBlock@> blocks = pm.Map.Blocks;` (value), NOT
    `MwFastBuffer<...>@ blocks = ...`. Handles on the BUFFER error with
    "Object handle is not supported for this type" / "Can't convert to int".
  - `array<T>@` sorting: use `arr.Sort(function(a,b){ return a.x < b.x; })` — there is
    NO `arr.sort(...)` (lowercase). The comparator must return bool (a less-than b).
  - `pm.Items` (CGameCtnEditorScriptAnchoredObject) exposes only `Position` (vec3),
    READ-ONLY (no set accessor). You CANNOT edit item transform (Yaw/Scale/Position)
    programmatically on MP4. Item mode = inspect only.
  - `CGameCtnBlock.CoordX/Y/Z` (uint) and `Coord` (nat3) both exist; for math use
    `float(b.CoordX)` etc. `GetBlock` takes `int3`, NOT `nat3`.

