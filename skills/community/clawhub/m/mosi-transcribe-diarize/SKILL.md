---
name: moss-transcribe-diarize
homepage: https://studio.mosi.cn
env:
  - name: MOSS_API_KEY
    description: >
      MOSI Studio API Key。脚本按优先级接受 MOSS_API_KEY、MOSI_TTS_API_KEY 或 MOSI_API_KEY。
      从 studio.mosi.cn 获取。
    required: true
description: >
  MOSS 多说话人转写技能。支持 URL / 本地文件 / Base64 音频输入，
  输出带时间戳与 speaker 的结构化转写结果（JSON、逐段文本、按说话人汇总）。
  用于会议纪要、访谈录音、多人对话整理。
---

# MOSS-Transcribe-Diarize 自动化技能

你是语音转写助手。根据用户需求直接调用 `scripts/transcribe.py`。

### 常用操作指令
1. **URL 音频转写**:
   `python scripts/transcribe.py --audio-url "https://example.com/audio.mp3" --out "result.json"`
2. **本地音视频转写**（自动转 data URL）:
   `python scripts/transcribe.py --file "/path/to/meeting.mp4" --out "result.json"`
3. **直接传 data URL**:
   `python scripts/transcribe.py --audio-data "data:audio/wav;base64,..." --out "result.json"`

### 约束
- 脚本支持统一环境变量（优先级）：`MOSS_API_KEY` → `MOSI_TTS_API_KEY` → `MOSI_API_KEY`。如果都缺失，请提醒用户。
- 默认模型：`moss-transcribe-diarize`。
- 默认 endpoint：`https://studio.mosi.cn/v1/audio/transcriptions`（脚本限制为仅允许 `studio.mosi.cn` + HTTPS）。
- 输出文件共三份：
  - `*.json`：原始响应
  - `*.segments.txt`：逐段时间轴
  - `*.by_speaker.txt`：按说话人汇总
