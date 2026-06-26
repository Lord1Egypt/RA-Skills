# Workflow 08 — Staged Cartoon Visual Storyboard Generation

This workflow is optional and starts **only after** the authoritative detailed report has been delivered.

## Separation rule

Text report and image generation must not happen in the same assistant turn.

- Step 0: text-only plan + complete deep-reading report + status + next-step prompts.
- Step 1+: one visual storyboard part per user request.
- Final assembly is a separate PDF-packaging step and must not generate new images.

## Multi-image decomposition rule

Each visual part should be generated as a sequence of multiple 16:9 cartoon images, not compressed into a single overloaded image. The default output for a section is a coherent image batch with one prompt per image.

Do not merge different visual parts into one image:

- background / old-method defects / motivation;
- algorithm overview;
- module internals and data flow;
- training and inference;
- experiments, metrics, baselines, and results;
- limitations and defense;
- future directions;
- cover, summary, and backup Q&A.

If the user asks for a single image, treat it as a compact overview only. State that the recommended mode remains a multi-image sequence, because dense paper explanations need separate shots for readability, evidence checking, and later PDF assembly.

## Platform guidance

In a text-only planning/status turn before image generation, tell the user:

- ChatGPT 网页版 / App: use **Create image**.
- Do not generate SVG diagrams for the cartoon storyboard.
- Codex / Claude Code / coding-agent environments: prefer the `imagegen` skill when it is available. If `imagegen` is unavailable or insufficient, call **ChatGPT Images 2.0 API** or another available image-generation API.

## Source basis for storyboard generation

Storyboard image generation can be based on **PDF**, **LaTeX source**, or both. Make this explicit in the planning/status text when relevant.

Use the following priority rules:

1. **PDF-only input**: use rendered pages, figure/table positions, visible diagrams, captions, axes, numeric tables, and nearby text.
2. **LaTeX-only input**: use `figure`/`table` environments, captions, labels, `\includegraphics` paths, equations, section text, appendix content, and source comments when useful.
3. **PDF + LaTeX input**: cross-check both; use the PDF for rendered visual appearance and LaTeX for exact captions, labels, formulas, figure filenames, and text around visuals.
4. **Authoritative report available**: treat the report as the storyboard's primary planning anchor, but preserve traceability back to PDF/LaTeX evidence.
5. **Conflict or missing detail**: do not invent; mark the item as “PDF/LaTeX 未报告” or ask the user for the missing source in a text-only turn.

Every storyboard step should state, internally or in a visible planning note, which source basis it is using: `PDF`, `LaTeX`, `PDF+LaTeX`, or `report-derived from PDF/LaTeX`.

When factual status matters, label content as one of:

- `paper-stated`
- `reasonable inference from this paper`
- `nearby-work inference`
- `missing / not reported`

## Visual source-grounding anti-hallucination check

Before writing image-generation prompts or directly generating images, check the planned visual content against the original paper sources and the authoritative detailed report.

Required checks:

- every module name, variable, formula, tensor shape, dataset, metric, baseline, numeric result, limitation, and claim in the prompt has a source in the PDF, LaTeX, or authoritative report;
- if a detail appears only in the report, verify that the report ties it back to the PDF/LaTeX evidence, or label it as report-derived inference;
- if the report conflicts with the original PDF/LaTeX, prefer the original paper and flag the conflict in a text-only note;
- if a detail is needed for the cartoon but not reported, write `未报告` / `not reported` or ask the user for the missing source; do not fill it in from memory;
- visual metaphors may simplify the idea, but must not imply unsupported causal relations, performance gains, hardware, runtime, baseline fairness, or data splits.

For text-only prompt handoff, include a short visible checklist:

```text
Anti-hallucination check:
- Original paper checked: yes
- Authoritative deep-reading report checked: yes
- Unsupported or missing facts: removed / marked not reported / needs user source
- Conflicts between paper and report: none / listed above
```

After images are generated, inspect them before accepting them into the storyboard sequence. Reject or revise images that introduce invented labels, wrong equations, unsupported numeric values, incorrect arrows/data flow, unreported hardware/runtime, ungrounded performance claims, or visual conclusions not supported by the paper/report. Do not assemble such images into the final PDF until corrected.

## Continuity and cinematography contract

Whenever the assistant writes image-generation prompts in text, or directly generates a continuous batch of multiple cartoon images, include a continuity/cinematography block. This applies to every visual step, not only the first one.

Required continuity fields:

- `sequence`: image number, section title, and whether this image opens, develops, turns, or closes the section;
- `decomposition`: the single teaching point assigned to this image and why it should not be merged with adjacent images;
- `camera`: establishing / wide / medium / close-up / top-down / split-screen / over-the-shoulder / zoom-in / pan / cutaway / reveal, chosen for the teaching purpose;
- `transition`: how this image connects to the previous and next image;
- `style bible`: narrator/protagonist, line style, color palette, typography, title/footer format, panel border style, and aspect ratio;
- `symbol bible`: repeated icons, variables, arrows, module blocks, data objects, metric badges, and evidence labels;
- `logic continuity`: what prerequisite the viewer should already know and what new idea this image adds.

For follow-up batches after earlier images exist, first restate the established storyboard bible and preserve it unless the user explicitly requests a style change. Later prompts must say how the new images continue the prior story, reuse the same narrator/visual metaphors/symbol dictionary, and avoid introducing a conflicting art style, color system, or data-flow direction.

Default camera rhythm for a section:

1. Establish the problem scene or section objective.
2. Move through process shots that show data flow or conceptual change.
3. Use close-ups for formulas, module internals, key table cells, or failure cases.
4. End with a synthesis shot that bridges to the next section.

## Visual expression suitability checklist

Before finalizing cartoon prompts, check whether the images will teach the idea rather than merely decorate it:

- one main teaching point per image;
- multiple images per section by default, with separate prompts for distinct concepts;
- no compressed all-in-one poster when the content contains several modules, datasets, metrics, limitations, or equations;
- clear visual hierarchy: title, central visual, labels, evidence status, and takeaway are easy to scan;
- readable labels: short phrases, no dense paragraphs, no tiny formula walls;
- stable spatial grammar: left-to-right or top-to-bottom flow, consistent arrow meanings, no crossed or ambiguous data-flow lines;
- recurring metaphor discipline: use the same metaphor for the same concept across all images, and do not introduce a cute scene that weakens technical precision;
- evidence honesty: paper facts, reasonable inferences, nearby-work inferences, and missing details remain visibly distinct;
- cognitive pacing: difficult equations or modules get a setup image before a close-up explanation;
- experiment clarity: charts/tables should highlight metric meaning, baseline source, exception cases, and reproduction risks rather than only showing winner/loser bars;
- accessibility: high contrast, color is not the only carrier of meaning, and text remains legible in a 16:9 slide/PDF;
- PDF assembly readiness: consistent margins, page numbers, title band, and safe area so later PDF pages do not feel like unrelated images.

## Default visual steps

1. Background, old-method defects, paper problem, inspiration.
2. Algorithm overview and module-by-module flow: include symbols, input/output, dimensions, trainable parameters, fixed hyperparameters, data flow, training, inference, and a small numeric walkthrough where useful.
3. Experiment section: datasets, label definitions, splits, baseline provenance, whether baselines are rerun/reimplemented, metrics, results, exceptions, ablations, qualitative plots, and reproducibility gaps.
4. Limitations and defense / reviewer-QA visuals.
5. Future directions and innovation graph visuals.
6. Cover, summary, and Q&A backup visuals.
7. Final image-PDF assembly: combine all approved storyboard images into one 16:9 PDF. See `workflow/09_storyboard_pdf_assembly.md`.

## Step output expectations

For each visual step, generate a coherent set of 16:9 cartoon-comic images with:

- multiple images by default, one prompt per image;
- consistent protagonist / narrator;
- consistent visual style, colors, icon language, panel numbering, and typography;
- clear continuity, camera progression, transitions, and left-to-right or top-to-bottom logic;
- paper-grounded data, equations, tables, or qualitative claims where relevant;
- knowledge dependency order: symbols before data, data before model, model before training/inference, training/inference before experiments;
- key concepts shown as intuition -> formula -> concrete example -> limitation when space permits;
- complex modules shown with inputs, outputs, symbols, dimensions, parameters, and data flow when available;
- missing experiment details shown explicitly as "not reported" rather than visually invented;
- no unsupported claims beyond the paper/report evidence;
- a compact continuity block in every prompt batch, especially when only text prompts are being handed to the user for later image generation;
- a source-grounding anti-hallucination checklist before prompt handoff and an image-inspection pass before PDF assembly;
- no attempt to pack a whole section into a single crowded collage.

## Stateless prompt reminder

At the end of each text-only status turn, tell the user:

`如果开启新会话或上下文丢失，并且要继续生图，请说：使用这个skill，根据状态，执行第X步：生成多张连续的卡通图，内容是...。如果不知道下一步怎么问，可以说：使用这个skill，根据状态，告知下一步应该问什么。`
