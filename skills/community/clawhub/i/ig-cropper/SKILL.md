---
name: ig-cropper
description: Transforms cluttered Instagram mobile screenshots into clean, distraction-free architectural and design references. Use when you need to automate the extraction of pure imagery from Instagram so that building a visual inspiration archive remains effortless, focused, and aesthetically consistent.
---

# IG Cropper

This skill provides a surgical tool to extract pure photographs from Instagram mobile screenshots (dark mode). 

## How it Works

**Adaptive Extraction**: Instagram's dark mode uses a very specific background color: **RGB (12, 15, 20)**. The tool scans the screenshot row by row, identifying the interface elements by this color signature and isolating the largest continuous block of non-background imagery—the photograph itself. It extracts this frame flawlessly, regardless of how much the user has scrolled.

## Usage

Run the Python script directly on any Instagram screenshot:

```bash
python3 scripts/ig_crop.py input_screenshot.png output_pure_photo.png
```

### Philosophy

This tool intentionally does *not* attempt to algorithmically paint over watermarks or icons located *inside* the photograph (like pagination numbers or tagged-people indicators). We leave the integrity of the architectural textures untouched, delegating complex restorations to professional generative tools or manual human craftsmanship.

## Dependencies

- Python 3
- Pillow (`pip install pillow`)
