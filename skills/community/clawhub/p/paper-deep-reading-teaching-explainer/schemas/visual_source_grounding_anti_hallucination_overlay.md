# Visual Source-Grounding Anti-Hallucination Overlay

Use this overlay whenever the workflow writes image prompts in text, directly generates storyboard images, revises generated images, or prepares images for final PDF assembly.

## Principle

The cartoon storyboard is a teaching layer over the paper, not a place to invent paper content. Every paper-specific visual element must respect:

1. the original paper sources: PDF, LaTeX, appendix, figures, tables, equations, captions, and nearby text;
2. the authoritative deep-reading report produced earlier by this skill;
3. the factual-status labels already used in the report.

The original paper has priority over the report. If the report and original paper disagree, do not silently choose the more convenient version. Prefer the original paper, flag the conflict, and keep the image prompt conservative.

## Before Writing Image Prompts

Run this check before writing prompt-only handoffs or calling an image-generation tool:

- List the paper-specific facts that will appear visually: module names, variables, equations, tensor shapes, datasets, label definitions, baselines, metrics, numeric results, limitations, and claims.
- For each fact, map it to one of:
  - `paper-stated`: directly from PDF/LaTeX/report with source grounding;
  - `report-derived`: from the authoritative report and traceable to source evidence;
  - `reasonable inference`: plausible from the paper but not explicitly stated;
  - `nearby-work inference`: borrowed from similar work, must be labeled;
  - `missing / not reported`: needed but absent.
- Remove or relabel unsupported facts before prompt handoff.
- If a missing detail matters for correctness, ask the user for the source or mark it as `未报告` / `not reported`.

## Prompt Handoff Checklist

For text answers that provide image-generation prompts, include a compact visible checklist:

```text
Anti-hallucination check
- Original paper checked: yes
- Authoritative deep-reading report checked: yes
- Unsupported facts: removed or marked not reported
- Paper/report conflicts: none / listed
- Image prompts contain only source-grounded or explicitly labeled inferred content
```

Do not include long audit tables unless the user asks. The checklist is meant to keep the image-generation step honest without burying the prompt.

## Direct Image Generation Check

If the assistant directly generates images:

1. Verify the prompt before generation using the same source-grounding check.
2. After generation, inspect the image text and visible logic.
3. Reject, revise, or regenerate images that contain:
   - invented equations, variables, datasets, baselines, or metrics;
   - unsupported numbers, ranks, performance gains, hardware, runtime, or hyperparameters;
   - wrong module names or data-flow arrows;
   - visual claims stronger than the paper/report;
   - inconsistent factual-status labels;
   - missing details drawn as if they were known.

Do not move a suspect image into final PDF assembly. Keep it in a revise/regenerate state until corrected.

## Allowed Simplification

Cartoons may simplify, metaphorize, or compress the explanation, but they must not change the technical claim.

Acceptable:

- a toy example clearly labeled as illustrative;
- icons for data, modules, metrics, or limitations;
- simplified chart highlights that preserve the actual trend;
- a visual metaphor that makes a stated mechanism easier to understand.

Not acceptable:

- inventing a training pipeline step absent from the paper/report;
- inventing GPU type, runtime, seed, split, or baseline implementation details;
- turning a weak or partial result into a decisive victory;
- drawing a causal mechanism that the paper only correlates;
- making the follow-up research direction look like a validated paper result.
