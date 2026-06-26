---
name: unreal-engine
description: Integrate OpenClaw with Unreal Engine 5.x projects, editors, and plugins. Use when an agent needs to inspect or scaffold Unreal Engine automation, create or modify UE5 C++ plugins, expose Blueprint-callable nodes, connect OpenClaw to the editor or a running game, drive editor-side tasks through Unreal Remote Control, or design/version-adapted workflows for Unreal Engine 5.0 and newer.
---

# Unreal Engine

## Overview

Use this skill to connect OpenClaw-style agent workflows to Unreal Engine 5.0+ in a way that survives engine minor-version differences. In the evaluated Unreal Engine source repo, built-in `RemoteControl`, `HttpBlueprint`, `JsonBlueprintUtilities`, `PythonScriptPlugin`, and `WebSockets` support are already present, so prefer composition over engine patching.

Prefer these integration paths:

1. **Editor automation path**: Use Unreal Remote Control for editor-time inspection and automation.
2. **Blueprint low-code path**: Compose `HttpBlueprint` + `JsonBlueprintUtilities` for Blueprint-driven request/response workflows.
3. **Project/plugin path**: Add a lightweight plugin that exposes OpenClaw-specific transport, auth, session, and task hooks to C++ and Blueprints.

Do not assume a single Unreal API surface works identically across all 5.x releases. Keep compile-time dependencies minimal and isolate version-sensitive code.

## Integration strategy

### 1. Pick the right control plane first

Choose based on the task:

- **Blueprint inspection, editor object/property changes, calling exposed editor functions, preset-driven tooling**
  - Prefer **Unreal Remote Control**.
  - Best for editor-time orchestration without deeply embedding agent logic into gameplay code.
- **Blueprint-first HTTP/JSON workflows without much C++**
  - Prefer built-in **HttpBlueprint** + **JsonBlueprintUtilities**.
  - Best for quick prototyping and designer-friendly task flows.
- **Editor automation where Python is a better fit than C++/Blueprint**
  - Prefer **PythonScriptPlugin**.
  - Best for content tooling, batch editor scripting, and rapid iteration.
- **Runtime communication from a packaged game or PIE session, Blueprint utility nodes, project-specific task execution, custom authentication/transport**
  - Prefer a **project plugin**.
- **Both editor-time and runtime tasks**
  - Use both: Remote Control for editor-side work, built-in Blueprint/Python tooling where appropriate, and a plugin for runtime-safe OpenClaw-specific behavior.

### 2. Keep version compatibility broad

For UE 5.0+

- Prefer engine modules with long-lived APIs: `Core`, `CoreUObject`, `Engine`, `HTTP`, `Json`, `JsonUtilities`, `WebSockets`.
- Wrap version-sensitive code behind helper functions or macros.
- Avoid depending on editor-only modules in runtime code.
- Split runtime/editor concerns into separate modules only if the task actually needs editor extensions.

### 3. Treat Blueprint support as a first-class requirement

When the user mentions Blueprints, do not stop at C++ plumbing. Provide:

- `UBlueprintFunctionLibrary` nodes for one-shot operations
- Optional `UGameInstanceSubsystem` or `UEngineSubsystem` for persistent connections/state
- Delegate/event surfaces for async results
- Simple JSON-in/JSON-out fallback nodes when typed schemas are not settled yet

## Default architecture

Use this mental model unless the project requires something else:

- **OpenClaw side**
  - Orchestrates tasks, optionally talks HTTP/WebSocket, can emit structured JSON task envelopes.
- **Unreal Editor**
  - Remote Control exposes editor-manageable objects/functions/properties.
- **Unreal plugin**
  - Provides Blueprint nodes and runtime transport.
  - Receives task envelopes, dispatches to Blueprint/C++ handlers, returns structured results.

## Task patterns

### Pattern A: Editor-time Blueprint and asset tasks

Use when the goal is to:

- inspect or tweak actors/components in the editor
- trigger exposed functions on editor utilities
- update properties on Remote Control presets
- support technical art / virtual production style workflows

Approach:

1. Ensure the project enables Unreal Remote Control.
2. Expose only the objects/functions/properties needed.
3. Have OpenClaw call the Remote Control HTTP/WebSocket API.
4. Keep destructive/editor-mutating actions explicit and scoped.

Good fit:

- level setup helpers
- virtual production controls
- editor utility actors/widgets
- batch property updates

### Pattern B: Runtime or gameplay-adjacent tasks

Use when the goal is to:

- connect a running client/editor session to OpenClaw
- send prompts/tasks/results over HTTP or WebSocket
- make tasks callable from Blueprints
- support packaged builds or PIE behavior

Approach:

1. Add a runtime plugin.
2. Put transport in a subsystem or manager UObject.
3. Expose simple Blueprint nodes.
4. Return structured results and explicit errors.

Good fit:

- AI-driven NPC tooling
- in-editor copilot panels backed by runtime-safe transport
- gameplay testing hooks
- diagnostics and telemetry bridges

## Workflow

Follow this sequence.

### Step 1: Identify the integration target

Determine:

- engine version or version range
- editor-only vs runtime vs both
- whether Blueprints must be supported directly
- transport needs: HTTP, WebSocket, local CLI bridge, or mixed
- whether packaged builds matter

If the source repository is not accessible, say so clearly and proceed with a standards-based scaffold.

### Step 2: Inspect the project structure

For an Unreal project, look for:

- `*.uproject`
- `Source/`
- `Plugins/`
- existing module `.Build.cs` files
- any existing editor utility widgets, subsystems, or automation scripts

If you are generating a new plugin, prefer placing it under `Plugins/<PluginName>/`.

### Step 3: Choose a plugin shape

Default to a **single runtime module** when possible.

Create extra modules only if needed:

- **Runtime module** for packaged/runtime-safe features
- **Editor module** only for details panels, menus, custom tabs, or editor-only APIs

### Step 4: Expose Blueprint surfaces

Minimum useful surface:

- Connect/disconnect node
- Send JSON task/request node
- Async result delegate or polling getter
- Availability/status node

If the schema is immature, prefer these stable nodes first:

- `ConnectToOpenClaw(Url, ApiKey)`
- `DisconnectFromOpenClaw()`
- `SendTaskJson(TaskJson)`
- `GetConnectionStatus()`

Then layer typed nodes later.

### Step 5: Keep JSON contracts explicit

Define small message envelopes like:

```json
{
  "id": "task-123",
  "type": "run_blueprint_task",
  "task": "summarize_scene",
  "payload": {
    "target": "/Game/Maps/TestMap"
  }
}
```

Return results like:

```json
{
  "id": "task-123",
  "ok": true,
  "result": {
    "summary": "..."
  },
  "error": null
}
```

Keep these envelopes version-neutral and avoid leaking Unreal internals into the protocol unless necessary.

### Step 6: Handle UE version differences conservatively

Prefer defensive code:

- Use minimal includes in headers.
- Put module-heavy includes in `.cpp` files.
- Avoid relying on newer helper APIs when older equivalents exist.
- Gate minor differences with `ENGINE_MAJOR_VERSION` / `ENGINE_MINOR_VERSION` checks when required.

## Blueprint guidance

When asked for “all types of tasks including blueprints,” interpret that as at least:

- Blueprint-callable connection nodes
- Blueprint-callable request/response nodes
- Blueprint events/delegates for async completion
- a sample actor/component/subsystem showing usage

Prefer these Unreal patterns:

- `UBlueprintFunctionLibrary` for stateless convenience methods
- `UGameInstanceSubsystem` for persistent connection lifecycle
- `DECLARE_DYNAMIC_MULTICAST_DELEGATE_*` for Blueprint events

Avoid over-engineering the first pass. A minimal plugin that compiles across 5.0+ beats a feature-rich plugin that only works on one minor version.

## Remote Control guidance

Use Remote Control when the task is fundamentally editor-side. Expect HTTP/WebSocket-based control of exposed properties and functions. Do not describe it as a packaged-game runtime automation layer unless the project specifically wires that up.

If the user asks to manipulate Blueprints broadly, separate the request into:

- **editing/inspecting Blueprint-owned objects in the editor** → Remote Control/editor tooling
- **calling Blueprint nodes at runtime** → plugin-exposed Blueprint library/subsystem

## Suggested repository deliverables

When scaffolding an Unreal integration, prefer these outputs:

- `references/architecture.md` — integration decisions and tradeoffs
- `references/blueprints.md` — Blueprint support patterns
- `assets/OpenClawUnrealPlugin/` — drop-in UE plugin scaffold
- optional script(s) to copy/install the plugin into a target UE project

## Validation checklist

Before claiming success, verify:

- plugin descriptor exists and names the module(s)
- `.Build.cs` includes required dependencies only
- public headers are minimal
- Blueprint node names are clear and async behavior is documented
- no editor-only module is required for runtime-only use
- version claims are phrased as “designed for UE 5.0+” unless actually compiled/tested across versions

## Resources

### references/

Read these when needed:

- `references/architecture.md` for integration choices and compatibility rules
- `references/blueprints.md` for Blueprint-facing API patterns
- `references/remote-control-notes.md` for editor automation guidance
- `references/openclaw-api-contract.md` for the default `/api/unreal/task` request/response schema
- `references/repo-evaluation-notes.md` for the verified target repo structure and integration implications
- `references/engine-builtins.md` for built-in Unreal systems to compose with before adding custom code
- `references/install-strategy.md` for engine-source vs project-plugin deployment choices
- `references/integration-map.md` for mapping OpenClaw tasks onto confirmed engine systems
- `references/sample-blueprint-flow.md` for built-in Blueprint HTTP/JSON wiring
- `references/sample-python-flow.md` for editor Python automation patterns
- `references/openclaw-server-notes.md` for the OpenClaw-side handler boundary
- `references/sample-uproject-plugin-config.md` for project-level plugin enablement
- `references/openclaw-server-handler-example.md` for a concrete `/api/unreal/task` handler sketch
- `references/remote-control-extension-points.md` for repo-observed Remote Control / WebRemoteControl source touchpoints
- `references/webremotecontrol-route-observations.md` for concrete route/request/response observations from the inspected engine branch

### scripts/

Use `scripts/install_plugin.sh` to copy the scaffold plugin into a target Unreal project.

### assets/

Use `assets/OpenClawUnrealPlugin/` as the drop-in plugin scaffold for UE 5.0+ projects.
