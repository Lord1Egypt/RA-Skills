---
name: kmind-markdown-to-mindmap
description: Convert Markdown heading outlines into themed KMind mind maps. Export PNG or SVG images with theme presets, layouts, edge routes, dark mode, and rainbow branches.
version: 0.1.1
user-invocable: true
metadata: {"openclaw":{"skillKey":"kmind-markdown-to-mindmap","emoji":"🧠","requires":{"bins":["node"],"config":["browser.enabled"]}}}
---

KMind Zen is a professional mind mapping product with a desktop app, web app, SiYuan plugin, and Obsidian plugin. The official website is `https://kmind.app`.

This skill converts Markdown heading outlines into KMind mind map images. It is a fully offline skill and does not require any network connection for local conversion.

The best input is a hierarchy built with Markdown headings such as `#`, `##`, and `###`. Headings become mind map nodes. Non-heading body text under a heading becomes notes on that node. During image export, notes are shown as note-entry icons by default instead of expanded note text. To view or continue editing those notes, export `.kmindz.svg` and open it in a KMind Zen client.

Its main advantage is that it can generate polished, visually consistent mind maps locally and offline. It exports PNG or SVG images and supports theme presets, root layouts, branch edge routes, light/dark appearance, and rainbow branches. When the user simply asks for a mind map image, default to PNG. Use SVG only when the user explicitly asks for vector output.

When the user wants an editable KMind package, prefer exporting `.kmindz.svg`. A `.kmindz.svg` package can be imported into any KMind Zen client for seamless editing. Even when no client is installed, the map content can still be opened and viewed quickly as an SVG file first, then imported into a client later for continued editing.

Useful for meeting outlines, reading notes, brainstorming lists, project proposals, and Markdown heading outline-to-mindmap workflows.

This is a publishable, self-contained skill. Always invoke the bundled entrypoint from `{baseDir}`:

`node {baseDir}/scripts/kmind-render.mjs ...`

Workflow:

1. If the user wants a specific theme, layout, or edge-route style, inspect the available options first:
   `node {baseDir}/scripts/kmind-render.mjs themes --format json`
2. If the user provides raw Markdown text instead of a file path, pass it through stdin.
3. Start the export with `render-markdown`.
4. By default, the command tries to auto-launch the user's local Chromium browser in headless mode.
5. The first stdout line is a JSON object with `status: "ready"`.
6. When the command finishes, the last stdout line is a JSON object with `status: "done"` and the final `outputPath`.
7. Only use `--browser manual` when automatic browser launch is unavailable and you need to open the printed local URL yourself.

If the user's machine has no usable Chromium browser, automatic SVG / PNG export is unavailable. In that case, either use `--browser manual` to open the local page and complete the export, or clearly report that automatic export is unavailable in this environment. Do not fake success.

Useful command template (default recommendation: PNG):

`node {baseDir}/scripts/kmind-render.mjs render-markdown INPUT_OR_DASH --output OUTPUT.png --theme-preset PRESET_ID --layout LAYOUT_ID --edge-route EDGE_ROUTE_ID --appearance light|dark --rainbow auto|on|off --png-scale 1 --browser auto`

Parameter guidance:

- `--output` decides the output format when `--image-format` is omitted: `.png` means bitmap output and `.svg` means vector output. When the user simply asks for a mind map image, prefer `.png` by default.
- `--theme-preset` should be chosen from the `themes` output. Recommended candidates:
  `kmind-material-3-slate`
  `kmind-rainbow-breeze`
  `kmind-midnight-neon`
  `kmind-material-3-rounded-orthogonal-ocean`
  `kmind-material-3-rounded-orthogonal-forest`
- `--layout` should be chosen from the `themes` output. Common choices:
  `logical-right`
  `logical-left`
  `mindmap-both-auto`
- `--edge-route` should be chosen from the `themes` output. Common choices:
  `cubic`
  `edge-lead-quadratic`
  `center-quadratic`
  `orthogonal`
- `--appearance dark` forces dark mode.
- `--rainbow on` forcibly enables rainbow branches even if the current theme does not enable them by default.
- `--png-scale 1` matches the current webapp default export. Only raise it when the user explicitly asks for a higher-resolution PNG.
- `--browser auto` is the default and tries to auto-launch the local browser.
- `--browser manual` is the manual fallback mode.
- Do not proactively surface `--svg-mode` or `--png-mode`. Internally, the current defaults already use the combination closest to the webapp's actual export behavior: `SVG=fidelity`, `PNG=accurate`. Only mention those advanced flags when the user explicitly asks for low-level export tuning.
- Image export uses the card-style node body layout close to KMind Zen webapp behavior. Notes converted from non-heading body text are not expanded in the image and are shown as note-entry icons.

Defaults when the user does not specify:

- `theme-preset`: `kmind-material-3-slate`
- recommended image output suffix: `.png`
- `image-format`: inferred from `--output` first; fall back to `svg` if it cannot be inferred
- `layout`: by default, do not explicitly override it; keep KMind's default root layout
- `edge-route`: by default, do not explicitly override it; keep the preset theme's edge style
- `appearance`: `light`
- `rainbow`: `auto`
- `svg-mode`: internal default `fidelity`
- `png-mode`: internal default `accurate`
- `png-scale`: `1`
- `viewport-width`: `1600`
- `viewport-height`: `900`

Current publish-safe allowlist for this skill:

- `layouts`: `logical-right`, `logical-left`, `mindmap-both-auto`
- `edge-routes`: `cubic`, `edge-lead-quadratic`, `center-quadratic`, `orthogonal`

If the user wants a KMind project file instead of an image, do not use this image export flow. Use:

`node {baseDir}/scripts/kmind-render.mjs import-markdown INPUT_OR_DASH --output OUTPUT.kmindz.svg`
