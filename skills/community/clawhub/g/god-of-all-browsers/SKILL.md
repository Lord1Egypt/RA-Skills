---
name: god-of-all-browsers
description: A 100x smarter browser automation CLI that mimics human behavior using a native stateful Chromium instance. It supports multi-tab management, bypasses bot detection, auto-closes popups, and preserves cookies permanently.
tools:
  - shell
---

# `God of all Browsers`

A stateful, multi-tab Puppeteer skill designed to help AI agents automate heavily protected websites the exact same way a human does.

It solves three critical AI problems:

1. **Tabs & Statefulness:** It launches a single background browser that stays open. Navigations, clicks that open new tabs, and cookies are remembered across multiple commands!
2. **Vision Abstraction:** AI cannot "see" coordinates well, so `snapshot` maps the DOM, assigns a `[tag]` ID to every visible button/input, and takes a screenshot. The AI just says "Click tag [15]."
3. **Bot Evasion:** Uses `headless: false`, custom user agents, removed `webdriver` footprints, and canvas spoofing.

**Important Setup:** Ensure the Chromium path is correct (`C:\Program Files\Google\Chrome\Application\chrome.exe` for Win or `/usr/bin/chromium` for Linux) and `puppeteer-core` is installed.

## 🚀 COMMANDS & WORKFLOW

### 1. Start the Browser (Required First Step)

Launch the browser in the background. It will use a persistent `chrome_profile` directory so you **NEVER** lose login sessions.

```bash
# Standard mode (Recommended for debugging)
node browser.js start

# Headless mode (Faster, silent background)
# Note: Automatically enabled if running in Termux.
node browser.js start --headless
```

### 2. Take a Snapshot (And auto-close popups)

This is your "eyes". Run this before any interaction to get the active window's current state and a list of clickable `[tag]` IDs.

```bash
# If navigating somewhere new:
node browser.js snapshot --url "https://www.google.com"

# If already on the page (refresh DOM):
node browser.js snapshot
```

_Wait for this command to output the JSON array of tags._ It will also automatically click away annoying Chatbot/Notification popups.

### 3. Click or Type (Like a human)

Use the tags captured during the snapshot.

```bash
# Click a button or link (e.g. tag [24])
node browser.js click --tag "[24]"

# Type into an input box (e.g. tag [5])
node browser.js type --tag "[5]" --text "MERN Stack Developer"

# Press a specific keyboard key (Default: Enter)
node browser.js press --key "Enter"
```

### 4. Reading & Content Extraction

Extract text content from any element using tags or CSS selectors.

```bash
# Read visible text from a specific tag
node browser.js read --tag "[12]"

# Read content of a specific CSS selector (e.g. the main article)
node browser.js read --selector "article.main-content"

# Deep-expand hidden content (clicks Read More/Show All buttons automatically)
node browser.js expand
```

### 5. Tab Management

Many sites open clicked links in a new tab! If your `click` command opens a new tab, the CLI will automatically say:
`⚠️ A NEW TAB WAS OPENED!! Automatically switched context to Tab [1].`

You can manually manage tabs using:

```bash
# List all currently open tabs
node browser.js check-tabs

# Switch to a specific tab index (e.g. going back to the search page: tab 0)
node browser.js switch-tab --index 0

# Just check the very current URL you are viewing:
node browser.js check-url
```

### 5. Find Tags (Accurate Filtered Search)

Use this to filter elements by keywords instead of reading a massive snapshot. It can search live on the current page or in a previously saved JSON file.

```bash
# Search live for "Apply" or "Success" buttons
node browser.js find --query "apply,success"

# Search within a specific saved snapshot file (e.g., to verify output)
node browser.js find --file "snapshot.json" --query "applied,successfully"
```

### 6. Refresh Page

Manually reload the current tab. Useful for status updates.

```bash
node browser.js refresh
```

### 7. Scrape Meta Tags (SEO/OpenGraph)

Extract hidden page data like Title, Description, and Social Media tags.

```bash
node browser.js scrap-meta
```

### 8. Dynamic Evolution (Eval)

Execute custom JavaScript logic directly in the browser context. **Note: For security, the `--force` flag is required.** Supports both inline code and script files.

```bash
# Execute inline code (Requires --force)
node browser.js eval --code "return { links: document.querySelectorAll('a').length }" --force

# Execute from a file (Requires --force)
node browser.js eval --file "custom_script.js" --force
```

### 9. Google Search (Direct Extraction)

Get the top 5 organic search results (Titles, Links, Snippets) in a single command. Extremely fast and agent-friendly.

```bash
node browser.js google --query "Mathanraj Murugesan"
```

### 10. Session & Learning

Manage your login state and keep track of automation failures for self-correction.

```bash
# Save current cookies to session.json (persists across runs)
node browser.js save-session

# Check if the page requires login or if the user already logged in
node browser.js auth-status

# Log a failure and a lesson learned for AI self-correction
node browser.js log-learning --failed "Selector [12] was hidden" --fixed "Used [expand] first" --lessons "Always try expanding content before reading"
```

### 11. Stop the Browser

Clean up resources when the task is entirely finished.

```bash
node browser.js stop
```

## 🧠 AI STRATEGY (HOW TO USE)

1. Run `start`.
2. Run `snapshot --url "[TARGET]"`.
3. Check `auth-status` if the page is restricted. Use `save-session` after manual/automated login.
4. Analyze the output tags. Think step-by-step. Does the page require a search? Does it require clicking an 'Apply' button?
5. Run `click` or `type` on the specific `[tag]`.
6. **READ THE CLICK OUTPUT CAREFULLY!** Did it say a new tab opened? If so, your next `snapshot` will read from that tab.
7. Run `snapshot` again WITHOUT a URL to read the new page/modal that loaded.
8. Repeat until the task is complete. If you need to return to the search results, run `check-tabs` and `switch-tab --index 0`.
9. If you encounter a bug (e.g., selector not found), use `log-learning` to record the fix for future runs.
10. If you need to run custom JS, use `eval` with the `--force` flag.
11. Once finished, run `stop`.

### 10. Common Extraction Patterns (USE EVAL)

When you need to get actual data (not just see the page), use the `eval` command with these patterns:

**Google Search Results:**

```bash
node browser.js eval --force --code "return Array.from(document.querySelectorAll('div.g')).slice(0,5).map(g => ({ title: g.querySelector('h3')?.innerText, link: g.querySelector('a')?.href }))"
```

**LinkedIn Profile (Basic):**

```bash
node browser.js eval --force --code "return { name: document.querySelector('.text-heading-xlarge')?.innerText, title: document.querySelector('.text-body-medium')?.innerText }"
```

**General Link Scraper:**

```bash
node browser.js eval --force --code "return Array.from(document.querySelectorAll('a')).map(a => ({ text: a.innerText, url: a.href })).filter(a => a.url.startsWith('http'))"
```

### 11. Robust Automation Workflow (Multi-Tab & State)

Follow this professional flow for complex, multi-stage automation tasks:

1.  **Initialize**: Run `start` to launch the persistent browser instance.
2.  **Navigation & Auth**: 
    - Run `snapshot --url "[TARGET]"` to land on the page.
    - Run `auth-status` to check if a login is required.
    - If you perform a manual/auto login, run `save-session` to persist the state.
3.  **Clean & Expand**: 
    - Always run `expand` before deep scanning. This removes popups and reveals hidden content that might be missing from the DOM.
4.  **Action Loop**:
    - Run `snapshot` (without URL) to get the latest `[tag]` list.
    - Perform interactions using `click`, `type`, or `press`.
    - **Pro Tip**: If a click result is ambiguous, run `check-url` to see if the page changed.
5.  **Multi-Tab Handling**:
    - If the terminal warns `⚠️ A NEW TAB WAS OPENED`, run `check-tabs`.
    - Note the index of the new tab (e.g., `[1]`) and run `switch-tab --index 1`.
    - Every snapshot and command thereafter will target this new tab.
6.  **Extraction**:
    - Use `read --tag "[#]"` for simple text.
    - Use `eval` for complex data structures (arrays of objects, etc.).
7.  **Recovery & Learning**:
    - If a command fails, use `log-learning --failed "..." --fixed "..."` to document the solution for the AI's internal memory.
8.  **Teardown**: Run `stop` only when the entire job (across all domains) is finished.
