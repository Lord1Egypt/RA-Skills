---
name: ko-browser
description: Browser automation CLI for AI agents, written in Go. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction.
allowed-tools: Bash(kbr:*)
---

# Browser Automation with ko-browser

The CLI uses Chrome/Chromium via CDP directly. Install via `go install github.com/libi/ko-browser/cmd/kbr@latest` or build from source. Run `kbr install` to verify Chrome is available, or `kbr install --with-deps` to auto-install it. Existing Chrome, Brave, and Chromium installations are detected automatically.

## Installation

```bash
# Install kbr binary directly (no CGO, no external dependencies)
go install github.com/libi/ko-browser/cmd/kbr@latest

# Or build from source
git clone https://github.com/libi/ko-browser.git
cd ko-browser
go build -o kbr ./cmd/kbr/
mv kbr /usr/local/bin/

# Verify browser dependency
kbr install

# Auto-install Chrome if missing
kbr install --with-deps
```

> **OCR is optional.** The default install has zero CGO dependencies.
> To enable `kbr snapshot --ocr`, rebuild with `-tags=ocr` (requires Tesseract):
> ```bash
> # Install Tesseract first: brew install tesseract (macOS) / apt install libtesseract-dev (Linux)
> CGO_ENABLED=1 go install -tags=ocr github.com/libi/ko-browser/cmd/kbr@latest
> ```

**Manual browser installation by OS:**

```bash
# macOS
brew install --cask google-chrome

# Linux (Debian/Ubuntu)
sudo apt-get install -y chromium-browser

# Linux (Alpine)
apk add chromium

# Windows
choco install googlechrome
```

Or download from: https://www.google.com/chrome/

## Core Workflow

Every browser automation follows this pattern:

1. **Navigate**: `kbr open <url>`
2. **Snapshot**: `kbr snapshot -i` (get element IDs like `1`, `2`, `3`)
3. **Interact**: Use numeric IDs to click, fill, select
4. **Re-snapshot**: After navigation or DOM changes, get fresh IDs

```bash
kbr open https://example.com/form
kbr snapshot -i
# Output:
# 1: textbox "Email"
# 2: textbox "Password"
# 3: button "Submit"

kbr fill 1 "user@example.com"
kbr fill 2 "password123"
kbr click 3
kbr wait load
kbr snapshot -i  # Check result
```

## Command Chaining

Commands can be chained with `&&` in a single shell invocation. The browser persists between commands via a background daemon, so chaining is safe and more efficient than separate calls.

```bash
# Chain open + wait + snapshot in one call
kbr open https://example.com && kbr wait load && kbr snapshot -i

# Chain multiple interactions
kbr fill 1 "user@example.com" && kbr fill 2 "password123" && kbr click 3

# Navigate and capture
kbr open https://example.com && kbr wait load && kbr screenshot page.png
```

**When to chain:** Use `&&` when you don't need to read the output of an intermediate command before proceeding (e.g., open + wait + screenshot). Run commands separately when you need to parse the output first (e.g., snapshot to discover IDs, then interact using those IDs).

## Handling Authentication

When automating a site that requires login, choose the approach that fits:

**Option 1: Persistent profile (simplest for recurring tasks)**

```bash
# First run: login manually or via automation
kbr --profile ~/.myapp open https://app.example.com/login
# ... fill credentials, submit ...

# All future runs: already authenticated
kbr --profile ~/.myapp open https://app.example.com/dashboard
```

**Option 2: State file (manual save/load)**

```bash
# After logging in:
kbr state export ./auth.json

# In a future session:
kbr state import ./auth.json
kbr open https://app.example.com/dashboard
```

**Option 3: Auth vault (credentials stored, login by name)**

```bash
kbr auth save mysite --url https://app.example.com/login --username user --password pass
kbr auth login mysite
```

`auth login` navigates to the URL and waits for login form selectors to appear before filling/clicking.

**Option 4: Session name (isolate parallel tasks)**

```bash
kbr --session myapp open https://app.example.com/login
# ... login flow ...
kbr close  # Session cleaned up

# Use named sessions for parallel automation
kbr --session agent1 open https://site-a.com
kbr --session agent2 open https://site-b.com
```

## Essential Commands

```bash
# Navigation
kbr open <url>                        # Navigate to URL
kbr close                             # Close browser session (alias: stop)
kbr restart                           # Restart browser session
kbr back                              # Go back in history
kbr forward                           # Go forward in history
kbr reload                            # Reload current page

# Snapshot
kbr snapshot -i                       # Interactive elements with IDs (recommended)
kbr snapshot -c                       # Compact mode: omit unnamed wrappers
kbr snapshot --selector "#content"    # Scope to CSS selector
kbr snapshot --depth 3                # Limit tree depth
kbr snapshot --ocr                    # Enable OCR for unnamed images
kbr snapshot --cursor                 # Mark [cursor] on focused element

# Interaction (use numeric IDs from snapshot)
kbr click 1                           # Click element
kbr click --new-tab 1                 # Click and open in new tab
kbr dblclick 1                        # Double-click element
kbr fill 2 "text"                     # Clear and type text
kbr type 2 "text"                     # Type without clearing (append)
kbr select 1 "option"                 # Select dropdown option
kbr check 1                           # Check checkbox
kbr uncheck 1                         # Uncheck checkbox
kbr press Enter                       # Press key (Enter, Tab, Control+a, Meta+c)
kbr keyboard type "text"              # Type at current focus (no element ID)
kbr keyboard inserttext "text"        # Insert without key events
kbr scroll down 500                   # Scroll page (up/down/left/right)
kbr scrollintoview 5                  # Scroll element into viewport
kbr hover 1                           # Hover over element
kbr focus 1                           # Focus element
kbr drag 1 5                          # Drag element 1 to element 5

# Mouse (low-level coordinate-based)
kbr mouse move 100 200                # Move to coordinates
kbr mouse click 100 200               # Click at coordinates
kbr mouse click --button right 100 200  # Right-click
kbr mouse down 100 200                # Press button
kbr mouse up 100 200                  # Release button
kbr mouse wheel 100 200 300           # Scroll wheel

# Get information
kbr get text 1                        # Get element text
kbr get html 1                        # Get element inner HTML
kbr get value 1                       # Get form element value
kbr get attr 1 href                   # Get element attribute
kbr get url                           # Get current URL
kbr get title                         # Get page title
kbr get count "li.item"               # Count elements matching CSS
kbr get box 1                         # Get element bounding box
kbr get styles 1                      # Get computed styles
kbr get cdp-url                       # Get CDP WebSocket URL

# State queries
kbr is visible 1                      # Returns true/false
kbr is enabled 1                      # Returns true/false
kbr is checked 1                      # Returns true/false

# Wait
kbr wait time 2s                      # Wait for duration
kbr wait load                         # Wait for page fully loaded
kbr wait selector "#modal"            # Wait for element to appear
kbr wait hidden ".spinner"            # Wait for element to disappear
kbr wait url "*login*"                # Wait for URL pattern (* wildcard)
kbr wait text "Welcome"               # Wait for text to appear
kbr wait func "window.ready"          # Wait for JS expression to be truthy
kbr wait download ./downloads         # Wait for download to complete

# Downloads & Uploads
kbr upload 3 ./file.pdf               # Upload file to input element
kbr download 5 ./output               # Click element to trigger download

# Network
kbr network start-logging             # Start recording requests
kbr network requests                  # List recorded requests
kbr network route "*.ads.*" --action block   # Block matching requests
kbr network route "*.js" --action continue   # Monitor without blocking
kbr network unroute "*.ads.*"         # Remove route rule
kbr network clear                     # Clear recorded requests

# Viewport & Device Emulation
kbr set viewport 1920 1080            # Set viewport size
kbr set viewport 1920 1080 2          # 2x retina
kbr set device "iPhone 12"            # Emulate device (viewport + UA)
kbr set geo 37.7749 -122.4194         # Override geolocation
kbr set offline true                  # Enable offline mode
kbr set headers X-Token=abc           # Set extra HTTP headers
kbr set credentials admin pass        # Set HTTP Basic Auth
kbr set media prefers-color-scheme=dark  # Emulate CSS media feature
kbr set colorscheme dark              # Shortcut for dark mode

# Capture
kbr screenshot page.png               # Screenshot to file
kbr screenshot -f full.png            # Full page screenshot
kbr screenshot -a annotated.png       # Annotated with element IDs
kbr screenshot --element 5 el.png     # Capture specific element
kbr screenshot -q 80 page.jpeg        # JPEG with quality
kbr pdf output.pdf                    # Save as PDF
kbr pdf -l landscape.pdf              # Landscape PDF

# Clipboard
kbr clipboard read                    # Read text from clipboard
kbr clipboard write "Hello"           # Write text to clipboard
kbr clipboard copy                    # Copy current selection
kbr clipboard paste                   # Paste into focused element

# Console & Errors
kbr console start                     # Start collecting console messages
kbr console messages                  # Get collected messages
kbr console messages --level error    # Filter by level
kbr console clear                     # Clear messages
kbr errors list                       # List page JS errors
kbr errors clear                      # Clear errors

# JavaScript execution
kbr eval "document.title"             # Evaluate JS expression
kbr eval "document.querySelectorAll('a').length"

# Diff (compare page states)
kbr diff snapshot                     # Compare current vs last snapshot
kbr diff snapshot -b before.txt       # Compare current vs saved file
kbr diff screenshot -b before.png     # Visual pixel diff
kbr diff url <url1> <url2>            # Compare two pages

# Tabs
kbr tab list                          # List all open tabs
kbr tab new https://other.com         # Open new tab
kbr tab switch 1                      # Switch to tab by index
kbr tab close 1                       # Close tab by index

# Sessions
kbr session                           # Show current session name
kbr session list                      # List all active sessions

# Cookies
kbr cookies get                       # Get all cookies
kbr cookies set token abc --domain example.com --secure --http-only
kbr cookies delete token              # Delete cookie by name
kbr cookies clear                     # Clear all cookies

# Storage (localStorage / sessionStorage)
kbr storage list                      # List all entries
kbr storage get theme                 # Get value
kbr storage set theme dark            # Set value
kbr storage delete theme              # Delete key
kbr storage clear                     # Clear all
kbr storage get key --type session    # Use sessionStorage

# State import/export
kbr state export auth.json            # Export cookies + localStorage
kbr state import auth.json            # Import from file

# Auth vault
kbr auth save mysite --url <url> --username <user> --password <pass>
kbr auth login mysite                 # Login using saved profile
kbr auth list                         # List saved profiles
kbr auth show mysite                  # Show profile details
kbr auth delete mysite                # Delete profile

# Debugging
kbr highlight 1                       # Highlight element with red border
kbr inspect                           # Open DevTools (headed mode only)

# Tracing & Profiling
kbr trace start                       # Start Chrome trace
kbr trace stop trace.json             # Stop and save
kbr profiler start                    # Start CPU profiling
kbr profiler stop profile.json        # Stop and save
kbr record start                      # Record screenshot sequence
kbr record stop                       # Stop recording

# Confirmation (when --confirm-actions is set)
kbr confirm                           # Approve pending action
kbr deny                              # Reject pending action

# Find elements (semantic locators, alternative to snapshot IDs)
kbr find role button --name "Submit"  # By ARIA role + name
kbr find text "Sign In"               # By accessible name
kbr find label "Email"                # By label text
kbr find placeholder "Search"         # By placeholder
kbr find alt "logo"                   # By image alt text
kbr find title "info"                 # By title attribute
kbr find testid "submit-btn"          # By data-testid
kbr find first "div.item"             # First CSS match
kbr find last "div.item"              # Last CSS match
kbr find nth 2 "div.item"            # Nth CSS match
```

## ID Lifecycle (Important)

IDs (`1`, `2`, `3`, ...) are invalidated when the page changes. Always re-snapshot after:

- Clicking links or buttons that navigate
- Form submissions
- Dynamic content loading (dropdowns, modals)

```bash
kbr click 5                           # Navigates to new page
kbr snapshot -i                       # MUST re-snapshot
kbr click 1                           # Use new IDs
```

IDs are strictly sequential integers starting from 1, assigned via depth-first traversal of the accessibility tree. They are temporary — never cache IDs across snapshots.

## Snapshot Format

The snapshot is a text representation of the browser's Accessibility Tree. Each line represents one element:

```
<indent><id>: <role> "<name>" [value="<value>"] [<state1> <state2> ...]
```

Example:
```
Page: "Login - GitHub"

1: link "GitHub"
2: heading "Sign in to GitHub"
3: textbox "Username or email" required
4: textbox "Password" required
5: link "Forgot password?"
6: button "Sign in"
7: link "Create an account"
```

**Format details:**
- `Page: "title"` — root node, not interactive, no ID assigned
- 2-space indentation indicates tree depth
- Names are truncated at 80 characters with `...`
- Values shown only when different from name (e.g., `value="admin"`)
- Common states: `focused`, `disabled`, `checked`, `expanded`, `collapsed`, `selected`, `required`, `readonly`, `multiline`

**Why numeric IDs:** Token-efficient for LLMs. `5: button "Submit"` uses fewer tokens than `@e5 button "Submit"` or `[5] button "Submit"`. LLMs reference elements with just a number: `kbr click 5`.

## Common Patterns

### Form Submission

```bash
kbr open https://example.com/signup
kbr snapshot -i
kbr fill 1 "Jane Doe"
kbr fill 2 "jane@example.com"
kbr select 3 "California"
kbr check 4
kbr click 5
kbr wait load
```

### Authentication with Auth Vault

```bash
# Save credentials once
kbr auth save github --url https://github.com/login --username user --password pass

# Login using saved profile (LLM never sees password)
kbr auth login github

# List/show/delete profiles
kbr auth list
kbr auth show github
kbr auth delete github
```

### Authentication with State Persistence

```bash
# Login once and save state
kbr open https://app.example.com/login
kbr snapshot -i
kbr fill 1 "$USERNAME"
kbr fill 2 "$PASSWORD"
kbr click 3
kbr wait url "*dashboard*"
kbr state export auth.json

# Reuse in future sessions
kbr state import auth.json
kbr open https://app.example.com/dashboard
```

### Data Extraction

```bash
kbr open https://example.com/products
kbr snapshot -i
kbr get text 5                        # Get specific element text
kbr get title                         # Get page title
kbr get url                           # Get current URL

# JSON output for parsing
kbr snapshot -i --json
kbr get text 1 --json
```

### Parallel Sessions

```bash
kbr --session site1 open https://site-a.com
kbr --session site2 open https://site-b.com

kbr --session site1 snapshot -i
kbr --session site2 snapshot -i

kbr session list
```

### Viewport & Responsive Testing

```bash
# Desktop
kbr set viewport 1920 1080
kbr screenshot desktop.png

# Mobile
kbr set viewport 375 812
kbr screenshot mobile.png

# Retina: same CSS layout, higher pixel density
kbr set viewport 1920 1080 2
kbr screenshot retina.png

# Device emulation (viewport + user agent)
kbr set device "iPhone 12"
kbr screenshot device.png
```

### Visual Browser (Debugging)

```bash
kbr --headed open https://example.com
kbr highlight 1                       # Highlight element
kbr inspect                           # Open Chrome DevTools
kbr record start                      # Record session
kbr profiler start                    # Start profiling
kbr profiler stop trace.json          # Stop and save
```

### Local Files

```bash
kbr --allow-file-access open file:///path/to/page.html
kbr snapshot -i
kbr screenshot output.png
```

### Color Scheme (Dark Mode)

```bash
kbr set colorscheme dark
kbr screenshot dark.png

# Or via media feature emulation
kbr set media prefers-color-scheme=dark
```

## Annotated Screenshots (Vision Mode)

Use `--annotate` (`-a`) to take a screenshot with numbered labels overlaid on interactive elements. This helps when:

- The page has unlabeled icon buttons or visual-only elements
- You need to verify visual layout or styling
- Canvas or chart elements are present (invisible to text snapshots)

```bash
kbr screenshot -a annotated.png
```

## Diffing (Verifying Changes)

Use `diff snapshot` after performing an action to verify it had the intended effect:

```bash
# Typical workflow: snapshot -> action -> diff
kbr snapshot -i                       # Take baseline snapshot
kbr click 2                           # Perform action
kbr diff snapshot                     # See what changed
```

For visual regression or monitoring:

```bash
# Save a baseline, then compare later
kbr screenshot baseline.png
# ... changes happen ...
kbr diff screenshot -b baseline.png

# Compare two URLs
kbr diff url https://staging.example.com https://prod.example.com
```

`diff snapshot` output uses `+` for additions and `-` for removals, similar to git diff. `diff screenshot` produces a diff image with changed pixels highlighted.

## Timeouts and Slow Pages

The default timeout is 30 seconds (configurable with `--timeout`). For slow pages, use explicit waits:

```bash
# Wait for network to settle
kbr wait load

# Wait for a specific element
kbr wait selector "#content"

# Wait for a URL pattern (useful after redirects)
kbr wait url "*dashboard*"

# Wait for a JS condition
kbr wait func "document.readyState === 'complete'"

# Wait a fixed duration as a last resort
kbr wait time 5s
```

When dealing with slow sites, use `kbr wait load` after `kbr open` to ensure the page is fully loaded before taking a snapshot.

## Session Management and Cleanup

When running multiple agents concurrently, use named sessions to avoid conflicts:

```bash
# Each agent gets its own isolated session
kbr --session agent1 open site-a.com
kbr --session agent2 open site-b.com

# Check active sessions
kbr session list
```

Always close your session when done to avoid leaked daemon processes:

```bash
kbr close                             # Close default session
kbr --session agent1 close            # Close specific session
```

## Security

### Content Boundaries

Enable `--content-boundaries` to wrap page-sourced output in markers that help LLMs distinguish tool output from untrusted page content:

```bash
kbr --content-boundaries snapshot
# Output wrapped in:
# <ko-browser-content>
# [accessibility tree]
# </ko-browser-content>
```

## Configuration File

Create `ko-browser.json` in the project root for persistent settings:

```json
{
  "headed": true,
  "proxy": "http://localhost:8080",
  "profile": "./browser-data"
}
```

Priority (lowest to highest): config file < env vars < CLI flags. Use `--config <path>` for a custom config location.
