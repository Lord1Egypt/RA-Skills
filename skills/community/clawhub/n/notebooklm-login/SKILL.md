---
name: notebooklm-login
description: Login to Google NotebookLM via Chrome DevTools Protocol and save auth cookies for notebooklm-mcp. Use when user asks to login, authenticate, or re-authenticate NotebookLM MCP, or when `nlm login --check` shows expired/missing credentials.
metadata: { "openclaw": { "requires": { "bins": ["chromium-browser", "uv"] } } }
---

# NotebookLM MCP Login

Authenticate with Google and save cookies for the `notebooklm-mcp` CLI/MCP server.

## Why this skill exists

The built-in `nlm login` command sometimes fails to launch Chromium via `subprocess.Popen` in
non-standard environments. This skill provides a tested workaround that:

1. Manually launches Chromium with `--remote-debugging-port=9222`
2. Waits for the user to complete Google login in the browser
3. Extracts cookies via CDP (`extract_cookies_via_existing_cdp`)
4. Saves them to `~/.notebooklm-mcp-cli/profiles/default/` via `AuthManager.save_profile()`

## Steps

### 1. Verify prerequisites

```bash
which chromium-browser && which uv
```

If missing, install Chromium (`apt install chromium-browser`) and uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`).

### 2. Run the login script

```bash
DISPLAY=:0 ~/.local/share/uv/tools/notebooklm-mcp-cli/bin/python3 {baseDir}/scripts/login.py
```

- A Chromium window opens on the host display.
- The user logs in to their Google account.
- The script waits up to 300s, then extracts and saves cookies automatically.

### 3. Verify

```bash
uv tool run --from notebooklm-mcp-cli nlm login --check
```

Expected output: `✓ Authentication valid!` with email and notebook count.

## Storage

- Cookies: `~/.notebooklm-mcp-cli/profiles/default/cookies.json`
- Metadata: `~/.notebooklm-mcp-cli/profiles/default/metadata.json`

## Troubleshooting

| Problem | Fix |
|---|---|
| `Cannot connect to browser on port 9222` | Kill stale Chrome: `pkill -f remote-debugging-port=9222` |
| `Profile not found: default` | Re-run the login script |
| `DISPLAY` not set | Export `DISPLAY=:0` before running |
