# Install strategy: engine source vs project plugin

## Recommendation

Prefer installing the OpenClaw integration as a **project plugin** by default, even when working from an engine source checkout.

Why:

- isolates OpenClaw-specific code from engine updates
- keeps the Unreal engine fork cleaner
- makes it easier to version the integration per game/project
- avoids unnecessary merge pain when updating engine branches

## Use project plugin when

- the integration is specific to one game/project
- you want safer upgrades across UE 5.x
- you mainly need Blueprint nodes, task routing, auth, or UI helpers
- you are composing built-in engine plugins like Remote Control, HttpBlueprint, and JsonBlueprintUtilities

Install location:

- `<ProjectRoot>/Plugins/OpenClawUnrealPlugin/`

## Use engine plugin when

- multiple projects on the same engine fork must share the exact same integration
- you are building organization-wide tooling on top of a custom engine distribution
- you have a real reason to make the plugin available engine-wide

Install location:

- `<EngineRoot>/Engine/Plugins/OpenClaw/OpenClawUnrealPlugin/`

## Avoid patching engine source unless

- you need a new engine-level hook not available through plugin APIs
- you need to modify Remote Control or WebRemoteControl internals directly
- you need changes that cannot be distributed as a plugin module

## Built-in plugin dependencies to enable

Depending on the workflow, enable some or all of:

- `RemoteControl`
- `HttpBlueprint`
- `JsonBlueprintUtilities`
- `PythonScriptPlugin`

## Suggested default rollout

1. install OpenClaw as a project plugin
2. enable built-in engine plugins as needed
3. validate editor-time automation via Remote Control
4. validate Blueprint HTTP/JSON flows
5. add Python-based editor tooling only where it clearly helps
6. promote to engine plugin only if multiple projects truly need shared deployment
