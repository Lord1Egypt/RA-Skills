# KMind Markdown To Mind Map

[中文说明](./README_zh_CN.md)

Convert Markdown heading outlines into polished KMind mind maps offline.

This skill exports:

- `PNG` for bitmap images
- `SVG` for vector images
- `.kmindz.svg` for editable KMind project files

It supports theme presets, root layouts, edge routes, light or dark appearance, and rainbow branches.

Recommended input is a hierarchy built with Markdown headings such as `#`, `##`, and `###`. Headings become mind map nodes. Non-heading body text under a heading becomes notes on that node. Image export shows notes as note-entry icons by default instead of expanding the note text. To view or continue editing those notes, export `.kmindz.svg` and open it in a KMind Zen client.

When the user simply asks for a mind map image, prefer PNG by default. Use SVG only when vector output is explicitly requested.

## What This Repo Contains

This repository is the publishable skill bundle for `kmind-markdown-to-mindmap`.

Main files:

- `SKILL.md`: skill instructions for agent runtimes
- `scripts/kmind-render.mjs`: local entrypoint
- `scripts/vendor/*`: bundled KMind CLI runtime
- `agents/openai.yaml`: agent metadata

## Requirements

- Node.js installed locally
- For automatic `SVG` or `PNG` image export: a usable local Chromium browser
- No network connection is required for local conversion itself

Notes:

- `.kmindz.svg` export does not depend on browser rendering
- `SVG` / `PNG` export uses a local browser render flow

## Quick Start

List available themes, layouts, and edge routes:

```bash
node ./scripts/kmind-render.mjs themes --format json
```

Create an editable KMind project file:

```bash
node ./scripts/kmind-render.mjs import-markdown ./outline.md \
  --output ./outline.kmindz.svg
```

Create a PNG mind map (recommended default image format):

```bash
node ./scripts/kmind-render.mjs render-markdown ./outline.md \
  --output ./outline.png \
  --theme-preset kmind-material-3-slate \
  --layout mindmap-both-auto \
  --edge-route orthogonal \
  --appearance dark \
  --rainbow on
```

Create an SVG mind map:

```bash
node ./scripts/kmind-render.mjs render-markdown ./outline.md \
  --output ./outline.svg \
  --theme-preset kmind-rainbow-breeze \
  --layout logical-left \
  --edge-route edge-lead-quadratic \
  --appearance dark \
  --rainbow auto
```

Use stdin instead of a file:

```bash
node ./scripts/kmind-render.mjs render-markdown - \
  --output ./stdin-demo.png <<'EOF'
# Terminal Demo
## Branch A
### Item 1
## Branch B
### Item 2
EOF
```

## Common Parameters

- `--output`: target file path; format is inferred from suffix when possible. Prefer `.png` for normal image requests and `.svg` only for vector output.
- `--theme-preset`: theme preset id from `themes --format json`
- `--layout`: root layout id
- `--edge-route`: branch edge style id
- `--appearance`: `light` or `dark`
- `--rainbow`: `auto`, `on`, or `off`
- `--png-scale`: PNG export scale; default is `1`
- `--browser`: `auto` or `manual`

Current publish-safe layout set:

- `logical-right`
- `logical-left`
- `mindmap-both-auto`

Current publish-safe edge-route set:

- `cubic`
- `edge-lead-quadratic`
- `center-quadratic`
- `orthogonal`

## Recommended Defaults

- `theme-preset`: `kmind-material-3-slate`
- Image output suffix: `.png`
- `appearance`: `light`
- `rainbow`: `auto`
- `png-scale`: `1`

If the user wants an editable KMind package instead of an image, prefer:

```bash
node ./scripts/kmind-render.mjs import-markdown INPUT_OR_DASH \
  --output OUTPUT.kmindz.svg
```

## Typical Use Cases

- Meeting outlines
- Reading notes
- Brainstorming lists
- Project proposals
- Markdown heading outline-to-mindmap workflows

## Limitations

- Automatic image export requires a usable local Chromium browser
- This skill does not bundle a browser
- If automatic browser launch is unavailable, use `--browser manual`
- Long non-heading body text is stored as node notes. In exported images, those notes are represented by note icons instead of expanded text.

## Related

- KMind Zen: `https://kmind.app`
- Skill id: `kmind-markdown-to-mindmap`
