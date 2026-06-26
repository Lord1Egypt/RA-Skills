# PDFMathTranslate

科学 PDF 文档翻译，保留公式和排版格式。

## 概述

EMNLP 2025 Demo 项目，可将科技论文 PDF 翻译为多种语言，同时完整保留公式、图表、目录和注释的原始格式。支持命令行工具、交互式 UI 和 Docker 部署。

## 核心特性

- 📊 保留公式、图表、目录和注释
- 🌐 支持多种语言和翻译服务
- 🤖 提供命令行工具、交互界面和 Docker

## 使用方式

### 在线演示（无需安装）
- https://pdf2zh.com/
- https://app.immersivetranslate.com/babel-doc/
- https://huggingface.co/spaces/reycn/PDFMathTranslate-Docker

### Docker 部署
```bash
# 使用 Docker 运行
docker run -p 8501:8501 pdfmathtranslate
```

### Python 安装
```bash
# 使用 uv 安装
uv pip install pdfmathtranslate

# 或使用 pip
pip install pdfmathtranslate
```

## 支持的翻译服务

OpenAI、DeepL、智谱 GLM、MiniMax、DeepSeek、Ollama 等

## 相关资源

- GitHub: https://github.com/PDFMathTranslate/PDFMathTranslate
- 在线演示: https://pdf2zh.com/
