---
name: lightcone-session
description: |
  Manual step-by-step computer control via Lightcone sessions. Activate when user needs fine-grained browser or desktop automation, multi-step workflows, login sequences, or precise click-by-click interaction. Create a cloud computer, send actions, see screenshots.
user-invocable: true
metadata: {"openclaw":{"emoji":"🖥️","homepage":"https://docs.lightcone.ai","requires":{"env":["TZAFON_API_KEY"]},"primaryEnv":"TZAFON_API_KEY"}}
---

# Lightcone Session Control

Three tools for manual step-by-step control of a cloud computer. Use when you need precise multi-step interaction with a website or desktop application.

For simple "go do this" tasks, prefer **lightcone-browse** (the `/lightcone-browse` command) instead.

## Tools

| Tool | Purpose |
|------|---------|
| `lightcone_session_create` | Create a cloud computer (browser or desktop) |
| `lightcone_session_action` | Send actions (click, type, scroll, screenshot, etc.) |
| `lightcone_session_close` | Shut down the computer |

## Workflow Pattern

```
1. lightcone_session_create  → get session ID + initial screenshot
2. lightcone_session_action  → navigate, click, type, screenshot (repeat)
3. lightcone_session_close   → shut down
```

## lightcone_session_create

| Parameter | Required | Description |
|-----------|----------|-------------|
| `url` | No | URL to navigate to immediately |
| `kind` | No | `"browser"` (default) or `"desktop"` |

Returns: session ID (e.g., `lc-a1b2c3d4`) + screenshot of initial state.

## lightcone_session_action

| Parameter | Required | Description |
|-----------|----------|-------------|
| `sessionId` | Yes | Session ID from create |
| `action` | Yes | One of the actions below |
| `url` | For navigate | Target URL |
| `x`, `y` | For click/scroll | Pixel coordinates |
| `text` | For type | Text to enter |
| `keys` | For hotkey | Comma-separated keys, e.g. `"Control,c"` |
| `dx`, `dy` | For scroll | Scroll deltas |
| `seconds` | For wait | Duration in seconds |
| `command` | For debug | Shell command to run |

### Actions

| Action | Returns | Use for |
|--------|---------|---------|
| `screenshot` | Screenshot | See current state |
| `navigate` | Screenshot | Go to a URL |
| `click` | Screenshot | Click at (x, y) |
| `doubleClick` | Screenshot | Double-click at (x, y) |
| `rightClick` | Screenshot | Right-click for context menu |
| `type` | Screenshot | Enter text at cursor |
| `hotkey` | Screenshot | Keyboard shortcut (e.g., Enter, Tab, Control+a) |
| `scroll` | Screenshot | Scroll at position |
| `html` | Page HTML | Extract page source |
| `wait` | Screenshot | Pause before next action |
| `debug` | Command output | Run shell command in the computer |

## Example: Login and extract data

```
Step 1: Create a cloud computer at the login page
  lightcone_session_create { url: "https://app.example.com/login" }

Step 2: Type username (click the email field first)
  lightcone_session_action { sessionId: "lc-...", action: "click", x: 640, y: 300 }
  lightcone_session_action { sessionId: "lc-...", action: "type", text: "user@example.com" }

Step 3: Type password
  lightcone_session_action { sessionId: "lc-...", action: "hotkey", keys: "Tab" }
  lightcone_session_action { sessionId: "lc-...", action: "type", text: "password123" }

Step 4: Submit
  lightcone_session_action { sessionId: "lc-...", action: "hotkey", keys: "Return" }
  lightcone_session_action { sessionId: "lc-...", action: "wait", seconds: 3 }

Step 5: Screenshot to verify login succeeded
  lightcone_session_action { sessionId: "lc-...", action: "screenshot" }

Step 6: Extract page content
  lightcone_session_action { sessionId: "lc-...", action: "html" }

Step 7: Shut down
  lightcone_session_close { sessionId: "lc-..." }
```

## Tips

- Always take a screenshot after navigation to see the current state before clicking
- Use coordinates from the screenshot to target clicks accurately
- Wait 2-3 seconds after navigation or form submission for pages to load
- Use `html` action to extract structured data from the page
- Always close sessions when done to free resources
