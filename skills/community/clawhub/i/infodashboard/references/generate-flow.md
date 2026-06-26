# Generate Flow

## Preconditions

- Repo path is confirmed
- `.env.local` is configured with an LLM key and database credentials
- `tools/frpc-visitor.ini` is configured (tunnel auto-starts with the server)
- InfoDashboard server is healthy at the selected `url`
- Docker daemon is running

## Submitting a Generation Request

If the user has already clearly asked to generate a dashboard and the preconditions are satisfied, submit the request immediately. Do not ask for a second confirmation.

```text
POST {url}/api/generate
Content-Type: application/json
```

Request body:

```json
{
  "user_request": "我要看冲压车间昨天的合格率，按产线对比，可以筛选日期"
}
```

Only `user_request` is required. The server reads database credentials from `.env.local`.

Optional fields:

- `max_retries` (integer, default 2) — how many times the QA agent may send code back to the developer for fixes before giving up

## Reading the SSE Stream

The endpoint returns a **Server-Sent Events** stream. Read events line by line until you see `data: [DONE]`.

Each event is a JSON object with a `type` field:

| Type | Meaning |
|------|---------|
| `agent_start` | An agent began working (analyst, developer, qa, deployer) |
| `text_delta` | Streamed LLM token — accumulate for display |
| `thinking` | Status message from an agent (e.g., "正在获取数据库表列表...") |
| `action` | Structured result (e.g., tables found, code written) |
| `code_block` | Generated app.py preview |
| `agent_end` | An agent finished |
| `done` | **Generation succeeded** — contains the dashboard URL |
| `error` | Generation failed — contains an error message |

### Agent Pipeline

The four agents run in sequence:

1. **需求分析官** — Queries SQL Server schema, selects relevant tables, produces a requirements spec
2. **Web 开发工程师** — Generates the Streamlit app code
3. **QA & 安全检查** — Validates syntax, checks for SQL injection, runs security scan
4. **部署运维工程师** — Builds and launches a Docker container, health-checks the dashboard

If QA fails, the developer retries up to `max_retries` times before the job fails.

### Success Event

When `type` is `done`, extract the URL:

```json
{
  "type": "done",
  "data": {
    "dashboardUrl": "http://localhost:8523",
    "port": 8523,
    "dashboardId": "dashboard-a1b2c3d4"
  }
}
```

### Error Event

When `type` is `error`:

```json
{
  "type": "error",
  "data": {
    "message": "数据库连接失败：..."
  }
}
```

Surface the error message directly. If it suggests a database or provider problem, tell the user to update `.env.local` and retry.

## Reliability Rules

- Do not resubmit the job just because a connection drops mid-stream. Ask the user before retrying.
- If the stream ends without a `done` event, report what the last known state was.
- Do not change request parameters to work around a provider or database error — direct the user to fix `.env.local` instead.

## What To Return

Return the dashboard ID and URL.

Output the URL as a raw absolute URL on its own line.

Do not wrap the URL in:

- bold markers such as `**...**`
- markdown links such as `[title](url)`
- code formatting such as `` `...` ``
- angle brackets such as `<...>`
- markdown tables

Use a compact format like:

```text
Dashboard ID: dashboard-a1b2c3d4
Dashboard URL:
http://localhost:8523
```

If the job fails, return the error message from the `error` event.

## Managing Running Dashboards

List all running dashboards:

```text
GET {url}/api/dashboards
```

Stop and remove a dashboard:

```text
DELETE {url}/api/dashboards/{dashboardId}
```

## Confirmation Requirements

- Do not ask for a second confirmation before the generation request if the user has already clearly asked to generate.
- Do ask before stopping or deleting a running dashboard.
