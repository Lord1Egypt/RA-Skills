---
name: journal-club-slides
description: "Use when building journal club or literature-report slides from research PDFs and you need a figure-first, audience-facing, visually polished deck that preserves paper logic, keeps crops safe, pairs main and supporting evidence correctly, and passes render-based QA."
version: 2.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [productivity, powerpoint, journal-club, literature-review, academic-presentations, paper-ppt, bilingual, figure-integrity, visual-design]
    related_skills: [powerpoint, ocr-and-documents, paper-journal-club-ppt]
---

# Journal Club Slides

## Overview

Use this skill to turn one or more research-paper PDFs into presentation-ready journal club or literature-report slides.

The standard is not "extract paper content into PPT". The standard is to produce a deck that is:
- faithful to the paper's argument
- optimized for live speaking
- visually strong enough to present directly
- figure-first rather than text-first
- grounded in real main and supporting evidence
- verified in rendered output, not just in source form

This skill is intentionally strict because paper decks often fail in predictable ways: wrong figure pairing, unsafe crops, unreadable support images, creator-facing labels, visually weak layouts, or a `.pptx` that looks fine in source but breaks after render.

## When to Use

Use this skill when the user wants:
- a journal club, lab meeting, literature review, or paper-report deck from one or more PDFs
- slide structure that follows the paper's logic rather than generic summary templates
- large readable figures with bilingual or audience-facing explanation
- visually polished academic slides rather than rough screenshot collages
- support figures mapped to the same conclusion as the main figure
- final delivery that is checked through real render QA

Do not use this as the primary workflow for:
- teaching decks that need major textbook-style pedagogy beyond the paper itself
- simple abstract-only summaries with no figure work
- business or corporate decks where paper-figure integrity is not the central constraint

## Quality Bar: What Good Output Looks Like

A good output from this skill has all of the following:
- the narrative follows the original paper's reasoning chain
- each result slide answers a clear question or states a clear conclusion
- figures are complete, undistorted, and readable
- main figures and same-conclusion support figures are paired correctly
- slide text speaks to the audience, not to the deck author
- the visual style is clean, premium, academic, and presentation-safe
- the final deck survives export/render QA without broken fonts, clipped headers, or unreadable support panels

## Hard Requirements

### 1. Preserve the paper's logic
- Follow the original argument order, especially the Results sequence.
- Do not reorder results just to make the layout prettier.
- If multiple papers are combined, build one integrated storyline instead of stacking mini-decks.

### 2. Use question-driven or claim-driven result slides
- Prefer a question or direct claim as the title of each result slide.
- Every result slide should make it obvious what problem that page is answering.
- Titles should help a speaker move naturally through the talk.

### 3. Figure integrity comes before decoration
- Prefer complete safe figure crops before panel splitting.
- Never crop into panel letters, axes titles, tick labels, legends, color bars, scale bars, workflow endpoints, right-edge labels, or bottom labels.
- If unsure, leave slightly more margin rather than cutting content.
- Never stretch figures; preserve aspect ratio at placement time.

### 4. Main + support evidence must be paired correctly
- Main figure and same-conclusion supporting figure should appear on the same slide whenever feasible.
- They should be shown at comparable visual scale, not as a hero image plus tiny thumbnail.
- Support pairing must come from conclusion-level mapping using the paper text and legends, not page adjacency.
- Never use a nearby text-heavy paper page as a fake support image.

### 5. Real support figures beat prose substitutes
- Always check whether supplementary figures exist in the same PDF or in separate supplementary files.
- If real supplementary figure assets exist, use them.
- If the page is dense, crop the actual supplementary figure body safely instead of shrinking a full text-heavy page to unreadability.
- Only use a support-summary text box when true support image assets genuinely cannot be obtained.

### 6. Slides must be audience-facing
- Write for listeners, not for the slide author.
- Remove creator-facing labels such as: Take-home, Reading note, Interpretation, speaker hint, "this slide wants to show", or similar scaffolding.
- If bilingual wording is requested, titles and explanatory text should both respect that request.
- Explanations should state what the figure shows, why it matters, and how it advances the paper's logic.

### 7. Visual design must be strong, restrained, and readable
- Prefer white or near-white content pages unless the user requests otherwise.
- Aim for premium academic / science-tech styling rather than business-template polish.
- Increase figure footprint before shrinking figures.
- Use hierarchy, spacing, alignment, restrained accent colors, and subtle structure rather than heavy shadows or decorative frames.
- Avoid oversized rounded cards, thick borders, bottom decorative bars, and dashboard-like chrome around figures.
- Make the deck feel presentation-ready, not merely correct.

### 8. Live-speaking readability is mandatory
- Use large enough titles and explanatory text for projection.
- Favor fuller layouts with clear hierarchy over sparse layouts with tiny figures.
- If a figure pair is too dense to read on one slide, split the content rather than shrinking it into illegibility.
- If support evidence remains unreadable at slide scale, re-crop or redesign the support area.

### 9. Render-based QA is non-optional
- `.pptx` source generation is not final acceptance.
- Final acceptance requires export/render inspection when the environment allows it.
- Verify crop integrity, figure identity, support readability, font rendering, title overflow, and audience-facing text in the rendered output.

## Recommended Deck Structure

A common paper-report flow is:
1. Cover
2. Why the problem matters
3. What question the paper asks
4. Why this team can do the work
5+. Results slides in paper order
6. Strengths / limitations / implications
7. Summary

Adapt this structure to the paper type:
- experimental papers: results-driven progression
- review papers: framework / field tension / conceptual map / future directions
- multi-paper synthesis: one integrated storyline with explicit transitions

## Workflow

### Step 1. Build a paper workspace
Create a project folder containing:
- original PDF(s)
- extracted text
- rendered page images
- supplementary page images
- crops
- PPT generation scripts
- rendered QA outputs

Keep assets organized enough that figure identity can be audited later.

### Step 2. Extract both text and page images
Work on two tracks in parallel:
- text track: abstract, introduction/problem framing, results, figure legends, supplementary legends
- image track: rendered paper pages for crop work and visual figure verification

If dependencies are missing, prefer a local virtual environment over assuming global installs.

### Step 3. Map questions, figures, and support evidence
Before slide design, explicitly map:
- each major figure
- the question or claim it answers
- which supplementary or extended-data figure supports the same conclusion
- where that result sits in the paper's logic

Do this before layout. Good decks are built from argument mapping, not from dragging images onto slides.

### Step 4. Write slide logic before layout
For each results slide, define:
- the title question or direct claim
- what the main figure proves
- what the support figure validates
- the most important quantitative or conceptual takeaway
- how this slide bridges from the previous one

### Step 5. Extract figures conservatively
- Start with full-figure-safe crops.
- For dense Nature/Cell/Science-style pages, remove dead page margin first, not scientific content.
- Confirm visually that the crop is figure-dominant rather than mostly body text.
- For review/framework papers, verify that the crop is a real figure body, not a text-heavy page with minor illustration.

### Step 6. Design slides for clarity and impact
Preferred result-slide behavior:
- main figure and support figure on the same page where feasible
- similar visual weight for main and support evidence
- concise audience-facing explanatory text
- clean figure area with minimal framing
- a clear visual center on each slide

Useful layout patterns include:
- left main figure / right support + explanation
- top figure pair / bottom conclusion strip
- two-up figure comparison with a compact text panel

But layout should always follow readability and argument structure, not a rigid template.

### Step 7. Polish for presentation quality
Actively improve:
- title hierarchy
- page fullness without clutter
- bilingual readability if needed
- scientific premium feel
- rhythm across slides
- cover / background / summary slides so the deck has visual presence, not just competent internals

For stronger aesthetics:
- use restrained accent colors
- create one visual center per slide
- trim dense text before adding decorative structure
- rebalance blank areas rather than letting figures stay too small

### Step 8. Run render QA
Export to PDF and/or slide images when possible.
Check for:
- clipped titles or header-band overflow
- tofu boxes / garbled CJK / broken fonts
- unreadable support panels
- wrong figure-number-to-image mapping
- creator-facing labels left in place
- image distortion
- accidental decorative leftovers
- blank panels created by late edits or language fallback

### Step 9. Fix and re-render
Do not stop at the first generated deck.
If render QA reveals problems, patch the source, regenerate, and re-check.
At least one fix-and-verify loop is expected for serious paper decks.

## Special Cases

### Review or framework-heavy papers
- Do not force them into a results-only format.
- Prioritize conceptual figures, framework diagrams, field maps, and future-direction logic.
- If a concept figure is dense, it may deserve two slides: one for structure, one for implications.

### Multi-paper decks
- Do not present them as isolated mini-presentations.
- Build a single narrative with explicit transitions and a shared biological or conceptual question.
- Exclude unrelated papers even if they were attached nearby.

### Environment or font constraints
- If bilingual rendering fails because CJK fonts are missing, treat that as a blocker, not a cosmetic issue.
- Prefer fixing the font/render environment first.
- If a fallback is unavoidable, make it deliberate and complete; do not leave a half-bilingual broken deck.

## Common Pitfalls

1. Using a summary card instead of the real support figure when supplementary assets exist.
2. Pairing support figures by page proximity instead of by conclusion.
3. Declaring a crop safe before checking the rendered slide.
4. Stretching figures by forcing both height and width.
5. Leaving support panels so small that they are technically present but presentation-useless.
6. Keeping creator-facing labels in the final deck.
7. Making the deck structurally correct but visually weak.
8. Using too much dashboard-style framing around scientific figures.
9. Treating source `.pptx` success as final QA.
10. Failing to adapt the workflow for review papers or multi-paper synthesis.

## Portability Rules

To keep this skill usable across environments and users:
- describe workflows in terms of outcomes and checks, not one narrow project layout
- prefer broadly available tooling and local-venv fallback patterns
- do not assume a specific font stack, filesystem, or user path
- make rendered verification part of the process whenever the environment allows it
- keep paper-specific lessons as references, but preserve a general workflow in the main skill
- when renaming or publishing a local umbrella skill under a new outward-facing name, migrate or recreate every referenced support file before calling the published skill complete
- after a rename, verify that every file listed in `## References` actually exists under the new skill directory rather than only in the old one

## Delivery Checklist

Before calling the deck done, confirm:
- output PPT path is known
- render QA output path is known when available
- figure/support mapping is correct
- crops preserve scientific content
- support figures are readable enough to matter
- slide text is audience-facing
- visual style is clean and presentation-ready
- no obvious decorative over-framing remains
- the delivered deck is the intended final variant, not an exploratory one

## References
- `references/metaedit-jcslides-mapping-and-crop-notes.md`
- `references/multi-paper-plasmid-copy-number-deck.md`
- `references/python-pptx-render-qa-first-pass.md`
- `references/figure-integrity-deep-fix-notes.md`
