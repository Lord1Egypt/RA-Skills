# Image Metadata Cleaner

**Clean privacy-sensitive metadata from user-owned images by writing sanitized copies.**

Cameras, editors, and image tools embed extensive metadata — EXIF camera data, GPS coordinates, C2PA provenance certificates, XMP/IPTC tags. This data can leak personal information and bloat file sizes. This tool removes it all by re-encoding pixel data into a fresh file.

Designed for privacy hygiene and reproducible publishing workflows. **Not for** hiding authorship, evading provenance checks, bypassing platform labels, or misrepresenting image origin.

```
Input:  photo.png (1.5MB, EXIF GPS + 23KB C2PA certificate)
Output: photo-clean.png (1.4MB, zero metadata, same resolution)
```

## Quick Start

```bash
# Install via ClawHub
clawhub install image-metadata-cleaner

# Single file — writes photo-clean.png beside the original
uv run --with "pillow>=10.0" scripts/strip.py "photo.png" --manifest

# Batch folder — writes to metadata-cleaned/ subdirectory
uv run --with "pillow>=10.0" scripts/strip.py "C:\Users\you\Downloads" --manifest

# Preview without writing files
uv run --with "pillow>=10.0" scripts/strip.py "/path/to/folder" --dry-run

# Force JPEG output
uv run --with "pillow>=10.0" scripts/strip.py "/path/to/folder" --format jpg
```

## Safety Features

| Feature | Description |
|---------|-------------|
| Never modifies original | Writes copies only; refuses output = input |
| Default subdirectory | Folder mode outputs to `metadata-cleaned/` |
| Verification scan | Reopens output, checks for residual metadata and C2PA/JUMBF markers |
| JSON manifest | Optional `--manifest` for reproducible workflows |
| Dry-run preview | `--dry-run` shows planned outputs without writing |

## Options

| Flag | Description |
|------|-------------|
| `-o <path>` | Output file path (single file mode) |
| `--output-dir <dir>` | Output directory (batch mode) |
| `-f preserve\|jpg\|png` | Output format (default: `preserve`) |
| `-q <1-100>` | JPEG quality (default: 95) |
| `--recursive` | Process subdirectories |
| `--overwrite` | Overwrite existing output (with confirmation) |
| `--dry-run` | Preview without writing |
| `--manifest [path]` | Write JSON manifest |

## Supported Formats

Input: PNG, JPEG, WebP, BMP, TIFF
Output: JPEG or PNG (default preserves input format)

## What Gets Removed

EXIF (GPS, camera, device) · XMP · IPTC/Photoshop · ICC Profile · C2PA/JUMBF provenance containers

## Known Limitations

- Does not remove pixel-level watermarks or invisible signals
- Does not affect external platform records or server-side provenance
- JPEG is lossy; PNG preferred for pixel fidelity

## License

MIT-0 (Free to use, modify, and redistribute. No attribution required.)
