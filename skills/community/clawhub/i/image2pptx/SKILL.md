---
name: image2pptx
description: >
  Convert static images (slides, posters, infographics) to editable PowerPoint files.
  OCR detects text, classical CV textmask detects ink pixels, mask-clip preserves
  illustrations, LAMA inpaints clean background, python-pptx assembles editable
  text boxes with auto-scaled fonts and detected colors.
  Trigger on 'convert image to pptx', 'make slide editable', 'image to powerpoint',
  'extract text from slide as editable', 'reconstruct slide', or when the user has
  a slide/poster image and wants an editable .pptx file.
metadata:
  author: Jade Liu
  source: https://github.com/JadeLiu-tech/px-image2pptx
risk: low
---

# image2pptx: Image to Editable PowerPoint

## What It Does

Converts a static image into an editable .pptx file where every text element is a selectable, editable text box over a clean inpainted background.

1. **OCR** (PaddleOCR PP-OCRv5) — detects text regions with bounding boxes and content
2. **Textmask** (classical CV) — finds text ink pixels via adaptive thresholding
3. **Mask-clip** — ANDs textmask with OCR bboxes to preserve non-text elements
4. **Inpaint** (LAMA) — reconstructs masked regions with neural inpainting
5. **Assemble** — places editable text boxes with auto-scaled fonts and detected colors

## When to Use

| Scenario | Recommendation |
|----------|---------------|
| Slide with text on solid/flat background | Best results |
| Slide with photo background | Good — uses inpainting (warn about overlap areas) |
| Slide with solid background | Good — use `--skip-inpaint` for speed |
| Chinese/multilingual slide | Good — `ch` OCR handles both Chinese and English |
| Poster or infographic with text | Good — works well if text is separate from graphics |
| Dense chart with axis labels on bars | Caution — line grouping may over-merge crowded labels |
| Very thick/large decorative fonts | Caution — may exceed standard mask dilation range |
| Extract individual assets as PNGs | No — use px-asset-extract |
| Read text without creating PPTX | No — use OCR directly |
| Edit an existing .pptx file | No — use the pptx skill |

## Installation

```bash
git clone https://github.com/JadeLiu-tech/px-image2pptx.git
cd px-image2pptx
pip install -e ".[all]"
```

## Usage

### CLI

```bash
px-image2pptx slide.png -o output.pptx
px-image2pptx slide.png -o output.pptx --lang ch
px-image2pptx slide.png -o output.pptx --skip-inpaint
px-image2pptx slide.png -o output.pptx --ocr-json text_regions.json
px-image2pptx slide.png -o output.pptx --work-dir ./debug/
```

### Python API

```python
from px_image2pptx import image_to_pptx

report = image_to_pptx("slide.png", "output.pptx")

# With options
report = image_to_pptx(
    "slide.png", "output.pptx",
    lang="ch",
    skip_inpaint=False,
    work_dir="./debug/",
)
```

## CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `-o`, `--output` | `output.pptx` | Output PPTX path |
| `--ocr-json` | | Pre-computed OCR JSON (skips OCR) |
| `--lang` | `auto` | OCR language: `auto`, `en`, `ch` |
| `--sensitivity` | `16` | Textmask sensitivity (lower = more) |
| `--dilation` | `12` | Textmask dilation pixels |
| `--min-font` | `8` | Min font size in points |
| `--max-font` | `72` | Max font size in points |
| `--skip-inpaint` | | Skip LAMA inpainting |
| `--work-dir` | | Save intermediate files |

## Models

Downloaded automatically on first use (~370 MB total). All models are from official open-source repositories.

| Model | Size | License | Source |
|-------|------|---------|--------|
| PP-OCRv5_server_det | 84 MB | Apache 2.0 | [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) |
| PP-OCRv5_server_rec | 81 MB | Apache 2.0 | [PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) |
| big-lama | 196 MB | Apache 2.0 | [advimman/lama](https://github.com/advimman/lama) |

Models are cached locally after first download (`~/.paddlex/official_models/` for OCR, `~/.cache/torch/hub/checkpoints/` for LAMA). To skip model downloads entirely, use `--ocr-json` with pre-computed OCR and `--skip-inpaint`.

## Limitations — When to Warn the User

| Input | Impact | What to tell the user |
|-------|--------|----------------------|
| Text on solid/flat background | Best results | No caveats needed |
| Text on textured background | Good results | LAMA handles repeating textures well |
| Text overlapping photos | Inpainting artifacts likely | "Areas where text covers photos may show blurring" |
| Dense chart with many labels | Over-merged labels | "Crowded labels may be grouped incorrectly" |
| Very thick/large fonts | Incomplete mask coverage | "Large fonts may exceed dilation range — try increasing `--dilation`" |
| Light text on dark background | Blockier inpainting | "White-on-dark text uses box masks instead of tight ink masks" |
| WebP image | OCR fails (0 regions) | Convert to PNG first: `Image.open("in.webp").save("in.png")` |
| Very large image (>4000px) | Slow inpainting | Suggest `--skip-inpaint` or downscaling |
| Decorative/handwritten fonts | Typeface won't match | "Fonts are reconstructed as Arial/Helvetica" |
| Centered/justified text | Left-aligned output | "Text alignment is not preserved" |
