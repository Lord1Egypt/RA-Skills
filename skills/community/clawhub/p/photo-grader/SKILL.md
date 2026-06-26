---
name: photo-grader
version: 1.0.0
description: |
  Apply professional-grade color grading to camera RAW/JPG/HEIC photos.
  Uses RawTherapee CLI as the sole processing engine.
  Driven by LLM-generated Lightroom-style parameters.

  Use when the user wants to:
  - Apply color grading / post-processing to camera RAW/JPG/HEIC files
  - Batch apply Lightroom-style adjustments (exposure, contrast, HSL, tone curve, etc.)
  - Process a set of photo files with AI-recommended color parameters
  - Export color-graded JPGs from RAW/JPG/HEIC files
  - Apply uniform grading to all files in a directory (timelapse / batch mode)
  - Generate RawTherapee PP3 sidecar files for manual inspection

  Triggers: User mentions color grading RAW files, applying Lightroom parameters,
  post-processing camera RAW photos, grading photos based on AI recommendations,
  or uniform grading for timelapse sequences.

  Dependencies:
    RawTherapee CLI: rawtherapee-cli in PATH (macOS; Homebrew works after user authorization, otherwise use official standalone CLI) / apt install rawtherapee-cli (Debian)
    Check: bash scripts/setup_deps.sh

  Workflow:
  1. Use `photo-toolkit` to generate thumbnails
  2. Use multimodal LLM with photo curator prompt to generate grading parameters
  3. Save LLM's JSON output as `grading_params.json`
  4. Run `grade.py` to batch-apply grading via RawTherapee

  ⚠️ IMPORTANT: Use photo_curator_prompt.md V3 (NOT v1/v2). V3 uses Lightroom-standard params with auto-mapping.
metadata:
  openclaw:
    homepage: https://github.com/konanok/photo-skills
    emoji: "🎨"
    requires:
      bins:
        - python3
        - rawtherapee-cli
---

# Photo Grader

Apply professional-grade color grading to camera photos via RawTherapee CLI, driven by JSON parameters.

## Engine

**RawTherapee CLI** is the sole processing engine, providing:

| Feature          | RawTherapee                          |
| ---------------- | ------------------------------------ |
| Demosaicing      | Multi-algorithm (AMAZE, IGT, etc.)   |
| Sharpening       | RL Deconvolution (Richardson-Lucy)   |
| Noise Reduction  | IWT / astronomy denoise              |
| Lens Correction  | **lensfun auto**                     |
| Color Management | ProPhoto internal pipeline           |
| Camera Matching  | **Auto-Matched Curve (~50 cameras)** |
| Output Quality   | **Professional**                     |

## Supported Formats

All RAW formats: NEF, CR2, CR3, ARW, RAF, ORF, RW2, DNG, PEF, SRW, 3FR, IIQ, X3F, etc.
Plus: JPEG (.jpg/.jpeg) and Apple HEIC/HEIF (.heic/.heif).

> **Note**: RAW files provide full 16-bit editing latitude for maximum quality. JPG/HEIC are 8-bit — grading range is more limited, exposure adjustments should be more conservative.

## Dependencies

**Declaration file:** `requirements.txt`

**Prefer venv**: Before running scripts, activate the project-root virtual environment (e.g. `.venv/`). If it doesn't exist, create one first:

```bash
# Create venv and install dependencies (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r photo-grader/requirements.txt

# Or use the skill's setup script (checks + installs)
bash photo-grader/scripts/setup_deps.sh

# Before each session, activate venv
source .venv/bin/activate
```

### RawTherapee CLI (Required)

```bash
# macOS
# Install RawTherapee from the official package, then copy the standalone
# rawtherapee-cli into a directory in PATH (for example ~/.local/bin).
rawtherapee-cli -h  # verify it prints "RawTherapee, version ..., command line"

# Debian / Ubuntu
sudo apt install rawtherapee-cli

# Fedora / RHEL
sudo dnf install RawTherapee
```

> macOS note: always verify with `rawtherapee-cli -h`. If it exits with `133` / `SIGTRAP`, macOS likely blocked it before startup. This is common when an agent installs RawTherapee via Homebrew and the user has not explicitly opened/authorized the app or CLI yet. A user-installed and authorized Homebrew CLI can work; otherwise use the official standalone `rawtherapee-cli` from the RawTherapee package.

## Configuration

Copy `config.example.toml` to `config.toml` and edit to set your directories. See `config.example.toml` for all available options.

## Usage

```bash
# With absolute paths in grading_params.json (--raw-dir not needed)
python3 scripts/grade.py grading_params.json --output ~/Photos/graded

# With relative filenames in params (needs --raw-dir)
python3 scripts/grade.py grading_params.json \
    --raw-dir ~/Photos/RAW --output ~/Photos/graded

# Full resolution
python3 scripts/grade.py grading_params.json --no-resize

# Uniform mode: apply one parameter set to ALL files in a directory
# (useful for timelapse or batch-processing with identical settings)
python3 scripts/grade.py grading_params.json \
    --uniform-dir ~/data/timelapse --output ~/data/output/graded

# Preview
python3 scripts/grade.py grading_params.json --dry-run

# Export PP3 only (for manual inspection or external use)
python3 scripts/grade.py grading_params.json --pp3-only --pp3-output ./pp3_files/

# Fast export mode (skip heavy modules for speed)
python3 scripts/grade.py grading_params.json --fast-export

# Control lens correction and camera matching
python3 scripts/grade.py grading_params.json --lens-corr
python3 scripts/grade.py grading_params.json --no-lens-corr
python3 scripts/grade.py grading_params.json --auto-match
python3 scripts/grade.py grading_params.json --no-auto-match
```

| Option          | Description                                          | Default      |
| --------------- | ---------------------------------------------------- | ------------ |
| `params_json`   | Grading parameters JSON                              | required     |
| `--raw-dir`     | RAW files directory (only needed for relative paths) | from config  |
| `--uniform-dir` | Apply first param set to ALL files in directory      | —            |
| `--output`      | Output directory                                     | from config  |
| `--quality`     | JPEG quality (1-100)                                 | 95           |
| `--workers`     | Parallel workers                                     | auto (max 8) |
| `--overwrite`   | Overwrite existing files                             | off          |
| `--dry-run`     | Preview only                                         | off          |
| `--pp3-only`    | Only generate PP3 files, don't render                | off          |
| `--pp3-output`  | Directory for PP3-only output                        | `./pp3/`     |
| `--fast-export` | Use RT fast export mode (skip heavy modules)         | off          |
| `--lens-corr`   | Enable/disable lens correction                       | from config  |
| `--auto-match`  | Enable/disable Auto-Matched Camera Curve             | from config  |

> **Note**: `--uniform-dir` ignores the `file` field in the JSON and applies the first parameter set to every supported photo in the directory. Useful for timelapse sequences where all frames share one grading preset.

## Color Grading Features

All standard Lightroom parameters are supported with intelligent mapping:

### Fully Supported

- ✅ Exposure (stop-based)
- ✅ Contrast
- ✅ Highlights / Shadows / Whites / Blacks
- ✅ White Balance (temperature/tint)
- ✅ Vibrance & Saturation
- ✅ Parametric Tone Curve
- ✅ HSL Per-channel Adjustments (8 channels)
- ✅ Three-Way Color Grading
- ✅ Sharpening (RL Deconvolution)
- ✅ Noise Reduction (IWT/astronomy)
- ✅ Vignette
- ✅ Film Grain

### RawTherapee-Specific Features

- **Auto-Matched Camera Profile**: Matches in-camera JPEG tone for ~50 camera models
- **Lens Correction**: Automatic via lensfun database
- **Fast Export Mode**: Skip heavy modules for speed
- **16-bit Output**: TIFF/PNG at 16-bit depth

## Cross-Format Support

The `find_raw_file()` function intelligently matches filenames across camera brands and formats:

- **Absolute path mode**: If `grading_params.json` has `"file": "/path/to/DSC_0001.NEF"` and the file exists, it's used directly
- **Absolute path fallback**: If the absolute path doesn't exist, tries different extensions in the same directory
- **Relative path mode**: If `"file": "DSC_0001.NEF"`, searches under `--raw-dir` by stem name
- **Subdirectory prefix**: If a RAW file is in a subdirectory under `--raw-dir`, the output filename gets a prefix: `001_DSC_0001_暖春丝滑.jpg`

Stem-based matching works across formats:

- If `grading_params.json` says `DSC_0001.NEF` but the actual file is `DSC_0001.CR2`, it will still be found
- Also matches JPG and HEIC files: `IMG_0001.HEIC` or `DSC_0001.JPG`

## Agent Integration

1. **Check dependencies**: `bash scripts/setup_deps.sh`
2. **Ensure thumbnails**: use `photo-toolkit` first
3. **Get grading params**: use `photo_curator_prompt.md` prompt with multimodal LLM
4. **Run grading**: `python3 scripts/grade.py grading_params.json --raw-dir ... --output ...`
