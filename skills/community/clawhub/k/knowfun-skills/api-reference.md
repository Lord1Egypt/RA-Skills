# Knowfun.io OpenAPI Reference

English | [简体中文](api-reference_CN.md)

Complete API documentation for the Knowfun.io OpenAPI.

## Base URL

```
https://api.knowfun.io
```

## Authentication

All requests require an API key passed as a Bearer token:

```bash
Authorization: Bearer kf_your_api_key_here
```

## Endpoints

### 1. Create Task

Create a content generation task.

**Endpoint:** `POST /api/openapi/v1/tasks`

**Headers:**
```
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

**Request Body:**
```json
{
  "requestId": "unique-request-id-123",
  "taskType": "course",
  "material": {
    "text": "Content to process",
    "url": "https://example.com/document.pdf",
    "type": "pdf"
  },
  "config": {
    "course": {
      "contentStyle": "concise",
      "contentLanguage": "zh",
      "explainLanguage": "zh"
    }
  },
  "callbackUrl": "https://your-server.com/callback",
  "language": "zh"
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| requestId | string | ✅ | Unique request ID (1-64 chars) for idempotency |
| taskType | string | ✅ | Task type: course, poster, game, film |
| material.text | string | * | Text content (either text or url required) |
| material.url | string | * | Document/webpage URL (either text or url required) |
| material.type | string | ❌ | Material type: text, url, pdf, doc, docx, ppt, pptx, txt |
| config | object | ❌ | Task-specific configuration |
| callbackUrl | string | ❌ | Callback URL for task completion |
| language | string | ❌ | Language setting (default: en) |

**Response:**
```json
{
  "success": true,
  "data": {
    "taskId": "c3199fb3-350b-4981-858d-09b949bfae88",
    "requestId": "unique-request-id-123",
    "status": "pending",
    "createdAt": "2026-03-01T10:00:00.000Z"
  }
}
```

---

### 2. Get Task Status (by taskId)

**Endpoint:** `GET /api/openapi/v1/tasks/:taskId`

**Headers:**
```
Authorization: Bearer <API_KEY>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "taskId": "c3199fb3-350b-4981-858d-09b949bfae88",
    "requestId": "unique-request-id-123",
    "taskType": "course",
    "status": "success",
    "progress": 100,
    "resultUrl": "https://r2.knowfun.io/courses/xxx.html",
    "resultData": {
      "title": "Course Title",
      "type": "ppt",
      "slidesCount": 12
    },
    "creditsUsed": 100,
    "createdAt": "2026-03-01T10:00:00.000Z",
    "completedAt": "2026-03-01T10:03:00.000Z"
  }
}
```

---

### 3. Get Task Status (by requestId)

**Endpoint:** `GET /api/openapi/v1/tasks/by-request/:requestId`

**Headers:**
```
Authorization: Bearer <API_KEY>
```

**Response:** Same as Get Task Status above.

---

### 4. Get Task Detail

Get detailed task information including full results.

**Endpoint:** `GET /api/openapi/v1/tasks/:taskId/detail`

**Query Parameters:**
- `verbose` (boolean, optional): Return full details including logs and metadata

**Headers:**
```
Authorization: Bearer <API_KEY>
```

**Response (course):**
```json
{
  "success": true,
  "data": {
    "taskId": "...",
    "requestId": "...",
    "taskType": "course",
    "status": "completed",
    "progress": 100,
    "result": {
      "title": "Course Title",
      "coverUrl": "https://r2.knowfun.io/covers/xxx.png",
      "course": {
        "url": "https://r2.knowfun.io/courses/xxx.html",
        "type": "ppt",
        "slidesCount": 12,
        "totalDuration": 180000
      },
      "pages": [
        {
          "pageNumber": 1,
          "title": "Slide 1",
          "content": "Content text...",
          "ttsText": "TTS narration...",
          "html": "<div>...</div>",
          "audioUrl": "https://r2.knowfun.io/audio/xxx.mp3",
          "duration": 15000,
          "status": "completed"
        }
      ]
    },
    "createdAt": "2026-03-01T10:00:00.000Z",
    "completedAt": "2026-03-01T10:03:00.000Z",
    "duration": 180000
  }
}
```

**Response (poster):**
```json
{
  "success": true,
  "data": {
    "taskType": "poster",
    "status": "completed",
    "result": {
      "posterUrl": "https://r2.knowfun.io/posters/xxx.png",
      "title": "Poster Title"
    }
  }
}
```

**Response (game):**
```json
{
  "success": true,
  "data": {
    "taskType": "game",
    "status": "completed",
    "result": {
      "codeUrl": "https://r2.knowfun.io/games/xxx.html",
      "coverUrl": "https://r2.knowfun.io/covers/xxx.png",
      "title": "Game Title"
    }
  }
}
```

**Response (film):**
```json
{
  "success": true,
  "data": {
    "taskType": "film",
    "status": "completed",
    "result": {
      "videoUrl": "https://r2.knowfun.io/videos/xxx.mp4",
      "coverUrl": "https://r2.knowfun.io/covers/xxx.png",
      "title": "Film Title"
    }
  }
}
```

---

### 5. List Tasks

Get a list of your tasks with pagination and filters.

**Endpoint:** `GET /api/openapi/v1/tasks`

**Query Parameters:**
- `limit` (integer, default: 20): Number of tasks per page
- `offset` (integer, default: 0): Offset for pagination
- `taskType` (string, optional): Filter by task type (course, poster, game, film)
- `status` (string, optional): Filter by status

**Headers:**
```
Authorization: Bearer <API_KEY>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "tasks": [
      {
        "taskId": "...",
        "requestId": "...",
        "taskType": "course",
        "status": "success",
        "createdAt": "2026-03-01T10:00:00.000Z"
      }
    ],
    "total": 100,
    "limit": 20,
    "offset": 0
  }
}
```

---

### 6. Get Credits Balance

**Endpoint:** `GET /api/openapi/v1/credits/balance`

**Headers:**
```
Authorization: Bearer <API_KEY>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "available": 1000,
    "earned": 1500,
    "used": 400,
    "locked": 100
  }
}
```

---

### 7. Get Credits Pricing

**Endpoint:** `GET /api/openapi/v1/credits/pricing`

**Headers:**
```
Authorization: Bearer <API_KEY>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "course": {
      "credits": 100,
      "description": "Generate course costs 100 credits"
    },
    "poster": {
      "credits": 100,
      "description": "Generate poster costs 100 credits"
    },
    "game": {
      "credits": 100,
      "description": "Generate game costs 100 credits"
    },
    "film": {
      "credits": 100,
      "description": "Generate film costs 100 credits"
    }
  }
}
```

---

### 8. Get Credit Usage

Get detailed credit usage history.

**Endpoint:** `GET /api/openapi/usage`

**Query Parameters:**
- `page` (integer, default: 1): Page number
- `pageSize` (integer, default: 10, max: 100): Items per page
- `taskType` (string, optional): Filter by task type
- `status` (string, optional): Filter by status
- `startDate` (string, optional): Start date (YYYY-MM-DD)
- `endDate` (string, optional): End date (YYYY-MM-DD)

**Headers:**
```
Authorization: Bearer <API_KEY>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "records": [
      {
        "taskId": "...",
        "requestId": "...",
        "taskType": "course",
        "status": "success",
        "creditsUsed": 100,
        "resultUrl": "...",
        "createdAt": "2026-03-01T10:00:00.000Z",
        "completedAt": "2026-03-01T10:03:00.000Z"
      }
    ],
    "pagination": {
      "page": 1,
      "pageSize": 10,
      "total": 100,
      "totalPages": 10
    },
    "summary": {
      "totalCreditsUsed": 1000,
      "taskCount": 10,
      "byTaskType": {
        "course": { "count": 5, "credits": 500 },
        "poster": { "count": 3, "credits": 300 },
        "game": { "count": 2, "credits": 200 }
      },
      "byStatus": {
        "success": { "count": 8, "credits": 800 },
        "failed": { "count": 2, "credits": 200 }
      }
    }
  }
}
```

---

### 9. Get Configuration Schema

Get available configuration options for all task types.

**Endpoint:** `GET /api/openapi/v1/schema`

**Response:**
```json
{
  "success": true,
  "data": {
    "poster": {
      "usage": {
        "default": "infographic",
        "options": [
          {
            "value": "infographic",
            "label": "Infographic",
            "labelZh": "知识图解",
            "description": "Structured infographic style...",
            "descriptionZh": "结构化信息图风格...",
            "recommended": true
          }
        ]
      },
      "style": { ... },
      "aspectRatio": { ... }
    },
    "game": { ... },
    "film": { ... },
    "course": { ... }
  }
}
```

---

## Task Status Values

| Status | Description |
|--------|-------------|
| pending | Task is queued |
| processing | Task is being processed |
| parsing | Parsing input material |
| generating | Generating content |
| completed / success | Task completed successfully |
| failed | Task failed |
| cancelled | Task was cancelled |

---

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_API_KEY | 401 | Invalid API key |
| API_KEY_EXPIRED | 401 | API key has expired |
| API_KEY_REVOKED | 401 | API key has been revoked |
| OPENAPI_NOT_ENABLED | 403 | OpenAPI not enabled for user |
| RATE_LIMIT_EXCEEDED | 429 | Rate limit exceeded |
| DAILY_LIMIT_EXCEEDED | 429 | Daily limit exceeded |
| TASK_TYPE_NOT_ALLOWED | 403 | Task type not allowed |
| INSUFFICIENT_CREDITS | 402 | Insufficient credits |
| INVALID_REQUEST_ID | 400 | Invalid request ID |
| DUPLICATE_REQUEST_ID | 400 | Duplicate request ID |
| INVALID_TASK_TYPE | 400 | Invalid task type |
| INVALID_MATERIAL | 400 | Invalid material parameters |
| MATERIAL_PARSE_FAILED | 400 | Failed to parse material |
| TASK_NOT_FOUND | 404 | Task not found |
| TASK_PROCESSING_FAILED | 500 | Task processing failed |
| INTERNAL_ERROR | 500 | Internal server error |

---

## Configuration Details

### Course Configuration

```typescript
{
  contentStyle?: 'detailed' | 'concise' | 'conversational',
  contentLanguage?: string,  // e.g., 'zh', 'en'
  explainLanguage?: string,  // e.g., 'zh', 'en'
  voiceType?: string,        // Standard voice types from schema
  ttsStyle?: string,         // e.g., 'classroom', from schema
  generateMethod?: string,   // e.g., 'llm'
  focusOnDocument?: boolean,
  userRequirement?: string   // Custom requirements
}
```

### Poster Configuration

```typescript
{
  usage?: 'infographic' | 'businessReports' | 'marketing' | 'illustration',
  style?: 'handDrawn' | 'photorealistic' | 'anime' | 'sciFi' | 'custom',
  customStylePrompt?: string,  // Required if style is 'custom'
  aspectRatio?: '1:1' | '4:3' | '3:4' | '16:9' | '9:16',
  posterTitle?: string
}
```

### Game Configuration

```typescript
{
  gameType?: 'story' | 'interactive' | 'explore' | 'mission' | 'roleplay' |
             'simulation' | 'puzzle' | 'arcade' | 'card' | 'word' |
             'timeline' | 'custom',
  customPrompt?: string,    // Required if gameType is 'custom'
  uploadedImages?: string[] // Array of image URLs
}
```

### Film Configuration

```typescript
{
  filmStyle?: 'story' | 'documentary' | 'tutorial' | 'concept_explainer' |
              'narration' | 'case_study' | 'animation' | 'cinematic' |
              'promotional' | 'custom',
  customPrompt?: string,   // Required if filmStyle is 'custom'
  aspectRatio?: '16:9' | '9:16' | '1:1',
  visualStyle?: string
}
```

---

## Rate Limits

- Default: 60 requests per minute
- Default: 1000 requests per day
- Configurable per API key

---

## Callback Notifications

If you provide a `callbackUrl` when creating a task, you'll receive a POST request when the task completes:

```json
{
  "taskId": "...",
  "requestId": "...",
  "taskType": "course",
  "status": "success",
  "resultUrl": "...",
  "resultData": { ... },
  "creditsUsed": 100,
  "completedAt": "2026-03-01T10:03:00.000Z"
}
```
