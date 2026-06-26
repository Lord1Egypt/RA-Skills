# Prompt Template

Use this template only after P6 has recorded/reviewed a candidate image board and the user has selected or accepted a visual direction.

```text
Create a publication-ready research-paper framework diagram as a raster image.

Goal:
<figure thesis>

Paper slot and audience:
<slot and audience>

Diagram subtype and layout:
<subtype, canvas, panel count, reading order>

Required content:
<modules/entities/stages/evidence>

Labels:
Use only these exact labels: <labels>.

Sample-image transfer:
<per-image transfer rules or "none">

Rendering route:
ChatGPT web should use Create image through ChatGPT Images 2.0.
Codex should use $imagegen first; if unavailable, use ChatGPT Images 2.0 API or another approved image-generation API.

Response boundary:
If this prompt is shown in a TEXT_ONLY reply, stop before image generation. Generate candidates only in a later IMAGE_ONLY response after user confirmation.

Style and color semantics:
<style, palette, what colors mean>

Candidate variation:
Generate <4/5/6> candidates, usually 6. Vary only <axis>.

Avoid:
long paragraphs, microscopic labels, fake metrics, fake UI, logos, watermarks, decorative clutter, SVG/Mermaid/TikZ/Graphviz/code-rendered diagram instructions.
```
