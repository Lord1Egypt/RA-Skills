---
name: nlm
description: NotebookLM CLI for listing notebooks, creating notebooks, adding sources, querying notebooks, generating studio artifacts, downloading outputs, sharing notebooks, setting up MCP integrations, and diagnosing auth/install issues. Use when working with the `nlm` command or automating NotebookLM from the terminal.
homepage: https://github.com/jacob-bd/notebooklm-mcp-cli
metadata: {"clawdbot":{"emoji":"📓","requires":{"bins":["nlm"]},"install":[{"id":"uv","kind":"uv-tool","package":"notebooklm-mcp-cli","bins":["nlm","notebooklm-mcp"],"label":"Install notebooklm-mcp-cli (uv)"},{"id":"pipx","kind":"pipx","package":"notebooklm-mcp-cli","bins":["nlm","notebooklm-mcp"],"label":"Install notebooklm-mcp-cli (pipx)"},{"id":"pip","kind":"pip","package":"notebooklm-mcp-cli","bins":["nlm","notebooklm-mcp"],"label":"Install notebooklm-mcp-cli (pip)"}]}}
---

# nlm

Use `nlm` to work with Google NotebookLM from the terminal.

Setup
- Install: `uv tool install notebooklm-mcp-cli`
- Check auth: `nlm login --check`
- Sign in: `nlm login`
- Use a named profile: `nlm login --profile work`
- Switch profile: `nlm login switch <profile>`
- Diagnose issues: `nlm doctor`

Notebooks
- List notebooks: `nlm notebook list`
- Create notebook: `nlm notebook create "Research Project"`
- Query notebook: `nlm notebook query <notebook> "What are the key findings?"`
- Show sharing: `nlm share show <notebook>`
- Enable public link: `nlm share public <notebook>`
- Disable public link: `nlm share private <notebook>`
- Invite collaborator: `nlm share invite <notebook> user@example.com --role editor`

Sources
- Add URL: `nlm source add <notebook> --url "https://example.com"`
- Add pasted text: `nlm source add <notebook> --text "..." --title "Notes"`
- Add local file: `nlm source add <notebook> --file ./notes.pdf`
- Add Google Drive file: `nlm source add <notebook> --drive <file-id>`
- List sources: `nlm source list <notebook>`
- Sync Drive sources: `nlm source sync <notebook>`
- Remove source: `nlm source delete <notebook> <source-id>`

Research + generation
- Start web research: `nlm research start <notebook> "enterprise AI ROI metrics"`
- Create studio artifact: `nlm studio create <notebook> --type audio --confirm`
- Revise slides: `nlm slides revise <notebook> <artifact-id> --prompt "Make it more concise"`
- Check artifact status: `nlm studio list <notebook>`
- Download artifact: `nlm download audio <notebook> <artifact-id>`

MCP + skills
- Configure Claude Code: `nlm setup add claude-code`
- Configure Gemini: `nlm setup add gemini`
- List configured tools: `nlm setup list`
- Remove MCP config: `nlm setup remove claude-code`
- Install OpenClaw skill: `nlm skill install openclaw`
- Update installed skills: `nlm skill update`

Notes
- `nlm` and `notebooklm-mcp` come from the same package: `notebooklm-mcp-cli`.
- Prefer `nlm login` before notebook commands; auth depends on browser cookies.
- Free-tier NotebookLM has rate limits; batch work when possible.
- After changing MCP setup, restart the target app or reconnect the MCP server.
- If `uv tool upgrade` does not move to the latest version, use `uv tool install --force notebooklm-mcp-cli`.
- If the user wants OpenClaw-managed browser auth, use `nlm login --provider openclaw --cdp-url http://127.0.0.1:18800`.
