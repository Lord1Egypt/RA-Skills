---
name: minimax-coding-plan-tool
description: MiniMax Token Plan工具 - 支持图片生成、图像理解、语音合成和视频生成。直接调用MiniMax官方API，纯JavaScript实现，无需外部MCP服务器。
metadata: {"openclaw":{"emoji":"🧩","requires":{"bins":["node"],"env":["MINIMAX_API_KEY"]},"primaryEnv":"MINIMAX_API_KEY"}}
---

# MiniMax Coding Plan Tool

> ⚠️ 使用你的 OpenClaw OAuth Token（sk-cp- 开头）作为 API Key
> 来自 MiniMax Token Plan 订阅额度

MiniMax Token Plan 工具，支持：
- **图片生成**（image-01模型，200张/日）
- **图像理解**（VLM模型）
- **语音合成**（speech-2.8-hd模型）
- **视频生成**（MiniMax-Hailuo-2.3模型）
- **网页搜索**

纯 JavaScript 实现，直接调用 MiniMax 官方 API，无需外部 MCP 服务器。

---

## ✨ Features

### 1. `minimax_generate_image`
图片生成，使用 MiniMax image-01 模型。每日200张额度。

### 2. `minimax_web_search`
网页搜索，使用 MiniMax 搜索 API。

### 3. `minimax_understand_image`
图像理解，使用 MiniMax VLM 模型分析图片内容。

### 4. `minimax_text_to_speech`
语音合成，使用 MiniMax speech-2.8-hd 模型。支持英语发音，可调节语速。

### 5. `minimax_generate_video`
视频生成，使用 MiniMax-Hailuo-2.3 模型。异步生成，返回 task_id 用于查询进度。

---

## 🧩 Architecture

- 纯 JavaScript 实现
- 直接 HTTPS API 调用
- 无需 MCP 服务器
- 无需外部工具依赖

---

## 🔑 Configuration

API Key 使用你的 OpenClaw OAuth Token：

```bash
openclaw config set skills.entries.minimax-coding-plan-tool.apiKey "sk-cp-gr3tv5pdbN3aPQRhXbREJQrHymKxPZhdn9mdS2Ak9B2uD39bKTTJyRJhBdLRjWrd2KbkEFV8-Zd03HgRkJwCTbLq3NYtmAzZ6U2C2Dfb35o5g89RoDBLBv8"
```

---

# Tool 1 — minimax_generate_image

## Purpose

图片生成。使用 MiniMax **image-01** 模型，通过 Token Plan API 调用。额度：每日200张。

## CLI Invocation

```
MINIMAX_API_KEY="sk-cp-..." node minimax_coding_plan_tool.js generate_image "描述词"
```

## Input Schema

```json
{
  "prompt": "string"
}
```

## Output Format

```json
{
  "success": true,
  "prompt": "a blue robot",
  "image_urls": ["https://..."],
  "job_id": "..."
}
```

---

# Tool 2 — minimax_web_search

## Purpose

实时网页搜索，使用 MiniMax 搜索 API。

## CLI Invocation

```
MINIMAX_API_KEY="sk-cp-..." node minimax_coding_plan_tool.js web_search "查询词"
```

## Input Schema

```json
{
  "query": "string"
}
```

## Output Format

```json
{
  "success": true,
  "query": "...",
  "results": [
    { "title": "...", "link": "...", "snippet": "...", "date": "..." }
  ]
}
```

---

# Tool 3 — minimax_understand_image

## Purpose

图像理解，使用 MiniMax VLM API 分析图片内容。支持 JPEG/PNG/WebP/GIF。

## CLI Invocation

```
MINIMAX_API_KEY="sk-cp-..." node minimax_coding_plan_tool.js understand_image @photo.png "描述这张图"
```

## Input Schema

```json
{
  "image_source": "string",
  "prompt": "string"
}
```

## Output Format

```json
{
  "success": true,
  "prompt": "...",
  "image_source": "...",
  "analysis": "model response"
}
```

---

# Tool 4 — minimax_text_to_speech

## Purpose

语音合成，使用 MiniMax **speech-2.8-hd** 模型，通过 Token Plan API 调用。支持英语等多种语言。

## CLI Invocation

```
MINIMAX_API_KEY="sk-cp-..." node minimax_coding_plan_tool.js text_to_speech "Hello, welcome to MiniMax"
```

## Input Schema

```json
{
  "text": "string",
  "voice_id": "string (optional, default: English_expressive_narrator)",
  "speed": "number (optional, default: 1.0)"
}
```

## Available Voice IDs

| voice_id | Description |
|----------|-------------|
| `English_expressive_narrator` | Expressive English narrator |
| `English_expressive` | Expressive English |
| `English_guy` | American male voice |
| `English_woman` | American female voice |
| `British_man` | British male voice |
| `Chinese_CN_female` | Chinese female voice |

## Output Format

```json
{
  "success": true,
  "text": "Hello, welcome to MiniMax",
  "audio": "base64_encoded_audio_data",
  "audio_format": "mp3",
  "audio_length_ms": 2700,
  "job_id": "..."
}
```

---

# Tool 5 — minimax_generate_video

## Purpose

视频生成，使用 MiniMax **MiniMax-Hailuo-2.3** 模型，通过 Token Plan API 调用。异步生成，返回 task_id。

## CLI Invocation

```
MINIMAX_API_KEY="sk-cp-..." node minimax_coding_plan_tool.js generate_video "a robot walking"
```

## Input Schema

```json
{
  "prompt": "string",
  "duration": "number (optional, 6 or 10 seconds, default: 6)",
  "resolution": "string (optional, '720P' or '1080P', default: '1080P')"
}
```

## Output Format

```json
{
  "success": true,
  "prompt": "a robot walking",
  "task_id": "380141647249520",
  "status": "pending"
}
```

## ⚠️ 注意

视频生成是**异步**的，需要等待完成后通过 task_id 查询结果。查询接口在 api.minimaxi.com 上返回 404，Token Plan 可能不支持视频进度查询，视频 URL 直接在生成完成后通过其他渠道获取。
