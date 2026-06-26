# Remote Control / WebRemoteControl extension points

Based on the evaluated engine repo, useful source areas include:

## Remote Control plugin descriptor and modules

- `Engine/Plugins/VirtualProduction/RemoteControl/RemoteControl.uplugin`
- `Source/RemoteControl`
- `Source/RemoteControlLogic`
- `Source/RemoteControlUI`
- `Source/WebRemoteControl`

## WebRemoteControl source areas

Observed files include:

- `WebRemoteControl.cpp`
- `WebRemoteControlEditorRoutes.cpp`
- `RemoteControlRequest.h`
- `RemoteControlResponse.h`
- `RemoteControlRoute.h`
- `WebSocketMessageHandler.cpp`
- `RemoteControlWebSocketServer.cpp`
- `WebRemoteControlUtils.h`

## Practical extension interpretation

These source areas suggest the Remote Control stack already has:

- request/response abstractions
- route registration concepts
- editor-specific routes
- websocket message handling

Observed request structures include fields such as `ObjectPath`, `FunctionName`, `PropertyName`, `GenerateTransaction`, and property-modification operations. That makes it straightforward to map OpenClaw task payloads onto existing Remote Control concepts rather than inventing a parallel editor mutation vocabulary.

## What to build on top

OpenClaw should usually extend at a plugin/application layer by:

- producing Remote Control-compatible requests
- routing OpenClaw task envelopes into Remote Control operations
- adding editor UX around approved actions

Avoid modifying these engine internals first unless:

- you need new route behavior impossible to achieve externally
- you need engine-level hooks or authorization changes inside WebRemoteControl itself
- performance or schema constraints force deeper integration
