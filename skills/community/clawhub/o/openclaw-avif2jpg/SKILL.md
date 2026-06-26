---
name: openclaw-avif2jpg
description: Convert `.avif` images to `.jpg` using a CLI workflow for one or more input paths. Use when the user asks to convert AVIF files, batch-convert a folder of AVIF images, or convert mixed file/folder path inputs while writing outputs next to the source location.
---

# OpenClaw AVIF to JPG

## Overview

Run the bundled Python script to convert AVIF images into JPEG.
Accept one folder path or multiple file/folder paths and place output beside source paths.

## Quick Start

1. Ensure dependencies exist:
```bash
python3 -m pip install Pillow pillow-avif-plugin
```
2. Convert one folder:
```bash
python3 scripts/avif2jpg.py /path/to/folder
```
3. Convert multiple files:
```bash
python3 scripts/avif2jpg.py /path/a.avif /path/b.avif
```
4. Recursively convert folder:
```bash
python3 scripts/avif2jpg.py /path/to/folder --recursive
```

## Output Rules

- If input is a folder `/data/photos`, output goes to sibling folder `/data/photos_jpg`.
- If input is a file `/data/a.avif`, output goes to `/data/a.jpg`.
- Skip non-`.avif` files and print warnings.

## Command Options

- `--quality <1-100>`: Set JPEG quality (default `92`).
- `--overwrite`: Overwrite existing output file.
- `--recursive`: Recursively scan folders.

## Execution Checklist

1. Resolve and validate each input path first.
2. Install dependencies if `Pillow` or AVIF plugin is missing.
3. Run `scripts/avif2jpg.py` with user options.
4. Report converted files, skipped files, and failures.
