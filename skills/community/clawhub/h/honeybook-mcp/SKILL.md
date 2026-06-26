---
name: honeybook-mcp
description: This skill should be used when the user asks about HoneyBook client-portal data. Triggers on phrases like "check HoneyBook", "sign contract", "pay invoice", "HoneyBook vendors", "unsigned contracts", "open invoices", or any request involving wedding-vendor contracts, invoices, brochures, proposals, or payments via HoneyBook.
---

# honeybook-mcp

MCP server for HoneyBook's client portal — 8 tools for viewing contracts and invoices across multiple wedding vendors, with magic-link session capture and deep-link fallback for signing and paying.

- **Source:** [github.com/chrischall/honeybook-mcp](https://github.com/chrischall/honeybook-mcp)

## Setup

### Option A — Claude Code

Add to `.mcp.json`:

```json
{
  "mcpServers": {
    "honeybook": {
      "command": "node",
      "args": ["/absolute/path/to/honeybook-mcp/dist/bundle.js"]
    }
  }
}
```

No env vars required. Activate a session by calling `use_magic_link` in Claude.

### Option B — from source

```bash
git clone https://github.com/chrischall/honeybook-mcp
cd honeybook-mcp && npm install && npm run build
```

## Tools

| Tool                   | What it does                                          |
|------------------------|-------------------------------------------------------|
| `use_magic_link`       | Capture a session from a vendor magic-link URL        |
| `list_active_sessions` | Show currently active portal sessions                 |
| `list_workspace_files` | All files one vendor has shared (filter by type)      |
| `get_workspace_file`   | Full detail for one file                              |
| `get_workspace`        | Workspace detail + status flags                       |
| `list_payment_methods` | Saved payment methods                                 |
| `sign_contract`        | Deep link to sign in portal (requires `confirm:true`) |
| `pay_invoice`          | Deep link to pay in portal (requires `confirm:true`)  |

## Workflows

- **First time with a vendor** → user pastes magic-link URL → `use_magic_link` → session captured
- **"What contracts haven't I signed?"** → `list_workspace_files` with `file_type=agreement`, filter by `is_file_accepted=false`
- **"Summarize my HB status with Silk Veil"** → `get_workspace` (status flags) + `list_workspace_files`
- **"Send me a link to sign the photographer's contract"** → `list_workspace_files` → `sign_contract` with `confirm:true`
- **"Which invoices are overdue?"** → `list_workspace_files` with `file_type=invoice`, sort by due date

## Notes

- All tools hit `api.honeybook.com/api/v2/*` with 8 custom `hb-api-*` headers
- Sessions are captured via Puppeteer from magic-link URLs and cached in `~/.honeybook-mcp/sessions.json` (mode 0600)
- Each vendor = separate session keyed by portal origin
- `sign_contract` / `pay_invoice` return deep links — actual signing/paying requires browser-side device/SCA handling
- Session expires → re-run `use_magic_link` with a fresh URL from the vendor's email
