---
name: ppt-generate-and-edit
description: Generate and edit PowerPoint files with python-pptx, including slide creation, text replacement, and image replacement while preserving layout. Use when the user asks to create PPTs from structured content, update existing PPT content, or perform country/theme replacement in slides.
---

# PPT Generate And Edit

## Purpose

Provide a reusable Python skill for AI agents to:
- Create PPT files from structured input.
- Update existing PPT files with text/image replacement.
- Keep image layout stable (same position and size) during replacement.

## Inputs

### create_ppt
- `title`: presentation title.
- `slides`: array of slide objects:
  - `title`: slide title.
  - `content`: string or list of paragraphs.
  - `image_prompt` (optional): prompt for image generation.

### update_ppt
- `ppt_path`: source `.pptx` path.
- `replace_rules`:
  - `text_replace`: dictionary for text replacement.
  - `image_replace`: dictionary for image replacement strategy.

## Outputs

### create_ppt
- Returns generated `.pptx` file path.

### update_ppt
- Returns:
  - `new_ppt_path`: new `.pptx` output path.
  - `replace_log`: replacement details grouped by slide.

## Module Structure

- `main.py`: external API for agent calls and demo entry.
- `ppt_generator.py`: PPT creation.
- `ppt_editor.py`: PPT text/image replacement.
- `image_service.py`: image generation abstraction (mock + extension points).
- `utils.py`: logging and path helpers.

## Usage

```python
from ppt_skill.main import create_ppt, update_ppt

slides = [
    {
        "title": "Brazil Overview",
        "content": ["Brazil is the largest country in South America."],
        "image_prompt": "Brazil skyline and national flag",
    }
]

ppt_path = create_ppt(title="Brazil Briefing", slides=slides)

result = update_ppt(
    ppt_path=ppt_path,
    replace_rules={
        "text_replace": {"Brazil": "Chile"},
        "image_replace": {"__all__": {"prompt": "Chile skyline and national flag"}},
    },
)
print(result["new_ppt_path"])
```

## Notes

- Current `generate_image()` uses `mock` backend by default.
- DALL·E and Stable Diffusion integration points are reserved as TODO.
- Keep API fields stable for downstream agent compatibility.
