# Authorized loader-plugin integrations

Use a loader plugin only when the runtime owner permits mods or instrumentation
and the test is offline or otherwise explicitly authorized. Check the game
license, mod policy, anti-cheat policy, engine/runtime version, and exact loader
release before generating code.

## Choose a supported lane

| Lane | First supported host | Upstream | Default truth |
| --- | --- | --- | --- |
| BepInEx | Unity Mono on BepInEx 5 LTS | <https://github.com/BepInEx/BepInEx> | live attach, real time |
| UE4SS | Unreal Lua mod on UE4SS 3.x | <https://github.com/UE4SS-RE/RE-UE4SS> | live attach, real time |

BepInEx IL2CPP and UE4SS C++ templates are not generated yet. Do not silently
substitute them for the supported variants. Record the exact compatible
upstream tag in `deployment/loader.json`; never use `latest` in a reproducible
adapter.

## Preserve the loader boundary

The loader hosts reviewed game-semantic code inside the runtime. The learner
stays outside through authenticated, target-bound local IPC. The host must:

1. start a fresh logical GLR episode with `attach`, not claim a physical reset;
2. keep the action vocabulary empty until reviewed handlers exist;
3. reject unknown, stale, oversized, or excess queued commands;
4. apply mutations on the engine/game thread;
5. return authoritative post-state before advancing the GLR step; and
6. remove hooks and release owned state when closed or reloaded.

Reuse the engine-neutral provider contracts when the selected runtime can load
them: C# `IRuntimeProvider` for Unity Mono/BepInEx and C++
`glr::runtime_provider` for a reviewed native Unreal lane. The current
`glr-hostd` stdio conformance transport is not authenticated or target-bound and
therefore cannot yet satisfy this loader boundary by itself.

Do not add object dumpers, unrestricted reflection/object search, arbitrary Lua
or C# evaluation, generic function calls, process scanning, stealth loading,
anti-cheat bypasses, or credential access. A loader's upstream capabilities do
not become GLR action authority.

## Stage deployment without selecting a game for the agent

Run `vx run package-runtime` after the declared host artifact exists. The
generated packager validates only portable relative paths and writes a
checksummed payload under `.glr/exports/loader-packages/`. It does not discover, select, or modify
a game directory. An operator must choose the exact authorized target and
perform or approve installation separately.

For BepInEx, build the reviewed C# project against operator-provided
`BEPINEX_ROOT` and `GAME_MANAGED_ROOT` values. Never commit those values. For
UE4SS, stage the generated Lua mod as data and keep its action table deny-empty
until the adapter implementation and negative tests are reviewed.

## Validate

- Parse `runtime-integration.json` and prove every required capability.
- Verify `agent-interface.json` still denies unknown operations.
- Exercise queue overflow, stale episode/step, unknown action, failed
  postcondition, reload, and disconnect tests.
- Run synthetic conformance and the reproducible model-bundle smoke test.
- Treat actual loader startup and live-game behavior as a separate bounded
  acceptance gate.

Official references:

- <https://docs.bepinex.dev/master/articles/dev_guide/plugin_tutorial/index.html>
- <https://docs.ue4ss.com/dev/guides/creating-a-lua-mod.html>
- <https://docs.ue4ss.com/dev/lua-api/global-functions/executeingamethread.html>
