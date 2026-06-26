---
name: liaogong-ocr
version: 1.0.0
description: "🔍 廖工AI设计实战出品 | LiaoGong-OCR — easyocr+tesseract双引擎OCR，15条预处理链含实测基准，手机拍屏数字识别87%准确率。支持中文海报/截图/英文文档/手机拍照/批量转文字。Use when: OCR this image, extract text from images, 图片转文字, OCR识别, 提取图片文字 | Dual-engine OCR (easyocr+tesseract) with 15 benchmarked preprocessing chains, 87% phone-photo digit accuracy"
homepage: https://github.com/jnbno1163/liaogong-ocr
license: MIT
metadata: {"clawdbot":{"emoji":"🔍","os":["win32","darwin","linux"],"requires":{"bins":["python"],"env":[]}}}
---

# LiaoGong-OCR · 廖工双引擎OCR

廖工AI设计实战出品 — easyocr + tesseract 双引擎OCR系统，15条可组合预处理链含实测基准数据。

## 三种用法

| 用法 | 命令/代码 | 场景 |
|------|-----------|------|
| **CLI工具** | `liaogong-ocr image.jpg` | 命令行一键提取文字 |
| **Python库** | `from liaogong_ocr import OCREngine` | 集成到你的Python项目 |
| **AI Agent** | `npx clawhub@latest install liaogong-ocr` | AI智能体自动触发OCR |

## 快速开始

```bash
# 安装系统依赖 tesseract（Windows用 winget install tesseract-ocr）
pip install -r requirements.txt
liaogong-ocr your_image.jpg
```

## 引擎模式

| 模式 | 命令 | 最适合 |
|------|------|--------|
| **自动** | `liaogong-ocr img.jpg` | 通用场景，自动选择引擎 |
| **easyocr** | `liaogong-ocr -e easyocr img.png` | 中文海报、截图、复杂排版 |
| **tesseract** | `liaogong-ocr -e tesseract doc.png` | 英文文档、白底黑字 |
| **手机拍照** | `liaogong-ocr -p phone photo.jpg` | 手机拍屏幕（87%数字准确率） |

## 预处理链（手机拍屏幕数字提取实测）

| 预处理链 | 数字准确率 | 速度 |
|----------|-----------|------|
| **optimal_phone** | **87%** | 快 |
| grayscale_binary | 72% | 快 |
| contrast_enhance | 65% | 快 |
| sharpen | 55% | 快 |
| clahe | 31% | 中 |
| adaptive_binary | 18% | 慢 |

## 系统要求

- Python 3.8+
- Tesseract（系统安装）
- 首次运行 easyocr 需下载 ~100MB 模型

---

**廖工AI设计实战出品 · github.com/jnbno1163**
