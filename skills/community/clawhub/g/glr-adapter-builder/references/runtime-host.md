# Runtime Host and provider SDK boundary

Use the Runtime Host to reuse protocol and lifecycle behavior, not to bypass an
engine's supported loading boundary.

## Current reusable pieces

- Rust `glr`: canonical standalone deployment and Agent control entrypoint. Its
  release archive carries the matching Runtime Host and both GLR Skills.
- Rust `glr-hostd`: strict `glr.host.v1`, serialized stdio, 1 MiB hard frame
  bound, episode/step fencing, synthetic conformance provider.
- Python `HostBridgeDriver`: explicit absolute executable, no shell, bounded
  response deadline, no mutating retry, child cleanup.
- C# `IRuntimeProvider`: .NET Standard 2.0 Unity/BepInEx-compatible semantic
  provider contract.
- C++ `glr::runtime_provider`: header-only C++20 Unreal/native semantic provider
  contract.

Run `vx just host-smoke` and `vx just provider-sdk-check` before adapting these
surfaces. Preserve flattened dot-separated tensor paths and little-endian GLR
v1 tensor bytes.

Run `glr --project . --json doctor` before using an existing adapter project.
Use the separate `glr-cli` Skill for training, capture, queries, knowledge
transfer, playback, or explicitly authorized `glr update` maintenance.

## Bootstrap choice

| Runtime access | Bootstrap | Provider contract |
| --- | --- | --- |
| Unity source | Official Unity plugin/assembly | C# `IRuntimeProvider` |
| Unreal source | Official Unreal Runtime Module | C++ `runtime_provider` |
| Unity Mono, authorized mods | Exact compatible BepInEx | C# `IRuntimeProvider` |
| Unreal, authorized mods | Exact compatible UE4SS or official SDK | C++ provider when native support is reviewed; Lua remains a bounded shim |
| External official API | Explicit external adapter | Python `BridgeDriver` or future Host provider transport |

Do not generate a universal injector, arbitrary dynamic-library path, process
scanner, reflection/object dumper, script evaluator, anti-cheat bypass, or
automatic installation step.

## Capability truth

`host-stdio` proves only one ordered local child-process session. It does not
prove authentication, OS process identity, exact game target binding, main
thread dispatch, physical reset, or live post-state. These capabilities belong
to a future authenticated local provider connection plus the specific engine
adapter and must fail closed until implemented and accepted live.
