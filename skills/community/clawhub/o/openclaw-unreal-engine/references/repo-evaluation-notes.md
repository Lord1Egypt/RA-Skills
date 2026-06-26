# Repo evaluation notes

## Verified repository identity

Authenticated inspection succeeded.

The target repository is a full Unreal Engine source distribution, not a game project. The checked branch is:

- `release`

Top-level structure includes:

- `Engine/`
- `Templates/`
- `Samples/`
- standard Unreal source build scripts (`Setup.*`, `GenerateProjectFiles.*`)

## Relevant engine capabilities already present

The repository already contains several built-in systems that materially affect the best OpenClaw integration strategy:

### Remote Control

Located under:

- `Engine/Plugins/VirtualProduction/RemoteControl/`
- `Engine/Plugins/VirtualProduction/RemoteControlWebInterface/`
- `Engine/Plugins/Experimental/RemoteControlComponents/`

Notable modules include:

- `RemoteControl`
- `WebRemoteControl`
- `RemoteControlUI`
- `RemoteControlLogic`

### Blueprint-friendly HTTP

Located under:

- `Engine/Plugins/Web/HttpBlueprint/`

### Blueprint-friendly JSON helpers

Located under:

- `Engine/Plugins/JsonBlueprintUtilities/`

### Python automation

Located under:

- `Engine/Plugins/Experimental/PythonScriptPlugin/`

This includes remote-execution and commandlet-related code paths.

### WebSocket support

Available in engine/runtime modules and experimental plugins:

- `Engine/Source/Runtime/Online/WebSockets/`
- `Engine/Plugins/Experimental/WebSocketMessaging/`
- `Engine/Plugins/Experimental/WebSocketNetworking/`

## Architectural conclusion

Because these engine capabilities already exist, the cleanest OpenClaw integration is **not** to deeply modify engine internals first.

Prefer this layering:

1. **Project/plugin layer** for OpenClaw-specific orchestration and UX
2. **Remote Control** for editor-side object/property/function automation
3. **HttpBlueprint + JsonBlueprintUtilities** for low-code Blueprint-side request/response flows
4. **PythonScriptPlugin** for editor automation and content tooling where Python is a better fit than custom C++
5. Optional custom runtime/editor plugin modules only where OpenClaw-specific state, auth, task routing, or UI is needed

## What changed in our design after real repo evaluation

Compared with a blind/generic UE5 scaffold:

- Remote Control is confirmed in-tree, so it should be treated as the default editor control plane.
- HttpBlueprint and JsonBlueprintUtilities are confirmed in-tree, so Blueprint support can lean on built-in engine plugins rather than custom JSON plumbing alone.
- PythonScriptPlugin is confirmed in-tree, so some OpenClaw tasks can be routed to Python-based editor scripting rather than only C++/Blueprint.
- WebSockets are confirmed in-tree, but a custom OpenClaw-specific wrapper/plugin is still useful for a stable task protocol and user-facing Blueprint nodes.

## Recommendation

Keep the OpenClaw Unreal plugin lightweight and compositional:

- expose OpenClaw-specific request/auth/session/task helpers
- integrate with built-in engine systems
- avoid patching engine source unless there is a clear engine-level need
