---
name: minimax-image
description: MiniMax文生图(T2I)和图生图(I2I)工具 / MiniMax image generation tool supporting T2I and I2I. Generate 1-9 images per request with customizable aspect ratios.
version: 1.1.1
metadata: {"openclaw": {"homepage": "https://github.com/lixiang92229/lx-minimax-image-generation"}}
---

# Minimax Image Generation Skill

## 概述 | Overview

通过 MiniMax API 实现**文生图（T2I）**和**图生图（I2I）**功能。

Supports **Text-to-Image** and **Image-to-Image** generation via MiniMax API.

---

## 环境变量 | Environment Variables

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `MINIMAX_API_KEY` | 是 | MiniMax API密钥 / MiniMax API Key |

> ⚠️ **重要**: 本skill需要 `MINIMAX_API_KEY` 环境变量才能运行。请从 [MiniMax开放平台](https://platform.minimaxi.com) 获取API Key。

---

## 功能 | Features

### 1. 文生图 Text-to-Image

根据文字描述生成图片 / Generate images from text prompts:

```python
from scripts.image_gen import generate_image

result = generate_image(
    prompt="北京故宫角楼，晴空万里，摄影作品",
    model="image-01",
    aspect_ratio="16:9",
    n=2
)
```

### 2. 图生图 Image-to-Image

基于参考图片生成新图，保持人物主体特征 / Create variations using a reference image:

```python
result = generate_image(
    prompt="穿着中国传统服装，站在长城上",
    model="image-01",
    aspect_ratio="3:4",
    subject_reference=[
        {
            "type": "character",
            "image_file": "https://example.com/photo.jpg"  # 或 base64 Data URL
        }
    ],
    n=1
)
```

### 3. 画风生成 Style Models (需要订阅 / Requires subscription)

使用 `image-01-live` 模型指定画风 / Specify artistic styles:

| 风格 Style | 说明 |
|-----------|------|
| 漫画 | Comic/ Manga |
| 元气 | Energetic/ Youthful |
| 中世纪 | Medieval |
| 水彩 | Watercolor |

```python
result = generate_image(
    prompt="一位中国科学家在实验室",
    model="image-01-live",
    style_type="水彩",
    style_weight=0.8
)
```

---

## 命令行使用 | CLI Usage

```bash
# 1. 设置环境变量 / Set environment variable
export MINIMAX_API_KEY="your-api-key-here"

# 2. 文生图 / Text-to-Image
python3 scripts/image_gen.py -p "一只可爱的橘猫在阳光下打盹" -r "16:9" -n 2

# 3. 图生图 / Image-to-Image
python3 scripts/image_gen.py -p "穿着西装" -r "3:4" --reference "https://example.com/photo.jpg"

# 4. 指定画风 / With style
python3 scripts/image_gen.py -p "海边日落" -s "水彩" -r "16:9"
```

---

## 参数说明 | Parameters

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--prompt, -p` | 必填 | 图片描述，最长1500字符 / Image description, max 1500 chars |
| `--model, -m` | image-01 | 模型 / Model: `image-01` 或 `image-01-live` |
| `--ratio, -r` | 1:1 | 宽高比 / Aspect ratio: 1:1, 16:9, 4:3, 3:2, 2:3, 3:4, 9:16, 21:9 |
| `--n` | 1 | 生成数量1-9 / Number of images [1-9] |
| `--style, -s` | - | 画风类型（仅image-01-live）/ Style type for image-01-live |
| `--reference, -ref` | - | 参考图URL或base64（用于图生图）/ Reference image URL or base64 |
| `--output, -o` | - | 输出路径 / Output file path（默认: /home/ubuntu/.openclaw/workspace/images）|
| `--base64` | false | 返回base64格式 / Return base64 instead of downloading |

---

## 输出 | Output

默认输出目录: `/home/ubuntu/.openclaw/workspace/images/`

可通过 `--output` 参数自定义路径 / Can be customized via `--output` parameter.

返回 / Returns:
- `image_urls`: 图片URL列表 / List of image URLs
- `_local_paths`: 本地保存路径 / Local saved file paths

---

## ⚠️ 安全风险提示 | Security Warnings

### 1. API密钥安全 / API Key Security
- 🔐 **必须设置 `MINIMAX_API_KEY` 环境变量**
- 🔐 请勿将API Key提交到版本控制系统
- 🔐 建议使用限额的API Key，定期轮换

### 2. 参考图隐私风险 / Reference Image Privacy Risk
- ⚠️ **图生图功能会将参考图片上传到MiniMax API**
- ⚠️ 请勿使用敏感或私人图片作为参考图
- ⚠️ 除非您信任MiniMax的服务及其隐私政策

### 3. 网络访问 / Network Access
- 🌐 本skill会访问 `https://api.minimaxi.com`
- 🌐 生成的图片URL有效期为24小时
- 🌐 请确认您的网络环境允许访问上述地址

### 4. 文件写入 / File Write
- 📁 默认保存到 `/home/ubuntu/.openclaw/workspace/images/`
- 📁 可通过 `--output` 参数修改保存路径
- 📁 请确保目标目录有写入权限

### 5. 本地调用日志 / Local Call Log
- 📝 每次成功调用后，会自动在 `/home/ubuntu/.openclaw/workspace/minimax-image-generation-log.md` 追加一条日志
- 📝 记录内容：时间戳、调用类型（T2I/I2I）、prompt摘要（最多80字）、图片数量、宽高比、本地保存路径
- 📝 如文件不存在，会自动创建（包含表头）
- ⚠️ **注意**：如 workspace 同步到 GitHub 或分享给他人，使用记录也会一并暴露，请知悉

---

## 注意事项 | Notes

- ⚠️ `image-01-live` 需要会员订阅 / Requires premium subscription
- ⚠️ 图片URL有效期24小时 / Image URLs expire in 24 hours
- 图片建议小于10MB / Image should be under 10MB
- 参考图建议单人正面照片 / Reference: single person, frontal photo works best

---

## 详细API文档 | Full API Reference

- [API文档（中文）](references/api.md)
- [API Reference（English）](references/api_en.md)
