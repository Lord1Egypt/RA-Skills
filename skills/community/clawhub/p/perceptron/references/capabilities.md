# Capabilities Reference

Docs: https://docs.perceptron.inc/capabilities/

## Visual Q&A

Ask grounded questions about any scene. Returns text answers, optionally with spatial annotations.

```python
from perceptron import question

# Simple Q&A
result = question("photo.jpg", "What's happening here?")
print(result.text)

# Grounded Q&A (with bounding boxes)
result = question("photo.jpg", "Where is the safety equipment?", expects="box")
for box in result.points or []:
    print(f"{box.mention}: ({box.top_left.x},{box.top_left.y}) → ({box.bottom_right.x},{box.bottom_right.y})")

# Counting with points
result = question("photo.jpg", "How many cars are there? Point to each.", expects="point")
for pt in result.points or []:
    print(f"{pt.mention}: ({pt.x}, {pt.y})")
```

## Object Detection

Locate targets with precise bounding boxes, points, or polygons.

```python
from perceptron import detect, scale_points_to_pixels
from PIL import Image

result = detect("warehouse.jpg", classes=["forklift", "person", "pallet"])
for box in result.points or []:
    print(f"{box.mention}: ({box.top_left.x},{box.top_left.y}) → ({box.bottom_right.x},{box.bottom_right.y})")

# Convert to pixel coordinates
w, h = Image.open("warehouse.jpg").size
pixel_pts = scale_points_to_pixels(result.points, width=w, height=h)
# or: pixel_pts = result.points_to_pixels(w, h)
```

## OCR

Extract structured text. Supports plain text, HTML, and Markdown output.

```python
from perceptron import ocr, ocr_html, ocr_markdown

# Basic OCR
result = ocr("document.png")
print(result.text)

# Custom extraction
result = ocr("receipt.jpg", prompt="Extract the table data as CSV")
print(result.text)

# Structured output formats
result = ocr_html("document.png")     # HTML output
result = ocr_markdown("document.png") # Markdown output
```

## Captioning

Generate concise or detailed descriptions with optional grounding.

```python
from perceptron import caption

# Concise
result = caption("photo.jpg", style="concise")
print(result.text)

# Detailed with grounding boxes
result = caption("photo.jpg", style="detailed", expects="box")
print(result.text)
for box in result.points or []:
    print(f"  [{box.mention}] ({box.top_left.x},{box.top_left.y}) → ({box.bottom_right.x},{box.bottom_right.y})")
```

## Streaming

Stream incremental text and coordinate deltas for real-time applications.

```python
from perceptron import detect

for event in detect("frame.png", classes=["person"], stream=True):
    if event["type"] == "text.delta":
        print(event["chunk"], end="", flush=True)
    elif event["type"] == "points.delta":
        print(f"Detection: {event['points']}")
    elif event["type"] == "final":
        result = event["result"]
```

## Focus (Zoom-and-Recall)

Let Isaac zoom into image regions for fine-grained answers. Useful for pixel-level scrutiny (serial numbers, fine print, tiny defects) and dense scenes.

```python
from perceptron import perceive, image, text

@perceive(focus=True)
def describe_scene(photo):
    return image(photo) + text("List every object you can see with colors.")

result = describe_scene("busy_scene.jpg")
print(result.text)
```

## Reasoning Traces

Expose chain-of-thought for complex analysis.

```python
from perceptron import perceive, image, text

@perceive(reasoning=True)
def analyze(img):
    return image(img) + text("Are all workers wearing proper safety equipment?")

result = analyze("factory.jpg")
print("answer:", result.text)
print("reasoning:", result.reasoning)
```

## Structured Outputs

Constrain model replies to Pydantic, JSON schemas, or regex.

### Pydantic
```python
from perceptron import image, perceive, pydantic_format, text
from pydantic import BaseModel, Field
from typing import Literal

class SceneAnalysis(BaseModel):
    scene_type: str = Field(description="outdoor, indoor, urban, nature")
    main_subjects: list[str]
    mood: Literal["calm", "energetic", "dramatic", "peaceful", "tense"]

@perceive(response_format=pydantic_format(SceneAnalysis))
def analyze_scene(path: str):
    return image(path) + text("Analyze this scene and return JSON.")

result = analyze_scene("scene.jpg")
analysis = SceneAnalysis.model_validate_json(result.text)
```

### JSON Schema
```python
from perceptron import image, json_schema_format, perceive, text

schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "keywords": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title", "keywords"],
    "additionalProperties": False
}

@perceive(response_format=json_schema_format(schema, name="summary", strict=True))
def summarize(path: str):
    return image(path) + text("Summarize the image.")
```

### Regex
```python
from perceptron import image, perceive, regex_format, text

@perceive(response_format=regex_format(r"yes|no"))
def quick_check(path: str):
    return image(path) + text("Is there a stop sign? Respond yes or no.")
```

## In-Context Learning (ICL)

Teach Isaac new visual concepts with annotated examples.

```python
from perceptron import annotate_image, bbox, detect

# Create exemplar from bootstrap detection
bootstrap = detect("example.jpg", classes=["mixer"])
first_box = (bootstrap.points or [])[0]
exemplar = annotate_image("example.jpg", {"mixer": [bbox(
    int(first_box.top_left.x), int(first_box.top_left.y),
    int(first_box.bottom_right.x), int(first_box.bottom_right.y),
    mention="mixer",
)]})

# Apply to new image with few-shot example
result = detect("kitchen.jpg", classes=["mixer"], examples=[exemplar])
```

## DSL Composition

Build custom multimodal workflows with typed nodes.

```python
from perceptron import perceive, image, text, system

@perceive(expects="box", stream=True)
def find_safety_equipment(image_path):
    return [
        system("<hint>BOX</hint>"),
        image(image_path),
        text("Locate all safety equipment including helmets, vests, and signs"),
    ]

# Inspect compiled payload without executing
from perceptron import inspect_task
payload = inspect_task(find_safety_equipment, "warehouse.jpg")
```

## Coordinate System

All spatial outputs use **normalized coordinates (0–1000)**.

```
pixel_x = (normalized_x / 1000) * image_width
pixel_y = (normalized_y / 1000) * image_height
```

SDK helpers:
- `result.points_to_pixels(width, height)` — on PerceiveResult
- `scale_points_to_pixels(result.points, width=w, height=h)` — standalone function

## Annotation Types

| Type | Attributes | Description |
|------|-----------|-------------|
| `SinglePoint` | `.x`, `.y`, `.mention`, `.t` | Single coordinate |
| `BoundingBox` | `.top_left`, `.bottom_right`, `.mention`, `.t` | Rectangle (two SinglePoints) |
| `Polygon` | `.hull`, `.mention`, `.t` | List of SinglePoints |
| `Collection` | `.items`, `.mention`, `.t` | Group of annotations |

## Text Parsing Utilities

```python
from perceptron import extract_points, parse_text, strip_tags

# Extract specific annotation types from raw text
boxes = extract_points(raw_text, expected="box")
points = extract_points(raw_text, expected="point")
polys = extract_points(raw_text, expected="polygon")

# Get ordered segments (text + tags)
segments = parse_text(raw_text)

# Strip all tags, return plain text
clean = strip_tags(raw_text)
```
