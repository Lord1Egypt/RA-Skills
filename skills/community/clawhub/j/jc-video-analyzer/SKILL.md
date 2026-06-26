---
name: video-analyzer
description: "Parse local video files into transcript and AI analysis. Extract audio, transcribe with faster-whisper, analyze with AI."
---

# Video Analyzer

本地视频文件解析管线：提取音频 → 语音转文字 → AI 深度分析。

## 前置条件

- **ffmpeg** — 系统 PATH 中可用
- **faster-whisper** — `pip install faster-whisper`
- **HF 模型下载** — 国内需设 `HF_ENDPOINT=https://hf-mirror.com`
- **中转站 API** — 从 `openclaw.json` 读取 `SU2_API_KEY`

## 工作流程

```
视频文件 → ffmpeg提取音频(16kHz WAV) → faster-whisper转写 → AI修正+分析
```

### Step 1: 检查视频信息

```bash
ffprobe -v quiet -print_format json -show_format -show_streams <video.mp4>
```

### Step 2: 提取音频

```bash
ffmpeg -i <video.mp4> -vn -acodec pcm_s16le -ar 16000 -ac 1 audio_16k.wav -y
```

### Step 3: 转写（用脚本）

```bash
# Windows
$env:HF_ENDPOINT='https://hf-mirror.com'
python scripts/transcribe.py <audio.wav> <output.txt>

# Linux/macOS
HF_ENDPOINT=https://hf-mirror.com python scripts/transcribe.py <audio.wav> <output.txt>
```

参数：`python scripts/transcribe.py <audio.wav> <output.txt> [model=tiny] [language=zh]`

### Step 4: AI 分析（用脚本）

```bash
node scripts/analyze.js <transcript.txt> <output.md>
```

分析内容：修正转写稿 + 核心观点 + 结构化对比 + 启示总结。

### 可选：提取关键帧

```bash
ffmpeg -i <video.mp4> -vf "fps=1/60,scale=640:-1" frame_%03d.jpg -y
```

## 输出

- `audio_16k.wav` — 提取的音频
- `transcript.txt` — 带时间戳的原始转写
- `transcript_corrected.md` — AI 修正后文字稿
- `analysis.md` — AI 分析报告
- `frame_*.jpg` — 关键帧（可选）

## 注意事项 / 踩坑记录

- **tiny 模型识别率一般**，专业术语会有同音错误，依赖 AI 修正。可换 `base` 或 `small` 提升质量。
- **python3** — Windows 上可能指向 Windows Store 别名，用 `python` 代替。
- **HF_ENDPOINT** — 国内必须设 `hf-mirror.com`，否则模型下载极慢或失败。
- **中转站 502** — 偶尔出现，重试即可。也可换其他模型。
- **编码** — Python 输出时设 `PYTHONIOENCODING=utf-8`。
