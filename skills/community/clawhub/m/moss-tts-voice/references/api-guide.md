# MOSS-TTS API 技术指南

## API 端点

| 用途 | 方法 | 端点 |
|------|------|------|
| 文本转语音 | POST | `https://studio.mosi.cn/v1/audio/tts` |
| 上传文件 | POST | `https://studio.mosi.cn/api/v1/files/upload` |
| 克隆音色 | POST | `https://studio.mosi.cn/api/v1/voice/clone` |
| 查询音色 | GET | `https://studio.mosi.cn/api/v1/voices` |

## 认证

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

---

## 1. 文本转语音 (TTS)

### 请求

```
POST /v1/audio/tts
```

### 必填参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 固定值 `"moss-tts"` |
| `text` | string | 待合成文本 |

### 音色参数（二选一）

| 参数 | 类型 | 说明 |
|------|------|------|
| `voice_id` | string | 预注册音色ID（推荐） |
| `reference_audio` | string | Base64 编码的参考音频 |

### 可选参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `sampling_params.temperature` | float | 1.7 | 采样温度 |
| `sampling_params.top_p` | float | 0.8 | Top-p 采样 |
| `sampling_params.top_k` | int | 25 | Top-k 采样 |

### 示例

**使用预注册音色：**
```bash
curl -X POST https://studio.mosi.cn/v1/audio/tts \
  -H "Authorization: Bearer $MOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "moss-tts",
    "text": "你好，我是MOSS",
    "voice_id": "YOUR_VOICE_ID"
  }'
```

**使用实时克隆：**
```python
import requests, base64

with open("voice.ogg", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

resp = requests.post(
    "https://studio.mosi.cn/v1/audio/tts",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "moss-tts",
        "text": "要合成的文本",
        "reference_audio": audio_base64
    }
)

audio_wav = base64.b64decode(resp.json()["audio_data"])
```

### 响应

**成功：**
```json
{
  "audio_data": "UklGRiQAAABXQVZFZm10..."
}
```

**错误：**
```json
{
  "code": 4004,
  "error": "Voice Not Found: voice not found"
}
```

---

## 2. 上传文件

### 请求

```
POST /api/v1/files/upload
Content-Type: multipart/form-data
```

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | file | ✅ | 音频文件 |

### 示例

```bash
curl -X POST https://studio.mosi.cn/api/v1/files/upload \
  -H "Authorization: Bearer $MOSS_API_KEY" \
  -F "file=@voice.ogg"
```

### 响应

```json
{
  "file_id": "YOUR_FILE_ID",
  "file_name": "voice.ogg",
  "file_size": 65391,
  "content_type": "audio/ogg",
  "status": "uploaded"
}
```

---

## 3. 克隆音色

### 请求

```
POST /api/v1/voice/clone
Content-Type: application/json
```

### 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file_id` | string | ✅ | 上传文件返回的 ID |
| `name` | string | ❌ | 音色名称 |

### 示例

```bash
curl -X POST https://studio.mosi.cn/api/v1/voice/clone \
  -H "Authorization: Bearer $MOSS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_id": "YOUR_FILE_ID", "name": "我的声音"}'
```

### 响应

```json
{
  "job_id": "2030984715560816640_xxx",
  "status": "PENDING",
  "voice_id": "YOUR_VOICE_ID",
  "transcription_source": "AUTO_ASR"
}
```

### 状态流转

```
PENDING → PROCESSING → ACTIVE
                   ↘ FAILED
```

---

## 4. 查询音色列表

### 请求

```
GET /api/v1/voices
```

### 响应

```json
{
  "count": 1,
  "voices": [
    {
      "voice_id": "YOUR_VOICE_ID",
      "voice_name": "我的声音",
      "status": "ACTIVE",
      "created_at": "2026-03-10T17:24:03+08:00"
    }
  ]
}
```

---

## 错误码

| 代码 | 说明 |
|------|------|
| 4000 | 请求参数错误 |
| 4001 | 缺少必要参数 |
| 4004 | 音色未找到 |
| 4290 | 请求频率超限 |
| 5000 | 服务器内部错误 |

---

## 音频要求

### 参考音频（克隆用）

| 项目 | 要求 |
|------|------|
| 格式 | ogg, mp3, wav, m4a |
| 时长 | 10-30 秒（推荐 20 秒以上） |
| 内容 | 清晰人声，无背景噪音 |
| 大小 | < 10MB |

### 输出音频

- 格式：WAV（原始）
- 采样率：16000 Hz
- 声道：单声道

---

## 速率限制

- 具体 QPS 限制参考 MOSS Studio 控制台
- 遇到 429 错误时等待后重试
- 建议使用预注册音色（减少音频传输）

---

## 调试技巧

### 测试 API 连通性

```bash
MOSS_API_KEY="sk-xxx" python3 -c "
import requests, json
headers = {'Authorization': f'Bearer \$MOSS_API_KEY', 'Content-Type': 'application/json'}
resp = requests.post('https://studio.mosi.cn/v1/audio/tts',
                    headers=headers,
                    json={'model': 'moss-tts', 'text': 'test'},
                    timeout=10)
print(f'Status: {resp.status_code}')
print(json.dumps(resp.json(), ensure_ascii=False)[:200])
"
```

### 检查音频格式

```bash
ffprobe -v error -show_entries stream=codec_name,codec_type -of default=noprint_wrappers=1 voice.ogg
```

---

## 联系支持

- MOSS Studio: https://studio.mosi.cn
- OpenClaw 社区: https://discord.com/invite/clawd
