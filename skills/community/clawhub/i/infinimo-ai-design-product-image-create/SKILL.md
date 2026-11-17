---
name: infinimo-ai-design-product-image-create
description: Generate e-commerce product images (hero, secondary, A+ detail) via Infinimo AI Design—marketplace/platform selection, model/aspect/resolution, reference uploads, submit and poll. Use for Amazon/Shopify listing heroes, lifestyle shots, and A+ modules.
---

# Product Image Design

## About Infinimo AI Design

Infinimo AI Design is an AI design platform for cross-border e-commerce product images and video. This skill calls the product image API (same as the web **Product image design** pages under `/studio`).

**Web page**: https://design.infinimo.ai/?source=q-i-d-clawhub

Studio tool paths (after sign-in):

| Scene | Path |
|-------|------|
| Hero / main image | `/product-image-create?scene=cover` |
| Secondary images | `/product-image-create?scene=cover_other` |
| Detail / A+ | `/product-image-create?scene=detail` |

## Authentication & base URL

- **Base URL**: `https://www.clawec.com/api`
- **Token**: Sign up at https://design.infinimo.ai/?source=q-i-d-clawhub; API Key at https://design.infinimo.ai/api-key?source=q-i-d-clawhub
- **Headers**: `Token: <TOKEN>`, `Content-Type: application/json`, `Time-Zone: Asia/Shanghai` (optional)

Read `INFINIMO_TOKEN` or `INFINIMO_API_KEY` from the environment; never hardcode.

### Common parameters

`platform=1`, `terminal=4`, `language=en` on all requests.

---

## End-to-end flow

```
1. GET  /aigc/ec_product_media/platform_options   → target platforms & markets
2. GET  /aigc/ec_media/image/create/dic             → models / ratios / sizes
3. POST /upload/image                              → reference uploads (optional, max 12)
4. POST /aigc/ec_media/image/create                → submit product image job
5. GET  /aigc/ec_media/image/create/logs/product   → poll results
```

Poll until `urls` is non-empty or `fail=true`.

**vs general `image-create`:**

- **Required** `target_platform`; optional `region`
- **Required** `image_scene` (hero / secondary / detail)
- Results via **`/logs/product`**, not `/logs`
- **Prompt or references**: at least one required

---

## 1. Platform & market options

`GET /aigc/ec_product_media/platform_options`

```bash
bash scripts/platform_options.sh
```

| Field | Description |
|-------|-------------|
| code | Platform code → `target_platform` |
| name | e.g. Amazon, Shopee |
| regions[].code | Market code → `region` |
| regions[].name | e.g. United States, Japan |

---

## 2. Model dictionary

`GET /aigc/ec_media/image/create/dic` — same as general image generation.

```bash
bash scripts/dic.sh
```

---

## 3. Upload references

`POST /upload/image` — max **12** images, `image/*` only.

```bash
bash scripts/upload.sh /path/to/product.jpg
```

---

## 4. Submit product image generation

`POST /aigc/ec_media/image/create`

| Parameter | Required | Description |
|-----------|----------|-------------|
| target_platform | yes | Platform code from platform_options |
| image_scene | no | Default `cover` |
| region | no | Market code |
| prompt | conditional | At least prompt or `images` required |
| model, ratio, size | no | Dictionary ids |
| images | no | Reference URL array |

### image_scene values

| Value | Scene | Studio alias |
|-------|-------|--------------|
| cover | Hero / main | `?scene=cover` |
| cover_other | Secondary | `?scene=cover_other` |
| detail | Detail / A+ | `?scene=detail` |

Reference tags in prompt: `[Image 1]`, `[Image 2]`, …

```bash
bash scripts/create.sh \
  --target-platform amazon \
  --scene cover \
  --region US \
  --prompt "White background hero, wireless earbuds, pro e-commerce photo" \
  --model MODEL_ID --ratio RATIO_ID --size SIZE_ID \
  --images '["https://cdn.example.com/ref.jpg"]'
```

---

## 5. Poll results

`GET /aigc/ec_media/image/create/logs/product?start=1&size=5`

```bash
bash scripts/logs.sh 1 5
```

| items field | Description |
|-------------|-------------|
| urls | Output image URLs |
| fail | `true` on failure |
| param | Includes image_scene, target_platform, region |

Poll every 3–5s until `urls` appear. Optional WebSocket: `wss://www.clawec.com/api/aigc/socket` → `image_result_refresh`.

Delete: `GET /aigc/ec_media/image/log/delete?id=<id>`

See [references/response-schema.md](references/response-schema.md).

---

## Workflow

1. Confirm scene (hero/secondary/detail), platform, and market
2. Ensure token is set
3. **platform_options** → pick `target_platform` / `region`
4. **dic** → model / ratio / size
5. **upload** references if needed
6. **create** (prompt and/or images)
7. Poll **logs/product** and return URLs

## Example

**Input**: Amazon US hero image for wireless earbuds using uploaded product photo

1. `platform_options.sh` → `amazon`, `US`
2. `dic.sh` → model / ratio / size
3. `upload.sh product.jpg`
4. `create.sh --target-platform amazon --region US --scene cover --prompt "White hero, wireless earbuds" --images '[...]'`
5. `logs.sh` → output URL
