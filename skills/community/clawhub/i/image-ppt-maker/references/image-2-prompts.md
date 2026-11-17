# Image-2 Prompt Rules

Write prompts for image-2. Each prompt must generate exactly one 16:9 PPT-style slide image.

Treat prompts as internal execution artifacts. Do not ask the user to review or approve prompts. Generate them after content and style approval, then proceed directly to image generation.

## Deck-wide style lock

Define one shared style lock before per-page prompts. It must specify:

- aspect ratio: 16:9;
- deck type: professional consulting-style PPT page;
- layout system: title area, content grid, margins, chart/table/card treatment;
- palette: primary, secondary, background, accent colors;
- typography: clear hierarchy, readable slide text, no decorative fonts;
- visual language: charts, diagrams, icons, photography, or abstract business visuals;
- density: high, medium, or low;
- optional LOGO space: no reserved area, upper-left reserved area, or upper-right reserved area;
- consistency rule: every page must look like part of the same deck.

Repeat the complete style lock inside every page prompt, but mark it as non-visible generation guidance. The style lock must influence layout and visual treatment only; image-2 must not render the style-lock wording as text on the slide.

## Per-page prompt structure

Each page prompt must include:

1. `Model`: image-2.
2. `Task`: generate only this single 16:9 PPT slide image.
3. `Style lock`: copy the shared deck-wide style lock.
4. `Style text handling`: state that style descriptions are instructions only and must not appear as visible text.
5. `Slide logic`: key question, governing thought, supporting logic, so what, transition.
6. `Expanded content`: the richer explanation or examples that should guide the visual emphasis.
7. `LOGO space`: if requested, reserve a small clear area in the chosen top corner; do not invent or render a logo unless the user provided one.
8. `Page message and content`: explain the thought this page should express, the core content to show, and the recommended title, key messages, labels, and emphasis.
9. `Composition`: layout, visual hierarchy, chart or diagram structure, spacing, alignment.
10. `Readability`: clean typography, enough contrast, no tiny unreadable text.
11. `Constraints`: factual constraints and source-material limits.
12. `Negative constraints`: forbidden outputs.

## Page message and content

Do not constrain the slide by enumerating every allowed visible word. Instead, describe the page's intended communication clearly enough for image-2 to design the slide:

- State the page's governing thought in an answer-first way.
- Explain the core content the slide should communicate, including the most important evidence, comparison, process, framework, or recommendation.
- Suggest the title, short labels, callouts, and chart/table labels that would help express the idea, but keep text concise and slide-like.
- Preserve McKinsey-style communication: structured, logical, executive-readable, and focused on one message per page.
- Do not render prompt section labels or internal reasoning labels such as "Style lock", "Slide logic", "Expanded content", "Page message and content", "McKinsey-style", "16:9", "professional consulting-style", or "image-2".
- If a style concept needs to show visually, express it through layout, color, spacing, chart treatment, and imagery, not through written words.
- If a LOGO area is reserved, it is a blank layout area unless the user supplies a logo. Do not render placeholder text such as "LOGO".
- Slide sequence numbers are file-management metadata only. Do not render page numbers, slide numbers, sequence labels, numeric badges, or file names anywhere in the image unless a number is explicitly part of the approved page content.
- For illustration-led styles, express the approved visual direction through recurring characters, coherent scenes, consistent linework or rendering, and visual metaphors; do not write the style name or illustration instructions on the slide.

Add this sentence to every prompt:

```text
Render concise slide text that supports the page message; all style descriptions, prompt section labels, and generation instructions are non-visible guidance and must not appear as words in the slide image.
```

## Negative constraints

Always forbid:

- multiple slides in one image;
- montage, contact sheet, overview, collage, or thumbnail grid;
- browser screenshot, app screenshot, chat screenshot, or document screenshot;
- long paragraphs, dense report prose, or text that does not support the page's governing thought;
- any visible wording copied from style descriptions, prompt section labels, or generation instructions;
- page numbers, slide numbers, sequence labels, numeric badges, or file names added only to identify the image;
- meta words such as style lock, deck-wide style, 16:9, image-2, prompt, McKinsey-style, typography, palette, layout system, consulting-style, Page message and content, or LOGO;
- watermark, signature, logo, model mark, or random brand mark;
- random icons, people, company names, or data not provided or approved;
- SVG, HTML, wireframe, or code-like rendering.

## Batch output

Generate one image per approved prompt. Use ordered names when saving files:

```text
images/slide-01.png
images/slide-02.png
images/slide-03.png
```

If a page fails visually, revise or regenerate that page only unless the style lock itself changed.

For any later single-page change, wait until the revised page logic, expanded content, and visual emphasis are explicitly approved. Then rebuild that page's prompt with the existing deck-wide style lock and generate only that page without adding a prompt-review step.
