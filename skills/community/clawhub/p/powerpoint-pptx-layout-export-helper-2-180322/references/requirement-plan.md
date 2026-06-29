# Requirement Plan

## Live Requirement

Validated demand: PowerPoint template maintainers need help repairing slide masters, placeholders, fonts, theme colors, chart links, and branded PPTX layouts that break during automated deck generation.

## Audience

Brand teams, consultants, presentation operations teams, and developers working with PowerPoint templates.

## Implementation Plan

1. Diagnose whether the issue belongs to the slide master, slide layout, slide content, theme, chart part, media relationship, or generation script.
2. Preserve the original PPTX and edit a copy.
3. Inspect PowerPoint Open XML parts before making changes.
4. Use template-aware generation that fills placeholders rather than drawing disconnected shapes.
5. Patch unsupported structures directly in OOXML only after identifying the exact relationship or part.
6. Validate the deck structurally and visually.

## Review Criteria

- The workflow protects the source template.
- The workflow distinguishes master, layout, slide, theme, and relationship failures.
- The workflow explains when `python-pptx` is enough and when OOXML inspection is required.
- The final answer includes validation steps for PowerPoint fidelity.
