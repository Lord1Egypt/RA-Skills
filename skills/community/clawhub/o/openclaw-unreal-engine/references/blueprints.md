# Blueprint integration patterns

## Minimum Blueprint surface

In the evaluated engine repo, first consider whether built-in `HttpBlueprint` and `JsonBlueprintUtilities` already satisfy the workflow. Add custom OpenClaw nodes only for the parts the engine does not already model well, such as auth/session/task routing.

Expose these first when a custom plugin is still warranted:

- `Connect To OpenClaw`
- `Disconnect From OpenClaw`
- `Send Task Json`
- `Send Task Request`
- `Send Ping`
- `Get OpenClaw Connection Status`

This gives designers immediate utility without forcing a final typed schema too early.

## Recommended classes

### `UOpenClawBlueprintLibrary`

Use for static convenience nodes.

Good for:

- simple connect/disconnect helpers
- one-shot send helpers
- status queries

### `UOpenClawSubsystem : UGameInstanceSubsystem`

Use for persistent connection lifecycle.

Good for:

- maintaining endpoint/api key config
- storing connection state
- receiving async callbacks/events

### Dynamic multicast delegates

Use for Blueprint events:

- `OnConnected`
- `OnDisconnected`
- `OnTaskResult`
- `OnError`

## Data shape advice

Start with string JSON payloads rather than large typed structs unless the request contract is already stable.

Why:

- simpler across engine versions
- easier interop with OpenClaw and external services
- avoids large Blueprint/USTRUCT maintenance cost early on

Later, add typed wrappers for frequent operations.

## Runtime vs editor

Blueprint nodes in a runtime module can be used in PIE and packaged builds. Do not assume editor-only features are available there.

If the user wants Blueprint editing operations, route those through editor tools or Remote Control instead of pretending packaged Blueprint bytecode is directly editable in the same way.

## Sample usage flow

1. On game instance init, set endpoint and optional auth token.
2. Connect.
3. Send a JSON task envelope.
4. Receive completion via delegate.
5. Parse the response in Blueprint or pass to C++ helper parsing later.
