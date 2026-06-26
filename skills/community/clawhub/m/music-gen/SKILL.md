---
name: senseaudio-music
description: SenseAudio Music Generation API for creating AI-generated lyrics and songs. Supports lyrics generation, song generation with style/vocal control, and async task polling.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn/docs/song/lyrics_create
---

# SenseAudio Music Generation

SenseAudio provides AI-powered music generation APIs for creating lyrics and full songs. The workflow is:
1. Generate lyrics (sync or async)
2. Generate a song using the lyrics (async, returns `task_id`)
3. Poll for results

**Base URL:** `https://api.senseaudio.cn`
**Auth:** `Authorization: Bearer $SENSEAUDIO_API_KEY`

---

## 1. Generate Lyrics

**POST** `/v1/song/lyrics/create`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| prompt | string | yes | Description of the lyrics to generate |
| provider | string | yes | Model provider, currently only `sensesong` |

**Response (sync):**
```json
{
  "data": [
    {
      "text": "[intro-medium] ; [verse] ... ; [chorus] ... ; [outro-medium]",
      "title": ""
    }
  ]
}
```

**Response (async):** Returns `task_id` — poll with lyrics pending endpoint.

```bash
curl -X POST https://api.senseaudio.cn/v1/song/lyrics/create \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "一段慷慨激昂的歌词", "provider": "sensesong"}'
```

---

## 2. Poll Lyrics (Async)

**GET** `/v1/song/lyrics/pending/:task_id`

**Response:**
```json
{
  "task_id": "bcee6b21-...",
  "status": "SUCCESS",
  "response": {
    "task_id": "bcee6b21-...",
    "data": [{"text": "...", "title": ""}]
  }
}
```

Status values: `PENDING` | `SUCCESS` | `FAILED`

```bash
curl https://api.senseaudio.cn/v1/song/lyrics/pending/{task_id} \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY"
```

---

## 3. Generate Song

**POST** `/v1/song/music/create`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| model | string | yes | Currently only `sensesong` |
| lyrics | string | no | Song lyrics (use format from lyrics API) |
| instrumental | bool | no | `true` for instrumental (no vocals) |
| style | string | no | Music style (e.g. "pop", "rock", "jazz") |
| style_weight | string | no | Style weight 0–1 |
| title | string | no | Song title |
| vocal_gender | string | no | `f` = female, `m` = male |
| negative_tags | string | no | Style elements to exclude |

**Response:**
```json
{"task_id": "50f979f5-2b9e-4254-8653-c277644a31fa"}
```

```bash
curl -X POST https://api.senseaudio.cn/v1/song/music/create \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sensesong",
    "lyrics": "[verse] Your lyrics here...",
    "style": "pop",
    "vocal_gender": "f",
    "title": "My Song"
  }'
```

---

## 4. Poll Song (Async)

**GET** `/v1/song/music/pending/:task_id`

**Response:**
```json
{
  "task_id": "50f979f5-...",
  "status": "SUCCESS",
  "response": {
    "task_id": "50f979f5-...",
    "data": [
      {
        "audio_url": "https://...",
        "lyrics": "...",
        "duration": 110
      }
    ]
  }
}
```

Status values: `PENDING` | `SUCCESS` | `FAILED`

```bash
curl https://api.senseaudio.cn/v1/song/music/pending/{task_id} \
  -H "Authorization: Bearer $SENSEAUDIO_API_KEY"
```

---

## Python Example (Full Flow)

```python
import requests
import time

API_KEY = "YOUR_API_KEY"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
BASE = "https://api.senseaudio.cn"

# Step 1: Generate lyrics
resp = requests.post(f"{BASE}/v1/song/lyrics/create",
    headers=HEADERS,
    json={"prompt": "一首关于夏天的流行歌曲", "provider": "sensesong"})
lyrics_data = resp.json()
lyrics_text = lyrics_data["data"][0]["text"]

# Step 2: Generate song
resp = requests.post(f"{BASE}/v1/song/music/create",
    headers=HEADERS,
    json={"model": "sensesong", "lyrics": lyrics_text, "style": "pop", "vocal_gender": "f"})
task_id = resp.json()["task_id"]

# Step 3: Poll for result
while True:
    resp = requests.get(f"{BASE}/v1/song/music/pending/{task_id}", headers=HEADERS)
    result = resp.json()
    if result["status"] == "SUCCESS":
        print("Audio URL:", result["response"]["data"][0]["audio_url"])
        break
    elif result["status"] == "FAILED":
        print("Failed")
        break
    time.sleep(5)
```

---

---

# SenseAudio 音乐生成

SenseAudio 提供 AI 驱动的音乐生成 API，支持歌词生成和完整歌曲生成。标准工作流程：
1. 生成歌词（同步或异步）
2. 使用歌词生成歌曲（异步，返回 `task_id`）
3. 轮询获取结果

**基础 URL：** `https://api.senseaudio.cn`
**鉴权：** `Authorization: Bearer $SENSEAUDIO_API_KEY`

---

## 1. 音乐歌词生成请求

**POST** `/v1/song/lyrics/create`

- 原始链接：https://senseaudio.cn/docs/song/lyrics_create

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| prompt | string | 是 | 歌词生成提示词 |
| provider | string | 是 | 模型，目前只支持 `sensesong` |

**同步响应示例：**
```json
{
  "data": [
    {
      "text": "[intro-medium] ; [verse] We stand upon the edge of dawn... ; [chorus] Rise up now...",
      "title": ""
    }
  ]
}
```

**异步响应：** 返回 `task_id`，需通过歌词轮询接口获取结果。

---

## 2. 音乐歌词轮询

**GET** `/v1/song/lyrics/pending/:task_id`

- 原始链接：https://senseaudio.cn/docs/song/lyrics_pending

使用创建歌词任务得到的异步任务 ID 获取歌词数据。

**响应示例：**
```json
{
  "task_id": "bcee6b21-dcf9-44d1-9b85-7bfef0e840db",
  "status": "SUCCESS",
  "response": {
    "task_id": "bcee6b21-dcf9-44d1-9b85-7bfef0e840db",
    "data": [{"text": "...", "title": ""}]
  }
}
```

任务状态：`PENDING`（处理中）| `SUCCESS`（成功）| `FAILED`（失败）

---

## 3. 音乐歌曲生成请求

**POST** `/v1/song/music/create`

- 原始链接：https://senseaudio.cn/docs/song/music_create

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| model | string | 是 | 模型，目前只能使用 `sensesong` |
| lyrics | string | 否 | 歌词内容 |
| instrumental | bool | 否 | 是否为纯音乐（无人声） |
| style | string | 否 | 歌曲风格（如 "pop"、"rock"） |
| style_weight | string | 否 | 风格权重，取值 0–1 |
| title | string | 否 | 歌曲标题 |
| vocal_gender | string | 否 | 人声性别：`f` 女性，`m` 男性 |
| negative_tags | string | 否 | 排除的风格元素 |

**响应示例：**
```json
{"task_id": "50f979f5-2b9e-4254-8653-c277644a31fa"}
```

---

## 4. 音乐歌曲轮询

**GET** `/v1/song/music/pending/:task_id`

- 原始链接：https://senseaudio.cn/docs/song/music_pending

使用创建歌曲任务得到的异步任务 ID 获取歌曲数据。

**响应示例：**
```json
{
  "task_id": "50f979f5-...",
  "status": "SUCCESS",
  "response": {
    "task_id": "50f979f5-...",
    "data": [
      {
        "audio_url": "https://...",
        "lyrics": "...",
        "duration": 110
      }
    ]
  }
}
```

任务状态：`PENDING`（处理中）| `SUCCESS`（成功）| `FAILED`（失败）

---

## 完整调用示例（Python）

```python
import requests
import time

API_KEY = "YOUR_API_KEY"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
BASE = "https://api.senseaudio.cn"

# 第一步：生成歌词
resp = requests.post(f"{BASE}/v1/song/lyrics/create",
    headers=HEADERS,
    json={"prompt": "一首关于夏天的流行歌曲", "provider": "sensesong"})
lyrics_text = resp.json()["data"][0]["text"]

# 第二步：生成歌曲
resp = requests.post(f"{BASE}/v1/song/music/create",
    headers=HEADERS,
    json={"model": "sensesong", "lyrics": lyrics_text, "style": "pop", "vocal_gender": "f"})
task_id = resp.json()["task_id"]

# 第三步：轮询结果
while True:
    resp = requests.get(f"{BASE}/v1/song/music/pending/{task_id}", headers=HEADERS)
    result = resp.json()
    if result["status"] == "SUCCESS":
        print("音频地址：", result["response"]["data"][0]["audio_url"])
        break
    elif result["status"] == "FAILED":
        print("生成失败")
        break
    time.sleep(5)
```
