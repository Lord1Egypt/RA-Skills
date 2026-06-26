---
name: gogcli-mcp
description: This skill should be used when the user asks about Google Workspace automation via gogcli — Docs, Sheets, Slides, Drive, or Classroom. Triggers on phrases like "edit this Google doc", "update the sheet", "find my slides", "grade this assignment", or any request involving Google Workspace documents, files, or classes. This is an umbrella skill — the 5 sibling packages (gogcli-mcp-docs, gogcli-mcp-sheets, gogcli-mcp-slides, gogcli-mcp-drive, gogcli-mcp-classroom) cover specific APIs.
---

# gogcli-mcp

Monorepo of 6 MCP servers wrapping the [`gogcli`](https://github.com/chrischall/gogcli) tool for Google Workspace automation:

- **`gogcli-mcp`** — Sheets-focused umbrella (also exposes some Docs + Drive helpers)
- **`gogcli-mcp-docs`** — Google Docs: create, read, edit, find-replace, comments
- **`gogcli-mcp-sheets`** — Google Sheets: cells, ranges, formulas, charts, named ranges
- **`gogcli-mcp-slides`** — Google Slides: deck + slide authoring
- **`gogcli-mcp-drive`** — Google Drive: search, upload, download, permissions
- **`gogcli-mcp-classroom`** — Google Classroom: courses, assignments, submissions, roster

All 6 share the same auth — they read from the gogcli account on your machine (`gogcli auth add`, `gogcli auth run`).

## Install (per sub-package)

Each sub-package is published as a separate npm module. Install the ones you want:

```json
{
  "mcpServers": {
    "gogcli-docs": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-docs"],
      "env": { "GOG_ACCOUNT": "you@example.com" }
    },
    "gogcli-sheets": {
      "command": "npx",
      "args": ["-y", "gogcli-mcp-sheets"]
    }
  }
}
```

Or all-in-one via the umbrella:

```json
{ "mcpServers": { "gogcli": { "command": "npx", "args": ["-y", "gogcli-mcp"] } } }
```

## Auth

Requires [`gogcli`](https://github.com/chrischall/gogcli) installed and authenticated:

```bash
gogcli auth add  # opens browser OAuth flow for your Google account
gogcli auth list
```

Set `GOG_ACCOUNT=you@example.com` in the MCP env if you have multiple accounts. Set `GOG_PATH` only if `gogcli` isn't on your PATH.

## Tools

Each sub-package exposes its own tools with a distinctive prefix (`gog_docs_*`, `gog_sheets_*`, etc.). See each package's own `SKILL.md` for the full list.

## Notes

- All 6 share the gogcli binary — you only authenticate once.
- This is the top-level skill; the sibling skills under `packages/*/SKILL.md` contain per-API detail.
