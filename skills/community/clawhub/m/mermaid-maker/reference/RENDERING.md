# Rendering & Export Backends

`mermaid-maker` can render `.mmd` through three backends. Pick by what you need to ship.

| Backend | Outputs | Install | Themes | Best for |
|---------|---------|---------|--------|----------|
| **beautiful-mermaid** (`scripts/`) | SVG, ASCII | Node only (auto-installs dep) | 15 curated themes + custom palette | Polished docs/web SVG, terminal/README ASCII, batch |
| **mmdc** (mermaid-cli) | PNG, SVG, PDF | npm + headless Chrome | 4 standard (`default`/`dark`/`neutral`/`forest`) | Raster PNG, PDF, offline |
| **Kroki API** | PNG, SVG | none (just `curl`) | standard via `%%{init}%%` | No-install / CI without Node |

beautiful-mermaid does **not** emit PNG or PDF — for those use mmdc. For a no-install path use Kroki.

---

## Backend 1 — beautiful-mermaid (themed SVG / ASCII / batch)

The Node scripts in `scripts/` wrap the `beautiful-mermaid` library. The dependency auto-installs into the skill folder on first run; no manual setup needed (manual fallback: `cd` to the skill root and `npm install`).

### Single render
```bash
# Themed SVG
node scripts/render.mjs --input diagram.mmd --output diagram.svg --theme tokyo-night

# ASCII to stdout (terminal / README)
node scripts/render.mjs --input diagram.mmd --format ascii --use-ascii
```

### Render flags (`render.mjs`)
| Flag | Meaning |
|------|---------|
| `-i, --input <file>` | Input `.mmd` (required) |
| `-o, --output <file>` | Output file (default: stdout) |
| `-f, --format <fmt>` | `svg` (default) or `ascii` |
| `-t, --theme <name>` | Theme name (see `THEMES.md`) |
| `--bg / --fg` | Background / foreground hex (mono custom theme) |
| `--accent / --muted / --line / --surface / --border` | Enriched custom palette |
| `--font <name>` | Font family (default: Inter) |
| `--transparent` | Transparent background (SVG only) |
| `--use-ascii` | Pure ASCII instead of Unicode (ASCII only) |
| `--padding-x / --padding-y / --box-border-padding <n>` | ASCII spacing |

### Custom palette (no theme)
```bash
node scripts/render.mjs --input diagram.mmd --output custom.svg \
  --bg "#1a1b26" --fg "#a9b1d6" --accent "#7aa2f7"
```

### Batch render (`batch.mjs`)
```bash
node scripts/batch.mjs --input-dir ./diagrams --output-dir ./output \
  --format svg --theme dracula --workers 4
```
Flags mirror `render.mjs` plus `-i/--input-dir`, `-o/--output-dir`, `-w/--workers <n>` (default 4; use 8 for 10+ files). SVG → `.svg`, ASCII → `.txt`.

### List themes
```bash
node scripts/themes.mjs
```

---

## Backend 2 — mmdc (PNG / SVG / PDF, offline)

```bash
npm install -g @mermaid-js/mermaid-cli
npx puppeteer browsers install chrome-headless-shell   # required — mmdc renders via Puppeteer
mmdc --version
```
> `mmdc --version` succeeds even with **no** Chrome installed, but every export then fails with `Could not find Chrome`. Install the browser above (or set `PUPPETEER_EXECUTABLE_PATH` to a system Chrome). If you can't, use Kroki — it needs no browser.

```bash
# PNG (recommended: 2048px wide, white background)
mmdc -i diagram.mmd -o diagram.png -w 2048 --backgroundColor white

# PNG with a standard theme — valid -t values: default | dark | neutral | forest
# (`base` is NOT a valid -t value; it only works inside a %%{init: {'theme':'base'}}%% directive)
mmdc -i diagram.mmd -o diagram.png -w 2048 --backgroundColor white --theme neutral

# SVG / PDF
mmdc -i diagram.mmd -o diagram.svg
mmdc -i diagram.mmd -o diagram.pdf
```

---

## Backend 3 — Kroki API (no install)

```bash
# SVG
curl -X POST -H "Content-Type: text/plain" --data-binary @diagram.mmd https://kroki.io/mermaid/svg -o diagram.svg

# PNG
curl -X POST -H "Content-Type: text/plain" --data-binary @diagram.mmd https://kroki.io/mermaid/png -o diagram.png

# PDF is NOT supported by Kroki for Mermaid — POSTing to /mermaid/pdf returns
# HTTP 400 ("Unsupported output format: pdf for mermaid. Must be one of png or svg").
# For PDF, use the local mmdc path instead:  mmdc -i diagram.mmd -o diagram.pdf
```

Kroki needs only `curl`, works in CI without Node, and also serves 20+ other diagram types (PlantUML, GraphViz, D2, …).

---

## Validation (run before exporting)

Validate by doing a trial render with whichever backend you'll ship. **Never export without validating first.**

```bash
# beautiful-mermaid (parse errors surface immediately)
node scripts/render.mjs -i diagram.mmd -o /tmp/test.svg

# mmdc
mmdc -i diagram.mmd -o /tmp/test.png 2>&1

# Kroki
curl -s -X POST -H "Content-Type: text/plain" --data-binary @diagram.mmd https://kroki.io/mermaid/svg -o /tmp/test.svg && echo "Valid" || echo "Invalid"
```

Common validation errors: missing quotes around labels with special characters; wrong arrow syntax (`->>` for sequence, `-->` for flowchart); undeclared participants in sequence diagrams.

> A `Could not find Chrome`/puppeteer error from `mmdc` is a **setup** problem, not a diagram error — the `.mmd` may be perfectly valid. Install the browser or validate via Kroki / beautiful-mermaid instead of "fixing" correct syntax.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `Cannot find module 'beautiful-mermaid'` | Should auto-install; else `npm install` in the skill root |
| `mmdc: command not found` | `npm install -g @mermaid-js/mermaid-cli` |
| `mmdc` error `Could not find Chrome` | `npx puppeteer browsers install chrome-headless-shell` (or use Kroki) |
| Valid diagram reported "invalid" by `mmdc` | It's a Chrome/puppeteer setup failure, not syntax — don't rewrite the `.mmd` |
| Kroki PDF fails HTTP 400 | Kroki does PNG/SVG only for Mermaid; use mmdc for PDF |
| `Parse error on line N` | Check missing spaces in `A --> B`, node shape syntax, unclosed brackets; test at https://mermaid.live |
| `Input file not found` | Verify the path; use an absolute path if needed |
| Blank / tiny PNG | Add `-w 2048` (mmdc) |
| Wrong arrow in sequence | `->>` request, `-->>` response |
| Special chars in label | Quote it: `A["Label: value"]` |
| Subgraph name with spaces | Quote it: `subgraph "My Layer"` |
