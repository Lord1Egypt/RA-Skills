# Static verification of .as sources (no compiler in workspace)

There is no offline AngelScript compiler — the only true compile happens in the
game runtime (Automation role greps `Openplanet.log`). When a Developer/Tester
role must verify a new module before the game is available, run this ad-hoc
static pass (Python, throwaway script in `%TEMP%` with a `hermes-verify-`
prefix; delete it after):

## HOW to query Openplanet4.json (the grep that "returns zero" is a false negative)

`Openplanet4.json` is a **single-line** file (no newlines), so line-based tools
(`read_file`, `grep -n`, ripgrep over "lines") misbehave. MORE IMPORTANTLY, the
DB contains **only game Nod-class reflection** under `ns.Game.<Class>.m[]`
(entries `n`=name, `t`=type) — plus an inherited parent pointer `p` on each
class. It does **NOT** enumerate the Openplanet script API: `IO::`, `UI::`,
`Time::`, `Path::`, `Json::`, `Icons::`, `Text::`, and globals like
`getExceptionInfo()` are Openplanet script namespaces that live in the engine,
not in this DB. So grepping the JSON for `UI::TextDisabled`,
`IO::FromUserGameFolder`, `getExceptionInfo`, `SetClipboard`, etc. returns
**zero matches BY DESIGN** — that is NOT evidence the member is missing.

✅ Correct, reliable procedure (Python, throwaway script):

```python
import json
db = json.load(open("<GameDir>/Openplanet4.json"))
game = db["ns"]["Game"]

# 1) confirm a class + member exist (handle inheritance via 'p')
def has_member(clsname, member, ns=game):
    cls = ns.get(clsname)
    while cls is not None:
        for m in cls.get("m", []):
            if m["n"] == member:
                return True, m.get("t")
        p = cls.get("p")          # parent class name, or absent
        cls = ns.get(p) if p else None
    return False, None

print(has_member("CGameEditorPluginMap", "SaveMap"))          # True, <type>
print(has_member("CGameCtnEditorFree", "PluginMapType"))      # walks up to
                                                              # CGameCtnEditorCommon
# 2) dump every member of a class (incl. inherited) for a quick eyeball:
def members_of(clsname, ns=game):
    out, cls = {}, ns.get(clsname)
    while cls is not None:
        for m in cls.get("m", []):
            out.setdefault(m["n"], m.get("t"))
        p = cls.get("p"); cls = ns.get(p) if p else None
    return out
```

Rule of thumb for the report:
- **Game-class native** (`CGameCtnChallenge.MapName`, `CGameEditorPluginMap.SaveMap`,
  `CGameCtnBlock.WaypointSpecialProperty`, editor `Challenge/Cursor/PluginMapType`
  via parent) → MUST be confirmed present in the JSON with this walk.
- **Script-namespace native** (`UI::ListBox`, `IO::IndexFolder`, `Time::Stamp`,
  `Json::ToFile`, `Icons::Save`, `getExceptionInfo()`) → confirmed against the
  trusted list / known Openplanet API, NOT against this DB. State explicitly in
  the report that the DB does not enumerate them so a zero-grep is expected.
- `Path`, `Time`, `Json`, `IO`, `UI`, `Text`, `Icons` are NOT top-level keys in
  the JSON (`"top-level keys: ['op','mp','ns']"`) — don't waste a turn grepping
  for them there.

## Checks that catch real MP4 breakage

1. **Balance**: count `{}`, `()`, `[]` — but only AFTER stripping string
   literals and comments, otherwise counts are wrong:
   ```python
   s = re.sub(r'\"(\\.|[^\"\\\\])*\"', '\"\"', code)
   s = re.sub(r'//.*', '', s)
   s = re.sub(r'/\\*.*?\\*/', '', s, flags=re.S)
   ```
2. **Banned-call scan on the comment-stripped text** — pitfall: scanning raw
   source gives false positives when the header comment says e.g.
   "(no UI::InputInt3)". Scan for real call forms with the open paren:
   `UI::InputInt3(`, `tostring(`, `char(`.
3. **Module-pattern conformance** (MapForge-style plugins): class derives the
   base module class, `TabName()/TabIcon()/Render()` carry `override`,
   `g_modules.Register(XModule());` present in `Main.as`.
4. **wstring wrap check**: any `.Name` of BlockModel/Map concatenated into a
   string should appear wrapped as `string(x.Name)`.
5. **Mutation safety**: every block-placing loop should show
   `CanPlaceBlock(` before `PlaceBlock(`, inside `try { } catch` with
   `getExceptionInfo()`.

Report the verdict honestly as "static verification only, final compile is the
game runtime's job" — never claim a clean compile you didn't run.

## Proven mutation pattern: grid/array replication of an existing block

Source block = block under `EditorContext.Cursor.Coord` (nat3) or a manual
coordinate; find it by iterating `Map.Blocks` and matching `CoordX/Y/Z` (uint).
Reuse `src.BlockModel` and `CGameEditorPluginMap::ECardinalDirections(int(src.BlockDir))`
instead of `GetBlockModelFromName`. Loop the grid, **skip the origin cell
(0,0,0)** so the source isn't double-placed, skip negative coords, gate each
`PlaceBlock` behind `CanPlaceBlock(model, int3, dir, true, 0)`, then call the
context's refresh (`PluginMapType.AutoSave()` guarded by try/catch). Working
example: `MapForge/src/Modules/ArrayMultiplier.as`.
