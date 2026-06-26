# API 参考

## 基础信息

| 项目 | 值 |
|------|-----|
| Base URL | `https://api.jiekou.ai` |
| 鉴权 | `Authorization: Bearer <API_KEY>` |
| 内容类型 | `application/json` |

## 端点列表

### 文生图

#### Gemini 3.1 Flash（默认）

**POST** `/v3/gemini-3.1-flash-image-text-to-image`

```json
{
  "prompt": "图片描述",
  "size": "1K",
  "aspect_ratio": "1:1",
  "output_format": "image/png"
}
```

**响应：**
```json
{
  "image_urls": ["https://..."]
}
```

#### Seedream 5.0 Lite（快速备选）

**POST** `/v3/seedream-5.0-lite`

```json
{
  "prompt": "图片描述"
}
```

**响应：**
```json
{
  "images": ["https://..."]
}
```

### 图片编辑

**POST** `/v3/gemini-3.1-flash-image-edit`

```json
{
  "prompt": "编辑指令",
  "reference_images": ["图片URL或Base64"]
}
```

**其他端点：**
- `/v3/gemini-3-pro-image-edit`
- `/v3/gemini-2.5-flash-image-edit`

### 文生视频

#### Veo 3.1（默认）

**POST** `/v3/async/veo-3.1-generate-text2video`

```json
{
  "prompt": "视频描述",
  "generate_audio": false,
  "duration_seconds": 4,
  "resolution": "720p",
  "aspect_ratio": "16:9"
}
```

**响应：**
```json
{
  "task_id": "xxx-xxx-xxx"
}
```

#### Hailuo 2.3（快速备选）

**POST** `/v3/async/minimax-hailuo-2.3-t2v`

```json
{
  "prompt": "视频描述",
  "duration": 6,
  "resolution": "768P"
}
```

### 图生视频

#### Veo 3.1

**POST** `/v3/async/veo-3.1-generate-img2video`

```json
{
  "prompt": "动作描述",
  "image": "图片URL或Base64"
}
```

#### Hailuo 2.3（快速备选）

**POST** `/v3/async/minimax-hailuo-2.3-i2v`

```json
{
  "prompt": "动作描述",
  "first_frame_image": "图片URL或Base64"
}
```

### 任务结果查询

**GET** `/v3/async/task-result?task_id={task_id}`

**响应：**
```json
{
  "task": {
    "task_id": "xxx",
    "status": "TASK_STATUS_SUCCEED",
    "progress_percent": 100
  },
  "videos": [
    {
      "video_url": "https://...",
      "video_type": "mp4"
    }
  ]
}
```

**状态值：**
- `TASK_STATUS_QUEUED` - 排队中
- `TASK_STATUS_PROCESSING` - 处理中
- `TASK_STATUS_SUCCEED` - 成功
- `TASK_STATUS_FAILED` - 失败

### TTS

**POST** `/v3/minimax-speech-2.6-turbo`

```json
{
  "text": "要转换的文字",
  "voice_setting": {
    "voice_id": "male-qn-qingse",
    "speed": 1.0,
    "vol": 1.0,
    "pitch": 0
  },
  "audio_setting": {
    "format": "mp3",
    "sample_rate": 32000,
    "bitrate": 128000
  }
}
```

**响应：**
```json
{
  "audio": "hex编码音频数据",
  "audio_url": "https://..."
}
```

### STT

**POST** `/v3/glm-asr`

```json
{
  "audio_url": "音频文件URL"
}
```

### 多模态理解

**POST** `/openai/v1/chat/completions`

```json
{
  "model": "gemini-2.5-flash",
  "messages": [{
    "role": "user",
    "content": [
      {"type": "text", "text": "分析指令"},
      {"type": "image_url", "image_url": {"url": "..."}}
    ]
  }]
}
```

**支持的内容类型：**
- `image_url` - 图片
- `audio_url` - 音频
- `video_url` - 视频

## 可用模型

### 图片生成模型
| 模型 | 端点 | 备注 |
|------|------|------|
| Gemini 3.1 Flash Image | `/v3/gemini-3.1-flash-image-text-to-image` | **默认** |
| Seedream 5.0 Lite | `/v3/seedream-5.0-lite` | **快速备选** |
| Gemini 3 Pro Image | `/v3/gemini-3-pro-image-text-to-image` | 高质量 |

### 图片编辑模型
| 模型 | 端点 | 备注 |
|------|------|------|
| Gemini 3.1 Flash | `/v3/gemini-3.1-flash-image-edit` | **默认** |
| Gemini 3 Pro | `/v3/gemini-3-pro-image-edit` | 高质量 |
| Gemini 2.5 Flash | `/v3/gemini-2.5-flash-image-edit` | |

### 视频生成模型
| 模型 | 端点（文生视频） | 端点（图生视频） | 备注 |
|------|------------------|------------------|------|
| Veo 3.1 | `/v3/async/veo-3.1-generate-text2video` | `/v3/async/veo-3.1-generate-img2video` | **默认** |
| Hailuo 2.3 | `/v3/async/minimax-hailuo-2.3-t2v` | `/v3/async/minimax-hailuo-2.3-i2v` | **快速备选** |

### TTS 模型
| 模型 | 端点 | 备注 |
|------|------|------|
| MiniMax Speech 2.6 Turbo | `/v3/minimax-speech-2.6-turbo` | **默认** |

### 视觉理解模型
| 模型 | 特点 |
|------|------|
| gemini-2.5-flash | 通用视觉 |
| gemini-2.5-pro | 高级分析 |
| gpt-4o | GPT-4 视觉 |

## TTS 可用声音

### MiniMax 声音列表

**男声：**
| voice_id | 名称 |
|----------|------|
| male-qn-qingse | 青涩 |
| male-qn-jingying | 精英 |
| male-qn-badao | 霸道 |
| male-qn-daxuesheng | 大学生 |

**女声：**
| voice_id | 名称 |
|----------|------|
| female-shaonv | 少女 |
| female-yujie | 御姐 |
| female-chengshu | 成熟 |
| female-tianmei | 甜美 |

## 错误码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | API Key 无效 |
| 402 | 余额不足 |
| 429 | 请求频率超限 |
| 500 | 服务端错误 |

## 限制

| 项目 | 限制 |
|------|------|
| 图片最大尺寸 | 4K (4096x4096) |
| 视频最长时长 | Veo: 8秒, Hailuo: 10秒 |
| TTS 文本长度 | 10000 字符 |
| 音频 URL 有效期 | 24 小时 |
| 视频 URL 有效期 | 48 小时 |
