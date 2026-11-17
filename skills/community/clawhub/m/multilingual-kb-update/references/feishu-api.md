# Feishu Wiki API Reference

## Authentication

```bash
curl -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d '{"app_id":"<APP_ID>","app_secret":"<APP_SECRET>"}'
```

Response: `{"tenant_access_token":"t-xxx","expire":7200}`

## Get Wiki Node → Document ID

```bash
curl -X GET \
  "https://open.feishu.cn/open-apis/wiki/v2/spaces/<SPACE_ID>/nodes/<NODE_TOKEN>" \
  -H "Authorization: Bearer <TOKEN>"
```

`data.node.obj_token` is the `document_id` for docx API calls.

## Get Document Blocks

```bash
curl -X GET \
  "https://open.feishu.cn/open-apis/docx/v1/documents/<DOC_ID>/blocks" \
  -H "Authorization: Bearer <TOKEN>"
```

Use `page_token` for pagination. The last block's `block_id` is where to append.

## Create Blocks (Append Children)

```bash
curl -X POST \
  "https://open.feishu.cn/open-apis/docx/v1/documents/<DOC_ID>/blocks/<BLOCK_ID>/children" \
  -H "Authorization: Bearer <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{
    "children": [
      {
        "block_type": 4,
        "heading2": {
          "elements": [{"text_run": {"content": "🇫🇷 Français"}}]
        }
      },
      {
        "block_type": 2,
        "text": {
          "elements": [{"text_run": {"content": "Bonjour!..."}}]
        }
      }
    ]
  }'
```

Block types:
- `2` — Text paragraph
- `3` — Heading 1
- `4` — Heading 2
- `5` — Heading 3
- `14` — Divider

## Update Document Title (Optional)

```bash
curl -X PATCH \
  "https://open.feishu.cn/open-apis/docx/v1/documents/<DOC_ID>" \
  -H "Authorization: Bearer <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"title":"<new title>"}'
```

## Notes

- Feishu API rate limit: ~50 req/s per app. Batch block creation when possible (up to 50 children per request).
- For large updates, consider deleting and recreating the document rather than block-by-block updates.
- The Wiki API requires the app to be added as a member of the Wiki space with edit permission.
