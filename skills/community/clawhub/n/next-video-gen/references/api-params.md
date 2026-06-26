# Next Video Gen API 参数参考

本文档为豆包 Next Video Gen 生成服务的完整 API 参数参考，基于火山引擎方舟平台。

## API 端点

### 图片生成
```
POST https://ark.cn-beijing.volces.com/api/v3/images/generations
GET  https://ark.cn-beijing.volces.com/api/v3/images/generations/{task_id}
Authorization: Bearer {DOUBAO_API_KEY}
Content-Type: application/json
```

### 视频生成
```
POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
GET  https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks/{task_id}
Authorization: Bearer {DOUBAO_API_KEY}
Content-Type: application/json
```

## 模型

| 模型 | API 端点 | 说明 |
|------|---------|------|
| `doubao-seedream-5-0-260128` | `/v3/images/generations` | 文生图 |
| `doubao-seedance-1-5-pro-251215` | `/v3/contents/generations/tasks` | 文生视频、图生视频、素材生视频（1.5 Pro） |
| `doubao-seedance-2-0-260128` | `/v3/contents/generations/tasks` | 文生视频、图生视频、素材生视频（2.0） |

---

## 图片 API（文生图）

### 请求体

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "一只橘猫在阳光下打盹",
  "sequential_image_generation": "disabled",
  "response_format": "url",
  "size": "2K",
  "aspect_ratio": "1:1",
  "watermark": true,
  "stream": false
}
```

### 字段说明

| 字段 | 类型 | 默认值 | 可选值 | 说明 |
|------|------|--------|--------|------|
| `model` | string | — | `doubao-seedream-5-0-260128` | **必填**。模型名称 |
| `prompt` | string | — | 任意文字 | **必填**。图片描述 |
| `sequential_image_generation` | string | `disabled` | `disabled` | 固定为 `disabled` |
| `response_format` | string | `url` | `url` | 固定为 `url` |
| `size` | string | `2K` | `2K`, `1K`, `HD` | 图片分辨率。2K ≈ 2048px |
| `aspect_ratio` | string | `1:1` | `1:1`, `16:9`, `9:16` | 宽高比 |
| `watermark` | boolean | `true` | `true`, `false` | 是否显示水印 |
| `stream` | boolean | `false` | `false` | 固定为 `false` |

### 图片成功响应

```json
{
  "id": "img-xxx-abc123",
  "status": "succeeded",
  "data": [{
    "url": "https://cdn.example.com/image.png"
  }]
}
```

---

## 视频 API（文生视频 / 图生视频 / 素材生视频）

### 请求体

```json
{
  "model": "doubao-seedance-2-0-260128",
  "content": [
    {
      "type": "text",
      "text": "一只猫在草地上奔跑，阳光明媚，有鸟叫"
    },
    {
      "type": "image_url",
      "image_url": { "url": "https://example.com/cat.jpg" },
      "role": "reference_image"
    },
    {
      "type": "video_url",
      "video_url": { "url": "https://example.com/input.mp4" },
      "role": "reference_video"
    },
    {
      "type": "audio_url",
      "audio_url": { "url": "https://example.com/bgm.mp3" },
      "role": "reference_audio"
    }
  ],
  "generate_audio": true,
  "ratio": "16:9",
  "duration": 5,
  "watermark": true
}
```

### 字段说明

| 字段 | 类型 | 默认值 | 可选值 | 说明 |
|------|------|--------|--------|------|
| `model` | string | — | `doubao-seedance-2-0-260128` | **必填**。模型名称 |
| `content` | array | — | — | **必填**。内容数组 |
| `content[].type` | string | — | `text`, `image_url`, `video_url`, `audio_url` | 内容类型 |
| `content[].role` | string | — | `reference_image`, `reference_video`, `reference_audio` | 仅 image/video/audio 需要 |
| `generate_audio` | boolean | `true` | `true`, `false` | 是否生成同步音频（语音、音效、背景音乐） |
| `ratio` | string | `16:9` | `16:9`, `9:16`, `1:1` | 视频宽高比 |
| `duration` | integer | `5` | `4`–`12` | 视频时长（秒） |
| `watermark` | boolean | `true` | `true`, `false` | 是否显示水印 |

### content 说明

- **text**: 必填，描述想要生成的内容
- **image_url**: 可选，参考图片，最多支持多张，`role: "reference_image"`
- **video_url**: 可选，视频素材，`role: "reference_video"`
- **audio_url**: 可选，音频素材（作为背景音乐等），`role: "reference_audio"`

### 视频成功响应

```json
{
  "id": "task-xxx-abc123",
  "status": "succeeded",
  "content": {
    "video_url": "https://cdn.example.com/video.mp4"
  },
  "duration": 5,
  "ratio": "16:9",
  "resolution": "720p",
  "generate_audio": true
}
```

---

## 任务状态值

| 状态 | 说明 | 操作 |
|------|------|------|
| `pending` | 任务已排队 | 继续轮询 |
| `running` | 生成中 | 继续轮询 |
| `succeeded` | 内容已就绪 | 从响应中提取 URL |
| `failed` | 生成失败 | 检查 error 字段 |

---

## 错误码

| 状态码 | 说明 | 常见原因 | 解决方案 |
|--------|------|---------|---------|
| `200` | 成功 | — | 处理响应 |
| `400` | 请求错误 | 参数无效、内容被拦截、文件过大 | 检查参数和内容 |
| `401` | 未授权 | API Key 无效或缺失 | 检查 `DOUBAO_API_KEY`，前往 [console.volcengine.com/ark](https://console.volcengine.com/ark) |
| `403` | 权限不足 | API Key 无模型访问权限 | 检查控制台中 API Key 的权限设置 |
| `429` | 请求过频 | 超过速率限制 | 等待后重试 |
| `500` | 服务器错误 | 服务异常 | 稍后重试 |

### 常见错误情况

#### 内容被拦截（400）
- **触发**：真实人脸、违规内容
- **解决**：修改 prompt，避免受限内容

#### 文件过大（400）
- **触发**：图片超过 30MB，视频超过 100MB
- **解决**：压缩文件后重试

#### Key 无效（401）
- **解决**：前往 [console.volcengine.com/ark](https://console.volcengine.com/ark) 确认 Key 状态

---

## 轮询策略

`scripts/seedance-gen.sh` 采用的轮询逻辑：
- 每 **5 秒**轮询一次
- 每 **30 秒**向用户报告一次进度
- **超时时间**：10 分钟（600 秒）

### 典型生成时间
- **文生图**：5–15 秒
- **4–5 秒, 480p 视频**：20–45 秒
- **5–8 秒, 720p 视频**：30–90 秒
- **10–12 秒, 1080p 视频**：60–180 秒

---

## 输出内容

- **有效期**：生成后 24 小时
- **图片格式**：PNG / JPEG / WebP
- **视频格式**：MP4
- **音频**：视频默认包含同步音频（语音、音效、背景音乐）
- **本地保存路径**：`~/Videos/next-video-gen/`（可通过 `NEXT_VIDEO_GEN_OUTPUT_DIR` 配置）

---

## 提示词建议

- 描述具体（颜色、光线、动作）
- 避免真实人脸
- 使用电影化语言获得更好效果
- 可在 prompt 中直接描述声音效果，如"背景音乐欢快"、"有鸟叫"、"人物说话"

---

## 参考

- 文生图模型详情：[console.volcengine.com/ark](https://console.volcengine.com/ark/model_detail?Id=doubao-seedream-5-0-260128)
- 视频生成模型详情：[console.volcengine.com/ark](https://console.volcengine.com/ark/model_detail?Id=doubao-seedance-2-0-260128)
- 生成脚本：`scripts/seedance-gen.sh`
