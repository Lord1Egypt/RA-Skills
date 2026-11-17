# MP4 trainer: verified nod chain + module scaffold

Session-verified reference for building an in-race trainer/HUD on ManiaPlanet 4
(rewrite of the TM2020 `TrackmaniaTrainer` native-DLL plugin). Everything here
was confirmed against `Openplanet4.json` on a live install — no guesses.

## 1. Nod chain (RaceContext gateway)

```
GetApp()                                  -> CGameCtnApp
  .CurrentPlayground                      -> CGamePlayground@
    .GameTerminals                        -> MwFastBuffer<CGameTerminal@>  (VALUE type)
    .GameTerminals[0].GUIPlayer           -> CGamePlayer@   (MUST cast)
      cast<CTrackManiaPlayer>(...)        -> CTrackManiaPlayer@
        .ScriptAPI                        -> CTrackManiaScriptPlayer@
  .RootMap                                -> CGameCtnChallenge@
```

Rules:
- `MwFastBuffer` is a **value type** — bound-check `Length`, never null-check.
- `CGamePlayer` exposes almost nothing; the cast to `CTrackManiaPlayer` is
  mandatory before any telemetry.
- Re-resolve the whole chain **every frame** in a `Refresh()` that returns
  `bool`; modules only run when it returned true.

## 2. Verified members (41 confirmed present)

`CTrackManiaPlayer`:

| member | type |
|---|---|
| `IsSpawned` | bool |
| `RaceState` | `CTrackManiaPlayer::ERaceState` |
| `Position` | vec3 |
| `Speed` | float |
| `SpawnLoc` | iso4 |
| `CurCheckpointRaceTime` | uint |
| `CurTriggerIndex` | int |
| `CurLapIndex` | uint |
| `CurrentNbLaps` | uint |
| `NbRespawns` | uint |
| `ScriptAPI` | `CTrackManiaScriptPlayer@` |

`ERaceState` values: `BeforeStart`, `Running`, `Finished`, `Eliminated`
(use as `CTrackManiaPlayer::ERaceState::Running`).

`CTrackManiaScriptPlayer` (rich telemetry): `Speed` float, `DisplaySpeed` uint
(km/h), `Distance` float, `EngineRpm` float, `EngineCurGear` int,
`EngineTurboRatio` float, `WheelsContactCount` uint, `WheelsSkiddingCount` uint,
`InputSteer` float, `InputGasPedal` float, `InputIsBraking` bool,
`FlyingDuration` uint, `SkiddingDuration` uint, `Upwardness` float,
`AimYaw` float, `AimPitch` float.

Map / geometry: `CGameCtnApp.CurrentPlayground`, `.RootMap`;
`CGamePlayground.GameTerminals`; `CGameTerminal.GUIPlayer`;
`CGameCtnChallenge.MapName` (**wstring** — wrap in `string(...)`),
`.EdChallengeId` (string, use as the per-map persistence key), `.Blocks`,
`.AnchoredObjects`; `CGameCtnBlock.Coord` (nat3), `.WaypointSpecialProperty`;
`CGameCtnAnchoredObject.BlockUnitCoord` (nat3), `.WaypointSpecialProperty`.

## 3. Checkpoints — the waypoint class lives in `GameData`, not `Game`

`ns.Game.CGameWaypointSpecialProperty` does **not** exist. The real path is
`ns.GameData.CGameWaypointSpecialProperty`, with exactly two useful members:

| member | type |
|---|---|
| `Tag` | string (`"Checkpoint"`, `"Finish"`, `"Start"`, `"StartFinish"`, ...) |
| `Order` | uint |

When a class lookup fails, walk the whole `ns` tree for the name before
concluding it is absent — several game classes sit under `GameData`, `Scene`,
or `TrackMania` rather than `Game`.

## 4. Dynamic checkpoint pattern (primary) + static scan (fallback)

**Primary — live, no map parsing.** `CurTriggerIndex` increments as the driver
*actually* crosses a waypoint. Track it in `Update()`:

```angelscript
int trigger = ctx.TriggerIndex();
uint lap    = ctx.LapIndex();
if (trigger < m_lastTrigger || lap < m_lastLap) Reset();   // restart detected
if (trigger > m_lastTrigger) {                              // crossing
    m_crossCount++;
    m_splits.InsertLast(ctx.RaceTime());
}
m_lastTrigger = trigger; m_lastLap = lap;
```

Multilap bucket key, unique across laps:
`bucket = int(LapIndex * max(cpCount,1)) + TriggerIndex` (`-1` before the first CP).

This works on maps with zero checkpoints and needs no precomputed table.

**Fallback — static scan.** Iterate `Map.Blocks` and `Map.AnchoredObjects`,
keep entries whose `WaypointSpecialProperty` is non-null, count those whose
`Tag` contains `"Checkpoint"` (case-insensitively — MP4 has no
`string::ToLower`, use a byte-compare helper). Use it for the "CP 3 / 7"
display and as the documented fallback if `CurTriggerIndex` ever misbehaves on
a given title pack. Cache the scan keyed on `EdChallengeId`.

## 5. Module scaffold that compiles on MP4

The MapForge editor layout ports cleanly to in-race work — rename the gateway
and keep everything else:

```
Plugins/<name>/
├── info.toml                 # [meta] name/author/category/version + [script] timeout
└── src/
    ├── Main.as               # Main(), RenderMenu(), RenderInterface(), Update(dt), OnDestroyed()
    ├── Core/
    │   ├── RaceContext.as    # nod chain + string/number helpers
    │   └── ModuleManager.as  # abstract TRModule + registry + tab rendering
    └── Modules/
        ├── Telemetry.as      # read-only proof the chain resolves
        └── Checkpoints.as    # dynamic tracking + static scan
```

Key details:
- `Update(float dt)` is a top-level plugin callback and runs even when the
  window is hidden — put tracking there, not in `Render`, or you lose crossings
  whenever the user closes the UI.
- `RenderInterface()` for the main window; `RenderMenu()` for the plugins menu.
- Wrap each module's `Render`/`Update` in try/catch so one bad module cannot
  take the plugin down.
- `UI::BeginTabBar(id)` takes the id only. Tab bodies go in `UI::BeginChild`.
- Helpers every MP4 plugin needs: `I2S(uint)` / `SI2S(int)` via
  `Text::Format("%d", ...)`, `F2S`/`F2S2` for floats, `LCByte(uint)` for
  lowercase, `ContainsCI` for case-insensitive search, `StripFormatCodes` for
  `$`-coded names.

## 6. Build order that de-risks the project

1. Scaffold + empty `Main.as` — prove it loads.
2. Telemetry tab (read-only) — **ask the user to confirm the numbers move while
   driving**. This single test validates the entire nod chain; everything else
   depends on it.
3. Dynamic checkpoint tracking (still read-only).
4. Clip store + hotkeys.
5. Tier-1 teleport restore (`Position` / `SpawnLoc`, no memory writes).
6. Tier-2 velocity restore via `Dev::SetOffset`, behind a self-check.
