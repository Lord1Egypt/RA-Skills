---
name: pdf2jpg
description: Convert PDF files to JPEG images with pdftoppm, support optional page ranges, and bundle generated JPGs into a zip archive for sharing. Use when a user wants to turn a PDF into page images, extract selected pages, or package the results. Requires poppler-utils / pdftoppm.
---

# pdf2jpg

## Overview

Convert a PDF into JPEG page images using `pdftoppm` from `poppler-utils`, then optionally zip the generated JPGs.

## Requirements

- `pdftoppm` must be available in `PATH`
- Install the `poppler-utils` package before running the scripts

### Install `poppler-utils`

- **Debian / Ubuntu**:
  ```bash
  sudo apt update
  sudo apt install -y poppler-utils
  ```

- **Windows**:
  - Install Poppler via a package manager, then make `pdftoppm.exe` available in your `PATH`
  - Common options:
    - `winget install -e --id oschwartz10612.Poppler`
    - `choco install poppler`
    - `scoop install poppler`

- **macOS**:
  ```bash
  brew install poppler
  ```

## Standard workflow

1. Convert the PDF with `scripts/pdf2jpg.sh`
2. Bundle the output images with `scripts/zip_jpgs.sh` if needed

```bash
./scripts/pdf2jpg.sh input.pdf
./scripts/pdf2jpg.sh input.pdf 2 5
./scripts/zip_jpgs.sh input.pdf
./scripts/zip_jpgs.sh input.pdf /tmp/output.zip
```

## Scripts

### `scripts/pdf2jpg.sh`
- Prompts for the PDF path if none is supplied
- Verifies the input file exists
- Verifies `pdftoppm` is installed and prints a `poppler-utils` install hint if not
- Writes JPEGs beside the PDF using the PDF basename as the output prefix
- Accepts optional `first` and `last` page arguments

### `scripts/zip_jpgs.sh`
- Finds matching `basename-*.jpg` files for the PDF
- Creates a zip archive containing those JPGs
- Uses `${base}-jpgs.zip` by default when no output path is supplied

## Notes

- Output files follow the `pdftoppm` naming convention, typically `basename-1.jpg`, `basename-2.jpg`, etc.
- If you need different image quality, output naming, or archive behavior, edit the bundled scripts rather than reimplementing the command inline.
