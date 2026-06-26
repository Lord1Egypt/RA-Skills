# ppt_skill

Reusable Python skill module for AI agents to generate and modify PowerPoint files.

## Features

- `create_ppt`: create PPT slides from structured content.
- `update_ppt`: replace text and replace images in existing PPT files.
- `generate_image`: image generation interface (mock by default, extensible to DALL·E or Stable Diffusion).
- Stable layout behavior for image replacement (keeps original position and size).

## Project Structure

```text
ppt_skill/
  __init__.py
  main.py
  ppt_generator.py
  ppt_editor.py
  image_service.py
  utils.py
  SKILL.md
  README.md
  requirements.txt
  LICENSE
```

## Install

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from ppt_skill.main import create_ppt, update_ppt

slides = [
    {
        "title": "Brazil Overview",
        "content": [
            "Brazil is the largest country in South America.",
            "Its economy is driven by agriculture, mining, and services.",
        ],
        "image_prompt": "Brazil flag and skyline of Sao Paulo",
    }
]

source_ppt = create_ppt("Brazil Trade Briefing", slides)

result = update_ppt(
    ppt_path=source_ppt,
    replace_rules={
        "text_replace": {"Brazil": "Chile", "Sao Paulo": "Santiago"},
        "image_replace": {"__all__": {"prompt": "Chile flag and Chilean city skyline"}},
    },
)

print(result["new_ppt_path"])
print(result["replace_log"])
```

## Demo

Run the built-in demo (Brazil -> Chile):

```bash
python -m ppt_skill.main
```

## Notes

- This package logs key steps for debug and traceability.
- `update_ppt` always saves to a new output file to avoid overriding source files.
- `image_replace` currently uses rule-based matching; visual semantic matching is left as future extension.
