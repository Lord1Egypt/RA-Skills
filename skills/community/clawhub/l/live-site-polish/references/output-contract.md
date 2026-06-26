# Output Contract

The final handoff must be easy to find and easy to understand. It does not need a rigid schema.

## Minimum Requirement

Put all final outputs under one obvious directory. The next code agent should not need to search the whole workspace to find them.

Good examples:

- `live-site-polish-output/homepage-hero-refresh/`
- `output/live-site-polish/2026-03-26-checkout-cta/`
- `tmp/site-redesign-round-2/`

## What Must Exist Somewhere In That Directory

- one or more before screenshots
- one or more after screenshots
- a reference patch script or equivalent implementation sketch
- written notes explaining the task and the final direction

Create this final directory after the reviewer approves the result. During iteration, temporary screenshots and draft notes can live elsewhere.

## Suggested Directory Shape

Use a simple structure like:

```text
<task-output>/
  before.png
  after.png
  notes.md
  patch.js
  tmp/
```

Use `tmp/` for temporary run artifacts only: intermediate screenshots, draft scripts, reviewer scratch files, and other disposable files. Clean `tmp/` before completion, or remove it entirely if nothing needs to remain.

## Flexible Formats

Use whatever filenames and lightweight formats make the handoff clear:

- screenshots: `.png`, `.jpg`, `.webp`
- notes: `.md`, `.txt`
- patch or implementation sketch: `.js`, `.ts`, `.html`, or another readable text format

## Notes Guidance

The notes should cover:

1. Page URL or page identity
2. User request or task brief
3. Exact area changed
4. Key design decisions
5. Anything the next code agent should preserve or be careful about

## Reference Patch Guidance

The reference patch is not expected to be production-safe code. It only needs to express:

- the DOM structure you introduced or changed
- the copy, layout, styling, and hierarchy decisions
- enough intent for a coding agent to port the change into source code

Avoid burying the final implementation inside unrelated experiment files.
