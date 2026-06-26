# WebRemoteControl route observations from the evaluated repo

## Observed route abstraction

`RemoteControlRoute.h` defines a route model with:

- route description text
- `FHttpPath`
- `EHttpServerRequestVerbs`
- `FHttpRequestHandler`

This confirms the WebRemoteControl layer is built around explicit route registration rather than ad-hoc request parsing everywhere.

## Observed request types

`RemoteControlRequest.h` includes concrete request wrappers such as:

- `FRCRequestWrapper`
- `FRCBatchRequest`
- `FRCCallRequest`
- `FRCObjectRequest`
- `FRCPresetSetPropertyRequest`
- `FRCPresetCallRequest`
- `FRemoteControlObjectEventHookRequest`

Important fields seen in request structures include:

- `ObjectPath`
- `FunctionName`
- `PropertyName`
- `GenerateTransaction`
- `Operation`

This is directly relevant to mapping OpenClaw task payloads onto Remote Control operations.

## Observed response types

`RemoteControlResponse.h` includes response structures for:

- API info / route listing
- preset listing and description
- object description
- asset search
- actor search
- metadata access
- event payloads

This suggests OpenClaw can often translate results instead of inventing an entirely separate editor-response schema.

## Observed editor routes

`WebRemoteControlEditorRoutes.cpp` registers editor-only routes such as:

- `/remote/object/event`
- `/remote/object/thumbnail`

The implementation shows:

- content-type validation
- request deserialization helpers
- route registration/unregistration patterns
- event dispatch integration using editor delegates

## Observed server behavior hints

`WebRemoteControl.cpp` shows:

- HTTP server module usage
- router/handler registration
- JSON struct serialization/deserialization backends
- command-line and console-variable gating such as `WebControl.EnableServerOnStartup`
- runtime/editor distinction via `RCWebControlEnable` and editor checks

## Practical implication for OpenClaw

OpenClaw should not treat Remote Control as a vague black box. The repo already contains:

- typed request/response models
- explicit route concepts
- editor-only route registration
- websocket handling

Therefore the cleanest OpenClaw integration is:

1. adapt OpenClaw envelopes to these concepts where useful
2. keep OpenClaw-specific auth/session/task semantics outside engine internals by default
3. only patch WebRemoteControl if you truly need new engine-level routes or behavior
