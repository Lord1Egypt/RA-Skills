# Artifact Patterns

Use these patterns as starting points. Combine them freely when the task benefits from more than one shape.

## Comparison

Use for choices, alternatives, approaches, vendors, designs, APIs, architectures, or tradeoffs.

Recommended structure:

- Header with the decision question.
- Recommendation strip near the top.
- Side-by-side option cards with the same dimensions in the same order.
- Real artifacts inside each option: code snippet, mockup, diagram, workflow, or sample output.
- Pro/con table inside each option.
- Hard metrics row for cost, risk, complexity, speed, reversibility, maintainability, bundle size, latency, confidence, or fit.
- Tradeoff matrix with shared dimensions across every option.
- "Choose this if..." guidance per option.
- Open questions or evidence gaps.

Keep comparable details aligned horizontally.

Always recommend one option unless the user explicitly asked only for neutral analysis. If all options look similar, widen the option space instead of producing cosmetic variants.

## Implementation Plan

Use for feature plans, specs, roadmaps, migrations, and handoffs.

Recommended structure:

- Summary with scope, effort, affected surfaces, and rollout shape.
- Milestone timeline with independently reviewable slices.
- Data flow or request flow diagram.
- Mockups or interface sketches when the user-facing behavior matters.
- Key code snippets or API contracts.
- Risk table with severity, mitigation, owner, and verification.
- Open questions with decision owners.
- "Not doing" section to control scope.

Make the page readable as a handoff document.

The data-flow diagram and risk table are load-bearing. Do not skip them when the plan touches more than two components.

## PR Review Or Code Review

Use for reviews, diff explanations, reviewer prep, or pull request writeups.

Recommended structure:

- Top findings ordered by severity.
- File map with status labels.
- Annotated diff blocks with margin notes.
- Risk map grouped by correctness, tests, performance, compatibility, and maintainability.
- Suggested next steps.
- Reviewer focus section: where to spend attention first.

Keep code excerpts close to commentary. Avoid separating findings from the exact code they refer to.

Use the diff as the spine of the page. Pin comments to lines. For larger changes, make file sections collapsible and add jump links to annotated regions.

## Code Understanding Or Module Map

Use for unfamiliar codebases, packages, features, data paths, and runtime flows.

Recommended structure:

- Entry points.
- Module boxes grouped by layer or responsibility.
- Arrows for calls, data flow, events, or ownership.
- Hot path highlighted.
- "What happens when..." walkthrough.
- Important files table.
- Gotchas and invariants.

Prefer SVG for maps and flow diagrams.

Do not draw every relationship. Show structural relationships, highlight the hot path, and list edge cases separately.

## Design System Or Component Sheet

Use for design tokens, UI inventory, component variants, and style references.

Recommended structure:

- Color swatches with names and values.
- Type scale with real sample text.
- Spacing, radius, elevation, and motion tokens.
- Component contact sheets by size, state, intent, density, and edge case.
- Copyable token values.
- Notes about visual rhythm and usage.

Render components as the user would see them, not as prose descriptions.

For design tokens, render the token as itself: color as swatch, type as actual type, spacing as measured gaps, shadows as shadowed surfaces. For components, include the awkward states: loading, empty, disabled, focused, error, long text, and narrow width.

## Visual Design Exploration

Use when the user is unsure which UI direction to take.

Recommended structure:

- Grid of 4-6 meaningfully different directions.
- Each direction uses a different layout, density, hierarchy, tone, or interaction model.
- Each direction has a short tradeoff caption.
- Optional full-width preview when a direction is selected.

Do not produce six versions of the same layout with different colors. Vary structure first, surface treatment second.

## Report Or Status Update

Use for weekly reports, project updates, research reports, stakeholder summaries, and operational reviews.

Recommended structure:

- TL;DR or executive summary.
- Metric cards for the few numbers that matter.
- What changed, what shipped, what slipped, what is blocked.
- Timeline or changelog.
- Risks and decisions needed.
- Appendix for detailed evidence.

Design for scanning first, then deeper reading.

## Incident Report Or Postmortem

Use for outages, regressions, operational failures, and retrospective analysis.

Recommended structure:

- Incident ID, severity, status, duration, owner.
- TL;DR.
- Timeline with exact times.
- Impact metrics.
- Root cause with relevant excerpts.
- Detection and response notes.
- Action items with owner and date.

Put the timeline and root cause in distinct visual regions.

Incident timelines should show pace. Use timestamped rows, event grouping, and inline logs where they mattered.

## Research Or Learning Explainer

Use for technical concepts, feature explainers, architecture learning, and synthesized research.

Recommended structure:

- One-screen summary.
- Diagram or interactive model.
- Step-by-step explanation.
- Code/config examples in tabs.
- Comparison table.
- Glossary in an aside or anchored section.
- FAQ or gotchas.

Use interaction when the concept involves parameters, state, or motion.

For stateful or spatial concepts, a live demo is load-bearing. Include controls that let the reader change the system and immediately see what moves, changes, or breaks.

## Deck

Use for meeting-ready narratives and presentations.

Recommended structure:

- One `<section>` per slide.
- Visible previous/next arrow buttons.
- Keyboard left/right navigation wired to the same state as the arrow buttons.
- Progress indicator.
- Full-viewport slide mode with stable aspect ratio.
- Fullscreen control or keyboard shortcut when possible.
- Speaker notes hidden behind a toggle when useful.
- Big idea per slide, not dense prose.

Numbered slide tabs may be included, but they are not a substitute for previous/next navigation. Slide decks should work through arrow buttons, arrow keys, and any direct slide selector without those controls drifting out of sync.

Use HTML when a quick shareable deck is more useful than a full presentation app.

## Dashboard

Use for state summaries, operating views, project boards, metrics, and decision rooms.

Recommended structure:

- Summary cards.
- Filters or segmented controls.
- Main chart/table/board.
- Detail panel for selected item.
- Change log or timeline.
- Export control when the selected state matters.

Prioritize information density and stable alignment.

## Figure Sheet

Use for article illustrations, technical diagrams, or visual aids.

Recommended structure:

- One `<figure>` per diagram.
- Inline SVG with `viewBox`, labels, captions, and consistent line weight.
- Copy SVG button for each figure.
- Shared visual language across the set.

Use round SVG coordinates and grouped elements so a human or another agent can edit the source.

## Annotated Flowchart

Use for pipelines, request flows, operational processes, and branching workflows.

Recommended structure:

- Inline SVG flowchart with directional arrows.
- Happy path highlighted.
- Failure, retry, or alternate paths visually distinct.
- Legend for color, shape, and line style.
- Clickable nodes or adjacent detail panel when each step has more context.

The chart is navigation; the detail panel is the explanation.
