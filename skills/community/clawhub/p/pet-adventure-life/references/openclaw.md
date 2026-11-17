# OpenClaw Integration

Use `scripts/openclaw_adapter.py` as a thin JSON bridge. It keeps OpenClaw integration separate from the core engine so the same state files work in any agent environment.

## Actions

Supported actions:

- `init`
- `advance`
- `status`
- `call`
- `answer`
- `auto_resolve`

Example:

```bash
python scripts/openclaw_adapter.py advance --payload '{"workspace":"/Users/me/pet-world","offline":true}'
```

The adapter returns JSON. On success, `ok` is `true`. On failure, `ok` is `false` with an `error` string.

## Notifications

OpenClaw hosts can inspect `pending_calls` from the `status` action. If a notification channel is configured, send:

- call title
- urgency
- deadline if present
- message
- numbered choices

If no notification channel is available, do not fail. Let the pending call appear as a missed call on the next `status` or `advance`.

## Suggested Host Loop

1. Run `status`.
2. If `pending_calls` is non-empty, notify the user or show missed calls.
3. Run `advance` on the user's schedule.
4. If the user selects an option, run `answer`.
5. Run `auto_resolve` before sleeping or at startup to close expired urgent calls.

The host should not rewrite `state.json` directly.
