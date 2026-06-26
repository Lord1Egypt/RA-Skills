---
name: photo-to-3d
description: One-click photo to 3D model pipeline. Upload any photo, AI generates a clean isometric view via Gemini (Nano Banana), then converts it to a production-ready 3D model (.glb) via Tripo3D API. Use when user wants to convert photos/images to 3D models, generate 3D assets from pictures, or create 3D content from 2D images. Triggers on "photo to 3D", "image to 3D", "convert to 3D model", "generate 3D", "照片转3D", "图片生成3D模型", "一键3D建模".
---

# Photo to 3D Model

Two-step pipeline that converts any photo into a 3D model:

1. **Gemini preprocess** — Transform photo into a clean white-background 45° isometric view
2. **Tripo3D generate** — Convert the isometric image into a .glb 3D model

## Requirements

- `GEMINI_API_KEY` — Get from https://aistudio.google.com/apikey
- `TRIPO_API_KEY` — Get from https://platform.tripo3d.ai/

## Usage

```bash
# Full pipeline: photo → isometric view → 3D model
python3 scripts/photo_to_3d.py <image_path>

# Custom prompt for Gemini preprocessing
python3 scripts/photo_to_3d.py <image_path> --prompt "your custom prompt"

# Skip preprocessing (image is already a clean isometric view)
python3 scripts/photo_to_3d.py <image_path> --skip-preprocess

# Custom output directory
python3 scripts/photo_to_3d.py <image_path> --output-dir ./my_output
```

## Output

- `output/{name}_isometric.png` — Gemini-generated isometric view
- `output/{name}_model.glb` — Final 3D model file

## Default Gemini Prompt

The built-in prompt generates a 45° isometric "3D-printed model" style render with PBR materials on a pure white background. Override with `--prompt` for custom styles (e.g., game assets, architectural models, product renders).

## Notes

- Supported input: .jpg, .jpeg, .png, .webp
- Tripo3D generation takes ~1-3 minutes depending on complexity
- For higher quality, preprocess source images with upscayl before running
- Output .glb files can be converted to .usdz for Apple AR using `usdzconvert`
