# Pagerunner Tools Reference

Complete documentation for Pagerunner MCP tools (~44 total as of upstream v0.8.0).

Tool families:

| Section | Tools |
|---|---|
| [Sessions & Tabs](#sessions--tabs-8-tools) | `open_session`, `attach_session`, `close_session`, `list_sessions`, `list_tabs`, `new_tab`, `close_tab`, `navigate` |
| [Navigation & Content](#navigation--content-5-tools) | `wait_for`, `get_content`, `screenshot`, `evaluate`, `scroll` |
| [Interactions](#interactions-5-tools) | `click`, `type_text`, `fill`, `select`, `scroll` |
| [Snapshots & Tab State](#snapshots--state-6-tools) | `save_snapshot`, `restore_snapshot`, `list_snapshots`, `delete_snapshot`, `save_tab_state`, `restore_tab_state` |
| [Session Checkpoints](#session-checkpoints-4-tools) *(v0.6.0+)* | `save_session_checkpoint`, `restore_session_checkpoint`, `list_session_checkpoints`, `delete_session_checkpoint` |
| [Key-Value Store](#key-value-store-5-tools) | `kv_set`, `kv_get`, `kv_list`, `kv_delete`, `kv_clear` |
| [Sealed Secrets](#sealed-secrets-4-tools) *(v0.7.0+)* | `extract_secret`, `use_secret`, `list_secrets`, `delete_secret` |
| [Network & Console](#network--console-2-tools) *(v0.3.0+)* | `get_network_log`, `get_console_log` |
| [Site Intelligence](#site-intelligence-4-tools) *(v0.5.0+)* | `get_site_knowledge`, `register_adapter`, `call_site_api`, `generate_adapter` |
| [Video Recording](#video-recording-7-tools) *(v0.8.0+)* | `start_recording`, `stop_recording`, `add_marker`, `list_recordings`, `get_recording`, `delete_recording`, `render_recording` |
| [Notifications](#notifications-1-tool) *(macOS)* | `notify` |

---

## Sessions & Tabs (8 tools)

### `open_session(profile, anonymize?, stealth?, allowed_domains?)`

**Launch a Chrome instance with a specific profile.**

**Arguments:**
- `profile` (string, required) — Chrome profile name from config.toml
- `anonymize` (boolean, optional) — Strip PII from get_content and evaluate results
- `stealth` (boolean, optional) — Hide automation signals (navigator.webdriver, etc.)
- `allowed_domains` (string[], optional) — Restrict navigation to these domains only

**Returns:** `session_id` (string)

**Examples:**

```javascript
// Basic: open your personal Chrome
const s1 = await open_session({ profile: "personal" });

// With security options
const s2 = await open_session({
  profile: "agent-work",
  stealth: true,
  allowed_domains: ["jira.mycompany.com", "github.com"]
});

// With anonymization (ICP 3)
const s3 = await open_session({
  profile: "agent-sensitive",
  anonymize: true,
  anonymization_mode: "tokenize"
});
```

**ICP Context:**
- **ICP 1:** `profile: "personal"` — your real Chrome with all logins
- **ICP 2:** Dedicated agent profile, saved with snapshots
- **ICP 3:** `anonymize: true` mandatory for sensitive data
- **ICP 4:** Session ID stored in KV for resumption across runs

**See Also:** PATTERNS.md → Pattern 1 (Session Management)

---

### `close_session(session_id)`

**Terminate a Chrome instance and release its resources.**

**Arguments:**
- `session_id` (string, required) — Session ID from open_session

**Returns:** Success message

**Example:**

```javascript
await close_session(sessionId);
```

**When to Call:**
- After completing a workflow
- To free resources before opening a new session
- Always close to avoid dangling Chrome processes

**Auto-Checkpoint (v0.6.0+):** Calling `close_session` automatically writes an "Autosave · close" checkpoint before terminating. This means session state is preserved even if you don't explicitly call `save_snapshot`.

---

### `attach_session(profile, debug_port, ...)` *(v0.6.0+)*

**Attach to a Chrome instance that's already running with `--remote-debugging-port`.**

Use this when you launched Chrome yourself (or a previous process did) and want Pagerunner to take over without killing and re-launching the browser. The Chrome must have been started with `--remote-debugging-port=<port>` on `127.0.0.1`.

**Arguments:**
- `profile` (string, required) — Chrome profile name (used for config lookup and the session registry)
- `debug_port` (number, required) — Port Chrome is listening on (e.g. `9222`)
- `anonymize` / `stealth` / `allowed_domains` — same meaning as `open_session`

**Returns:** `session_id` (string), just like `open_session`.

**Example:**

```javascript
// Chrome already running on port 9222
const sessionId = await attach_session({
  profile: "personal",
  debug_port: 9222
});
```

**When to use:**
- You want to preserve a hand-launched Chrome (e.g. during interactive debugging).
- A previous daemon crashed; you want to reattach without the startup reconciliation path.
- Integration tests that spin up Chrome separately.

**See Also:** `list_sessions` — reattached sessions are listed with `status` = `Alive`.

---

### `list_sessions()`

**List all active Chrome sessions.**

**Returns:** Array of session objects

```json
[
  { "id": "sess_abc123", "profile": "personal", "stealth": false, "anonymize": false, "alive": true, "status": "Alive" },
  { "id": "sess_def456", "profile": "agent-work", "stealth": true, "anonymize": true, "alive": true, "status": "Reconnecting" }
]
```

**`status` field (v0.7.0+):**
- `Alive` — healthy, tools should succeed
- `Reconnecting` — CDP WebSocket dropped (e.g. sleep/wake); auto-reconnecting with exponential backoff. Tool calls during this state return structured errors with retry hints — retry after a short delay.
- `Recovering` — Chrome process died; daemon is spawning a new Chrome and restoring the latest checkpoint. Same session ID — no need to call `open_session`.
- `Dead` — recovery failed. Call `close_session` and open a new one.

`alive` (boolean) is kept for backward compatibility and is `true` for everything except `Dead`.

See [ADVANCED.md § Daemon Hardening](ADVANCED.md#daemon-hardening-and-auto-recovery-v070) for the full state machine.

**Example:**

```javascript
const sessions = await list_sessions();
for (const session of sessions) {
  console.log(`Session ${session.id} (profile: ${session.profile})`);
}
```

**ICP Context:**
- **ICP 4:** Daemon mode lists sessions across multiple agents
- **Metadata hint:** Response includes `_total` and `_schema` for clarity

**Session Persistence (v0.6.0+):** Sessions persist across daemon restarts. After a daemon restart, `list_sessions()` shows reattached sessions — Chrome windows that survived the restart. Dead sessions are automatically cleaned up from the registry.

---

### `list_tabs(session_id)`

**List all open tabs in a session.**

**Arguments:**
- `session_id` (string, required)

**Returns:** Array of tab objects

```json
[
  { "target_id": "TAB_123", "url": "https://example.com", "title": "Example Site" },
  { "target_id": "TAB_456", "url": "https://github.com/foo/bar", "title": "foo/bar" }
]
```

**Example:**

```javascript
const tabs = await list_tabs(sessionId);
const firstTab = tabs[0].target_id;  // Use in navigate, get_content, etc.
console.log(`Found ${tabs.length} tabs`);
```

**Common Pattern:**

```javascript
const sessionId = await open_session({ profile: "personal" });
const [tab] = await list_tabs(sessionId);  // Get first tab
await navigate(sessionId, tab.target_id, "https://example.com");
```

---

### `new_tab(session_id, url?)`

**Open a new tab in the session.**

**Arguments:**
- `session_id` (string, required)
- `url` (string, optional) — URL to open in the new tab

**Returns:** New tab object

**Examples:**

```javascript
// Open a new blank tab
const newTab = await new_tab(sessionId);

// Open a new tab with URL
const newTab = await new_tab(sessionId, "https://example.com");

// Open multiple tabs in parallel
const [tab1, tab2, tab3] = await Promise.all([
  new_tab(sessionId, "https://site-a.com"),
  new_tab(sessionId, "https://site-b.com"),
  new_tab(sessionId, "https://site-c.com")
]);
```

**ICP Context:**
- **ICP 1:** Multiple tabs for research (docs, tests, design specs)
- **ICP 5:** Parallel scraping across multiple sources

---

### `close_tab(session_id, target_id)`

**Close a single tab in a session.** Fails if it's the last tab — use `close_session` instead.

**Arguments:**
- `session_id` (string, required)
- `target_id` (string, required) — Tab to close

**Returns:** Success message; the remaining tabs in the session are unaffected.

**Example:**

```javascript
// Close only the scratch tab, keep the session running
await close_tab(sessionId, scratchTabId);
```

**When to use:**
- Long-running sessions that accumulate tabs (e.g. research agents).
- Cleanup after a sub-task without tearing down the whole session.

---

### `navigate(session_id, target_id, url)`

**Navigate a tab to a URL.**

**Arguments:**
- `session_id` (string, required)
- `target_id` (string, required) — Tab ID from list_tabs or new_tab
- `url` (string, required) — URL to navigate to

**Returns:** Success message

**Examples:**

```javascript
await navigate(sessionId, tabId, "https://example.com");

// Navigate to local dev server
await navigate(sessionId, tabId, "http://localhost:3000");

// Navigate to new URL after user interaction
await click(sessionId, tabId, ".next-page-link");
await navigate(sessionId, tabId, "https://example.com/page-2");
```

**Important:** After navigate, always use `wait_for` before interacting:

```javascript
await navigate(sessionId, tabId, "https://app.example.com");
await wait_for(sessionId, tabId, selector: ".main-content", ms: 5000);
// Now safe to click, fill, etc.
```

**Metadata Hint:** Response includes `_requested_url` — verify navigation succeeded.

---

## Navigation & Content (5 tools)

### `wait_for(session_id, target_id, selector?, url?, ms?)`

**Wait for a condition: CSS selector appears, URL changes, or fixed time passes.**

**Arguments:**
- `session_id`, `target_id` (required)
- `selector` (string) — CSS selector to wait for
- `url` (string) — URL pattern to match (glob-style)
- `ms` (number) — Fixed delay in milliseconds
- **Note:** Exactly one of `selector`, `url`, or `ms` required

**Returns:** Success message (or timeout error)

**Examples:**

```javascript
// Wait for selector (element appears)
await wait_for(sessionId, tabId, selector: ".load-more-btn", ms: 5000);

// Wait for URL change
await wait_for(sessionId, tabId, url: "**/dashboard", ms: 5000);

// Fixed delay
await wait_for(sessionId, tabId, ms: 2000);

// With timeout
try {
  await wait_for(sessionId, tabId, selector: ".popup", ms: 3000);
} catch {
  console.log("Popup didn't appear");
}
```

**Metadata Hint:** Response includes `_condition_type` and `_condition_met`:
```json
{
  "_tool": "wait_for",
  "_condition_type": "selector",
  "_condition_met": true,
  "_note": "Condition met — proceed with next action"
}
```

**Common Mistakes:**
- ❌ Not waiting before clicking: `click()` → fails if element not ready
- ✅ Always: `wait_for(selector)` → `click()`

---

### `get_content(session_id, target_id)`

**Get visible text content of the page.**

**Arguments:**
- `session_id`, `target_id` (required)

**Returns:** String (cleaned, readable text)

**Examples:**

```javascript
const content = await get_content(sessionId, tabId);
console.log(content);

// With anonymization (ICP 3): content has PII replaced
// Original page: "Contact john@company.com"
// Returned: "Contact [EMAIL:abc123]"

// Use for structural inspection
if (content.includes("Login")) {
  await navigate(sessionId, tabId, "/login");
}
```

**What It Returns:**
- All visible text (no hidden elements)
- Sanitized HTML and zero-width characters removed
- Wrapped in `<<<UNTRUSTED_WEB_CONTENT>>>` markers for security
- With `anonymize: true`, PII replaced with tokens

**What It Doesn't Return:**
- HTML source (use `evaluate` if needed)
- Hidden form values
- JavaScript-only content that hasn't rendered

**ICP Context:**
- **ICP 1:** Verify page structure before filling forms
- **ICP 3:** Main way to read page content (all PII stripped)

**Metadata Hint:** Response warns about untrusted content.

---

### `screenshot(session_id, target_id)`

**Capture current viewport as PNG.**

**Arguments:**
- `session_id`, `target_id` (required)

**Returns:** Base64-encoded PNG image (or file path if saved locally)

**Examples:**

```javascript
// Take screenshot of current viewport
const img = await screenshot(sessionId, tabId);
// Returns base64: "data:image/png;base64,iVBORw0KGgo..."

// Common pattern: take screenshot to verify work
await navigate(sessionId, tabId, "http://localhost:3000");
const beforeShot = await screenshot(sessionId, tabId);

// Make a change
// ... edit code, wait for reload ...

const afterShot = await screenshot(sessionId, tabId);
// Compare before/after
```

**Full Page Screenshot:**

To capture more than viewport, scroll first:

```javascript
// Scroll to top
await evaluate(sessionId, tabId, "window.scrollTo(0, 0)");
const topShot = await screenshot(sessionId, tabId);

// Scroll to middle
await evaluate(sessionId, tabId, "window.scrollTo(0, document.body.scrollHeight / 2)");
const midShot = await screenshot(sessionId, tabId);

// Scroll to bottom
await evaluate(sessionId, tabId, "window.scrollTo(0, document.body.scrollHeight)");
const bottomShot = await screenshot(sessionId, tabId);
```

**ICP Context:**
- **ICP 1:** Verify UI changes from code edits
- **All:** Visual proof of what agent accomplished

---

### `evaluate(session_id, target_id, expression)`

**Run JavaScript in the page context and return the result.**

**Arguments:**
- `session_id`, `target_id` (required)
- `expression` (string) — JavaScript code to execute

**Returns:** Result of the expression (JSON-serializable)

**Examples:**

```javascript
// Simple value
const title = await evaluate(sessionId, tabId, "document.title");

// DOM inspection
const buttonCount = await evaluate(sessionId, tabId, `
  document.querySelectorAll('button').length
`);

// Structured extraction (ALWAYS return labeled objects)
const metrics = await evaluate(sessionId, tabId, `
  ({
    totalItems: document.querySelectorAll('.item').length,
    cartValue: parseFloat(document.querySelector('[data-total]').textContent),
    itemsInCart: document.querySelectorAll('.cart-item').length
  })
`);

// Trigger events
await evaluate(sessionId, tabId, `
  document.querySelector('input').focus();
  document.querySelector('input').dispatchEvent(new Event('focus', { bubbles: true }));
`);

// Access window globals
const userID = await evaluate(sessionId, tabId, "window.__USER_ID__");
```

**With Anonymization (ICP 3):**

```javascript
const sessionId = await open_session({
  profile: "sensitive",
  anonymize: true
});

// Evaluate still works, but returns sanitized
const content = await evaluate(sessionId, tabId, `
  document.querySelector('.user-email').textContent
`);
// Returns: "[EMAIL:abc123]" instead of "john@company.com"
```

**Metadata Hint:** Response includes `_result_type`:
```json
{
  "_result_type": "array",
  "_warning": "Result is an array — use labeled objects instead"
}
```

**Critical Rule:** Always return labeled objects, never arrays:

```javascript
// ❌ BAD (array — ambiguous)
return [25, 2];

// ✅ GOOD (labeled — clear)
return { likes: 25, replies: 2 };
```

**See Also:** HALLUCINATION_PREVENTION.md

---

## Interactions (5 tools)

### `click(session_id, target_id, selector)`

**Click an element matching the CSS selector.**

**Arguments:**
- `session_id`, `target_id` (required)
- `selector` (string) — CSS selector or data-testid

**Returns:** Success message

**Examples:**

```javascript
// Click a button
await click(sessionId, tabId, "button.submit");

// Click by data attribute (most stable)
await click(sessionId, tabId, "[data-testid='save-btn']");

// Click by aria-label
await click(sessionId, tabId, "button[aria-label='Close']");
```

**Always Wait Before Clicking:**

```javascript
await navigate(sessionId, tabId, newUrl);
await wait_for(sessionId, tabId, selector: ".button", ms: 5000);  // Wait first!
await click(sessionId, tabId, ".button");  // Now safe
```

**Common Mistakes:**
- ❌ Clicking without wait_for → "selector not found"
- ✅ Always `wait_for(selector)` before `click(selector)`

---

### `type_text(session_id, target_id, text, selector?)`

**Type text into an element (or focused element).**

**Arguments:**
- `session_id`, `target_id`, `text` (required)
- `selector` (string, optional) — CSS selector to focus first

**Returns:** Success message

**Examples:**

```javascript
// Type into focused element
await click(sessionId, tabId, "input[name='search']");
await type_text(sessionId, tabId, "search term");

// Type into specific element
await type_text(sessionId, tabId, "my text", selector: "input[name='comment']");

// Append to existing text
await type_text(sessionId, tabId, " continued...");
```

**When to Use type_text:**
- Plain HTML inputs
- Appending to existing text (doesn't clear first)
- Simple forms without React/Vue

**When to Use fill() instead:**
- React, Vue, Angular apps
- Need to clear field first
- Framework apps with change handlers

**ICP Context:** ICP 1 uses for search fields. ICP 2 uses for filling forms.

---

### `fill(session_id, target_id, selector, value)`

**Set input value and trigger change events (for React/Vue/Angular).**

**Arguments:**
- `session_id`, `target_id`, `selector`, `value` (required)

**Returns:** Success message

**Examples:**

```javascript
// Fill email input
await fill(sessionId, tabId, "input[name='email']", "user@example.com");

// Fill password input
await fill(sessionId, tabId, "input[type='password']", "secret");

// With anonymization: pass tokens, pagerunner de-tokenizes
await fill(sessionId, tabId, "input[name='reply-to']", "[EMAIL:abc123]");
// Pagerunner converts [EMAIL:abc123] to real email before typing

// Fill textarea
await fill(sessionId, tabId, "textarea[name='message']", "Multi-line\ntext here");
```

**How fill() Works:**
1. Focuses the element
2. Clears existing value (unlike type_text)
3. Types the new value
4. Fires synthetic change events (React/Vue compatible)

**ICP Context:**
- **ICP 1:** Filling UI forms for testing
- **ICP 2:** Agent filling work tools (Jira, etc.)
- **ICP 3:** Using tokens from anonymization

**See Also:** PATTERNS.md → Pattern 2 (Form Filling)

---

### `select(session_id, target_id, selector, value)`

**Select an option in a dropdown or multi-select.**

**Arguments:**
- `session_id`, `target_id`, `selector` (required)
- `value` (string or string[]) — Option value to select

**Returns:** Success message

**Examples:**

```javascript
// Single select
await select(sessionId, tabId, "select[name='country']", "US");

// Multi-select (multiple values)
await select(sessionId, tabId, "select[name='interests']", ["nodejs", "python", "rust"]);

// By data attribute
await select(sessionId, tabId, "[data-testid='status-dropdown']", "active");
```

---

### `scroll(session_id, target_id, selector?, x?, y?)`

**Scroll the page or scroll element into view.**

**Arguments:**
- `session_id`, `target_id` (required)
- `selector` (string, optional) — Element to scroll into view
- `x`, `y` (number, optional) — Pixel deltas to scroll

**Returns:** Success message

**Examples:**

```javascript
// Scroll down by 500px
await scroll(sessionId, tabId, x: 0, y: 500);

// Scroll to element
await scroll(sessionId, tabId, selector: ".load-more-btn");

// Scroll to top
await evaluate(sessionId, tabId, "window.scrollTo(0, 0)");

// Infinite scroll pattern
for (let i = 0; i < 5; i++) {
  await scroll(sessionId, tabId, x: 0, y: window.innerHeight);
  await wait_for(sessionId, tabId, ms: 500);  // Let content load
}
```

**ICP Context:** ICP 4 uses for scraping infinite-scroll lists.

**See Also:** PATTERNS.md → Pattern 7 (Scrolling)

---

## Snapshots & State (6 tools)

### `save_snapshot(session_id, target_id, origin)`

**Save authenticated session state (cookies + localStorage) for later restore.**

**Arguments:**
- `session_id`, `target_id` (required)
- `origin` (string, required) — URL origin to snapshot (e.g., `https://jira.mycompany.com`)

**Returns:** Snapshot ID

**Examples:**

```javascript
// First time: log in manually
const sessionId = await open_session({ profile: "agent-work" });
const [tab] = await list_tabs(sessionId);

await navigate(sessionId, tab.target_id, "https://jira.mycompany.com");
// ... manually fill login form ...
await click(sessionId, tab.target_id, ".login-btn");
await wait_for(sessionId, tab.target_id, selector: ".dashboard", ms: 10000);

// Save the authenticated state
await save_snapshot(sessionId, tab.target_id, origin: "https://jira.mycompany.com");
await close_session(sessionId);

// Later: restore it
const sessionId2 = await open_session({ profile: "agent-work" });
const [tab2] = await list_tabs(sessionId2);
await navigate(sessionId2, tab2.target_id, "https://jira.mycompany.com");
await restore_snapshot(sessionId2, tab2.target_id, origin: "https://jira.mycompany.com");
// Already logged in, no re-auth needed
```

**TOTP Handling:**

Log in manually (including TOTP), then snapshot. The saved cookies bypass TOTP in future restores:

```javascript
// Login with TOTP
await fill(..., "[data-testid='totp']", "123456");  // Human enters TOTP
await click(..., ".confirm-btn");
await wait_for(..., selector: ".post-auth-page");

// Now snapshot — post-TOTP session is saved
await save_snapshot(sessionId, tabId, origin);

// Next restore: no TOTP needed
await restore_snapshot(sessionId2, tabId2, origin);
```

**Encryption:** Snapshots are encrypted with AES-256-GCM. Key stored in macOS Keychain, never on disk.

**ICP Context:**
- **ICP 2:** Essential for agent profiles — no re-auth ever
- **ICP 4:** Auth checkpoints between agents

---

### `restore_snapshot(session_id, target_id, origin, from_profile?)`

**Restore previously saved authenticated session.**

**Arguments:**
- `session_id`, `target_id`, `origin` (required)
- `from_profile` (string, optional) — Restore from different profile's snapshot

**Returns:** Success message

**Example:**

```javascript
const sessionId = await open_session({ profile: "agent-work" });
const [tab] = await list_tabs(sessionId);

await navigate(sessionId, tab.target_id, "https://jira.mycompany.com");
await restore_snapshot(sessionId, tab.target_id, origin: "https://jira.mycompany.com");

// Now authenticated, can access all Jira content
const content = await get_content(sessionId, tab.target_id);
```

---

### `list_snapshots(profile?, all?)`

**List saved snapshots.**

**Arguments:**
- `profile` (string, optional) — Filter by profile name
- `all` (boolean, optional) — Show all versions (default: latest only)

**Returns:** Array of snapshots

```json
[
  { "profile": "agent-work", "origin": "https://jira.mycompany.com", "saved_at": "2026-03-22T10:15:00Z" },
  { "profile": "agent-work", "origin": "https://github.com", "saved_at": "2026-03-22T10:20:00Z" }
]
```

---

### `delete_snapshot(profile, origin, saved_at?)`

**Delete a saved snapshot.**

**Arguments:**
- `profile`, `origin` (required)
- `saved_at` (string, optional) — Delete specific version; omit to delete all versions

**Returns:** Success message

---

### `save_tab_state(session_id)`

**Save all open tabs' URLs and scroll positions.**

**Arguments:**
- `session_id` (required)

**Returns:** State ID

**Examples:**

```javascript
// Open multiple research tabs
const sessionId = await open_session({ profile: "research" });
await new_tab(sessionId, "https://competitor-a.com");
await new_tab(sessionId, "https://competitor-b.com");
await new_tab(sessionId, "https://news-site.com");

// Do research...
await scroll(sessionId, tab1.target_id, x: 0, y: 1000);
// ... more work ...

// Save tab state (URLs + scroll positions)
await save_tab_state(sessionId);
await close_session(sessionId);

// Later: restore the tabs
const sessionId2 = await open_session({ profile: "research" });
await restore_tab_state(sessionId2);
// All tabs re-open with same URLs and scroll positions
```

---

### `restore_tab_state(session_id)`

**Restore previously saved tab state.**

**Arguments:**
- `session_id` (required)

**Returns:** Success message

---

## Session Checkpoints (4 tools) *(v0.6.0+)*

Session checkpoints capture **full tab state** — URLs, scroll positions, and auth state for every tab in the session — and store it in the encrypted DB. Distinct from `save_snapshot` (which is per-origin cookies/localStorage) and `save_tab_state` (which is just URLs without auth).

Use them when you need to pause a multi-tab investigation and pick up exactly where you left off.

**Auto-checkpoints:** The daemon writes `"Autosave · close"` on every `close_session` and `"Autosave · periodic"` every 5 minutes (configurable via `[checkpoints] interval_seconds`). Retention: `[retention] max_snapshot_versions` (default 10).

See [ADVANCED.md § Session Persistence](ADVANCED.md#session-persistence--auto-reattach-v060) for retention tuning and recovery flows.

### `save_session_checkpoint(session_id, name?)`

Snapshot every open tab's URL + scroll + auth into one checkpoint. Returns `checkpoint_id`.

```javascript
const { checkpoint_id } = await save_session_checkpoint(sessionId, "before-deploy-review");
```

### `restore_session_checkpoint(session_id, checkpoint_id)`

Reopen all saved tabs at their stored URLs in the given session.

```javascript
await restore_session_checkpoint(sessionId, "cp_abc123");
```

### `list_session_checkpoints(profile?)`

List checkpoints for a profile. Profile scoping keeps agent and personal checkpoints separate.

### `delete_session_checkpoint(checkpoint_id)`

Remove a specific checkpoint. Auto-checkpoints honor retention but manual ones stick around until you delete them.

---

## Key-Value Store (5 tools)

### `kv_set(namespace, key, value)`

**Store a value in a persistent, namespaced KV store.**

**Arguments:**
- `namespace` (string, required) — Logical grouping (e.g., "pipeline", "config")
- `key` (string, required) — Key name
- `value` (string, required) — Value (JSON-serialize if object)

**Returns:** Success message

**Examples:**

```javascript
// Store simple values
await kv_set("config", "api_key", "sk_test_123");
await kv_set("config", "user_id", "123");

// Store JSON objects
const checkpointData = { status: "scraped", count: 1500, timestamp: new Date().toISOString() };
await kv_set("pipeline", "scrape_checkpoint", JSON.stringify(checkpointData));

// Overwrite existing
await kv_set("config", "user_id", "456");  // Updates from 123 to 456
```

**Use Cases:**
- Multi-agent coordination (Agent A → KV → Agent B)
- Config storage
- Checkpoint data for resumption
- Metrics and counters

**ICP Context:**
- **ICP 2:** Session ID stored for resumption
- **ICP 4:** Data handoff between agents in pipeline

---

### `kv_get(namespace, key)`

**Retrieve a value from KV store.**

**Arguments:**
- `namespace`, `key` (required)

**Returns:** Value (string), or null if not found

**Examples:**

```javascript
// Get simple value
const apiKey = await kv_get("config", "api_key");

// Get and parse JSON
const checkpointJson = await kv_get("pipeline", "scrape_checkpoint");
const checkpoint = JSON.parse(checkpointJson);
console.log(`Scraped ${checkpoint.count} items`);

// Handle missing key
const sessionId = await kv_get("pipeline", "session_id");
if (!sessionId) {
  console.log("No session ID, starting fresh");
}
```

---

### `kv_delete(namespace, key)`

**Delete a key from KV store.**

**Arguments:**
- `namespace`, `key` (required)

**Returns:** Success message

---

### `kv_list(namespace, prefix?, keys_only?)`

**List all keys in a namespace.**

**Arguments:**
- `namespace` (required)
- `prefix` (string, optional) — Filter by key prefix
- `keys_only` (boolean, optional) — Return just keys (not values)

**Returns:** Array of keys, or array of {key, value} objects

**Examples:**

```javascript
// List all keys in namespace
const allKeys = await kv_list("pipeline");

// List keys with prefix
const syncKeys = await kv_list("pipeline", prefix: "sync_");

// Get key-value pairs
const allData = await kv_list("pipeline");  // [{ key: "k1", value: "v1" }, ...]

// Get just keys
const justKeys = await kv_list("pipeline", keys_only: true);  // ["k1", "k2", ...]
```

---

### `kv_clear(namespace)`

**Delete all keys in a namespace.**

**Arguments:**
- `namespace` (required)

**Returns:** Success message

**Warning:** This deletes everything in the namespace. Be careful!

```javascript
// Clear old pipeline data
await kv_clear("old_pipeline");
```

---

## Sealed Secrets (4 tools) *(v0.7.0+)*

A **trust boundary** for credentials. Secrets extracted from pages live in an encrypted sealed table and are injected into subprocesses via stdin — the raw value never passes through the LLM prompt or the audit log. Use this for tokens you don't want a model to see (GitHub PATs, npm tokens, API keys scraped from a dashboard).

See [SECURITY.md § Sealed-Secret Trust Boundary](SECURITY.md#sealed-secret-trust-boundary-v070) for the threat model and scrubbing details.

### `extract_secret(session_id, target_id, expression, name)`

Evaluate JS in a tab and store the result as a named sealed secret. The value never appears in stdout, the tool response, or the audit log.

```javascript
// Read a freshly-generated npm token from the dashboard, seal it
await extract_secret(
  sessionId, tabId,
  `document.querySelector('.token-value').textContent.trim()`,
  "npm_token"
);
// Tool response: { "name": "npm_token", "stored": true } — the value itself is NEVER echoed.
```

### `use_secret(name, command, args)`

Run a subprocess with the sealed value piped to stdin. The value is read from the sealed store, written to the child's stdin, then zeroed in memory.

```bash
# CLI equivalent
pagerunner use-secret npm_token -- gh secret set NPM_TOKEN --repos owner/repo
```

### `list_secrets()`

Names only — values are never returned.

### `delete_secret(name)`

Remove a sealed entry.

**Important:** Sealed secrets are intentionally one-way for the LLM. There is no `get_secret` that returns a raw value. If you need the value in JS, use `use_secret` to pipe it to a helper script.

---

## Network & Console (2 tools) *(v0.3.0+)*

Inspect HTTP requests and JS console output captured during a session. Replaces the fragile `evaluate`-based fetch-monkey-patching pattern — use these instead.

### `get_network_log(session_id, target_id?, filters?)`

Query the session's CDP network ring buffer. Filter by URL glob, method, status, or time window.

```javascript
// Find the XHR that loaded invoices
const hits = await get_network_log(sessionId, tabId, {
  url_glob: "**/api/invoices**",
  method: "GET",
  status_range: [200, 299]
});
// Each hit has { url, method, status, request_headers, response_headers, body_preview, timing }
```

**When to use:** figure out which API endpoint the site UI actually calls, inspect auth headers before registering a site adapter, debug failed requests.

### `get_console_log(session_id, target_id, since?)`

Recent `console.*` messages and uncaught exceptions. Useful for catching JS errors without opening DevTools.

```javascript
const log = await get_console_log(sessionId, tabId, { since: "2s" });
// [{ level: "error", text: "TypeError: ...", source: "https://...", line: 42 }]
```

**Pattern:** Call this after any interaction that should not emit a JS error; treat any `level: "error"` as a hard fail.

---

## Site Intelligence (4 tools) *(v0.5.0+)*

Pagerunner **learns about sites as you use them**. Adapters are short JS functions executed in the browser tab — same origin as the logged-in user, so they inherit all cookies and tokens. The site knowledge store also remembers auth tokens seen in network traffic (in an encrypted vault) and tracks selector health over time.

Seed adapters for **GitHub, Linear, Jira, Notion, and Gmail** are built in — call them without registering anything.

### `get_site_knowledge(origin)`

Return what Pagerunner knows about a site: registered adapters, detected auth tokens (names + detection metadata, never raw values), selector health stats.

```javascript
const k = await get_site_knowledge("https://github.com");
// { adapters: [...], auth_tokens: [{name: "github_pat", detected_in: "Authorization header"}], selectors: [...] }
```

### `register_adapter(origin, name, description, js_code)`

Store a JS adapter. The function is executed inside the tab when called — it has access to the site's session, cookies, and any detected auth tokens via a `credentials` argument.

```javascript
await register_adapter(
  "https://api.github.com",
  "list-issues",
  "List open issues for a repo",
  `async ({ owner, repo }, { credentials }) => {
     const r = await fetch(\`/repos/\${owner}/\${repo}/issues\`, {
       headers: { Authorization: 'Bearer ' + credentials.github_pat }
     });
     return r.json();
   }`
);
```

### `call_site_api(session_id, target_id, origin, name, params)`

Execute a registered adapter.

```javascript
const issues = await call_site_api(sessionId, tabId, "https://github.com", "list-issues", {
  owner: "Enreign", repo: "pagerunner"
});
```

### `generate_adapter(origin, goal)` *(requires `ANTHROPIC_API_KEY`)*

Auto-generate a JS adapter from captured network traffic using the Claude API. Pagerunner passes recent network log entries + a natural-language goal to the model and stores the resulting adapter.

```javascript
await generate_adapter("https://linear.app", "create an issue given title + description");
```

**Why adapters beat DOM automation:** they're faster, less brittle (no selectors), and reuse browser credentials. Use them for bulk / repeatable operations; use `click`/`fill` for one-off UI tasks.

**Selector fragility warnings:** `click`, `fill`, and `select` track success/failure per selector. Responses include a warning block when a selector fails > 30% over ≥ 5 uses. Treat that as a cue to switch to an adapter.

---

## Video Recording (7 tools) *(v0.8.0+)*

Record tabs as polished MP4 with auto-zoom, cursor tracking, markers, and Screen Studio-quality rendering. Requires `ffmpeg` on PATH (ImageMagick for text overlays).

**Tools at a glance:**

| Tool | Purpose |
|---|---|
| `start_recording(session_id, target_id, name?)` | Begin capture on a tab |
| `stop_recording(session_id)` | End the active recording, returns `recording_id` |
| `add_marker(session_id, label, note?)` | Timestamped annotation (burned into overlays + SRT) |
| `list_recordings(profile?)` | List saved recordings |
| `get_recording(recording_id)` | Metadata: duration, markers, events, file paths |
| `delete_recording(recording_id)` | Remove a recording and its files |
| `render_recording(recording_id, options?)` | Post-process: overlays, zoom, motion interpolation, window chrome |

**This is a doc-lite summary.** The real value of recording lies in *how* you structure the session and *how* you render it. For a full walkthrough — cursor choreography, marker scripts, zoom targeting, auto-record mode, SRT subtitles, and examples for the three common use cases (bug repros, feature demos, onboarding tutorials) — see **[RECORDING.md](RECORDING.md)**.

---

## Notifications (1 tool)

### `notify(title, message, session_id?)` *(macOS menu bar)*

Send a macOS notification through the Pagerunner menu bar app. Requires the menu bar companion running (`apps/menubar`). No-op on Linux/Windows.

```javascript
await notify("Deployment green", "All Jira tickets for sprint-42 closed.");
```

**When to use:** long-running agent jobs where you want a passive signal ("done", "needs attention") without dumping to the Claude transcript.

---

## Quick Reference Table

| Tool | Use Case | ICP |
|------|----------|-----|
| `open_session` | Start Chrome | All |
| `close_session` | Stop Chrome | All |
| `list_sessions` | See active sessions | 4 |
| `list_tabs` | Get tab IDs | All |
| `new_tab` | Open tab | All |
| `navigate` | Go to URL | All |
| `wait_for` | Wait for condition | All |
| `get_content` | Read page | All |
| `screenshot` | Capture viewport | All |
| `evaluate` | Run JS | All |
| `click` | Click element | All |
| `type_text` | Type (plain HTML) | 1, 2 |
| `fill` | Type (React/Vue) | 1, 2, 3 |
| `select` | Pick dropdown | All |
| `scroll` | Scroll page | All |
| `save_snapshot` | Save auth state | 2, 3, 4 |
| `restore_snapshot` | Restore auth | 2, 3, 4 |
| `list_snapshots` | List saved | 2, 3, 4 |
| `delete_snapshot` | Delete saved | 2, 3, 4 |
| `save_tab_state` | Save tab URLs | 1, 4 |
| `restore_tab_state` | Restore tabs | 1, 4 |
| `kv_set` | Store value | 2, 4 |
| `kv_get` | Get value | 2, 4 |
| `kv_delete` | Delete key | 2, 4 |
| `kv_list` | List keys | 4 |
| `kv_clear` | Clear namespace | 4 |
| `attach_session` | Attach to existing Chrome | 4 |
| `close_tab` | Close one tab | All |
| `save_session_checkpoint` | Full tab-state snapshot | 2, 4 |
| `restore_session_checkpoint` | Reopen all tabs at URLs | 2, 4 |
| `extract_secret` | Seal a credential | 3 |
| `use_secret` | Pipe sealed value to subprocess | 3, 4 |
| `get_network_log` | Inspect HTTP traffic | All |
| `get_console_log` | Inspect JS console | All |
| `get_site_knowledge` | What do we know about this site? | 2, 4 |
| `register_adapter` | Store a direct-API function | 2, 4 |
| `call_site_api` | Call a stored adapter | 2, 4 |
| `generate_adapter` | Auto-generate adapter via Claude | 2, 4 |
| `start_recording` | Begin video capture | All |
| `stop_recording` | End video capture | All |
| `add_marker` | Timestamped note in video | All |
| `render_recording` | Post-process to polished MP4 | All |
| `notify` | macOS notification | 2 |

See [RECORDING.md](RECORDING.md) for recording how-to and [ADVANCED.md](ADVANCED.md) for checkpoint/daemon internals.

---

## Metadata Hints

Pagerunner wraps each tool response with semantic metadata to prevent hallucinations:

```json
{
  "content": [
    { "type": "text", "text": "...actual response..." },
    { "type": "text", "text": "{...metadata...}" }
  ]
}
```

**Read the metadata block.** It tells you:
- `_tool`: Which tool returned this
- `_result_type`: Is the result an array (bad), object (good), or primitive?
- `_warning`: Array results get a warning
- `_condition_met`: For wait_for, did the condition actually meet?
- `_schema`: For list_* tools, describes the returned structure

**Example metadata for evaluate:**
```json
{
  "_tool": "evaluate",
  "_result_type": "array",
  "_warning": "Result is an array — field-order ambiguous. Use { field: value } instead."
}
```

See HALLUCINATION_PREVENTION.md for details.
