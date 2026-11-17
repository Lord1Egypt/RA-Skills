# BlockableInputCallbacks (BIC) on ManiaPlanet 4 — verified facts (2026-08)

The `ackepta/BlockableInputCallbacks` optimizer (already shipped as
`Plugins/BlockableInputCallbacks.op`, siteid 893, v0.1.0) is the input layer used
by trainers (e.g. `TrackmaniaTrainer`). Facts verified by unpacking the `.op`
(zip) before using it:

## manifest shape (uses `[script]` module/exports, NOT `dependencies`)
```toml
[meta]
name = "BlockableInputCallbacks"
author = "achepta"
version = "0.1.0"
siteid = 893

[script]
module = "BlockableInputCallbacks"
exports = [ "Export.as" ]
shared_exports = [ "Shared.as" ]
```
Dependency plugin window: a plugin that imports it writes
`[script] dependencies = ["BlockableInputCallbacks"]` in ITS info.toml.

## import surface (Export.as)
```angelscript
namespace BlockableInputCallbacks {
    import int RegisterCallback(const string &in name, IInputCallback@ callback) from "BlockableInputCallbacks";
    import int RegisterCallback(const string &in name, IInputCallback@ callback, float activationThreshold) from "BlockableInputCallbacks";
    import void UnregisterCallback(int id) from "BlockableInputCallbacks";
    import void UnregisterCallbacks(const string &in name) from "BlockableInputCallbacks";
    import void SetInputBlocked(PadInput input, bool blocked) from "BlockableInputCallbacks";
    import void SetInputBlocked(KeyboardInput input, bool blocked) from "BlockableInputCallbacks";
    import KeyboardInput VirtualKeyToKeyboardInput(VirtualKey key) from "BlockableInputCallbacks";
    import VirtualKey KeyboardInputToVirtualKey(KeyboardInput input) from "BlockableInputCallbacks";
}
```

## verified enum values (Shared.as)
- `PadInput`: `None = 255`, then per-pad buttons.
- `KeyboardInput`: `None = 0x00`; function keys **F5 = 0x3F, F6 = 0x40, F8 = 0x42**
  (F7 = 0x41 by sequence).
- `InputDecision`, `PadInputEvent` shared enums — usable in the importing plugin.

## pitfalls
- Do NOT assume TM2020's REML can't bind F5/F6/F8 the same way: verify the enum
  against `Shared.as` in THIS plugin's `.op` before relying on it (values above
  are for v0.1.0).
- The callbacks are into-game with a `IInputCallback@` interface — if the plugin
  is missing from `Plugins/` at runtime the import fails the whole plugin pencil.
- Simpler zero-dependency fallback for a trainer: plain `OnKeyPress(bool down,
  VirtualKey key)` with `[Setting hidden] VirtualKey` — no BIC needed unless the
  key must also be BLOCKED from reaching the game.