# API 接口文档

## 概述

AI 音乐创作引擎提供 RESTful API 接口，支持端到端的音乐生成流程。所有接口均使用 JSON 格式传输数据。

### 基础信息
- **基础 URL**: `https://api.huo15.com/music/v1`
- **认证方式**: JWT Bearer Token
- **请求格式**: JSON
- **响应格式**: JSON
- **字符编码**: UTF-8

### 认证机制

```bash
# 获取认证令牌
curl -X POST https://api.huo15.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "your_api_key",
    "user_id": "user123"
  }'

# 使用令牌访问 API
curl -X POST https://api.huo15.com/music/v1/generate \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## 核心接口

### 1. 音频文件上传

上传用户录音样本文件。

#### 请求
```http
POST /api/v1/upload
Content-Type: multipart/form-data
Authorization: Bearer {token}

Form Data:
- audio: File (required) - 音频文件 (WAV, MP3, FLAC)
- filename: String (optional) - 自定义文件名
```

#### 请求示例
```bash
curl -X POST https://api.huo15.com/music/v1/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "audio=@voice_sample.wav" \
  -F "filename=my_voice.wav"
```

#### 响应
```json
{
  "success": true,
  "filename": "uuid_generated_filename.wav",
  "path": "/data/uploads/uuid_generated_filename.wav",
  "size": 1572864,
  "duration": 32.5,
  "sample_rate": 48000,
  "format": "WAV",
  "metadata": {
    "channels": 1,
    "bit_depth": 16
  }
}
```

#### 错误码
- `400`: 文件格式不支持或文件损坏
- `401`: 认证失败
- `413`: 文件过大 (超过 200MB)

### 2. 音乐生成主接口

启动 AI 音乐生成任务。

#### 请求
```http
POST /api/v1/generate
Content-Type: application/json
Authorization: Bearer {token}

Request Body:
{
  "voice_sample": "string (required)",
  "lyrics": "string (optional)",
  "theme": "string (optional)",
  "style": "string (optional, default: 'pop')",
  "tempo": "integer (optional, default: 120)",
  "duration": "integer (optional, default: 180)",
  "key": "string (optional, default: 'C')",
  "emotion": "string (optional, default: 'uplifting')",
  "language": "string (optional, default: 'chinese')",
  "style_config": "object (optional)",
  "output_formats": "array (optional)",
  "callback_url": "string (optional)"
}
```

#### 请求参数表

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| voice_sample | string | ✓ | - | 上传的音频样本文件路径 |
| lyrics | string | | - | 歌词文本内容 (与 theme 二选一) |
| theme | string | | - | 主题关键词，用于自动生成歌词 |
| style | string | | "pop" | 音乐风格：pop, rock, folk, electronic, rap, ballad, jazz, classical |
| tempo | integer | | 120 | 速度 (BPM)，范围：60-200 |
| duration | integer | | 180 | 歌曲时长 (秒)，范围：30-600 |
| key | string | | "C" | 调性，可选值见下表 |
| emotion | string | | "uplifting" | 情绪基调，可选值见下表 |
| language | string | | "chinese" | 语言：chinese, english, mixed |
| style_config | object | | {} | 高级风格配置 |
| output_formats | array | | ["wav_hd"] | 输出格式：wav_hd, mp3_hq, midi, karaoke |
| callback_url | string | | - | 完成后回调通知地址 |

##### 调性选项
- C, C#, D, D#, E, F, F#, G, G#, A, A#, B
- Cm, C#m, Dm, D#m, Em, Fm, F#m, Gm, G#m, Am, A#m, Bm

##### 情绪选项
- uplifting (振奋)
- romantic (浪漫) 
- energetic (活力)
- melancholy (忧郁)
- peaceful (平和)
- dramatic (戏剧)

##### 风格配置示例
```json
{
  "style_config": {
    "instruments": ["lead_guitar", "bass", "drums", "keyboard"],
    "effects": {
      "reverb": 0.3,
      "delay": 0.2,
      "distortion": 0.1
    },
    "structure": {
      "intro": 8,
      "verse": 16,
      "chorus": 8,
      "bridge": 8,
      "outro": 8
    }
  }
}
```

#### 响应

##### 成功响应
```json
{
  "success": true,
  "job_id": "uuid-string",
  "status": "pending",
  "message": "Music generation started",
  "estimated_time": 3000,
  "queue_position": 1
}
```

##### 错误响应
```json
{
  "success": false,
  "error": "Missing required parameter: voice_sample",
  "code": "VALIDATION_ERROR"
}
```

### 3. 任务状态查询

查询音乐生成任务的实时状态。

#### 请求
```http
GET /api/v1/job/{job_id}
Authorization: Bearer {token}
```

#### 请求示例
```bash
curl -X GET https://api.huo15.com/music/v1/job/abc123-def456 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

#### 响应
```json
{
  "job_id": "abc123-def456",
  "user_id": "user123",
  "status": "completed",
  "progress": 100,
  "stages": {
    "preprocess": "completed",
    "voice_clone": "completed",
    "lyrics": "completed",
    "instrumental": "completed",
    "singing": "completed",
    "mixing": "completed",
    "quality": "completed"
  },
  "created_at": "2024-07-19T10:30:00Z",
  "started_at": "2024-07-19T10:30:05Z",
  "completed_at": "2024-07-19T11:15:20Z",
  "total_time": 2720,
  "result": {
    "generated_lyrics": "当微风吹过脸庞...",
    "audio_files": [
      {
        "format": "wav_hd",
        "url": "https://storage.huo15.com/outputs/abc123.wav",
        "size": 12450000,
        "duration": 180
      },
      {
        "format": "mp3_hq",
        "url": "https://storage.huo15.com/outputs/abc123.mp3",
        "size": 8700000,
        "duration": 180
      },
      {
        "format": "midi",
        "url": "https://storage.huo15.com/outputs/abc123.mid",
        "size": 125000
      }
    ],
    "quality_report": {
      "overall_score": 4.3,
      "vocal_quality": 4.2,
      "rhythm_accuracy": 4.5,
      "style_adherence": 4.1
    }
  }
}
```

#### 任务状态码
- `pending`: 排队中
- `running`: 运行中
- `completed`: 已完成
- `failed`: 失败
- `cancelled`: 已取消

### 4. 任务取消接口

取消正在运行或排队中的任务。

#### 请求
```http
DELETE /api/v1/job/{job_id}
Authorization: Bearer {token}
```

#### 响应
```json
{
  "success": true,
  "message": "Job cancelled successfully",
  "job_id": "abc123-def456"
}
```

### 5. 用户任务列表

查询用户的所有音乐生成任务。

#### 请求
```http
GET /api/v1/jobs?page=1&limit=10&status=all
Authorization: Bearer {token}
```

#### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | integer | 1 | 页码，从1开始 |
| limit | integer | 10 | 每页数量，最大50 |
| status | string | "all" | 状态筛选：pending, running, completed, failed, all |

#### 响应
```json
{
  "jobs": [
    {
      "job_id": "job1",
      "status": "completed",
      "progress": 100,
      "created_at": "2024-07-19T10:30:00Z",
      "completed_at": "2024-07-19T11:15:20Z",
      "style": "pop",
      "duration": 180,
      "has_audio": true
    },
    {
      "job_id": "job2", 
      "status": "running",
      "progress": 65,
      "created_at": "2024-07-19T11:20:00Z",
      "style": "rock",
      "duration": 210,
      "has_audio": false
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10,
  "has_more": true
}
```

## 辅助接口

### 6. 系统状态查询

获取系统整体状态和资源使用情况。

#### 请求
```http
GET /api/v1/status
```

#### 响应
```json
{
  "system": {
    "version": "v1.0.0",
    "uptime": "P5DT12H30M",
    "status": "healthy"
  },
  "resources": {
    "gpu_usage": "75%",
    "memory_usage": "68%", 
    "disk_usage": "45%",
    "active_jobs": 3
  },
  "services": {
    "voice_clone": "healthy",
    "music_gen": "healthy",
    "lyrics_ai": "healthy",
    "audio_process": "healthy",
    "redis": "healthy"
  }
}
```

### 7. 音乐风格查询

获取支持的音乐风格列表和详细配置。

#### 请求
```http
GET /api/v1/styles
```

#### 响应
```json
{
  "styles": [
    {
      "id": "pop",
      "name": "流行音乐",
      "description": "现代流行音乐，适合大众口味",
      "characteristics": ["upbeat", "catchy", "electronic"],
      "typical_instruments": ["synth", "drums", "bass"],
      "tempo_range": [90, 140],
      "examples": ["Taylor Swift", "Ed Sheeran"]
    },
    {
      "id": "rock",
      "name": "摇滚",
      "description": "充满力量和激情的音乐",
      "characteristics": ["aggressive", "distorted", "powerful"],
      "typical_instruments": ["electric_guitar", "drums", "bass"],
      "tempo_range": [100, 160]
    }
  ],
  "total": 8
}
```

### 8. 批量生成接口

支持批量提交多个音乐生成任务。

#### 请求
```http
POST /api/v1/batch-generate
Content-Type: application/json
Authorization: Bearer {token}

Request Body:
{
  "configs": [
    {
      "voice_sample": "path/to/voice1.wav",
      "theme": "夏日恋歌",
      "style": "pop"
    },
    {
      "voice_sample": "path/to/voice2.wav", 
      "lyrics": "自己的歌词内容",
      "style": "rock"
    }
  ],
  "parallel_limit": 2
}
```

#### 响应
```json
{
  "success": true,
  "batch_id": "batch_uuid",
  "job_ids": ["job1", "job2"],
  "message": "Batch generation started"
}
```

## 错误处理

### 错误响应格式

```json
{
  "success": false,
  "error": "详细的错误信息", 
  "code": "ERROR_CODE",
  "details": {
    "field": "错误字段",
    "value": "错误值"
  }
}
```

### 错误码表

| 错误码 | HTTP 状态码 | 说明 |
|--------|-------------|------|
| `VALIDATION_ERROR` | 400 | 参数验证失败 |
| `AUTH_ERROR` | 401 | 认证失败 |
| `FORBIDDEN` | 403 | 权限不足 |
| `NOT_FOUND` | 404 | 资源未找到 |
| `RATE_LIMITED` | 429 | 请求频率超限 |
| `INSUFFICIENT_QUOTA` | 402 | 配额不足 |
| `RESOURCE_BUSY` | 423 | 资源正忙 |
| `GENERATION_FAILED` | 500 | 生成失败 |
| `SERVICE_UNAVAILABLE` | 503 | 服务暂时不可用 |

## Webhooks

### 任务完成通知

当任务完成时，系统会向配置的 callback_url 发送 POST 请求。

#### Webhook 请求格式
```json
{
  "event": "job.completed",
  "timestamp": "2024-07-19T11:15:20Z",
  "data": {
    "job_id": "abc123-def456",
    "status": "completed", 
    "result_url": "https://api.huo15.com/music/v1/job/abc123-def456"
  }
}
```

#### 事件类型
- `job.started`: 任务开始
- `job.progress`: 进度更新 
- `job.completed`: 任务完成
- `job.failed`: 任务失败

## 使用示例

### Python 客户端示例

```python
import requests
import json

class AIMusicClient:
    def __init__(self, base_url, token):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
    
    def upload_audio(self, file_path):
        with open(file_path, 'rb') as f:
            files = {'audio': f}
            response = self.session.post(f"{self.base_url}/upload", files=files)
            return response.json()
    
    def generate_music(self, config):
        response = self.session.post(f"{self.base_url}/generate", json=config)
        return response.json()
    
    def get_job_status(self, job_id):
        response = self.session.get(f"{self.base_url}/job/{job_id}")
        return response.json()

# 使用示例
client = AIMusicClient('https://api.huo15.com/music/v1', 'your_token')

# 上传录音
upload_result = client.upload_audio('my_voice.wav')
print(f"上传成功: {upload_result['filename']}")

# 生成音乐
config = {
    'voice_sample': upload_result['path'],
    'theme': '夏日恋歌',
    'style': 'pop',
    'tempo': 120
}

generation_result = client.generate_music(config)
job_id = generation_result['job_id']
print(f"任务已创建: {job_id}")

# 查询状态
status = client.get_job_status(job_id)
print(f"任务状态: {status['status']}, 进度: {status['progress']}%")
```

## 附录

### A. 音频格式支持

| 格式 | 最大码率 | 采样率 | 位深 | 推荐度 |
|------|----------|--------|------|--------|
| WAV | 无压缩 | 48kHz | 16-24bit | ⭐⭐⭐⭐⭐ |
| FLAC | 无损压缩 | 48kHz | 16-24bit | ⭐⭐⭐⭐☆ |
| MP3 | 320kbps | 44.1kHz | 16bit | ⭐⭐⭐☆☆ |
| M4A | 无损/有损 | 48kHz | 16-24bit | ⭐⭐⭐⭐☆ |

### B. 频率限制
- 同一用户并发任务数: ≤ 5
- API 调用频率: ≤ 100次/分钟
- 每日生成配额: 标准用户 10首，Pro用户 50首

### C. 联系支持
如需技术支持，请联系：
- 邮箱: support@huo15.com
- 工单系统: https://help.huo15.com
- 紧急热线: 400-888-6888