---
name: marp-slides
description: Turn docs, notes, data, logs, screenshots, and code summaries into polished Marp slide decks.
homepage: https://marp.app
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["marp"] }, "install": [{ "id": "node-marp", "kind": "node", "package": "@marp-team/marp-cli", "bins": ["marp"], "label": "Install Marp CLI (node)" }] } }
---

# Marp Slide Show/Deck Generator

## Overview

Generate polished Marp slide decks from raw source material, then render them into the format the user wants. Focus on turning notes, data, and mixed inputs into a presentation with a clear takeaway, not a transcript dump.

If the user does not specify an output format, default to a rendered `.html` slideshow and also keep the `.slides.md` source deck.

## Input Scope

This skill should work from almost any information that can be summarized into a presentation, including:

- notes, docs, reports, and memos
- tables, CSV, JSON, YAML, and metrics
- logs, transcripts, timelines, and research notes
- architecture docs, design docs, plans, and RFCs
- code snippets, API descriptions, and technical change summaries
- screenshots, images, and mixed structured + unstructured inputs

## Workflow

1. Identify the audience, purpose, and takeaway.
2. Determine the requested output format from the user prompt, target filename, or explicit extension.
3. If no format is specified, default to `.html`.
4. Classify the input: numeric data, tabular data, text notes, logs, timeline, comparison, screenshots, code summary, or mixed.
5. Extract the few facts that matter most.
6. Choose a slide arc: title, context, key insights, supporting visuals, recommendation, close.
7. Build the source deck as Marp markdown, typically named `*.slides.md`.
8. Add visual structure with charts, diagrams, timelines, callouts, and section slides where useful.
9. Render the deck into the requested format with the installed `marp` CLI.
10. Verify the rendered deck in its target aspect ratio and confirm that no slide content is cropped or vertically cut off.

## Output Rules

- Accept any source material that can be turned into a coherent presentation.
- Supported rendered outputs are `.html` (default), `.pdf`, `.pptx`, notes text, single-slide `.png` / `.jpeg`, and multi-slide image export.
- Unless the user explicitly asks for markdown only, produce a rendered artifact.
- If the user does not specify a format, render `.html` by default.
- Keep the Marp source deck as `*.slides.md` when rendering to another format.
- If the user asks for multiple formats, render all requested formats from the same `*.slides.md` source.
- If the user asks for an unsupported format, ask one short question or offer the closest supported option.
- Use direct `marp` CLI commands for rendering.
- Use a strong title slide, then 4 to 8 content slides by default.
- Keep one idea per slide.
- Convert tables into short bullets or focused comparison slides when possible.
- Use numbers, percentages, trends, and deltas instead of vague summaries.
- Prefer short headers, short bullets, and purposeful whitespace.
- Include speaker-friendly structure if the user wants notes.
- If a slide is close to overflowing, split it into two slides instead of shrinking it until it becomes hard to read.
- Avoid combining large tables, multi-card layouts, and large callouts on the same slide unless you have confirmed the rendered slide still fits.

## Visual Patterns

- Use `mermaid` for flows, timelines, funnels, and simple system diagrams.
- Use comparison tables only when they improve readability.
- Use callout boxes for key takeaways.
- Use section divider slides for long decks.
- Use a consistent palette and avoid clutter.
- Favor simple, high-contrast layouts over dense decoration.

## Deck Shape

- Title slide
- Context slide
- Insight slides
- Visual proof slides
- Recommendation or summary slide
- Optional appendix

## Quality Check

- Does the deck answer the user’s question fast?
- Is each slide visually scannable?
- Are the main numbers and conclusions obvious?
- Does the deck feel designed, not auto-generated?
- Does every rendered slide fit fully in-frame with no clipped bottom content or hidden overflow?

## Resources

See `references/slide-patterns.md` for slide archetypes, visual rules, and mapping guidance.

See `references/output-formats.md` for supported output formats, default behavior, and render commands.

### references/
Use references for reusable guidance on slide structure and visual decisions.

### assets/
No bundled assets are required for this skill.

---

Keep the deck concise, visual, and specific.
