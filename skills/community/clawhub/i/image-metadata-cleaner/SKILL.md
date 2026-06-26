---
name: image-metadata-cleaner
slug: image-metadata-cleaner
version: "1.0.1"
description: "Clean privacy-sensitive metadata (C2PA, EXIF, XMP, IPTC, GPS) from user-owned images by writing sanitized copies. For privacy hygiene and file preparation."
os: ["windows", "macos", "linux"]
---

# Image Metadata Cleaner

Clean privacy-sensitive metadata from user-owned images by writing sanitized copies. Designed for legitimate privacy hygiene, file preparation, and reproducible publishing workflows.

**Use only for**: images you own or are authorized to process, for privacy protection, file-size optimization, and clean publishing.

## What it does

- Re-encodes image pixels into a fresh output file — all metadata discarded
- Writes copies instead of modifying originals in place
- Defaults folder output to `metadata-cleaned/` subdirectory
- Refuses output paths that resolve to the same file as the input
- Reopens outputs and scans for residual metadata keys and provenance markers
- Produces a human-readable summary and optional JSON manifest

## Usage

### Single file

```
User: clean metadata from this image: photo.png
User: remove EXIF data from IMG_2024.jpg
```

### Folder batch

```
User: clean metadata from all images in "C:\Users\me\Downloads"
User: remove privacy data from /path/to/folder
```

## Steps

1. **Confirm the task is for privacy hygiene** on images the user owns or is authorized to process.

2. **Preview with dry-run** (optional):
   ```bash
   uv run --with "pillow>=10.0" scripts/strip.py "<path>" --dry-run
   ```

3. **Run the cleanup**:
   ```bash
   uv run --with "pillow>=10.0" scripts/strip.py "<path>" --manifest
   ```

   Options:
   - `-o <path>` — Output file path (single file only)
   - `--output-dir <dir>` — Output directory (batch mode)
   - `-f preserve|jpg|png` — Output format (default: `preserve` — JPEG stays JPEG, others become PNG)
   - `-q <1-100>` — JPEG quality (default: 95)
   - `--recursive` — Process subdirectories
   - `--overwrite` — Overwrite existing output (only after user confirmation)
   - `--dry-run` — Preview without writing files
   - `--manifest [path]` — Write JSON manifest

   If `uv` is not available:
   ```bash
   pip install "pillow>=10.0" && python scripts/strip.py "<path>" --manifest
   ```

4. **Report results**:
   - Files processed, failed, or dry-run previewed
   - Output filenames and location
   - File size before → after
   - Dimensions preserved
   - Verification scan results (any residual metadata keys or provenance markers)

   Note: this removes file-level metadata only. Pixel-level watermarks and external platform records are outside the scope.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| "No supported image files found" | Folder has no matching extensions | Check input path and file types |
| "Output already exists" | Explicit output path exists | Use `--overwrite` after user confirmation |
| "Refusing to overwrite input file" | Output path = input path | Choose a different output path |
| "Unsupported image extension" | File extension not in supported list | Use PNG, JPEG, WebP, BMP, or TIFF |
| "cannot identify image file" | Corrupted or non-image file | Skip and continue with other files |
| Pillow ImportError | Missing dependency | Run `pip install "pillow>=10.0"` |

## What gets removed

| Metadata Type | Notes |
|---|---|
| EXIF | Camera, GPS, device tags. Orientation applied before saving. |
| XMP | Adobe and application metadata |
| IPTC/Photoshop | Press and photo metadata |
| ICC Profile | Color profile (not copied to output) |
| C2PA/JUMBF | Provenance containers removed by re-encoding |

## Output behavior

- **Format**: Default `preserve` — JPEG inputs stay JPEG, others written as PNG
- **Naming**: `{name}-clean.{ext}` (e.g., `photo-clean.png`)
- **Folder mode**: Outputs go to `metadata-cleaned/` subdirectory
- **Single file**: Sibling copy next to the original
- **Never overwrites input** — script refuses if output resolves to input

## Supported inputs

`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`, `.tiff`, `.tif`

## Known limitations

- Does not remove pixel-level watermarks, fingerprints, or invisible signals
- Does not affect external platform records or server-side provenance
- Removing ICC profiles may affect color management in some workflows
- JPEG output is lossy; PNG preferred for pixel fidelity
- Transparent images written as JPEG are composited onto white background
