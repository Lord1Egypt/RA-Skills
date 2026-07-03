---
name: nishare-api
description: Use when the user wants to publish, update, or explain how to publish AI-generated HTML, image, or document content to Nishare via its API, needs curl examples, API-Key/Bearer authentication, 工作组 targeting, payload validation rules, or wants an agent prompt that returns a Nishare shareUrl.
metadata:
  short-description: Publish and update Nishare shares
---

# Nishare API

Use this skill when helping a user or another AI tool publish generated content to Nishare.

## Quick Workflow

1. Choose the base URL:
   - Production: `https://nishare.com`
2. Choose an endpoint:
   - Create a share: `POST /api/ai/publish`
   - Update an existing project: `POST /api/ai/update`
3. Choose content type:
   - HTML: full HTML document only
   - Markdown: document text
   - Image: `imageDataUrl`, `imageBase64`, or `imageUrl`
4. Add authentication only when publishing into an account/工作组 or updating:
   - `X-Nishare-Key: nsk_xxx`, or
   - `Authorization: Bearer nsk_xxx`
5. Return `shareUrl` to the user on success. On failure, surface `message` and any `matches`.

## Copyable Agent Prompt

Use this prompt when instructing another AI tool:

```text
把内容发布到 Nishare：POST https://nishare.com/api/ai/publish，成功后返回 shareUrl，失败时返回 message。
```

For full HTML pages:

```text
请把你生成的完整页面 HTML 通过 POST 发送到 https://nishare.com/api/ai/publish，JSON 格式为 {"title":"页面标题","type":"html","html":"完整页面 HTML"}，然后把响应里的 shareUrl 返回给我。
```

## Essential Examples

Publish HTML:

```bash
curl -s https://nishare.com/api/ai/publish \
  -H 'Content-Type: application/json' \
  -d '{"title":"AI 生成演示","type":"html","html":"<!doctype html><html><body><h1>Hello</h1></body></html>"}'
```

Publish with API Key:

```bash
curl -s https://nishare.com/api/ai/publish \
  -H 'Content-Type: application/json' \
  -H 'X-Nishare-Key: nsk_xxx' \
  -d '{"title":"AI 生成演示","type":"html","html":"<!doctype html><html><body><h1>Hello</h1></body></html>"}'
```

Update a project:

```bash
curl -s https://nishare.com/api/ai/update \
  -H 'Content-Type: application/json' \
  -H 'X-Nishare-Key: nsk_xxx' \
  -d '{"projectId":"project_id","title":"更新后的演示","type":"html","html":"<!doctype html><html><body><h1>Updated</h1></body></html>"}'
```

## Detailed Reference

Read [references/api.md](references/api.md) when you need:

- All accepted payload fields and headers
- Markdown, image, raw HTML, or text examples
- 工作组 targeting
- Response shapes
- Validation limits and common errors
