# MiniMax 语音 API 参考

## 基础配置

- **国内用户**: `https://api.minimaxi.com/v1`
- **国际用户**: `https://api.minimax.io/v1`
- **认证方式**: `Authorization: Bearer $MINIMAX_API_KEY`

## API 端点

### 1. 同步语音合成 (T2A v2)

```
POST /v1/t2a_v2
```

**请求体**:
```json
{
  "model": "speech-2.8-hd",
  "text": "要转换的文本",
  "stream": false,
  "voice_setting": {
    "voice_id": "音色ID"
  },
  "audio_setting": {
    "sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3"
  }
}
```

**响应**:
```json
{
  "audio_file": "base64编码的音频数据",
  "extra_info": {}
}
```

### 2. 异步语音合成 (T2A Async v2)

```
POST /v1/t2a_async_v2
```

**请求体**:
```json
{
  "model": "speech-2.8-hd",
  "text": "要转换的文本",
  "voice_setting": {
    "voice_id": "音色ID"
  },
  "audio_setting": {
    "sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3"
  }
}
```

**响应**:
```json
{
  "task_ids": ["任务ID"]
}
```

### 3. 查询异步任务状态

```
GET /v1/query/t2a_async_query_v2?task_id=xxx
```

**响应**:
```json
{
  "task_id": "任务ID",
  "status": "Success",
  "audio_url": "音频下载URL"
}
```

### 4. 音色快速复刻 (Voice Clone)

```
POST /v1/voice_clone
```

**请求体**:
```json
{
  "model": "speech-01",
  "audios": ["base64编码的音频文件"],
  "title": "音色名称"
}
```

**响应**:
```json
{
  "voice_id": "音色ID"
}
```

### 5. 音色设计 (Voice Design)

```
POST /v1/voice_design
```

**请求体**:
```json
{
  "model": "speech-01",
  "text": "音色描述文本",
  "voice_setting": {
    "style": "音色风格"
  }
}
```

**响应**:
```json
{
  "voice_id": "音色ID"
}
```

### 6. 查询音色

```
POST /v1/get_voice
```

**请求体**:
```json
{
  "voice_id": "音色ID"
}
```

**响应**:
```json
{
  "voice": {
    "voice_id": "音色ID",
    "name": "音色名称",
    "status": "Active"
  }
}
```

### 7. 删除音色

```
POST /v1/delete_voice
```

**请求体**:
```json
{
  "voice_id": "音色ID"
}
```

**响应**:
```json
{
  "success": true
}
```

## 可用音色列表

常用内置音色:
- `female-tianmei` - 女声甜美
- `male-yunyang` - 男声播音
- `female-badu` - 女声巴度
- `male-shawn` - 男声 Shawn
- `female-shanshan` - 女声杉杉

## 音频格式支持

- 格式: mp3, wav, pcm
- 采样率: 16000, 32000, 48000
- 比特率: 64000, 128000, 192000
