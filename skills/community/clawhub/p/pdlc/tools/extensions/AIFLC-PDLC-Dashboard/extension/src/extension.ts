import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

let panel: vscode.WebviewPanel | undefined;

export function activate(context: vscode.ExtensionContext) {

    // Command: Open Dashboard
    const openCmd = vscode.commands.registerCommand('aiflc-pdlc-dashboard.open', () => {
        if (panel) {
            panel.reveal();
            refreshPanel(context);
            return;
        }

        panel = vscode.window.createWebviewPanel(
            'aiflcDashboard',
            'AIFLC Dashboard',
            vscode.ViewColumn.Beside,
            {
                enableScripts: true,
                retainContextWhenHidden: true,
                localResourceRoots: [
                    vscode.Uri.file(path.join(context.extensionPath, '..', 'ui'))
                ]
            }
        );

        refreshPanel(context);
        panel.onDidDispose(() => { panel = undefined; });

        // Handle messages from webview — open a referenced file in the editor
        panel.webview.onDidReceiveMessage(
            (message) => {
                if (message.type === 'openFile' && message.path) {
                    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
                    if (workspaceFolder) {
                        const filePath = path.join(workspaceFolder.uri.fsPath, message.path);
                        if (fs.existsSync(filePath)) {
                            vscode.window.showTextDocument(vscode.Uri.file(filePath));
                        }
                    }
                }
            },
            undefined,
            context.subscriptions
        );
    });

    // Command: Refresh Dashboard
    const refreshCmd = vscode.commands.registerCommand('aiflc-pdlc-dashboard.refresh', () => {
        if (panel) { refreshPanel(context); }
    });

    // File watcher: auto-refresh when the AI-DFE data surface changes.
    // Option B — the dashboard reads ONLY the data fabric, never *-state.md directly.
    const watcher = vscode.workspace.createFileSystemWatcher('**/data/{REGISTRY.json,dashboard-data.json}');
    watcher.onDidChange(() => { if (panel) { refreshPanel(context); } });
    watcher.onDidCreate(() => { if (panel) { refreshPanel(context); } });

    context.subscriptions.push(openCmd, refreshCmd, watcher);
}

/**
 * Build the webview HTML — loads CSS + JS from the sibling ui/ folder,
 * injects the dashboard payload produced by AI-DFE.
 */
async function refreshPanel(context: vscode.ExtensionContext) {
    if (!panel) return;

    const result = await loadDashboardData();
    const dataJSON = JSON.stringify(result.data);

    // Find UI files from extension-relative paths
    let cssContent = '';
    let jsContent = '';

    const possibleUIPaths = [
        path.join(context.extensionPath, '..', 'ui'),
        path.join(context.extensionPath, 'ui')
    ];

    if (vscode.workspace.workspaceFolders) {
        for (const folder of vscode.workspace.workspaceFolders) {
            const root = folder.uri.fsPath;
            const candidates = [
                path.join(root, 'tools', 'extensions', 'AIFLC-PDLC-Dashboard', 'ui'),
                ...findDirsMatching(root, 'AIFLC-PDLC-Dashboard', 3)
            ];
            candidates.forEach(p => { if (!possibleUIPaths.includes(p)) possibleUIPaths.push(p); });
        }
    }

    for (const uiPath of possibleUIPaths) {
        const cssFile = path.join(uiPath, 'styles.css');
        const jsFile = path.join(uiPath, 'dashboard.js');
        if (fs.existsSync(cssFile) && fs.existsSync(jsFile)) {
            cssContent = fs.readFileSync(cssFile, 'utf-8');
            jsContent = fs.readFileSync(jsFile, 'utf-8');
            break;
        }
    }

    if (!cssContent) { cssContent = '/* UI files not found */'; }
    if (!jsContent) { jsContent = 'document.body.innerHTML="<p>Dashboard UI files not found.</p>";'; }

    // Notice banner when the data fabric hasn't produced data yet.
    const notice = result.found ? '' : `<div class="notice" style="padding:10px 16px;background:#5a3a00;color:#ffd479;font-size:13px;">
      No data fabric output found. ${escapeHtml(result.message)} Run <code>DAT__ all</code> (AI-DFE) to populate <code>${escapeHtml(result.expectedPath)}</code>.
    </div>`;

    panel.webview.html = `<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIFLC Dashboard</title>
<style>${cssContent}</style>
</head>
<body>
<div class="topbar">
  <span class="topbar-title">AIFLC : AI-* PDLC Family</span>
  <span class="badge" id="overall-badge">0%</span>
  <button class="theme-toggle" onclick="toggleTheme()">\u2600/\uD83C\uDF19</button>
</div>
${notice}
<div class="main">
  <div class="panel-left">
    <div class="tabs" id="left-tabs">
      <div class="tab active" data-tab="portfolio">Portfolio</div>
      <div class="tab" data-tab="ideas">Ideas</div>
      <div class="tab" data-tab="stats-left">Stats</div>
    </div>
    <div class="tab-content active" id="tc-portfolio"></div>
    <div class="tab-content" id="tc-ideas"></div>
    <div class="tab-content" id="tc-stats-left"></div>
  </div>
  <div class="panel-right">
    <h2 id="right-header" style="color:var(--text-heading);margin-bottom:12px;font-size:16px;">Select a project</h2>
    <div class="tabs" id="right-tabs">
      <div class="tab active" data-tab="pm">PM</div>
      <div class="tab" data-tab="po" style="display:none;">PO</div>
      <div class="tab" data-tab="architect" style="display:none;">Architect</div>
      <div class="tab" data-tab="ux" style="display:none;">UX</div>
      <div class="tab" data-tab="chain">Chain</div>
      <div class="tab" data-tab="mgmt">MF</div>
      <div class="tab" data-tab="stats-right">Stats</div>
    </div>
    <div class="tab-content active" id="tc-pm"></div>
    <div class="tab-content" id="tc-po"></div>
    <div class="tab-content" id="tc-architect"></div>
    <div class="tab-content" id="tc-ux"></div>
    <div class="tab-content" id="tc-chain"><div id="chain-container"><div class="mermaid" id="chain-mermaid"></div></div></div>
    <div class="tab-content" id="tc-mgmt"></div>
    <div class="tab-content" id="tc-stats-right"></div>
  </div>
</div>
<div class="footer">AIFLC PDLC Dashboard v0.4.0 <span id="footer-date"></span></div>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>var D = ${dataJSON};</script>
<script>${jsContent}</script>
</body>
</html>`;
}

// ─── Data Loading (Option B — AI-DFE data fabric is the SOLE source) ─────────

interface LoadResult { found: boolean; data: any; message: string; expectedPath: string; }

/**
 * Load the dashboard payload from the AI-DFE data surface.
 *
 * Resolution (per the consumer contract — Decision §4.4):
 *   1. Locate REGISTRY.json under a data folder in the workspace.
 *   2. Read the registry, find the `dashboard-data.json` entry, resolve its path.
 *   3. Read that file and return its `data` payload (the envelope body).
 *
 * The dashboard NEVER parses `*-state.md` files directly and NEVER hardcodes a
 * data-file path — everything resolves through REGISTRY.json.
 */
async function loadDashboardData(): Promise<LoadResult> {
    const expectedPath = '{family}-ws/data/REGISTRY.json';
    const folders = vscode.workspace.workspaceFolders;
    if (!folders) {
        return { found: false, data: emptyData(), message: 'No workspace open.', expectedPath };
    }

    // 1. Find REGISTRY.json under any */data/ folder (e.g. pdlc-ws/data/REGISTRY.json).
    const registryFiles = await vscode.workspace.findFiles(
        '**/data/REGISTRY.json',
        '{**/node_modules/**,**/templates/**,**/rule-details/**}',
        5
    );
    if (registryFiles.length === 0) {
        return { found: false, data: emptyData(), message: 'REGISTRY.json not found.', expectedPath };
    }

    const registryUri = registryFiles[0];
    const dataRoot = path.dirname(registryUri.fsPath);

    let registry: any;
    try {
        const bytes = await vscode.workspace.fs.readFile(registryUri);
        registry = JSON.parse(Buffer.from(bytes).toString('utf-8'));
    } catch {
        return { found: false, data: emptyData(), message: 'REGISTRY.json could not be parsed.', expectedPath };
    }

    // 2. Find the dashboard-data.json entry in the registry.
    const entry = registry?.files?.['dashboard-data.json'];
    if (!entry) {
        return { found: false, data: emptyData(), message: 'No dashboard-data.json registered.', expectedPath: path.join(dataRoot, 'dashboard-data.json') };
    }

    // Resolve the data-file path: prefer registry path relative to workspace root,
    // fall back to the sibling of REGISTRY.json.
    const wsRoot = folders[0].uri.fsPath;
    const candidatePaths = [
        entry.path ? path.join(wsRoot, entry.path) : null,
        path.join(dataRoot, 'dashboard-data.json')
    ].filter(Boolean) as string[];

    for (const candidate of candidatePaths) {
        if (fs.existsSync(candidate)) {
            try {
                const parsed = JSON.parse(fs.readFileSync(candidate, 'utf-8'));
                // DFE wraps payloads in a metadata envelope; the UI consumes `.data`.
                const payload = (parsed && typeof parsed === 'object' && parsed.data) ? parsed.data : parsed;
                return { found: true, data: payload, message: '', expectedPath: candidate };
            } catch {
                return { found: false, data: emptyData(), message: 'dashboard-data.json could not be parsed.', expectedPath: candidate };
            }
        }
    }

    return { found: false, data: emptyData(), message: 'dashboard-data.json not yet produced.', expectedPath: candidatePaths[0] };
}

function emptyData(): any {
    return {
        generated: new Date().toISOString(),
        projects: [],
        ideas: [],
        ppm: { totalProjects: 0, dispatched: 0, pending: 0, strategicFit: 0, topPriority: '' },
        health: { totalBlockers: 0, stalledProjects: 0, overallProgress: 0 }
    };
}

function escapeHtml(s: string): string {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/**
 * Recursively find directories matching a target name up to maxDepth levels.
 * Returns paths to `{match}/ui` if it exists.
 */
function findDirsMatching(root: string, targetName: string, maxDepth: number): string[] {
    const results: string[] = [];
    function walk(dir: string, depth: number) {
        if (depth > maxDepth) return;
        try {
            const entries = fs.readdirSync(dir, { withFileTypes: true });
            for (const entry of entries) {
                if (!entry.isDirectory()) continue;
                if (entry.name === 'node_modules' || entry.name === '.git') continue;
                const fullPath = path.join(dir, entry.name);
                if (entry.name === targetName) {
                    const uiPath = path.join(fullPath, 'ui');
                    if (fs.existsSync(uiPath)) results.push(uiPath);
                } else {
                    walk(fullPath, depth + 1);
                }
            }
        } catch { /* permission denied or broken symlink */ }
    }
    walk(root, 0);
    return results;
}

export function deactivate() {}
