---
name: perceptron
description: >
  Image and video analysis powered by Isaac vision models. Capabilities include visual Q&A,
  object detection, OCR, captioning, counting, and grounded spatial reasoning with bounding boxes,
  points, and polygons. Supports streaming, structured outputs, DSL composition, and in-context learning.
  NOT for: generating images (analysis only).
metadata: {"openclaw": {"requires": {"env": ["PERCEPTRON_API_KEY"]}, "primaryEnv": "PERCEPTRON_API_KEY"}}
---

# Perceptron — Vision SDK

Docs: https://docs.perceptron.inc/

Image and video analysis via the Perceptron Python SDK. Pass file paths or URLs directly — the SDK handles base64 conversion automatically.

## Setup

```bash
pip install perceptron
export PERCEPTRON_API_KEY=ak_...
```

## Quick Reference

| Task | Function | Example |
|------|----------|---------|
| Describe / Q&A | `question()` | `question("photo.jpg", "What's in this image?")` |
| Grounded Q&A | `question()` | `question("photo.jpg", "Where is the cat?", expects="box")` |
| Object detection | `detect()` | `detect("photo.jpg", classes=["person", "car"])` |
| OCR | `ocr()` | `ocr("document.png")` |
| OCR (markdown) | `ocr_markdown()` | `ocr_markdown("document.png")` |
| Caption | `caption()` | `caption("photo.jpg", style="detailed")` |
| Counting | `question()` | `question("photo.jpg", "How many dogs?", expects="point")` |
| Custom workflow | `@perceive` | See DSL composition below |

## Python SDK

```python
from perceptron import configure, detect, caption, ocr, ocr_markdown, question

# Configuration (or set PERCEPTRON_API_KEY env var)
configure(provider="perceptron", api_key="ak_...")

# Visual Q&A — the most common operation
result = question("photo.jpg", "What's happening in this image?")
print(result.text)

# Grounded Q&A — get bounding boxes with answers
result = question("photo.jpg", "Where is the damage?", expects="box")
for box in result.points or []:
    print(f"{box.mention}: ({box.top_left.x},{box.top_left.y}) → ({box.bottom_right.x},{box.bottom_right.y})")

# Object detection
result = detect("warehouse.jpg", classes=["forklift", "person"])
for box in result.points or []:
    print(f"{box.mention}: ({box.top_left.x},{box.top_left.y}) → ({box.bottom_right.x},{box.bottom_right.y})")

# OCR
result = ocr("receipt.jpg", prompt="Extract the total amount")
print(result.text)

result = ocr_markdown("document.png")  # structured markdown output
print(result.text)

# Captioning
result = caption("scene.png", style="detailed")
print(result.text)
```

### DSL Composition (Advanced)

Build custom multimodal workflows:

```python
from perceptron import perceive, image, text, system

@perceive(expects="box", model="isaac-0.2-2b-preview")
def find_hazards(img_path):
    return [system("<hint>BOX</hint>"), image(img_path), text("Locate all safety hazards")]

result = find_hazards("factory.jpg")
```

### Structured Outputs

Constrain responses to Pydantic models, JSON schemas, or regex:

```python
from perceptron import perceive, image, text, pydantic_format
from pydantic import BaseModel

class Scene(BaseModel):
    objects: list[str]
    count: int

@perceive(response_format=pydantic_format(Scene))
def count_objects(path):
    return image(path) + text("List all objects and count them. Return JSON.")

result = count_objects("photo.jpg")
scene = Scene.model_validate_json(result.text)
```

### Pixel Coordinate Conversion

All spatial outputs use normalized coordinates (0–1000). Convert to pixels:

```python
pixel_boxes = result.points_to_pixels(width=1920, height=1080)

# Or standalone:
from perceptron import scale_points_to_pixels
pixel_pts = scale_points_to_pixels(result.points, width=1920, height=1080)
```

## CLI Script

Located at: `<skill-dir>/scripts/perceptron_cli.py`

Requires `PERCEPTRON_API_KEY` environment variable. The provider is always `perceptron`.

```bash
P=<skill-dir>/scripts/perceptron_cli.py

# Visual Q&A
python3 $P question photo.jpg "What do you see?"
python3 $P question photo.jpg "Where is the car?" --expects box

# Object detection
python3 $P detect photo.jpg --classes person,car
python3 $P detect photo.jpg --classes forklift --format json --pixels
python3 $P detect ./frames/ --classes defect  # batch directory

# OCR
python3 $P ocr document.png
python3 $P ocr receipt.jpg --output markdown

# Captioning
python3 $P caption scene.png --style detailed

# Custom perceive
python3 $P perceive frame.png --prompt "Describe this scene" --expects box

# Batch processing
python3 $P batch --images img1.jpg img2.jpg --prompt "Describe" --output results.json

# Parse raw model output
python3 $P parse "<point_box ...>" --mode points

# List models
python3 $P models
```

## Models

| Model | Best for | Speed | Temp |
|-------|----------|-------|------|
| `isaac-0.2-2b-preview` (default) | General use, detection, OCR | Fast | 0.0 |
| `isaac-0.2-1b` | Quick/simple tasks | Fastest | 0.0 |

Override with `model="..."` in any SDK call or `--model ...` in CLI.

## Grounding (expects parameter)

| Value | Returns | Use case |
|-------|---------|----------|
| `text` (default) | Plain text | Q&A, descriptions, OCR |
| `box` | Bounding boxes | Detection, localization |
| `point` | Point coordinates | Counting, pointing |
| `polygon` | Polygon vertices | Segmentation |

## Video Analysis

Extract frames with ffmpeg, then analyze:

```bash
# Single frame at 5 seconds
ffmpeg -ss 5 -i video.mp4 -frames:v 1 -q:v 2 /tmp/frame.jpg

# Then analyze
python3 $P question /tmp/frame.jpg "What's happening?"
```

For continuous monitoring, extract multiple frames and batch process.

## Reference Files

For deeper SDK usage, consult these when needed:

- **[references/capabilities.md](references/capabilities.md)** — Focus mode, reasoning, streaming, ICL, structured outputs, annotation types
- **[references/prompting.md](references/prompting.md)** — Optimal prompts per task, vision hints (`<hint>BOX</hint>`), temperature guide
- **[references/api.md](references/api.md)** — SDK configuration, models, image formats, streaming, best practices
