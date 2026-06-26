---
name: maus-html-summary
description: Turn articles, transcripts, long posts, and raw text into a self-contained illustrated HTML explainer with simple language, memorable structure, source-grounded extraction, and explanatory SVG metaphors. Inspired by the German show "Die Sendung mit der Maus": make dense content easy to learn and remember.
---

# Maus HTML Summary

Turn a source text (article, transcript, talk, long post, raw text) into
one self-contained HTML page that explains it with the clarity of a
children's science show for adults: friendly, concrete, visual,
source-faithful, and easy to remember.

The name references "Die Sendung mit der Maus", a German educational TV
show known for explaining complex topics in simple visual steps. Outputs
should be internationally understandable; do not assume the reader knows
the show.

## Goal

A single self-contained HTML page that is:

- easy to scan
- visually illustrated with real explanatory SVGs (not decorative icons)
- plain-language but substantively concrete
- faithful to the source and honest about what was left out
- memorable through metaphor and clear hierarchy

The tone is "clear science explainer for adults": friendly, concrete,
slightly playful, never childish, never vague.

## The non-negotiable workflow

These seven stages run in order, every time. Skipping a stage produces
shallow or hallucinated output. Reproducibility is the audit (Stage 7)
catching what earlier stages missed.

### Stage 1 - Internal extraction (no output yet)

Read the source. Build a short internal notes block. It never appears in
the HTML; it is the only material allowed in the HTML.

Capture four buckets:

- **Facts** - numbers, dates, names, places, technical terms
- **Mechanisms** - how things work: concrete steps, cause -> effect, before/after
- **Examples** - specific cases mentioned in the source
- **Source claims** - what the source explicitly argues or shows

Anti-hallucination rule: if a claim is not in this list, it cannot
appear in the HTML.

### Stage 2 - Plan hierarchy

Count source words. Pick main-idea count by size:

- **< 500 words** (short transcript snippet, social post): **3** main ideas
- **500-2000 words** (article, talk excerpt): **4** main ideas
- **2000+ words** (long article, full transcript): **5-6** main ideas

For transcripts: first mentally filter filler words, false starts,
hesitations, repetition. Extract from the cleaned signal, not the raw
text.

For each main idea, plan **2-4 sub-points**. Sub-points are where
concreteness lives.

Identify the **one-sentence core message**; this becomes the hero.

### Stage 3 - Pick an SVG metaphor per main idea

Every main idea carries exactly one explanatory SVG. Pick from this
catalog:

- **Layer stack** - layered concepts, abstraction levels, stacked components
- **Pipeline / conveyor belt** - sequential processes, transformations, flows
- **Cross-section** - what is inside something: anatomy, internals, structure
- **Before / after** - change, transformation, improvement
- **Node graph** - networks, relationships, dependencies, hubs
- **Funnel** - filtering, narrowing, conversion
- **Growth curve** - growth, decay, trends over time
- **Circuit / logic flow** - logical wiring, if/then chains, branching flow

Use the skeleton SVGs in [svg-patterns.md](./svg-patterns.md) as the
geometric base. Adapt labels, colors, element count to the specific
content. Never copy-paste verbatim.

If none of the metaphors fit a given idea, the idea is probably too
abstract to stand alone. Fold it into another idea.

Decorative emoji or icons are not SVG metaphors. A row of generic symbols
does not satisfy the SVG requirement.

### Stage 4 - Draft sections

Build the HTML around this arc:

1. **Hero / What is this about?** - the one-sentence core message plus a 1-2 sentence lead.
2. **Main ideas section** - 3-6 cards (per Stage 2), each with:
   - Headline
   - SVG metaphor (from Stage 3, adapted from svg-patterns.md)
   - 2-4 sub-points (each passing the concreteness check in Stage 5)
3. **Why it matters** - one box, the broader significance as stated in the source.
4. **What we left out** - honesty box: **2-4 things** from the source that were intentionally omitted, each with a one-line reason ("too technical for this format", "side path not tied to the core message", "redundant with idea 2", ...).
5. **Memory hook** - one memorable sentence, readable aloud in under 5 seconds.
6. **If you only remember 3 things** - exactly three bullets, the absolute minimum take-away.

### Stage 5 - Concreteness check per sub-point

Every sub-point must contain **at least one** of:

- a **number** (count, percentage, duration, threshold, version)
- a **proper noun** (product, person, company, technology, place)
- a **concrete example** (a specific case from the source)
- a **mechanism step** (how it works, not just that it works)

If a sub-point has none of these, it is too vague. Rewrite it using
material from the Stage 1 extraction notes, or remove it.

Vague-by-default phrases that signal a failed sub-point:

- "improves efficiency"
- "plays an important role"
- "enables new possibilities"
- "is an important aspect"
- "contributes to ..."
- "is significant"

If you catch yourself writing any of these, you're describing the
existence of a thing instead of explaining it. Go back to the extraction
notes and pull a fact, name, example, or step.

### Stage 6 - Render HTML

Write one complete, self-contained HTML document:

- All CSS inline in `<style>`
- All SVGs inline
- No external scripts, fonts, images, fetches, or `<link>` tags
- Mobile-friendly (verify mental layout at 360 px width)
- Strong visual hierarchy: hero -> idea cards -> significance -> honesty -> memorable closing
- Rounded shapes, warm muted palette, soft shadows, light borders
- Hierarchy through size, weight, and color; not through heavy lines

### Stage 7 - Pre-emit audit (the reproducibility gate)

Before delivering, walk this checklist mentally. Any failed item must be
fixed before emitting.

```text
[ ] Every sub-point contains a number, proper noun, concrete example,
    or mechanism step (Stage 5 rule)
[ ] Every main idea has exactly one explanatory SVG drawn from the
    catalog, adapted from svg-patterns.md; not a decorative icon
[ ] The "What we left out" box names at least 2 specific things from the
    source that were left out, each with a one-line reason
[ ] No fact in the output is missing from the Stage 1 extraction notes
    (no hallucinations)
[ ] The memory hook reads aloud in under 5 seconds
[ ] The "If you only remember 3 things" box has exactly 3 items
[ ] HTML is self-contained: no <script>, no <link rel="stylesheet">,
    no <img src="http...">, no external font URLs
```

The audit is the difference between consistent and inconsistent output.
Don't skip it. Don't treat it as a wish list. It is a checklist.

## Writing rules

- Use the source language by default. If the user or audience context
  indicates English, use English.
- Concreteness over brevity. If forced to choose between "short and
  vague" and "two sentences and concrete", pick concrete.
- Explain jargon once, then drop it.
- One narrative thread per main idea; don't mix topics inside one card.
- Short paragraphs, but use lists where lists fit naturally (steps,
  ingredients, options).
- Avoid long quotations. Summarize.

## HTML rules

- One complete document, self-contained, no external dependencies.
- Mobile-first layout, generous padding.
- Warm muted palette, but keep it globally readable and not region-specific.
- Rounded corners, soft shadows.
- Hierarchy via size, weight, color; not via heavy lines or borders.

## When the source is unclear

If the source is genuinely ambiguous about a point, say so in the output
inside the relevant card or in the "What we left out" box. Never invent
details to fill space.

## Resources

- [svg-patterns.md](./svg-patterns.md) - skeleton SVGs for the eight
  metaphor types in Stage 3. Use as geometric base, adapt content.
