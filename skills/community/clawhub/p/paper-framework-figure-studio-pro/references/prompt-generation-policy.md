# Prompt Generation Policy

Version: 1.2.0

## Prompt Types

This skill uses two prompt stages:

- **P4 candidate-board brief:** low-commitment board for choosing a direction after text candidates.
- **P7 final image brief:** formal prompt for the selected direction after P6 candidate review.

Do not use P7 as a substitute for P4/P5/P6. After 4-6 text candidates, the candidate-board bridge must happen unless explicitly skipped by the user.

## Candidate-Board Brief

```text
Board purpose:
Generate candidate images or schematic candidates for choosing a framework-figure direction, not a final figure.

Candidate count:
6 by default, allowed 4-6.

Hold fixed:
<paper thesis, target slot, required modules, exact labels, color semantics, sample-image transfer rules>

Vary only:
<subtype / scheme / layout / style / metaphor / density / prompt framing>

Compare:
<what the user should decide by looking at the images>

Rendering route:
ChatGPT web: Create image through ChatGPT Images 2.0.
Codex: $imagegen first; if unavailable, ChatGPT Images 2.0 API or another approved image-generation API.
```

## Final Image Brief

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

Style and color semantics:
<style, palette, what colors mean>

Candidate variation:
Generate <4/5/6> candidates, usually 6. Vary only <axis>.

Avoid:
long paragraphs, microscopic labels, fake metrics, fake UI, logos, watermarks, decorative clutter, SVG/Mermaid/TikZ/Graphviz/code-rendered diagram instructions.
```

## Rendering Route

- ChatGPT web: use Create image through ChatGPT Images 2.0.
- Codex: use `$imagegen` first.
- Codex fallback: ChatGPT Images 2.0 API or another approved image-generation API.

Allowed bitmap outputs: PNG, JPG, JPEG, WebP.

Forbidden visual outputs/fallbacks: SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, filesystem code drawing, or code-rendered/exported images.
