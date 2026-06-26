OpenClaw Unreal Plugin scaffold

Drop this folder into your Unreal project's Plugins/ directory as OpenClawUnrealPlugin, or use the install_plugin.sh helper from the sibling skill scripts directory.

What it provides:
- Runtime module for UE 5.0+
- Editor module scaffold for menu/tooling expansion
- UGameInstanceSubsystem for connection lifecycle
- Blueprint-callable accessor library
- HTTP-based SendTaskJson example
- richer request types and status enum scaffold
- WebSocket client scaffold for future streaming/events
- helper surface for building editor Remote Control task envelopes

Repo-informed note:
- the evaluated Unreal Engine source repo already includes RemoteControl, HttpBlueprint, JsonBlueprintUtilities, PythonScriptPlugin, and WebSockets support
- this plugin should stay thin and compose those built-ins rather than replacing them wholesale

Recommended next steps:
1. Install this as a project plugin first unless multiple projects truly need engine-wide deployment.
2. Enable built-in plugins needed for your workflow: RemoteControl, HttpBlueprint, JsonBlueprintUtilities, PythonScriptPlugin.
3. Build typed Blueprint nodes for your highest-value tasks.
4. Wire WebSocket events into Blueprint delegates if you need server push/progress updates.
5. Expand the editor module into tabs, menus, or Remote Control helpers for editor workflows.
6. Add approved Python task wrappers rather than exposing arbitrary remote script execution by default.
