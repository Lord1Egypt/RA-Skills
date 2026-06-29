---
name: make-html
description: Aggressively produce self-contained HTML artifacts instead of Markdown for substantial agent outputs. Use when the user asks for a doc, plan, spec, report, review, PR description, explainer, summary, comparison, research artifact, dashboard, diagram, flowchart, timeline, deck, slides, prototype, design reference, component sheet, editor, prompt tuner, config editor, triage board, or any human-facing deliverable that benefits from layout, visual hierarchy, navigation, diagrams, interactivity, or sharing. Default to this skill even when the user does not explicitly request HTML; stay in plain chat only for very short replies, code-only snippets, terminal commands, or explicit non-HTML requests.
---

# Make HTML

## Default Posture

Make an HTML artifact for substantial deliverables. When in doubt, use HTML. Markdown and plain chat are fallbacks for brief exchanges, not the default for work a human needs to read, compare, present, share, or manipulate.

Usually produce a single self-contained `.html` file. If the environment cannot create files, output the complete HTML document in one fenced `html` block and name the intended filename.

Do not ask permission to use HTML unless the user requested a conflicting output format.

Use the strongest version of the medium. Do not wrap a Markdown-shaped answer in HTML. If the content is a comparison, make it comparable. If it is a timeline, draw a timeline. If it is a diagram, draw the diagram. If it is an editor, make the export path central.

## Workflow

1. Classify the job shape: comparison, plan, review, code map, explainer, report, dashboard, diagram, deck, prototype, or editor.
2. Read the relevant reference file:
   - `references/recognition.md` when deciding whether the task deserves HTML.
   - `references/artifact-patterns.md` for static or mostly static documents.
   - `references/interaction-patterns.md` for prototypes, explainers, dashboards, and editors.
   - `references/visual-quality.md` before writing the final artifact structure and styling.
   - `references/validation.md` before returning any nontrivial artifact, especially artifacts with JavaScript, SVG, tables, diagrams, or dense responsive layouts.
   - `references/sharing.md` when the user asks for a hosted preview, shareable link, password protection, custom URL, or cross-device review.
   - `references/source-style.md` when the artifact is about an existing product, repository, brand, app, docs site, or design system.
   - `references/custom-themes.md` when the user asks for a saved/custom/personal theme, when a theme name is provided, or when no source style exists and `themes/` contains a default or clearly matching theme.
   - `themes/fallback-theme.md` when no source/project style can be found after a quick style search, or when the artifact has no natural brand.
   - `references/example-layout-catalog.md` when the task resembles one of the HTML-effectiveness example pages, or when choosing a specific style, layout, or interaction recipe.
   - Read multiple references when the artifact spans categories, such as a plan with mockups and a flowchart.
3. Resolve style provenance before writing CSS: source-backed style with concrete files/tokens, an explicitly selected saved theme, or the built-in fallback theme. Do not invent an unlabeled generic theme between these choices.
4. Choose a page structure that makes the shape of the information obvious. Prefer side-by-side layouts, timelines, maps, tables, diagrams, controls, and navigation over long linear prose.
5. Write a complete HTML5 document with inline CSS and, when useful, inline JavaScript.
6. For editor-style artifacts, include a visible export path such as copy as Markdown, copy as JSON, copy diff, copy prompt, or download file.
7. Include enough source excerpts, labels, assumptions, and style provenance inside the page for the artifact to stand alone.
8. Validate the artifact before returning it. At minimum, check self-containment, required HTML tags, dynamic render output when JavaScript is present, and narrow-viewport behavior.
9. When the user asks for a hosted or shareable link, follow `references/sharing.md` after local validation. Never upload an artifact automatically.

## Universal Requirements

- Use one self-contained `.html` file by default.
- Include `<!doctype html>`, `<html lang="en">`, `<meta charset="utf-8">`, a viewport meta tag, and a meaningful `<title>`.
- Put CSS in a `<style>` block and JavaScript in a `<script>` block. Do not require a bundler, package install, or build step.
- Work offline by default. Do not require network calls, remote fonts, CDN scripts, or external stylesheets for the artifact to render. Use inline SVG, inline data, and data URIs when assets are necessary.
- Prefer semantic HTML: `header`, `main`, `section`, `article`, `nav`, `aside`, `table`, `details`, `button`, `label`, and form controls where they fit.
- Use inline SVG, canvas, CSS, and native controls freely when they make the artifact clearer.
- Make the page responsive. It should remain readable on narrow screens without page-level horizontal scrolling. Intentional horizontal scrolling is acceptable only inside bounded regions such as code blocks, dense tables, and large diagrams.
- Chip-like UI must wrap instead of scrolling horizontally. This includes jump links, filter chips, segmented controls, badges, button groups, tag rows, and legends. Never hide these controls in a horizontal scroll strip.
- Force long tokens to wrap where they appear in prose, callouts, badges, cells, and inline code. Local paths, URLs, branch names, hashes, commands, and long identifiers must not widen the whole page.
- Do not size text with viewport units. Use explicit sizes plus media-query breakpoints so headings and labels fit predictably.
- Use clear hierarchy and dense, scannable layout. Avoid filling the page with decorative shells that do not add meaning.
- Styling precedence is: source/project style, explicitly requested saved theme, saved default or clearly matching theme, then fallback theme.
- When claiming source/project style, the artifact must be backed by concrete style evidence such as CSS variables, theme config, UI component source, local screenshots, or product pages. Source content alone is not source style.
- When no source style evidence is found, use `themes/fallback-theme.md` directly. Do not create a neutral light dashboard, generic docs UI, or model-invented palette as a substitute fallback.
- Add a compact style provenance note in the artifact, usually in the footer or a source/evidence section: name the source files/tokens, saved theme, or fallback theme used.
- Make state visible. Selected tabs, active filters, changed values, warnings, and recommendations should be obvious at a glance.
- Selection state must be real. Tabs, chips, filters, segmented controls, nav pills, selected cards, and toggles must update their visual state and `aria-selected`, `aria-pressed`, or `aria-current` value when the user changes selection. Do not hard-code the first item as active unless it is the only possible state.
- Make interactive controls discoverable and reversible. Sliders, toggles, filters, and editors should have labels and reset behavior when helpful.
- For comparisons, keep options aligned so the reader can compare the same dimension across choices.
- For reports and reviews, put the conclusion, recommendation, or highest-priority findings near the top.
- For diagrams, add labels, legends, and short explanations near the visual rather than burying them below.
- For diagrams, prefer lane-based or layered layouts with orthogonal or clearly routed arrows. Avoid crossing arrows; if crossings appear in a screenshot, redesign the layout rather than accepting it.
- For decks, use one `<section>` per slide and keyboard navigation.
- For design references and figure sheets, include copy controls for tokens, SVG, code, or parameters.
- For code examples, prefer tabbed examples, collapsible detail, annotated snippets, or diff blocks over plain fenced-code styling. Code samples should feel like first-class artifacts.
- Code blocks must remain readable: style inline code with `:not(pre) > code`, never a bare `code` selector, and reset `pre code` to transparent background, no border, inherited block color, inherited monospace font, and preserved whitespace.
- Code blocks should include offline syntax highlighting by default. Use semantic token spans or a small inline highlighter for common languages such as JSON, shell, HTML, CSS, JavaScript, TypeScript, and diffs. Do not depend on CDN highlighters or leave substantial code blocks monochrome.
- For long artifacts, add jump links, tabs, filters, or collapsible sections instead of making the user scroll through a wall.

## When Plain Chat Is Enough

Stay out of HTML only when the response is genuinely small or the user asked for a different format:

- A short conversational answer.
- A command or terminal-style response.
- A single code snippet or config block.
- A quick list that the reader will scan once.
- An explicit request for Markdown, JSON, plain text, or another format.

If the output starts becoming a document, switch to HTML.

## Artifact Families

Common outputs this skill should create:

- Option comparison pages with aligned tradeoffs and a recommendation.
- Implementation plans with milestones, data flow, key code, risks, and open questions.
- PR or code review pages with annotated diffs, severity labels, and reviewer focus areas.
- Module maps and architecture explainers with boxes, arrows, call paths, and entry points.
- Design system references with colors, type, spacing, components, states, and copyable tokens.
- Component variant sheets showing every state, size, intent, and edge case.
- Animation or interaction prototypes with live controls and exported parameters.
- Flowcharts, timelines, process maps, and SVG figure sheets.
- Research or learning explainers with tabs, collapsible sections, glossary, diagrams, and live demos.
- Status reports and incident reports with metric cards, timelines, impact, root cause, and action items.
- Slide decks implemented as HTML sections with keyboard navigation.
- Custom editors for triage, prioritization, config, prompts, datasets, annotations, copy, and structured content.

## Output Conventions

When creating a file, use a short descriptive filename such as:

- `implementation-plan.html`
- `pr-review.html`
- `module-map.html`
- `concept-explainer.html`
- `incident-report.html`
- `triage-editor.html`
- `prompt-tuner.html`

When returning the artifact, mention what was created and where it is. Keep the chat response brief; the HTML page is the deliverable.

When returning a hosted preview, also state its expiry and keep the local `.html` file as the canonical fallback.
