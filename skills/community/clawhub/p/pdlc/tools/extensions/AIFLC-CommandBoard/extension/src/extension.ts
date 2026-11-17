import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

let panel: vscode.WebviewPanel | undefined;

export function activate(context: vscode.ExtensionContext) {

    const openCmd = vscode.commands.registerCommand('aiflc-commandboard.open', () => {
        if (panel) {
            panel.reveal();
            return;
        }

        panel = vscode.window.createWebviewPanel(
            'aiflcCommandBoard',
            'AIFLC Command Board',
            vscode.ViewColumn.Beside,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        panel.webview.html = buildHTML(context);
        panel.onDidDispose(() => { panel = undefined; });

        // Handle messages from webview
        panel.webview.onDidReceiveMessage(
            (message) => {
                if (message.type === 'copyTrigger' && message.key) {
                    vscode.env.clipboard.writeText(message.key);
                    vscode.window.showInformationMessage(`Copied: ${message.key}`);
                }
            },
            undefined,
            context.subscriptions
        );
    });

    context.subscriptions.push(openCmd);
}

function buildHTML(context: vscode.ExtensionContext): string {
    let cssContent = '';
    let jsContent = '';
    let triggerData = '{}';

    const possiblePaths = [
        path.join(context.extensionPath, '..', 'ui'),
        path.join(context.extensionPath, 'ui')
    ];

    // Dynamically search workspace for the extension's UI files
    if (vscode.workspace.workspaceFolders) {
        for (const folder of vscode.workspace.workspaceFolders) {
            const root = folder.uri.fsPath;
            // Search common patterns where extensions land
            const searchDirs = [
                'tools/extensions/AIFLC-CommandBoard/ui',
                '**/tools/extensions/AIFLC-CommandBoard/ui',
                '**/AIFLC-CommandBoard/ui'
            ];
            // Walk known depth levels (avoids expensive deep recursion)
            const candidates = [
                path.join(root, 'tools', 'extensions', 'AIFLC-CommandBoard', 'ui'),
                ...findDirsMatching(root, 'AIFLC-CommandBoard', 3)
            ];
            candidates.forEach(p => { if (!possiblePaths.includes(p)) possiblePaths.push(p); });
        }
    }

    for (const uiPath of possiblePaths) {
        const cssFile = path.join(uiPath, 'styles.css');
        const jsFile = path.join(uiPath, 'commandboard.js');
        if (fs.existsSync(cssFile) && fs.existsSync(jsFile)) {
            cssContent = fs.readFileSync(cssFile, 'utf-8');
            jsContent = fs.readFileSync(jsFile, 'utf-8');
            const dataFile = path.join(uiPath, '..', 'data', 'triggers.json');
            if (fs.existsSync(dataFile)) {
                triggerData = fs.readFileSync(dataFile, 'utf-8');
            }
            break;
        }
    }

    if (!cssContent) { cssContent = 'body { font-family: sans-serif; padding: 20px; }'; }
    if (!jsContent) { jsContent = 'document.body.innerHTML="<p>Command board files not found.</p>";'; }

    return `<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AIFLC Command Board</title>
<style>${cssContent}</style>
</head>
<body>
<div class="topbar">
  <span class="topbar-title">AIFLC Command Board</span>
  <input type="text" id="search" class="search-input" placeholder="Search triggers..." autocomplete="off">
  <button class="theme-toggle" onclick="toggleTheme()">\u2600/\uD83C\uDF19</button>
</div>
<div class="filter-bar">
  <div class="filter-row" id="family-filter"></div>
  <div class="filter-row" id="category-filter"></div>
</div>
<div class="command-grid" id="command-grid"></div>
<div class="toast" id="toast">Copied!</div>
<div class="footer">AIFLC CommandBoard v0.3.0 \u00B7 Click any card to expand</div>
<script>var TRIGGERS = ${triggerData};</script>
<script>${jsContent}</script>
</body>
</html>`;
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
