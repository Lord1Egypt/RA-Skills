---
name: pixshop-creative-api
description: Pixshop 开发者 REST API — 图片生成/编辑、视频制作、提示词库、应用市场、社区 / Pixshop Developer REST API — image generation/editing, video, prompts, apps, community endpoints. Use when user wants to integrate Pixshop AI capabilities into their app via HTTP API, or call endpoints with curl/fetch.
allowed-tools: Bash, Read
---

# Pixshop Creative API — 开发者 REST 接口 / Developer REST API

> **[Pixshop (pixshop.app)](https://pixshop.app)** — AI 图片编辑 & 视频创意平台

通过 REST API 将 Pixshop 的 AI 创意能力集成到任何应用。覆盖图片生成（15+ 模型）、16 种图片编辑工具、视频生成、48+ AI 应用、提示词库、社区功能。所有接口统一返回 `{ success, data?, error? }` 格式。

## Setup / 配置

### 获取 Auth Token

```bash
# 方式 1：通过 CLI 登录获取 token
npm install -g pixshop
pixshop login
cat ~/.pixshop-config.json | jq '.accessToken'

# 方式 2：通过 Supabase Auth API
curl -X POST 'https://<supabase-url>/auth/v1/token?grant_type=password' \
  -H 'apikey: <anon-key>' \
  -d '{"email":"...","password":"..."}'
```

### 请求通用格式

```bash
curl -X POST https://pixshop.app/api/<endpoint> \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

## API 列表 (6 Groups, 30+ Endpoints)

### 1. AI 图片生成

#### `POST /api/ai/generate` — 文本生成图片

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `prompt` | string | ✅ | 图片描述 |
| `model` | string | | 模型名（默认 nano-banana） |
| `aspectRatio` | string | | 1:1, 16:9, 9:16, 4:3, 3:4 |
| `quality` | string | | standard, hd |
| `referenceImage` | string | | 参考图片 base64 或 URL |
| `appId` | string | | Nano Banana App ID |

**示例**:
```bash
curl -X POST https://pixshop.app/api/ai/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"a cute cat in space","aspectRatio":"1:1"}'
```

**返回**: `{ "success": true, "data": { "imageUrl": "...", "metadata": {...} } }`

#### `POST /api/ai/generate-video` — 视频生成

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `imageUrl` | string | ✅ | 源图片 URL |
| `prompt` | string | | 运动描述 |
| `model` | string | | 视频模型 |
| `duration` | string | | 时长 5/10/15 秒 |

#### `POST /api/ai/adapt-parameters` — 参数适配 (免费)

根据描述自动推荐最佳生成参数。

### 2. AI 图片编辑工具 (16 Tools)

所有工具统一格式：`POST /api/tools/<tool-name>`，需要 Auth Token。

#### `POST /api/tools/face-swap` — 人脸替换

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `targetImage` | string | ✅ | 目标图片（base64 或 URL） |
| `sourceImage` | string | ✅ | 人脸来源图片 |
| `mode` | string | | swap (默认) 或 analyze |

#### `POST /api/tools/upscale` — 超分辨率

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 图片 |
| `scale` | number | | 2 或 4 |
| `modelType` | string | | general, portrait, anime, art |

#### `POST /api/tools/try-on` — 虚拟试穿

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `personImage` | string | ✅ | 人物图片 |
| `garmentImage` | string | ✅ | 服装图片 |

#### `POST /api/tools/makeup-studio/analyze` — 妆容分析

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 人脸图片 |

#### `POST /api/tools/makeup-studio/apply` — 妆容应用

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 人脸图片 |
| `style` | string | ✅ | 妆容风格 |

#### `POST /api/tools/aice-ps` — AI 修图

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 图片 |
| `action` | string | ✅ | retouch, filter, adjust, erase, beautify |
| `prompt` | string | | 编辑指令 |

#### `POST /api/tools/inpaint` — 智能填充

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 图片 |
| `mask` | string | ✅ | 遮罩区域 |
| `prompt` | string | | 填充内容 |

#### `POST /api/tools/fashion-photoshoot` — 时尚大片

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 模特图片 |
| `style` | string | | 拍摄风格 |

#### `POST /api/tools/id-photo` — 证件照

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 人像图片 |
| `background` | string | | 背景颜色 |
| `size` | string | | 尺寸预设 |

#### `POST /api/tools/transform` — 图片变换

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 图片 |
| `prompt` | string | ✅ | 变换指令 |

#### `POST /api/tools/sticker-set` — 贴纸生成

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `prompt` | string | ✅ | 贴纸描述 |
| `style` | string | | 贴纸风格 |

#### `POST /api/tools/pose-generate` — 姿态生成

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `prompt` | string | ✅ | 姿态描述 |

#### `POST /api/tools/angles` — 多角度生成

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 源图片 |

#### `POST /api/tools/motion-control/generate` — 运动控制

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 源图片 |
| `prompt` | string | | 运动描述 |

### 3. Nano Banana Apps

#### `GET /api/nano-banana/apps` — 应用列表

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `category` | query | | 分类筛选 |
| `search` | query | | 搜索 |
| `featured` | query | | 精选应用 |

```bash
curl https://pixshop.app/api/nano-banana/apps?category=generation
```

#### `GET /api/nano-banana/apps/[id]` — 应用详情
#### `GET /api/nano-banana/apps/categories` — 分类列表
#### `GET /api/nano-banana/apps/featured` — 精选应用
#### `GET /api/nano-banana/apps/popular` — 热门应用

### 4. 提示词库

#### `GET /api/prompt-library` — 提示词列表

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `search` | query | | 搜索关键词 |
| `category_id` | query | | 分类 ID |
| `tags` | query | | 标签筛选 |
| `page` | query | | 页码 |
| `per_page` | query | | 每页数量 |

```bash
curl "https://pixshop.app/api/prompt-library?search=cyberpunk&per_page=10"
```

#### `GET /api/prompt-library/[id]` — 提示词详情
#### `POST /api/prompt-library/submit` — 提交提示词（需登录）
#### `GET /api/prompt-library/related?id=xxx` — 相关推荐

### 5. 表情包生成

#### `POST /api/meme` — 表情包生成

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `image` | string | ✅ | 源图片 |
| `caption` | string | | 文字 |
| `style` | string | | 风格 |

### 6. Agent Skills

#### `GET /api/agent/skills` — 技能列表

返回所有可用 AI 技能及其参数定义。

#### `POST /api/agent/skills/[id]/execute` — 执行技能

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `...` | object | ✅ | 技能对应的输入参数 |

```bash
curl -X POST https://pixshop.app/api/agent/skills/image-generate/execute \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"prompt":"a sunset","aspectRatio":"16:9"}'
```

#### `GET /api/agent/discover` — 工具发现

浏览完整的 AI 工具目录。

## 统一响应格式

```json
// 成功
{ "success": true, "data": { "imageUrl": "...", ... } }

// 失败
{ "success": false, "error": { "code": "AUTH_REQUIRED", "message": "..." } }
```

**错误码**:
| 状态码 | 错误码 | 说明 |
|--------|--------|------|
| 401 | AUTH_REQUIRED | 未登录 |
| 402 | INSUFFICIENT_CREDITS | 积分不足 |
| 429 | RATE_LIMIT_EXCEEDED | 速率限制 |
| 500 | INTERNAL_ERROR | 服务错误 |

## 典型工作流

### 开发者集成
获取 Token → `GET /api/agent/discover` 查看工具目录 → `POST /api/ai/generate` 生成图片 → `POST /api/tools/upscale` 超分放大

### 批量处理
`GET /api/prompt-library` → 获取提示词列表 → 循环调用 `POST /api/ai/generate` → 批量生成

### 电商场景
`POST /api/tools/face-swap` 换脸 → `POST /api/tools/fashion-photoshoot` 生成大片 → `POST /api/tools/upscale` 放大

## 注意事项

- **认证**：除 `GET /api/nano-banana/apps` 和 `GET /api/prompt-library` 外，所有写操作需 Bearer Token
- **积分**：AI 生成/编辑操作消耗积分，GET 查询免费
- **速率限制**：每个用户每分钟有请求上限，超出返回 429
- **图片输入**：支持 base64 data URL 或 HTTP URL
- **异步操作**：视频生成等长时间操作返回任务 ID，需轮询结果
- **CORS**：API 支持跨域请求

## 在线体验

- [Pixshop 首页](https://pixshop.app) — AI 创意平台全景
- [Nano Banana Apps](https://pixshop.app/apps) — 48+ AI 应用市场
- [提示词库](https://pixshop.app/prompt-library) — 海量高质量提示词
- [Design Agent](https://pixshop.app/agent) — AI 设计工作台
- [MCP 接口](https://pixshop.app/api/mcp) — MCP 协议端点
- [定价方案](https://pixshop.app/pricing) — 免费 / 高级 / 企业

---
Powered by [Pixshop](https://pixshop.app) — AI 图片编辑 & 视频创意平台
