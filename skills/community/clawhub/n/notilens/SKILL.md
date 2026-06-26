---
name: notilens
description: Send real-time alerts to NotiLens from any script, app, or AI agent — task lifecycle events, errors, completions, metric tracking, and custom alerts.
version: 0.2.0
metadata:
  openclaw:
    requires:
      env:
        - NOTILENS_TOKEN
        - NOTILENS_SECRET
      bins:
        - curl
    primaryEnv: NOTILENS_TOKEN
    emoji: "🔔"
    homepage: https://www.notilens.com
---

# NotiLens — Real-time Alerts

NotiLens delivers real-time push notifications to your phone or team when tasks start, make progress, hit errors, or finish. No polling — instant alerts.

Get your `NOTILENS_TOKEN` and `NOTILENS_SECRET` from your topic settings at https://www.notilens.com.

## Sending a Notification

All notifications are sent as a POST to the NotiLens webhook:

```
POST https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send
X-NOTILENS-KEY: $NOTILENS_SECRET
Content-Type: application/json
```

### Payload Fields

| Field           | Type    | Required | Description |
|-----------------|---------|----------|-------------|
| `event`         | string  | yes      | Event name, e.g. `task.started`, `task.completed` |
| `title`         | string  | yes      | Short heading shown on the notification |
| `message`       | string  | yes      | Notification body text |
| `type`          | string  | yes      | `info` \| `success` \| `warning` \| `urgent` |
| `agent`         | string  | yes      | Name identifying the source (app, script, agent, etc.) |
| `task_id`       | string  | no       | Task label for grouping related events |
| `run_id`        | string  | no       | Unique ID for this specific run, e.g. `run_1714000000000_a3f2` |
| `is_actionable` | boolean | no       | Set `true` when the event needs human attention |
| `image_url`     | string  | no       | Image to display with the notification |
| `open_url`      | string  | no       | URL to open when the notification is tapped |
| `download_url`  | string  | no       | URL of a file to attach to the notification |
| `tags`          | string  | no       | Comma-separated tags, e.g. `prod,backend` |
| `ts`            | number  | no       | Unix timestamp (seconds). Defaults to now. |
| `meta`          | object  | no       | Metrics, counters, timing, and any custom key-value pairs |

## Standard Events and When to Fire Them

Use these canonical event names for consistency across sources:

| Event              | `type`    | When to fire |
|--------------------|-----------|--------------|
| `task.queued`      | `info`    | Task is queued before a worker picks it up |
| `task.started`     | `info`    | Execution begins |
| `task.progress`    | `info`    | Meaningful checkpoint during a long task |
| `task.paused`      | `warning` | Task is pausing (waiting on I/O, rate limit, etc.) |
| `task.waiting`     | `warning` | Task is blocked waiting for an external resource |
| `task.resumed`     | `info`    | Task resumed after a pause or wait |
| `task.loop`        | `warning` | Same step is repeating — possible loop |
| `task.retry`       | `warning` | Task is being retried after a failure |
| `task.error`       | `urgent`  | Non-fatal error occurred, task continues |
| `task.completed`   | `success` | Task finished successfully |
| `task.failed`      | `urgent`  | Task failed — will not be retried |
| `task.timeout`     | `urgent`  | Task exceeded its time limit |
| `task.cancelled`   | `warning` | Task was cancelled before completion |
| `task.stopped`     | `info`    | Task was stopped intentionally (not an error) |
| `task.terminated`  | `urgent`  | Task was forcibly terminated |
| `input.required`   | `warning` | Needs human input to continue |
| `input.approved`   | `success` | Human approved the request |
| `input.rejected`   | `warning` | Human rejected the request |
| `output.generated` | `success` | Output produced (file, report, result, etc.) |
| `output.failed`    | `urgent`  | Failed to produce expected output |

You may also use any custom event name appropriate to your workflow (e.g. `order.placed`, `deploy.started`, `pipeline.complete`).

## Metric Tracking

Attach numeric or string metrics to any event's `meta` object. NotiLens surfaces these in the dashboard for filtering and analytics.

### Recommended `meta` Fields

**Timing** (milliseconds):

| Key                  | Description |
|----------------------|-------------|
| `total_duration_ms`  | Wall-clock time from task start to now |
| `active_ms`          | Time actively running (excludes pauses and waits) |
| `queue_ms`           | Time spent in queue before task started |
| `pause_ms`           | Total time spent paused |
| `wait_ms`            | Total time spent waiting on external resources |

**Counters**:

| Key            | Description |
|----------------|-------------|
| `retry_count`  | Number of retries so far |
| `loop_count`   | Number of loop iterations |
| `error_count`  | Number of non-fatal errors encountered |
| `pause_count`  | Number of times the task paused |
| `wait_count`   | Number of times the task waited |

**Custom metrics** — include any domain-specific values:

```json
"meta": {
  "rows_processed": 4218,
  "rows_failed": 3,
  "tokens_used": 18400,
  "model": "claude-opus-4-6",
  "env": "production",
  "region": "us-east-1"
}
```

Numeric metrics accumulate meaningfully when charted over time. Include them on `task.completed` and `task.failed` events at minimum.

### `run_id` — Unique Run Identification

Generate a `run_id` at the start of each task run and include it on every event for that run. This allows NotiLens to correlate all events from the same execution even if `task_id` is reused across runs.

```
run_id format: run_{unix_ms}_{random_hex4}
example:       run_1714000000000_a3f2
```

## Loop Detection

Fire `task.loop` when the same step is repeating. Include the loop count in `meta`.

```bash
curl -s -X POST "https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send" \
  -H "Content-Type: application/json" \
  -H "X-NOTILENS-KEY: $NOTILENS_SECRET" \
  -d '{
    "event": "task.loop",
    "title": "my-app | scraper | task.loop",
    "message": "Same page returned 5 times — possible infinite loop.",
    "type": "warning",
    "agent": "my-app",
    "task_id": "scraper",
    "run_id": "run_1714000000000_a3f2",
    "is_actionable": true,
    "meta": {
      "loop_count": 5
    }
  }'
```

## Examples

### Full task lifecycle (queue → start → complete with metrics)

```bash
# 1. Queued
curl -s -X POST "https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send" \
  -H "Content-Type: application/json" \
  -H "X-NOTILENS-KEY: $NOTILENS_SECRET" \
  -d '{
    "event": "task.queued",
    "title": "my-app | data-pipeline | task.queued",
    "message": "Data pipeline job queued.",
    "type": "info",
    "agent": "my-app",
    "task_id": "data-pipeline",
    "run_id": "run_1714000000000_a3f2"
  }'

# 2. Started
curl -s -X POST "https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send" \
  -H "Content-Type: application/json" \
  -H "X-NOTILENS-KEY: $NOTILENS_SECRET" \
  -d '{
    "event": "task.started",
    "title": "my-app | data-pipeline | task.started",
    "message": "Starting nightly data pipeline run.",
    "type": "info",
    "agent": "my-app",
    "task_id": "data-pipeline",
    "run_id": "run_1714000000000_a3f2",
    "meta": { "queue_ms": 1240 }
  }'

# 3. Completed with metrics
curl -s -X POST "https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send" \
  -H "Content-Type: application/json" \
  -H "X-NOTILENS-KEY: $NOTILENS_SECRET" \
  -d '{
    "event": "task.completed",
    "title": "my-app | data-pipeline | task.completed",
    "message": "Pipeline finished. Processed 4,218 records in 47s.",
    "type": "success",
    "agent": "my-app",
    "task_id": "data-pipeline",
    "run_id": "run_1714000000000_a3f2",
    "meta": {
      "total_duration_ms": 47200,
      "active_ms": 45800,
      "rows_processed": 4218,
      "rows_failed": 0,
      "env": "production"
    }
  }'
```

### Task failed with counters

```bash
curl -s -X POST "https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send" \
  -H "Content-Type: application/json" \
  -H "X-NOTILENS-KEY: $NOTILENS_SECRET" \
  -d '{
    "event": "task.failed",
    "title": "my-app | data-pipeline | task.failed",
    "message": "Database connection timed out after 3 retries.",
    "type": "urgent",
    "agent": "my-app",
    "task_id": "data-pipeline",
    "run_id": "run_1714000000000_a3f2",
    "is_actionable": true,
    "meta": {
      "total_duration_ms": 92000,
      "active_ms": 88000,
      "retry_count": 3,
      "error_count": 3,
      "last_error": "connect ETIMEDOUT 10.0.0.5:5432"
    }
  }'
```

### Pause and resume with timing

```bash
# Pausing (e.g. hit rate limit)
curl -s -X POST "https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send" \
  -H "Content-Type: application/json" \
  -H "X-NOTILENS-KEY: $NOTILENS_SECRET" \
  -d '{
    "event": "task.paused",
    "title": "my-app | api-sync | task.paused",
    "message": "Rate limit hit — waiting 30s before resuming.",
    "type": "warning",
    "agent": "my-app",
    "task_id": "api-sync",
    "run_id": "run_1714000000000_b7c1",
    "meta": { "pause_count": 1, "wait_reason": "rate_limit" }
  }'

# Resuming
curl -s -X POST "https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send" \
  -H "Content-Type: application/json" \
  -H "X-NOTILENS-KEY: $NOTILENS_SECRET" \
  -d '{
    "event": "task.resumed",
    "title": "my-app | api-sync | task.resumed",
    "message": "Resuming after rate limit window.",
    "type": "info",
    "agent": "my-app",
    "task_id": "api-sync",
    "run_id": "run_1714000000000_b7c1",
    "meta": { "pause_ms": 31200, "pause_count": 1 }
  }'
```

### Human input required

```bash
curl -s -X POST "https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send" \
  -H "Content-Type: application/json" \
  -H "X-NOTILENS-KEY: $NOTILENS_SECRET" \
  -d '{
    "event": "input.required",
    "title": "my-app | approval needed",
    "message": "About to delete 83 records. Please confirm.",
    "type": "warning",
    "agent": "my-app",
    "is_actionable": true,
    "open_url": "https://dashboard.example.com/approve/123"
  }'
```

### Output generated (with download link)

```bash
curl -s -X POST "https://hook.notilens.com/webhook/$NOTILENS_TOKEN/send" \
  -H "Content-Type: application/json" \
  -H "X-NOTILENS-KEY: $NOTILENS_SECRET" \
  -d '{
    "event": "output.generated",
    "title": "my-app | report-gen | output.generated",
    "message": "Monthly report ready. 24 pages, 3 charts.",
    "type": "success",
    "agent": "my-app",
    "task_id": "report-gen",
    "download_url": "https://storage.example.com/reports/2026-04.pdf",
    "meta": {
      "pages": 24,
      "charts": 3,
      "total_duration_ms": 18400
    }
  }'
```

## Usage Guidance

- **Always fire `task.started`** when beginning a significant task so the user knows work has begun.
- **Fire `task.completed` or `task.failed`** at every terminal state — never leave a started task without a closing event.
- **Generate a `run_id`** at task start (`run_{unix_ms}_{random_hex4}`) and include it on every event for that run.
- **Include timing in `meta`** on terminal events (`task.completed`, `task.failed`, `task.timeout`) — `total_duration_ms` and `active_ms` at minimum.
- **Include counters in `meta`** whenever they are non-zero: `retry_count`, `error_count`, `loop_count`, `pause_count`, `wait_count`.
- **Use `input.required` with `is_actionable: true`** whenever a human decision is needed before continuing.
- **Fire `task.loop`** when the same logical step is repeating. Include `loop_count` in `meta`.
- **Keep `message` concise and informative** — include counts, durations, or key values (e.g. "Processed 1,240 rows in 3.2s — 2 errors").
- **Use `task_id`** consistently across all events for the same logical task so NotiLens can group them.
- **Do not spam** — avoid sending `task.progress` more than once every few seconds for fast-running tasks.

## Configuration

Set these environment variables before running:

```bash
export NOTILENS_TOKEN=your_topic_token
export NOTILENS_SECRET=your_topic_secret
```

Both are found in your topic settings at https://www.notilens.com.
