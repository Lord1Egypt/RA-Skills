<!--
SPDX-License-Identifier: MIT-0
Copyright 2026 InvestorClaw Contributors

This INSTALL.md is MIT-0-licensed. The InvestorClaw service it installs is
Apache 2.0. See ../../LICENSE-MIT-0 for the full MIT text.
-->

# Installing InvestorClaw for Claude Desktop

This is the full install path for Claude Desktop users. End-to-end it
takes about five minutes. You'll run two terminal commands, edit one
JSON file, and restart Claude Desktop.

## Step 1 — Install Docker

InvestorClaw runs as two Docker containers. Install Docker Desktop if
you don't already have it.

- **macOS:** download from <https://www.docker.com/products/docker-desktop/>
  and drag to Applications. Launch it once so it finishes setup.
- **Windows:** download Docker Desktop from the same URL. Enable WSL2
  during install (the installer guides you).
- **Linux:** follow your distro's instructions
  (<https://docs.docker.com/engine/install/>). The `docker compose`
  plugin must be available.

Verify with:

```bash
docker --version
docker compose version
```

Both must return a version string. If `docker compose version` fails,
your Compose plugin isn't installed — fix that before continuing.

## Step 2 — Stage the compose file

```bash
mkdir -p ~/.investorclaw
curl -sSL https://raw.githubusercontent.com/ncz-os/mnemos-ic-runtime/main/compose.yml > ~/.investorclaw/compose.yml
```

On Windows, run this in PowerShell or Git Bash. The `~` expands to
your home directory (`C:\Users\<you>` on Windows).

## Step 3 — Start the service

```bash
cd ~/.investorclaw
docker compose up -d
```

The first run pulls two images (~300-450 MB combined). Subsequent
starts are near-instant. Confirm both containers are healthy:

```bash
docker compose ps
curl -fsS http://localhost:18090/healthz && echo " ic-engine OK"
curl -fsS http://localhost:5002/healthz && echo " mnemos OK"
```

Both health checks should return `200 OK`.

## Step 4 — Edit `claude_desktop_config.json`

This is where Claude Desktop learns about the two MCP servers.

**Locate the config file** for your OS:

| OS | Path |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` (if Claude Desktop is available for your distro) |

**If the file doesn't exist yet,** create it with this content:

```json
{
  "mcpServers": {
    "investorclaw": {
      "transport": "http",
      "url": "http://localhost:18090/mcp"
    },
    "mnemos": {
      "transport": "http",
      "url": "http://localhost:5002/mcp"
    }
  }
}
```

**If the file already exists,** open it in a text editor and merge the
two servers into the existing `mcpServers` object. For example, if
your config currently looks like this:

```json
{
  "mcpServers": {
    "filesystem": { "command": "...", "args": ["..."] }
  }
}
```

Add the two new entries alongside the existing one:

```json
{
  "mcpServers": {
    "filesystem": { "command": "...", "args": ["..."] },
    "investorclaw": {
      "transport": "http",
      "url": "http://localhost:18090/mcp"
    },
    "mnemos": {
      "transport": "http",
      "url": "http://localhost:5002/mcp"
    }
  }
}
```

A reference snippet ships in `config-snippet.json` next to this file.

**Validate the JSON before saving.** Trailing commas and missing
closing braces are the top reason MCP servers don't appear. Paste your
edited file into <https://jsonlint.com> if unsure.

## Step 5 — Fully quit and relaunch Claude Desktop

This step is critical. Closing the Claude Desktop window does **not**
reload the MCP config — the app keeps running in the background and
caches the old config.

- **macOS:** right-click the Claude Desktop icon in the Dock and choose
  *Quit*, or press `Cmd+Q` while the app is focused. Confirm it's gone
  from `Activity Monitor` or `pgrep -f Claude`. Then relaunch.
- **Windows:** right-click the Claude Desktop icon in the system tray
  and choose *Quit* / *Exit*. Confirm via Task Manager that no
  `Claude.exe` process remains. Then relaunch.
- **Linux:** quit from the application menu, then `pkill -f Claude`
  for good measure. Then relaunch.

When Claude Desktop comes back up, it will read `claude_desktop_config.json`
fresh and connect to both MCP servers.

## Step 6 — Configure your portfolio in the dashboard

Open the dashboard in your browser:

<http://localhost:18092>

The first-run wizard walks you through:

1. Drag-drop your broker CSV / XLS / XLSX / PDF
2. (Optional) Add provider keys for richer market data and narrative
   tier — Together, FRED, Finnhub, NewsAPI all optional and degrade
   gracefully
3. Confirm the connected agent ("Claude Desktop" should show as
   connected if Steps 4 and 5 succeeded)

## Step 7 — Try it in Claude Desktop

Open a new chat and ask:

> "What's in my portfolio?"

Claude should call `investorclaw.portfolio_holdings` and return your
positions. Other prompts to try:

- "How did my portfolio perform this year?"
- "What would happen if rates rose 100 basis points?"
- "Remember that I'm planning to retire in 2030." (writes to mnemos)

## Troubleshooting

**Tools don't appear in Claude Desktop.** The most common cause is
that the app wasn't fully quit before relaunch. Close it from the Dock
/ system tray (not just the window) and relaunch. Second most common
cause is invalid JSON in `claude_desktop_config.json` — validate at
<https://jsonlint.com>.

**`Connection refused` when Claude tries to call a tool.** The
containers aren't running. `cd ~/.investorclaw && docker compose ps`
to check, then `docker compose up -d` to restart.

**Docker not running.** On macOS / Windows, launch Docker Desktop
(menu-bar / system-tray app must show "Docker Desktop is running").
On Linux, `sudo systemctl start docker`.

**Port 8090 / 5002 / 8092 already in use.** Edit
`~/.investorclaw/compose.yml` and remap the host-side port (left of
the colon in the `ports:` blocks). Update the URLs in
`claude_desktop_config.json` to match, then fully quit and relaunch
Claude Desktop again.

**Dashboard loads but agent shows "not connected".** The dashboard
sees connections in the last ~30s. Send a message in Claude Desktop
that requires a tool call (e.g., "What's in my portfolio?") and
refresh the dashboard's MCP Server section.

**Want to wipe and start over.**

```bash
cd ~/.investorclaw
docker compose down -v   # -v also removes the data volume — your portfolio + memory go away
```

Then restart from Step 3.

## Uninstall

```bash
cd ~/.investorclaw
docker compose down -v
rm -rf ~/.investorclaw
```

Then remove the `investorclaw` and `mnemos` entries from
`claude_desktop_config.json` and fully quit + relaunch Claude Desktop.
