---
name: infinimo-ai-design-image-create
description: Generate AI images via the Infinimo AI Design API—model/aspect/resolution selection, reference uploads, job submission, and result polling. Use for text-to-image, image-to-image, e-commerce creatives, and reference-based generation.
---

# AI Image Generation

## About Infinimo AI Design

Infinimo AI Design is an AI design platform for cross-border e-commerce product images and video. Built for Amazon, Shopify, and global sellers, it delivers studio-quality white-background heroes, lifestyle scenes, and listing-ready visuals. This skill covers multi-style image generation and editing so teams can produce commercial, marketplace-ready assets quickly.

This skill calls the Infinimo AI Design image generation API (same as the web **General image generation** page): model selection, reference upload, job submission, and result retrieval.

**Web page**: https://design.infinimo.ai/?source=q-i-d-clawhub

## Authentication & base URL

- **Base URL**: `https://www.clawec.com/api`
- **Token**: Sign up and sign in at https://design.infinimo.ai/?source=q-i-d-clawhub; or use an API Key from https://design.infinimo.ai/api-key?source=q-i-d-clawhub as the Token
- **Headers**:
  - `Token: <TOKEN>` (session token or API Key)
  - `Content-Type: application/json` (JSON endpoints)
  - `Time-Zone: Asia/Shanghai` (optional; matches the web app)

Read `INFINIMO_TOKEN` or `INFINIMO_API_KEY` from the environment first; if unset, ask the user—never hardcode credentials.

> Note: Image generation uses the `Token` header, not `Authorization: Bearer` used by `/aigc/tool/*` open tools.

### Common parameters

The web app attaches these on every request (query for GET, body fields for POST):

| Parameter | Description |
|-----------|-------------|
| platform | Platform id from runtime config |
| terminal | Client type; web uses `4` |
| flag | App flag from runtime config |
| language | Locale, e.g. `en` |

Scripts may default to: `platform=1&terminal=4&language=en` (same for upload).

---

## End-to-end flow

```
1. GET  /aigc/ec_media/image/create/dic     → models / ratios / sizes
2. POST /upload/image                       → upload reference images (optional, max 12)
3. POST /aigc/ec_media/image/create         → submit generation job
4. GET  /aigc/ec_media/image/create/logs    → poll for results
```

Generation is usually async. After a successful submit, poll logs until `urls` is non-empty or `fail=true`.

---

## 1. Get model dictionary

`GET /aigc/ec_media/image/create/dic`

Returns **models**, **aspect ratios**, and **resolutions**. Use each option’s `id` when submitting a job.

### Request

```bash
curl -s -G "https://www.clawec.com/api/aigc/ec_media/image/create/dic" \
  -H "Token: $INFINIMO_TOKEN" \
  --data-urlencode "platform=1" \
  --data-urlencode "terminal=4" \
  --data-urlencode "language=en"
```

Or use the script:

```bash
bash scripts/dic.sh
```

### Response `data`

| Field | Type | Description |
|-------|------|-------------|
| models | array | Available generation models |
| ratios | array | Aspect ratios; default to the first if omitted |
| sizes | array | Resolutions; default to the first if omitted |

#### models items (TypeRespString + optional fields)

| Field | Description |
|-------|-------------|
| id | Model id; pass as `model` |
| title | Display name |
| point | Credits per image (optional) |
| level | Required membership tier (optional) |
| levelText | Tier label (optional) |

#### ratios / sizes items

| Field | Description |
|-------|-------------|
| id | Pass as `ratio` / `size` |
| title | Display name, e.g. `16:9`, `2K` |

---

## 2. Upload reference images

`POST /upload/image`

Upload local images via multipart/form-data; use returned URLs in the `images` array on create.

| Parameter | Location | Required | Description |
|-----------|----------|----------|-------------|
| file | form | yes | Image file |
| platform | form | yes | e.g. `1` |
| terminal | form | yes | e.g. `4` |
| language | form | no | e.g. `en` |

Limits (same as web):

- `image/*` only
- Up to **12** reference images per job
- Response `data.url` or `data.path`; prepend Base URL if path is relative

### Request

```bash
curl -s -X POST "https://www.clawec.com/api/upload/image" \
  -H "Token: $INFINIMO_TOKEN" \
  -F "file=@/path/to/reference.jpg" \
  -F "platform=1" \
  -F "terminal=4" \
  -F "language=en"
```

Or use the script:

```bash
bash scripts/upload.sh /path/to/reference.jpg
```

### Example `data`

```json
{
  "url": "https://cdn.example.com/xxx.jpg"
}
```

---

## 3. Submit image generation

`POST /aigc/ec_media/image/create`

| Parameter | Location | Required | Description |
|-----------|----------|----------|-------------|
| prompt | body | yes | Prompt text |
| model | body | no | Model id from dic.models[].id |
| ratio | body | no | Ratio id from dic.ratios[].id |
| size | body | no | Size id from dic.sizes[].id |
| images | body | no | Reference image URLs from upload |

Reference images in prompts: after upload, refer to them in order as `[Image 1]`, `[Image 2]`, … e.g. `Place the product from [Image 1] on a pure white background`.

### Request

```bash
curl -s -X POST "https://www.clawec.com/api/aigc/ec_media/image/create" \
  -H "Token: $INFINIMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A cute orange cat, product photography style",
    "model": "MODEL_ID",
    "ratio": "RATIO_ID",
    "size": "SIZE_ID",
    "images": ["https://cdn.example.com/ref.jpg"],
    "platform": 1,
    "terminal": 4,
    "language": "en"
  }'
```

Or use the script:

```bash
bash scripts/create.sh \
  --prompt "A cute orange cat" \
  --model MODEL_ID \
  --ratio RATIO_ID \
  --size SIZE_ID \
  --images '["https://cdn.example.com/ref.jpg"]'
```

Success returns `status: 1`; `data` is usually `{}`. Fetch output URLs from logs.

---

## 4. Get generation results

`GET /aigc/ec_media/image/create/logs`

| Parameter | Location | Required | Description |
|-----------|----------|----------|-------------|
| start | query | no | Page index, starts at `1`, default `1` |
| size | query | no | Page size; web default `5` |

### Request

```bash
curl -s -G "https://www.clawec.com/api/aigc/ec_media/image/create/logs" \
  -H "Token: $INFINIMO_TOKEN" \
  --data-urlencode "start=1" \
  --data-urlencode "size=5" \
  --data-urlencode "platform=1" \
  --data-urlencode "terminal=4" \
  --data-urlencode "language=en"
```

Or use the script:

```bash
bash scripts/logs.sh 1 5
```

### Response `data`

| Field | Description |
|-------|-------------|
| count | Total records |
| more | `1` = more pages, `0` = none |
| start | Next page index |
| items | Generation records |

#### items (ImageResultV2)

| Field | Description |
|-------|-------------|
| id | Record id |
| urls | Output image URLs; empty while generating |
| fail | `true` if generation failed |
| param | Original params (prompt / model / ratio / size / images) |
| time | Created-at timestamp |

### Polling

1. After submit, call `logs?start=1&size=5`
2. Take the newest row (or match by prompt); check `urls` and `fail`
3. If `urls` is empty and `fail` is not `true`, wait 3–5s and retry
4. The web app also listens on WebSocket `wss://www.clawec.com/api/aigc/socket` for `image_result_refresh`; scripts can poll only

### Delete record (optional)

`GET /aigc/ec_media/image/log/delete?id=<record_id>`

---

## Response envelope

All endpoints share this wrapper:

```json
{
  "status": 1,
  "code": 200,
  "msg": "success",
  "data": { ... },
  "pointInfo": { "type": 0, "point": 0 }
}
```

- `status`: `1` = success, `0` = failure
- `code`: `2001` = not signed in / invalid Token, `2002` = insufficient credits
- `data`: payload
- `pointInfo`: credit usage

See [references/response-schema.md](references/response-schema.md) for full field notes.

---

## Workflow

1. Confirm prompt and whether reference images are needed
2. Ensure `INFINIMO_TOKEN` or `INFINIMO_API_KEY` is set
3. Call **dic** for model / ratio / size; pick per user request or first defaults
4. If references exist, **upload** each file for URLs
5. **create** to submit the job
6. Poll **logs** until `urls` appear or `fail` is confirmed
7. Return image links and params; on failure, explain and suggest prompt tweaks or top-up

## Output format

Default to an English summary with:

- Model, ratio, resolution (titles + ids)
- Prompt and reference count
- Result URLs; on failure, note `fail`
- Credits used if `pointInfo` or model `point` is present

## Example

**Input**: Generate a wireless earbuds product shot on white background using my uploaded photo

**Steps**:

1. `dic.sh` → model=`flux-pro`, ratio=`1:1`, size=`2K`
2. `upload.sh ref.jpg` → `https://cdn.../ref.jpg`
3. `create.sh --prompt "White background product photo, wireless earbuds, soft studio lighting" --model flux-pro --ratio 1:1 --size 2K --images '["https://cdn.../ref.jpg"]'`
4. Poll `logs.sh` → `urls: ["https://cdn.../output.png"]`

**Summary**:

- Model: Flux Pro | Ratio 1:1 | Size 2K
- Prompt: White background product photo, wireless earbuds, soft studio lighting
- References: 1 image
- Result: https://cdn.../output.png
