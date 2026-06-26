# Event Stream Protocol

This skill uses structured JSON-line stdout events.

## Rule

When event streaming is enabled, stdout is reserved for structured events only.

## Event Types

| Event | Meaning | Consumer action |
|---|---|---|
| `task_preview` | pre-execution summary | show planned task |
| `info` | stage or info update | show status update |
| `progress` | polling progress | update progress UI |
| `warning` | non-fatal issue | surface warning |
| `error` | fatal issue | stop and surface error |
| `prompt` | user decision required | ask user |
| `result` | final success payload | deliver result |

## OpenClaw Rule

Do not manually narrate progress while the script is running.

Use the event stream as the source of truth.

## Output Mode

Recommended:

```bash
IMA_STDOUT_MODE=events
```
