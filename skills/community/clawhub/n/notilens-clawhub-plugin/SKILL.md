---
name: notilens
description: Send real-time alerts to NotiLens from any script, app, or AI agent — task lifecycle events, errors, completions, and metric tracking.
version: 0.2.0
metadata:
  openclaw:
    requires:
      env:
        - NOTILENS_TOKEN
        - NOTILENS_SECRET
    primaryEnv: NOTILENS_TOKEN
    emoji: "🔔"
    homepage: https://www.notilens.com
---

# NotiLens Plugin for OpenClaw

This is a **code plugin** — all functions are callable directly by the agent at runtime. No curl needed.

Get your `NOTILENS_TOKEN` and `NOTILENS_SECRET` from your topic settings at https://www.notilens.com.

## Available Functions

### `notify(name, event, message, options?)`
Send a notification. Title is auto-generated from `name + event`. Options: `type`, `image_url`, `open_url`, `download_url`, `tags`, `meta`.

### `track(name, event, message, type?, meta?)`
Track any custom event (e.g. `order.placed`, `deploy.started`). Title is auto-generated.

### `taskStarted(name, taskId, message?, meta?)`
Fire `task.started` when execution begins.

### `taskProgress(name, taskId, message, meta?)`
Fire `task.progress` at meaningful checkpoints.

### `taskCompleted(name, taskId, message, meta?)`
Fire `task.completed` when a task finishes successfully. Include `total_duration_ms`, `active_ms`, and custom metrics in `meta`.

### `taskFailed(name, taskId, message, meta?)`
Fire `task.failed` when a task fails. Automatically sets `is_actionable: true`.

### `taskError(name, taskId, message, meta?)`
Fire `task.error` for non-fatal errors (task continues).

### `taskRetry(name, taskId, retryCount, meta?)`
Fire `task.retry` when retrying. Pass the current retry number (1-based).

### `taskLoop(name, taskId, message, loopCount, meta?)`
Fire `task.loop` when the same step is repeating. Pass the current loop count.

### `inputRequired(name, message, openUrl?, meta?)`
Fire `input.required` when a human decision is needed. Automatically sets `is_actionable: true`.

## Recommended `meta` Fields

| Key                | Description |
|--------------------|-------------|
| `run_id`           | Unique run ID — format `run_{unix_ms}_{hex4}` |
| `total_duration_ms`| Wall-clock time from task start to now |
| `active_ms`        | Active time (excludes pauses/waits) |
| `retry_count`      | Number of retries so far |
| `error_count`      | Number of non-fatal errors |
| `loop_count`       | Number of loop iterations |
| `last_error`       | Last error message string |

## Configuration

```
NOTILENS_TOKEN=your_topic_token
NOTILENS_SECRET=your_topic_secret
```

Both are found in your topic settings at https://www.notilens.com.
