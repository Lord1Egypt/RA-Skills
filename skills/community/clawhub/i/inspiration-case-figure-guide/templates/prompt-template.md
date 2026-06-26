# Prompt Template

## Candidate Board Prompt

```text
Generate 6 candidate images or schematic candidates for choosing the visual direction of a research-paper inspiration figure. This is not the final figure.

Figure thesis:
<one sentence: why the paper is needed>

Target slot:
<introduction / method lead-in / analysis / limitation / rebuttal / slides>

Hold fixed:
<paper thesis, exact case facts, evidence anchors, required labels, color semantics, reference-image transfer rules>

Vary only:
<subtype / layout / style / metaphor / density / prompt framing>

Candidate mapping:
C1: ...
C2: ...
C3: ...
C4: ...
C5: ...
C6: ...

Visual constraints:
Publication-ready scientific figure, compact labels, clear reading order, no long paragraphs.

Avoid:
Invented examples, fake metrics, fake screenshots, logos, watermarks, decorative clutter, SVG/Mermaid/TikZ/Graphviz/code-rendered diagram instructions.
```

## Final Image Prompt

```text
Create a publication-ready scientific inspiration figure for a research paper.

Goal / figure thesis:
<one sentence answering why the paper is needed>

Paper slot and audience:
<introduction / method lead-in / analysis / limitation / rebuttal / slides>

Inspiration source:
<motivating case, failure, observation, before/after contrast, scenario, taxonomy gap, mechanism intuition, or evidence board>

Canvas and layout:
<aspect ratio, panel count, reading order>

Panel content:
Panel A: ...
Panel B: ...
Panel C: ...

Evidence anchors:
Use only these supplied facts, observations, metrics, or qualitative outputs: <list>.

Labels:
Use only these exact short labels: <list>.

Sample-image transfer:
<per-image attributes to borrow, or none>

Style and color semantics:
<style family, palette role, what each color means>

Candidate variation:
Generate <4/5/6> candidates, usually 6. Vary only <axis>.

Avoid:
invented examples, fake metrics, fake screenshots, long paragraphs, unreadable labels, logos, watermarks, decorative clutter, SVG/Mermaid/TikZ/Graphviz/code-rendered diagram instructions.
```
