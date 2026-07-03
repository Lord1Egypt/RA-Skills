# Nishare API Reference

## Endpoints

| Method | Path | Auth | Purpose |
|---|---|---|---|
| `POST` | `/api/ai/publish` | Optional | Create a new share. Anonymous publishing is allowed. |
| `POST` | `/api/ai/update` | Required | Update an existing project owned by the API user. |

Production base URL: `https://nishare.com`

Local development base URL: `http://localhost:4173`

## Authentication

Use either header:

```http
X-Nishare-Key: nsk_xxx
```

or:

```http
Authorization: Bearer nsk_xxx
```

Authentication is required for `/api/ai/update`. For `/api/ai/publish`, authentication attaches the project to the user's account/default private 工作组 and enables 工作组 targeting.

## JSON Payload Fields

Common fields:

- `title`: display title. Defaults by content type when omitted.
- `description`: optional short description.
- `type`: `html`, `markdown`, or `image`. If omitted, Nishare infers from the payload.
- `workspaceId`: publish into a specific 工作组.
- `workspaceName`: alternative 工作组 hint.
- `projectId` or `id`: target project for updates.

HTML fields:

- `html`: full HTML document.
- `content`: alternative field for HTML content.

Markdown fields:

- `markdown`: Markdown document.
- `content`: alternative field for Markdown content when `type` is `markdown`.

Image fields:

- `imageDataUrl`: `data:image/png;base64,...`, `jpeg/jpg`, `webp`, or `gif`.
- `imageBase64`: raw base64 image content; include `mime` when possible.
- `imageUrl`: HTTP or HTTPS URL.
- `content`: may be a `data:image/...` URL.
- `mime`: image MIME type for base64 payloads.

## Headers for Non-JSON Requests

Accepted metadata headers:

- `X-Nishare-Title`
- `X-Nishare-Description`
- `X-Nishare-Type`
- `X-Nishare-Workspace-Id`
- `X-Nishare-Workspace`
- `X-Nishare-Project-Id`
- Legacy aliases: `X-HTML-DIY-Title`, `X-HTML-DIY-Description`

## Examples

### Publish HTML JSON

```bash
curl -s https://nishare.com/api/ai/publish \
  -H 'Content-Type: application/json' \
  -d '{"title":"AI 生成演示","type":"html","html":"<!doctype html><html><body><h1>Hello</h1></body></html>"}'
```

### Publish Raw HTML

```bash
curl -s https://nishare.com/api/ai/publish \
  -H 'Content-Type: text/html' \
  -H 'X-Nishare-Title: AI 生成演示' \
  --data-binary '<!doctype html><html><body><h1>Hello</h1></body></html>'
```

### Publish Markdown

```bash
curl -s https://nishare.com/api/ai/publish \
  -H 'Content-Type: application/json' \
  -d '{"title":"需求说明","type":"markdown","markdown":"# 需求说明\n- 支持快速分享"}'
```

Raw Markdown is also accepted:

```bash
curl -s https://nishare.com/api/ai/publish \
  -H 'Content-Type: text/markdown' \
  -H 'X-Nishare-Title: 需求说明' \
  --data-binary '# 需求说明
- 支持快速分享'
```

### Publish Image

```bash
curl -s https://nishare.com/api/ai/publish \
  -H 'Content-Type: application/json' \
  -d '{"title":"视觉草图","type":"image","imageDataUrl":"data:image/png;base64,..."}'
```

With URL:

```bash
curl -s https://nishare.com/api/ai/publish \
  -H 'Content-Type: application/json' \
  -d '{"title":"视觉草图","type":"image","imageUrl":"https://example.com/image.png"}'
```

### Publish to 工作组

```bash
curl -s https://nishare.com/api/ai/publish \
  -H 'Content-Type: application/json' \
  -H 'X-Nishare-Key: nsk_xxx' \
  -d '{"workspaceId":"workspace_id","title":"AI 生成演示","type":"html","html":"<!doctype html><html><body><h1>Hello</h1></body></html>"}'
```

### Update Project

```bash
curl -s https://nishare.com/api/ai/update \
  -H 'Content-Type: application/json' \
  -H 'X-Nishare-Key: nsk_xxx' \
  -d '{"projectId":"project_id","title":"更新后的演示","type":"html","html":"<!doctype html><html><body><h1>Updated</h1></body></html>"}'
```

`projectId` may also be sent as `id` or `X-Nishare-Project-Id`.

## Responses

Publish success returns HTTP `201`:

```json
{
  "id": "abc123",
  "url": "/p/abc123",
  "shareUrl": "https://nishare.com/p/abc123",
  "expiresAfterViews": 10,
  "workspaceId": "",
  "createdAt": "2026-06-29T00:00:00.000Z"
}
```

When the AI-oriented publish route is used, `url` may equal the absolute `shareUrl`, and `message` may be included.

Update success returns HTTP `200`:

```json
{
  "id": "abc123",
  "shareUrl": "https://nishare.com/p/abc123",
  "projectUrl": "https://nishare.com/projects/abc123",
  "workspaceId": "workspace_id",
  "updatedAt": "2026-06-29T00:00:00.000Z",
  "message": "已更新 Nishare 项目：https://nishare.com/p/abc123"
}
```

Failure responses include `message`, and content review failures may include `matches`:

```json
{
  "message": "内容审核未通过，命中敏感词：example",
  "matches": ["example"]
}
```

## Validation Rules

- HTML must be pure HTML, start with `<!doctype html>` or `<html>`, include `<html>...</html>`, and end with `</html>`.
- HTML must not include Markdown code fences or explanatory text outside the document.
- HTML and Markdown are limited to 1 MB.
- Images are limited to 5 MB.
- Image Data URLs support `png`, `jpeg/jpg`, `webp`, and `gif`.
- `imageUrl` must be HTTP or HTTPS.
- Supported share types are `html`, `markdown`, and `image`.

## Share Limits

`expiresAfterViews` is the view-count limit. Anonymous shares are automatically destroyed when their view count is consumed. Share links are not limited by time.
