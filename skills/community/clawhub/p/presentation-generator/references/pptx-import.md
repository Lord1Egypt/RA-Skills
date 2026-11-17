# Import from PowerPoint

Turn an existing `.pptx` into a presentation-md **deck JSON** so you can theme it,
edit layouts, render HTML, and re-export editable PowerPoint.

## CLI

```bash
presentation-md-render --from-pptx ./board-deck.pptx -o deck.json --theme claude
```

Optional `--assets-dir ./assets` writes extracted images to disk (relative paths in the deck)
instead of embedding data URIs.

## MCP

```
import_pptx
  pptx_path: "./board-deck.pptx"   # OR pptx_base64
  theme: "claude"                  # optional
  output_path: "./deck.json"       # optional
```

## Agent workflow

1. **Import** — run the CLI or `import_pptx` tool.
2. **Review** — check `warnings` and skim slide layouts (`title`, `feature-grid`, `data-table`, …).
   Adjust layouts/copy in the deck JSON when the heuristics guessed wrong.
3. **Theme** — `apply_theme` or set `meta.theme` (`list_themes` for options).
4. **Render / export** — `render_deck` for HTML, `export_deck` for `.pptx`.

## Fidelity notes

Import is **content + best-fit layout**, not a pixel clone. Animations, masters, charts, and
EMF/WMF images are skipped (with warnings). Images become data URIs by default so a later
export round-trip can embed them again.
