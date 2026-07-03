# Agent Browser Skill

Fast browser automation using accessibility tree snapshots with refs for deterministic element selection.

## Why Use This Over Built-in Browser Tool

Use agent-browser when:
- Automating multi-step workflows
- Need deterministic element selection
- Performance is critical
- Working with complex SPAs
- Need session isolation

Use built-in browser tool when:
- Need screenshots/PDFs for analysis
- Visual inspection required
- Browser extension integration needed

## Core Workflow

```
# 1. Navigate and snapshot
agent-browser open https://example.com
agent-browser snapshot -i --json

# 2. Parse refs from JSON, then interact
agent-browser click @e2
agent-browser fill @e3 "text"

# 3. Re-snapshot after page changes
agent-browser snapshot -i --json
```

## Key Commands

### Navigation
```
agent-browser open <url>
agent-browser back | forward | reload | close
```

### Snapshot (Always use -i --json)
```
agent-browser snapshot -i --json                    # Interactive elements, JSON output
agent-browser snapshot -i -c -d 5 --json            # + compact, depth limit
agent-browser snapshot -s "#main" -i                # Scope to selector
```

### Interactions (Ref-based)
```
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser type @e3 "text"
agent-browser hover @e4
agent-browser check @e5 | uncheck @e5
agent-browser select @e6 "value"
agent-browser press "Enter"
agent-browser scroll down 500
agent-browser drag @e7 @e8
```

### Get Information
```
agent-browser get text @e1 --json
agent-browser get html @e2 --json
agent-browser get value @e3 --json
agent-browser get attr @e4 "href" --json
agent-browser get title --json
agent-browser get url --json
agent-browser get count ".item" --json
```

### Check State
```
agent-browser is visible @e2 --json
agent-browser is enabled @e3 --json
agent-browser is checked @e4 --json
```

### Wait
```
agent-browser wait @e2                     # Wait for element
agent-browser wait 1000                    # Wait ms
agent-browser wait --text "Welcome"        # Wait for text
agent-browser wait --url "**/dashboard"    # Wait for URL
agent-browser wait --load networkidle      # Wait for network
agent-browser wait --fn "window.ready === true"
```

### Sessions (Isolated Browsers)
```
agent-browser --session admin open site.com
agent-browser --session user open site.com
agent-browser session list
```

### State Persistence
```
agent-browser state save auth.json    # Save cookies/storage
agent-browser state load auth.json    # Load (skip login)
```

### Screenshots & PDFs
```
agent-browser screenshot page.png
agent-browser screenshot --full page.png
agent-browser pdf page.pdf
```

### Network Control
```
agent-browser network route "**/ads/*" --abort          # Block
agent-browser network route "**/api/*" --body '{"x":1}' # Mock
agent-browser network requests --filter api             # View
```

### Cookies & Storage
```
agent-browser cookies                        # Get all
agent-browser cookies set name value
agent-browser storage local key              # Get localStorage
agent-browser storage local set key val
```

### Tabs & Frames
```
agent-browser tab new https://example.com
agent-browser tab 2                          # Switch to tab
agent-browser frame @e5                      # Switch to iframe
agent-browser frame main                     # Back to main
```

## Snapshot Output Format

```json
{
  "success": true,
  "data": {
    "snapshot": "...",
    "refs": {
      "e1": {"role": "heading", "name": "Example Domain"},
      "e2": {"role": "button", "name": "Submit"},
      "e3": {"role": "textbox", "name": "Email"}
    }
  }
}
```

## Best Practices

- Always use `-i` flag — Focus on interactive elements
- Always use `--json` — Easier to parse
- Wait for stability — `agent-browser wait --load networkidle`
- Save auth state — Skip login flows with `state save/load`
- Use sessions — Isolate different browser contexts
- Use `--headed` for debugging — See what's happening

## Configuration

On this machine:
- CLI: `agent-browser` (installed globally via npm, Node 24)
- Chromium: `/root/.cache/ms-playwright/chromium-1223/chrome-linux/chrome`
- Config: `browser.executablePath` set in `~/.openclaw/openclaw.json`

## Credits

Skill created by Yossi Elkrief ([@MaTriXy](https://github.com/MaTriXy))
agent-browser CLI by [Vercel Labs](https://github.com/vercel-labs/agent-browser)
