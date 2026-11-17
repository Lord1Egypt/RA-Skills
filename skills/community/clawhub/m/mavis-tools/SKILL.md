---
name: mcp-control
description: Local browser and Windows desktop control for Mavis. Uses the official Microsoft playwright-cli (a11y-tree based, no screenshot flash) for browser automation, and a PowerShell + .NET helper for Windows desktop (mouse, keyboard, screenshots, windows, clipboard, run). Includes a unified `mcp.cjs` dispatcher with shortcuts for the common operations.
---

# mcp-control — browser + Windows control for Mavis

Two layers, in `C:\Users\fvegi\.mavis\workspace\mcp-control\`:

1. **Browser** — official `playwright-cli` (Microsoft, ships inside `@playwright/mcp`),
   driven over CDP against your running Edge. Uses the **accessibility tree**, not
   screenshots. No flash, no vision model needed.
2. **Windows desktop** — `windows.cjs` (PowerShell + .NET) for mouse, keyboard,
   screenshots, window management, clipboard, shell.

## Quick start

```powershell
# 1. Edge in debug mode (port 9223, profile MavisDebug)
cd "C:\Users\fvegi\.mavis\workspace\mcp-control"
.\start-edge-debug.bat

# 2. One-time attach
node mcp.cjs attach

# 3. Drive the browser
node mcp.cjs tabs                            # list tabs
node mcp.cjs snap                            # full a11y snapshot with refs (e15, e22, ...)
node mcp.cjs find "Kahnawake"                # search snapshot for an element
node mcp.cjs click e15                       # click by ref
node mcp.cjs fill e5 "hello@exemple.com"     # fill an input
node mcp.cjs type "search query"             # type into focused element
node mcp.cjs press Enter                     # press a key
node mcp.cjs eval "document.title"           # run JS, get string back
node mcp.cjs goto https://minimax.io         # navigate
node mcp.cjs shot out.png                    # screenshot (rare — snapshot is preferred)

# Windows desktop
node mcp.cjs screen out.png                  # desktop screenshot
node mcp.cjs lswin                           # list visible windows
node mcp.cjs focus "Claude"                  # activate a window
```

## Why playwright-cli (a11y) and not CSS selectors

- **No screenshot flash.** Every interaction is text-based; nothing captures the screen.
- **Deterministic.** Refs (`e15`) are stable for the duration of a snapshot.
- **Token-efficient.** A snapshot is ~1-5 KB of YAML vs 1-2 MB for a screenshot.
- **No vision model needed.** Pure structured data.
- **Recommended by Microsoft for coding agents** (Mavis qualifies) — the README
  explicitly prefers CLI+SKILLs over MCP for this use case.

## Files

| File | What |
|---|---|
| `mcp.cjs` | unified dispatcher with shortcuts (browser + windows) |
| `pwcli.cjs` | thin wrapper around the official `playwright-cli` (a11y tree) |
| `windows.cjs` | Windows desktop helper (PowerShell + .NET) |
| `mcp-servers.json` | MCP server config for any MCP host (alternative to CLI) |
| `start-edge-debug.bat` | launch Edge with `--remote-debugging-port=9223` |
| `start-playwright-mcp.bat` | launch the official `@playwright/mcp` server (alternative to CLI) |
| `package.json` | pinned to `playwright` ^1.x and `@playwright/mcp` ^0.0.78 |
| `node_modules/` | installed dependencies |

## How CDP setup works

1. `start-edge-debug.bat` launches Edge with `--remote-debugging-port=9223` and
   `--user-data-dir=%LOCALAPPDATA%\Microsoft\Edge\MavisDebug` (separate profile,
   doesn't touch your normal Edge session).
2. `mcp.cjs attach` (or `node pwcli.cjs attach`) connects the CLI to that Edge
   via CDP. Run once per session.
3. The `default` session is then persisted in `.playwright-cli/` so subsequent
   commands automatically reattach to the same Edge.
4. Port 9222 is intentionally left for Lenovo Vantage's existing debug endpoint.

## pwcli.cjs — playwright-cli subcommands

`pwcli.cjs` is a thin wrapper. Anything not in the shortcuts list is forwarded
verbatim to the official CLI. Full list:

```
open [url]                  open the browser
attach [name]               attach to a running playwright browser (--cdp, --endpoint, --extension)
close                       close the browser
detach                      detach from an attached browser
goto <url>                  navigate to a url
type <text>                 type text into editable element
click <target> [button]     perform click on a web page (target = ref or selector)
dblclick <target>           perform double click
fill <target> <text>        fill text into editable element
drag <startTarget> <endTarget> drag and drop between two elements
drop <target>               drop files or data onto an element
hover <target>              hover over element
select <target> <val>       select an option in a dropdown
upload <file>               upload one or multiple files
check / uncheck <target>    check / uncheck a checkbox or radio
snapshot [target]           capture page snapshot to obtain element ref
find [text]                 search the page snapshot for text or regexp
eval <func> [target]        evaluate javascript expression on page or element
dialog-accept / dialog-dismiss
resize <w> <h>              resize the browser window
delete-data                 delete session data
press <key>                 press a key (e.g. Enter, ArrowDown, F5)
keydown / keyup <key>       press/release a key
mousemove / mousedown / mouseup / mousewheel
screenshot [target]         take a screenshot (rare)
pdf --filename=...          save page as PDF
go-back / go-forward / reload
```

## windows.cjs — subcommands

```
screenshot <outPath>             Capture full screen to PNG
click <x> <y>                    Left-click at coords
dblclick <x> <y>                 Double-click
rightclick <x> <y>               Right-click
move <x> <y>                     Move mouse
scroll <amount>                  Scroll wheel (+ up, - down)
type <text>                      Type unicode text (clipboard paste)
key <name>                       Press a key
chord <keys>                     Key chord (e.g. "ctrl+c", "alt+F4")
windows                          List visible top-level windows
find <titleSubstr>               Find window by title
activate <titleSubstr>           Bring window to front
clipboard get | set <text>       Clipboard
run <command>                    Run shell command
ps <script>                      Run PowerShell
size                             Get primary screen size
```

## Config for Mavis (or any MCP host)

`mcp-servers.json` in this directory is ready to use. The official
`@playwright/mcp` server (v0.0.78) is registered there for hosts that prefer
MCP transport. For Mavis specifically, the CLI approach (`pwcli.cjs`) is
recommended by Microsoft for coding agents.

For Claude Desktop, copy the `mcpServers` block from `mcp-servers.json` into
`%APPDATA%\Claude\claude_desktop_config.json`.

## Safety notes

- `windows run` and `windows ps` execute arbitrary commands. Treat them like a shell.
- Screenshots and click events affect the user's actual desktop.
- `windows activate` will switch the foreground window out from under the user.
- `playwright-cli` over CDP sees and acts on whatever's open in the connected
  Edge session, including your logged-in state on any site — be careful what
  you click while you're logged in to sensitive accounts.
