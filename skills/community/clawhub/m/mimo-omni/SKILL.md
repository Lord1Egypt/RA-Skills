---
name: mimo-omni
description: 使用小米 MiMo 的多模态模型分析和理解图片、视频和音频。当用户发送图片/视频/音频附件，询问视觉内容，请求图片描述、OCR、物体检测、场景理解、视频分析或音频转录/理解时使用。
---

# 视觉与音频理解 / Vision & Audio Understanding (MiMo API)

通过 `mimo_api.sh`（Curl）或 `mimo_api.py`（Python）调用小米 MiMo 多模态模型，支持图片、视频、音频输入。两个工具参数完全一致。
Call the Xiaomi MiMo multimodal model via `mimo_api.sh` (Curl) or `mimo_api.py` (Python). Supports image, video, and audio inputs. Both tools share identical parameters.

> **Windows 环境强制使用 `python mimo_api.py`**（不支持 bash）。macOS/Linux 优先使用 `bash mimo_api.sh`。
> **Windows MUST use `python mimo_api.py`** (no bash/curl). macOS/Linux prefers `bash mimo_api.sh`。
> **注意：Windows 用户不需要安装 Git 或 WSL！** 直接用 Python 就行。
> **Note: Windows users do NOT need Git or WSL!** Just use Python directly.

## 通用调用格式 / General Call Format

问题参数支持任意自然语言，直接传入用户的原始 query 即可：
The question supports any natural language — just pass the user's original query:

```bash
# 用户问什么就传什么，不需要改写 / Pass whatever the user asked, no rewriting needed
bash mimo_api.sh image /path/to/photo.jpg "<用户的问题 / user's question>"
bash mimo_api.sh video /path/to/video.mp4 "<用户的问题 / user's question>" --fps 1
bash mimo_api.sh audio /path/to/audio.wav "<用户的问题 / user's question>"

# 示例 / Example
bash mimo_api.sh image /path/to/cat.jpg "这张图里的猫是什么品种？/ What breed is the cat in this picture?"
```

---

## 图片 / Image

```bash
# 🪟 Windows (Python) — 直接用，无需 Git/WSL
python mimo_api.py image "https://example.com/photo.jpg" "描述这张图片 / Describe this image" --max-tokens 65536
python mimo_api.py image /path/to/image.png "图中有哪些物体？/ What objects are in the image?" --max-tokens 65536
python mimo_api.py image /path/to/screenshot.png "提取图中所有文字，保持排版结构 / Extract all text, preserve layout" --max-tokens 262144

# 🍎 macOS / Linux (bash)
bash mimo_api.sh image "https://example.com/photo.jpg" "描述这张图片 / Describe this image" --max-tokens 65536
bash mimo_api.sh image /path/to/image.png "图中有哪些物体？/ What objects are in the image?" --max-tokens 65536
bash mimo_api.sh image /path/to/screenshot.png "提取图中所有文字，保持排版结构 / Extract all text, preserve layout" --max-tokens 262144

# 多图对比 / Multi-image comparison
python mimo_api.py images /path/to/img1.jpg /path/to/img2.jpg --question "比较这两张图片的异同 / Compare these two images" --max-tokens 65536
bash mimo_api.sh images /path/to/img1.jpg /path/to/img2.jpg --question "比较这两张图片的异同 / Compare these two images" --max-tokens 65536
```

---

## 视频 / Video

参数说明 / Parameters: `--fps` 每秒采样帧数 / frames per second, `--resolution` 分辨率模式 / resolution mode (default/max)

```bash
# 🪟 Windows (Python)
python mimo_api.py video /path/to/video.mp4 "描述视频内容 / Describe the video" --fps 1 --max-tokens 65536
python mimo_api.py video /path/to/short.mp4 "详细描述 / Detailed description" --fps 2 --max-tokens 65536
python mimo_api.py video /path/to/long.mp4 "用3-5句话概括 / Summarize in 3-5 sentences" --fps 0.5 --max-tokens 262144
python mimo_api.py video /path/to/sports.mp4 "识别关键动作 / Identify key actions" --fps 4 --max-tokens 65536
python mimo_api.py video /path/to/video.mp4 "识别视频中所有文字 / Extract all text" --fps 2 --resolution max --max-tokens 262144

# 🍎 macOS / Linux (bash)
bash mimo_api.sh video /path/to/video.mp4 "描述视频内容 / Describe the video" --fps 1 --max-tokens 65536
bash mimo_api.sh video /path/to/short.mp4 "详细描述 / Detailed description" --fps 2 --max-tokens 65536
bash mimo_api.sh video /path/to/long.mp4 "用3-5句话概括 / Summarize in 3-5 sentences" --fps 0.5 --max-tokens 262144
bash mimo_api.sh video /path/to/sports.mp4 "识别关键动作 / Identify key actions" --fps 4 --max-tokens 65536
bash mimo_api.sh video /path/to/video.mp4 "识别视频中所有文字 / Extract all text" --fps 2 --resolution max --max-tokens 262144
```

### 视频推荐配置速查 / Video Config Quick Reference

| 场景 / Scenario | `--fps` | `--resolution` | `--max-tokens` |
|---|---|---|---|
| 通用描述 / General | `1` | default | 65536 |
| 短视频 / Short (<30s) | `2` | default | 65536 |
| 长视频摘要 / Long (>5min) | `0.5` | default | 262144 |
| 动作识别 / Sports/Action | `4`~`8` | default | 65536 |
| OCR / 字幕提取 / Subtitles | `2` | max | 262144 |
| 教学 / PPT | `0.5` | max | 262144 |
| 图表 / Charts | `1` | max | 262144 |
| 字幕翻译 / Subtitle TL | `2` | max | 262144 |

> **Token 参考 / Token reference:** fps=1 → ~3168 tokens, fps=4 → ~6408 tokens. fps ×2 ≈ tokens ×2.

---

## 音频 / Audio

```bash
# 🪟 Windows (Python)
python mimo_api.py audio "https://example.com/audio.wav" "转录音频内容 / Transcribe the audio" --max-tokens 65536
python mimo_api.py audio /path/to/audio.mp3 "转录并区分说话人 / Transcribe, identify speakers" --max-tokens 65536
python mimo_api.py audio /path/to/audio.wav "描述音频中的声音 / Describe sounds (speech, music, ambience)" --max-tokens 65536

# 🍎 macOS / Linux (bash)
bash mimo_api.sh audio "https://example.com/audio.wav" "转录音频内容 / Transcribe the audio" --max-tokens 65536
bash mimo_api.sh audio /path/to/audio.mp3 "转录并区分说话人 / Transcribe, identify speakers" --max-tokens 65536
bash mimo_api.sh audio /path/to/audio.wav "描述音频中的声音 / Describe sounds (speech, music, ambience)" --max-tokens 65536
```

---

## 视频 + 音频联合 / Mixed Video + Audio

```bash
# 🪟 Windows (Python)
python mimo_api.py mixed --video /path/to/video.mp4 --audio /path/to/audio.mp3 "描述视频并转录音频 / Describe video & transcribe audio" --max-tokens 262144

# 🍎 macOS / Linux (bash)
bash mimo_api.sh mixed --video /path/to/video.mp4 --audio /path/to/audio.mp3 "描述视频并转录音频 / Describe video & transcribe audio" --max-tokens 262144
```

---

## 返回格式 / Response Format

API 原始返回为 JSON / Raw API response is JSON:
```json
{
  "choices": [{"message": {"role": "assistant", "content": "..."}}],
  "usage": {"prompt_tokens": 4026, "completion_tokens": 474, "total_tokens": 4500}
}
```

脚本自动解析，输出两部分 / Script auto-parses into two outputs:
- **stderr**（调试 / debug info）：`[9.0s | prompt=4026, completion=474]`
- **stdout**（模型回复 / model reply）：纯文本内容 / plain text content

将 stdout 的内容直接作为回答返回给用户即可 / Return stdout content directly to the user.

---

## 文件大小限制 / File Size Limits

- 本地文件会被 base64 编码后上传，**API 限制 base64 数据最大 10MB** / Local files are base64-encoded; **API limit: 10MB for base64 data**
- 图片和音频通常不超限；**视频文件容易超限** / Images & audio are fine; **video files often exceed the limit**
- 超限时返回 / Error on limit: `exceeded maximum size limit for video base64 data (max: 10MB)`
- **解决方案 / Solution:** 大文件优先使用 URL / Prefer URL for large files:
  ```bash
  python mimo_api.py video "https://example.com/large.mp4" "描述 / Describe"  # ✅
  bash mimo_api.sh video "https://example.com/large.mp4" "描述 / Describe"  # ✅
  ```

---

## 超时与重试 / Timeout & Retry

- 默认超时 300s（5 分钟），适用于图片、短视频、音频 / Default: 300s (5min) for images, short video, audio
- **长视频（>2min）建议加 `--timeout 600`** / **Long videos (>2min): add `--timeout 600`**
  ```bash
  python mimo_api.py video /path/to/long.mp4 "概括 / Summarize" --fps 0.5 --timeout 600
  bash mimo_api.sh video /path/to/long.mp4 "概括 / Summarize" --fps 0.5 --timeout 600
  ```
- 超时重试建议 / Retry suggestions on timeout:
  1. 降低 `--fps` / Reduce `--fps`
  2. 改用 `--resolution default` / Switch to `--resolution default`
  3. 仍然超时则建议用户截取片段 / Still timing out? Ask user to clip a shorter segment

---

## 文件说明 / File Reference

| 文件 / File | 用途 / Purpose |
|---|---|
| `mimo_api.py` | Python CLI 调用工具 / Python CLI tool |
| `mimo_api.sh` | Bash/Curl CLI 调用工具 / Bash CLI tool |
