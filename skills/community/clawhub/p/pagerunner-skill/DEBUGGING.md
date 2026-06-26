# Debugging: Troubleshooting Common Issues

How to diagnose and fix Pagerunner problems.

---

## "Selector not found" After Navigation

### Symptom
```
Error: Selector ".load-more-btn" not found
```

### Root Cause
React/Vue/Angular apps render asynchronously. The selector doesn't exist immediately after `navigate()`.

### Fix

**Always use `wait_for` with a selector before interacting:**

```javascript
// ❌ WRONG
await navigate(sessionId, tabId, "https://app.example.com");
await click(sessionId, tabId, ".button");  // Error: selector not found

// ✅ RIGHT
await navigate(sessionId, tabId, "https://app.example.com");
await wait_for(sessionId, tabId, selector: ".button", ms: 5000);
await click(sessionId, tabId, ".button");  // Now safe
```

### Diagnosis

If you're not sure what selector to wait for:

```javascript
// Get content to see page structure
const content = await get_content(sessionId, tabId);
console.log(content);

// Find a unique element that appears when page is ready
// Then wait for that selector
```

---

## "fill() Didn't Update the Input" or "Value Not Changed"

### Symptom
Form field doesn't update after `fill()`, or the value reverts immediately.

### Root Cause
You used `type_text()` on a React/Vue/Angular controlled input. Framework inputs require synthetic events.

### Fix

**Use `fill()` for modern frameworks, `type_text()` for plain HTML:**

```javascript
// ❌ WRONG — type_text on React input
await type_text(sessionId, tabId, "user@example.com", selector: "input[name='email']");
// React doesn't see the change → input reverts

// ✅ RIGHT — fill() triggers synthetic events
await fill(sessionId, tabId, "input[name='email']", "user@example.com");
// React's onChange handler fires → value updates
```

### How to Detect

```javascript
// Check if input is a React/Vue/Angular component
const isControlled = await evaluate(sessionId, tabId, `
  document.querySelector('input[name="email"]').__reactInternalInstance !== undefined  // React
`);

// If true → use fill(), not type_text()
```

---

## "Screenshot is Blank" or "All White"

### Symptom
Screenshot returns a white or empty image when it should show content.

### Root Cause
Element was off-screen or not visible in the viewport.

### Fix

**Scroll the element into view before screenshot:**

```javascript
// ❌ WRONG — element may be off-screen
await screenshot(sessionId, tabId);

// ✅ RIGHT — scroll element into viewport
await scroll(sessionId, tabId, selector: ".target-element");
await screenshot(sessionId, tabId);

// Or scroll to top first
await evaluate(sessionId, tabId, "window.scrollTo(0, 0)");
await screenshot(sessionId, tabId);
```

### Diagnosis

Check if element exists and is visible:

```javascript
const isVisible = await evaluate(sessionId, tabId, `
  {
    exists: !!document.querySelector('.target-element'),
    visible: document.querySelector('.target-element')?.offsetHeight > 0,
    inViewport: (() => {
      const rect = document.querySelector('.target-element').getBoundingClientRect();
      return rect.top >= 0 && rect.bottom <= window.innerHeight;
    })()
  }
`);
```

---

## "wait_for Timed Out"

### Symptom
```
Error: Timeout waiting for condition after 5000ms
```

### Root Cause
Either the selector never appears, or the timeout is too short.

### Fix Options

**1. Increase timeout:**

```javascript
// Longer timeout
await wait_for(sessionId, tabId, selector: ".slow-element", ms: 10000);
```

**2. Verify selector exists at all:**

```javascript
const content = await get_content(sessionId, tabId);
if (content.includes("slow-element")) {
  console.log("Element text exists, but CSS selector might be wrong");
}

// Try a different selector
await wait_for(sessionId, tabId, selector: ".different-selector", ms: 5000);
```

**3. Use URL pattern instead:**

```javascript
// If waiting for page redirect
await wait_for(sessionId, tabId, url: "**/success", ms: 5000);
```

### Diagnosis

Check page state:

```javascript
const currentState = await evaluate(sessionId, tabId, `
  ({
    url: window.location.href,
    title: document.title,
    selectors: [
      '.expected-selector',
      '.another-option'
    ].map(sel => ({ selector: sel, found: !!document.querySelector(sel) }))
  })
`);
```

---

## "Snapshot Failed to Restore"

### Symptom
```
Error: Failed to restore snapshot for origin
```

### Root Cause
Snapshot doesn't exist, or origin URL doesn't match.

### Fix

**1. Verify snapshot exists:**

```javascript
const snapshots = await list_snapshots();
console.log(snapshots);  // Check if your origin is there

// If missing, create one first
await save_snapshot(sessionId, tabId, origin: "https://jira.mycompany.com");
```

**2. Verify origin matches exactly:**

```javascript
// ❌ WRONG — origin mismatch
await restore_snapshot(sessionId, tabId, origin: "https://jira.mycompany.com");  // saved
await restore_snapshot(sessionId2, tabId2, origin: "https://jira.mycompany.com/");  // trailing slash

// ✅ RIGHT — exact match
const savedOrigin = "https://jira.mycompany.com";
await save_snapshot(sessionId, tabId, origin: savedOrigin);
await restore_snapshot(sessionId2, tabId2, origin: savedOrigin);
```

**3. Check if session still has auth:**

If the restore worked but page is now logged out:
- Snapshot is from before TOTP auth was complete
- Log in manually again, then re-snapshot after passing TOTP

---

## "Allowed Domains Blocking Valid Domain"

### Symptom
```
Error: Domain not in allowed list: example.com
```

### Root Cause
Domain doesn't match the allowlist pattern.

### Fix

**1. Check exact domain:**

```javascript
// Current allowed
allowed_domains: ["jira.mycompany.com", "github.com"]

// ❌ WRONG — www prefix not in list
await navigate(sessionId, tabId, "https://www.github.com");  // Blocked!

// ✅ RIGHT — exact match
await navigate(sessionId, tabId, "https://github.com");
```

**2. Use wildcards for subdomains:**

```javascript
// ✅ Allows all subdomains
allowed_domains: ["*.mycompany.com", "github.com"]

// Now both work:
await navigate(sessionId, tabId, "https://jira.mycompany.com");
await navigate(sessionId, tabId, "https://wiki.mycompany.com");
```

**3. Update allowed_domains dynamically:**

```javascript
// Can't change mid-session, but can open new session
await close_session(sessionId);

const sessionId2 = await open_session({
  profile: "agent",
  allowed_domains: ["jira.mycompany.com", "new-domain.com"]  // Added new domain
});
```

---

## "evaluate() Returns Array With Warning"

### Symptom
Metadata shows `_warning: "Result is an array..."`

### Root Cause
Your evaluate() is returning `[a, b, c]` instead of `{ a, b, c }`.

### Fix

**Refactor to return labeled object:**

```javascript
// ❌ WRONG
const result = await evaluate(sessionId, tabId, `
  [
    document.querySelectorAll('.item').length,
    document.querySelectorAll('.empty').length
  ]
`);
// Returns: [25, 3]
// Metadata warns: "array"

// ✅ RIGHT
const result = await evaluate(sessionId, tabId, `
  ({
    itemCount: document.querySelectorAll('.item').length,
    emptyCount: document.querySelectorAll('.empty').length
  })
`);
// Returns: { itemCount: 25, emptyCount: 3 }
// No warning
```

**Then re-run and verify:**

```javascript
const result = await evaluate(...);  // Refactored version
console.log(result);  // Should show: { itemCount: ..., emptyCount: ... }
```

See HALLUCINATION_PREVENTION.md for details.

---

## "PII Not Being Anonymized"

### Symptom
Email addresses, names, etc. still visible in `get_content` results.

### Root Cause
Anonymization not enabled, or running without `anonymize: true`.

### Fix

**Enable anonymization:**

```javascript
// ❌ WRONG — not anonymized
const sessionId = await open_session({ profile: "sensitive" });

// ✅ RIGHT
const sessionId = await open_session({
  profile: "sensitive",
  anonymize: true,
  anonymization_mode: "tokenize"
});
```

**Verify it's working:**

```javascript
const content = await get_content(sessionId, tabId);

// Should see tokens like [EMAIL:abc123], [PERSON:xyz789]
// Not raw email addresses or names
console.log(content);

if (content.includes("@")) {
  console.error("Anonymization failed — email still visible!");
}
```

**Check metadata:**

```javascript
// After get_content, check metadata for pii_entities
// Should show: { EMAIL: 3, PERSON: 2 }
// This proves anonymization detected and stripped PII
```

---

## "Form Submission Worked But Page Didn't Redirect"

### Symptom
Form click succeeded, but page didn't navigate.

### Root Cause
Form submission is async. Page update happens after the click.

### Fix

**Wait for page change after form submission:**

```javascript
// ❌ WRONG
await click(sessionId, tabId, ".submit-btn");
await get_content(sessionId, tabId);  // Still on form page

// ✅ RIGHT
await click(sessionId, tabId, ".submit-btn");
await wait_for(sessionId, tabId, selector: ".success-message", ms: 5000);
await get_content(sessionId, tabId);  // Now on success page
```

---

## "KV Store Value Lost"

### Symptom
```
kv_get returns null, but I just set the value
```

### Root Cause
Different namespace, or value was never set.

### Fix

**Check namespace:**

```javascript
// ❌ WRONG — different namespaces
await kv_set("pipeline", "data", JSON.stringify({...}));
const value = await kv_get("config", "data");  // Different namespace!

// ✅ RIGHT — same namespace
await kv_set("pipeline", "data", JSON.stringify({...}));
const value = await kv_get("pipeline", "data");
```

**List keys to verify:**

```javascript
const allKeys = await kv_list("pipeline");
console.log(allKeys);  // Should include "data"
```

**Check value is JSON-serializable:**

```javascript
// ❌ WRONG — functions can't be serialized
const value = { fn: () => {} };
await kv_set("pipeline", "data", JSON.stringify(value));  // Fails

// ✅ RIGHT — only JSON-compatible types
const value = { timestamp: new Date().toISOString(), count: 5 };
await kv_set("pipeline", "data", JSON.stringify(value));
```

---

## "Stealth Mode Not Working" (Still Detected)

### Symptom
Cloudflare, reCAPTCHA, or other anti-bot still detects automation.

### Root Cause
Stealth mode hides basic signals but isn't foolproof. Some sites have advanced detection.

### Fix Options

**1. Try a different timing:**

```javascript
// Add delays between actions
await click(sessionId, tabId, ".button");
await wait_for(sessionId, tabId, ms: 1000);  // Human-like delay
await type_text(sessionId, tabId, "text");
```

**2. Check if site blocks CDP:**

```javascript
// Some sites specifically block Chrome DevTools Protocol
// No configuration can bypass that
// Consider using agent-browser's headless mode instead
```

**3. Verify stealth is enabled:**

```javascript
const sessions = await list_sessions();
const mySession = sessions.find(s => s.id === sessionId);
console.log(mySession.stealth);  // Should be true
```

---

## "Credential Extraction Failed"

### Symptom
`get_content` or `evaluate` can't find login credentials, email, etc.

### Root Cause
Input fields are empty, or selectors don't match the page structure.

### Fix

**Inspect page structure:**

```javascript
const structure = await get_content(sessionId, tabId);
console.log(structure);  // See what's visible

// If no email visible, page might not have loaded
await wait_for(sessionId, tabId, selector: "input[name='email']", ms: 5000);
```

**Try different selectors:**

```javascript
// ❌ WRONG — selector too specific
const email = await evaluate(sessionId, tabId, `
  document.querySelector('.email-input-form-v2-2026').value
`);

// ✅ RIGHT — more generic
const email = await evaluate(sessionId, tabId, `
  document.querySelector('input[type="email"]').value
`);
```

---

## When to Check Audit Log

Enable audit logging to debug security events:

```bash
# View audit log
tail -f ~/.pagerunner/audit.log | jq .

# Filter by session
cat ~/.pagerunner/audit.log | jq 'select(.session_id == "sess_abc123")'

# Check what PII was encountered
cat ~/.pagerunner/audit.log | jq '.pii_entities | values'
```

---

## General Debugging Checklist

- [ ] Is the session still open? (`list_sessions`)
- [ ] Is the tab still active? (`list_tabs`)
- [ ] Did the page load? (`get_content`)
- [ ] Can I locate the element? (`evaluate` with querySelector check)
- [ ] Is the selector correct? (Try `document.querySelectorAll(".selector").length`)
- [ ] Should I wait for something? (Use `wait_for`)
- [ ] Is anonymization enabled? (Check session flags)
- [ ] Does evaluate() return a labeled object? (Check metadata)
- [ ] Am I using the right tool? (`fill` for React, `type_text` for HTML)
- [ ] Did the action succeed? (Check metadata `_success`)

---

## Getting Help

- **SKILL.md** — Quick start for your ICP
- **PATTERNS.md** — Detailed workflow patterns
- **REFERENCE.md** — All 27 tools with examples
- **SECURITY.md** — Security troubleshooting
- **HALLUCINATION_PREVENTION.md** — Metadata and result clarity

Still stuck? Check the main pagerunner repo: https://github.com/Enreign/pagerunner
