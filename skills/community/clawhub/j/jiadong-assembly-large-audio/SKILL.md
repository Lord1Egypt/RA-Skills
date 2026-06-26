---
name: assembly-large-audio-transcriber
description: Transcribe large audio files (100MB+, up to 1GB/12 hours) with speaker diarization. Uses AssemblyAI API with direct HTTP calls. Supports MP3, WAV, M4A, FLAC, OGG, WEBM. Zero SDK dependency.
metadata:
  openclaw:
    requires:
      env:
        - ASSEMBLYAI_API_KEY
    optional:
      tools: [exec, audios_understand]
---

# AssemblyAI Large Audio Transcriber

Transcribe超大音频文件（100MB~1GB）专用方案，零SDK依赖，直接调HTTP API。

## 功能

- 支持超大文件：最高 **1GB / 12小时**音频
- **说话人分离**（Speaker A/B/C…）
- **词级时间戳**
- 100+语言，自动检测
- MP3 / WAV / M4A / FLAC / OGG / WEBM 支持

## 安装依赖

服务器执行（只需一次）：
```bash
pip install requests
```

## 设置 API Key

在环境变量中设置：
```bash
export ASSEMBLYAI_API_KEY="your-key"
```

或告知许霸天你的 AssemblyAI API Key，我来配置。

免费额度：每月100分钟；付费约 $0.01/分钟。

## 使用方式

告诉许霸天：
> 用 AssemblyAI 转录 [文件路径]

支持本地文件和 URL。

## 技术方案

### 第一步：上传文件（针对大文件）
AssemblyAI 要求先上传获取 `upload_url`，再提交转录任务：

```python
import requests, os, time

API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
HEADERS = {"authorization": API_KEY}

# 1. 上传文件获取 upload_url
def upload_file(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.assemblyai.com/v2/upload",
            headers=HEADERS,
            data=f,
            timeout=300
        )
    response.raise_for_status()
    return response.json()["upload_url"]

# 2. 提交转录任务
def transcribe(upload_url, language="zh"):
    payload = {
        "audio_url": upload_url,
        "speaker_labels": True,
        "format_text": True,
        "language_code": language if language != "auto" else None,
    }
    if language == "auto":
        payload["language_detection"] = True
    response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=HEADERS,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    return response.json()["id"]

# 3. 轮询结果
def wait_for_result(transcript_id, poll_interval=5, max_wait=3600):
    start = time.time()
    while True:
        result = requests.get(
            f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
            headers=HEADERS,
            timeout=30
        )
        result.raise_for_status()
        data = result.json()
        status = data["status"]
        elapsed = time.time() - start
        if status == "completed":
            return data
        elif status == "error":
            raise Exception(f"Transcription error: {data.get('error')}")
        elif elapsed > max_wait:
            raise TimeoutError(f"Timeout after {max_wait}s")
        else:
            print(f"[{elapsed:.0f}s] Status: {status}...")
            time.sleep(poll_interval)

# 4. 完整流程
def transcribe_large_audio(file_path, language="auto"):
    print(f"上传中: {file_path}")
    upload_url = upload_file(file_path)
    print(f"提交转录任务...")
    tid = transcribe(upload_url, language)
    print(f"任务ID: {tid}")
    print("等待转录完成（可能需要数分钟）...")
    result = wait_for_result(tid)
    return result
```

### 处理结果

```python
result = transcribe_large_audio("/path/to/meeting.mp3", language="zh")

# 打印带说话人的转录
for utt in result.get("utterances", []):
    speaker = utt.get("speaker", "?")
    text = utt.get("text", "")
    start = utt.get("start", 0) / 1000  # 毫秒→秒
    print(f"[{speaker}] {start:.1f}s: {text}")

# 或打印纯文本
print(result.get("text", ""))
```

### 通过 URL 转录（如果文件已在网上）
如果文件可通过公网访问，直接提交 URL 更简单：

```python
def transcribe_url(audio_url, language="zh"):
    payload = {
        "audio_url": audio_url,
        "speaker_labels": True,
        "language_detection": True,
    }
    response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=HEADERS, json=payload, timeout=30
    )
    response.raise_for_status()
    tid = response.json()["id"]
    result = wait_for_result(tid)
    return result
```

## 完整使用示例

```python
import json, sys

file_path = sys.argv[1] if len(sys.argv) > 1 else "meeting.mp3"
language = sys.argv[2] if len(sys.argv) > 2 else "zh"

result = transcribe_large_audio(file_path, language)

output = {
    "file": file_path,
    "language": result.get("language_code"),
    "duration_s": result.get("audio_duration"),
    "transcript": result.get("text"),
    "utterances": [
        {
            "speaker": u.get("speaker"),
            "start_s": round(u.get("start", 0) / 1000, 2),
            "end_s": round(u.get("end", 0) / 1000, 2),
            "text": u.get("text"),
        }
        for u in result.get("utterances", [])
    ]
}

print(json.dumps(output, ensure_ascii=False, indent=2))
```

## 大文件处理流程（许霸天专用）

当用户提交超大音频文件时，按以下步骤执行：

1. 确认文件路径和大小
2. 确认 ASSEMBLYAI_API_KEY 已配置
3. 执行上面的 `transcribe_large_audio()` 流程
4. 轮询直到完成
5. 整理输出：按时间顺序输出每句话，带说话人和时间戳
6. 写文件存档：`/workspace/memory/meetings/{日期}-{会议名}_原始转录.md`

## 错误处理

| 错误 | 原因 | 解决 |
|------|------|------|
| 401 Unauthorized | API Key 无效或未设置 | 检查 ASSEMBLYAI_API_KEY |
| 413 Payload Too Large | 文件超 1GB | 需分割文件 |
| 422 Unprocessable Entity | 音频格式不支持 | 用 ffmpeg 转换格式 |
| 429 Rate Limit | 超出并发限制 | 等待后重试，降低轮询频率 |

## 文件分割（如果单文件超过1GB）

如遇 1GB 限制，用以下方式分割：

```bash
ffmpeg -i large.mp3 -ss 00:00:00 -to 01:00:00 -c copy part1.mp3
ffmpeg -i large.mp3 -ss 01:00:00 -c copy part2.mp3
```

再分别转录，最后拼接结果。
