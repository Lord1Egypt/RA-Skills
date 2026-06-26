# NoddyAI API Endpoints Reference

Base URL: `https://api.graine.ai`
Auth: `Authorization: Bearer <API_KEY>`

---

## 1. API Key Management

### Validate API Token
```
GET /api/v1/api-tokens/validate-token
Authorization: Bearer <API_KEY>
```

### List API Tokens
```
GET /api/v1/api-tokens/list-tokens?org_id=<ORG_ID>
Authorization: Bearer <API_KEY>
```

### Revoke API Token
```
DELETE /api/v1/api-tokens/revoke-token/<TOKEN_TO_REVOKE>
Authorization: Bearer <API_KEY>
```

---

## 2. Agent Management

### Create Voice Agent
```
POST /api/v1/agents
Authorization: Bearer <API_KEY>
Content-Type: application/json
```
See `examples.md` → Create Agent for full body.

### Get Agent (raw Bolna format — use for runtime/API calls)
```
GET /api/v1/agents/<AGENT_ID>?org_id=<ORG_ID>
Authorization: Bearer <API_KEY>
```

### Get Agent UI Config (masked providers — dashboard only)
```
GET /api/v1/voiceagents/<AGENT_ID>?org_id=<ORG_ID>
Authorization: Bearer <API_KEY>
```
> Do NOT use /voiceagents for runtime calls — returns masked/transformed data.

### List Agents
```
GET /api/v1/agents?org_id=<ORG_ID>&page=1&per_page=20
Authorization: Bearer <API_KEY>
```

### Update Agent (PATCH — voice, prompt, or tools)
```
PATCH /api/v1/agents/<AGENT_ID>?org_id=<ORG_ID>
Authorization: Bearer <API_KEY>
Content-Type: application/json
```
Send only the fields you want to change. See `examples.md` for specific update shapes.

### Delete Agent
```
DELETE /api/v1/agents/<AGENT_ID>?org_id=<ORG_ID>
Authorization: Bearer <API_KEY>
```

---

## 3. Telephony — Outbound Calls

### Make Outbound Call
```
POST /api/v1/telephony/call
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

| Field | Required | Description |
|-------|----------|-------------|
| `recipient` | Yes | E.164 phone number, e.g. `+911234567890` |
| `agent_id` | Yes | Agent to drive the call |
| `org_id` | Yes | Your org ID |
| `provider` | No | `jambonz` \| `exotel` \| omit for auto |
| `from_number` | No | Caller ID (required for jambonz/exotel) |
| `record` | No | `true` to record |
| `timeout` | No | Ring timeout in seconds |
| `webhook_url` | No | URL to receive completed-call payload |
| `metadata` | No | Object of custom key/value pairs injected into prompt as variables |

### Get Call Status
```
GET /api/v1/telephony/call/<CALL_SID>
Authorization: Bearer <API_KEY>
```

### Transfer Call (mid-call human handoff)
```
POST /api/v1/telephony/transfer
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "call_sid": "<CALL_SID>",
  "transfer_to": "+911112223333",
  "caller_id": "+911234567890"
}
```

---

## 4. Telephony — Inbound

### Create Inbound Agent
```
POST /api/v1/telephony/inbound-agents
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "provider": "jambonz",
  "name": "Sales Inbound",
  "agent_id": "<AGENT_ID>",
  "org_id": "<ORG_ID>"
}
```

### Update Inbound Webhook URLs
```
PATCH /api/v1/telephony/inbound-agents/webhooks
Authorization: Bearer <API_KEY>
Content-Type: application/json

{
  "provider": "jambonz",
  "org_id": "<ORG_ID>",
  "agent_id": "<AGENT_ID>",
  "call_hook_url": "https://rotaryrouter.graine.ai/webhooks/jambonz/inbound/<AGENT_ID>",
  "call_status_hook_url": "https://rotaryrouter.graine.ai/webhooks/jambonz/status"
}
```

---

## 5. Batch Calls

### Submit Batch Call
```
POST /api/v1/batch/calls
Authorization: Bearer <API_KEY>
Content-Type: application/json
```
See `examples.md` → Batch Call.

### Upload CSV Batch
```
POST /api/v1/batch/upload
Authorization: Bearer <API_KEY>
Content-Type: multipart/form-data

Fields:
  file      — CSV file (columns: phone, name, <custom_vars...>)
  agent_id  — agent ID
  org_id    — org ID
```

---

## 6. Call Records

### List Call Records
```
GET /api/v1/calls?org_id=<ORG_ID>&page=1&per_page=20&status=completed
Authorization: Bearer <API_KEY>
```
`status` values: `completed` | `failed` | `no-answer` | `busy`

### Get Single Call Record
```
GET /api/v1/calls/<CALL_SID>
Authorization: Bearer <API_KEY>
```
