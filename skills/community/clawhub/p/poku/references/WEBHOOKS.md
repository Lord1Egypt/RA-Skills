# Webhooks & Inbound Configuration

Webhooks are required to receive inbound SMS and calls. Without a webhook registered, inbound events will not be delivered to your agent.

For full setup instructions, see: https://docs.pokulabs.com/poku-skill/webhook

---

## Supported Inbound Event Types

| Event | Fires when… |
|---|---|
| `message.received` | An inbound SMS arrives on your reserved number |
| `call.conversation.ended` | An inbound phone call arrives on your reserved number |


```json
{
  "eventType": "message.received",
  "payload": {
    "interactionId": "ia_abc123",
    "medium": "sms",
    "from": "+14155550199",
    "to": "+14155550100",
    "body": "Hey, are you available tomorrow?",
    "mediaUrls": []
  }
}
```

```json
{
  "eventType": "call.conversation.ended",
  "payload": {
    "interactionId": "ia_abc123",
    "summary": "Caller confirmed their appointment for tomorrow at 3pm.",
    "from": "+14155550199",
    "to": "+14155550100"
  }
}
```

Documentation: https://docs.pokulabs.com/poku-skill/webhook

---

## OpenClaw Setup

To forward inbound Poku events to your OpenClaw agent, add a `hooks` mapping to `~/.openclaw/openclaw.json`
Example mapping below:

```json
{
  "hooks": {
    "enabled": true,
    "token": "<openclaw-hooks-token>",
    "transformsDir": "~/.openclaw/hooks/transforms",
    "defaultSessionKey": "hook:ingress",
    "allowRequestSessionKey": false,
    "allowedSessionKeyPrefixes": ["hook:"],
    "mappings": [
      {
        "match": { "path": "poku" },
        "action": "agent",
        "agentId": "main",
        "sessionKey": "hook:poku",
        "wakeMode": "now",
        "name": "Poku",
        "deliver": true,
        "channel": "telegram",
        "to": "<your-telegram-id>",
        "messageTemplate": "You received a message from {{payload.payload.from}}: \"{{payload.payload.body}}{{payload.payload.summary}}\""
      }
    ]
  }
}
```

For the full OpenClaw webhook reference: https://docs.openclaw.ai/automation/webhook

---

## Managing Webhooks via API

### List Webhooks - Check if there is a webhook configured to your account

```bash
curl -s https://api.pokulabs.com/webhooks \
  -H "Authorization: Bearer $POKU_API_KEY"
```

### Create a Webhook

```bash
curl -s -X POST https://api.pokulabs.com/webhooks \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Inbound SMS webhook",
    "url": "https://example.com/poku-webhook",
    "signingSecret": "supersecret123",
    "eventTypes": ["phone.sms.received"]
  }'
```

| Field | Required | Description |
|---|---|---|
| `url` | Yes | Destination URL for webhook deliveries |
| `eventTypes` | Yes | One or more of the supported event types above. Max 10. |
| `name` | No | Friendly label |
| `signingSecret` | No | 8–200 char shared secret for signature verification |
| `headers` | No | Extra static headers attached to every delivery |

### Update a Webhook

```bash
curl -s -X PATCH https://api.pokulabs.com/webhooks/<WEBHOOK_ID> \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"isActive": false}'
```

Updatable fields: `name`, `url`, `signingSecret`, `headers`, `isActive`, `eventTypes`.

### Delete a Webhook

```bash
curl -s -X DELETE https://api.pokulabs.com/webhooks/<WEBHOOK_ID> \
  -H "Authorization: Bearer $POKU_API_KEY"
```

Returns `204 No Content` on success.
