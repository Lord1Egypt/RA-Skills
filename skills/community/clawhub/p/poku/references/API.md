# Poku API Reference

## Contents

- [Calls](#calls) — Place outbound call, get call result
- [Messages](#messages) — SMS, WhatsApp, Slack, saved channels
- [Numbers](#numbers) — List available, list reserved, reserve, release
- [Webhooks](#webhooks) — List, create, update, delete

Base URL: `https://api.pokulabs.com`

All requests use Bearer auth:
```
Authorization: Bearer $POKU_API_KEY
```

---

## Calls

### POST /calls — Place an outbound call

| Field | Type | Required | Description |
|---|---|---|---|
| `prompt` | string | Yes | Instructions for the call: goal, context, branching behavior, voicemail script. |
| `to` | string | Yes | Recipient number in E.164 format. |
| `from` | string | No | Caller ID. Defaults to your reserved number, or a shared Poku number. |
| `transferTo` | string | No | E.164 number to transfer the call to if the recipient asks for a human. |
| `language` | string | No | Language e.g. `en-US`, `de-DE`. Defaults to `en-US`. Note: accents/dialects not supported |
| `voice` | `"male"` \| `"female"` | No | Voice for the call. Defaults to `"female"`. |
| `waitForCallEnd` | boolean | No | `true` = block until call ends (Mode A). `false` = return immediately with `interactionId` (Mode B). Default `false` |
| `yieldMs` | number | No | Mode A: set to `300000`. Mode B: set to `1000`. |

**Response (Mode A):**
```json
{
  "response": "ABC restaurant confirmed your reservation for 2 people at 6pm tomorrow.",
  "call": {
    "recordingUrl": "https://cdn.example.com/recordings/abc123.wav"
  },
  "interactionId": "f3f7870f-30f5-4bf2-83b0-a05bc140030c"
}
```

`call.recordingUrl` may be omitted when no recording is available.

**Response (Mode B):**
```json
{
  "interactionId": "f3f7870f-30f5-4bf2-83b0-a05bc140030c"
}
```

### GET /interactions/:interactionId/status — Get call result

Use with Mode B to poll for the outcome after placing a non-blocking call.

```bash
curl -s https://api.pokulabs.com/interactions/<interactionId>/status \
  -H "Authorization: Bearer $POKU_API_KEY"
```

---

## Messages

### POST /messages/sms

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | Yes | Message body. Max 1000 characters. |
| `to` | string | Yes | Recipient in E.164 format. |
| `from` | string | No | Sender number in E.164 format. Defaults to your reserved number. |
| `waitTime` | number | No | Seconds to hold the request open for a reply (1–600). |
| `followUpTime` | number | No | Seconds for webhook to keep listening (1–60000). |

### POST /messages/whatsapp

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | Yes | Message body. Max 1000 characters. |
| `to` | string | Yes | Recipient in E.164 format. |
| `waitTime` | number | No | Seconds to hold the request open for a reply (1–600). |
| `followUpTime` | number | No | Seconds for webhook to keep listening (1–60000). |

### POST /messages/slack

| Field | Type | Required | Description |
|---|---|---|---|
| `message` | string | Yes | Slack message body. |
| `to` | string | Yes | Slack user, member, or channel ID. |
| `from` | string | No | Slack workspace ID. Omit to send from the Poku Slack workspace. |
| `waitTime` | number | No | Seconds to wait for a threaded reply. |
| `followUpTime` | number | No | Seconds to continue listening after `waitTime`. |

---

## Numbers

### GET /numbers/available

| Param | Type | Required | Description |
|---|---|---|---|
| `country` | `"US"` \| `"GB"` | No | Country to search. Defaults to `"US"`. |
| `areaCode` | number | No | Three-digit US area code. US only. |

**Response:** Array of `{ phoneNumber, locality, region, country }` objects.

### GET /numbers

Lists your currently reserved numbers. Each includes `id`, `phoneNumber`, `createdAt`, `updatedAt`.

### POST /numbers/reserve

| Field | Type | Required | Description |
|---|---|---|---|
| `phoneNumber` | string | Yes | E.164 number from `GET /numbers/available`. |

**Response:** `{ id, phoneNumber, createdAt, updatedAt }`

### DELETE /numbers/:id

Releases a reserved number. Irreversible — confirm with the user before calling. Returns `{ id, number }`.

---

## Webhooks

### GET /webhooks

Lists all registered webhooks.

### POST /webhooks

| Field | Type | Required | Description |
|---|---|---|---|
| `url` | string | Yes | Destination URL. |
| `eventTypes` | string[] | Yes | Event types to subscribe to. Max 10. |
| `name` | string | No | Friendly name. |
| `signingSecret` | string | No | Shared secret for verification. 8–200 characters. |
| `headers` | object | No | Extra static headers on deliveries. |

### PATCH /webhooks/:id

Updates a webhook. Only fields you send are changed. Updatable: `name`, `url`, `signingSecret`, `headers`, `isActive`, `eventTypes`.

### DELETE /webhooks/:id

Deletes a webhook. Returns `204 No Content`.
