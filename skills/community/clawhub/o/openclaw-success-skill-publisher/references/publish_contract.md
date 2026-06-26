# Publish Contract

This skill uses webhook-style integration for sharing channels and a generic HTTP API contract for ClawHub publishing.

## ClawHub Publish Payload

POST `${CLAWHUB_API_BASE}/v1/skills`

```json
{
  "name": "skill-slug",
  "title": "Human Title",
  "bundle_path": "/abs/path/generated_skill.zip",
  "bundle_b64": "<hex-string>"
}
```

## Share Payload

POST `<platform_webhook_url>`

```json
{
  "platform": "zhihu",
  "content": "...markdown content..."
}
```

If real platform APIs are unavailable, keep the generated markdown drafts under `share_payloads/` and publish manually.
