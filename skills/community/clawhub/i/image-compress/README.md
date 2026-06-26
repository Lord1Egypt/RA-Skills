# Image Compress Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![sharp](https://img.shields.io/badge/Powered%20by-sharp-brightgreen)](https://sharp.pixelplumbing.com)

> 🌏 [English Version](#english-version) | [简体中文](#简体中文版)

---

# 简体中文版

## 📖 概述

**Image Compress Skill** 是一个面向 OpenClaw 的跨平台图片压缩工具。它提供智能压缩，在保持优秀画质的同时，最高可节省 75% 的文件体积。

### ✨ 特性

- 🚀 **高压缩率** - PNG 最高 75%，JPG 最高 54% 体积节省
- 🎨 **智能画质** - 针对截图优化的颜色量化（1024 色）
- 🌐 **跨平台** - macOS、Windows、Linux 全支持
- 📦 **多格式** - JPG、PNG、WebP、AVIF、HEIC
- ⚡ **快速处理** - 基于 sharp (libvips) 高性能引擎
- 🔒 **安全** - 永不覆盖原图，自动重命名保护

---

## 🚀 快速开始

### 安装

```bash
# 克隆到 OpenClaw 技能目录
git clone https://github.com/JustZeroX/skill-image-compress.git \
  ~/.openclaw/workspace/skills/image-compress

# 安装依赖
cd ~/.openclaw/workspace/skills/image-compress
npm install
```

### 基础用法

```bash
# 压缩单张图片（默认设置）
/compress ~/Desktop/photo.png

# 使用预设（推荐）
/compress photo.jpg --preset web        # 网页优化
/compress photo.jpg --preset wechat     # 微信发送
/compress photo.jpg --preset email      # 邮件附件
/compress photo.jpg --preset quality    # 高质量存档

# 自定义参数
/compress photo.png -f webp -q 0.6 -w 1920  # 格式 + 画质 + 尺寸
/compress ./photos/ -p web -r               # 批量 + 预设 + 递归
```

---

## 📊 压缩性能

### PNG 截图压缩

| 原图 | 优化后 | 节省 |
|------|--------|------|
| 380.7 KB | 95.0 KB | **75.0%** |

### JPEG 照片压缩

| 原图 | 优化后 | 节省 |
|------|--------|------|
| 88.8 KB | 40.7 KB | **54.1%** |

### WebP 格式对比

| 格式 | 画质 | 大小 | 节省 |
|------|------|------|------|
| PNG | 无损 | 380.7 KB | - |
| WebP | 75% | 65.2 KB | **82.9%** |
| WebP | 65% | 48.5 KB | **87.3%** |

---

## 📋 参数说明

### 预设模式

| 预设 | 画质 | 适用场景 | 压缩率 |
|------|------|----------|--------|
| `web` | 75% | 网页展示、博客文章 | 60-70% |
| `wechat` | 65% | 微信发送、社交媒体 | 70-80% |
| `email` | 55% | 邮件附件、快速传输 | 80-90% |
| `quality` | 95% | 高质量存档、打印 | 30-40% |

### 命令行选项

| 选项 | 简写 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `--format` | `-f` | string | `original` | 输出格式：`jpg`, `png`, `webp`, `avif` |
| `--quality` | `-q` | number | `0.85` | 画质 (0.1-1.0)，越低体积越小 |
| `--maxWidth` | `-w` | number | `null` | 最大宽度（等比缩放） |
| `--maxHeight` | `-h` | number | `null` | 最大高度（等比缩放） |
| `--recursive` | `-r` | boolean | `false` | 递归处理子文件夹 |
| `--preset` | `-p` | string | `无` | 预设：`web`, `wechat`, `email`, `quality` |

---

## 📁 输出结构

```
~/Downloads/compressed-images/
├── 2026-03-11/
│   ├── photo.png              # 保持原名
│   ├── photo_001.png          # 同名自动编号
│   └── trip/
│       └── image001.jpg       # 保持原目录结构
└── 2026-03-12/
    └── ...
```

---

## 🔧 开发指南

### 项目结构

```
skill-image-compress/
├── SKILL.md                  # 技能定义
├── README.md                 # 本文件
├── LICENSE                   # MIT 许可证
├── package.json              # 依赖定义
├── scripts/
│   ├── detect-env.js         # 环境检测
│   ├── install.js            # 依赖安装
│   ├── post-install.js       # 安装后配置
│   └── compress.js           # 核心压缩逻辑
├── references/
│   └── technical.md          # 技术文档
├── evals/
│   └── evals.json            # 测试用例
└── assets/
    └── eval_review.html      # 评估界面
```

### 安装依赖

```bash
npm install
```

### 运行测试

```bash
# 压缩测试图片
node scripts/compress.js ~/test.png

# 自定义参数
node scripts/compress.js ~/test.png -f webp -q 0.6
```

---

## 🎯 优化技术

### PNG 压缩

```javascript
processor.png({
  compressionLevel: 9,    // 最大压缩级别
  palette: true,          // 颜色量化
  colors: 1024,           // 1024 色（平衡画质和体积）
  dither: 0.5,            // 抖动处理
  strip: true             // 移除元数据
})
```

### JPEG 压缩

```javascript
processor.jpeg({
  quality: 85,            // 质量级别
  progressive: true,      // 渐进式加载
  strip: true             // 移除元数据
})
```

---

## 📝 使用示例

### 单张图片压缩

```bash
# 默认压缩（85% 画质）
/compress ~/Desktop/screenshot.png

# 输出：~/Downloads/compressed-images/2026-03-11/screenshot.png
```

### 批量压缩

```bash
# 压缩文件夹内所有图片
/compress ~/Photos/trip/ --recursive

# 全部转换为 WebP 格式
/compress ~/Photos/ -f webp -r
```

### 格式转换

```bash
# PNG 转 JPG（透明通道用白色填充）
/compress image.png --format jpg

# HEIC 转 JPG（iPhone 照片）
/compress IMG_1234.HEIC --format jpg
```

---

## ⚠️ 安全特性

- ✅ **永不覆盖** - 原图始终保留，输出到独立目录
- ✅ **自动重命名** - 重名文件添加 `_001`, `_002` 后缀
- ✅ **大文件警告** - 超过 50MB 时提示确认
- ✅ **进度追踪** - 批量操作显示进度条

---

## 🤝 贡献指南

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [sharp](https://sharp.pixelplumbing.com/) - 高性能图像处理库
- [OpenClaw](https://openclaw.ai) - AI 助手框架
- [Anthropic Skills](https://github.com/anthropics/skills) - 技能系统参考

---

## 📧 联系方式

- GitHub: [@JustZeroX](https://github.com/JustZeroX)
- 项目：[https://github.com/JustZeroX/skill-image-compress](https://github.com/JustZeroX/skill-image-compress)

---

**[⬆ 返回顶部](#image-compress-skill)**

---

# English Version

## 📖 Overview

**Image Compress Skill** is a cross-platform image compression tool for OpenClaw. It provides intelligent compression with up to 75% size reduction while maintaining excellent quality.

### ✨ Features

- 🚀 **High Compression** - Up to 75% size reduction (PNG), 54% (JPEG)
- 🎨 **Smart Quality** - Color quantization optimized for screenshots (1024 colors)
- 🌐 **Cross-Platform** - macOS, Windows, Linux support
- 📦 **Multi-Format** - JPG, PNG, WebP, AVIF, HEIC
- ⚡ **Fast Processing** - Powered by sharp (libvips)
- 🔒 **Safe** - Never overwrites original files, auto-rename protection

---

## 🚀 Quick Start

### Installation

```bash
# Clone to OpenClaw skills directory
git clone https://github.com/JustZeroX/skill-image-compress.git \
  ~/.openclaw/workspace/skills/image-compress

# Install dependencies
cd ~/.openclaw/workspace/skills/image-compress
npm install
```

### Basic Usage

```bash
# Compress a single image (default settings)
/compress ~/Desktop/photo.png

# Use preset (recommended)
/compress photo.jpg --preset web        # Web optimization
/compress photo.jpg --preset wechat     # WeChat sharing
/compress photo.jpg --preset email      # Email attachment
/compress photo.jpg --preset quality    # High quality archive

# Custom parameters
/compress photo.png -f webp -q 0.6 -w 1920  # Format + Quality + Size
/compress ./photos/ -p web -r               # Batch + Preset + Recursive
```

---

## 📊 Compression Performance

### PNG Screenshots

| Original | Optimized | Savings |
|----------|-----------|---------|
| 380.7 KB | 95.0 KB | **75.0%** |

### JPEG Photos

| Original | Optimized | Savings |
|----------|-----------|---------|
| 88.8 KB | 40.7 KB | **54.1%** |

### WebP Comparison

| Format | Quality | Size | Savings |
|--------|---------|------|---------|
| PNG | Lossless | 380.7 KB | - |
| WebP | 75% | 65.2 KB | **82.9%** |
| WebP | 65% | 48.5 KB | **87.3%** |

---

## 📋 Parameters

### Presets

| Preset | Quality | Use Case | Savings |
|--------|---------|----------|---------|
| `web` | 75% | Web display | 60-70% |
| `wechat` | 65% | WeChat sharing | 70-80% |
| `email` | 55% | Email attachment | 80-90% |
| `quality` | 95% | High quality archive | 30-40% |

### Command Line Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--format` | `-f` | string | `original` | Output format: `jpg`, `png`, `webp`, `avif` |
| `--quality` | `-q` | number | `0.85` | Quality (0.1-1.0) |
| `--maxWidth` | `-w` | number | `null` | Maximum width (proportional) |
| `--maxHeight` | `-h` | number | `null` | Maximum height (proportional) |
| `--recursive` | `-r` | boolean | `false` | Process subdirectories |
| `--preset` | `-p` | string | `none` | Preset: `web`, `wechat`, `email`, `quality` |

---

## 📁 Output Structure

```
~/Downloads/compressed-images/
├── 2026-03-11/
│   ├── photo.png              # Original name
│   ├── photo_001.png          # Auto-renamed
│   └── trip/
│       └── image001.jpg       # Keep structure
└── 2026-03-12/
    └── ...
```

---

## 🔧 Development

### Project Structure

```
skill-image-compress/
├── SKILL.md                  # Skill definition
├── README.md                 # This file
├── LICENSE                   # MIT License
├── package.json              # Dependencies
├── scripts/
│   ├── detect-env.js         # Environment detection
│   ├── install.js            # Dependency installation
│   ├── post-install.js       # Post-install setup
│   └── compress.js           # Core compression logic
├── references/
│   └── technical.md          # Technical documentation
├── evals/
│   └── evals.json            # Test cases
└── assets/
    └── eval_review.html      # Review interface
```

### Install Dependencies

```bash
npm install
```

### Run Tests

```bash
# Compress a test image
node scripts/compress.js ~/test.png

# With custom parameters
node scripts/compress.js ~/test.png -f webp -q 0.6
```

---

## 🎯 Optimization Technology

### PNG Compression

```javascript
processor.png({
  compressionLevel: 9,    // Maximum compression
  palette: true,          // Color quantization
  colors: 1024,           // 1024 colors (balanced)
  dither: 0.5,            // Dithering
  strip: true             // Remove metadata
})
```

### JPEG Compression

```javascript
processor.jpeg({
  quality: 85,            // Quality level
  progressive: true,      // Progressive loading
  strip: true             // Remove metadata
})
```

---

## 📝 Examples

### Single Image

```bash
# Default compression (85% quality)
/compress ~/Desktop/screenshot.png

# Output: ~/Downloads/compressed-images/2026-03-11/screenshot.png
```

### Batch Compression

```bash
# Compress all images in folder
/compress ~/Photos/trip/ --recursive

# Convert all to WebP format
/compress ~/Photos/ -f webp -r
```

### Format Conversion

```bash
# PNG to JPG (white background for transparency)
/compress image.png --format jpg

# HEIC to JPG (iPhone photos)
/compress IMG_1234.HEIC --format jpg
```

---

## ⚠️ Safety Features

- ✅ **Never Overwrites** - Original files are always preserved
- ✅ **Auto-Rename** - Duplicate names get `_001`, `_002` suffixes
- ✅ **Large File Warning** - Prompts for files > 50MB
- ✅ **Progress Tracking** - Shows progress for batch operations

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [sharp](https://sharp.pixelplumbing.com/) - High performance image processing
- [OpenClaw](https://openclaw.ai) - AI assistant framework
- [Anthropic Skills](https://github.com/anthropics/skills) - Skill system reference

---

## 📧 Contact

- GitHub: [@JustZeroX](https://github.com/JustZeroX)
- Project: [https://github.com/JustZeroX/skill-image-compress](https://github.com/JustZeroX/skill-image-compress)

---

**[⬆ Back to Top](#image-compress-skill)**

---

<div align="center">

**Made with ❤️ for OpenClaw Community**

**为 OpenClaw 社区制作** ⭐

</div>
