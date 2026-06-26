# li_nvvideocodec - NVIDIA AV1 影片壓縮工具

**版本**: 1.0.1  
**語言**: 繁體中文 (zh-TW)

## 📋 概述

使用NVIDIA GPU硬體加速AV1編碼的批次影片壓縮工具。透過智慧驗證和多種壓縮方案高效壓縮影片。

## ✨ 特性

- 🎯 **智慧驗證** - 自動測試壓縮效果
- 📊 **三種方案** - 保守/平衡/激進
- 🖥️ **跨平台** - Windows 和 Ubuntu Linux
- 📈 **即時進度** - 顯示壓縮進度
- 🔒 **安全** - 保護原始檔案

## 🚀 快速開始

```bash
# 互動模式
python scripts/compress_videos.py

# 命令列模式
python scripts/compress_videos.py -i "/path/to/videos" -p B --no-confirm

# 測試模式
python scripts/compress_videos.py -i "/path/to/videos" -p B --test
```

## 📊 壓縮方案

| 方案 | 解析度 | CRF | 幀率 | 音訊 | 節省 |
|------|--------|-----|------|------|------|
| **A** | 保持原樣 | 23 | 保持 | 128k | 40-60% |
| **B** ⭐ | 1280x720 | 24 | 24 | 96k | 65-75% |
| **C** | 1280x720 | 28 | 15 | 64k | 78-85% |

## ⚙️ 系統需求

- **FFmpeg** (支援av1_nvenc)
- **NVIDIA GPU** (GTX 1650及以上)
- **Python 3.7+**

## 🤖 Agent使用

```bash
# 檢查環境
python agent_interface.py --action check

# 分析影片
python agent_interface.py --action analyze -i "/path/to/videos"

# 壓縮
python agent_interface.py --action compress -i "/path/to/videos" -p B
```
