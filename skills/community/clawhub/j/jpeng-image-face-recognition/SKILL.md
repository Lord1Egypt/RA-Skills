---
name: jpeng-image-face-recognition
description: "Recognize and identify faces"
version: "1.0.0"
author: "jpeng"
tags: ["ai", "recognition", "image"]
---

# Image Face Recognition

Recognize and identify faces

## When to Use

- User needs ai related functionality
- Automating recognition tasks
- Image operations

## Usage

```bash
python3 scripts/image_face_recognition.py --input <input> --output <output>
```

## Configuration

Set required environment variables:

```bash
export RECOGNITION_API_KEY="your-api-key"
```

## Output

Returns JSON with results:

```json
{
  "success": true,
  "data": {}
}
```
