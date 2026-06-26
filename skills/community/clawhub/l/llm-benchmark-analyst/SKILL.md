---
name: llm-benchmark-analyst
description: search and analyze llm benchmark results within a fixed benchmark universe, then produce evidence-based model strength and weakness reports or domain-leader summaries. use when comparing a model across benchmarks, ranking the best models by domain, explaining what a benchmark measures, checking predecessor-vs-current progress, or writing benchmark reports that must prioritize exact model version, evaluation date, benchmark variant, score semantics, sub-scores, and benchmark defect warnings. works with browser, web, and multimodal extraction for text, table, canvas, or image-only leaderboards.
---

# LLM Benchmark Analyst

## Overview
Use this skill to research benchmark evidence and write structured reports about:
1. a single model's strengths and weaknesses
2. best models in a capability domain
3. what a benchmark measures and how trustworthy it is
4. predecessor vs current-model progress

Default to the user's language. Never invent scores, ranks, dates, benchmark variants, or missing table values.

## Core constraints
- Restrict the benchmark universe to `references/benchmark-source.md`. If a benchmark is not in that file, exclude it.
- Use `references/core-dimensions.md` to collapse scattered benchmarks into a small set of report dimensions.
- Follow `references/search-playbook.md` for routing, overlap expansion, evidence gathering, and comparison anchors.
- Follow `references/report-template.md` for output structure.
- Apply `references/data-defect-warnings.md` benchmark by benchmark, inline and again in the limitations section.
- Prefer official benchmark or benchmark-author pages. Use aggregators mainly to discover links and context.
- Record the evaluation mode exactly: benchmark version, split, difficulty, public/private, verified/original, with-tools/without-tools, pass@k, and any visible sub-score names.
- Keep score units exact. Do not average incompatible metrics into a fake composite.

## Required workflow
1. **Normalize the model identity before searching**
   - Resolve exact provider, family, generation, version suffix, and release label.
   - Put time and version first. Reject ambiguous aliases like `claude`, `gemini pro`, `gpt latest`, or `qwen max` until you have the exact currently relevant model string for the searched leaderboard rows.
   - Capture the evaluation time point or access date for every key score.

2. **Route the request through core dimensions before web crawling**
   - Start with `references/core-dimensions.md` to select the primary dimension(s).
   - Then list candidate benchmarks inside those dimensions.
   - Only then start website-by-website retrieval.
   - Keep the first pass narrow and token-efficient: start from the best 3-6 benchmarks for the asked domain, then expand only if needed.

3. **Expand beyond section labels**
   - Do not let the source document's headings blind you.
   - After selecting the primary dimension, inspect benchmark descriptions and overlap tags to find relevant benchmarks that live in other sections.
   - Example: a coding analysis may need coding benchmarks, agentic coding benchmarks, general benchmarks with coding components, and research/math benchmarks with strong code components.
   - Example: a multimodal analysis may need vision benchmarks, OCR, GUI/computer-use, multimodal deep-research, and omni/video/audio benchmarks.

4. **Collect evidence in this order**
   - official leaderboard or benchmark site
   - benchmark paper or benchmark README
   - benchmark-author blog or release note
   - trusted aggregator
   - vendor blog only as secondary evidence, clearly labeled as vendor-reported if no independent leaderboard row exists

5. **Use multimodal extraction when the leaderboard is not machine-readable**
   - If the page uses images, canvas, screenshots, or chart-only rendering and plain text extraction misses the table, inspect screenshots or page images.
   - Extract only values that are clearly visible.
   - Mark the provenance as `image-extracted`.
   - If the image is unreadable or partially occluded, say so instead of guessing.

6. **Apply anchor comparisons**
   - For code or agentic coding, compare against the latest available Claude Opus, latest Claude Sonnet, and latest GPT family model.
   - For multimodal analysis, compare against the latest available Gemini model. Add the latest GPT multimodal model if relevant.
   - For intelligence or reasoning analysis, compare against the latest available GPT family model.
   - Never assume which model is currently `latest`. Search that first.

7. **Apply predecessor comparison**
   - If data exists, compare the target model with its immediate predecessor or last broadly comparable prior generation from the same provider/family.
   - Only compare like-for-like benchmark variants. If the predecessor only appears under a different benchmark mode, say the comparison is not clean.

8. **Attach defect warnings**
   - Any benchmark with a known quality or methodology issue must carry an inline warning from `references/data-defect-warnings.md`.
   - If the report's conclusion depends heavily on warned benchmarks, lower confidence and say so explicitly.

## Decision rules
- When the user asks for `best models in a domain`, do not use only one benchmark. Use a cluster of relevant benchmarks and explain why each one matters.
- When the user asks for `what is this model good or bad at`, synthesize at the core-dimension level first, then support with benchmark evidence.
- When benchmark scores conflict, prefer freshness, exact version match, official source quality, and the number of agreeing benchmarks over one standout score.
- Treat very small gaps as non-decisive when the benchmark is noisy, image-extracted, or known to be unstable.
- Always include one short clause describing what each benchmark actually tests.

## Minimum evidence to capture
For every benchmark you cite, capture:
- benchmark name
- what it tests in one short phrase
- exact model row name
- exact score and unit
- rank or relative placement if visible
- benchmark variant, split, or mode
- date or access time point
- source quality note if not official
- data warning if applicable

## Output expectations
Use the matching template in `references/report-template.md`.

At minimum, every substantive report must include:
- a scope and identity section
- a short executive summary
- strengths
- weaknesses or gaps
- evidence table
- comparison section
- data-defect warnings and confidence
- methodology or exclusions

## Resource map
- `references/core-dimensions.md`: benchmark routing and de-fragmentation map
- `references/search-playbook.md`: token-efficient search order, overlap expansion, and comparison rules
- `references/data-defect-warnings.md`: warning catalog and ready-to-use caution language
- `references/report-template.md`: output structures for single-model, domain-leader, and benchmark-explainer tasks
- `references/benchmark-source.md`: full allowed benchmark universe copied from the user's benchmark document

## Example tasks
- `analyze gpt-5's coding and agentic coding strengths and weaknesses, and compare it with the latest claude opus, claude sonnet, and gpt model`
- `find the best multimodal models right now using only the approved benchmark list and explain each benchmark briefly`
- `write a report on qwen's reasoning strengths, benchmark gaps, predecessor comparison, and all data-quality caveats`
- `tell me which models lead in deep research and search, with benchmark-specific warnings and freshness notes`
