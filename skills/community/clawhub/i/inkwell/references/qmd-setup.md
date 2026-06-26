# QMD Setup Guide

QMD is a local-first search sidecar that provides BM25 + vector + reranking search across your memory files, knowledge base, and session transcripts.

## Table of Contents

- [Installation](#installation)
- [Windows-Specific Setup](#windows-specific-setup)
- [OpenClaw Configuration](#openclaw-configuration)
- [Verification](#verification)
- [Fallback Behavior](#fallback-behavior)
- [Troubleshooting](#troubleshooting)

## Installation

### Linux / macOS

```bash
bun install -g @tobilu/qmd
```

Verify: `qmd --version`

If running OpenClaw as a service, ensure QMD is on the service's PATH:
```bash
sudo ln -s ~/.bun/bin/qmd /usr/local/bin/qmd
```

### Windows

QMD runs best via WSL2 on Windows. Native Windows support has known issues with the `.cmd` wrapper that npm generates.

**Option A: WSL2 (recommended)**
```powershell
# Install WSL2 if not already installed
wsl --install

# Inside WSL2:
curl -fsSL https://bun.sh/install | bash
bun install -g @tobilu/qmd
```

**Option B: Native Node runner (workaround)**

When installed via npm on Windows, QMD gets a `.cmd` wrapper that doesn't handle arguments correctly. Create a runner script:

```javascript
// qmd-runner.js — place in your OpenClaw root or workspace
const { execFileSync } = require('child_process');
const path = require('path');
const qmdPath = path.join(
  process.env.APPDATA || '', 'npm', 'node_modules',
  '@tobilu', 'qmd', 'dist', 'cli', 'qmd.js'
);
const args = process.argv.slice(2);
try {
  execFileSync(process.execPath, [qmdPath, ...args], {
    stdio: 'inherit', env: process.env
  });
} catch (e) {
  process.exit(e.status || 1);
}
```

Then set `memory.qmd.command` to `node /path/to/qmd-runner.js` in your config.

## OpenClaw Configuration

Add to `openclaw.json`:

```json5
{
  memory: {
    backend: "qmd",
    citations: "auto",
    qmd: {
      // Use default "qmd" on Linux/Mac.
      // On Windows with the runner workaround:
      // command: "node C:/Users/<you>/.openclaw/qmd-runner.js",

      includeDefaultMemory: true,

      // Index the PARA knowledge base
      paths: [
        {
          name: "life",
          path: "life",     // relative to workspace
          pattern: "**/*.md"
        }
      ],

      // Index session transcripts for recall
      sessions: {
        enabled: true
      },

      // Search settings
      searchMode: "search",   // "search", "vsearch", or "query"
      limits: {
        maxResults: 6,
        timeoutMs: 4000        // increase to 120000 on slower hardware
      },

      // Scope: DM-only by default (security)
      scope: {
        default: "deny",
        rules: [
          { action: "allow", match: { chatType: "direct" } }
        ]
      },

      // Refresh schedule
      update: {
        interval: "5m",
        debounceMs: 15000,
        onBoot: true
      }
    }
  }
}
```

**Restart the gateway** after config changes:
```bash
openclaw gateway restart
```

## Verification

Test that QMD is working:

```bash
# Check QMD is accessible
qmd --version

# Run a test search (after gateway restart)
# In a chat session, use memory_search to search for something you know exists
```

Check gateway logs for QMD-related messages:
- `QMD sidecar started` — QMD is running
- `QMD update complete` — indexing finished
- `QMD search failed, falling back to builtin` — QMD issue, check config

## Fallback Behavior

If QMD is unavailable (not installed, crashed, timed out), OpenClaw automatically falls back to the builtin SQLite search engine. This happens seamlessly — `memory_search` still works, just without QMD's advanced features.

The builtin engine provides:
- BM25 text search
- Basic embedding search (if a provider is configured)
- Searches MEMORY.md and memory/*.md

What you lose without QMD:
- Reranking and query expansion
- Searching /life/ files (unless added to `memorySearch.extraPaths`)
- Session transcript search
- Advanced hybrid scoring

## Troubleshooting

**"QMD not found"** — Ensure the QMD binary is on the gateway's PATH. If OpenClaw runs as a service, PATH may differ from your shell.

**First search is very slow** — QMD auto-downloads GGUF models (~2 GB) on first use. Pre-warm with: `qmd query "test"` using the same home directory OpenClaw uses.

**Search times out** — Increase `memory.qmd.limits.timeoutMs`. Default is 4000ms, set to 120000 for slower hardware.

**Empty results in group chats** — Check `memory.qmd.scope`. Default only allows DM sessions.

**Windows .cmd wrapper issues** — Use the Node runner workaround described above, or install QMD in WSL2.
