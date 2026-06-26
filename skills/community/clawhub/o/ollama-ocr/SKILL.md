---
name: ollama-ocr
description: Use Ollama's vision/OCR models to recognize text from images. Supports glm-ocr, llava, moondream, and llama3.2-vision models. Ideal when you need local offline OCR without relying on cloud APIs.
metadata:
  {
    "author": "hongjiahao371-pixel",
    "version": "1.0.0",
    "openclaw": {
      "description": "Local Ollama OCR for image text recognition",
      "examples": [
        "recognize text from image",
        "extract text from screenshot",
        "OCR this picture"
      ]
    }
  }
---

# Ollama OCR Skill

Use this skill when you need to recognize text from images using Ollama's local vision/OCR models. No internet required - fully offline OCR.

## When to Use

- User sends an image and wants text extraction
- User asks to recognize text from a screenshot or picture
- Need local offline OCR without cloud API dependency
- Processing sensitive images that shouldn't be sent to third parties

## Models Available

| Model | Best For | Size |
|-------|----------|------|
| `glm-ocr:latest` | Chinese text OCR | ~2.2GB |
| `llava:7b` | General image understanding | ~4.7GB |
| `moondream` | Lightweight vision model | ~1.5GB |
| `llama3.2-vision:latest` | Large vision model | ~7GB+ |

## Ollama Endpoint

Default: `http://172.17.0.2:11434` (Docker container to host gateway)

**Note:** Endpoint is pre-configured for OpenClaw running in Docker accessing host Ollama. Adjust `OLLAMA_HOST` in `ollama_ocr.py` if your setup differs.

## Usage

### Command Line

```bash
python3 ollama_ocr.py /path/to/image.jpg [model_name]
```

Examples:
```bash
python3 ollama_ocr.py receipt.png glm-ocr:latest
python3 ollama_ocr.py screenshot.jpg llava:7b
```

### Python API

```python
from ollama_ocr import ollama_ocr

# Basic OCR with default model (glm-ocr)
result = ollama_ocr('/path/to/image.jpg')

# Specify model
result = ollama_ocr('/path/to/image.jpg', 'glm-ocr:latest')

print(result)
```

## Example Prompts to Activate This Skill

- "识别这张图片里的文字"
- "帮我 OCR 一下这个截图"
- "Extract text from this image"
- "What text is in this screenshot?"

## Notes

- Image path must be absolute or relative to script location
- For large images, consider resizing first to avoid timeout
- `glm-ocr` works best for Chinese text
- Some models may have output quirks (e.g., glm-ocr occasionally repeats)
- First call may be slow if model isn't cached in memory

## Requirements

- Ollama installed and running
- At least one vision/OCR model downloaded (e.g., `ollama pull glm-ocr:latest`)
