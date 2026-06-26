# Examples

## Example requests

- "Turn this flowchart image into an editable PowerPoint slide. It should match the image closely."
- "Recreate this dashboard screenshot as an editable PPTX slide."
- "Convert this infographic into a fully editable PowerPoint slide, not just an embedded image."
- "Turn these 5 screenshots into a matching editable PowerPoint deck. One slide per image."

## Suggested execution pattern

1. Analyze the image visually
2. Decide whether it is a one-slide or multi-slide job
3. Create either:
   - a one-off generator script in the workspace, e.g. `make_flowchart.py`, or
   - a JSON spec plus reusable script
4. Use `python-pptx` to rebuild the layout with editable objects
5. Save the PPTX
6. Do a second pass for fidelity
7. Commit the resulting files

## Starter template generator

Generate a starter spec for a single slide:

```bash
python skills/image-to-editable-ppt-slide/scripts/generate_spec_template.py \
  --title "Sample Flowchart" \
  --output sample_spec.json
```

Generate a 3-slide deck starter spec:

```bash
python skills/image-to-editable-ppt-slide/scripts/generate_spec_template.py \
  --title "Incident Deck" \
  --slides 3 \
  --output incident_deck_spec.json
```

## Build a PPTX from a JSON spec

```bash
python skills/image-to-editable-ppt-slide/scripts/pptx_rebuilder.py sample_spec.json output.pptx
```

## Minimal multi-slide JSON spec example

```json
{
  "presentation": {
    "width": 13.333,
    "height": 7.5,
    "background": "F8F8FA"
  },
  "slides": [
    {
      "background": "F8F8FA",
      "items": [
        {
          "kind": "textbox",
          "x": 0,
          "y": 0.4,
          "w": 13.333,
          "h": 0.5,
          "text": "Slide 1",
          "size": 32,
          "color": "1B3460"
        }
      ]
    },
    {
      "items": [
        {
          "kind": "shape",
          "shape": "round_rect",
          "x": 0.8,
          "y": 1.2,
          "w": 3.2,
          "h": 0.8,
          "fill": "E9EBF1",
          "text": "Slide 2 Card",
          "size": 20,
          "color": "1B3460"
        }
      ]
    }
  ]
}
```

## Publish to ClawHub when ready

```bash
clawhub whoami
clawhub publish ./skills/image-to-editable-ppt-slide \
  --slug image-to-editable-ppt-slide \
  --name "Image to Editable PPT Slide" \
  --version 1.0.0 \
  --changelog "Initial release with multi-slide support and JSON template generator"
```
