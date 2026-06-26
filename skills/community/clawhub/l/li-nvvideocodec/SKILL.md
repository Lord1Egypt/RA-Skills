---
name: li_nvvideocodec
description: NVIDIA AV1视频批量压缩工具，使用FFmpeg调用NVIDIA NVENC硬件编码，支持智能压缩验证和多方案选择
version: 1.0.1
tags:
  - video
  - compression
  - nvidia
  - av1
  - ffmpeg
  - gpu
  - multilingual
compatible_agents:
  - hermes
  - openclaw
  - qwen-code
languages:
  - en
  - ja
  - ko
  - zh-CN
  - zh-TW
  - fr
  - de
  - es
  - ru
  - ar
---

# li_nvvideocodec - NVIDIA AV1 视频压缩工具

## 🌍 多语言支持 / Multi-Language Support

本工具支持10种语言：

| 语言 | 代码 | 文档路径 |
|------|------|----------|
| 🇺🇸 English | en | `locales/en/README.md` |
| 🇯🇵 日本語 | ja | `locales/ja/README.md` |
| 🇰🇷 한국어 | ko | `locales/ko/README.md` |
| 🇨🇳 简体中文 | zh-CN | `locales/zh-CN/README.md` |
| 🇹🇼 繁體中文 | zh-TW | `locales/zh-TW/README.md` |
| 🇫🇷 Français | fr | `locales/fr/README.md` |
| 🇩🇪 Deutsch | de | `locales/de/README.md` |
| 🇪🇸 Español | es | `locales/es/README.md` |
| 🇷🇺 Русский | ru | `locales/ru/README.md` |
| 🇸🇦 العربية | ar | `locales/ar/README.md` |

## 📋 功能简介

使用NVIDIA GPU硬件加速的AV1视频批量压缩工具，可以：
- 🎯 **智能验证** - 自动测试压缩效果，避免无效压缩
- 📊 **三种方案** - 保守/平衡/激进，满足不同需求
- 🖥️ **双平台** - 支持Windows和Ubuntu Linux
- 📈 **实时进度** - 显示压缩进度和详细统计
- 🔒 **安全保护** - 原文件不删除，输出到独立目录

**兼容Agent**: hermes, openclaw, qwen-code

## 🚀 快速使用

### 基本用法

```bash
# 交互式模式（会引导你选择参数）
python scripts/compress_videos.py

# 指定目录和方案
python scripts/compress_videos.py -i "输入目录" -p B

# 测试模式（只压缩1个视频验证）
python scripts/compress_videos.py -i "输入目录" -p B --test --test-count 1 --no-confirm

# 完整压缩（非交互）
python scripts/compress_scripts/compress_videos.py -i "输入目录" -p B --no-confirm
```

## 📊 压缩方案

| 方案 | 分辨率 | CRF | 帧率 | 音频 | 预估节省 | 适用场景 |
|------|--------|-----|------|------|----------|----------|
| **A** | 保持原样 | 23 | 保持 | 128k | 40-60% | 追求质量 |
| **B** ⭐ | 1280x720 | 24 | 24fps | 96k | 65-75% | **平衡推荐** |
| **C** | 1280x720 | 28 | 15fps | 64k | 78-85% | 最大节省 |

## ⚙️ 系统要求

### 必需
- ✅ **FFmpeg** - 需要支持av1_nvenc编码器
- ✅ **NVIDIA GPU** - GTX 1650及以上（支持NVENC）
- ✅ **NVIDIA驱动** - 已安装并正常工作
- ✅ **Python 3.7+** - 运行脚本

### 可选
- tqdm库 - 显示进度条（脚本会自动安装）

### 安装FFmpeg

**Windows:**
```bash
# 下载: https://ffmpeg.org/download.html
# 解压后将ffmpeg.exe添加到PATH
```

**Ubuntu:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## 📝 完整参数

| 参数 | 简写 | 说明 | 示例 |
|------|------|------|------|
| `--input` | `-i` | 输入视频目录 | `-i "E:\视频"` |
| `--output` | `-o` | 输出目录 | `-o "F:\压缩后"` |
| `--profile` | `-p` | 压缩方案 (A/B/C) | `-p B` |
| `--test` | | 测试模式 | `--test` |
| `--test-count` | | 测试文件数 | `--test-count 5` |
| `--no-confirm` | | 跳过确认 | `--no-confirm` |

## 🔍 工作流程

```
1. 环境检查
   ↓
   检查FFmpeg、GPU、编码器支持
   ↓
2. 选择压缩方案
   ↓
   A（保守）/ B（平衡）/ C（激进）
   ↓
3. 验证压缩效果
   ↓
   测试压缩1个小视频，对比大小
   ↓
4. 智能判断
   ↓
   如果有效 → 继续批量压缩
   如果无效 → 提示取消任务
   ↓
5. 批量压缩
   ↓
   显示进度、统计信息
   ↓
6. 生成报告
```

## ⚠️ 重要提示

### B站视频等特殊情況

如果视频来自B站（Bilibili）等平台：
- 这些视频已被高度压缩（低码率）
- AV1压缩可能**不会节省空间**
- 脚本会自动检测并提示

### 原文件保护

- ✅ 原文件**不会删除**
- ✅ 压缩文件输出到**独立目录**
- ✅ 可以安全对比测试

## 📞 技术支持

如遇问题，请检查：
1. NVIDIA驱动是否正常（`nvidia-smi`）
2. FFmpeg是否安装（`ffmpeg -version`）
3. FFmpeg是否支持av1_nvenc（`ffmpeg -encoders | grep av1_nvenc`）

## 📄 许可证

作者: 北京老李 (beijingLL)
