# Minimax Image Generation Skills for OpenClaw

[English](#english) | [中文](#中文)

---

## English

### Overview

This is an **OpenClaw Skill** for generating images via the MiniMax API. It supports **Text-to-Image (T2I)** and **Image-to-Image (I2I)** generation.

### Features

- **Text-to-Image**: Generate images from text prompts
- **Image-to-Image**: Create variations based on a reference image (maintains character features)
- **Multiple Aspect Ratios**: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9
- **Multiple Output**: Generate 1-9 images in one request
- **Style Models** (requires premium subscription): Comic, Energetic, Medieval, Watercolor

### Requirements

- **MiniMax API Key** — Get it from [MiniMax Platform](https://platform.minimaxi.com)
- OpenClaw environment

### Installation

1. Install via ClawHub:
```bash
npx clawhub install lx-minimax
```

2. Set environment variable:
```bash
export MINIMAX_API_KEY="your-api-key-here"
```

### Quick Start

```bash
# Text-to-Image
python3 scripts/image_gen.py -p "A cute orange cat sleeping in sunlight" -r "16:9" -n 2

# Image-to-Image
python3 scripts/image_gen.py -p "Wearing a suit" -r "3:4" --reference "https://example.com/photo.jpg"

# With style (premium)
python3 scripts/image_gen.py -p "Sunset at the beach" -s "watercolor" -r "16:9"
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `-p, --prompt` | Required | Image description (max 1500 chars) |
| `-m, --model` | image-01 | Model: `image-01` or `image-01-live` |
| `-r, --ratio` | 1:1 | Aspect ratio |
| `-n` | 1 | Number of images [1-9] |
| `-s, --style` | - | Style type (image-01-live only) |
| `--reference` | - | Reference image URL or base64 (for I2I) |
| `-o, --output` | /home/ubuntu/.openclaw/workspace/images/ | Output directory |

### ⚠️ Security Warnings

#### 1. API Key Security
- 🔐 You MUST set `MINIMAX_API_KEY` environment variable
- 🔐 Never commit API keys to version control
- 🔐 Use scoped API keys with billing limits when possible

#### 2. Reference Image Privacy
- ⚠️ **Image-to-Image uploads reference images to MiniMax API**
- ⚠️ Do NOT use sensitive or private images as references
- ⚠️ Only use if you trust MiniMax's privacy policy

#### 3. Network Access
- 🌐 This skill accesses `https://api.minimaxi.com`
- 🌐 Generated image URLs expire in 24 hours
- 🌐 Ensure your network allows access to the above domain

#### 4. File Write
- 📁 Default output: `/home/ubuntu/.openclaw/workspace/images/`
- 📁 Can be changed via `--output` parameter

#### 5. Local Call Log
- 📝 Every successful call appends a log entry to `/home/ubuntu/.openclaw/workspace/minimax-image-generation-log.md`
- 📝 Logged: timestamp, call type (T2I/I2I), truncated prompt (max 80 chars), count, aspect ratio, local paths
- 📝 File is auto-created with header if it doesn't exist
- ⚠️ **Note**: If your workspace is synced to GitHub or shared, usage history will be exposed — be aware

### License

MIT License

---

## 中文

### 概述

这是面向 **OpenClaw** 的 **Minimax 图片生成 Skill**。支持**文生图（T2I）**和**图生图（I2I）**两种模式。

### 功能特点

- **文生图**：根据文字描述生成图片
- **图生图**：基于参考图生成新图，保持人物主体特征
- **多种比例**：1:1、16:9、4:3、3:2、2:3、3:4、9:16、21:9
- **批量生成**：单次请求可生成1-9张图片
- **画风模式**（需会员订阅）：漫画、元气、中世纪、水彩

### 环境要求

- **Minimax API Key** — 从 [Minimax 开放平台](https://platform.minimaxi.com) 获取
- OpenClaw 环境

### 安装方式

1. 通过 ClawHub 安装：
```bash
npx clawhub install lx-minimax
```

2. 设置环境变量：
```bash
export MINIMAX_API_KEY="your-api-key-here"
```

### 快速开始

```bash
# 文生图
python3 scripts/image_gen.py -p "一只可爱的橘猫在阳光下打盹" -r "16:9" -n 2

# 图生图
python3 scripts/image_gen.py -p "穿着西装" -r "3:4" --reference "https://example.com/photo.jpg"

# 画风模式（会员）
python3 scripts/image_gen.py -p "海边日落" -s "水彩" -r "16:9"
```

### 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `-p, --prompt` | 必填 | 图片描述（最长1500字符） |
| `-m, --model` | image-01 | 模型：`image-01` 或 `image-01-live` |
| `-r, --ratio` | 1:1 | 宽高比 |
| `-n` | 1 | 生成数量 [1-9] |
| `-s, --style` | - | 画风类型（仅 image-01-live） |
| `--reference` | - | 参考图URL或base64（图生图用） |
| `-o, --output` | /home/ubuntu/.openclaw/workspace/images/ | 输出目录 |

### ⚠️ 安全风险提示

#### 1. API密钥安全
- 🔐 **必须设置 `MINIMAX_API_KEY` 环境变量**
- 🔐 请勿将API Key提交到版本控制系统
- 🔐 建议使用有限额的API Key，定期轮换

#### 2. 参考图隐私风险
- ⚠️ **图生图功能会将参考图片上传到Minimax API**
- ⚠️ 请勿使用敏感或私人图片作为参考图
- ⚠️ 仅在您信任Minimax的隐私政策时使用

#### 3. 网络访问
- 🌐 本skill会访问 `https://api.minimaxi.com`
- 🌐 生成的图片URL有效期为24小时
- 🌐 请确认您的网络环境允许访问上述地址

#### 4. 文件写入
- 📁 默认输出目录：`/home/ubuntu/.openclaw/workspace/images/`
- 📁 可通过 `--output` 参数修改

#### 5. 本地调用日志
- 📝 每次成功调用后，会自动在 `/home/ubuntu/.openclaw/workspace/minimax-image-generation-log.md` 追加一条日志
- 📝 记录内容：时间戳、调用类型（T2I/I2I）、prompt摘要（最多80字）、图片数量、宽高比、本地保存路径
- 📝 如文件不存在，会自动创建（包含表头）
- ⚠️ **注意**：如 workspace 同步到 GitHub 或分享给他人，使用记录也会一并暴露，请知悉

### 开源协议

MIT License
