---
name: photo-screener
version: 1.0.0
description: |
  AI-powered photo pre-screening using MobileCLIP2-S0 model.
  18x faster than ViT-L/14 with 80% selection consistency (Top-10 overlap 8/10).

  Use when the user wants to:
  - Filter/screen a large batch of photos before sending to LLM
  - Score photos by aesthetic quality
  - Remove near-duplicate photos (burst shots)
  - Classify photos by scene type
  - Prepare photos for multimodal LLM processing

  Triggers: User mentions filtering photos, screening images, aesthetic scoring,
  removing duplicates, classifying scenes, or preparing photos for LLM.
  Auto-skipped when photo count ≤ user's requested output count OR ≤ 20 (batch_size).
  Only triggered when photo count exceeds both thresholds.

  Dependencies:
    Python: torch, open-clip-torch, pillow, numpy, pillow-heif (optional, for HEIC/HEIF)
    Model: MobileCLIP2-S0 (~300MB, downloaded on demand with user confirmation)
    Check: bash scripts/setup_deps.sh

  Model Download:
    The model is NOT pre-downloaded. On first run:
    - Interactive mode: prompts user for confirmation
    - Non-interactive mode: exits with manual download instructions
    - Uses HuggingFace mirror (hf-mirror.com) for China acceleration
    - Add --auto-download to skip confirmation
metadata:
  openclaw:
    homepage: https://github.com/konanok/photo-skills
    emoji: "🔍"
    requires:
      bins:
        - python3
---

# Photo Screener — MobileCLIP-powered Smart Pre-screening

Intelligently filter, deduplicate, and classify photos using Apple MobileCLIP2-S0, preparing them for efficient multimodal LLM processing.

## Why MobileCLIP2-S0?

Based on 4-model comparison test:

| Metric                  |  MobileCLIP2-S0   | ViT-L/14 (baseline) |
| ----------------------- | :---------------: | :-----------------: |
| **Encoding Speed**      | **26.7ms/img** ⚡ |     483.7ms/img     |
| **Speed Ratio**         | **18.1x faster**  |         1x          |
| **Pearson Correlation** |     **0.78**      |   1.0 (baseline)    |
| **Top-10 Overlap**      |     **8/10**      |        10/10        |
| **Model Size**          |     **74.8M**     |       427.6M        |
| **Embed Dim**           |        512        |         768         |

> 💡 1/18 of the time, 80% selection consistency — best speed/quality tradeoff.

## Dependencies

**Declaration file:** `requirements.txt`

**Prefer venv**: Before running scripts, activate the project-root virtual environment (e.g. `.venv/`). If it doesn't exist, create one first:

```bash
# Create venv and install dependencies (recommended)
python3 -m venv .venv
source .venv/bin/activate
pip install -r photo-screener/requirements.txt

# Or use the skill's setup script (checks + installs)
bash photo-screener/scripts/setup_deps.sh

# Before each session, activate venv
source .venv/bin/activate
```

Alternatively, install globally:

```bash
pip3 install -r photo-screener/requirements.txt
```

## Model Download Policy

**The model is NOT pre-downloaded.** This is by design to avoid:

- Unexpected large downloads (~300MB)
- Wasted bandwidth if the user doesn't need this skill

### Download Behavior

| Mode                              | Behavior                                |
| --------------------------------- | --------------------------------------- |
| **Interactive** (terminal)        | Prompts user: "是否下载模型？[Y/n]"     |
| **Non-interactive** (piped/agent) | Exits with manual download instructions |
| **--auto-download flag**          | Downloads without confirmation          |

### Manual Download

```bash
# Using China mirror (recommended)
HF_ENDPOINT=https://hf-mirror.com python3 -c \
    "import open_clip; open_clip.create_model_and_transforms('MobileCLIP2-S0', pretrained='dfndr2b')"

# Or run setup script
bash photo-screener/scripts/setup_deps.sh
```

## Configuration

Copy `config.example.toml` to `config.toml` and edit. See `config.example.toml` for all available options.

## Usage

```bash
# Basic screening
python3 scripts/screen.py ~/data/output/thumbnails

# Custom thresholds
python3 scripts/screen.py ~/data/output/thumbnails \
    --min-score 5.0 --sim-threshold 0.95

# Keep top 50
python3 scripts/screen.py ~/data/output/thumbnails --top-k 50

# Auto-download model (skip confirmation)
python3 scripts/screen.py ~/data/output/thumbnails --auto-download

# Pass specific file paths instead of a directory
python3 scripts/screen.py \
    --paths ~/data/RAW/001/thumbnails/DSC_0001.jpg \
            ~/data/RAW/001/thumbnails/DSC_0002.jpg

# Dry run
python3 scripts/screen.py ~/data/output/thumbnails --dry-run
```

| Option            | Description                                     | Default  |
| ----------------- | ----------------------------------------------- | -------- |
| `input_dir`       | Directory with photos (optional with --paths)   | required |
| `--paths`         | Specific image paths (alternative to input_dir) | —        |
| `--output`, `-o`  | Output JSON path                                | auto     |
| `--min-score`     | Min aesthetic score (1-10)                      | 4.0      |
| `--sim-threshold` | Dedup threshold (0-1)                           | 0.97     |
| `--batch-size`    | Max photos per LLM batch                        | 20       |
| `--top-k`         | Keep only top K                                 | all      |
| `--recursive`     | Search subdirectories                           | off      |
| `--auto-download` | Skip model download prompt                      | off      |
| `--dry-run`       | Preview only                                    | off      |

## Pipeline

```
Photos (thumbnails)
    │
    ▼  Stage 1: MobileCLIP Encoding (~27ms/image)
    │  → 512-dim normalized embeddings
    │
    ├── Stage 2: Aesthetic Scoring
    │   └── LAION MLP (zero-padded 512→768 dim)
    │   └── Remove below threshold (default: 4.0)
    │
    ├── Stage 3: Similarity Dedup
    │   └── Cosine similarity + greedy dedup
    │   └── Higher score = higher priority
    │
    ├── Stage 4: Scene Classification
    │   └── Zero-shot text matching (14 categories)
    │
    └── Output: filter_report.json
```

## Agent Integration

When using this skill from an agent:

1. **Check dependencies**: `bash scripts/setup_deps.sh`
2. **Run with --auto-download**: in agent context, use `--auto-download` to skip interactive prompt
3. **Or pre-download**: run setup_deps.sh first which handles model download with user confirmation

```bash
# Agent-friendly command (auto-download)
python3 photo-screener/scripts/screen.py \
    ~/data/output/{session-id}/thumbnails \
    --output ~/data/output/{session-id}/filter_report.json \
    --auto-download
```
