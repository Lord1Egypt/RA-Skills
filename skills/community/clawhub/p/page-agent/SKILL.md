---
name: page-agent
license: MIT
description: Enhanced browser DOM manipulation using PageAgent's page-controller. Injects into any web page to provide precise DOM extraction, interactive element detection (cursor:pointer heuristic), and robust interaction (full event chain simulation, React-compatible input). Use when you need to operate on web pages with precision — clicking, typing, scrolling, form filling, or reading page structure. Combines with frontend-design skill for full design→code→browser-operate workflow.
---

# PageAgent Browser Enhancement Skill

Injects [alibaba/page-agent](https://github.com/alibaba/page-agent) v1.5.6 `PageController` into web pages via the browser tool's evaluate action. Gives you **superior DOM manipulation** compared to basic browser actions.

## Key Advantages Over Basic Browser Tool

1. **cursor:pointer heuristic** — detects clickable elements even without semantic tags
2. **Full event chain** — mouseenter→mouseover→mousedown→focus→mouseup→click (not just `.click()`)
3. **React/Vue compatible input** — uses native value setter to bypass framework interception
4. **contenteditable support** — proper beforeinput/input event dispatch
5. **Indexed elements** — `[N]<tag>` format for precise LLM-directed operations
6. **Incremental change detection** — `*[N]` marks new elements since last step

## Usage Flow

### Step 1: Inject PageController into the page

Use the CDP injection script (handles the 72KB library injection):

```bash
node ~/.openclaw/workspace/skills/page-agent/scripts/inject-cdp.mjs <TARGET_ID>
```

Where `TARGET_ID` is from `browser(action="open", ...)`. The script injects both `page-controller-global.js` and `inject.js` via CDP WebSocket, outputting `✅ injected` on success.

### Step 2: Get page state (DOM extraction)

```javascript
// Returns { url, title, header, content, footer }
// content is the LLM-readable simplified HTML with indexed interactive elements
const state = await window.__PA__.getState();
return JSON.stringify({ url: state.url, title: state.title, content: state.content, footer: state.footer });
```

The `content` field looks like:
```
[0]<a aria-label=首页 />
[1]<div >PageAgent />
[2]<button role=button>快速开始 />
[3]<input placeholder=搜索... type=text />
```

### Step 3: Perform actions by index

```javascript
// Click element at index 2
await window.__PA__.click(2);

// Type text into input at index 3
await window.__PA__.input(3, "hello world");

// Select dropdown option
await window.__PA__.select(5, "Option A");

// Scroll down 1 page
await window.__PA__.scroll(true, 1);

// Scroll specific element
await window.__PA__.scrollElement(4, true, 1);
```

### Step 4: Re-read state after actions

After each action, call `getState()` again to see the updated DOM. Look for `*[N]` markers which indicate newly appeared elements.

## Practical Workflow: Design → Code → Operate

1. **Design**: Use `frontend-design` skill to create the page
2. **Serve**: Start a local dev server (`npx serve` or framework dev server)
3. **Open**: `browser(action="open", targetUrl="http://localhost:3000")`
4. **Inject**: Load PageController into the page (Step 1 above)
5. **Inspect**: Get DOM state to understand current page structure
6. **Operate**: Click, type, scroll to test and interact with the page
7. **Iterate**: Modify code based on what you observe, re-inject, repeat

## Tips

- Always re-inject after page navigation (SPA route changes are fine, full reloads need re-inject)
- The `content` output is token-efficient — use it instead of screenshots when possible
- For long pages, use scroll + getState to see content below the fold
- Clean up highlights with `window.__PA__.cleanUp()` before taking screenshots
- Use `profile="openclaw"` for the isolated browser, or `profile="chrome"` for the Chrome extension relay

## Files

- `scripts/page-controller.js` — PageController library (72KB, from @page-agent/page-controller@1.5.6)
- `scripts/inject.js` — Helper wrapper that creates `window.__PA__` API
