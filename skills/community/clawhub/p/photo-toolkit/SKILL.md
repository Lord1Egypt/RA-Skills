---
name: photo-toolkit
version: 1.0.0
description: |
  Photography utility toolkit: convert RAW/JPG/HEIC to thumbnails, find photos by shooting date,
  generate layout previews, deflicker timelapse frames, and assemble video.
  Supports all major camera brands: Nikon (NEF), Canon (CR2/CR3), Sony (ARW),
  Fujifilm (RAF), Olympus (ORF), Panasonic (RW2), Pentax (PEF), Samsung (SRW),
  Leica (DNG), Adobe (DNG), Hasselblad (3FR), Phase One (IIQ), Sigma (X3F),
  plus standard JPEG (.jpg/.jpeg) and Apple HEIC/HEIF (.heic/.heif).

  Use when the user wants to:
  - Convert RAW/JPG/HEIC files to JPG format (single file or batch)
  - Generate thumbnails / previews from camera photos
  - Batch process photo files in a directory (with optional recursive search)
  - Find / filter photos by shooting date
  - List all photo files grouped by shooting date
  - Generate layout preview grid from graded photos
  - Remove flicker from timelapse frame sequences (deflicker)
  - Assemble sequential JPG frames into MP4 video

  Triggers: User mentions converting RAW/NEF/CR2/ARW/RAF/JPG/HEIC to JPG, generating thumbnails,
  batch processing camera photos, finding photos by date, deflicker, timelapse video assembly.

  Dependencies:
    System: libraw (RedHat: dnf install LibRaw-devel / Debian: apt-get install libraw-dev)
    Python: rawpy, pillow, numpy, pillow-heif (optional, for HEIC/HEIF)
    Check: bash scripts/setup_deps.sh
metadata:
  openclaw:
    homepage: https://github.com/konanok/photo-skills
    emoji: "📸"
    requires:
      bins:
        - python3
---

# Photo Toolkit

Convert camera RAW files (NEF/CR2/CR3/ARW/RAF/ORF/DNG/...), JPG photos, and Apple HEIC/HEIF images to JPG thumbnails, find photos by shooting date, and generate layout previews.

## Supported Formats

### Camera RAW

| Brand      | Extensions             |
| ---------- | ---------------------- |
| Nikon      | `.nef`, `.nrw`         |
| Canon      | `.cr2`, `.cr3`, `.crw` |
| Sony       | `.arw`, `.srf`, `.sr2` |
| Fujifilm   | `.raf`                 |
| Olympus/OM | `.orf`                 |
| Panasonic  | `.rw2`                 |
| Pentax     | `.pef`                 |
| Samsung    | `.srw`                 |
| Leica      | `.rwl`, `.dng`         |
| Adobe DNG  | `.dng`                 |
| Hasselblad | `.3fr`, `.fff`         |
| Phase One  | `.iiq`                 |
| Sigma      | `.x3f`                 |

### Standard Image

| Format | Extensions      | Notes            |
| ------ | --------------- | ---------------- |
| JPEG   | `.jpg`, `.jpeg` | 直接 Pillow 处理 |

### Apple (iPhone/iPad)

| Format    | Extensions       | Notes                          |
| --------- | ---------------- | ------------------------------ |
| HEIC/HEIF | `.heic`, `.heif` | 需要 `pip install pillow-heif` |

## Dependencies

**Declaration file:** `requirements.txt`

**Prefer venv**: Before running scripts, activate the project-root virtual environment (e.g. `.venv/`). If it doesn't exist, create one first:

```bash
# Create venv and install dependencies (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r photo-toolkit/requirements.txt

# Or use the skill's setup script (checks + installs)
bash photo-toolkit/scripts/setup_deps.sh

# Before each session, activate venv
source .venv/bin/activate
```

Alternatively, install globally:

```bash
brew install libraw              # macOS
# apt-get install libraw-dev     # Debian/Ubuntu
# dnf install LibRaw-devel       # RedHat/CentOS/Fedora
pip3 install -r photo-toolkit/requirements.txt
```

**Verify:**

```bash
python3 -c "import rawpy; from PIL import Image; import numpy; print('✓ Core dependencies installed')"
python3 -c "from pillow_heif import register_heif_opener; print('✓ HEIC/HEIF support available')" 2>/dev/null || echo "ℹ HEIC/HEIF support not installed (optional: pip install pillow-heif)"
```

## Configuration

Copy `config.example.toml` to `config.toml` and edit to set your directories. See `config.example.toml` for all available options.

## Scripts

### 1. `convert.py` — Photo → JPG Thumbnails

Supports RAW, JPG, and HEIC/HEIF input. By default, thumbnails are output to `{input}/thumbnails/`.

```bash
# Convert all photo files (thumbnails output to ~/data/RAW/thumbnails/)
python3 scripts/convert.py ~/data/RAW

# Custom settings
python3 scripts/convert.py ~/data/RAW ~/data/output/thumbnails --size 2048 --quality 95

# Read file list from stdin (pipe from find_by_date.py)
python3 scripts/find_by_date.py --date today ~/data/RAW | \
    python3 scripts/convert.py --from-stdin

# With report output
python3 scripts/convert.py ~/data/RAW --report /tmp/convert_report.json

# Dry run
python3 scripts/convert.py ~/data/RAW --dry-run
```

| Option         | Description                        | Default               |
| -------------- | ---------------------------------- | --------------------- |
| `input`        | Photo file or directory            | from config           |
| `output_dir`   | Output directory                   | `{input}/thumbnails/` |
| `--size`       | Max thumbnail dimension (px)       | 1200                  |
| `--quality`    | JPEG quality (1-100)               | 85                    |
| `--workers`    | Parallel workers                   | auto (max 8)          |
| `--recursive`  | Search subdirectories              | off                   |
| `--overwrite`  | Overwrite existing files           | off                   |
| `--dry-run`    | Preview only                       | off                   |
| `--no-exif`    | Skip EXIF copy                     | off                   |
| `--report`     | Output processing report JSON path | none                  |
| `--from-stdin` | Read file paths from stdin (JSON)  | off                   |

### 2. `find_by_date.py` — Find Photo Files by Date / Detect Timelapse

Searches for RAW, JPG, and HEIC/HEIF files by EXIF shooting date. Outputs JSON path list to stdout. Also detects timelapse sequences by identifying runs of photos with regular shooting intervals.

```bash
# Find by exact date (outputs JSON to stdout)
python3 scripts/find_by_date.py --date 3月15日
python3 scripts/find_by_date.py --date 2026-03-15

# Date range
python3 scripts/find_by_date.py --from 2026-03-10 --to 2026-03-15

# Save output to file
python3 scripts/find_by_date.py --date 3月15日 --output ~/data/found_files.json

# List all dates
python3 scripts/find_by_date.py --list-dates

# Timelapse: detect sequences with regular intervals, exclude casual shots
python3 scripts/find_by_date.py ~/data/RAW --timelapse
python3 scripts/find_by_date.py ~/data/RAW --timelapse --output ~/data/timelapse_found.json
python3 scripts/find_by_date.py ~/data/RAW --timelapse --min-sequence 50

# Pipe to convert.py
python3 scripts/find_by_date.py --date today ~/data/RAW | \
    python3 scripts/convert.py --from-stdin
```

| Option                 | Description                                    | Default |
| ---------------------- | ---------------------------------------------- | ------- |
| `--output`, `-o`       | Save JSON output to file                       | stdout  |
| `--timelapse`          | Detect timelapse sequences (regular intervals) | off     |
| `--min-sequence`       | Minimum frames to qualify as timelapse         | 30      |
| `--interval-tolerance` | Interval deviation tolerance (0.5 = ±50%)      | 0.5     |

Supported date formats: `2026-03-15`, `03-15`, `3月15日`, `today`, `yesterday`, `3 days ago`

### 3. `layout_preview.py` — Layout Preview (Comparison / Grid)

**Default: side-by-side comparison** (left=original, right=graded)

When `--params` is provided and contains absolute paths, originals are resolved automatically without `--originals`.

```bash
# Comparison mode with absolute paths in params (--originals not needed)
python3 scripts/layout_preview.py ~/data/output/graded \
    --params grading_params.json

# Comparison mode with explicit originals directory
python3 scripts/layout_preview.py ~/data/output/graded \
    --originals ~/data/RAW --params grading_params.json

# Grid mode (宫格) — only graded photos
python3 scripts/layout_preview.py ~/data/output/graded --grid \
    --params grading_params.json
```

| Option        | Description                     | Default                 |
| ------------- | ------------------------------- | ----------------------- |
| `graded_dir`  | Graded JPG directory (required) | —                       |
| `--originals` | Original photos directory       | auto-detect from params |
| `--params`    | grading_params.json path        | none                    |
| `--grid`      | Use grid layout instead         | off (comparison)        |
| `--cell-size` | Row height / grid cell px       | 800                     |
| `--gap`       | Gap between images px           | 6                       |
| `--quality`   | JPEG output quality             | 92                      |
| `-o/--output` | Output path                     | `../layout_preview.jpg` |

> **Note**: Without `--grid`, the script generates side-by-side BEFORE|AFTER comparisons.
> Use `--grid` only when user explicitly requests 四宫格 or 九宫格.

## Agent Integration

When the user asks to convert photo files or find photos by date:

1. **Check dependencies**: `bash scripts/setup_deps.sh`
2. **Determine input**: user path or config's `input_dir`
3. **Run the appropriate script**
4. **Report results** to the user
