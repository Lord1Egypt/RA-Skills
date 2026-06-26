# Prompting Reference

Docs: https://docs.perceptron.inc/best-practices/prompting-reference

## Optimal Prompts by Task

| Task | SDK Helper | Optimal Prompt |
|------|-----------|---------------|
| Concise caption | `caption(style="concise")` | `Provide a concise, human-friendly caption for the upcoming image.` |
| Detailed caption | `caption(style="detailed")` | `Provide a detailed caption describing key objects, relationships, and context in the upcoming image.` |
| OCR | `ocr()` | System: `You are an OCR system. Accurately detect, extract, and transcribe all readable text from the image.` |
| General detection | `detect()` | `Your goal is to segment out the objects in the scene` |
| Class detection | `detect(classes=[...])` | `Your goal is to segment out the following categories: {categories}` |
| Visual Q&A | `question()` | Pass your question directly as user content |
| Grounded Q&A | `question(expects="box")` | Same question, model returns boxes with answers |
| Counting | `question()` | `How many {objects} are there? Point to each.` |

## Vision Hints (System Message)

Add hints to the system message to optimize model behavior for spatial tasks:

| Hint | Output Type | Use Case |
|------|------------|----------|
| `<hint>BOX</hint>` | Bounding boxes | Object detection, region selection |
| `<hint>POINT</hint>` | Single points | Pointing, counting |
| `<hint>POLYGON</hint>` | Polygons | Segmentation, irregular shapes |
| `<hint>THINK</hint>` | Reasoning traces | Chain-of-thought, complex analysis |

### Example: Requesting boxes with hints
```python
from perceptron import perceive, image, text, system

@perceive(expects="box")
def find_people(img_path):
    return [system("<hint>BOX</hint>"), image(img_path), text("Find every person in this scene.")]

result = find_people("photo.jpg")
```

## Prompting Tips

- **Be explicit about output format** — specify text, points, boxes, or polygons
- **Use concise, direct prompts** — trim verbosity for better results
- **Ask for rationale** when you need the model to explain reasoning
- **Supply multiple images** when in-context examples are useful
- **Tighten language** for single- vs. multi-target pointing
- **Use temperature 0.0** for deterministic, repeatable outputs

### Detection Prompts

- General: `"Your goal is to segment out the objects in the scene"`
- Targeted: `"Bound the {objects}"` (e.g. "Bound the homes")
- Attribute-based: `"Bound the blue books"` or `"Find the person in a yellow vest"`
- Counting: `"How many boxes are there?"` with expects=point
