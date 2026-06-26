# Operations — Paperclip CLI and API

## CLI Essentials

```bash
pnpm paperclipai company list
pnpm paperclipai issue list --status todo,in_progress
pnpm paperclipai issue create --title "Define CTO hiring plan" --status todo --priority high
pnpm paperclipai approval list --status pending
pnpm paperclipai heartbeat run --agent-id <agent-id>
```

## API Identity Check

```bash
curl -sS "$PAPERCLIP_API_URL/api/agents/me" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY"
```

## Create a Company

```bash
curl -sS -X POST "$PAPERCLIP_API_URL/api/companies" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme AI","description":"Autonomous product studio"}'
```

## Create and Update Work

```bash
curl -sS -X POST "$PAPERCLIP_API_URL/api/companies/$PAPERCLIP_COMPANY_ID/issues" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"Draft onboarding system","status":"todo","priority":"high"}'

curl -sS -X PATCH "$PAPERCLIP_API_URL/api/issues/$ISSUE_ID" \
  -H "Authorization: Bearer $PAPERCLIP_API_KEY" \
  -H "X-Paperclip-Run-Id: $PAPERCLIP_RUN_ID" \
  -H "Content-Type: application/json" \
  -d '{"status":"done","comment":"Completed and documented the workflow."}'
```

## Operating Principle

Use the CLI for fast local control and the API when you need automation, external tooling, or explicit heartbeat-aware mutations.
