---
name: inngest
description: Manage Inngest serverless background jobs and event-driven workflows via REST API. Use when asked to send events, trigger functions, list runs, cancel jobs, or inspect workflow history. Requires INNGEST_EVENT_KEY and INNGEST_SIGNING_KEY env vars.
---

# Inngest Skill

Base event ingestion URL: `https://inn.gs/e/<INNGEST_EVENT_KEY>`
Management API base: `https://api.inngest.com/v1`

## Auth
```bash
# Send an event (key in URL)
curl -X POST "https://inn.gs/e/$INNGEST_EVENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"app/user.signup","data":{"userId":"123"}}'

# Management API
curl -H "Authorization: Bearer $INNGEST_SIGNING_KEY" \
  https://api.inngest.com/v1/runs
```

## Common Operations

**Send a single event:**
```bash
curl -X POST "https://inn.gs/e/$INNGEST_EVENT_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"app/order.created","data":{"orderId":"ord_123","total":49.99},"user":{"id":"usr_456"}}'
```

**Send a batch of events:**
```bash
curl -X POST "https://inn.gs/e/$INNGEST_EVENT_KEY" \
  -H "Content-Type: application/json" \
  -d '[{"name":"app/email.sent","data":{"to":"a@example.com"}},{"name":"app/email.sent","data":{"to":"b@example.com"}}]'
```

**List function runs:**
```bash
curl -H "Authorization: Bearer $INNGEST_SIGNING_KEY" \
  "https://api.inngest.com/v1/runs?limit=20&status=running"
```

**Get a specific run:**
```bash
curl -H "Authorization: Bearer $INNGEST_SIGNING_KEY" \
  "https://api.inngest.com/v1/runs/$RUN_ID"
```

**Cancel a function run:**
```bash
curl -X DELETE \
  -H "Authorization: Bearer $INNGEST_SIGNING_KEY" \
  "https://api.inngest.com/v1/runs/$RUN_ID"
```

**List all registered apps:**
```bash
curl -H "Authorization: Bearer $INNGEST_SIGNING_KEY" \
  "https://api.inngest.com/v1/apps"
```

**Replay a failed run:**
```bash
curl -X POST \
  -H "Authorization: Bearer $INNGEST_SIGNING_KEY" \
  "https://api.inngest.com/v1/runs/$RUN_ID/replay"
```

## Tips
- Event names follow `domain/noun.verb` convention (e.g. `app/user.created`)
- Batch up to 512 events per POST to reduce HTTP overhead
- The `user.id` field enables per-user throttle and concurrency controls
- Filter runs by `status` (running, completed, failed, cancelled) to keep responses lean
