# How to Use the Dashboard

**Purpose:** Complete guide to running the AIFLC PDLC Dashboard — in the browser, in VS Code, or from any HTTP server. Covers setup, data population, troubleshooting common failures, and keeping data fresh.

---

## What the Dashboard Is

The AIFLC PDLC Dashboard is a visual interface that shows your project lifecycle at a glance — package progress, chain flow, management framework, product ownership, architecture, and UX status. It runs in two modes: as a **VS Code extension** (live data) or as a **standalone HTML page** (static data, zero dependencies beyond a browser).

---

## Mode 1: VS Code Extension (Recommended)

### Install

```bash
code --install-extension tools/extensions/AIFLC-PDLC-Dashboard/extension/AIFLC-PDLC-Dashboard.vsix
```

### Open

Command Palette → **AIFLC: Open Dashboard**

### How Data Flows

The extension reads your workspace's `*-state.md` files, shapes them into the dashboard format, and injects the data directly into the webview. No external files or HTTP servers needed — data is always live.

### Refresh

The panel auto-refreshes when state files change. To force a refresh, close and reopen the panel.

---

## Mode 2: Standalone Browser (HTTP Server)

### Quick Start

1. Navigate to the `ui/` folder:
   ```bash
   cd tools/extensions/AIFLC-PDLC-Dashboard/ui
   ```
2. Start any HTTP server:
   ```bash
   npx serve -p 8080
   ```
   or:
   ```bash
   python -m http.server 8080
   ```
3. Open `http://localhost:8080/index.html`

### How Data Flows (Standalone)

The standalone page resolves data through a fallback chain:

1. **REGISTRY path** — fetches `REGISTRY.json` from the data root, reads the entry for `dashboard-data.json`, then fetches that file. This is the AI-DFE consumer contract path (works when served from workspace root with the data surface populated).
2. **Direct file fallback** — if REGISTRY fails (404, no entry), tries loading `dashboard-data.json` directly from the same directory as `index.html`.
3. **Manual file picker** — if both fail, shows an empty state with a "Load data file…" button for manual JSON upload.

### Populating Data (Standalone)

Before the standalone dashboard can show anything, it needs a `dashboard-data.json` file. There are two ways to get one:

**Option A: Run AI-DFE (recommended)**

In your AI assistant session:
```
DAT__ all
```

This gathers data from all packages, shapes it, and writes `dashboard-data.json` to your workspace's `data/` folder. Then copy it to the dashboard's `ui/` folder:

```bash
copy data\dashboard-data.json tools\extensions\AIFLC-PDLC-Dashboard\ui\dashboard-data.json
```

**Option B: Use the demo data**

The `demo/` folder includes a pre-populated `dashboard-data.json` with sample data:
```bash
copy tools\extensions\AIFLC-PDLC-Dashboard\demo\dashboard-data.json tools\extensions\AIFLC-PDLC-Dashboard\ui\dashboard-data.json
```

---

## Mode 3: Direct File (file://)

Opening `index.html` directly in a browser (double-click) uses the `file://` protocol. Browsers block network requests from `file://` origins, so automatic data loading is disabled. You have two options:

- **Use the file picker** — the empty state shows a "Load data file…" button. Click it and select your `dashboard-data.json` from disk.
- **Switch to HTTP** — serve the folder over HTTP as shown in Mode 2.

---

## Troubleshooting

### "No data loaded" / Empty Dashboard

**Cause:** The page cannot find `dashboard-data.json`.

**Fix checklist:**
1. Confirm `dashboard-data.json` exists in the same folder as `index.html`:
   ```
   tools/extensions/AIFLC-PDLC-Dashboard/ui/
   ├── index.html
   ├── dashboard.js
   ├── styles.css
   └── dashboard-data.json   ← must exist here
   ```
2. If missing, populate it:
   - Run `DAT__ all` then copy from `data/dashboard-data.json`, or
   - Copy from `demo/dashboard-data.json` for sample data
3. If serving from a non-standard root, use the `?data=` query parameter to point to the folder containing `REGISTRY.json` or `dashboard-data.json`:
   ```
   http://localhost:8080/index.html?data=../../data
   ```

### Dashboard Loads But Shows Stale Data

**Cause:** The `ui/dashboard-data.json` is a static copy. When you run `DAT__ all`, only the canonical file at `data/dashboard-data.json` is updated — the `ui/` copy doesn't auto-refresh.

**Fix:** After each `DAT__` run, copy the fresh file:
```bash
copy data\dashboard-data.json tools\extensions\AIFLC-PDLC-Dashboard\ui\dashboard-data.json
```

Then hard-refresh the browser (Ctrl+Shift+R / Cmd+Shift+R).

### Tabs Show "null" or Missing Panes (PO, Architect, UX)

**Cause:** Those panes are populated by specific packages (AI-POLC → PO tab, AI-ADLC → Architect tab, AI-UXD → UX tab). If those packages haven't been run yet, their data is `null` and the pane is empty.

**Fix:** This is expected behavior — the dashboard degrades gracefully for packages not yet executed. Run the corresponding package, then refresh data:
```
DAT__ all
```

### Chain Diagram Not Rendering

**Cause:** The chain diagram uses Mermaid.js loaded from a CDN (`cdn.jsdelivr.net`). If you're offline or the CDN is blocked, the diagram won't render.

**Fix:**
- Check internet connectivity
- If working offline, the chain data is still visible in the Chain tab as text — only the visual diagram is affected

### VS Code Extension: Panel Is Blank

**Cause:** The extension generates dashboard HTML from workspace state files. If no state files exist yet (no packages have been run), there's nothing to display.

**Fix:**
1. Run at least one package (e.g., AI-ILC or AI-PILC) to generate state files
2. Reopen the dashboard panel
3. If state files exist but the panel is still blank, check the VS Code Developer Console (Help → Toggle Developer Tools) for errors

### Served from Workspace Root But Still 404

**Cause:** When serving from the workspace root, the URL path to the dashboard changes:
```
http://localhost:8080/tools/extensions/AIFLC-PDLC-Dashboard/ui/index.html
```

The data root defaults to `.` (the folder containing `index.html`), which is `ui/`. If your `dashboard-data.json` is at `data/dashboard-data.json` relative to workspace root, the dashboard can't find it without help.

**Fix:** Use the `?data=` query parameter:
```
http://localhost:8080/tools/extensions/AIFLC-PDLC-Dashboard/ui/index.html?data=../../../../data
```

Or set `window.DASHBOARD_DATA_ROOT` before the loading script:
```html
<script>window.DASHBOARD_DATA_ROOT = '../../../../data';</script>
```

### Browser Shows Security/CORS Errors

**Cause:** Opening via `file://` triggers CORS restrictions on fetch requests.

**Fix:** Use an HTTP server (Mode 2). Even a simple one-liner works:
```bash
npx serve -p 8080
```

---

## Data Refresh Workflow

| Step | Command | What Happens |
|------|---------|--------------|
| 1. Gather | `DAT__ all` | AI-DFE reads all `*-state.md` files, shapes `dashboard-data.json` |
| 2. Copy (standalone only) | `copy data\dashboard-data.json tools\extensions\AIFLC-PDLC-Dashboard\ui\dashboard-data.json` | Static UI copy updated |
| 3. Refresh | Hard-refresh browser / reopen VS Code panel | Dashboard shows fresh data |

For VS Code mode, only step 1 is needed — the extension reads state files directly.

---

## Configuration Options

| Option | Method | Example |
|--------|--------|---------|
| Custom data root | `?data=<path>` query param | `?data=../../data` |
| Override globally | `window.DASHBOARD_DATA_ROOT = '<path>'` before loading script | Set in a wrapper HTML |
| Use REGISTRY | Place `REGISTRY.json` in the data root folder | Standard AI-DFE surface |
| Direct file | Place `dashboard-data.json` alongside `index.html` | Simplest standalone setup |

---

## File Layout Reference

```
tools/extensions/AIFLC-PDLC-Dashboard/
├── ui/                        ← Standalone browser mode
│   ├── index.html             ← Entry point
│   ├── dashboard.js           ← Rendering logic
│   ├── styles.css             ← Themes (dark/light)
│   └── dashboard-data.json    ← Data file (populate manually or via DAT__)
│
├── demo/                      ← Sample data for quick preview
│   ├── index.html             ← Self-contained demo (data embedded)
│   ├── dashboard.js
│   ├── styles.css
│   └── dashboard-data.json    ← Pre-populated sample data
│
├── extension/                 ← VS Code extension
│   └── AIFLC-PDLC-Dashboard.vsix
│
├── data-demand/               ← AI-DFE consumer contract
│   └── dashboard-data.demand.md
│
├── data-contract/             ← Schema pointer (owned by AI-DFE)
│   └── POINTER.md
│
└── README.md                  ← Quick-start guide
```

---

## Related Documents

| Document | Location |
|----------|----------|
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How the Flow Orchestrator Works | `knowledge_docs/HOW_FLOW_ORCHESTRATOR_WORKS.md` |
| How Portfolio Management Works | `knowledge_docs/HOW_PORTFOLIO_MANAGEMENT_WORKS.md` |
| How Package Installation Works | `knowledge_docs/HOW_PACKAGE_INSTALLATION_WORKS.md` |

*Knowledge Document | Created: 2026-06-28 | Updated: 2026-06-28 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
