---
name: image-ai-kit
description: AI图像工具包 - 智能图像处理与增强 | AI Image Kit - Intelligent image processing and enhancement
homepage: https://github.com/openclaw/image-ai-kit
category: image-processing
tags: ["image", "ai", "opencv", "pillow", "ocr", "enhancement", "computer-vision"]
---

# Image AI Kit - AI图像工具包

智能图像处理解决方案，支持图像增强、风格迁移、智能裁剪和 OCR 文字识别。

## 核心功能

| 功能模块 | 说明 |
|---------|------|
| **图像增强** | 超分辨率、去噪、锐化、色彩增强 |
| **智能裁剪** | 自动识别主体，智能裁剪构图 |
| **OCR识别** | 文字提取，支持多语言 |
| **格式转换** | 支持 JPG/PNG/WebP/HEIC 等格式 |
| **批量处理** | 多图像并行处理 |

## 快速开始

```python
from scripts.image_enhancer import ImageEnhancer

# 图像增强
enhancer = ImageEnhancer()
enhancer.upscale('input.jpg', 'output.jpg', scale=2)

# OCR识别
from scripts.ocr_engine import OCREngine
ocr = OCREngine()
text = ocr.extract_text('image_with_text.png')
```

## 安装

```bash
pip install -r requirements.txt
```

## 项目结构

```
image-ai-kit/
├── SKILL.md                 # Skill说明文档
├── README.md                # 完整文档
├── requirements.txt         # 依赖列表
├── scripts/                 # 核心模块
│   ├── image_enhancer.py    # 图像增强器
│   ├── ocr_engine.py        # OCR引擎
│   └── image_utils.py       # 图像工具
├── examples/                # 使用示例
│   └── basic_usage.py
└── tests/                   # 单元测试
    └── test_image.py
```
