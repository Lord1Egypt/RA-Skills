# Interaction Patterns

Add interaction whenever it helps the user inspect, compare, tune, edit, or export the work.

## Common Controls

- Tabs: switch between code examples, options, personas, environments, or report sections.
- Filters: narrow tickets, files, findings, metrics, rows, or glossary terms.
- Sort controls: order by priority, severity, date, owner, cost, or confidence.
- Collapsible sections: hide detail while preserving a skim-friendly overview.
- Sliders: tune duration, thresholds, weights, opacity, scale, budget, latency, or probability.
- Toggles: enable feature flags, states, layers, annotations, or alternate assumptions.
- Segmented controls: switch modes, views, scenarios, or environments.
- Detail panels: show one selected item without navigating away.
- Copy buttons: export the current state, code, prompt, diff, JSON, Markdown, or CSS.
- Reset buttons: restore the original state.

## Code Example Controls

- Use tabbed code examples for related variants such as HTML/CSS/JS, before/after, providers, or competing approaches.
- Use collapsible examples when snippets are long but still useful for a skim-first artifact.
- Give code blocks concise headers such as file path, language, or purpose.
- Add copy buttons when the user is likely to reuse code, CSS, JSON, prompt text, or diffs.
- Keep tab bars and code-example toolbars wrapping. Only the code pane itself may scroll horizontally.
- Make the selected tab obvious with a fill, underline, or accent border.

## Selection State Rules

- A control that looks selectable must update when selected. This includes chips, tabs, filters, segmented controls, selected cards, nav pills, diagram nodes, and board lanes.
- Pair visual selected state with semantics: `aria-selected` for tabs/options, `aria-pressed` for toggle buttons, `aria-current` for current navigation links, checked inputs for radio/checkbox controls.
- Do not style `.toc a:first-child`, `.chip:first-child`, or the first card as active unless JavaScript or the current URL/state also updates that active item.
- For hash navigation, update `aria-current` on click, `hashchange`, and initial load. Add scrollspy only when the active section should follow scrolling.
- For filters, show selected chips, update counts/results, and include a reset or "All" control.
- For multi-select chips, each chip can toggle independently. For single-select chips, selecting one must clear the others.

## Editor Artifacts

For one-off editors, always include an export path. The artifact should tighten the human-agent loop: the user manipulates the UI, then copies the result back into a prompt, file, issue, PR, or config.

Build the export first, then build the rest of the editor. Without export, the editor is a demo rather than a workflow.

Useful editors:

- Ticket triage board: drag items across Now / Next / Later / Cut, export Markdown.
- Feature flag editor: toggle grouped flags, show dependency warnings, export changed keys.
- Prompt tuner: edit a template, preview sample inputs, export final prompt.
- Dataset curator: approve, reject, tag, and export selected examples.
- Annotation tool: mark transcript, document, image regions, code excerpts, or findings.
- Prioritization matrix: move items across impact/effort axes, export ranking.
- Copy variant tester: compare copy across personas or moods, export selected version.

## Export Patterns

Choose the export format that matches the next step:

- Markdown for planning docs, issue comments, PR descriptions, status updates.
- JSON for structured data, config, datasets, or programmatic handoff.
- Diff for config edits and small file changes.
- Prompt text for agent handoff.
- CSS or design tokens for visual tuning.
- CSV for tabular review.

Make the export button label specific: "Copy as Markdown", "Copy changed JSON", "Copy diff", "Copy prompt", "Copy CSS".

## Implementation Notes

- Store source data as a JavaScript object near the top of the script when possible.
- Pre-fill the data the user already provided. Do not make the user paste it again.
- Keep DOM generation straightforward and easy to edit.
- Use `data-*` attributes for item IDs, states, filters, and categories.
- Use event delegation for lists, boards, and tables.
- Keep visible state and exported state derived from the same data object.
- Show a small "copied" confirmation after copy actions.
- For drag-and-drop, support click-based movement too when simple to add.
- Kanban/triage boards should support actual drag-and-drop between lanes when the page presents draggable cards. Also provide click buttons or keyboard-accessible fallback movement for users who cannot drag.
- During drag, show the dragged card state and the active drop lane. After drop, update lane counts, estimates, selected state, and export output from the same data object.
- Add keyboard shortcuts for repetitive classification or review tasks.
- Add undo/redo for editors with many small state changes when practical.
- Show validation errors, dependency warnings, counts, and changed-state indicators immediately.
- Persist state in the page when the environment supports it and the task is long enough that refresh loss would be painful.
- For sliders and toggles, update the preview live.
- For tabs and filters, make the active state visually obvious.
- For slide decks, provide visible previous/next arrow buttons and left/right keyboard navigation. Both paths must update the active slide, any numbered tab state, and the progress label from one shared slide index.

## Common Editor Mistakes

- Building a generic product instead of a throwaway tool for the exact data at hand.
- Adding settings instead of direct controls.
- Creating interaction without export.
- Hiding constraints until export time.
- Making the work area smaller than the chrome around it.
- Requiring a backend, account, API, or build step.

## Prototype Patterns

For motion, design, and interaction prototypes:

- Put the live preview next to the controls.
- Include sliders for timing, easing, scale, distance, opacity, color, and delay.
- Include presets when several directions are plausible.
- Show the generated CSS, JSON, or parameters.
- Provide reset and copy controls.

The page should let the user feel the interaction, then export the chosen parameters.

## Diagram Interactions

For complex diagrams:

- Let the user click a node to show details.
- Keep the diagram readable without interaction; interaction should reveal detail, not hide the basics.
- Highlight related nodes and edges on hover or selection.
- Provide reset and "show all" controls when filtering.
- Keep labels visible; do not rely only on hover text.
