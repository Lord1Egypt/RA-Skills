# PostNitro Carousel Skill Examples

Ready-to-use request bodies for common carousel creation scenarios.

## Examples Index

| File | Description |
|------|-------------|
| [generate-from-text.json](generate-from-text.json) | AI generation from user-provided text |
| [generate-from-article.json](generate-from-article.json) | AI generation from an article URL |
| [generate-from-x-post.json](generate-from-x-post.json) | AI generation from an X (Twitter) post |
| [import-default.json](import-default.json) | Basic carousel with custom slide content |
| [import-infographics.json](import-infographics.json) | Carousel with infographic grid and cycle layouts |

## Usage

### AI Generation Examples

Each generation JSON is a complete request body for `POST /post/initiate/generate`. Replace the placeholder IDs:
- `YOUR_TEMPLATE_ID` → your `$POSTNITRO_TEMPLATE_ID`
- `YOUR_BRAND_ID` → your `$POSTNITRO_BRAND_ID`
- `YOUR_PRESET_ID` → your `$POSTNITRO_PRESET_ID`

### Content Import Examples

Each import JSON is a complete request body for `POST /post/initiate/import`. Replace:
- `YOUR_TEMPLATE_ID` → your `$POSTNITRO_TEMPLATE_ID`
- `YOUR_BRAND_ID` → your `$POSTNITRO_BRAND_ID`

### After Initiating

All examples return `{ "success": true, "data": { "embedPostId": "...", "status": "PENDING" } }`.

Then:
1. Poll `GET /post/status/{embedPostId}` until status is `"COMPLETED"`
2. Download from `GET /post/output/{embedPostId}`

See [references/api-reference.md](../references/api-reference.md) for full response schemas.
