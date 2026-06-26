---
name: mistral-ocr
description: "Convert PDF/images to Markdown/JSON/HTML using Mistral OCR API. Supports image extraction, table recognition, header/footer handling, and multi-column layouts. Usage: Upload a file and say Use Mistral OCR to process this."
registry:
  homepage: https://github.com/YZDame/Mistral-OCR-SKILL
  author: YZDame
  credentials:
    required: true
    env_vars:
      - MISTRAL_API_KEY
---

# ⚠️ Privacy Warning - 隐私警告

**IMPORTANT - READ BEFORE INSTALLING:**

This skill **uploads your files to Mistral's cloud servers** for OCR processing.

**Do NOT use with sensitive or confidential documents** unless:
- You trust Mistral's data handling policies
- You have reviewed Mistral's privacy policy
- You accept that file contents will be transmitted and processed remotely

**For sensitive documents, use offline/local OCR tools instead.**

---

# Mistral OCR Skill

A powerful OCR tool that converts PDF files and images into Markdown, JSON, or HTML formats using Mistral's state-of-the-art OCR API.

## Installation

```bash
# Clone or download this repository
git clone https://github.com/YZDame/Mistral-OCR-SKILL.git
cd Mistral-OCR-SKILL

# Install dependencies
pip install -r requirements.txt
```

## 🔑 API Key Setup (Required)

**Get your API key:**
👉 https://console.mistral.ai/home

**Set the environment variable:**

```bash
export MISTRAL_API_KEY=your_api_key
```

## CLI Usage

```bash
cd scripts

# Process PDF to Markdown
python3 mistral_ocr.py -i input.pdf

# Process PDF to JSON
python3 mistral_ocr.py -i input.pdf -f json

# Specify output directory
python3 mistral_ocr.py -i input.pdf -o ~/my_ocr_results
```

## Arguments

| Flag | Description |
|------|-------------|
| `-i, --input` | Input file path (required) |
| `-f, --format` | Output format: markdown/json/html (default: markdown) |
| `-o, --output` | Output directory |

## Data Privacy

**What happens to your files:**
1. Files are uploaded to Mistral's OCR API
2. Files are processed on Mistral servers
3. Processing results are returned to you
4. Files are not stored on Mistral servers (per Mistral policy)

**For more details, see:** https://mistral.ai/privacy-policy

## License

MIT
