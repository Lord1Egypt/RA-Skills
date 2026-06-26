# Engine built-ins relevant to OpenClaw integration

This file summarizes the systems confirmed in the evaluated Unreal Engine source repository that should be reused before adding custom engine modifications.

## Remote Control

Paths:

- `Engine/Plugins/VirtualProduction/RemoteControl/`
- `Engine/Plugins/VirtualProduction/RemoteControlWebInterface/`
- `Engine/Plugins/Experimental/RemoteControlComponents/`

Use for:

- editor-side object/property/function control
- preset-based remote workflows
- external orchestration from OpenClaw

## HttpBlueprint

Path:

- `Engine/Plugins/Web/HttpBlueprint/`

Use for:

- Blueprint-first HTTP requests to OpenClaw endpoints
- low-code request/response prototypes

## JsonBlueprintUtilities

Path:

- `Engine/Plugins/JsonBlueprintUtilities/`

Use for:

- constructing and parsing JSON payloads in Blueprint
- reducing custom string-manipulation nodes

## PythonScriptPlugin

Path:

- `Engine/Plugins/Experimental/PythonScriptPlugin/`

Use for:

- editor automation
- batch content operations
- rapid scripting where C++ is overkill

## WebSockets runtime support

Paths:

- `Engine/Source/Runtime/Online/WebSockets/`
- `Engine/Plugins/Experimental/WebSocketMessaging/`
- `Engine/Plugins/Experimental/WebSocketNetworking/`

Use for:

- streaming events
- interactive assistant sessions
- progress notifications

## Design rule

Before adding a new OpenClaw Unreal feature, ask:

1. Can Remote Control already do this for editor-time work?
2. Can HttpBlueprint + JsonBlueprintUtilities already do this in Blueprints?
3. Would PythonScriptPlugin handle this faster for editor scripting?
4. Is a custom OpenClaw plugin still needed for auth, task protocol, session management, or runtime packaging?

Only add custom code for the parts not already solved by the engine.
