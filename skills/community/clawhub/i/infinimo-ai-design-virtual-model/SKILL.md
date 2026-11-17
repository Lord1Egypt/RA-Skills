---
name: infinimo-ai-design-virtual-model
description: Generate virtual model showcase images via Infinimo AI Design from a source photo, optional background, and prompts. Use for fashion lookbooks, model swaps, and on-model product presentation without a live shoot.
---

# Virtual Model

## About Infinimo AI Design

Infinimo AI Design is an AI design platform for e-commerce visuals. This skill calls the **Virtual model** tool (same as `/virtual-model` in the design studio).

**Web page**: https://design.infinimo.ai/?source=q-i-d-clawhub

## Authentication & base URL

- **Base URL**: `https://www.clawec.com/api`
- **Token**: https://design.infinimo.ai/?source=q-i-d-clawhub · https://design.infinimo.ai/api-key?source=q-i-d-clawhub
- **Headers**: `Token: <TOKEN>`

Use `INFINIMO_TOKEN` or `INFINIMO_API_KEY`. Common params: `platform=1`, `terminal=4`, `language=en`.

---

## End-to-end flow

```
1. POST /upload/image                          → upload source (and optional background)
2. GET  /aigc/image/virtual_model_create       → submit generation job
3. GET  /aigc/log/list?type=101                → poll results (log type 101)
```

Generation is async; poll logs until output images appear in the newest record.

---

## 1. Upload images

`POST /upload/image`

| Image | Required | Description |
|-------|----------|-------------|
| Source / base | yes | Real person or mannequin photo |
| Background | no | Optional scene reference |

```bash
bash scripts/upload.sh /path/to/source.jpg
bash scripts/upload.sh /path/to/background.jpg
```

---

## 2. Submit virtual model generation

`GET /aigc/image/virtual_model_create`

| Parameter | Required | Description |
|-----------|----------|-------------|
| base_image_url | yes | Source image URL |
| base_image_type | yes | `1` = real person, `2` = mannequin |
| bg_image_url | no | Background reference URL |
| prompt | no | Model look / styling prompt |
| face_prompt | no | Face-specific prompt |
| num | no | Output count, e.g. `1`–`4` |
| aspect_radio | no | Aspect ratio (H:W), e.g. `1:1`, `9:16`, `比例不变` (keep original) |

Allowed aspect values include: `比例不变`, `2:1`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `1:2`.

```bash
bash scripts/create.sh \
  --base-url "https://cdn.../source.jpg" \
  --base-type 1 \
  --bg-url "https://cdn.../bg.jpg" \
  --prompt "Professional fashion model, studio lighting" \
  --face-prompt "Natural smile, soft makeup" \
  --num 1 \
  --aspect "9:16"
```

---

## 3. Poll results

`GET /aigc/log/list`

| Parameter | Value | Description |
|-----------|-------|-------------|
| type | `101` | Virtual model log type |
| agent_id | `0` | Default |
| group_id | `0` | Default |

```bash
bash scripts/logs.sh
```

### Response `data.logs[]`

| Field | Description |
|-------|-------------|
| logId | Record id |
| createTime | Timestamp |
| param | Submit parameters |
| data.type | `image` when complete |
| data.data | Output image URL array |

Poll every 3–5s until the latest log has `data.type === "image"` and non-empty `data.data`.

Delete: `GET /aigc/log/delete?log_id=<logId>`

See [references/response-schema.md](references/response-schema.md).

---

## Workflow

1. Confirm source type (real person vs mannequin) and prompts
2. **upload** source and optional background
3. **create** with URLs and options
4. Poll **logs** (type 101) until images return
5. Return output URLs and parameters

## Example

**Input**: Generate 9:16 showcase from mannequin photo with luxury boutique background

1. `upload.sh mannequin.jpg` → base URL
2. `upload.sh boutique.jpg` → bg URL
3. `create.sh --base-url ... --base-type 2 --bg-url ... --aspect 9:16 --prompt "Luxury boutique fashion shoot"`
4. `logs.sh` → image URLs
