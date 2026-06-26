# KMind Markdown To Mind Map CN

[中文说明](./README_zh_CN.md)

Chinese-localized variant of the KMind Markdown-to-mindmap skill.

This bundle is intended for Chinese-speaking workflows and agent prompts. It converts Markdown heading outlines into KMind mind maps offline and supports:

- `PNG` export
- `SVG` export
- editable `.kmindz.svg` export

Recommended input is a hierarchy built with Markdown headings such as `#`, `##`, and `###`. Headings become mind map nodes. Non-heading body text under a heading becomes notes on that node. Image export shows notes as note-entry icons by default instead of expanding the note text. To view or continue editing those notes, export `.kmindz.svg` and open it in a KMind Zen client.

When the user simply asks for a mind map image, prefer PNG by default. Use SVG only when vector output is explicitly requested.

It keeps the same runtime behavior as the main skill, but exposes a Chinese-oriented skill identity and prompt surface.

## What This Repo Contains

- `SKILL.md`: localized skill instructions
- `scripts/kmind-render.mjs`: local entrypoint
- `scripts/vendor/*`: bundled KMind CLI runtime
- `agents/openai.yaml`: localized agent metadata

## Requirements

- Node.js installed locally
- For automatic `SVG` or `PNG` image export: a usable local Chromium browser
- No network connection is required for local conversion itself

## Quick Start

List available themes:

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

## Notes

- `.kmindz.svg` export does not require browser rendering
- Automatic image export requires a usable local Chromium browser
- Prefer PNG for normal image requests
- Long non-heading body text is stored as node notes. In exported images, those notes are represented by note icons instead of expanded text.
- If automatic browser launch is unavailable, use `--browser manual`

## Related

- KMind Zen: `https://kmind.app`
- Skill id: `kmind-markdown-to-mindmap-cn`
