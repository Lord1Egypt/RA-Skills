---
name: pdf-intelligence-suite
description: PDF智能处理套件 - 文本提取、表格识别、OCR、PDF转Word/Excel等 | PDF Intelligence Suite - Text extraction, table recognition, OCR, PDF to Word/Excel conversion
homepage: https://github.com/kaiyuelv/pdf-intelligence-suite
category: productivity
tags:
  - pdf
  - ocr
  - document
  - extraction
  - converter
  - automation
version: 1.0.0
---

# PDF Intelligence Suite - PDF智能处理套件

---

## 中文描述

### 概述

PDF智能处理套件是一个功能强大的PDF文档处理工具集，提供文本提取、表格识别、OCR文字识别、格式转换等一站式服务。

### 功能特性

- **📄 文本提取**: 从PDF中提取纯文本或结构化文本，支持多种布局分析
- **📊 表格识别**: 自动识别PDF中的表格并提取为结构化数据（CSV/Excel）
- **🔍 OCR识别**: 对扫描件和图片型PDF进行文字识别，支持多语言
- **🔄 格式转换**: PDF转Word、PDF转Excel、PDF转图片等
- **✂️ 页面操作**: 合并、拆分、旋转、删除页面
- **🔒 安全处理**: 加密、解密、添加水印、数字签名
- **📝 元数据管理**: 读取和修改PDF文档属性

### 技术栈

- **PyPDF2**: PDF基础操作（合并、拆分、加密等）
- **pdfplumber**: 高级文本和表格提取，精准定位
- **camelot-py**: 专业表格识别引擎
- **pytesseract**: OCR文字识别（需安装Tesseract）
- **pdf2image**: PDF转图片
- **reportlab**: PDF生成和编辑
- **Pillow**: 图像处理

### 目录结构

```
pdf-intelligence-suite/
├── SKILL.md              # 本文件
├── README.md             # 使用文档
├── requirements.txt      # 依赖声明
├── setup.py              # 安装配置
├── src/
│   └── pdf_intelligence_suite/
│       ├── __init__.py
│       ├── extractor.py      # 文本提取模块
│       ├── tables.py         # 表格识别模块
│       ├── ocr.py            # OCR识别模块
│       ├── converter.py      # 格式转换模块
│       ├── manipulator.py    # 页面操作模块
│       ├── security.py       # 安全处理模块
│       └── utils.py          # 工具函数
├── examples/
│   └── basic_usage.py    # 使用示例
└── tests/
    └── test_pdf_suite.py # 单元测试
```

### 快速开始

```python
from pdf_intelligence_suite import PDFExtractor, TableExtractor, OCRProcessor

# 文本提取
extractor = PDFExtractor()
text = extractor.extract_text("document.pdf")

# 表格提取
tables = TableExtractor.extract_tables("report.pdf", output_format="excel")

# OCR识别
ocr = OCRProcessor(lang='chi_sim+eng')
text = ocr.process("scanned.pdf")
```

### 安装

```bash
pip install -r requirements.txt

# 安装Tesseract OCR引擎（Ubuntu/Debian）
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-chi-tra

# macOS
brew install tesseract tesseract-lang

# Windows: 下载安装包 https://github.com/UB-Mannheim/tesseract/wiki
```

---

## English Description

### Overview

PDF Intelligence Suite is a powerful PDF document processing toolkit providing one-stop services for text extraction, table recognition, OCR, format conversion, and more.

### Features

- **📄 Text Extraction**: Extract plain or structured text from PDFs with layout analysis
- **📊 Table Recognition**: Automatically detect and extract tables as structured data (CSV/Excel)
- **🔍 OCR Recognition**: Recognize text in scanned documents and image-based PDFs, multi-language support
- **🔄 Format Conversion**: PDF to Word, PDF to Excel, PDF to images, etc.
- **✂️ Page Operations**: Merge, split, rotate, delete pages
- **🔒 Security**: Encryption, decryption, watermarking, digital signatures
- **📝 Metadata**: Read and modify PDF document properties

### Tech Stack

- **PyPDF2**: Basic PDF operations (merge, split, encrypt, etc.)
- **pdfplumber**: Advanced text and table extraction with precise positioning
- **camelot-py**: Professional table recognition engine
- **pytesseract**: OCR text recognition (requires Tesseract installation)
- **pdf2image**: PDF to image conversion
- **reportlab**: PDF generation and editing
- **Pillow**: Image processing

### Quick Start

```python
from pdf_intelligence_suite import PDFExtractor, TableExtractor, OCRProcessor

# Text extraction
extractor = PDFExtractor()
text = extractor.extract_text("document.pdf")

# Table extraction
tables = TableExtractor.extract_tables("report.pdf", output_format="excel")

# OCR recognition
ocr = OCRProcessor(lang='eng')
text = ocr.process("scanned.pdf")
```

### Installation

```bash
pip install -r requirements.txt

# Install Tesseract OCR engine (Ubuntu/Debian)
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

### License

MIT License

### Author

ClawHub Skills Collection
