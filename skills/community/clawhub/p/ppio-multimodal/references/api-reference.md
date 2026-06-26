# API 参考

## 基础配置

| 配置项 | 值 |
|--------|-----|
| Base URL | `https://api.ppio.com` |
| 鉴权头 | `Authorization: Bearer <API_KEY>` |
| Content-Type | `application/json` |

## 获取 API Key

https://ppio.com/settings/key-management

## 模型列表

https://ppio.com/models

## 定价

https://ppio.com/pricing

| 模型 | 价格 |
|------|------|
| Seedream 5.0 Lite | ￥0.245/张 |
| Vidu Q3 Pro | ￥0.47-1.0/秒 (720P) |
| MiniMax Speech 2.8 Turbo | ￥2/万字符 |
| GLM ASR | ￥0.15/Mt |

---

## 文生图

**POST** `https://api.ppio.com/v3/seedream-5.0-lite`

### 请求

```json
{
  "prompt": "一只可爱的猫咪坐在窗台上"
}
```

### 响应

```json
{
  "images": [
    {
      "url": "https://..."
    }
  ]
}
```

---

## 图片编辑

**POST** `https://api.ppio.com/v3/seedream-5.0-lite`

### 请求

```json
{
  "prompt": "转换为油画风格",
  "reference_images": ["https://example.com/image.jpg"]
}
```

### 响应

```json
{
  "images": [
    {
      "url": "https://..."
    }
  ]
}
```

---

## 文生视频（异步）

**POST** `https://api.ppio.com/v3/async/vidu-q3-pro-t2v`

### 请求

```json
{
  "prompt": "海浪拍打沙滩，夕阳西下",
  "duration": 4
}
```

### 响应

```json
{
  "task_id": "xxx-xxx-xxx"
}
```

---

## 图生视频（异步）

**POST** `https://api.ppio.com/v3/async/vidu-q3-pro-i2v`

### 请求

```json
{
  "prompt": "轻柔的微风吹动，镜头缓缓移动",
  "images": ["https://example.com/image.jpg"]
}
```

### 响应

```json
{
  "task_id": "xxx-xxx-xxx"
}
```

---

## TTS - 文字转语音（异步）

**POST** `https://api.ppio.com/v3/async/minimax-speech-2.8-turbo`

### 请求

```json
{
  "text": "你好，欢迎使用 PPIO",
  "voice_setting": {
    "voice_id": "male-qn-qingse",
    "speed": 1.0
  },
  "audio_setting": {
    "format": "mp3"
  }
}
```

### 可用声音

| 声音 ID | 描述 |
|---------|------|
| `male-qn-qingse` | 男声，青涩 |
| `male-qn-jingying` | 男声，精英 |
| `female-shaonv` | 女声，少女 |
| `female-yujie` | 女声，御姐 |

### 响应

```json
{
  "task_id": "xxx-xxx-xxx"
}
```

---

## STT - 语音转文字

**POST** `https://api.ppio.com/v3/glm-asr`

### 请求

```json
{
  "file": "https://example.com/audio.mp3"
}
```

**说明：** `file` 支持音频 URL 或 Base64 编码。支持格式：.wav、.mp3。最大 25MB，最长 30 秒。

### 响应

```json
{
  "text": "识别出的文字内容"
}
```

---

## 任务结果查询

**GET** `https://api.ppio.com/v3/async/task-result?task_id={task_id}`

### 响应

```json
{
  "task_id": "xxx",
  "status": "TASK_STATUS_SUCCEED",
  "output": {
    "video_url": "https://..."
  }
}
```

### 状态值

| 状态 | 含义 |
|------|------|
| `TASK_STATUS_QUEUED` | 排队中 |
| `TASK_STATUS_PROCESSING` | 处理中 |
| `TASK_STATUS_SUCCEED` | 完成 |
| `TASK_STATUS_FAILED` | 失败 |

---

## 错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 400 | 请求无效 | 检查参数 |
| 401 | 未授权 | 检查 API Key |
| 402 | 余额不足 | https://ppio.com/billing 充值 |
| 429 | 请求过快 | 等待后重试 |
| 500 | 服务器错误 | 稍后重试 |

---

## 支持

- 控制台：https://ppio.com/console
- 文档：https://docs.ppio.com
