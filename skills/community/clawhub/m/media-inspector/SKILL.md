---
name: media-inspector
description: 本地音视频文件分析工具。支持扫描媒体文件、提取元数据、语音转文字（Whisper）、生成摘要和关键片段。支持 MP4/MOV/MKV/MP3/WAV/M4A/FLAC 等格式。
---

# Media Inspector 📺 🎵

本地音视频文件分析工具，可扫描、提取元数据、转录、摘要和导出报告。

## 支持格式

**视频**: mp4, mov, mkv, avi, webm, m4v, ts, mpg, mpeg  
**音频**: mp3, wav, m4a, aac, flac, ogg, opus, aiff, wma

## 快速开始

### 1. 扫描媒体文件

```bash
python scripts/scan_media.py /path/to/media --out-dir ./media_scan
```

输出文件：
- `scan_results.json` - JSON格式
- `scan_results.csv` - CSV格式  
- `scan_results.md` - Markdown格式

### 2. 深度分析

```bash
python scripts/analyze_media.py /path/to/file.mp4 --out-dir ./media_analysis
```

分析内容：
1. 元数据提取（ffprobe）
2. 语音转文字（Whisper，可选）
3. 内容摘要
4. 关键片段提取（带时间戳）
5. 报告导出（JSON/CSV/Markdown）

## 依赖安装

```bash
# 必需：ffmpeg (包含 ffprobe)
brew install ffmpeg

# 可选：Whisper 语音转文字
pip install whisper
# 或
brew install whisper
```

## 使用规则

- ✅ 优先使用转录文本进行分析，不要仅凭文件名猜测
- ⚠️ Whisper 不可用时，明确告知用户并仅返回元数据
- ❌ 不要虚构内容摘要
- 📝 关键片段必须包含时间戳
- 📊 批量分析时，每个文件单独报告

## 输出示例

### 扫描报告
```markdown
# Media Scan Report

## Summary
- scanned path: /path/to/media
- files found: 10
- audio files: 3
- video files: 7

## Candidates
| filename | duration | type | file size |
|---|---|---|---|
| video.mp4 | 01:30:00 | video | 500.2 MB |
| audio.mp3 | 00:05:30 | audio | 5.2 MB |
```

### 分析报告
```markdown
# Media Analysis Report

## File
- path: /path/to/video.mp4
- type: video
- duration: 01:30:00

## Transcript
- available: yes
- whisper used: yes

## Summary
[基于转录文本的摘要内容]

## Key excerpts
1. [00:01:30 - 00:02:15] 关键片段内容...
2. [00:15:00 - 00:16:30] 另一个关键片段...
```
