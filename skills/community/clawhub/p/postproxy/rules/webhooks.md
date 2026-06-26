# Webhooks

Receive real-time HTTP callbacks for post publishing, stats, comments, messages, and profile events instead of polling.

> 🔒 **Data egress.** Webhook payloads are sent to the registered URL and can contain private content — DM text, comment bodies, author metadata. Only register HTTPS endpoints the user controls and trusts; confirm the destination URL with the user before creating or updating a webhook.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/webhooks` | List all webhooks |
| GET | `/api/webhooks/{id}` | Retrieve a single webhook |
| POST | `/api/webhooks` | Create a webhook |
| PATCH | `/api/webhooks/{id}` | Update a webhook |
| DELETE | `/api/webhooks/{id}` | Delete a webhook |
| GET | `/api/webhooks/{id}/deliveries` | View delivery history |

## Create Webhook
```bash
curl -X POST "https://api.postproxy.dev/api/webhooks" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/postproxy/webhook",
    "events": ["platform_post.published", "platform_post.failed"],
    "description": "Publish notifications"
  }'
```

Parameters:
- `url` (required): HTTPS endpoint to deliver events to
- `events` (required): Array of event types to subscribe to. Use `["*"]` for all events.
- `description` (optional): Webhook label

The response includes a `secret` needed for signature verification. **Treat it as a credential**: store it in a secret manager or environment variable, never echo it into chat output, logs, or source control. Anyone holding the secret can forge signed webhook requests to the receiving endpoint.

## Update Webhook
```bash
curl -X PATCH "https://api.postproxy.dev/api/webhooks/{id}" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "enabled": false }'
```

Modifiable fields: `url`, `events`, `enabled`, `description`.

## Event Types

Post lifecycle: `post.processed`, `post.imported`

Platform publishing: `platform_post.published`, `platform_post.failed`, `platform_post.failed_waiting_for_retry`, `platform_post.insights`

Profiles: `profile.connected`, `profile.disconnected`, `profile.stats`

Comments: `comment.created`, `comment.failed`, `comment.failed_waiting_for_retry`, `profile_comment.created`, `profile_comment.failed`, `profile_comment.failed_waiting_for_retry`

Messaging: `message.received`, `message.sent`, `message.delivered`, `message.read`, `message.edited`, `message.deleted`, `message.failed_waiting_for_retry`, `message.failed`

Interactions: `reaction.received`, `referral.received`

Media: `media.failed`

## Payload Envelope

All deliveries share the same envelope:
```json
{
  "id": "whevt_abc",
  "object": "event",
  "type": "platform_post.published",
  "created_at": "2026-06-11T10:30:00Z",
  "data": {
    "object": { }
  }
}
```

`data.object` carries the event-specific resource (e.g. the platform post, comment, or message).

Delivery request headers:
- `Content-Type: application/json`
- `User-Agent: Postproxy-Webhooks/1.0`
- `X-Postproxy-Event`: event type
- `X-Postproxy-Delivery`: unique delivery ID
- `X-Postproxy-Signature`: HMAC signature (see below)

## Signature Verification

Header: `X-Postproxy-Signature`, format `t={timestamp},v1={hex_digest}`.
Algorithm: HMAC-SHA256 over the string `"{timestamp}.{raw_json_body}"`, keyed with the webhook `secret`.

Node.js:
```javascript
const crypto = require("crypto");
function verifyWebhook(payload, signatureHeader, secret) {
  const parts = Object.fromEntries(
    signatureHeader.split(",").map((p) => p.split("=", 2))
  );
  const signedPayload = `${parts.t}.${payload}`;
  const computed = crypto
    .createHmac("sha256", secret)
    .update(signedPayload)
    .digest("hex");
  return crypto.timingSafeEqual(Buffer.from(computed), Buffer.from(parts.v1));
}
```

Python:
```python
import hmac, hashlib

def verify_webhook(payload: str, signature_header: str, secret: str) -> bool:
    parts = dict(p.split("=", 1) for p in signature_header.split(","))
    signed_payload = f"{parts['t']}.{payload}"
    computed = hmac.new(
        secret.encode(), signed_payload.encode(), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed, parts["v1"])
```

## Retry Policy

Deliveries are retried with exponential backoff, up to 5 attempts:

| Attempt | Delay |
|---------|-------|
| 1 | Immediate |
| 2 | 1 minute |
| 3 | 5 minutes |
| 4 | 30 minutes |
| 5 | 2 hours |

Your endpoint must return a 2xx within 30 seconds; the connection timeout is 10 seconds.

## Delivery History
```bash
curl -X GET "https://api.postproxy.dev/api/webhooks/{id}/deliveries?page=0&per_page=20" \
  -H "Authorization: Bearer $POSTPROXY_API_KEY"
```

Query parameters: `page` (default `0`), `per_page` (default `20`).

Each delivery includes: `id`, `event_id`, `event_type`, `response_status`, `attempt_number`, `success`, `attempted_at`, `created_at`.
