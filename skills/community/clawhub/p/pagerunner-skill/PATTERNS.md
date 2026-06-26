# 11 Workflow Patterns

Master these patterns and you can build any Pagerunner workflow.

---

## Pattern 1: Session Management & Multi-Tab Workflows

**What:** Open a session, manage multiple tabs, coordinate them, close cleanly.

**When:** Every workflow starts here. Understand sessions + tabs before doing anything else.

**Key Concepts:**
- One session = one Chrome instance
- Multiple profiles = multiple sessions (each isolated)
- Multiple tabs = same session, shared cookies
- Use tabs for parallel reads (research), session separation for isolation

**Implementation:**

```javascript
// Open a session
const sessionId = await open_session({ profile: "research" });

try {
  // List existing tabs — always do this to get target_id
  const tabs = await list_tabs(sessionId);
  console.log(`Session has ${tabs.length} tabs`);

  // Open new tabs in parallel
  const tab1 = await new_tab(sessionId, "https://competitor-a.com");
  const tab2 = await new_tab(sessionId, "https://competitor-b.com");

  // All share same auth cookies — logged in once
  // Read all tabs in parallel
  const results = await Promise.all([
    get_content(sessionId, tab1.target_id),
    get_content(sessionId, tab2.target_id)
  ]);
} finally {
  // Always close — even if something throws above
  // Also writes an auto-checkpoint (v0.6.0+)
  await close_session(sessionId);
}
```

**ICP-Specific Context:**

- **ICP 1 (Developer):** One session, multiple tabs for related research (docs, tests, tickets). Fast context switching without re-auth.
- **ICP 2 (Power User):** Separate agent profile session, never mixed with human profile. Session ID persisted in KV store for resumption.
- **ICP 3 (Security):** One session per domain to minimize PII leakage scope. `allowed_domains` contains which tabs can navigate where.
- **ICP 4 (Server-Side):** Daemon handles session lifecycle. Reuse `session_id` from KV store across task runs.

**Common Mistakes:**

- ❌ Opening a new session for each action (wasteful, loses auth)
- ❌ Assuming cookies transfer between sessions (they don't — each session is isolated)
- ❌ Mixing human and agent profiles in the same session (security risk for ICP 2)

**Learn More:** SKILL.md → "Solo Developer" quick start

---

## Pattern 2: Form Filling with React/Vue/Angular

**What:** Fill forms correctly on modern JavaScript frameworks using synthetic events.

**Why:** Plain `type_text` doesn't trigger React/Vue change handlers. `fill()` uses CDP synthetic events that frameworks respect.

**Key Difference:**
- **`fill()`** — clears field, types text, fires change events (use for React/Vue/Angular)
- **`type_text()`** — just types without clearing (use for plain HTML, append mode)

**Implementation:**

```javascript
// Navigate to form
await navigate(sessionId, tabId, "https://app.example.com/form");
await wait_for(sessionId, tabId, selector: ".submit-btn", ms: 5000);

// Fill fields using fill() for framework apps
await fill(sessionId, tabId, "input[name='email']", "user@example.com");
await fill(sessionId, tabId, "input[name='password']", "secret123");

// Click checkbox
await click(sessionId, tabId, "input[type='checkbox']");

// Click submit
await click(sessionId, tabId, ".submit-btn");

// Wait for post-submit action (page load, modal, etc.)
await wait_for(sessionId, tabId, selector: ".success-message", ms: 5000);

// Verify the result
const resultContent = await get_content(sessionId, tabId);
console.log(resultContent);
```

**With Anonymization (ICP 3):**

```javascript
// When `anonymize: true`, fill() works transparently with tokens
const sessionId = await open_session({
  profile: "sensitive",
  anonymize: true,
  anonymization_mode: "tokenize"
});

// Agent gets: "[EMAIL:abc123]" instead of real email
const email = await get_content(sessionId, tabId);  // "[EMAIL:abc123]"

// Pass token directly to fill() → Pagerunner de-tokenizes automatically
await fill(sessionId, tabId, "input[name='reply-to']", "[EMAIL:abc123]");
// DOM receives the real email address, never exposed to agent
```

**Common Mistakes:**

- ❌ Using `type_text()` on React controlled inputs (won't trigger change handlers)
- ❌ Not waiting for the form to load before filling (selector timing)
- ❌ Filling without error recovery (if validation fails, agent doesn't retry)

**ICP Context:** ICP 1 uses this for frontend testing. ICP 3 uses with tokenization for PII workflows.

**Learn More:** SKILL.md → "Core Workflow: Form Filling with Error Recovery"

---

## Pattern 3: Content Extraction (get_content & evaluate)

**What:** Read page content, extract structured data, and evaluate JavaScript in the page context.

**When:** You need information from the page — text, state, computed values.

**Key Strategy:**
1. `get_content()` → read page structure (HTML as text)
2. `evaluate()` → run JavaScript to extract specific values
3. Never mix ("read HTML string and parse in your head")

**Implementation:**

```javascript
// First: get the page structure
const pageText = await get_content(sessionId, tabId);
// Returns visible text, cleaned for readability

// Identify what you need to extract
// Example: extracting metrics from a dashboard

// Second: use evaluate() for structured extraction
const metrics = await evaluate(sessionId, tabId, `
  ({
    totalUsers: document.querySelectorAll('.user-card').length,
    activeToday: parseInt(document.querySelector('[data-metric="active"]').textContent),
    avgSessionTime: parseFloat(document.querySelector('[data-metric="session-time"]').textContent),
    lastUpdated: document.querySelector('[data-last-updated]').getAttribute('data-last-updated')
  })
`);

// Always return labeled objects, never arrays
console.log(metrics);
// { totalUsers: 42, activeToday: 28, avgSessionTime: 5.3, lastUpdated: "2026-03-22T14:00Z" }
```

**Common Mistakes:**

- ❌ Returning arrays from evaluate: `[42, 28, 5.3]` → Claude guesses wrong meaning
- ✅ Always return labeled objects: `{ totalUsers: 42, activeToday: 28, avgSessionTime: 5.3 }`

- ❌ Using evaluate() to read static HTML (use get_content instead)
- ✅ Use evaluate() for dynamic values, computed properties, page state

**Hallucination Prevention:**

Pagerunner metadata warns if evaluate returns an array:
```json
{
  "_result_type": "array",
  "_warning": "Result is an array — always return labeled objects { field: value }"
}
```

Read the metadata block every time.

**ICP Context:** All ICPs use this. ICP 1 extracts test results. ICP 3 uses with anonymization (PII stripped).

**Learn More:** HALLUCINATION_PREVENTION.md → "The Incident: 25 likes vs 25 views"

---

## Pattern 4: Authentication Persistence (Snapshots)

**What:** Save authenticated session state once, restore it automatically in future runs.

**Why:** Skip manual login every time. Agent gets pre-authenticated session.

**Implementation:**

```javascript
// FIRST TIME: Log in manually and save the state
const sessionId = await open_session({ profile: "agent-work" });
const [tab] = await list_tabs(sessionId);

// Navigate to login page
await navigate(sessionId, tab.target_id, "https://jira.mycompany.com");

// Agent fills login form
await fill(sessionId, tab.target_id, "input[name='username']", "agent@company.com");
await fill(sessionId, tab.target_id, "input[type='password']", "secret");
await click(sessionId, tab.target_id, ".login-btn");

// Wait for auth to complete (including TOTP if present)
await wait_for(sessionId, tab.target_id, selector: ".dashboard", ms: 10000);

// NOW save the snapshot (after auth is complete)
await save_snapshot(sessionId, tab.target_id, origin: "https://jira.mycompany.com");
await close_session(sessionId);

// FUTURE RUNS: Restore the snapshot, already authenticated
const sessionId2 = await open_session({ profile: "agent-work" });
const [tab2] = await list_tabs(sessionId2);

// Navigate to the app
await navigate(sessionId2, tab2.target_id, "https://jira.mycompany.com");

// Restore the saved credentials
await restore_snapshot(sessionId2, tab2.target_id, origin: "https://jira.mycompany.com");

// Already logged in, no re-auth needed
await navigate(sessionId2, tab2.target_id, "https://jira.mycompany.com/board");
const content = await get_content(sessionId2, tab2.target_id);  // Full access
```

**TOTP Handling:**

Log in manually once (human types TOTP code), snapshot after. The saved cookies include the post-TOTP session. Future restores skip TOTP entirely.

**ICP Context:**

- **ICP 2 (Power User):** Essential. Agent profile snapshots mean no re-auth ever. Mobile WhatsApp → agent logs in pre-authenticated.
- **ICP 3 (Security):** Named snapshots per origin. Each domain gets its own auth checkpoint.
- **ICP 4 (Server-Side):** Snapshots as auth handoff between agents. Agent A logs in, Agent B continues without re-auth.

**Common Mistakes:**

- ❌ Snapshotting during TOTP challenge (code expires in 30s)
- ✅ Snapshot after passing all auth, including TOTP

- ❌ Assuming one snapshot works for multiple origins
- ✅ Save separate snapshots per origin (Jira, GitHub, Salesforce all different)

**Learn More:** SKILL.md → "Power User" quick start

---

## Pattern 5: Multi-Tab Coordination

**What:** Open multiple tabs, read/extract from one, act on another, coordinate results.

**When:** Research + action workflows (read competitor site, then update your own).

**Implementation:**

```javascript
const sessionId = await open_session({ profile: "research" });

// Open research tab
const researchTab = await new_tab(sessionId, "https://competitor.com/pricing");
await wait_for(sessionId, researchTab.target_id, selector: ".pricing-table", ms: 5000);

// Open your site (same session, same auth)
const yourSiteTab = await new_tab(sessionId, "https://yoursite.com/admin/pricing");
await wait_for(sessionId, yourSiteTab.target_id, selector: ".edit-price-btn", ms: 5000);

// Extract competitor pricing
const competitorPricing = await evaluate(sessionId, researchTab.target_id, `
  Array.from(document.querySelectorAll('.pricing-row')).map(row => ({
    tier: row.querySelector('.tier-name').textContent,
    price: parseFloat(row.querySelector('.price').textContent.replace('$', ''))
  }))
`);

// Update your pricing based on competitor
for (const tier of competitorPricing) {
  await fill(sessionId, yourSiteTab.target_id, `input[data-tier="${tier.tier}"]`, tier.price.toString());
}

// Save changes
await click(sessionId, yourSiteTab.target_id, ".save-btn");
await wait_for(sessionId, yourSiteTab.target_id, selector: ".success-message", ms: 5000);

await close_session(sessionId);
```

**Common Mistakes:**

- ❌ Assuming tabs are independent (they share session auth)
- ✅ Leverage shared auth for multi-domain workflows

- ❌ Operating on tabs in parallel without coordination (race conditions)
- ✅ Sequence operations carefully when they depend on each other

**ICP Context:** ICP 1 uses for research-then-code workflows. ICP 4 uses for data pipelines.

---

## Pattern 6: Error Recovery & Retries

**What:** Handle validation errors, network timeouts, and page state changes gracefully.

**When:** Real-world workflows fail. Agents need to recover.

**Implementation:**

```javascript
const maxRetries = 3;
let attempt = 0;

while (attempt < maxRetries) {
  try {
    // Attempt the action
    await fill(sessionId, tabId, "input[name='email']", email);
    await fill(sessionId, tabId, "input[name='password']", password);
    await click(sessionId, tabId, ".login-btn");

    // Wait for success or error
    await wait_for(sessionId, tabId,
      selector: ".success-message, .error-message",
      ms: 5000
    );

    // Check result
    const result = await get_content(sessionId, tabId);

    if (result.includes("success")) {
      console.log("Login successful");
      break;
    } else if (result.includes("Invalid email")) {
      console.log("Email invalid, aborting");
      throw new Error("Invalid email, retry won't help");
    } else if (result.includes("Too many attempts")) {
      console.log("Rate limited, waiting before retry");
      await wait_for(sessionId, tabId, ms: 5000);  // Fixed delay
      attempt++;
      continue;
    }

  } catch (error) {
    attempt++;
    if (attempt >= maxRetries) {
      throw new Error(`Failed after ${maxRetries} attempts: ${error.message}`);
    }
    console.log(`Attempt ${attempt} failed, retrying...`);
    // Optionally refresh the page
    await navigate(sessionId, tabId, await evaluate(sessionId, tabId, "window.location.href"));
  }
}
```

**ICP Context:** All ICPs need this for reliability. ICP 4 especially (server-side automation needs robustness).

---

## Pattern 7: Scrolling & Viewport Management

**What:** Navigate the page viewport, scroll to load content, handle dynamic "load more" buttons.

**When:** Page content is larger than viewport, or content loads on scroll.

**Implementation:**

```javascript
// Scroll by pixel amount
await scroll(sessionId, tabId, x: 0, y: 500);  // Scroll down 500px

// Scroll to a specific element
await scroll(sessionId, tabId, selector: ".load-more-btn");

// Get full page height and scroll to bottom
const fullHeight = await evaluate(sessionId, tabId, "document.body.scrollHeight");
const screenHeight = await evaluate(sessionId, tabId, "window.innerHeight");

for (let y = 0; y < fullHeight; y += screenHeight) {
  await scroll(sessionId, tabId, x: 0, y: screenHeight);
  await wait_for(sessionId, tabId, ms: 500);  // Let content load
}

// Load more pattern
while (true) {
  const loadMoreBtn = await evaluate(sessionId, tabId, `
    document.querySelector('.load-more-btn') ? document.querySelector('.load-more-btn').textContent : null
  `);

  if (!loadMoreBtn) break;  // No more content

  await scroll(sessionId, tabId, selector: ".load-more-btn");
  await click(sessionId, tabId, ".load-more-btn");
  await wait_for(sessionId, tabId, ms: 2000);  // Wait for new content
}

// Get all content
const allContent = await get_content(sessionId, tabId);
```

**Screenshot & Verify:**

```javascript
// Take screenshot of current viewport
await screenshot(sessionId, tabId);

// To capture full page, scroll to top first
await evaluate(sessionId, tabId, "window.scrollTo(0, 0)");
await screenshot(sessionId, tabId);
```

**Common Mistakes:**

- ❌ Assuming all content is visible without scrolling
- ✅ Always scroll to element before interacting with it

- ❌ Clicking "load more" without waiting for new content
- ✅ Always `wait_for` after clicking buttons that load content

**ICP Context:** ICP 1 uses for fullpage screenshots. ICP 4 uses for scraping infinite-scroll lists.

---

## Pattern 8: JavaScript Evaluation

**What:** Run JavaScript in the page context to extract state, trigger events, or inspect the DOM.

**When:** You need more than what `get_content` provides, or you need to interact with page state.

**Implementation:**

```javascript
// Simple value extraction
const title = await evaluate(sessionId, tabId, "document.title");

// DOM inspection
const elementCount = await evaluate(sessionId, tabId, `
  document.querySelectorAll('[data-testid="item"]').length
`);

// React component state (if you have access to React DevTools props)
const isLoading = await evaluate(sessionId, tabId, `
  window.__REACT_DEVTOOLS_GLOBAL_HOOK__.getFiber(
    document.querySelector('[data-component="Main"]')
  ).memoizedState.isLoading
`);

// Trigger events
await evaluate(sessionId, tabId, `
  document.querySelector('input[type="text"]').focus();
  document.querySelector('input[type="text"]').dispatchEvent(new Event('input', { bubbles: true }));
`);

// Read page metadata
const meta = await evaluate(sessionId, tabId, `
  ({
    url: window.location.href,
    title: document.title,
    lang: document.documentElement.lang,
    description: document.querySelector('meta[name="description"]')?.content
  })
`);
```

**Return Value Expectations:**

```javascript
// ✅ These work fine
evaluate(..., "1 + 1")                           // Returns: 2
evaluate(..., "document.title")                  // Returns: "Page Title"
evaluate(..., "{ name: 'John', age: 30 }")      // Returns: { name: 'John', age: 30 }
evaluate(..., "[1, 2, 3]")                       // Returns: [1, 2, 3] (okay for primitive arrays)

// ❌ Array of objects — ambiguous fields
evaluate(..., `
  Array.from(document.querySelectorAll('.item')).map(el => [
    el.querySelector('.name').textContent,
    el.querySelector('.price').textContent
  ])
`)
// Returns: [["Item A", "$10"], ["Item B", "$20"]]
// Claude has to guess: is it [name, price] or [id, quantity]?

// ✅ Labeled object — unambiguous
evaluate(..., `
  Array.from(document.querySelectorAll('.item')).map(el => ({
    name: el.querySelector('.name').textContent,
    price: el.querySelector('.price').textContent
  }))
`)
// Returns: [{ name: "Item A", price: "$10" }, { name: "Item B", price: "$20" }]
// Clear and unambiguous
```

**Common Mistakes:**

- ❌ Returning arrays of arrays
- ✅ Return labeled objects or primitive values only

- ❌ Assuming evaluate has access to page's JavaScript modules/globals
- ✅ Evaluate runs in the page context but has limits (some bundled code unavailable)

**ICP Context:** All ICPs use this. ICP 1 inspects React state. ICP 3 extracts structured data with anonymization.

**Learn More:** HALLUCINATION_PREVENTION.md

---

## Pattern 9: Selector Strategy & Stability

**What:** Choose selectors that survive page updates, DOM re-renders, and dynamic changes.

**When:** Building robust workflows on real-world pages with dynamic content.

**Selector Hierarchy (Most to Least Stable):**

```javascript
// 1. Data attributes (most stable)
await click(sessionId, tabId, "[data-testid='submit-btn']");
await click(sessionId, tabId, "[data-qa='user-card']");

// 2. Semantic HTML (stable)
await click(sessionId, tabId, "button[aria-label='Save']");
await fill(sessionId, tabId, "input[type='email']", "...");

// 3. Class names (risky for React/generated classes)
await click(sessionId, tabId, ".btn-primary");  // May break if classes regenerate

// 4. IDs (stable but rare)
await click(sessionId, tabId, "#save-button");

// 5. Text content (fragile, breaks with localization)
await click(sessionId, tabId, "button:has-text('Save')");
```

**Testing Selector Stability:**

```javascript
// Take snapshot before and after page update
const snapshot1 = await evaluate(sessionId, tabId, `
  document.querySelectorAll('.item').length
`);

// Trigger an update
await click(sessionId, tabId, ".refresh-btn");
await wait_for(sessionId, tabId, ms: 1000);

const snapshot2 = await evaluate(sessionId, tabId, `
  document.querySelectorAll('.item').length
`);

// If both match, selector is stable
if (snapshot1 === snapshot2) {
  console.log("Selector is stable across update");
}
```

**ICP Context:** ICP 1 builds selectors for their own app (data attributes available). ICP 4 builds selectors for third-party sites (less control, need more defensive strategies).

---

## Pattern 10: Stealth Mode & Security

**What:** Mask automation signals and implement domain restrictions to prevent detection and contain scope.

**When:** Visiting sites that detect automation, or running agent on untrusted domains.

**Implementation:**

```javascript
// Enable stealth mode (hides automation signals)
const sessionId = await open_session({
  profile: "agent",
  stealth: true,  // Masks navigator.webdriver, adds human-like delays
  allowed_domains: ["jira.mycompany.com", "github.com", "slack.com"]
});

// Stealth mode benefits:
// - Hides navigator.webdriver = true
// - Adds delays between actions (human-like)
// - Masks CDP signatures

// Domain allowlisting enforcement:
await navigate(sessionId, tabId, "https://jira.mycompany.com");  // ✓ OK
await navigate(sessionId, tabId, "https://github.com");           // ✓ OK
await navigate(sessionId, tabId, "https://personal-banking.com"); // ✗ Error

// With anonymization (ICP 3):
const sessionId2 = await open_session({
  profile: "agent-secure",
  anonymize: true,
  allowed_domains: ["jira.mycompany.com"]
});
```

**Common Scenarios:**

```javascript
// Booking flights (Skyscanner, Kayak) → use stealth
const sessionId = await open_session({
  profile: "agent-travel",
  stealth: true,
  allowed_domains: ["skyscanner.com", "kayak.com"]
});

// Sensitive workflows (HR, finance) → use anonymize
const sessionId = await open_session({
  profile: "agent-hr",
  anonymize: true,
  allowed_domains: ["hr.company.com", "payroll.company.com"]
});

// Both (maximum protection) → stealth + anonymize + allowed-domains
const sessionId = await open_session({
  profile: "agent-max-security",
  stealth: true,
  anonymize: true,
  allowed_domains: ["company.internal"]
});
```

**ICP Context:**

- **ICP 2 (Power User):** Stealth on for flight/hotel booking sites
- **ICP 3 (Security):** Anonymize on for sensitive data workflows
- **ICP 4 (Server-Side):** Allowed-domains for agent containment

**Learn More:** SECURITY.md → "Domain Allowlisting" and "Stealth Mode"

---

## Pattern 11: State Coordination (KV Store & Multi-Agent)

**What:** Use the persistent KV store to coordinate between multiple agents and persist state across runs.

**When:** Multi-agent pipelines, server-side automation, or data handoff between tasks.

**Implementation:**

```javascript
// Agent A: Collects data and saves state
const sessionA = await open_session({ profile: "agent-scraper" });
const tabA = (await list_tabs(sessionA))[0];

// Scrape competitor prices
await navigate(sessionA, tabA.target_id, "https://competitor.com/pricing");
const prices = await evaluate(sessionA, tabA.target_id, `
  Array.from(document.querySelectorAll('.price-item')).map(el => ({
    product: el.querySelector('.product-name').textContent,
    price: parseFloat(el.querySelector('.price').textContent.replace('$', ''))
  }))
`);

// Store in KV for Agent B to access
await kv_set("pipeline", "competitor_prices_2026-03-22", JSON.stringify(prices));
await kv_set("pipeline", "last_scrape_time", new Date().toISOString());

await close_session(sessionA);

// Agent B (later, different session): Retrieves and processes
const sessionB = await open_session({ profile: "agent-analyzer" });

// Fetch data from KV
const pricesJson = await kv_get("pipeline", "competitor_prices_2026-03-22");
const prices = JSON.parse(pricesJson);

// Analyze and update your own pricing
const analysis = prices.map(item => ({
  ...item,
  ourPrice: item.price * 1.1,  // 10% markup
  profit: item.price * 0.1
}));

// Save analysis back to KV
await kv_set("pipeline", "pricing_analysis_2026-03-22", JSON.stringify(analysis));

await close_session(sessionB);

// Agent C: Reports results
const sessionC = await open_session({ profile: "agent-reporter" });
const analysis = JSON.parse(await kv_get("pipeline", "pricing_analysis_2026-03-22"));
// Send summary to Slack, write to database, etc.
```

**Namespacing Strategy:**

```javascript
// Use namespaces to organize state
await kv_set("pricing-pipeline", "competitor_data", ...);
await kv_set("pricing-pipeline", "our_analysis", ...);
await kv_set("pricing-pipeline", "sync_status", ...);

// List all keys in a namespace
const allKeys = await kv_list("pricing-pipeline");

// Filter by prefix
const syncKeys = await kv_list("pricing-pipeline", prefix: "sync");

// Later cleanup
await kv_delete("pricing-pipeline", "competitor_data");
await kv_clear("pricing-pipeline");  // Delete entire namespace
```

**Daemon Setup (ICP 4):**

```bash
# Start once
pagerunner daemon &

# All agents connect automatically
# No DB lock conflicts
# Shared KV state across all sessions
```

**ICP Context:**

- **ICP 2 (Power User):** Agent stores checkpoint in KV, resumes from phone trigger
- **ICP 4 (Server-Side):** Essential for multi-agent pipelines. Agent A → KV → Agent B → KV → Agent C

**Learn More:** ADVANCED.md → "Multi-Agent Coordination via KV Store"

---

## Quick Reference

| Pattern | Use Case | ICP |
|---------|----------|-----|
| 1. Session Management | Open/manage sessions and tabs | All |
| 2. Form Filling | Fill modern framework forms | 1, 3 |
| 3. Content Extraction | Read pages, evaluate JavaScript | All |
| 4. Auth Persistence | Save/restore login state | 2, 4 |
| 5. Multi-Tab Coordination | Research + action workflows | 1, 4 |
| 6. Error Recovery | Handle failures gracefully | 4 |
| 7. Scrolling & Viewport | Load dynamic content | 1, 4 |
| 8. JavaScript Evaluation | Inspect state, trigger events | All |
| 9. Selector Strategy | Choose stable selectors | All |
| 10. Stealth & Security | Hide automation, domain limits | 2, 3 |
| 11. State Coordination | Multi-agent KV pipeline | 2, 4 |
