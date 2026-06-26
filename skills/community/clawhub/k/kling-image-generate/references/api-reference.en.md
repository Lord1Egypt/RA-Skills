# Kling Image Generation API Reference

Detailed API documentation for reference when needed.

## Environment Variables

```bash
export KLING_ACCESS_KEY="your_access_key"
export KLING_SECRET_KEY="your_secret_key"
```

## API Endpoint

```
https://api-beijing.klingai.com
```

## Authentication

Generate JWT Token using Access Key and Secret Key.

**Request Headers:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

---

## 1. Image Generation

Standard text-to-image and image-to-image interface.

**Endpoint:** `POST /v1/images/generations`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model_name` | string | Yes | Model: kling-v1, kling-v1-5, kling-v2, kling-v2-new, kling-v2-1, kling-v3 |
| `prompt` | string | Yes | Positive prompt, max 2500 characters |
| `negative_prompt` | string | No | Negative prompt |
| `image` | string | No | Reference image (URL or Base64) |
| `image_reference` | string | No | Reference type: subject, face |
| `image_fidelity` | float | No | Image reference strength [0,1] |
| `human_fidelity` | float | No | Face reference strength [0,1], subject type only |
| `element_list` | array | No | Subject reference list |
| `resolution` | string | No | Resolution: 1k, 2k (default: 1k) |
| `n` | int | No | Number of images [1,9] (default: 1) |
| `aspect_ratio` | string | No | Aspect ratio: 16:9, 9:16, 1:1, 4:3, 3:4, 3:2, 2:3, 21:9 (default: 16:9) |
| `watermark_info` | object | No | Watermark `{"enabled": true}` |
| `callback_url` | string | No | Callback URL |
| `external_task_id` | string | No | Custom task ID |

### Query Tasks

- Single task: `GET /v1/images/generations/{id}`
- Task list: `GET /v1/images/generations?pageNum=1&pageSize=30`

---

## 2. Omni-Image

Advanced image generation with multi-image reference and subject reference.

**Endpoint:** `POST /v1/images/omni-image`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model_name` | string | Yes | kling-image-o1, kling-v3-omni |
| `prompt` | string | Yes | Prompt, supports `<<<image_1>>>` format |
| `image_list` | array | No | Reference images, max 10 |
| `element_list` | array | No | Subject reference list |
| `resolution` | string | No | 1k, 2k, 4k (default: 1k) |
| `result_type` | string | No | Result type: single, series (default: single) |
| `n` | int | No | Number of images [1,9], invalid for series |
| `series_amount` | int | No | Series count [2,9], valid for series |
| `aspect_ratio` | string | No | Aspect ratio |
| `watermark_info` | object | No | Watermark info |
| `callback_url` | string | No | Callback URL |
| `external_task_id` | string | No | Custom task ID |

### Query Tasks

- Single task: `GET /v1/images/omni-image/{id}`
- Task list: `GET /v1/images/omni-image?pageNum=1&pageSize=30`

---

## 3. Image Expansion

Intelligently expand image boundaries.

**Endpoint:** `POST /v1/images/editing/expand`

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | string | Yes | Reference image (URL or Base64) |
| `up_expansion_ratio` | float | Yes | Up expansion ratio [0,2], based on original height |
| `down_expansion_ratio` | float | Yes | Down expansion ratio [0,2], based on original height |
| `left_expansion_ratio` | float | Yes | Left expansion ratio [0,2], based on original width |
| `right_expansion_ratio` | float | Yes | Right expansion ratio [0,2], based on original width |
| `prompt` | string | No | Positive prompt |
| `n` | int | No | Number of images [1,9] |
| `watermark_info` | object | No | Watermark info |
| `callback_url` | string | No | Callback URL |
| `external_task_id` | string | No | Custom task ID |

**Limit:** New image area must not exceed 3x original area.

### Query Tasks

- Single task: `GET /v1/images/editing/expand/{id}`
- Task list: `GET /v1/images/editing/expand?pageNum=1&pageSize=30`

---

## Other APIs

### 4. Multi Image to Image

**Endpoint:** `POST /v1/images/multi-image-to-image`

### 5. AI Multi Shot

**Endpoint:** `POST /v1/images/ai-multishot`

### 6. Virtual Try-On

**Endpoint:** `POST /v1/images/virtual-try-on`

---

## Task Status

| Status | Description |
|--------|-------------|
| `submitted` | Task submitted |
| `processing` | Processing |
| `succeed` | Success |
| `failed` | Failed |

## Image Constraints

- **Format:** jpg, jpeg, png
- **Size:** Max 10MB
- **Dimensions:** Min 300px
- **Aspect Ratio:** 1:2.5 ~ 2.5:1
- **Base64:** Do not add `data:image/png;base64,` prefix

---

[← Back to SKILL.md](../SKILL.en.md) | [中文版](../SKILL.md)
