# Unreal Engine + OpenClaw architecture

## Goal

Connect OpenClaw to Unreal Engine 5.0+ for editor automation, Blueprint-accessible task execution, and runtime-safe transport without depending on a specific UE 5 minor release.

## Recommended split

### Editor-side automation

Use Unreal Remote Control when you need to:

- inspect/edit exposed properties
- call exposed functions on actors/objects
- drive editor workflows from an external agent

Why:

- avoids intrusive engine/plugin changes for editor-only use
- lines up with Epic's intended remote automation path
- maps well to JSON/HTTP/WebSocket orchestration

### Runtime-side integration

Use a project plugin when you need to:

- communicate during PIE or packaged runtime
- expose Blueprint nodes
- manage connection state inside the game/editor runtime
- add project-specific logic or security controls

## Default plugin shape

Start with one runtime module:

- `OpenClawUnreal`

Add an editor module only if you later need custom editor tabs, toolbar buttons, details panels, or editor-only APIs.

## Transport choices

### HTTP

Pros:

- simplest to debug
- request/response fits many task patterns
- available through UE's built-in HTTP module

Cons:

- no native push channel without polling

Use for:

- one-shot tasks
- health checks
- command submission

### WebSocket

Pros:

- supports bidirectional real-time events
- good for streaming task progress or agent notifications

Cons:

- connection lifecycle is more complex
- can be less consistent across environments if not carefully managed

Use for:

- long-lived assistant sessions
- event streaming
- interactive copilot-style experiences

### Mixed

Often best:

- HTTP for task submission
- WebSocket for events/progress

## Compatibility rules for UE 5.0+

- keep public headers light
- include heavy engine/networking headers in `.cpp`
- avoid using APIs introduced only in later 5.x minors when older patterns exist
- prefer `FString` / JSON string payloads at boundaries when typed protocol stability is uncertain
- separate runtime-safe code from editor-only logic

## OpenClaw task model

A small neutral envelope works best:

```json
{
  "id": "uuid",
  "type": "task-type",
  "task": "task-name",
  "payload": {}
}
```

Suggested task categories:

- `editor.remote_control.call`
- `editor.remote_control.set_property`
- `runtime.blueprint.invoke`
- `runtime.query.status`
- `runtime.content.inspect`

## Security notes

- do not ship hard-coded API keys in plugin defaults
- keep remote endpoints configurable in project settings or Blueprint init
- treat remote mutation as opt-in
- restrict editor-destructive operations behind explicit user control

## Practical recommendation

After evaluating the target repository, prefer a compositional design over engine patching.

For first delivery, ship:

1. a reusable skill that explains both paths
2. a lightweight plugin with OpenClaw-specific Blueprint nodes and HTTP/WebSocket support
3. a sample JSON protocol
4. an installer script that copies the plugin into `Plugins/`
5. explicit guidance for composing with built-in engine plugins already present in the evaluated repo:
   - `RemoteControl`
   - `HttpBlueprint`
   - `JsonBlueprintUtilities`
   - `PythonScriptPlugin`
