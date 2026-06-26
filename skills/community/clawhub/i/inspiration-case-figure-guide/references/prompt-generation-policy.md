# Prompt Generation Policy

## Prompt Construction Order

1. Figure thesis: one sentence answering "why is this paper needed?"
2. Paper slot and audience.
3. Inspiration source: motivating case, observation, failure, contrast, scenario, taxonomy, or mechanism.
4. Canvas and layout.
5. Panel choreography and reading order.
6. Required objects, actors, modules, states, evidence items, or examples.
7. Exact label strategy.
8. Visual rhetoric and style family.
9. Color semantics.
10. Sample/reference-image transfer rules.
11. Negative constraints.
12. Candidate count and varied axis.

## Candidate-Board Prompt Boundary

Generated skills must distinguish two prompt types:

- **P4 candidate-board brief:** low-commitment visual comparison for choosing direction after text candidates.
- **P7 final image brief:** formal prompt for the selected direction after the user has reviewed and locked/revised a visual candidate.

Do not use the final image brief as a substitute for the candidate-board step.

## Candidate-Board Setup Template

```text
Board purpose:
Generate candidate images or schematic candidates for choosing an inspiration-figure direction, not a final figure.

Candidate count:
<4/5/6; default 6>

Hold fixed:
<paper thesis, target slot, exact case evidence, required labels, color semantics, sample-image transfer rules>

Vary only:
<subtype / scheme / layout / style / metaphor / density / prompt framing>

Compare:
<what the user should choose by looking at the images>

Rendering route:
ChatGPT web: Create image through ChatGPT Images 2.0.
Codex: $imagegen first; if unavailable, ChatGPT Images 2.0 API or another approved image-generation API.
```

The setup turn is `TEXT_ONLY` and must stop before generation.

## Final Image Brief Template

```text
Create a publication-ready scientific inspiration figure for a research paper.

Goal / figure thesis:
<one sentence answering why the paper is needed>

Paper slot and audience:
<introduction / method lead-in / analysis / limitation / rebuttal / slides>

Inspiration source:
<case, observation, failure, before/after contrast, scenario, taxonomy gap, or mechanism intuition>

Canvas and layout:
<aspect ratio, panel count, reading order>

Panel content:
Panel A: ...
Panel B: ...
Panel C: ...

Evidence anchors:
Use only these supplied case facts / observations / metrics / qualitative outputs: <list>.

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

## Rendering Route

Candidate boards, draft candidates, final visuals, and revisions must use native image generation:

1. ChatGPT web: Create image through ChatGPT Images 2.0.
2. Codex: `$imagegen` first.
3. Codex fallback: ChatGPT Images 2.0 API or another approved image-generation API.

Allowed bitmap outputs from that route: PNG, JPG, JPEG, WebP.

Forbidden visual outputs/fallbacks: SVG, Mermaid, TikZ, Graphviz, HTML/CSS diagrams, canvas diagrams, matplotlib/code-generated figures, filesystem image exports produced by local code or scripts.

If image generation is unavailable, stop and provide a prompt handoff. Do not substitute code-rendered figures.
