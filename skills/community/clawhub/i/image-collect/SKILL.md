---
name: image-collect
description: This skill extracts knowledge from an image and saves it locally.
---

# Image Collect Skill

This skill extracts knowledge from an image and saves it locally.

## When to use

Use this skill when:

- User sends an image
- User asks to save image as knowledge
- Image needs OCR or content understanding

## What it does

1. Download image
2. Extract text and meaning
3. Generate summary
4. Save image locally
5. Append knowledge to JSON database

## Command

Run:

node dist/index.js "<image_url>"

Example:

node dist/index.js "https://example.com/image.png"
node dist/index.js "data:image/png;base64,xxxx"
node dist/index.js "/tmp/image.png"

## Output

Returns extracted knowledge including:

- summary
- keywords
- text
- saved image path