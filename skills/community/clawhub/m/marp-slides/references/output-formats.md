# Marp Output Formats

## Default Behavior

- If the user does not specify an output format, render the deck as `.html`.
- Keep the editable source deck as `*.slides.md`.
- If the user explicitly asks for markdown only, stop at `*.slides.md`.
- Use the installed `marp` CLI as the render entrypoint.

## Supported Outputs

### HTML slideshow (default)

Use when:

- the user says "slideshow", "deck", or "presentation" without naming a format
- the user wants an easy-to-open interactive artifact

Command:

```bash
marp input.slides.md -o output.slides.html
```

### PDF

Use when:

- the user wants a shareable static deck
- they need easy printing or offline review

Command:

```bash
marp input.slides.md --pdf -o output.slides.pdf
```

### PowerPoint

Use when:

- the user wants a presentation file for slide software

Command:

```bash
marp input.slides.md --pptx -o output.slides.pptx
```

Optional editable mode:

```bash
npx --yes @marp-team/marp-cli input.slides.md --pptx --pptx-editable -o output.slides.pptx
```

Note: use standard `.pptx` export unless the user specifically asks for editable PowerPoint output.

### Notes text

Use when:

- the user wants presenter notes or a text extract of slide notes

Command:

```bash
marp input.slides.md --notes -o output.notes.txt
```

### Single-slide image

Use when:

- the user wants a cover slide or preview image

Commands:

```bash
marp input.slides.md --image png -o output.png
marp input.slides.md --image jpeg -o output.jpeg
```

### One image per slide

Use when:

- the user wants each slide exported separately for chat, docs, or embeds

Commands:

```bash
marp input.slides.md --images png -o output-dir/
marp input.slides.md --images jpeg -o output-dir/
```

## Format Selection Rules

Choose format in this order:

1. Explicit user request, like `.pdf`, `.pptx`, `PNG`, or `notes`
2. Explicit output filename or extension
3. Delivery context if the user clearly asks for multiple render targets
4. Default to `.html` if nothing else is specified

## Suggested Source + Output Naming

- Source deck: `name.slides.md`
- Default render: `name.slides.html`
- PDF: `name.slides.pdf`
- PPTX: `name.slides.pptx`
- Notes: `name.notes.txt`

## Delivery Guidance

- When producing a rendered artifact, mention both the source `*.slides.md` and the rendered output path.
- If the user asks for multiple outputs, render from the same source deck rather than maintaining separate slide variants.
- If a requested format is unsupported by Marp CLI, ask a short clarification question or offer the nearest supported format.
- If `marp` is unavailable, install `@marp-team/marp-cli` before rendering.
