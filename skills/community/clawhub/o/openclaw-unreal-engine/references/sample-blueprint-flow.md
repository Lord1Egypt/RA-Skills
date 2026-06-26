# Sample Blueprint flow

## Goal

Show the simplest repo-informed way to connect a Blueprint graph to OpenClaw using built-in engine plugins plus the custom OpenClaw plugin only where useful.

## Preferred low-code path

Enable:

- `HttpBlueprint`
- `JsonBlueprintUtilities`
- optional `OpenClawUnrealPlugin`

## Flow

1. Build a request JSON object.
2. Convert it to a JSON string.
3. Add headers, including Authorization if needed.
4. Send an HTTP request to `/api/unreal/task`.
5. Parse the response JSON.
6. Route success/error in Blueprint.

## Example envelope

```json
{
  "id": "bp-task-001",
  "type": "runtime.query.status",
  "task": "ping",
  "payload": {}
}
```

## Node-level outline

### Build request

Use `JsonBlueprintUtilities` nodes to:

- create/load a JSON object wrapper
- set fields:
  - `id`
  - `type`
  - `task`
  - `payload`
- convert object to string

### Add headers

Use `HttpBlueprint` header helpers to add:

- `Content-Type: application/json`
- `Authorization: Bearer <token>` if required

### Send request

Use the async HTTP request node from `HttpBlueprint`:

- URL: `http://<openclaw-host>/api/unreal/task`
- Verb: `POST`
- Body: request JSON string

### Handle response

On completion:

- inspect `bSuccessful`
- parse response JSON string with `JsonBlueprintUtilities`
- branch on `ok`
- read `result` or `error`

## Where the custom OpenClaw plugin helps

Add the plugin when you want to avoid rebuilding the same graph patterns repeatedly. It can provide:

- prebuilt connection/task nodes
- standard task envelope generation
- stable auth/session handling
- optional WebSocket event handling
