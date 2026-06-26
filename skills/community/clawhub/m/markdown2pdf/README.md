# 📄 Markdown2PDF

**A professional OpenClaw skill that converts Markdown documents to beautiful PDF files and PNG images with colored emoji support.**

[![Version 1.0.0](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/leohuang8688/markdown2pdf)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**[English](#-markdown2pdf)** | **[中文](#-markdown2pdf-中文版)**

---

## ✨ Features

- 📄 **Markdown to PDF** - Professional PDF document generation
- 🖼️ **Markdown to PNG** - High-quality PNG image generation
- 🎨 **5 Professional Themes** - default, dark, github, minimal, professional
- 🌈 **Colored Emoji Support** - Automatic emoji to colored text label conversion
- ✨ **Custom CSS** - Complete style control
- 🚀 **CLI & API** - Multiple usage methods
- 🧩 **OpenClaw Integration** - Seamless integration

---

## 🚀 Quick Start

### Installation

```bash
cd ~/.openclaw/workspace/skills/markdown2pdf

# Install Python dependencies
pip3 install markdown pdfkit imgkit

# Install wkhtmltopdf (required)
# macOS
brew install wkhtmltopdf

# Ubuntu/Debian
sudo apt-get install wkhtmltopdf

# CentOS/RHEL
sudo yum install wkhtmltopdf
```

### Basic Usage

```bash
# Convert to PDF and PNG
python3 src/converter.py input.md

# Convert to PDF only
python3 src/converter.py input.md -f pdf

# Use theme
python3 src/converter.py input.md -t github -f pdf

# List themes
python3 src/converter.py --list-themes
```

---

## 🎨 Theme System

### Available Themes

| Theme | Description | Use Case |
|-------|-------------|----------|
| `default` | Modern clean design | General documents |
| `dark` | Dark theme | Presentations, night reading |
| `github` | GitHub-style | Technical docs, README |
| `minimal` | Minimalist design | Elegant documents |
| `professional` | Business style | Reports, business docs |

### Using Themes

```bash
# Use github theme
python3 src/converter.py README.md -t github -f pdf -o readme

# Use professional theme
python3 src/converter.py report.md -t professional -f pdf
```

---

## 🌈 Colored Emoji Support

### Automatic Conversion

markdown2pdf automatically converts emoji to colored text labels for PDF compatibility:

| Emoji | Converted | Color |
|-------|-----------|-------|
| 📊 | [数据] | 🔵 Blue |
| 📈 | [趋势↑] | 🟢 Green |
| 📉 | [趋势↓] | 🔴 Red |
| ✅ | [√] | 🟢 Green |
| ❌ | [×] | 🔴 Red |
| ⚠️ | [!] | 🟠 Orange |
| 🚀 | [启动] | 🔴 Red |
| ⭐ | ★ | 🟡 Gold |

### Color Semantics

- 🟢 **Green** - Positive, growth, success
- 🔴 **Red** - Negative, decline, warning
- 🔵 **Blue** - Neutral, information, data
- 🟡 **Gold** - Important, highlights, money
- 🟠 **Orange** - Attention, caution

---

## 📖 API Usage

### Python API

```python
from src.converter import (
    MarkdownConverter,
    convert_markdown,
    convert_markdown_to_pdf,
    convert_markdown_to_png
)

# Method 1: Simple conversion
pdf_path = convert_markdown_to_pdf(
    markdown_text="# Hello World",
    output_filename="hello.pdf",
    theme="github"
)

# Method 2: Multi-format conversion
results = convert_markdown(
    markdown_text="# Document",
    output_filename="doc",
    formats=["pdf", "png"],
    theme="professional"
)

# Method 3: Advanced usage
converter = MarkdownConverter(
    output_dir=Path("./output"),
    theme="dark",
    custom_css=".custom { color: red; }"
)

# Convert to PDF
pdf_path = converter.convert_to_pdf(
    markdown_text="# My Document",
    output_filename="document.pdf",
    page_size="A4",
    margin="15mm"
)

# Convert to PNG
png_path = converter.convert_to_png(
    markdown_text="# My Document",
    output_filename="document.png",
    width=1920,
    quality=100
)
```

---

## 🔧 CLI Options

```
usage: converter.py [-h] [-o OUTPUT] [-f FORMATS] [-t THEME] [-d OUTPUT_DIR]
                   [--width WIDTH] [--page-size PAGE_SIZE] [--margin MARGIN]
                   [--list-themes]
                   input

Convert Markdown to PDF/PNG

positional arguments:
  input                 Input markdown file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output filename (without extension)
  -f FORMATS, --formats FORMATS
                        Output formats (comma-separated: pdf,png)
  -t THEME, --theme THEME
                        Theme (default, dark, github, minimal, professional)
  -d OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Output directory
  --width WIDTH         PNG width in pixels (default: 1200)
  --page-size PAGE_SIZE
                        PDF page size (default: A4)
  --margin MARGIN       PDF margin (default: 20mm)
  --list-themes         List available themes
```

---

## 📁 Project Structure

```
markdown2pdf/
├── src/
│   ├── converter.py          # Main converter
│   └── emoji_replacer.py     # Emoji conversion utility
├── output/                    # Output files
├── tests/
│   └── test_converter.py     # Test suite
├── pyproject.toml            # Python project config
├── requirements.txt          # Python dependencies
├── README.md                 # This document
└── SKILL.md                  # OpenClaw skill definition
```

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Test conversion
python3 src/converter.py test_document.md -t github -f pdf
```

---

## 🎯 Use Cases

### 1. Investment Analysis Reports

```bash
python3 src/converter.py stock_analysis.md -t professional -f pdf
```

### 2. Technical Documentation

```bash
python3 src/converter.py README.md -t github -f pdf,png
```

### 3. Presentations

```bash
python3 src/converter.py presentation.md -t dark -f png --width 1920
```

### 4. Business Reports

```bash
python3 src/converter.py business_report.md -t professional -f pdf
```

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### v1.0.0 (2026-03-16)
- ✨ Initial stable release
- 📄 Markdown to PDF/PNG converter
- 🎨 5 professional themes
- 🌈 Colored emoji support
- 🔧 CLI and API interfaces

---

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**PocketAI for Leo** - OpenClaw Community

GitHub: [@leohuang8688](https://github.com/leohuang8688/markdown2pdf)

---

## 🙏 Acknowledgments

- [OpenClaw Team](https://github.com/openclaw/openclaw) - Amazing framework
- [markdown](https://pypi.org/project/markdown/) - Markdown processing
- [pdfkit](https://pypi.org/project/pdfkit/) - PDF generation
- [imgkit](https://pypi.org/project/imgkit/) - Image generation
- [wkhtmltopdf](https://wkhtmltopdf.org/) - HTML to PDF engine

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/leohuang8688/markdown2pdf/issues)
- **Discussions:** [GitHub Discussions](https://github.com/leohuang8688/markdown2pdf/discussions)

---

**Happy Converting! 📄🎨**

---

---

# 📄 Markdown2PDF 中文版

**一个专业的 OpenClaw 技能，将 Markdown 文档转换为美观的 PDF 文件和 PNG 图片，支持彩色 emoji。**

---

## ✨ 核心功能

- 📄 **Markdown 转 PDF** - 专业 PDF 文档生成
- 🖼️ **Markdown 转 PNG** - 高质量 PNG 图片
- 🎨 **5 种专业主题** - default, dark, github, minimal, professional
- 🌈 **彩色 Emoji 支持** - 自动转换为彩色文字标签
- ✨ **自定义 CSS** - 完全控制样式
- 🚀 **CLI 和 API** - 多种使用方式

---

## 🚀 快速开始

### 安装依赖

```bash
cd ~/.openclaw/workspace/skills/markdown2pdf

# 安装 Python 依赖
pip3 install markdown pdfkit imgkit

# 安装 wkhtmltopdf（必需）
# macOS
brew install wkhtmltopdf

# Ubuntu/Debian
sudo apt-get install wkhtmltopdf
```

### 基本使用

```bash
# 转换为 PDF 和 PNG
python3 src/converter.py input.md

# 只生成 PDF
python3 src/converter.py input.md -f pdf

# 使用主题
python3 src/converter.py input.md -t github -f pdf
```

---

## 🎨 主题系统

### 可用主题

| 主题 | 描述 | 适用场景 |
|------|------|----------|
| `default` | 现代简洁设计 | 通用文档 |
| `dark` | 深色主题 | 演示、夜间阅读 |
| `github` | GitHub 风格 | 技术文档、README |
| `minimal` | 极简设计 | 优雅文档、出版物 |
| `professional` | 商务风格 | 报告、商业文档 |

---

## 🌈 彩色 Emoji 支持

### 自动转换

markdown2pdf 会自动将 emoji 转换为彩色文字标签：

| Emoji | 转换后 | 颜色 |
|-------|--------|------|
| 📊 | [数据] | 🔵 蓝色 |
| 📈 | [趋势↑] | 🟢 绿色 |
| 📉 | [趋势↓] | 🔴 红色 |
| ✅ | [√] | 🟢 绿色 |
| ❌ | [×] | 🔴 红色 |
| ⚠️ | [!] | 🟠 橙色 |

### 颜色语义

- 🟢 **绿色** - 积极、上涨、成功
- 🔴 **红色** - 消极、下跌、警告
- 🔵 **蓝色** - 中性、信息、数据
- 🟡 **金色** - 重要、亮点、金钱
- 🟠 **橙色** - 注意、警告

---

## 📖 Python API

```python
from src.converter import convert_markdown_to_pdf

# 简单转换
pdf_path = convert_markdown_to_pdf(
    markdown_text="# Hello World",
    output_filename="hello.pdf",
    theme="github"
)
```

---

## 🎯 使用案例

### 1. 投资分析报告
```bash
python3 src/converter.py stock_analysis.md -t professional -f pdf
```

### 2. 技术文档
```bash
python3 src/converter.py README.md -t github -f pdf,png
```

### 3. 演示文稿
```bash
python3 src/converter.py presentation.md -t dark -f png --width 1920
```

---

## 📝 更新日志

### v1.0.0 (2026-03-16)
- ✨ 首次正式发布
- 📄 Markdown 转 PDF/PNG 转换器
- 🎨 5 种专业主题
- 🌈 彩色 emoji 支持
- 🔧 CLI 和 API 接口

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👨‍💻 作者

**PocketAI for Leo** - OpenClaw Community

GitHub: [@leohuang8688](https://github.com/leohuang8688/markdown2pdf)

---

## 📞 支持

- **问题反馈:** [GitHub Issues](https://github.com/leohuang8688/markdown2pdf/issues)
- **讨论:** [GitHub Discussions](https://github.com/leohuang8688/markdown2pdf/discussions)

---

**Happy Converting! 📄🎨**
