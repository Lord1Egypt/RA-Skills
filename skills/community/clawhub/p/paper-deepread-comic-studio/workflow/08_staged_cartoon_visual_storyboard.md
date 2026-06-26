# Workflow 08 — Staged Cartoon Visual Storyboard Generation

This workflow is optional and starts **only after** the authoritative detailed report has been delivered.

## Separation rule

Text report and image generation must not happen in the same assistant turn.

- Step 0: text-only plan + complete deep-reading report + status + next-step prompts.
- Step 1+: one visual storyboard part per user request, generated as multiple separate continuous cartoon images/cards.
- Final assembly is a separate PDF-packaging step and must not generate new images.

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

## Multi-image prompt contract

Whenever a text reply writes a prompt for continuous cartoon generation:

- Require **multiple separate 16:9 images/cards**, ordered as `第1张`, `第2张`, and so on.
- Split different paper parts into different images or batches. Do not compress background, method, experiments, limitations, and future directions into one image.
- Add camera direction for the sequence: establishing shot, medium shot, close-up, zoom-in, pan, cutaway, transition, or final recap as appropriate.
- Preserve a style bible: same protagonist/narrator, color palette, line style, typography, icon language, panel numbering, source tags, and formula/table rendering style.
- For later batches, reuse earlier visual continuity. If earlier images are not in context, restate the last known style and avoid inventing factual continuity.
- Check every paper-specific number, dataset, module, equation, baseline, figure, claim, and limitation against the original PDF/LaTeX and the authoritative report before prompting.
- Mark evidence strength in prompt notes when needed: `paper-explicit`, `report-derived`, `reasonable inference`, `nearby-work inference`, or `missing / not reported`.
- Keep each image teachable: one main idea, readable labels, limited text, clear source grounding, and no unsupported visual claims.

## Default visual steps

1. Background, old-method defects, paper problem, inspiration.
2. Algorithm overview and module-by-module flow.
3. Experiment section: datasets, baselines, metrics, results, ablations, qualitative plots, reproducibility gaps.
4. Limitations and defense / reviewer-QA visuals.
5. Future directions and innovation graph visuals.
6. Cover, summary, and Q&A backup visuals.
7. Final image-PDF assembly: combine all approved storyboard images into one 16:9 PDF. See `workflow/09_storyboard_pdf_assembly.md`.

## Step output expectations

For each visual step, generate a coherent set of 16:9 cartoon-comic images with:

- consistent protagonist / narrator;
- consistent visual style, colors, icon language, panel numbering, and typography;
- clear continuity, camera movement, and left-to-right logic;
- paper-grounded data, equations, tables, or qualitative claims where relevant;
- no unsupported claims beyond the paper/report evidence.

## Stateless prompt reminder

At the end of each text-only status turn, tell the user:

`如果开启新会话或上下文丢失，请说：使用这个skill，根据状态，执行第X步：生成多张连续的卡通图，...。如果不知道下一步怎么问，可以说：使用这个skill，根据状态，告知下一步应该问什么。`
