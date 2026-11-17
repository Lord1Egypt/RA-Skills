# MapForge — working plugin skeleton (built July 2026)

Full working example at `C:\Users\tomekdot\Openplanet4\Plugins\MapForge\`. Module-registry
architecture, deliberately different from Editor++ (no memory patching layer).

## File map

| File | Role |
|---|---|
| `info.toml` | metadata |
| `src/Main.as` | entry: Main() registers modules; RenderMenu() toggle; RenderInterface() gated by EditorContext.Refresh() |
| `src/Core/EditorContext.as` | null-safe gateway: App/Editor/Map/Cursor/PluginMapType handles; GetBlock/GetItem bounds-checked; RequestRefresh() = try AutoSave(); StripFormatCodes() helper |
| `src/Core/ModuleManager.as` | abstract `MFModule` (TabName/TabIcon/Render/Update) + registry rendering UI::BeginTabBar, each module's Render wrapped in try/catch |
| `src/Modules/BlockInspector.as` | filtered block list, coord/dir editing, recent-block quick access (copies block name to clipboard — `CursorBlockModel` has no value setter on MP4) |
| `src/Modules/ItemInspector.as` | AbsolutePositionInMap, Yaw/Pitch/Roll sliders (deg UI ↔ rad storage), Scale, live-refresh toggle |
| `src/Modules/CursorTools.as` | cursor Coord view/set clamped to Map.Size, reset to center, Dir rotate with 0..3 wraparound |
| `src/Modules/CheckpointTools.as` | scans blocks+items for WaypointSpecialProperty into a table; Order editing; group-link shared Order; renumber 1..N filtered by tag contains "checkpoint" |
| `src/Modules/Randomizer.as` | random item Yaw / position jitter / block Dir, name filter, position clamped to map bounds |
| `src/Modules/DevTools.as` | hidden fields (MobilIndex, IVariant, AnchorTreeId, BlockUnitCoord) + `ExploreNod(label, nod)` integration with Openplanet Nod Explorer |

## Key API details verified/used

- `CGameCtnBlock::ECardinalDirections(int)` cast for BlockDir; `CGameCursorBlock::ECardinalDir(int)` for cursor Dir.
- `it.ItemModel.CollectionId.GetName()`, `it.AnchorTreeId.GetName()` for MwId names.
- `map.EdChallengeId` = UID; `map.TMObjective_AuthorTime` (uint(-1) = unset).
- `Icons::` namespace for FontAwesome glyphs in labels; `##suffix` for unique ImGui IDs in loops.
- Openplanet UI wrappers return the new value (e.g. `m_filter = UI::InputText("label", m_filter)`), unlike raw ImGui out-params.

## Extension pattern

New feature = subclass MFModule + one `g_modules.Register(...)` line in Main(). All game access through EditorContext only.
