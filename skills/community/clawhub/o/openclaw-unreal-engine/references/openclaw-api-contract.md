# OpenClaw `/api/unreal/task` contract

## Goal

Provide a small, explicit HTTP contract between Unreal and OpenClaw that works for editor or runtime-originated requests.

## Endpoint

- Method: `POST`
- Path: `/api/unreal/task`
- Content-Type: `application/json`
- Auth: `Authorization: Bearer <token>` when configured

## Request envelope

```json
{
  "id": "a4fdc7f5-9f0a-4f3e-b4b8-5a43f5fef001",
  "source": {
    "kind": "unreal",
    "engineVersion": "5.3.2",
    "project": "MyGame",
    "level": "/Game/Maps/TestMap",
    "mode": "editor"
  },
  "type": "runtime.query.status",
  "task": "ping",
  "payload": {}
}
```

## Response envelope

```json
{
  "id": "a4fdc7f5-9f0a-4f3e-b4b8-5a43f5fef001",
  "ok": true,
  "result": {
    "message": "pong"
  },
  "error": null,
  "meta": {
    "handledBy": "openclaw",
    "timestamp": "2026-03-30T13:00:00Z"
  }
}
```

## Error shape

```json
{
  "id": "a4fdc7f5-9f0a-4f3e-b4b8-5a43f5fef001",
  "ok": false,
  "result": null,
  "error": {
    "code": "invalid_task",
    "message": "Unknown task type runtime.foo.bar"
  },
  "meta": {
    "handledBy": "openclaw",
    "timestamp": "2026-03-30T13:00:00Z"
  }
}
```

## Suggested task types

### Runtime-safe

- `runtime.query.status`
- `runtime.content.inspect`
- `runtime.blueprint.invoke`
- `runtime.telemetry.push`

### Editor-oriented

- `editor.remote_control.call`
- `editor.remote_control.set_property`
- `editor.asset.query`

## Example: invoke a Blueprint-facing gameplay task

Request:

```json
{
  "id": "task-42",
  "source": {
    "kind": "unreal",
    "engineVersion": "5.2.1",
    "project": "ActionPrototype",
    "mode": "pie"
  },
  "type": "runtime.blueprint.invoke",
  "task": "spawn_test_enemy",
  "payload": {
    "class": "/Game/BP/BP_TestEnemy.BP_TestEnemy_C",
    "count": 3,
    "location": { "x": 0, "y": 0, "z": 120 }
  }
}
```

Response:

```json
{
  "id": "task-42",
  "ok": true,
  "result": {
    "spawned": 3
  },
  "error": null,
  "meta": {
    "handledBy": "openclaw"
  }
}
```

## WebSocket event shape

When streaming progress/events, use the same `id` and keep the message small:

```json
{
  "id": "task-42",
  "event": "progress",
  "progress": 0.5,
  "message": "Halfway done"
}
```

Completion:

```json
{
  "id": "task-42",
  "event": "completed",
  "ok": true,
  "result": {
    "spawned": 3
  }
}
```
