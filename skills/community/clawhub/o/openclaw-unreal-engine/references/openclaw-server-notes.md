# OpenClaw server notes for Unreal integration

## Endpoint

Default example endpoint:

- `POST /api/unreal/task`

## Suggested responsibilities

The OpenClaw-side handler should:

- authenticate requests
- validate the task envelope
- route by `type` and `task`
- return compact JSON
- optionally emit progress events over WebSocket

## Suggested routing table

- `runtime.query.status` -> status/ping handlers
- `runtime.blueprint.invoke` -> project-defined runtime task handlers
- `editor.remote_control.call` -> Remote Control bridge handlers
- `editor.remote_control.set_property` -> Remote Control bridge handlers
- `editor.asset.query` -> editor query handlers

## Keep boundaries clear

OpenClaw should orchestrate and reason.
Unreal should execute engine/editor/game-specific actions.

Do not put all business logic into Unreal if it belongs in the external orchestrator.
Do not put all engine mutation logic into OpenClaw if it requires in-editor context.
