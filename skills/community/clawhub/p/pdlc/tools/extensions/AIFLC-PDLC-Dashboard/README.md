# AIFLC PDLC Dashboard

**Version:** 0.4.0
**Extension Code:** AIFLC-PDLC-Dashboard

---

## What Is This?

An interactive HTML dashboard + VS Code extension for visualizing your PDLC family project lifecycle. Shows chain progress, package status, blockers, management framework, and more — driven by the AI-DFE data surface.

---

## Dual-Mode Access

### VS Code Extension Mode (Recommended)

Install the `.vsix` package:

```bash
code --install-extension tools/extensions/AIFLC-PDLC-Dashboard/extension/AIFLC-PDLC-Dashboard.vsix
```

Then open the command palette and run: **AIFLC: Open Dashboard**

The extension reads your `*-state.md` files live and renders the dashboard inside VS Code as a webview panel. Auto-refreshes when state files change.

### Browser Mode (Standalone)

Serve the `ui/` folder over HTTP:

```bash
cd tools/extensions/AIFLC-PDLC-Dashboard/ui
npx serve -p 8080
```

Open `http://localhost:8080/index.html`.

**Requirements for standalone:**
- A `dashboard-data.json` file in the `ui/` folder (or reachable via `REGISTRY.json`)
- Any HTTP server (`npx serve`, `python -m http.server`, VS Code Live Server, etc.)

### Quick Demo (no setup)

Open `demo/index.html` — it has sample data embedded inline and works without a server (even from `file://` with the built-in file picker).

---

## Populating Data

### VS Code Mode
Data is generated live from workspace state files. No manual population needed.

### Standalone Mode

Run AI-DFE to generate fresh data:
```
DAT__ all
```

Then copy to the dashboard:
```bash
copy data\dashboard-data.json tools\extensions\AIFLC-PDLC-Dashboard\ui\dashboard-data.json
```

Or use demo data for a quick preview:
```bash
copy tools\extensions\AIFLC-PDLC-Dashboard\demo\dashboard-data.json tools\extensions\AIFLC-PDLC-Dashboard\ui\dashboard-data.json
```

---

## What It Shows

- **Portfolio view** — all projects with status indicators
- **Package progress** — per-package phase/stage/artifact tracking
- **Chain diagram** — Mermaid flow visualization of the PDLC chain
- **Management framework** — decisions, risks, actions, issues, lessons
- **Ideas kanban** — idea lifecycle from capture to routing
- **PO view** — product vision, roadmap, backlog health, acceptance criteria
- **Architecture view** — C4 progress, ADRs, tech stack, integrations, NFRs
- **UX view** — personas, journeys, IA, flows, design system, accessibility
- **Statistics** — charts for status distribution and progress

---

## Data Resolution (Standalone)

The standalone page resolves data through a fallback chain:

1. **REGISTRY path** — fetches `REGISTRY.json` from the data root, reads the `dashboard-data.json` entry, fetches that file
2. **Direct fallback** — if REGISTRY fails, tries `dashboard-data.json` directly from the same directory
3. **Manual picker** — if both fail, shows a "Load data file…" button

Override the data root with: `?data=<relative-path-to-data-folder>`

---

## Troubleshooting

### "No data loaded" — Empty Dashboard

| Possible Cause | Fix |
|---------------|-----|
| `dashboard-data.json` missing from `ui/` folder | Copy it: `copy data\dashboard-data.json tools\extensions\AIFLC-PDLC-Dashboard\ui\dashboard-data.json` |
| Using `file://` protocol (double-clicked HTML) | Serve over HTTP: `npx serve -p 8080` from the `ui/` folder |
| Serving from wrong root | Use `?data=<path>` query param to point to the data folder |
| AI-DFE never ran | Run `DAT__ all` to generate data, then copy to `ui/` |

### Dashboard Shows Stale / Outdated Data

The `ui/dashboard-data.json` is a static copy. After each `DAT__` run:
```bash
copy data\dashboard-data.json tools\extensions\AIFLC-PDLC-Dashboard\ui\dashboard-data.json
```
Then hard-refresh the browser (Ctrl+Shift+R).

### Specific Tabs Empty (PO, Architect, UX)

Each tab is populated by a specific package:
| Tab | Source Package | When Populated |
|-----|---------------|----------------|
| PO | AI-POLC | After Product Ownership lifecycle runs |
| Architect | AI-ADLC | After Architecture Design lifecycle runs |
| UX | AI-UXD | After UX Design lifecycle runs |

Tabs show as empty until their source package has been executed. This is expected — not an error.

### Chain Diagram Not Rendering

Requires internet — Mermaid.js loads from CDN (`cdn.jsdelivr.net`). Offline? The Chain tab still works but without the visual diagram.

### VS Code Panel Blank

1. Ensure at least one package has been run (state files must exist)
2. Reopen the panel (Command Palette → **AIFLC: Open Dashboard**)
3. Check Developer Console (Help → Toggle Developer Tools) for errors

### CORS / Security Errors

Don't open `index.html` via `file://`. Use an HTTP server:
```bash
npx serve -p 8080
```

---

## Theme Support

- Dark theme (default)
- Light theme (toggle via ☀/🌙 button)
- Respects VS Code theme in extension mode

---

## Requirements

- **Browser mode:** Any modern browser + HTTP server
- **VS Code mode:** VS Code 1.80+
- **Mermaid CDN:** Required for chain diagrams (loaded from `cdn.jsdelivr.net`)

---

## Further Reading

See `knowledge_docs/HOW_TO_USE_THE_DASHBOARD.md` for the complete operational guide with advanced configuration, data refresh workflows, and file layout reference.

---

*Part of [AIFLC](../../../README.md) — the AI-* PDLC Family*
