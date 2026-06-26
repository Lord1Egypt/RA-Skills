---
name: mac-compute-use
description: "Control macOS applications via Accessibility API through an MCP server. Open apps, click buttons, type text, press keys, scroll, and read UI state. Use when: (1) interacting with native macOS apps (Finder, Messages, Mail, etc.), (2) automating GUI workflows — clicking, typing, navigating menus, (3) reading screen content or UI state from any app, (4) controlling browsers for web automation without browser extensions, (5) any task requiring 'computer use' or 'desktop control' on macOS. NOT for: Linux/Windows, headless servers, or tasks achievable via CLI/API without GUI."
homepage: https://github.com/mediar-ai/mcp-server-macos-use
metadata:
  {
    "openclaw":
      {
        "emoji": "🖥️",
        "requires": { "os": "darwin", "bins": ["mcporter"] },
        "install":
          [
            {
              "id": "brew-mcp",
              "kind": "shell",
              "command": "brew tap reedburns/mcp-server-macos-use && brew install mcp-server-macos-use",
              "bins": ["mcp-server-macos-use"],
              "label": "Install mcp-server-macos-use via Homebrew",
            },
            {
              "id": "mcporter-config",
              "kind": "shell",
              "command": "mcporter config add macos-use --transport stdio --command $(which mcp-server-macos-use)",
              "label": "Register MCP server with mcporter",
            },
          ],
      },
  }
---

# Mac Compute Use

Control macOS GUI through the Accessibility API via MCP.

## Setup

1. Install the MCP server:
```bash
brew tap reedburns/mcp-server-macos-use
brew install mcp-server-macos-use
```

2. Register with mcporter:
```bash
mcporter config add macos-use --transport stdio --command $(which mcp-server-macos-use)
```

3. Grant Accessibility permission:
   **System Settings → Privacy & Security → Accessibility** → add `mcp-server-macos-use`

4. Verify:
```bash
mcporter list macos-use --schema
```

## Tools

All tools are called via `mcporter call macos-use.<tool> key=value`.

### open_application_and_traverse
Open/activate an app and get its UI tree.
```bash
mcporter call macos-use.macos-use_open_application_and_traverse identifier="Google Chrome"
mcporter call macos-use.macos-use_open_application_and_traverse identifier="com.apple.finder"
mcporter call macos-use.macos-use_open_application_and_traverse identifier="TextEdit"
```
Returns: PID, element count, visible interactive elements, and a JSON file path with full UI tree.

### click_and_traverse
Click at coordinates (from UI tree) and get updated state.
```bash
mcporter call macos-use.macos-use_click_and_traverse pid=408 x=701 y=73 width=102 height=41
```
- `x`, `y`: top-left corner of the element (from traversal)
- `width`, `height`: optional, when provided click lands at center

### type_and_traverse
Type text into the focused app.
```bash
mcporter call macos-use.macos-use_type_and_traverse pid=408 text="Hello world"
```

### press_key_and_traverse
Press a key with optional modifiers.
```bash
mcporter call macos-use.macos-use_press_key_and_traverse pid=408 keyName=Return
mcporter call macos-use.macos-use_press_key_and_traverse pid=408 keyName=a modifierFlags='["Command"]'
mcporter call macos-use.macos-use_press_key_and_traverse pid=408 keyName=Tab
mcporter call macos-use.macos-use_press_key_and_traverse pid=408 keyName=Escape
```
Valid modifiers: CapsLock, Shift, Control, Option, Command, Function, NumericPad, Help.

### scroll_and_traverse
Scroll within an app window.
```bash
mcporter call macos-use.macos-use_scroll_and_traverse pid=408 x=500 y=400 deltaY=3
mcporter call macos-use.macos-use_scroll_and_traverse pid=408 x=500 y=400 deltaY=-3
```
- `deltaY` positive = scroll down, negative = scroll up
- `deltaX` optional, for horizontal scroll

### refresh_traversal
Get current UI state without performing any action.
```bash
mcporter call macos-use.macos-use_refresh_traversal pid=408
```

## Workflow Pattern

Typical automation flow:

1. **Open app** → get PID and visible elements
2. **Read the visible_elements** in the response summary — these are interactive elements with coordinates
3. **Click/type/press** using coordinates from the UI tree
4. **Read the response** — it shows what changed (diff) and new visible elements
5. **Repeat** until task is complete

## Reading the Response

Each tool returns a compact summary with:
- `status`: success/error
- `pid`: process ID (use for subsequent calls)
- `file`: path to full JSON with all elements (use `grep` or `python3` to search)
- `visible_elements`: key interactive elements currently visible, with coordinates

When you need to find a specific element, grep the JSON file:
```bash
grep -i "search text" /tmp/macos-use/<file>.json
```

Or parse with Python:
```bash
python3 -c "
import json
with open('/tmp/macos-use/<file>.json') as f:
    data = json.load(f)
for e in data.get('traversal',{}).get('elements',[]):
    text = (e.get('text') or '').strip()
    if text and 'search' in text.lower():
        print(f'[{e[\"role\"]}] ({e[\"x\"]},{e[\"y\"]} {e.get(\"width\",\"?\")}x{e.get(\"height\",\"?\")}) {text}')
"
```

## Tips

- Always use `--output json` for machine-readable results when chaining commands
- After clicking, wait a moment then `refresh_traversal` if the UI didn't update in the diff
- Use app name ("Google Chrome"), bundle ID ("com.google.Chrome"), or path to open apps
- Coordinates are absolute screen positions — if the window moves, refresh the traversal
- The server writes traversal JSON to `/tmp/macos-use/` — these files are temporary
