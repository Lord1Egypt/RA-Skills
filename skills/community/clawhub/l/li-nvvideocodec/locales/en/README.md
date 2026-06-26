# li_nvvideocodec - NVIDIA AV1 Video Compressor

**Version**: 1.0.1  
**Language**: English (en)

## 📋 Overview

A batch video compression tool using NVIDIA GPU hardware-accelerated AV1 encoding. Compress videos efficiently with intelligent validation and multiple compression profiles.

## ✨ Features

- 🎯 **Smart Validation** - Auto-test compression effectiveness
- 📊 **Three Profiles** - Conservative/Balanced/Aggressive
- 🖥️ **Cross-Platform** - Windows & Ubuntu Linux
- 📈 **Real-time Progress** - Live progress display
- 🔒 **Safe** - Original files protected

## 🚀 Quick Start

```bash
# Interactive mode
python scripts/compress_videos.py

# Command line mode
python scripts/compress_videos.py -i "/path/to/videos" -p B --no-confirm

# Test mode
python scripts/compress_videos.py -i "/path/to/videos" -p B --test
```

## 📊 Compression Profiles

| Profile | Resolution | CRF | FPS | Audio | Savings |
|---------|-----------|-----|-----|-------|---------|
| **A** | Original | 23 | Original | 128k | 40-60% |
| **B** ⭐ | 1280x720 | 24 | 24 | 96k | 65-75% |
| **C** | 1280x720 | 28 | 15 | 64k | 78-85% |

## ⚙️ Requirements

- **FFmpeg** with av1_nvenc support
- **NVIDIA GPU** (GTX 1650+)
- **Python 3.7+**

## 🤖 Agent Usage

```bash
# Check environment
python agent_interface.py --action check

# Analyze videos
python agent_interface.py --action analyze -i "/path/to/videos"

# Compress
python agent_interface.py --action compress -i "/path/to/videos" -p B
```

## 🌍 Supported Languages

This skill supports 10 languages:
- 🇺🇸 English (en)
- 🇯🇵 日本語 (ja)
- 🇰🇷 한국어 (ko)
- 🇨🇳 简体中文 (zh-CN)
- 🇹🇼 繁體中文 (zh-TW)
- 🇫🇷 Français (fr)
- 🇩🇪 Deutsch (de)
- 🇪🇸 Español (es)
- 🇷🇺 Русский (ru)
- 🇸🇦 العربية (ar)

See `locales/` directory for localized documentation.
