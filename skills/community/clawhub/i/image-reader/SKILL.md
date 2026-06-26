---
name: image-reader
description: >
  Image recognition and understanding tool. Uses a multimodal model (e.g. doubao-seed-2.0-pro, kimi-k2.5) to analyze image content and supports OCR text extraction and image description.
  Use this skill when a user sends a screenshot or image and needs the text extracted or the image content understood.
compatibility:
  requires:
    - Python 3
    - openai>=1.0.0
    - pyyaml>=6.0
---

# Image Reader Skill

Image recognition and understanding tool that leverages Doubao multimodal models to analyze image content.

---

## Features

- **Text Extraction (OCR)**: Extract text from images, suitable for documents, screenshots, posters, menus, etc.
- **Image Description**: Generate detailed descriptions of images, suitable for photos, illustrations, memes, UI screens, etc.
- **General Analysis**: Automatically choose the best analysis strategy based on the image type.

---

## API Configuration

| Item | Value |
|------|------|
| API Endpoint | `https://ark.cn-beijing.volces.com/api/coding/v3` |
| Model | `doubao-seed-2.0-pro` |
| Authentication | API Key (configured in config.yaml) |

---

## Usage

### Command Line

```bash
# General analysis
python image_reader.py /path/to/image.png

# Extract text (OCR)
python image_reader.py /path/to/image.png -p "Extract all text from the image"

# Describe the image
python image_reader.py /path/to/image.png -p "Describe this image in detail"
```

### OpenClaw Skill Invocation

Once installed, you can invoke it using natural language:

```yaml
Analyze this image
Extract the text from the image
Describe this screenshot
```

---

## Output

- **Text-heavy images**: Returns all extracted text, preserving original formatting.
- **Non-text images**: Returns a detailed scene description, including objects, people, colors, style, etc.
- **Mixed content**: Provides both text extraction and a visual description.

---

## Technical Details

- Uses an OpenAI-compatible API to call Doubao multimodal models
- Images are sent as base64-encoded data
- The system prompt adapts to the image type to select the most appropriate analysis strategy