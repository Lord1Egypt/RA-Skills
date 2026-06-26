---
name: postergen-parser
description: >-
  Parse PDF/Markdown files into structured HTML posters with multi-modal output
  (PDF, PNG, DOCX, PPTX), or generate poster/slides images via Gemini image generation.
---

# PosterGen Parser Unit

Parse PDF or Markdown documents into styled HTML posters with LLM-based rendering, then convert to PDF, PNG, DOCX, and PPTX. Additionally, generate **poster images** and **slides images** using Gemini's native image generation API.

## Prerequisites

- Python 3.12+
- LLM API key (OpenAI, Gemini, or Qwen)
- System dependencies (fonts, Chromium libs)

## Quick Start

### 1. Install

```bash
bash install.sh
```

This will:
- Install UV (Python package manager)
- Install Python 3.12
- Install system dependencies (fonts, Chromium libraries)
- Create virtual environment and install dependencies
- Install Playwright Chromium browser
- Create `.env` configuration file

### 2. Configure

Edit `.env` file with your API credentials:

```bash
# OpenAI
TEXT_MODEL="gpt-4.1-2025-04-14"
OPENAI_API_KEY="your-key"
OPENAI_BASE_URL="https://api.openai.com/v1"

# Qwen (MAAS)
TEXT_MODEL="qwen3-vl-235b-a22b-instruct"
OPENAI_API_KEY="your-key"
OPENAI_BASE_URL="https://maas.devops.xiaohongshu.com/v1"

# Gemini
TEXT_MODEL="gemini-3-pro-preview"
RUNWAY_API_KEY="your-key"
```

### 3. Run

```bash
# Full pipeline: PDF → HTML → PDF/PNG/DOCX
uv run python run.py --pdf_path input.pdf --output_dir ./output

# Markdown → HTML with template
uv run python run.py --md_path input.md --output_dir ./output --template templates/doubao.txt

# Generate poster image (Gemini)
uv run python run.py --md_path input.md --output_dir ./output \
  --output_type poster_image --style academic --density medium

# Generate slides images (Gemini)
uv run python run.py --md_path input.md --output_dir ./output \
  --output_type slides_image --style doraemon --slides_length medium

# Generate XHS slides
uv run python run.py --md_path input.md --output_dir ./output \
  --output_type xhs_slides --style academic --slides_length short

# Convert HTML to multi-modal
uv run python -m mm_output.cli input.html --format all --output-dir ./mm_outputs
```

### 4. Run Tests

```bash
bash run.sh
```

## Command Reference

### Main Entry: `run.py`

| Command | Description |
|---------|-------------|
| `uv run python run.py --pdf_path FILE --output_dir DIR` | Parse PDF to HTML + multi-modal outputs |
| `uv run python run.py --md_path FILE --output_dir DIR` | Parse Markdown to HTML + multi-modal outputs |
| `--output_type poster_image` | Generate poster image (Gemini) |
| `--output_type slides_image` | Generate slides images (Gemini, 16:9) |
| `--output_type xhs_slides` | Generate XHS slides (Gemini, 9:16 + HTML) |
| `--template templates/NAME.txt` | Use specific template |
| `--style {academic,doraemon,minimal}` | Visual style for image generation |
| `--density {sparse,medium,dense}` | Content density for poster_image |
| `--slides_length {short,medium,long}` | Slide count: short=5-8, medium=8-12, long=12-15 |
| `--text_model MODEL` | Override LLM model |
| `--language {auto,zh,en}` | Output language |

### Multi-modal Conversion: `mm_output.cli`

```bash
# Convert HTML to specific format
uv run python -m mm_output.cli input.html --format pdf --output-dir ./out

# Convert to all formats
uv run python -m mm_output.cli input.html --format all --output-dir ./out

# Supported formats: pdf, png, docx, pptx, all
```

## Environment Setup (UV)

This project uses [UV](https://github.com/astral-sh/uv) for Python package management.

### Manual Setup (if install.sh fails)

> **Note:** The `uv.lock` file is renamed to `uv.lock.txt` to avoid tracking. Before using UV, rename it back:
> ```bash
> mv uv.lock.txt uv.lock
> ```

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python 3.12
uv python install 3.12

# Create virtual environment
uv venv .venv --python 3.12

# Rename lock file back and sync dependencies
mv uv.lock.txt uv.lock
uv sync

# Install Playwright browsers
uv run playwright install chromium
```

### Dependency Management

```bash
# Sync dependencies from pyproject.toml
uv sync

# Add new dependency
uv add package_name

# Lock dependencies
uv lock
```

## Templates

Available templates in `templates/`:

| Template | Description |
|----------|-------------|
| `doubao.txt` | Default style |
| `doubao_dark.txt` | Dark theme |
| `doubao_minimal.txt` | Minimal clean |
| `doubao_newspaper.txt` | Multi-column layout |
| `doubao_enterprise_blue.txt` | Corporate style |
| `doubao_refine.txt` | Refined style |
| `report_web.txt` | Web report style |
| `report_web_reduced.txt` | Simplified web style |

## System Dependencies

Required for non-Docker installation:

```bash
# Fonts
fonts-noto-cjk fonts-wqy-zenhei fonts-wqy-microhei

# Chromium libraries
libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2
libdrm2 libxcomposite1 libxdamage1 libxrandr2 libgbm1
libxshmfence1 libasound2 libpangocairo-1.0-0 libgtk-3-0
libx11-xcb1 libxcursor1 libxi6 libxss1 libxtst6
```

Install via:
```bash
bash install.sh
```

## Troubleshooting

- **Chrome not found**: Leave `CHROME_EXECUTABLE_PATH` empty to use Playwright's Chromium
- **Chinese characters garbled**: Install `fonts-noto-cjk`
- **LLM API errors**: Check `.env` has correct `TEXT_MODEL` and API key
- **Slow first run**: Model downloads are cached; subsequent runs are faster

## Project Structure

```
.
├── run.py              # Main entry point
├── run.sh              # Test script
├── parser_unit.py      # PDF/Markdown parsing
├── renderer_unit.py    # HTML rendering

├── mm_output/          # Multi-modal conversion (HTML→PDF/PNG/DOCX/PPTX)
├── paper2slides/       # Image generation (Poster/Slides via Gemini)
├── templates/          # HTML templates
├── install.sh          # Setup script (no options needed)
├── pyproject.toml      # UV configuration
├── uv.lock             # Locked dependencies
└── README.md           # Documentation
```
