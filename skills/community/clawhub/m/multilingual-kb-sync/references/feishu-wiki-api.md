# Feishu Wiki API Reference

## Authentication

```bash
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"<APP_ID>","app_secret":"<APP_SECRET>"}'
```

Response: `{"tenant_access_token":"t-xxx","expire":7200}`

## Create Wiki Node

```
POST /open-apis/wiki/v2/spaces/{space_id}/nodes
```

Body:
```json
{
  "obj_type": "docx",
  "parent_node_token": "<optional>",
  "title": "Document Title"
}
```

## Add Blocks to Document

```
POST /open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children
```

Key block types:
- `2` — Text
- `3` — Heading 1
- `4` — Heading 2
- `5` — Heading 3
- `12` — Bullet list
- `13` — Ordered list
- `14` — Code
- `19` — Callout

## Markdown to Block Conversion

For production use, parse markdown and map:
- `# ` → block_type 3 (H1)
- `## ` → block_type 4 (H2)
- `### ` → block_type 5 (H3)
- `- ` → block_type 12 (bullet)
- fenced code → block_type 14
- plain text → block_type 2

## API Docs

- Wiki: https://open.feishu.cn/document/server-docs/docs/wiki-v2/space-node/create
- Docx blocks: https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document-block/create
