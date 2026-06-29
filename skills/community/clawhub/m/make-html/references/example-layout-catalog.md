# Example Layout Catalog

Use this catalog when a task matches one of the HTML-effectiveness example families or when the user asks to borrow that site's style, layout, or design language. Combine it with `source-style.md` first; use `themes/fallback-theme.md` only when no source style exists.

## Shared Rules

- Choose a layout because it fits the job, not because it is decorative.
- Keep the artifact self-contained and offline.
- Use the fallback editorial theme for unbranded examples: ivory paper, slate text, serif display headings, mono labels, oat borders, and plum active states.
- Build real interactions when controls imply state. Tabs, filters, chips, deck navigation, selected nodes, toggles, and editors must update visible state and ARIA state.
- Chip-like controls wrap. Only code panes, diffs, dense tables, and large diagrams may scroll horizontally.
- Code examples need a designed container: file label, tabs or collapsible detail when useful, line numbers or diff rows when reviewing, and copy buttons when reuse is likely.
- Clickable cards should feel clickable: use a slight lift, stronger border, soft shadow, thumbnail/header tint change, and small arrow/file-label motion on hover and `:focus-visible`.
- Clickable cards must link to something real. Use a page URL, an in-page detail panel, an anchored section, or a copy/export action; do not use decorative arrows with dead destinations.

## Page Recipes

### 01-exploration-code-approaches.html — Exploration: Code Approaches

Use for choosing between implementation strategies.

- Layout: prompt/context block, three aligned approach cards, code snippet in each card, shared tradeoff dimensions, recommendation strip.
- Include: comparable metrics, "choose this if" guidance, risk/complexity labels, and real code excerpts.
- Avoid: three prose sections with different dimensions or a weak "it depends" conclusion.

### 02-exploration-visual-designs.html — Exploration: Visual Design Directions

Use when the user needs to react to UI directions before choosing one.

- Layout: toolbar/controls, 4-up visual direction board, live mini artboards, palette/tone tags, rationale captions.
- Include: structurally different directions, not only color swaps; selected-state preview if a direction can be chosen.
- Avoid: generic mood boards without rendered UI.

Homepage/card-index variant:

- Use when presenting a gallery of examples, routes, demos, choices, or generated artifacts.
- Render each item as an anchor card with a media/thumb band, serif title, short description, filename/action row, and trailing arrow.
- Hover/focus should promote the card with lift, darker border, warmer/tinted thumb band, stronger shadow, and arrow movement. Neighboring cards remain quiet.
- The card destination should be visible and testable: navigate to a page, update an adjacent detail panel, or scroll to a named in-page target.

### 03-code-review-pr.html — Code Review: Annotated Pull Request

Use for code review, reviewer triage, or risk-focused diff summaries.

- Layout: PR header, risk chips, file cards, dark diff blocks with line numbers, inline review bubbles, collapsible lower-risk files, checklist.
- Include: severity tags, jump links, exact line anchors, and next actions.
- Avoid: separating findings from the code that proves them.

### 04-code-understanding.html — Code Understanding: Module Map

Use for unfamiliar codebases, feature flows, runtime paths, and ownership maps.

- Layout: repo/file context, SVG module diagram, highlighted hot path, key files, details for nodes or steps.
- Include: entry points, data/control arrows, gotchas, invariants, and snippets for the important surfaces.
- Avoid: drawing every dependency edge; use lanes and side panels to prevent crossing arrows.

### 05-design-system.html — Design: Living Design System

Use for tokens, source style extraction, and reusable visual references.

- Layout: swatch grids, typography rows, spacing/radius/shadow demonstrations, component examples, copyable tokens.
- Include: token names and values, actual rendered samples, focus/disabled/error states where relevant.
- Prefer compact square swatches beside token names/values for token lists; use large color slabs only for palette exploration.
- Avoid: prose-only design system descriptions.

### 06-component-variants.html — Design: Component Variants

Use for reviewing a component across size, state, intent, density, and edge cases.

- Layout: controls/filters, variant matrix, repeated component cells, code snippet for the selected variant.
- Include: long text, disabled, loading, focused, selected, empty, and narrow states.
- Avoid: only showing the happy-path component.

### 07-prototype-animation.html — Prototype: Animation Sandbox

Use when timing, easing, or motion needs to be felt.

- Layout: live preview stage, control panel with sliders/segmented easing presets, timeline/readout, generated CSS.
- Include: replay/reset, current parameter values, copyable CSS or token output.
- Avoid: describing motion without a live preview.

### 08-prototype-interaction.html — Prototype: Clickable Flow

Use for low-fidelity interaction checks and screen-to-screen workflows.

- Layout: simulated screen or sidebar, draggable/clickable items, notes/questions panel, visible selected/drag states.
- Include: keyboard or click fallback for drag actions when practical, and reset state.
- Avoid: static screenshots when the request is about interaction feel.

### 09-slide-deck.html — Deck: Arrow-Key Slide Deck

Use for meeting-ready narratives, updates, and design/readout decks.

- Layout: one full-viewport `<section>` per slide, progress bar, visible previous/next arrow buttons, keyboard navigation, concise slide title, slide-specific visual.
- Include: left/right arrow buttons and left/right keyboard shortcuts wired to the same slide state, progress state, and notes or appendix only when useful.
- Active slide controls must update `aria-selected` and the progress label/count together whether the user clicks a numbered tab, clicks an arrow button, or presses an arrow key.
- Avoid: dense document pages pretending to be slides.

### 10-svg-illustrations.html — Diagrams: SVG Figure Sheet

Use for article figures, visual aids, or reusable inline illustrations.

- Layout: figure sheet with consistent SVG style, caption/metadata per figure, palette legend, copy/download SVG buttons.
- Include: editable inline SVG groups, `viewBox`, labels, captions, and shared line weights.
- Avoid: raster diagrams when SVG would be editable.

### 11-status-report.html — Reports: Weekly Status

Use for recurring status updates and stakeholder summaries.

- Layout: report header, summary band, metric cards, small chart, shipped/slipped/carryover sections, risk table.
- Include: dates, owners, status labels, trend indicators, and concise evidence.
- Avoid: long chronological prose without scannable metrics.

### 12-incident-report.html — Reports: Incident Timeline

Use for incident reports, postmortems, regressions, and operational failures.

- Layout: incident header, severity/status pills, TL;DR, minute-by-minute timeline, log/diff excerpts, action items.
- Include: impact, detection, mitigation, root cause, owner/date for actions.
- Avoid: hiding exact times or mixing root cause with follow-up tasks.

### 13-flowchart-diagram.html — Diagrams: Annotated Flowchart

Use for pipelines, request flows, workflows, and branching operational processes.

- Layout: SVG flowchart as the main surface, legend, clickable nodes, adjacent detail panel, happy path and failure path styles.
- Include: timings, commands, failure modes, retry paths, and selected-node state.
- Avoid: crisscrossing arrows; split into lanes or panels if routing gets messy.

### 14-research-feature-explainer.html — Research: Feature Explainer

Use for explaining how a feature works inside a repo or system.

- Layout: TL;DR callout, files/where section, collapsible path steps, tabbed code/config snippets, FAQ.
- Include: request path, important files, config examples, gotchas, and copyable snippets.
- Avoid: a linear wall of explanation.

### 15-research-concept-explainer.html — Research: Concept Explainer

Use for teaching a stateful or spatial concept.

- Layout: live model/demo, controls, readout, comparison table, hover-linked glossary.
- Include: parameters the reader can change and immediate visual feedback.
- Avoid: static diagrams for concepts where state changes are the point.

### 16-implementation-plan.html — Planning: Implementation Plan

Use for feature specs, handoffs, migrations, and multi-slice work.

- Layout: scope summary, milestone timeline, data-flow SVG, small mockups, risky code/API snippets, risk table.
- Include: independently reviewable slices, owners or dependencies, verification plan, and non-goals.
- Avoid: a checklist with no data flow or risk model.

### 17-pr-writeup.html — Code Review: PR Writeup

Use for author-side PR descriptions and reviewer prep.

- Layout: motivation, before/after, stats, file-by-file tour, collapsible file sections, review focus, tests/rollout.
- Include: why each file changed, where reviewers should focus, and what proof exists.
- Avoid: repeating commit messages without a review map.

### 18-editor-triage-board.html — Editor: Ticket Triage Board

Use when the user must sort, prioritize, classify, or sequence many items.

- Layout: sticky toolbar with lane counts and export/reset actions, Kanban lanes, compact draggable/clickable tickets, lane estimate footers, summary/export panel.
- Include: copy Markdown/JSON export, visible selected/filter state, drag-and-drop movement, and click-based movement fallback.
- Ticket cards should be dense and scannable: small title, issue id, type chip, size/estimate badge, assignee initials/avatar, and hover/focus/drag state.
- Lanes should have visible names, counts, optional colored top borders, drop-target feedback, and estimate totals.
- Avoid: a board with no export path back to the agent/workflow.

### 19-editor-feature-flags.html — Editor: Feature Flag Editor

Use for config toggles, feature flags, environment settings, and dependency-sensitive switches.

- Layout: grouped toggles, side summary, warnings for dependency violations, generated diff panel, copy diff button.
- Include: original vs changed state, dependency chips, warning counts, reset/copy actions.
- Avoid: letting invalid combinations look acceptable.

### 20-editor-prompt-tuner.html — Editor: Prompt Tuner

Use for prompts, templates, copy variants, generated-response tuning, and variable-slot editing.

- Layout: editable template, highlighted slots, sample input selector, live rendered previews, missing-variable warnings, export button.
- Include: token/character counts when useful, sample scenarios, and copy final prompt.
- Avoid: making the user edit text without seeing downstream output.
