---
name: Browser Use
description: >
  Autonomous browser automation for AI agents. Two tools: agent-browser (CLI Playwright for step-by-step control)
  and browser-use (Python autonomous agent that decides what to do on pages). Navigate, click, fill forms,
  scrape data, manage sessions, and run complex multi-step browser tasks.
read_when:
  - Automating web interactions beyond simple fetch
  - Filling forms or completing multi-step web flows
  - Scraping structured data from dynamic pages
  - Running an autonomous browsing agent for complex tasks
  - Testing or interacting with authenticated web apps
  - Taking screenshots or recording browser sessions
metadata:
  clawdbot:
    emoji: "🌐"
    requires:
      bins: ["node", "npm", "python3"]
      system: ["chromium", "xvfb"]
allowed-tools: Bash(agent-browser:*,browser-use-agent:*,xvfb-run:*)
---

# Browser Use — Autonomous Browser Automation

Two complementary tools for browser automation:

| Tool | Best for | How it works |
|------|----------|-------------|
| **agent-browser** | Step-by-step control, scraping, form filling | CLI commands, you drive each action |
| **browser-use** | Complex autonomous tasks | Python agent that decides actions itself |

## Quick Start

### agent-browser (recommended for most tasks)

```bash
# Navigate and inspect
agent-browser open "https://example.com"
agent-browser snapshot -i          # Get interactive elements with @refs

# Interact using refs
agent-browser click @e3            # Click element
agent-browser fill @e2 "text"      # Fill input (clears first)
agent-browser press Enter          # Press key

# Extract data
agent-browser get text @e1         # Get element text
agent-browser get attr @e1 href    # Get attribute
agent-browser screenshot /tmp/p.png # Screenshot

# Done
agent-browser close
```

### browser-use (autonomous agent)

```bash
# Run a full autonomous browsing task
browser-use-agent "Find the pricing for Notion and compare plans"
```

The agent will navigate, click, read pages, and return a structured result.

## agent-browser — Full Reference

### Navigation
```bash
agent-browser open <url>           # Navigate to URL
agent-browser back                 # Go back
agent-browser forward              # Go forward
agent-browser reload               # Reload page
agent-browser close                # Close browser
```

### Snapshot (page analysis)
```bash
agent-browser snapshot             # Full accessibility tree
agent-browser snapshot -i          # Interactive elements only (recommended)
agent-browser snapshot -c          # Compact output
agent-browser snapshot -d 3        # Limit depth to 3
agent-browser snapshot -s "#main"  # Scope to CSS selector
agent-browser snapshot -i --json   # JSON output for parsing
```

### Interactions (use @refs from snapshot)
```bash
agent-browser click @e1            # Click
agent-browser dblclick @e1         # Double-click
agent-browser fill @e2 "text"      # Clear and type (use this for inputs)
agent-browser type @e2 "text"      # Type without clearing
agent-browser press Enter          # Press key
agent-browser press Control+a      # Key combination
agent-browser hover @e1            # Hover
agent-browser check @e1            # Check checkbox
agent-browser uncheck @e1          # Uncheck checkbox
agent-browser select @e1 "value"   # Select dropdown option
agent-browser scroll down 500      # Scroll page
agent-browser scrollintoview @e1   # Scroll element into view
agent-browser drag @e1 @e2         # Drag and drop
agent-browser upload @e1 file.pdf  # Upload files
```

### Extract Data
```bash
agent-browser get text @e1         # Get element text
agent-browser get html @e1         # Get innerHTML
agent-browser get value @e1        # Get input value
agent-browser get attr @e1 href    # Get attribute
agent-browser get title            # Page title
agent-browser get url              # Current URL
agent-browser get count ".item"    # Count matching elements
```

### Wait
```bash
agent-browser wait @e1             # Wait for element
agent-browser wait 2000            # Wait milliseconds
agent-browser wait --text "Done"   # Wait for text to appear
agent-browser wait --url "/dash"   # Wait for URL pattern
agent-browser wait --load networkidle  # Wait for network idle
```

### Screenshots, PDF & Recording
```bash
agent-browser screenshot path.png      # Save screenshot
agent-browser screenshot --full        # Full page screenshot
agent-browser pdf output.pdf           # Save as PDF
agent-browser record start ./demo.webm # Start recording
agent-browser record stop              # Stop and save
```

### Sessions (parallel browsers)
```bash
agent-browser --session s1 open "https://site1.com"
agent-browser --session s2 open "https://site2.com"
agent-browser session list
```

### State (persist auth/cookies)
```bash
agent-browser state save auth.json     # Save session (cookies, storage)
agent-browser state load auth.json     # Restore session
```

### Cookies & Storage
```bash
agent-browser cookies                  # Get all cookies
agent-browser cookies set name value   # Set cookie
agent-browser cookies clear            # Clear cookies
agent-browser storage local            # Get all localStorage
agent-browser storage local set k v    # Set value
```

### Tabs & Frames
```bash
agent-browser tab                      # List tabs
agent-browser tab new [url]            # New tab
agent-browser tab 2                    # Switch to tab
agent-browser frame "#iframe"          # Switch to iframe
agent-browser frame main               # Back to main frame
```

### Browser Settings
```bash
agent-browser set viewport 1920 1080
agent-browser set device "iPhone 14"
agent-browser set geo 37.7749 -122.4194
agent-browser set offline on
agent-browser set media dark
```

### JavaScript
```bash
agent-browser eval "document.title"    # Run JS in page context
```

## browser-use — Autonomous Agent

For complex tasks where you want the agent to figure out the browsing steps:

```bash
browser-use-agent "Your task description here"
```

### Custom Script (advanced)

```python
# Run via: /opt/browser-use/bin/python3 script.py
import asyncio, os
from browser_use import Agent, Browser
from langchain_anthropic import ChatAnthropic

async def run():
    browser = Browser()
    llm = ChatAnthropic(
        model='claude-sonnet-4-20250514',
        api_key=os.environ['ANTHROPIC_API_KEY']
    )
    agent = Agent(
        task="Compare pricing on 3 competitor sites",
        llm=llm,
        browser=browser,
    )
    result = await agent.run(max_steps=15)
    await browser.close()
    return result

asyncio.run(run())
```

You can swap the LLM for any langchain-compatible model (OpenAI, Anthropic, etc).

## Standard Workflow

```bash
# 1. Open page
agent-browser open "https://example.com"

# 2. Snapshot to see what's on the page
agent-browser snapshot -i

# 3. Interact with elements using @refs from snapshot
agent-browser fill @e1 "search query"
agent-browser click @e2

# 4. Wait for new page to load
agent-browser wait --load networkidle

# 5. Re-snapshot (refs change after navigation!)
agent-browser snapshot -i

# 6. Extract what you need
agent-browser get text @e5

# 7. Close when done
agent-browser close
```

## Important Rules

1. **Always `snapshot -i` after navigation** — refs change on every page load
2. **Use `fill` not `type`** for inputs — fill clears existing text first
3. **Wait after clicks that trigger navigation** — `wait --load networkidle`
4. **Close the browser when done** — `agent-browser close`
5. **Google/Bing block headless browsers** (CAPTCHA) — use DuckDuckGo or `web_search` instead
6. **Save auth state** for sites requiring login — `state save/load`
7. **Use `--json`** when you need machine-parseable output
8. **Use sessions** for parallel browsing — `--session <name>`

## Troubleshooting

- **Element not found**: Re-run `snapshot -i` to get current refs
- **Page not loaded**: Add `wait --load networkidle` after navigation
- **CAPTCHA on search engines**: Use DuckDuckGo or the `web_search` tool instead
- **Auth expired**: Re-login and `state save` again
- **Display errors**: The install script sets up Xvfb for headless rendering
