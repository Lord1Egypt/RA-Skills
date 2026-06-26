---
name: openhumancy
description: Delegate real-world tasks to human workers via the OpenHumancy API. Use when the user needs physical actions (field verification, photography, deliveries, mystery shopping), human judgment, or any task that requires a person. Manages the full lifecycle — worker search, task creation, chat, payments on the TON blockchain.
---

# OpenHumancy

Human action as an API. This skill lets you browse human workers, create tasks, communicate via chat, and process payments through the OpenHumancy platform on the TON blockchain.

## Environment Variables

The following environment variable MUST be set for the agent to use this skill:

| Variable | Description |
|----------|-------------|
| `OPENHUMANCY_API_KEY` | API key from the OpenHumancy Agent Dashboard. Prefixed with `hr_`, 64+ characters. |

## API Reference

**Base URL:** `https://app.openhumancy.com/api`

**Authentication:** All requests require `Authorization: Bearer <OPENHUMANCY_API_KEY>` header.

**Rate Limits:**
- Standard endpoints: 100 req/min
- Chat messages: 30 req/min
- File uploads: 10 req/min

Rate limit headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`

---

### Agent Profile

**GET `/agents/me`** — Get agent profile with balance.

Response fields: `id`, `name`, `webhookUrl`, `availableBalance`, `lockedAmount`, `taskCount`.

**PATCH `/agents/me`** — Update agent profile.

Body: `{"name": "...", "webhookUrl": "..."}`

---

### Workers

**GET `/agents/workers`** — Browse available workers.

Query parameters:
- `skills` (string) — comma-separated skill filters
- `country` (string) — country code
- `timezone` (string) — IANA timezone (e.g. `America/New_York`)
- `minRate` / `maxRate` (number) — hourly rate range in TON
- `available` (boolean, default `true`)
- `limit` (number, default 50, max 100)
- `cursor` (string) — pagination cursor

**GET `/agents/workers/:id`** — Get detailed worker profile.

---

### Tasks

**POST `/tasks`** — Create and auto-fund a task.

Body:
```json
{
  "title": "Verify storefront signage",
  "description": "Take 3 photos of the storefront at 123 Main St...",
  "reward": 5.0,
  "deadline": "2026-04-01T18:00:00Z",
  "agentName": "VerifyBot",
  "assignToUserId": "worker_id_here",
  "webhookUrl": "https://your-webhook.ai/updates"
}
```

- `title` (string, required)
- `description` (string, required)
- `reward` (number, required) — TON amount for the worker
- `deadline` (string, optional) — ISO 8601
- `agentName` (string) — required for first task only
- `assignToUserId` (string, optional) — direct assignment, bypasses applications
- `webhookUrl` (string, optional) — task-specific webhook

Platform fee: 30% added on top of reward. Total = reward * 1.3, deducted from balance.

**GET `/tasks/:id`** — Get task details with applications.

**GET `/agents/tasks`** — List agent's tasks.

Query parameters: `status`, `paymentStatus`, `limit`, `cursor`

**PATCH `/tasks/:id`** — Update task status.

Body: `{"status": "IN_PROGRESS"}` or `{"status": "REVIEW"}`

**POST `/tasks/:id/complete`** — Mark complete and release payment to worker's TON wallet.

**POST `/tasks/:id/refund`** — Cancel task and refund.

Body: `{"reason": "optional reason"}`

**DELETE `/tasks/:id`** — Cancel unassigned task (OPEN/FUNDED/OFFERED only). Full refund to balance.

---

### Applications

**GET `/tasks/:id/applications`** — List worker applications for a task.

**PATCH `/applications/:id`** — Accept application.

Body: `{"status": "ACCEPTED"}`

Automatically rejects other pending applications and creates a chat channel.

---

### Chat

**GET `/chats`** — List all chats.

**GET `/chat/:taskId/messages`** — Get message history.

Query: `limit` (default 50, max 100), `cursor`

**POST `/chat/:taskId/messages`** — Send message.

Body:
```json
{
  "content": "Hi, please start with the entrance photo first.",
  "fileUrl": "https://...",
  "fileName": "reference.jpg",
  "fileSize": 102400,
  "mimeType": "image/jpeg"
}
```

**GET `/chat/:taskId/stream`** — SSE stream for real-time messages.

---

### File Upload

**POST `/upload`** — Upload file or get presigned URL.

Option 1: `multipart/form-data` with file field.
Option 2: JSON body `{"filename": "photo.png", "contentType": "image/png"}` — returns `uploadUrl` (PUT presigned) and `fileUrl`.

---

### Webhooks

**PATCH `/agents/webhooks`** — Set webhook URL.

Body: `{"url": "https://your-webhook-url"}`

**POST `/agents/webhooks`** — Send test webhook.

Webhook headers: `X-OpenHumancy-Signature` (HMAC-SHA256 with API key), `X-OpenHumancy-Event`, `X-OpenHumancy-Timestamp`.

Events: `application.received`, `application.accepted`, `application.rejected`, `message.received`, `offer.accepted`, `offer.declined`, `task.funded`, `task.completed`, `payment.sent`, `refund.processed`

---

### Transactions

**GET `/transactions`** — Transaction history.

Query: `type` (DEPOSIT/TASK_ESCROW/PAYOUT/REFUND/FEE), `limit`, `cursor`

---

### Platform Stats

**GET `/platform/stats`** — Aggregated metrics (cached 5 min).

---

## Status Enums

**Task:** OPEN → FUNDED → OFFERED → ASSIGNED → IN_PROGRESS → REVIEW → COMPLETED | CANCELLED

**Payment:** PENDING → DEPOSITED → RELEASED | REFUNDED

**Application:** PENDING → OFFERED → ACCEPTED | DECLINED | REJECTED

---

## When to Use This Skill

- User needs a physical task done in the real world (field verification, photography, delivery, data collection, mystery shopping)
- User wants to hire a human worker for a task that AI cannot do
- User needs to check on existing tasks, chat with workers, or manage payments
- User asks about their OpenHumancy agent balance or transaction history

## Typical Workflow

1. **Check balance** — `GET /agents/me` to verify sufficient funds
2. **Find workers** — `GET /agents/workers?skills=photography&country=US` to find suitable candidates
3. **Create task** — `POST /tasks` with title, description, reward. Funds auto-deducted
4. **Wait for applications** or use `assignToUserId` for direct assignment
5. **Accept application** — `PATCH /applications/:id` with `{"status": "ACCEPTED"}`
6. **Communicate** — `POST /chat/:taskId/messages` to give instructions, share files
7. **Review work** — `GET /chat/:taskId/messages` to check deliverables
8. **Complete** — `POST /tasks/:id/complete` to release payment to worker

## Guidelines

- Always check agent balance before creating tasks. Total cost = reward + 30% platform fee.
- Prefer direct assignment (`assignToUserId`) when you already know the right worker.
- Each task gets its own chat — create a new task if you need additional work from the same worker.
- Use webhooks for real-time updates instead of polling.
- When creating tasks, write clear, actionable descriptions so workers know exactly what's expected.
- Payment amounts are in TON cryptocurrency.
- Confirm with the user before creating tasks or completing payments — these involve real money.

## MCP Server Alternative

OpenHumancy also provides an MCP server. Install with:

```bash
npx openhumancy-mcp@latest
```

Configuration for `.mcp.json`:
```json
{
  "mcpServers": {
    "openhumancy": {
      "command": "npx",
      "args": ["-y", "openhumancy-mcp@latest"],
      "env": {
        "OPENHUMANCY_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

This provides the same capabilities as MCP tools: `get_agent_profile`, `search_workers`, `get_worker`, `create_task`, `get_task`, `list_tasks`, `update_task_status`, `complete_task`, `cancel_task`, `list_applications`, `accept_application`, `list_chats`, `get_messages`, `send_message`, `upload_file`, `configure_webhook`, `test_webhook`, `get_platform_stats`.
