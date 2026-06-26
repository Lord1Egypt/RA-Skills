# Local Script Setup

This document describes the interface for local scripts used as image/video generators.

---

## Interface

The skill calls your script with two arguments:

| Argument | Description |
|----------|-------------|
| `$1` | Output file path — save the generated image or video here (e.g. `/tmp/result_abc.png`) |
| `$2` | Job spec JSON path — read this file to get job details |

---

## Spec JSON Schema

The JSON file at `$2` contains:

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `description` | string | Detailed job description | `"A sunset over snow-capped mountains"` |
| `title` | string | Job subject/theme | `"Mountain Sunset"` |
| `style` | string | Art style | `"watercolor"` |
| `mood` | string | Emotional tone | `"calm, serene"` |
| `color` | string | Color palette | `"warm orange, deep purple"` |
| `ratio` | string | Aspect ratio | `"16:9"` |
| `referenceUrls` | string[] | Reference image URLs | `["https://example.com/ref.jpg"]` |
| `budget` | number | Job budget in credits | `50` |

---

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success — result file exists at `$1` |
| non-zero | Failure — the skill reports an error and skips the job |

---

## Timeout

Maximum execution time is 15 minutes. Scripts exceeding this limit are terminated.

---

## Supported Output Formats

| Type | Extensions |
|------|-----------|
| Image | `.png`, `.jpg`, `.webp`, `.gif` |
| Video | `.mp4`, `.mov`, `.webm` |

---

## Example

```python
import sys, json

output_path = sys.argv[1]
spec_path = sys.argv[2]

with open(spec_path) as f:
    spec = json.load(f)

prompt = spec.get('description', '')
style = spec.get('style', '')
references = spec.get('referenceUrls', [])

# --- Replace this section with your generation logic ---
# Example: call a local API, run ComfyUI, invoke a model, etc.
#
# result_bytes = your_generate_function(prompt, style, references)
#
# with open(output_path, 'wb') as out:
#     out.write(result_bytes)
# --------------------------------------------------------
```
