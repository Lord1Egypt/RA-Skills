# Knowfun.io OpenAPI 参考文档

[English](api-reference.md) | 简体中文

Knowfun.io OpenAPI 的完整 API 文档。

## Base URL

```
https://api.knowfun.io
```

## 认证

所有请求都需要作为 Bearer token 传递的 API key：

```bash
Authorization: Bearer kf_your_api_key_here
```

## 端点

### 1. 创建任务

创建内容生成任务。

**端点：** `POST /api/openapi/v1/tasks`

**请求头：**
```
Authorization: Bearer <API_KEY>
Content-Type: application/json
```

**请求体：**
```json
{
  "requestId": "unique-request-id-123",
  "taskType": "course",
  "material": {
    "text": "要处理的内容",
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

**参数：**

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| requestId | string | ✅ | 唯一请求 ID（1-64 字符）用于幂等性 |
| taskType | string | ✅ | 任务类型：course, poster, game, film |
| material.text | string | * | 文本内容（text 或 url 二选一） |
| material.url | string | * | 文档/网页 URL（text 或 url 二选一） |
| material.type | string | ❌ | 素材类型：text, url, pdf, doc, docx, ppt, pptx, txt |
| config | object | ❌ | 任务特定配置 |
| callbackUrl | string | ❌ | 任务完成的回调 URL |
| language | string | ❌ | 语言设置（默认：en） |

**响应：**
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

### 2. 获取任务状态（通过 taskId）

**端点：** `GET /api/openapi/v1/tasks/:taskId`

**请求头：**
```
Authorization: Bearer <API_KEY>
```

**响应：**
```json
{
  "success": true,
  "data": {
    "taskId": "c3199fb3-350b-4981-858d-09b949bfae88",
    "requestId": "unique-request-id-123",
    "taskType": "course",
    "status": "success",
    "progress": 100,
    "resultUrl": "https://oss.knowfun.io/courses/xxx.html",
    "resultData": {
      "title": "课程标题",
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

### 3. 获取任务状态（通过 requestId）

**端点：** `GET /api/openapi/v1/tasks/by-request/:requestId`

**请求头：**
```
Authorization: Bearer <API_KEY>
```

**响应：** 与上面的获取任务状态相同。

---

### 4. 获取任务详情

获取任务的详细信息，包括完整结果。

**端点：** `GET /api/openapi/v1/tasks/:taskId/detail`

**查询参数：**
- `verbose` (boolean, 可选): 返回完整详情，包括日志和元数据

**请求头：**
```
Authorization: Bearer <API_KEY>
```

**响应（课程）：**
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
      "title": "课程标题",
      "coverUrl": "https://oss.knowfun.io/covers/xxx.png",
      "course": {
        "url": "https://oss.knowfun.io/courses/xxx.html",
        "type": "ppt",
        "slidesCount": 12,
        "totalDuration": 180000
      },
      "pages": [
        {
          "pageNumber": 1,
          "title": "第 1 页",
          "content": "内容文本...",
          "ttsText": "TTS 旁白...",
          "html": "<div>...</div>",
          "audioUrl": "https://oss.knowfun.io/audio/xxx.mp3",
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

**响应（海报）：**
```json
{
  "success": true,
  "data": {
    "taskType": "poster",
    "status": "completed",
    "result": {
      "posterUrl": "https://oss.knowfun.io/posters/xxx.png",
      "title": "海报标题"
    }
  }
}
```

**响应（游戏）：**
```json
{
  "success": true,
  "data": {
    "taskType": "game",
    "status": "completed",
    "result": {
      "codeUrl": "https://oss.knowfun.io/games/xxx.html",
      "coverUrl": "https://oss.knowfun.io/covers/xxx.png",
      "title": "游戏标题"
    }
  }
}
```

**响应（视频）：**
```json
{
  "success": true,
  "data": {
    "taskType": "film",
    "status": "completed",
    "result": {
      "videoUrl": "https://oss.knowfun.io/videos/xxx.mp4",
      "coverUrl": "https://oss.knowfun.io/covers/xxx.png",
      "title": "视频标题"
    }
  }
}
```

---

### 5. 任务列表

获取你的任务列表，支持分页和筛选。

**端点：** `GET /api/openapi/v1/tasks`

**查询参数：**
- `limit` (integer, 默认: 20): 每页任务数
- `offset` (integer, 默认: 0): 分页偏移量
- `taskType` (string, 可选): 按任务类型筛选 (course, poster, game, film)
- `status` (string, 可选): 按状态筛选

**请求头：**
```
Authorization: Bearer <API_KEY>
```

**响应：**
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

### 6. 获取积分余额

**端点：** `GET /api/openapi/v1/credits/balance`

**请求头：**
```
Authorization: Bearer <API_KEY>
```

**响应：**
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

### 7. 获取积分定价

**端点：** `GET /api/openapi/v1/credits/pricing`

**请求头：**
```
Authorization: Bearer <API_KEY>
```

**响应：**
```json
{
  "success": true,
  "data": {
    "course": {
      "credits": 100,
      "description": "生成课程消耗 100 积分"
    },
    "poster": {
      "credits": 100,
      "description": "生成海报消耗 100 积分"
    },
    "game": {
      "credits": 100,
      "description": "生成游戏消耗 100 积分"
    },
    "film": {
      "credits": 100,
      "description": "生成视频消耗 100 积分"
    }
  }
}
```

---

### 8. 获取积分使用情况

获取详细的积分使用历史。

**端点：** `GET /api/openapi/usage`

**查询参数：**
- `page` (integer, 默认: 1): 页码
- `pageSize` (integer, 默认: 10, 最大: 100): 每页项目数
- `taskType` (string, 可选): 按任务类型筛选
- `status` (string, 可选): 按状态筛选
- `startDate` (string, 可选): 开始日期 (YYYY-MM-DD)
- `endDate` (string, 可选): 结束日期 (YYYY-MM-DD)

**请求头：**
```
Authorization: Bearer <API_KEY>
```

**响应：**
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

### 9. 获取配置架构

获取所有任务类型的可用配置选项。

**端点：** `GET /api/openapi/v1/schema`

**响应：**
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

## 任务状态值

| 状态 | 描述 |
|------|------|
| pending | 任务已排队 |
| processing | 任务正在处理中 |
| parsing | 正在解析输入素材 |
| generating | 正在生成内容 |
| completed / success | 任务成功完成 |
| failed | 任务失败 |
| cancelled | 任务已取消 |

---

## 错误码

| 错误码 | HTTP 状态 | 描述 |
|--------|----------|------|
| INVALID_API_KEY | 401 | 无效的 API key |
| API_KEY_EXPIRED | 401 | API key 已过期 |
| API_KEY_REVOKED | 401 | API key 已被撤销 |
| OPENAPI_NOT_ENABLED | 403 | 用户未启用 OpenAPI |
| RATE_LIMIT_EXCEEDED | 429 | 超出速率限制 |
| DAILY_LIMIT_EXCEEDED | 429 | 超出每日限制 |
| TASK_TYPE_NOT_ALLOWED | 403 | 任务类型不允许 |
| INSUFFICIENT_CREDITS | 402 | 积分不足 |
| INVALID_REQUEST_ID | 400 | 无效的 requestId |
| DUPLICATE_REQUEST_ID | 400 | 重复的 requestId |
| INVALID_TASK_TYPE | 400 | 无效的任务类型 |
| INVALID_MATERIAL | 400 | 无效的素材参数 |
| MATERIAL_PARSE_FAILED | 400 | 素材解析失败 |
| TASK_NOT_FOUND | 404 | 任务未找到 |
| TASK_PROCESSING_FAILED | 500 | 任务处理失败 |
| INTERNAL_ERROR | 500 | 内部错误 |

---

## 配置详情

### 课程配置

```typescript
{
  contentStyle?: 'detailed' | 'concise' | 'conversational',
  contentLanguage?: string,  // 如：'zh', 'en'
  explainLanguage?: string,  // 如：'zh', 'en'
  voiceType?: string,        // 从 schema 获取标准音色类型
  ttsStyle?: string,         // 如：'classroom', 从 schema 获取
  generateMethod?: string,   // 如：'llm'
  focusOnDocument?: boolean,
  userRequirement?: string   // 自定义要求
}
```

### 海报配置

```typescript
{
  usage?: 'infographic' | 'businessReports' | 'marketing' | 'illustration',
  style?: 'handDrawn' | 'photorealistic' | 'anime' | 'sciFi' | 'custom',
  customStylePrompt?: string,  // 如果 style 是 'custom' 则必需
  aspectRatio?: '1:1' | '4:3' | '3:4' | '16:9' | '9:16',
  posterTitle?: string
}
```

### 游戏配置

```typescript
{
  gameType?: 'story' | 'interactive' | 'explore' | 'mission' | 'roleplay' |
             'simulation' | 'puzzle' | 'arcade' | 'card' | 'word' |
             'timeline' | 'custom',
  customPrompt?: string,    // 如果 gameType 是 'custom' 则必需
  uploadedImages?: string[] // 图片 URL 数组
}
```

### 视频配置

```typescript
{
  filmStyle?: 'story' | 'documentary' | 'tutorial' | 'concept_explainer' |
              'narration' | 'case_study' | 'animation' | 'cinematic' |
              'promotional' | 'custom',
  customPrompt?: string,   // 如果 filmStyle 是 'custom' 则必需
  aspectRatio?: '16:9' | '9:16' | '1:1',
  visualStyle?: string
}
```

---

## 速率限制

- 默认：60 次/分钟
- 默认：1000 次/天
- 可按 API key 配置

---

## 回调通知

如果你在创建任务时提供了 `callbackUrl`，任务完成后你将收到 POST 请求：

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
