# PostNitro Embed API Reference

Base URL: `https://embed-api.postnitro.ai`
Auth: `embed-api-key` header with your PostNitro API key.

## Endpoints

### POST /post/initiate/generate

Generate a carousel using AI. Returns an `embedPostId` for async tracking.

**Headers:**
- `Content-Type: application/json`
- `embed-api-key: your-api-key` (required)

**Request Body:**

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `postType` | string | Yes | Type of post | `"CAROUSEL"` |
| `requestorId` | string | No | Custom tracking identifier | Any string |
| `templateId` | string | Yes | Template ID | Valid template ID |
| `brandId` | string | Yes | Brand configuration ID | Valid brand ID |
| `presetId` | string | Yes | AI preset ID | Valid preset ID |
| `responseType` | string | No | Output format (default: `"PDF"`) | `"PDF"`, `"PNG"` |
| `aiGeneration` | object | Yes | AI generation config | See below |

**aiGeneration Object:**

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `type` | string | Yes | Generation type | `"text"`, `"article"`, `"x"` |
| `context` | string | Yes | For `"text"`: text content. For `"article"`: article URL. For `"x"`: X post/thread URL. | Any string |
| `instructions` | string | No | Style/tone instructions | Any string |

**Response:**
```json
{
  "success": true,
  "message": "CAROUSEL generation initiated",
  "data": {
    "embedPostId": "post123",
    "status": "PENDING"
  }
}
```

Credit cost: 2 credits per slide.

---

### POST /post/initiate/import

Create a carousel by importing your own slide content. Returns an `embedPostId` for async tracking.

**Headers:**
- `Content-Type: application/json`
- `embed-api-key: your-api-key` (required)

**Request Body:**

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `postType` | string | Yes | Type of post | `"CAROUSEL"` |
| `requestorId` | string | No | Custom tracking identifier | Any string |
| `templateId` | string | Yes | Template ID | Valid template ID |
| `brandId` | string | Yes | Brand configuration ID | Valid brand ID |
| `responseType` | string | No | Output format (default: `"PDF"`) | `"PDF"`, `"PNG"` |
| `slides` | array | Yes | Array of slide objects | See below |

**Slide Structure:**

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `type` | string | Yes | Slide type | `"starting_slide"`, `"body_slide"`, `"ending_slide"` |
| `heading` | string | Yes | Main heading text | Any string |
| `sub_heading` | string | No | Subtitle text | Any string |
| `description` | string | No | Description text | Any string |
| `image` | string | No | Foreground image URL | Valid public URL |
| `background_image` | string | No | Background image URL | Valid public URL |
| `cta_button` | string | No | Call-to-action button text | Any string |
| `layoutType` | string | No | Slide layout | `"default"`, `"infographics"` |
| `layoutConfig` | object | No | Infographics config | See below |

**Slide Rules:**
- Exactly 1 `starting_slide` (required)
- At least 1 `body_slide` (required)
- Exactly 1 `ending_slide` (required)

**Infographics Layout Config:**

Set `layoutType` to `"infographic"` on a `body_slide` to replace the image area with structured data.

| Field | Type | Required | Description | Allowed Values |
|-------|------|----------|-------------|----------------|
| `columnCount` | number | Yes | Number of columns | `1`, `2`, `3` |
| `columnDisplay` | string | Yes | Layout mode | `"cycle"`, `"grid"` |
| `displayCounterAs` | string | Yes | Counter display | `"none"`, `"counter"` |
| `hasHeader` | boolean | Yes | Show column headers | `true`, `false` |
| `columnData` | array | No | Column content | See below |

**columnData items:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `header` | string | Yes | Column header text |
| `content` | array | Yes | Array of `{"title": "...", "description": "..."}` objects |

**Infographics notes:**
- `layoutType: "infographic"` replaces the slide image with the infographic
- Column count must not exceed 3
- Cyclical display (`"cycle"`) only uses data from the first column — no need to add data to columns 2+
- Grid display (`"grid"`) uses data from all columns

**Response:**
```json
{
  "success": true,
  "message": "CAROUSEL generation initiated",
  "data": {
    "embedPostId": "post123",
    "status": "PENDING"
  }
}
```

Credit cost: 1 credit per slide.

---

### GET /post/status/{embedPostId}

Check the status of a carousel generation request.

**Headers:**
- `embed-api-key: your-api-key` (required)

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `embedPostId` | string | Yes | ID from the initiate response |

**Response:**
```json
{
  "success": true,
  "data": {
    "embedPostId": "post123",
    "embedPost": {
      "id": "post123",
      "postType": "CAROUSEL",
      "status": "COMPLETED",
      "createdAt": "2026-02-19T21:11:50.115Z",
      "updatedAt": "2026-02-19T21:12:08.333Z"
    },
    "logs": [
      {
        "id": "log1",
        "embedPostId": "post123",
        "step": "INITIATED",
        "status": "SUCCESS",
        "message": "Post generation initiated",
        "timestamp": "2026-02-19T21:11:50.115Z"
      },
      {
        "id": "log2",
        "embedPostId": "post123",
        "step": "PROCESSING",
        "status": "SUCCESS",
        "message": "Content generated successfully",
        "timestamp": "2026-02-19T21:11:55.000Z"
      },
      {
        "id": "log3",
        "embedPostId": "post123",
        "step": "COMPLETED",
        "status": "SUCCESS",
        "message": "Post generation completed",
        "timestamp": "2026-02-19T21:12:08.333Z"
      }
    ]
  }
}
```

Poll every 3–5 seconds. Check `data.embedPost.status` for `"COMPLETED"`.

---

### GET /post/output/{embedPostId}

Retrieve the generated carousel output.

**Headers:**
- `embed-api-key: your-api-key` (required)

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `embedPostId` | string | Yes | ID from the initiate response |

**Response (PNG):**
```json
{
  "success": true,
  "data": {
    "embedPost": {
      "id": "post123",
      "postType": "CAROUSEL",
      "responseType": "PNG",
      "status": "COMPLETED",
      "credits": 4,
      "createdAt": "2026-02-19T21:11:50.115Z",
      "updatedAt": "2026-02-19T21:12:08.333Z"
    },
    "result": {
      "id": "result123",
      "name": "Welcome to the Carousel!",
      "size": {
        "id": "4:5",
        "dimensions": { "width": 1080, "height": 1350 }
      },
      "type": "png",
      "mimeType": "image/png",
      "data": [
        "https://...supabase.co/.../slide_0.png",
        "https://...supabase.co/.../slide_1.png"
      ]
    }
  }
}
```

**Response (PDF):**
```json
{
  "success": true,
  "data": {
    "embedPost": {
      "id": "post123",
      "postType": "CAROUSEL",
      "responseType": "PDF",
      "status": "COMPLETED",
      "credits": 10,
      "createdAt": "2026-02-19T21:11:50.115Z",
      "updatedAt": "2026-02-19T21:12:08.333Z"
    },
    "result": {
      "id": "result123",
      "name": "Welcome to the Carousel!",
      "size": {
        "id": "4:5",
        "dimensions": { "width": 1080, "height": 1350 }
      },
      "type": "pdf",
      "mimeType": "application/pdf",
      "data": "https://...supabase.co/.../output.pdf"
    }
  }
}
```

**Result object:**

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique result identifier |
| `name` | string | Design name (from template or "Untitled") |
| `size` | object | `{ "id": "4:5", "dimensions": { "width": 1080, "height": 1350 } }` |
| `type` | string | File type: `"png"` or `"pdf"` |
| `mimeType` | string | `"image/png"` or `"application/pdf"` |
| `data` | string or array | **PNG**: Array of URLs (one per slide). **PDF**: Single URL. |

Download the URLs directly to save the carousel files.

---

## Credits

| Plan | Price | Credits/Month |
|------|-------|---------------|
| Free | $0/month | 5 |
| Monthly | $10/month | 250+ (scalable multiplier 1–100) |

- Content import: 1 credit per slide
- AI generation: 2 credits per slide

## Support

- Documentation: https://postnitro.ai/docs/embed/api
- Get API Key: https://postnitro.ai/app/embed
- Postman Collection: https://www.postman.com/postnitro/postnitro-embed-apis/overview
- Email: support@postnitro.ai
