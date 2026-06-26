---
name: neo
description: >
  Browse websites, read web pages, interact with web apps, call website APIs, and automate web tasks.
  Use Neo when: user asks to check a website, read a web page, post on social media (Twitter/X),
  interact with any web app, look up information on a specific site, scrape data from websites,
  automate browser tasks, or when you need to call any website's API.
  Keywords: website, web page, browse, URL, http, API, twitter, tweet, post, scrape, web app,
  open site, check site, read page, social media, online service.
metadata:
  openclaw:
    requires:
      bins: [neo]
    install:
      - id: neo
        kind: node
        package: "@4ier/neo"
        bins: [neo]
        label: "Install Neo CLI (npm)"
---

# Neo 2.0 — Web App API Discovery & Browser Automation

Neo turns any website into an AI-callable API. Zero extensions required — pure CDP.

## ⚠️ MANDATORY FIRST STEP

```bash
neo doctor
```

- All ✓ → proceed
- Chrome CDP ✗ → `neo start` (launches Chrome with correct profile + CDP)
- Still ✗ → ask the user, then STOP. Don't loop.

### Critical Rules

1. **NEVER start Chrome manually** — always `neo start`
2. **NEVER copy Chrome profiles** — login sessions live in the real profile
3. **NEVER `pkill chrome`** — user may have important tabs open
4. **If stuck → tell user, STOP.** Don't retry in a loop.

## Workflows

### Read a web page

```bash
neo doctor
neo read example.com          # Extract readable text from any open tab
# If page isn't open:
neo open https://example.com
neo read example.com
```

### Call a website's API (fast path)

```bash
neo doctor
neo schema show x.com                   # Check existing API knowledge
neo api x.com HomeTimeline              # Call it (auto-auth from browser)
neo api x.com CreateTweet --body '{"variables":{"tweet_text":"hello"}}'
```

### Discover APIs for a new website

```bash
neo doctor
neo open https://example.com            # Open in Chrome
# Browse around to generate traffic
neo capture list example.com --limit 20
neo schema generate example.com
neo api example.com <keyword>
```

### UI automation (click/fill/type — when no API exists)

```bash
neo doctor
neo snapshot                  # Get a11y tree with compact ref IDs
neo click 14                  # Click element by ref number
neo fill 7 "search query"    # Clear + fill input
neo type 7 "text"             # Append text
neo press Enter
neo scroll down 500
neo screenshot
```

Refs are compact integers: `[0] button "Sign in"`, `[1] input "Search"`.
Use `neo click 0`, `neo fill 1 "query"` etc. Legacy `@e5` and `[5]` formats also work.

### Cookie management

```bash
neo cookies list                        # All cookies for active page
neo cookies list github.com             # Filter by domain
neo cookies export github.com cookies.json  # Save to file
neo cookies import cookies.json         # Restore cookies
neo cookies clear github.com            # Delete by domain
neo cookies clear                       # Delete all
```

Use `export` + `import` to persist login sessions across browser restarts.

### Profile management

```bash
neo profile list              # Discover all Chrome profiles + emails
neo profile use "Default"     # Set default profile
neo start                     # Launches with selected profile
```

### Clean up — close tabs when done

```bash
neo tabs
neo eval "window.close()" --tab example.com
```

## Command Reference

```bash
# Page Reading & Interaction
neo open <url>                          # Open URL in Chrome
neo read <tab-pattern>                  # Extract readable text
neo eval "<js>" --tab <pattern>         # Run JS in page context
neo tabs [filter]                       # List open Chrome tabs

# UI Automation (compact refs: neo click 5, neo fill 3 "text")
neo snapshot [-i] [-C] [--json] [--diff]  # A11y tree with compact refs
neo click <ref> [--new-tab]             # Click element
neo fill <ref> "text"                   # Clear + fill input
neo type <ref> "text"                   # Append text to input
neo press <key>                         # Keyboard key (Ctrl+a, Enter, etc.)
neo hover <ref>                         # Hover
neo scroll <dir> [px] [--selector css]  # Scroll
neo select <ref> "value"               # Select dropdown
neo screenshot [path] [--full]          # Capture screenshot
neo get text <ref> | url | title        # Extract info
neo wait <ref> | --load | <ms>          # Wait for element/load/time

# Cookie Management
neo cookies list [domain]               # List cookies
neo cookies export [domain] [file]      # Export as JSON
neo cookies import <file>               # Import from JSON
neo cookies clear [domain]              # Clear cookies

# Profile Management
neo profile list                        # Discover Chrome profiles
neo profile use <name>                  # Set default profile

# Capture & Traffic (no extension needed — pure CDP)
neo status                              # Overview
neo capture start                       # Start CDP network capture
neo capture stop                        # Stop capture
neo capture list [domain] [--limit N]   # Recent captures
neo capture search <query>              # Search by URL pattern
neo capture domains                     # Domains with counts
neo capture detail <id>                 # Full capture details

# Schema (API Knowledge)
neo schema generate <domain>            # Generate from captures
neo schema show <domain>                # Human-readable
neo schema list                         # All cached schemas
neo schema search <query>               # Search endpoints

# API Execution
neo api <domain> <keyword> [--body '{}']  # Smart call (schema + auto-auth)
neo exec <url> [--method POST] [--body] [--tab pattern] [--auto-headers]
neo replay <id> [--tab pattern]         # Replay captured call

# Setup & Diagnostics
neo setup                               # First-time setup
neo start [--profile <name>]            # Launch Chrome with correct profile + CDP
neo doctor [--fix]                      # Health check (--fix to auto-repair)
```

## Decision Tree

```
Want to interact with a website?
  │
  ├─ FIRST: neo doctor
  │   ├─ All ✓ → continue
  │   ├─ Chrome ✗ → neo start → retry
  │   └─ Still ✗ → ask user, STOP
  │
  ├─ Just read content? → neo read <domain>
  │
  ├─ Need to call an API?
  │   ├─ neo schema show <domain> → exists? → neo api
  │   └─ No schema? → neo open → browse → neo schema generate → neo api
  │
  ├─ Need to click/fill/type?
  │   └─ neo snapshot → neo click 5 / neo fill 3 "text"
  │
  ├─ Need to manage cookies/sessions?
  │   └─ neo cookies list/export/import/clear
  │
  └─ Done? → neo eval "window.close()" --tab <domain>
```

## Key Principles

1. **`neo doctor` first, always.**
2. **API > UI automation.** If schema has it, use `neo api`. Don't snapshot+click.
3. **Auth is automatic.** API calls inherit browser cookies/session/CSRF.
4. **Close tabs after use.** Every `neo open` creates a new tab.
5. **If stuck, stop.** Don't loop on Chrome startup. Ask the user.
