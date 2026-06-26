---
name: markmap
description: markmap — Render Markdown as interactive SVG mindmaps. Use when users need to convert Markdown documents into mindmaps, generate HTML files via CLI, or navigate mindmap nodes interactively in the browser.
---

# Markmap — Build mindmaps with plain text

Markdown → interactive SVG mindmaps. Powered by markdown-it + d3-flextree.

## Quick Start

```bash
npm install -g markmap-cli
markmap README.md --open          # Generate interactive HTML mindmap
markmap README.md --offline       # Offline standalone HTML
```

## Core API

```ts
import { Transformer } from 'markmap-lib';
import { Markmap } from 'markmap-view';
const { root } = new Transformer().transform('# Hello\n- World');
Markmap.create('#mindmap', { zoom: true }, root);
```

## Reference Files

| File | Coverage |
|------|----------|
| references/transform.md | Transformer + Frontmatter + HTML Parser + CDN + Vite Build |
| references/render.md | Markmap Rendering + deriveOptions + Full HTML Examples |
| references/cli.md | CLI Commands + Programmatic API + Dev Server Architecture |
| references/architecture.md | Package Architecture + Markdown→SVG Pipeline + Asset Loading |
| references/common-api.md | All Options/Node Types + CSS Variables + Hook/Loader |
| references/plugins.md | 6 Built-in Plugins + Custom Plugins |