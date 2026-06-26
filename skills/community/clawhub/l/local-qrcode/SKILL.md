---
name: local-qrcode
description: Generate QR codes locally from text/URL to PNG image or ASCII art. Pure local generation using qrcode library. No API key required. Use when users need to create QR codes for links, text, or any content.
---

# local-qrcode

## Overview

A simple skill for generating QR codes locally. Convert any text or URL to a QR code image (PNG) or display as ASCII art in terminal. Everything runs locally, no external API calls needed.

## Features

- **Generate PNG QR code**: Save QR code as PNG image file
- **ASCII QR output**: Display QR code directly in terminal as ASCII art
- **Customizable**: Adjust box size and border size for output

## Dependencies

Requires `qrcode` and `Pillow` Python packages:
```bash
pip install qrcode pillow
```

## Usage

### Generate PNG QR code
```bash
python3 scripts/generate_png.py "https://example.com" output.png
```

### Generate ASCII QR code
```bash
python3 scripts/generate_ascii.py "Hello World"
```

### Custom size
```bash
python3 scripts/generate_png.py --box-size 10 --border 4 "content" output.png
```

## Resources

### scripts/
- `generate_png.py` - Generate QR code as PNG image file
- `generate_ascii.py` - Generate QR code as ASCII art for terminal output

