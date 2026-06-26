# 📄 Markdown2PDF Skill

**A professional OpenClaw skill for converting Markdown documents to PDF and PNG with colored emoji support.**

---

## 📋 Overview

| Property | Value |
|----------|-------|
| **Name** | markdown2pdf |
| **Version** | 1.0.0 |
| **Author** | PocketAI for Leo |
| **License** | MIT |
| **Category** | Document Conversion |
| **Repository** | [GitHub](https://github.com/leohuang8688/markdown2pdf) |

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
pip3 install markdown pdfkit imgkit
brew install wkhtmltopdf  # macOS
# or
sudo apt-get install wkhtmltopdf  # Ubuntu
```

### Basic Usage

```bash
# Convert to PDF
python3 src/converter.py input.md -f pdf

# Use theme
python3 src/converter.py README.md -t github -f pdf

# List themes
python3 src/converter.py --list-themes
```

---

## 🎨 Available Themes

| Theme | Description | Best For |
|-------|-------------|----------|
| `default` | Modern clean design | General documents |
| `dark` | Dark theme | Presentations, night reading |
| `github` | GitHub-style | Technical docs, README |
| `minimal` | Minimalist design | Elegant documents |
| `professional` | Business style | Reports, business docs |

---

## 🌈 Colored Emoji Support

Automatically converts emoji to colored text labels for PDF compatibility:

| Emoji | Converted | Color | Meaning |
|-------|-----------|-------|---------|
| 📊 | [数据] | 🔵 Blue | Data |
| 📈 | [趋势↑] | 🟢 Green | Growth |
| 📉 | [趋势↓] | 🔴 Red | Decline |
| ✅ | [√] | 🟢 Green | Success |
| ❌ | [×] | 🔴 Red | Error |
| ⚠️ | [!] | 🟠 Orange | Warning |
| 🚀 | [启动] | 🔴 Red | Launch |
| ⭐ | ★ | 🟡 Gold | Star |

---

## 📖 API Usage

### Python API

```python
from src.converter import convert_markdown_to_pdf, MarkdownConverter

# Simple conversion
pdf_path = convert_markdown_to_pdf(
    markdown_text="# Hello World",
    output_filename="hello.pdf",
    theme="github"
)

# Advanced usage
converter = MarkdownConverter(
    output_dir=Path("./output"),
    theme="professional",
    custom_css=".custom { color: red; }"
)

pdf_path = converter.convert_to_pdf(
    markdown_text="# Document",
    output_filename="doc.pdf",
    page_size="A4",
    margin="15mm"
)
```

---

## ⚙️ Configuration

### Default Settings

| Setting | Value | Description |
|---------|-------|-------------|
| `default_theme` | professional | Default theme for conversion |
| `default_formats` | ["pdf"] | Default output formats |
| `default_width` | 1200 | Default PNG width in pixels |
| `default_page_size` | A4 | Default PDF page size |
| `default_margin` | 20mm | Default PDF margin |
| `emoji_support` | true | Enable emoji replacement |
| `colored_emoji` | true | Use colored text labels |

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `markdown` | >=3.5.0 | Markdown processing |
| `pdfkit` | >=1.0.0 | PDF generation |
| `imgkit` | >=1.2.3 | Image generation |
| `wkhtmltopdf` | >=0.2.0 | HTML to PDF engine |

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
├── README.md                  # Documentation
├── SKILL.md                   # This file
└── requirements.txt           # Dependencies
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

## 📝 Changelog

### v1.0.0 (2026-03-16)

**Initial Stable Release**

- ✨ Markdown to PDF/PNG converter
- 🎨 5 professional themes
- 🌈 Colored emoji support
- 🔧 CLI and API interfaces
- 📚 Complete documentation
- 🧩 OpenClaw integration

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

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/leohuang8688/markdown2pdf/issues)
- **Discussions:** [GitHub Discussions](https://github.com/leohuang8688/markdown2pdf/discussions)
- **Repository:** [GitHub](https://github.com/leohuang8688/markdown2pdf)

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Happy Converting! 📄🎨**

---

*Last Updated: 2026-03-17*  
*Version: 1.0.0*  
*Author: PocketAI for Leo*
