---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
version: 1.1.0
license: Complete terms in LICENSE.txt
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

## Triggers
Activate this skill when the user wants to:
- Verify frontend functionality of a local web application
- Debug UI behavior or capture browser screenshots
- Automate browser interactions (form fills, button clicks, navigation)
- View browser console logs or test rendering
- Write Playwright automation scripts for local dev environments

**This skill is for local development environments only.** Do not run against production URLs.

## NOT For
- **Production testing** — do not run against live production URLs; use staging only
- **Load testing or performance testing** — use dedicated tools (k6, Locust, etc.)
- **API-only testing** — no browser needed; use `exec` with curl or httpx
- **Visual regression testing at scale** — this skill handles functional automation, not pixel-diffing

---

**Helper Scripts Available**:
- `scripts/with_server.py` - Manages server lifecycle (supports multiple servers)

**Always run scripts with `--help` first** to see usage. Prefer calling scripts directly rather than reading large source files into context. If customization is needed, read the relevant section of the source. All bundled scripts are open-source and auditable — review them before first use in any new environment.

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server (safe default — no shell):**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers:**
```bash
python scripts/with_server.py \
  --server "python server.py" --port 3000 \
  --server "npm run dev" --port 5173 \
  -- python your_automation.py
```

**Compound commands (explicit shell mode — only for trusted commands):**
```bash
python scripts/with_server.py --shell \
  --server "cd backend && python server.py" --port 3000 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Safety & Security

- **Local-only:** This skill targets `localhost` development servers only. Never use it against production URLs.
- **Script auditing:** All bundled scripts (`scripts/with_server.py`) are open-source Python. Review them before first use.
- **Server commands:** The `with_server.py` helper runs server commands as argv by default (no shell interpretation, safe against injection). For compound commands requiring shell features (`cd && ...`, pipes), use the explicit `--shell` flag. Shell mode should only be used with trusted commands you've reviewed.
- **No network exfiltration:** Playwright connects only to localhost. No data is sent to external endpoints.
- **No credentials:** This skill does not require, store, or transmit any API keys or tokens.

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly. 
- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or `page.wait_for_timeout()`

## Reference

The `scripts/with_server.py` helper is the primary bundled utility. Check `scripts/` for any other available helpers before writing custom code.