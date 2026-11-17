# MP4 runtime (in-race) API + `Dev::` memory access — verified 2026-08

`references/mp4-api-verified.md` covers the **editor**. This file covers the
**playground / driving** side, which is what trainers, HUDs, telemetry and
save-state plugins need. All members below were read out of
`C:\Users\tomekdot\Openplanet4\Openplanet4.json` (game classes) and
`C:\Users\tomekdot\Openplanet4\OpenplanetCore.json` (built-ins).

## 1. Nod chain to the driving player

```
GetApp()                              -> CGameCtnApp
  .CurrentPlayground                  -> CGamePlayground
    .GameTerminals                    -> MwFastBuffer<CGameTerminal@>   (value type!)
    .GameTerminals[0].GUIPlayer       -> CGamePlayer   -> cast<CTrackManiaPlayer>
    .Players                          -> MwFastBuffer<CGamePlayer@>
  .GameScene                          -> CGameScene (parent CScene3d -> CScene)
    .MgrVehicleVis                    -> CSceneMgrVehicleVis  (.Impl, .CustomSkinModels)
  .RootMap                            -> CGameCtnChallenge
```

`CGamePlayer` itself exposes only `User : CGamePlayerInfo@` — you MUST cast to
`CTrackManiaPlayer` to get anything useful.

## 2. `CTrackManiaPlayer` (verified)

`ScriptAPI` (CTrackManiaScriptPlayer@), `Score`, `RaceState`
(`ERaceState`: BeforeStart / Running / Finished / Eliminated), `IsSpawned`,
`CurTriggerIndex` (int), `CurrentNbLaps`, `CurLapIndex`,
`CurCheckpointRaceTime`, `CurCheckpointLapTime`, `CurRaceContinuousRank`,
`Position` (vec3), `Distance`, `Speed`, `DisplaySpeed`, `NbRespawns`,
`AutoPilotEnabled`, `SpawnLoc` (**iso4**), `InOffZoneStartTime`.

## 3. `CTrackManiaScriptPlayer` — the telemetry goldmine (~120 members)

This is the single best source for a HUD or a recorder, and it needs **zero**
memory hacking. Verified members worth knowing:

- Timing: `RaceStartTime`, `LapStartTime`, `CurCheckpointRaceTime`,
  `CurCheckpointLapTime`, `CurTriggerIndex`, `CurRace` / `CurLap`
  (`CTmRaceResultNod@`).
- Transform-ish: `Position` (vec3), `AimDirection` (vec3), `AimYaw`, `AimPitch`,
  `Upwardness`.
- Motion: `Speed`, `DisplaySpeed`, `Distance`, `FlyingDistance`,
  `SkiddingDistance`, `FlyingDuration`, `SkiddingDuration`, `InWaterDuration`,
  `FreeWheelingDuration`.
- **Driver input**: `InputSteer` (float), `InputGasPedal` (float),
  `InputIsBraking` (bool).
- Drivetrain: `EngineRpm`, `EngineCurGear` (int), `EngineTurboRatio`,
  `WheelsContactCount`, `WheelsSkiddingCount`.
- Damage: `DamageHullRatio`, `DamageWindowRatio`.
- Whole stunt/bonus block: `Stunt*` (~25 members), `BonusMode*` (~15).
- Tweakables (writable-looking): `AccelCoef`, `ControlCoef`, `GravityCoef`,
  `MaxiAirControl`, `TinyCar`, `EnableStuntMode`, `JumpMode`.

## 4. Where reflection stops — `CSceneVehicleVis`

`ns.Scene.CSceneVehicleVis` exists in the DB but has **no `m[]` array** — only
`{"i":"A018000","s":3464}`. So the writable physics state (linear/angular
velocity, wheel state, full rotation matrix) has **no named members on MP4**.
`CSceneMgrVehicleVisImpl` only exposes `Extrapolation` and `HermiteInterp`.

Consequence: read-only telemetry = free via `ScriptAPI`; **writing** vehicle
state (true "flying respawn", teleport-with-velocity, freeze/slow-mo) requires
raw offsets into a 3464-byte object.

## 5. `Dev::` is fully available on this build

Confirmed present in `OpenplanetCore.json`:

- Offset reads on a nod: `Dev::GetOffsetInt8/16/32/64`,
  `GetOffsetUint8/16/32/64`, `GetOffsetFloat`, `GetOffsetDouble`,
  `GetOffsetVec2/3/4`, `GetOffsetInt2/3`, `GetOffsetNat2/3`,
  **`GetOffsetIso3` / `GetOffsetIso4`**, `GetOffsetNod`, `GetOffsetString`,
  plus generic `T Dev::Get<T>(const ?&in nod, uint offset)`.
- Offset writes: `Dev::SetOffset(nod, offset, v)` overloaded for every one of
  those types incl. `iso4` and `CMwNod@`, plus `Dev::Set<T>`.
- Absolute memory: `Dev::BaseAddress()`, `BaseAddressEnd()`,
  `FindPattern(pattern)`, `Patch(ptr, pattern)` (returns backup bytes),
  `Read*` / `Write*` and `SafeRead*` / `SafeWrite*` (safe = slower).
- Code hooks: `Dev::Hook(ptr, padding, funcName, pushRegisters, freeRegister)`
  / `Dev::Unhook(hook)`, `Dev::InterceptProc(className, procName, func)` /
  `ResetInterceptProc`. `Dev::Allocate(size, executable)` / `Free`.
- Note: `Dev::ReadUInt32`-style names (capital `I`) are **deprecated**; the
  live spelling is `Dev::ReadUint32`. Same for `SafeReadUint*`.

Also useful: `Reflection::GetType(name)`, `Reflection::TypeOf(nod)`,
`MwClassInfo.Members` / `.GetMember(name)`, `MwMemberInfo.Name` — enough to
build a runtime member browser inside the plugin.

## 6. Offset-hunting procedure (do this in-game, per build)

Offsets are **build-specific**. Never hardcode someone else's.

1. Resolve the target nod and confirm with `ExploreNod` / `Reflection::TypeOf`.
2. Build a debug panel that renders `Dev::GetOffsetFloat(nod, i)` and
   `Dev::GetOffsetVec3(nod, i)` for `i` in `0..objectSize` step 4, live.
3. Correlate while driving against known-good `ScriptAPI` values:
   - vec3 whose length tracks `ScriptAPI.Speed` -> linear velocity
   - iso4 whose translation equals `player.Position` -> world transform
   - float matching `EngineRpm`, int matching `EngineCurGear`
   - floats clamped to [-1,1] tracking `InputSteer` -> input block
4. Freeze findings into an `OffsetTable.as` **with a load-time self-check**:
   re-read the position offset and compare to `player.Position` within epsilon.
5. **Never `SetOffset` unless the self-check passed.** Fall back to read-only
   mode instead of writing garbage — a bad write into a physics object crashes
   the game, not just the plugin.

## 7. Dynamic checkpoints (no static CP list needed)

A trainer/split plugin should bucket by checkpoint **dynamically**:

- Live bucket key = `player.CurTriggerIndex` (increments as the driver actually
  crosses waypoints). Authoritative, needs no map parsing, works on any map.
- Total count / ordering: iterate `RootMap.Blocks` (and `AnchoredObjects`) for
  entries whose `WaypointSpecialProperty` is non-null; `CGameWaypointSpecialProperty`
  exposes `Tag` (string, e.g. `"Checkpoint"`) and `Order` (uint) — both verified.
- Detect a crossing in `Update()` by watching `CurTriggerIndex` increment or
  `CurCheckpointRaceTime` change.
- Multilap: make the key unique with `CurLapIndex * cpCount + CurTriggerIndex`,
  using `CurrentNbLaps` for bounds.

## 8. Persistence

There is **no** `IO::WriteFile` on this build. Use
`Json::ToFile(path, value, pretty)` / `Json::FromFile(path)` into
`IO::FromStorageFolder("<sub>/<key>.json")`, creating the folder with
`IO::CreateFolder(folder, true)` first. Map key: `RootMap.EdChallengeId`
(string, verified).
