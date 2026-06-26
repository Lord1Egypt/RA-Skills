# MOSI API Reference

## Base URL
```
https://studio.mosi.cn
```

## Authentication
All requests require Bearer token authentication:
```
Authorization: Bearer YOUR_API_KEY
```

---

## TTS API

### POST /api/v1/audio/speech

将文本转换为语音。

**Request Headers:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Authorization | String | 是 | Bearer YOUR_API_KEY |
| Content-Type | String | 是 | application/json |

**Request Body:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model | String | 是 | 固定值 `moss-tts` |
| text | String | 是 | 待合成的文本 |
| voice_id | String | 是 | 音色 ID（公共音色或自定义音色） |
| expected_duration_sec | Float | 否 | 期望时长（秒），建议为正常朗读时间的 0.5-1.5 倍 |
| sampling_params | Object | 否 | 采样配置 |
| meta_info | Boolean | 否 | 是否返回性能指标，默认 false |

**sampling_params:**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| max_new_tokens | Int | 512 | 最大 Token 数 |
| temperature | Float | 1.7 | 采样温度（中文最佳 1.7，英文最佳 1.5） |
| top_p | Float | 0.8 | 核采样 |
| top_k | Int | 25 | Top-K 采样 |

**Response:**
```json
{
  "audio_data": "UklGRiQAAABXQVZFZm10...",  // Base64 编码的音频
  "duration_s": 0.72,
  "usage": {
    "prompt_tokens": 0,
    "completion_tokens": 0,
    "total_tokens": 6,
    "credit_cost": 6
  }
}
```

---

## Voice Clone API

### POST /api/v1/files/upload

上传音频文件。

**Request Headers:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Authorization | String | 是 | Bearer YOUR_API_KEY |
| Content-Type | String | 是 | multipart/form-data |

**Request Body:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | File | 是 | 音频文件（WAV/MP3/M4A/FLAC，最大 100MB） |

**Response:**
```json
{
  "file_id": "1234567890",
  "filename": "speaker_audio.wav",
  "size": 1048576,
  "content_type": "audio/wav"
}
```

### POST /api/v1/voice/clone

创建自定义音色。

**Request Body:**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file_id | String | 否* | 上传的文件 ID（与 url 二选一） |
| url | String | 否* | 音频 URL（与 file_id 二选一） |
| text | String | 否 | 可选的转写文本，提供可提升质量 |

**Response:**
```json
{
  "voice_id": "08219ad1",
  "voice_name": "Voice 08219ad1",
  "status": "SUCCESS",
  "transcription_text": "你好，我是张三。"
}
```

### GET /api/v1/voices

获取音色列表。

**Query Parameters:**
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| limit | Int | 50 | 每页数量（1-100） |
| offset | Int | 0 | 偏移量 |
| status | String | - | 过滤状态：ACTIVE/FAILED/INACTIVE/DELETED |

### GET /api/v1/voices/{voice_id}

获取单个音色详情。

---

## 公共音色

可直接使用的预置音色：

| Voice ID | 名称 | 描述 | 标签 |
|----------|------|------|------|
| 2001257729754140672 | 阿树 | 冬天清晨的灰白天空，风很冷，但阳光迟早会出来 | 松弛耐听 |
| 2001286865130360832 | 周周 | 薄雾里的风、旧磁带、夜里低声自言自语 | 独白讲述 |
| 2020008594694475776 | 北京男声 | 普通话标准，带轻微北京口音，发音清晰自然 | 清晰自然 |
| 2020009311371005952 | 台湾女声 | 台湾口音柔和细腻，语气温柔平稳 | 温柔治愈 |
| 2001898421836845056 | 子琪 | 雨后未干的水泥地，空气里有点凉 | 轻快元气 |
| 2001910895478837248 | 小满 | 音色清透偏高，带自然甜感 | 轻快明亮 |
| 2001931510222950400 | 程述 | 中低音偏中，带轻微电台感 | 播客理性 |
| 2002941772480647168 | 阿宁 | 声音柔和而稳定，给人被照顾的安心感 | 温柔 |
| 2002991117984862208 | 梁子 | 咬字清晰，但又语气放松 | 新闻专业 |

---

## 错误码

| 错误码 | 描述 | 处理建议 |
|--------|------|----------|
| 4000 | Invalid Request | 检查请求参数格式 |
| 4002 | Invalid Audio | 检查音频格式（支持 16-48kHz WAV） |
| 4010 | Unauthorized | 检查 API Key 是否添加到请求头 |
| 4011 | Invalid API Key | 检查 API Key 是否正确 |
| 4020 | Insufficient Credits | 余额不足，请充值 |
| 4029 | Rate Limit | 降低请求频率（RPM: 5） |
| 5000 | Internal Error | 稍后重试 |
| 5002 | Voice Not Found | 确认 voice_id 状态为 ACTIVE |
| 5004 | Timeout | 减少单次请求文本长度 |

---

## 限制

- **RPM**: 每分钟 5 次请求
- **输出**: 24kHz WAV 格式
- **超时**: 默认 600 秒
- **文本长度**: 最长 1 小时音频
