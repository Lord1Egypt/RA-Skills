---
name: huo15-douyin-video-summary
displayName: 抖音视频去水印总结
version: 1.1.0
description: "给一个抖音视频链接，下载无水印视频并提取音频，然后配合 huo15-openclaw-asr 转写、由 OpenClaw 自身生成内容总结文稿与章节结构。脚本只做确定性下载/转码工作，转写复用 ASR skill，总结由 OpenClaw LLM 完成——无需配置任何 API key。触发词：抖音总结、抖音文稿、视频总结、视频转文字、去水印下载、douyin summary。"
homepage: https://cnb.cool/huo15/ai/huo15-skills
metadata: { "openclaw": { "emoji": "🎬", "requires": { "bins": ["yt-dlp", "ffmpeg"] } } }
aliases:
  - 抖音视频去水印总结
  - 抖音视频总结
  - 抖音文稿
  - 视频总结
  - 视频转文字
  - 去水印下载
  - douyin summary
  - 抖音下载
---

# 抖音视频去水印 + 内容总结

> 抖音视频链接 → 下载无水印视频 + 提取音频 → ASR 转写 → OpenClaw 生成总结文稿

遵循 OpenClaw 原则 **"enhance the runtime, never duplicate it"**：
- **脚本只做确定性工作**：yt-dlp 下载、ffmpeg 转码（LLM 做不了的外部命令）
- **转写复用 `huo15-openclaw-asr` skill**：不重复造轮子
- **总结由 OpenClaw 本身完成**：OpenClaw 就是 LLM，无需脚本调 API

**零 API key 配置。**

---

## 工作流程

```
用户给抖音链接
    │
    ▼
[1] 脚本 scripts/douyin_download.py
    yt-dlp 下载无水印视频 → ffmpeg 提取 audio.mp3
    │
    ▼
[2] 复用 huo15-openclaw-asr skill
    audio.mp3 → Whisper 本地转写 → transcript.txt
    │
    ▼
[3] OpenClaw 自身（LLM）
    transcript.txt → 生成总结文稿 + 章节分析
```

---

## 步骤 1：下载去水印视频 + 提取音频

```bash
python3 scripts/douyin_download.py "https://v.douyin.com/xxxxx/" -o ./output
```

输出：
- `output/video.mp4` — 无水印视频（yt-dlp 从抖音 API 获取无水印源）
- `output/audio.mp3` — 音频（MP3 格式，ASR skill 的标准输入）

**依赖**：`yt-dlp` + `ffmpeg`（macOS: `brew install yt-dlp ffmpeg`）

**无水印原理**：yt-dlp 的 Douyin extractor 从抖音 API 获取 `play_addr`（无水印源），非录屏去水印。抖音需浏览器 fresh cookies，脚本自动从 Chrome/Safari/Firefox 导入（无需登录态）。

---

## 步骤 2：转写（复用 ASR skill）

拿到 `audio.mp3` 后，**调用 `huo15-openclaw-asr` skill** 做转写：

- 本地优先：openai-whisper（`whisper "audio.mp3" --model base --language Chinese`）
- 说话人分离：WhisperX
- 云端（可选）：`huo15-openclaw-asr-bailian`（百炼 Paraformer）

转写产出 `transcript.txt`（逐字原文）。

> 不要在本 skill 内重复实现 ASR——那是 `huo15-openclaw-asr` 的职责。

---

## 步骤 3：内容总结（OpenClaw 自身）

OpenClaw 拿到转录文本后，**直接生成总结**（OpenClaw 本身就是 LLM，无需脚本调 API）。建议输出格式：

```markdown
### 📌 一句话总结
（视频核心内容）

### 📝 详细总结
（300-600 字，按逻辑段落组织）

### 🔑 关键要点
- 要点 1
- 要点 2

### 📑 章节结构
1. [章节标题] — 摘要
2. [章节标题] — 摘要

### 🏷️ 标签
#话题1 #话题2
```

总结须严格基于转录原文，不杜撰未出现的信息。

---

## 依赖

| 依赖 | 用途 | 安装 |
|---|---|---|
| yt-dlp | 下载无水印视频 | `brew install yt-dlp` |
| ffmpeg | 提取音频 | `brew install ffmpeg` |
| huo15-openclaw-asr | 语音转写 | `clawhub install huo15-openclaw-asr` |

转写依赖见 `huo15-openclaw-asr` 文档（openai-whisper / WhisperX）。

---

## 对话示例

```
用户: 帮我总结这个抖音视频 https://v.douyin.com/xxxxx/
Agent: [步骤1] 运行 douyin_download.py 下载无水印视频...
       ✅ video.mp4 (58MB) + audio.mp3 (3MB)
       [步骤2] 调用 huo15-openclaw-asr 转写 audio.mp3...
       ✅ 转录完成 (4500字)
       [步骤3] 基于转录生成总结：

       ### 📌 一句话总结
       ...

       ### 📝 详细总结
       ...
```

---

## 注意事项

1. **抖音 cookies**：脚本自动从浏览器导入，无需登录态
2. **合规**：仅用于个人学习分析，不二次分发原视频
3. **长视频**：Whisper 本地转写长视频较慢，可改用 `huo15-openclaw-asr-bailian` 云端
4. **音频格式**：脚本输出 MP3（非 WAV），体积小，是 ASR skill 的标准输入格式

---

## 版本历史

- **v1.1.0**（2026-07）— 架构重构：脚本只做下载+音频提取，转写交给 `huo15-openclaw-asr`，总结交给 OpenClaw 自身。零 API key 配置，遵循 "enhance the runtime, never duplicate it"
- v1.0.0 — 首版（含内置 ASR/LLM API 调用，已废弃）
