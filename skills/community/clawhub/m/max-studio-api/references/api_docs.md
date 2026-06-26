# 📖 API Integration Guide — Max Studio

> **Version:** 1.0 | **Updated:** 01-04-2026 | **Base URL:** `https://max-studio.store`
>
> Tài liệu này dành cho **đối tác tích hợp bên ngoài** (third-party integrators).  
> Tất cả endpoint đều yêu cầu header xác thực `X-API-Key` trừ khi ghi chú khác.

---

## 📋 Mục Lục

1. [Authentication](#1-authentication)
2. [Headers Chung](#2-headers-chung)
3. [check-apikey-status](#3-endpoint-check-apikey-status)
4. [create-task — Tổng quan](#4-endpoint-create-taskworker_endpoint)
   - [4.1 text-to-video](#41-text-to-video)
   - [4.2 text-to-image](#42-text-to-image)
   - [4.3 image-to-image](#43-image-to-image)
   - [4.4 image-to-video](#44-image-to-video)
   - [4.5 reference-images-to-video](#45-reference-images-to-video)
   - [4.6 start-end-image-to-video](#46-start-end-image-to-video)
   - [4.7 extend-video](#47-extend-video)
   - [4.8 upscale-video](#48-upscale-video)
   - [4.9 upscale-image](#49-upscale-image)
   - [4.10 upload-image](#410-upload-image)
5. [check-status/{task_id}](#5-endpoint-check-statustask_id)
6. [Response Format Chung](#6-response-format-chung)
7. [Error Codes & Messages](#7-error-codes--messages)

---

## 1. Authentication

Tất cả request phải kèm API Key trong header:

```
X-API-Key: <your_api_key>
```

Nếu thiếu hoặc sai → HTTP 401/403.

### Lấy API key ở đâu?

Nếu người dùng hỏi lấy API key ở đâu, hãy hướng dẫn rõ:

- vào `https://max-studio.shop`
- tự đăng ký hoặc đăng nhập tài khoản của họ
- tự lấy API key trong tài khoản đó

Không bịa thêm nguồn API key khác.

---

## 2. Headers Chung

| Header | Bắt buộc | Mô tả |
|--------|----------|-------|
| `X-API-Key` | ✅ | API Key xác thực user |
| `Content-Type` | ✅ (POST body) | `application/json` |

---

## 3. Endpoint: check-apikey-status

Kiểm tra trạng thái API Key, số dư, và giới hạn task.

```
POST /api/v1/check-apikey-status
```

**Headers:**
```
X-API-Key: <your_api_key>
```

> ⚠️ **Không cần body JSON.** API Key được đọc từ header `X-API-Key`.

**Response thành công (200):**
```json
{
  "status": "success",
  "balance": 150.5,
  "group": "pro",
  "task_limit": 5,
  "active_tasks": 2,
  "remaining_tasks": 3
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| `status` | string | `"success"` hoặc `"failed"` |
| `balance` | float | Số dư credits hiện tại |
| `group` | string | Nhóm user (`free`, `pro`, `ultra`, ...) |
| `task_limit` | int \| null | Giới hạn số task đồng thời (null = không giới hạn) |
| `active_tasks` | int | Số task đang chạy |
| `remaining_tasks` | int \| null | Task slot còn lại (null = không giới hạn) |

---

## 4. Endpoint: create-task/{worker_endpoint}

**URL Pattern:**
```
POST /api/v1/create-task/{worker_endpoint}
```

**Headers:**
```
X-API-Key: <your_api_key>
Content-Type: application/json
```

**Response chung khi tạo task thành công:**
```json
{
  "code": 200,
  "taskid": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "messages": "Task created successfully",
  "amount": 5.0,
  "balance": 145.5
}
```

> Sau khi nhận `taskid`, dùng [check-status](#5-endpoint-check-statustask_id) để poll kết quả.

---

### 4.1 text-to-video

Tạo video từ text prompt (Google Veo 3.1).

```
POST /api/v1/create-task/text-to-video
```

**Payload:**

```json
{
  "prompt": "A serene mountain landscape at sunrise with fog rolling through valleys",
  "ratio": "LANDSCAPE",
  "quantity": 1,
  "model": "Veo_3.1-Fast",
  "jwt": "<google_access_token>"
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `prompt` | string | ✅ | — | Mô tả video muốn tạo |
| `ratio` | string | ❌ | `LANDSCAPE` | Tỉ lệ khung hình |
| `quantity` | int | ❌ | `1` | Số video muốn tạo (1–4) |
| `model` | string | ❌ | `Veo_3.1-Fast` | Model Veo |
| `jwt` | string | ✅ | — | Google Access Token |

**`ratio` hợp lệ:**

| Giá trị | Mô tả |
|---------|-------|
| `LANDSCAPE` hoặc `16:9` | Nằm ngang — **mặc định** |
| `PORTRAIT` hoặc `9:16` | Dọc |

**`model` hợp lệ:**

| Model | Tier yêu cầu |
|-------|-------------|
| `Veo_3.1-Lite` | Tất cả |
| `Veo_3.1-Fast` | Tất cả — **mặc định** |
| `Veo_3.1-Quality` | PRO hoặc ULTRA |
| `Veo_3.1-Fast_Lower_Priority` | **ULTRA only** |

---

### 4.2 text-to-image

Tạo hình ảnh từ text prompt.

```
POST /api/v1/create-task/text-to-image
```

**Payload:**

```json
{
  "prompt": "A futuristic cityscape with neon lights reflecting in rain puddles",
  "ratio": "LANDSCAPE",
  "quantity": 2,
  "model": "Nano_Banana_Pro",
  "jwt": "<google_access_token>",
  "seed": 54321
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `prompt` | string | ✅ | — | Mô tả hình ảnh muốn tạo |
| `ratio` | string | ❌ | `LANDSCAPE` | Tỉ lệ khung hình |
| `quantity` | int | ❌ | `1` | Số ảnh muốn tạo (1–4) |
| `model` | string | ❌ | `Nano_Banana_Pro` | Model image generation |
| `jwt` | string | ✅ | — | Google Access Token |
| `seed` | int | ❌ | — | Seed 5 chữ số (10000–99999); chỉ áp dụng khi quantity=1 |

**`ratio` hợp lệ:**

| Giá trị | Mô tả |
|---------|-------|
| `16:9`, `landscape`, `auto` | Nằm ngang — **mặc định** |
| `4:3` | Nằm ngang (tỉ lệ 4:3) |
| `1:1`, `square` | Vuông |
| `3:4` | Dọc (tỉ lệ 3:4) |
| `9:16`, `portrait` | Dọc (tỉ lệ 9:16) |

**`model` hợp lệ:**

| Model | Mô tả |
|-------|-------|
| `Nano_Banana_Pro` | **Mặc định** |
| `Nano_Banana_2` | |
| `Imagen_4` | |

> ℹ️ `jwt` bắt buộc nhưng endpoint này **không tiêu Google Credit**.

---

### 4.3 image-to-image

Biến đổi ảnh dựa trên prompt.

```
POST /api/v1/create-task/image-to-image
```

**Payload:**

```json
{
  "prompt": "Transform into oil painting style with warm sunset colors",
  "mediaId": ["550e8400-e29b-41d4-a716-446655440002"],
  "ratio": "LANDSCAPE",
  "quantity": 1,
  "model": "Nano_Banana_Pro",
  "jwt": "<google_access_token>"
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `prompt` | string | ✅ | — | Mô tả biến đổi mong muốn |
| `mediaId` | string \| array | ✅ | — | UUID ảnh nguồn (tối đa 10) |
| `ratio` | string | ❌ | `LANDSCAPE` | Tỉ lệ khung hình |
| `quantity` | int | ❌ | `1` | Số ảnh muốn tạo (1–4) |
| `model` | string | ❌ | `Nano_Banana_Pro` | Model image generation |
| `jwt` | string | ✅ | — | Google Access Token |

**`ratio` hợp lệ:**

| Giá trị | Mô tả |
|---------|-------|
| `16:9`, `landscape`, `auto` | Nằm ngang — **mặc định** |
| `4:3` | Nằm ngang (tỉ lệ 4:3) |
| `1:1`, `square` | Vuông |
| `3:4` | Dọc (tỉ lệ 3:4) |
| `9:16`, `portrait` | Dọc (tỉ lệ 9:16) |

**`model` hợp lệ:**

| Model | Mô tả |
|-------|-------|
| `Nano_Banana_Pro` | **Mặc định** |
| `Nano_Banana_2` | |
| `Imagen_4` | |

**`mediaId` chấp nhận:** UUID

---

### 4.4 image-to-video

Tạo video từ ảnh + prompt.

```
POST /api/v1/create-task/image-to-video
```

**Payload:**

```json
{
  "prompt": "The character slowly turns to face the camera with a warm smile",
  "mediaId": ["550e8400-e29b-41d4-a716-446655440002"],
  "ratio": "LANDSCAPE",
  "quantity": 1,
  "model": "Veo_3.1-Fast",
  "jwt": "<google_access_token>"
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `prompt` | string | ✅ | — | Mô tả chuyển động mong muốn |
| `mediaId` | string \| array | ✅ | — | UUID ảnh nguồn |
| `ratio` | string | ❌ | `LANDSCAPE` | Tỉ lệ khung hình |
| `quantity` | int | ❌ | `1` | Số video (1–4) |
| `model` | string | ❌ | `Veo_3.1-Fast` | Model Veo |
| `jwt` | string | ✅ | — | Google Access Token |

**`ratio` hợp lệ:**

| Giá trị | Mô tả |
|---------|-------|
| `LANDSCAPE` hoặc `16:9` | Nằm ngang — **mặc định** |
| `PORTRAIT` hoặc `9:16` | Dọc |

**`model` hợp lệ:**

| Model | Tier yêu cầu |
|-------|-------------|
| `Veo_3.1-Lite` | Tất cả |
| `Veo_3.1-Fast` | Tất cả — **mặc định** |
| `Veo_3.1-Quality` | PRO hoặc ULTRA |
| `Veo_3.1-Fast_Lower_Priority` | **ULTRA only** |

**`mediaId` chấp nhận:** UUID

---

### 4.5 reference-images-to-video

Tạo video sử dụng tối đa 3 ảnh tham chiếu, hỗ trợ thêm giọng nói (audio).

```
POST /api/v1/create-task/reference-images-to-video
```

**Payload:**

```json
{
  "prompt": "A person walking through a cherry blossom garden",
  "mediaId": [
    "550e8400-e29b-41d4-a716-446655440002",
    "550e8400-e29b-41d4-a716-446655440003"
  ],
  "audio": "achernar",
  "ratio": "LANDSCAPE",
  "quantity": 1,
  "model": "Veo_3.1-Fast",
  "jwt": "<google_access_token>"
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `prompt` | string | ✅ | — | Mô tả video |
| `mediaId` | array | ✅ | — | Mảng UUID ảnh tham chiếu (tối đa **3**) |
| `audio` | string | ❌ | — | Voice ID âm thanh (xem danh sách dưới) |
| `ratio` | string | ❌ | `LANDSCAPE` | Tỉ lệ khung hình |
| `quantity` | int | ❌ | `1` | Số video (1–4) |
| `model` | string | ❌ | `Veo_3.1-Fast` | Model Veo |
| `jwt` | string | ✅ | — | Google Access Token |

**`ratio` hợp lệ:**

| Giá trị | Mô tả |
|---------|-------|
| `LANDSCAPE` hoặc `16:9` | Nằm ngang — **mặc định** |
| `PORTRAIT` hoặc `9:16` | Dọc |

**`model` hợp lệ:**

| Model | Tier yêu cầu |
|-------|-------------|
| `Veo_3.1-Fast` | Tất cả — **mặc định** |
| `Veo_3.1-Fast_Lower_Priority` | **ULTRA only** |

> ⚠️ Endpoint này **không hỗ trợ** `Veo_3.1-Quality` và `Veo_3.1-Lite`.

**`audio` — Danh sách voices hợp lệ:**

```
achernar, achird, algenib, algieba, alnilam, aoede, autonoe, callirrhoe, charon,
despina, enceladus, erinome, fenrir, gacrux, iapetus, kore, laomedeia, leda, orus,
puck, pulcherrima, rasalgethi, sadachbia, sadaltager, schedar, sulafat, umbriel,
vindemiatrix, zephyr, zubenelgenubi
```

> ℹ️ Nếu truyền `"none"` (string) → tự động set voice mặc định `"achernar"`.

---

### 4.6 start-end-image-to-video

Tạo video nội suy từ ảnh bắt đầu + ảnh kết thúc.

```
POST /api/v1/create-task/start-end-image-to-video
```

**Payload:**

```json
{
  "prompt": "Smooth transition from day to night",
  "start_image_media_id": "550e8400-e29b-41d4-a716-446655440010",
  "end_image_media_id": "550e8400-e29b-41d4-a716-446655440011",
  "ratio": "LANDSCAPE",
  "quantity": 1,
  "model": "Veo_3.1-Fast",
  "jwt": "<google_access_token>"
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `prompt` | string | ✅ | — | Mô tả chuyển tiếp |
| `start_image_media_id` | string | ✅ | — | UUID ảnh frame đầu |
| `end_image_media_id` | string | ✅ | — | UUID ảnh frame cuối |
| `ratio` | string | ❌ | `LANDSCAPE` | Tỉ lệ khung hình |
| `quantity` | int | ❌ | `1` | Số video (1–4) |
| `model` | string | ❌ | `Veo_3.1-Fast` | Model Veo |
| `jwt` | string | ✅ | — | Google Access Token |

**`ratio` hợp lệ:**

| Giá trị | Mô tả |
|---------|-------|
| `LANDSCAPE` hoặc `16:9` | Nằm ngang — **mặc định** |
| `PORTRAIT` hoặc `9:16` | Dọc |

**`model` hợp lệ:**

| Model | Tier yêu cầu |
|-------|-------------|
| `Veo_3.1-Lite` | Tất cả |
| `Veo_3.1-Fast` | Tất cả — **mặc định** |
| `Veo_3.1-Quality` | PRO hoặc ULTRA |
| `Veo_3.1-Fast_Lower_Priority` | **ULTRA only** |

---

### 4.7 extend-video

Kéo dài video ra thêm (theo giây).

```
POST /api/v1/create-task/extend-video
```

**Payload:**

```json
{
  "prompt": "Continue the movement naturally",
  "mediaId": "550e8400-e29b-41d4-a716-446655440020",
  "end_second": 8,
  "ratio": "LANDSCAPE",
  "quantity": 1,
  "model": "Veo_3.1-Fast",
  "jwt": "<google_access_token>"
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `prompt` | string | ✅ | — | Mô tả cách tiếp tục video |
| `mediaId` | string | ✅ | — | **UUID** video nguồn |
| `end_second` | int | ❌ | `8` | Giây kết thúc; `start_second` tự động = `end_second - 1` |
| `ratio` | string | ❌ | `LANDSCAPE` | Tỉ lệ khung hình |
| `quantity` | int | ❌ | `1` | Số video (1–4) |
| `model` | string | ❌ | `Veo_3.1-Fast` | Model Veo |
| `jwt` | string | ✅ | — | Google Access Token |

> ⚠️ **`mediaId` của extend-video chỉ chấp nhận UUID** — không dùng direct URL.

**`ratio` hợp lệ:**

| Giá trị | Mô tả |
|---------|-------|
| `LANDSCAPE` hoặc `16:9` | Nằm ngang — **mặc định** |
| `PORTRAIT` hoặc `9:16` | Dọc |

**`model` hợp lệ:**

| Model | Tier yêu cầu |
|-------|-------------|
| `Veo_3.1-Lite` | Tất cả |
| `Veo_3.1-Fast` | Tất cả — **mặc định** |
| `Veo_3.1-Quality` | PRO hoặc ULTRA |
| `Veo_3.1-Fast_Lower_Priority` | **ULTRA only** |

---

### 4.8 upscale-video

Nâng cấp độ phân giải video.

```
POST /api/v1/create-task/upscale-video
```

**Payload:**

```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440030",
  "resolution": "1080P",
  "ratio": "LANDSCAPE",
  "jwt": "<google_access_token>"
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `media_id` | string | ✅ | — | UUID video cần upscale |
| `resolution` | string | ❌ | `1080P` | Độ phân giải output |
| `ratio` | string | ❌ | `LANDSCAPE` | Tỉ lệ khung hình |
| `jwt` | string | ✅ | — | Google Access Token |

**`resolution` hợp lệ:**

| Giá trị | Tier yêu cầu | Mô tả |
|---------|-------------|-------|
| `1080P` | PRO, ULTRA | Full HD — **mặc định** |
| `4K` | **ULTRA only** | 4K Ultra HD |

**`ratio` hợp lệ:**

| Giá trị | Mô tả |
|---------|-------|
| `LANDSCAPE` hoặc `16:9` | Nằm ngang — **mặc định** |
| `PORTRAIT` hoặc `9:16` | Dọc |

> ⚠️ **Free tier không được dùng endpoint này.**

---

### 4.9 upscale-image

Nâng cấp độ phân giải ảnh.

```
POST /api/v1/create-task/upscale-image
```

**Payload:**

```json
{
  "media_id": "550e8400-e29b-41d4-a716-446655440031",
  "resolution": "2K",
  "jwt": "<google_access_token>"
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `media_id` | string | ✅ | — | **UUID** ảnh cần upscale |
| `resolution` | string | ❌ | `2K` | Độ phân giải output |
| `jwt` | string | ✅ | — | Google Access Token |

**`resolution` hợp lệ:**

| Giá trị | Mô tả |
|---------|-------|
| `2K` | **Mặc định** |
| `4K` | |

---

### 4.10 upload-image

Upload ảnh lên hệ thống, trả về `mediaId` để dùng cho các endpoint khác.

```
POST /api/v1/create-task/upload-image
```

**Payload:**

```json
{
  "image_path": "https://example.com/photo.jpg",
  "jwt": "<google_access_token>",
  "ratio": "auto"
}
```

| Field | Type | Bắt buộc | Mặc định | Mô tả |
|-------|------|----------|----------|-------|
| `image_path` | string | ✅ | — | URL của ảnh cần upload |
| `jwt` | string | ✅ | — | Google Access Token |
| `ratio` | string | ❌ | `auto` | Tỉ lệ (mặc định `auto`) |

> ℹ️ Endpoint này **đồng bộ** — response trả ngay kết quả, không cần poll check-status.

**Response:**
```json
{
  "code": 200,
  "taskid": "550e8400-...",
  "status": "completed",
  "messages": "Image uploaded successfully",
  "result": "<mediaId_uuid>"
}
```

---

## 5. Endpoint: check-status/{task_id}

Poll trạng thái task sau khi tạo.

```
GET /api/v1/check-status/{task_id}
```

**Headers:**
```
X-API-Key: <your_api_key>
```

**Ví dụ:**
```
GET /api/v1/check-status/550e8400-e29b-41d4-a716-446655440000
```

### Response: PENDING (chưa xong)

```json
{
  "code": 200,
  "status": "pending",
  "taskid": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Response: COMPLETED (thành công)

```json
{
  "code": 200,
  "status": "successfully",
  "taskid": "550e8400-e29b-41d4-a716-446655440000",
  "messages": "Task completed",
  "amount": 5.0,
  "balance": 145.5,
  "result": "https://cdn.example.com/video/output.mp4"
}
```

### Response: FAILED (thất bại)

```json
{
  "code": 200,
  "status": "failed",
  "taskid": "550e8400-e29b-41d4-a716-446655440000",
  "messages": "JWT has expired!",
  "amount": 0,
  "balance": 150.5
}
```

| Field | Type | Mô tả |
|-------|------|-------|
| `code` | int | Luôn là `200` |
| `status` | string | `pending` \| `processing` \| `successfully` \| `failed` |
| `taskid` | string | UUID của task |
| `messages` | string | Mô tả kết quả (chỉ có khi completed/failed) |
| `amount` | float | Chi phí đã trừ (chỉ có khi completed/failed) |
| `balance` | float | Số dư sau khi thực hiện (chỉ có khi completed/failed) |
| `result` | string \| object | URL media hoặc data kết quả (chỉ có khi successfully) |

> 💡 **Khuyến nghị polling:** Cứ 3–5 giây poll một lần. Không poll quá nhanh (< 1s).

---

## 6. Response Format Chung

### Create Task Response

```json
{
  "code": 200,
  "taskid": "<uuid>",
  "status": "pending",
  "messages": "<optional message>",
  "amount": 5.0,
  "balance": 145.5,
  "result": null
}
```

### Check Status Response

```json
{
  "code": 200,
  "status": "successfully | pending | processing | failed",
  "taskid": "<uuid>",
  "messages": "<optional>",
  "amount": 5.0,
  "balance": 145.5,
  "result": "<url or data>"
}
```

---

> 📬 **Hỗ trợ tích hợp:** Liên hệ team kỹ thuật để được cấp API Key và hỗ trợ integration.

---

## 7. Error Codes & Messages

### JWT / Authentication Errors

| Message | Nguyên nhân | Xử lý |
|---------|------------|-------|
| `JWT required` | Không truyền `jwt` | Thêm `jwt` vào body |
| `JWT has expired!` | JWT Google hết hạn hoặc không hợp lệ | Refresh access token |
| `Credit = 0, provide new JWT with enough credit to create media` | Google account hết credit | Dùng account Google còn credit |
| `JWT invalid or the balance is too low, please provide new JWT and try again` | Credit ≤ 10 | Dùng account Google còn đủ credit |

### Model / Tier Errors

| Message | Nguyên nhân | Xử lý |
|---------|------------|-------|
| `Veo_3.1-Fast_Lower_Priority is only available for ULTRA (PAYGATE_TIER_TWO) accounts` | Dùng Lower Priority nhưng không phải ULTRA | Upgrade lên ULTRA hoặc đổi model |
| `Veo_3.1-Quality is not available for Free tier` | Free tier dùng Quality model | Upgrade lên PRO/ULTRA |
| `Model input invalid with PRO or FREE tier` | PRO/Free gửi model không được phép | Bỏ field `model` hoặc upgrade |
| `Free tier cannot upscale video` | Free tier dùng upscale-video | Upgrade lên PRO/ULTRA |
| `Your resolution invalid, free / pro tier just can use "1080P" resolution` | PRO/Free dùng 4K upscale | Đổi sang `1080P` hoặc upgrade ULTRA |

### Validation Errors

| Message | Nguyên nhân | Xử lý |
|---------|------------|-------|
| `prompt is required for {endpoint}` | Thiếu prompt | Thêm `prompt` vào body |
| `mediaId is required for {endpoint}` | Thiếu mediaId | Thêm `mediaId` |
| `media_id is required for {endpoint}` | Thiếu media_id (upscale) | Thêm `media_id` |
| `start_image_media_id is required for start_end_image_to_video` | Thiếu ảnh frame đầu | Thêm `start_image_media_id` |
| `end_image_media_id is required for start_end_image_to_video` | Thiếu ảnh frame cuối | Thêm `end_image_media_id` |
| `start_second invalid, try again` | `start_second != end_second - 1` | Sửa lại giá trị hoặc bỏ `start_second` |
| `mediaId không được là direct link` | extend-video nhận URL thay vì UUID | Dùng UUID cho mediaId của extend-video |
| `audio invalid. Must be one of: ...` | Voice không hợp lệ | Dùng voice trong danh sách |
| `ratio invalid, it must be 2:3, 3:2, 1:1, 9:16, 16:9` | Grok ratio không hợp lệ | Dùng ratio đúng cho Grok |
| `resolution invalid, it must be 480p or 720p` | Grok resolution không hợp lệ | Dùng `480p` hoặc `720p` |
| `videoLength invalid, it must be 6 or 10` | videoLength không đúng | Dùng `6` hoặc `10` |
| `type is required and must be 'image' or 'video'` | Captcha endpoint thiếu type | Truyền `"type": "image"` hoặc `"video"` |

### Balance Errors

| Message | Nguyên nhân | Xử lý |
|---------|------------|-------|
| `Insufficient balance. Current: X credits, Required: Y credits.` | Số dư không đủ | Nạp tiền trước khi tạo task |
| `Worker endpoint 'X' not found or inactive` | Endpoint bị tắt | Liên hệ admin |
