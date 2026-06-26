---
name: translate-ppt
version: 1.0.0
description: "Translate Chinese PowerPoint presentations to English while preserving all images, charts, shapes, and media content. Adjusts fonts to Calibri and optimizes layout for professional business presentations. Use when the user asks to translate a PPT/PPTX file from Chinese to English, or mentions PPT translation, slide translation, or presentation localization."
requires:
  tools:
    - python3
triggers:
  - translate PPT
  - translate PPTX
  - translate PowerPoint
  - translate slides
  - Chinese to English PPT
  - presentation translation
  - slide translation
  - PPT localization
---

# Translate PPT

Translate Chinese PowerPoint presentations (.pptx) to English with professional business styling.

## Overview

This skill translates Chinese PPTX files to English using any OpenAI-compatible LLM endpoint (local or cloud). It preserves all non-text content while:
- Preserving all non-text content (images, charts, shapes, tables, SmartArt, media)
- Adjusting fonts to Calibri family for consistent business styling
- Optimizing text box sizing and layout for English text (typically longer than Chinese)
- Maintaining original slide masters, layouts, animations, and transitions

## Prerequisites

- Python 3.8+
- Required packages: `python-pptx`, `requests`
- An LLM endpoint that supports OpenAI-compatible API (e.g., Qoderwork built-in models, Ollama, OpenAI, DeepSeek, etc.)

## Quick Start

### Option A: Use with Qoderwork (Easiest — No Extra Setup)

If you're running this skill within Qoderwork, models are already available. Just run:

```bash
pip install python-pptx requests
python .qoder/skills/translate-ppt/scripts/translate_ppt.py input.pptx --api-base <qoderwork-endpoint> --model <available-model>
```

### Option B: Use with Local Ollama

1. **Install Ollama:**
   Download and install from https://ollama.com

2. **Pull a recommended model:**
   ```bash
   ollama pull qwen2.5:14b
   ```

3. **Install Python dependencies:**
   ```bash
   pip install python-pptx requests
   ```

4. **Run translation:**
   ```bash
   python .qoder/skills/translate-ppt/scripts/translate_ppt.py input.pptx
   ```

   If output path is not specified, defaults to `<input_name>_en.pptx`.

### Option C: Use with Cloud API

Run with your cloud endpoint:

```bash
python .qoder/skills/translate-ppt/scripts/translate_ppt.py input.pptx --api-base https://api.openai.com/v1 --api-key sk-xxx --model gpt-4o
```

## Translation Rules

- **Translate:** All text content (titles, body text, notes, table cells, grouped shape text)
- **Preserve:** Images, charts data, embedded media, hyperlinks, original formatting
- **Mixed content:** Only translate Chinese portions of mixed Chinese/English text

## Font & Layout Adjustments

| Element | Font | Style |
|---------|------|-------|
| Titles | Calibri | Bold |
| Body text | Calibri | Regular |

- Maintain original font sizes (with auto-shrink if text overflows)
- Adjust text box width up to 20% if English text is significantly longer
- Preserve original color scheme and text formatting (bold, italic, underline)

## Business Style Guidelines

- Consistent Calibri font family throughout
- Clean, professional spacing
- Preserved slide master/layout templates
- All animations and transitions intact

## Recommended Models

Translation quality varies significantly between models. Choose based on your setup:

> **Note for Qoderwork users:** You can use whatever models are already configured in your client environment — no additional setup required.

| Model | Size | Quality | Speed | Command |
|-------|------|---------|-------|---------|
| `qwen2.5:14b` | ~9GB | ★★★★★ Best for Chinese | Fast | `ollama pull qwen2.5:14b` |
| `qwen2.5:7b` | ~4.7GB | ★★★★ Good balance | Faster | `ollama pull qwen2.5:7b` |
| `llama3.1:8b` | ~4.7GB | ★★★ Decent | Fast | `ollama pull llama3.1:8b` |
| `gemma2:9b` | ~5.4GB | ★★★ Decent | Fast | `ollama pull gemma2:9b` |
| `qwen2.5:3b` | ~2GB | ★★ Basic | Fastest | `ollama pull qwen2.5:3b` |

> **Tip:** For best results with Chinese-to-English business content, **Qwen2.5 14B is strongly recommended** as it has excellent Chinese language understanding. Smaller models may produce less accurate or less natural translations.

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--font` | Override default font | Calibri |
| `--model` | LLM model to use | qwen2.5:14b |
| `--api-base` | OpenAI-compatible API base URL | http://localhost:11434/v1 |
| `--api-key` | API key (optional, not needed for local models) | None |
| `--batch-size` | Text segments per API call | 20 |
| `--verbose`, `-v` | Enable detailed logging | False |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection refused | Check your API endpoint URL. For Ollama: ensure `ollama serve` is running. For cloud APIs: verify the URL is correct. |
| Model not found | Verify the model name is correct for your endpoint. For Ollama: `ollama pull <model>` |
| Corrupt PPTX | Verify file opens in PowerPoint; try saving as new file first |
| Font not found | Ensure Calibri is installed on your system |
| API rate limits | Reduce `--batch-size` or add delay between calls |

## Reference

See [reference.md](reference.md) for detailed API documentation and architecture.
