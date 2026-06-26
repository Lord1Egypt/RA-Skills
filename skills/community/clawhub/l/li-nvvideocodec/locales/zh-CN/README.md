# li_nvvideocodec - NVIDIA AV1 视频压缩工具

**版本**: 1.0.1  
**语言**: 简体中文 (zh-CN)

## 📋 概述

使用NVIDIA GPU硬件加速AV1编码的批量视频压缩工具。通过智能验证和多种压缩方案高效压缩视频。

## ✨ 特性

- 🎯 **智能验证** - 自动测试压缩效果
- 📊 **三种方案** - 保守/平衡/激进
- 🖥️ **跨平台** - Windows 和 Ubuntu Linux
- 📈 **实时进度** - 显示压缩进度
- 🔒 **安全** - 保护原始文件

## 🚀 快速开始

```bash
# 交互模式
python scripts/compress_videos.py

# 命令行模式
python scripts/compress_videos.py -i "/path/to/videos" -p B --no-confirm

# 测试模式
python scripts/compress_videos.py -i "/path/to/videos" -p B --test
```

## 📊 压缩方案

| 方案 | 分辨率 | CRF | 帧率 | 音频 | 节省 |
|------|--------|-----|------|------|------|
| **A** | 保持原样 | 23 | 保持 | 128k | 40-60% |
| **B** ⭐ | 1280x720 | 24 | 24 | 96k | 65-75% |
| **C** | 1280x720 | 28 | 15 | 64k | 78-85% |

## ⚙️ 系统要求

- **FFmpeg** (支持av1_nvenc)
- **NVIDIA GPU** (GTX 1650及以上)
- **Python 3.7+**

## 🤖 Agent使用

```bash
# 检查环境
python agent_interface.py --action check

# 分析视频
python agent_interface.py --action analyze -i "/path/to/videos"

# 压缩
python agent_interface.py --action compress -i "/path/to/videos" -p B
```
