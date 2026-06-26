OpenClaw Unreal Plugin composition notes

This scaffold is intended to compose with Unreal Engine built-ins confirmed in the evaluated engine repo:
- RemoteControl
- HttpBlueprint
- JsonBlueprintUtilities
- PythonScriptPlugin
- WebSockets runtime support

Recommended deployment order:
1. Install as a project plugin.
2. Enable the built-in plugins your workflow needs.
3. Use Remote Control for editor-side automation.
4. Use HttpBlueprint + JsonBlueprintUtilities for Blueprint-first HTTP/JSON flows.
5. Add Python editor automation only for approved/editor-safe tasks.
6. Use the custom OpenClaw plugin layer for auth, task envelopes, session management, and runtime/editor glue.
