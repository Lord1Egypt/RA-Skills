# Examples: Full ICP Workflows

Real-world, production-ready examples for each of the 4 ICPs.

---

## ICP 1: Solo Developer — Frontend Dev Loop (Claude Code)

**Goal:** Implement a feature, verify the UI live, iterate without manual browser checking.

### Scenario
You're building a checkout flow. Need to implement a "Save for Later" button that toggles a favorite state. Claude should:
1. Implement the button and handler
2. Open the app in the browser
3. Take a screenshot to verify it renders
4. Evaluate the state to confirm functionality
5. Report back on what to fix next

### Full Workflow

```javascript
// Step 1: Claude opens your dev app
const sessionId = await open_session({ profile: "personal" });
const tabs = await list_tabs(sessionId);
const tabId = tabs[0].target_id;

// Navigate to dev app
await navigate(sessionId, tabId, "http://localhost:3000/checkout");
await wait_for(sessionId, tabId, selector: "[data-testid='save-later-btn']", ms: 5000);

// Step 2: Get page structure to understand what exists
const pageStructure = await get_content(sessionId, tabId);
console.log("Page structure:", pageStructure);
// Output: "Product: Widget | Price: $29.99 | [Save for Later] button"

// Step 3: Take screenshot to verify button appearance
const screenshot1 = await screenshot(sessionId, tabId);
// Claude sees button renders correctly, position looks good

// Step 4: Test the button functionality
// Click the button
await click(sessionId, tabId, "[data-testid='save-later-btn']");

// Wait for state change
await wait_for(sessionId, tabId, ms: 500);

// Step 5: Evaluate button state
const buttonState = await evaluate(sessionId, tabId, `
  ({
    buttonText: document.querySelector('[data-testid="save-later-btn"]').textContent,
    buttonAriaPressed: document.querySelector('[data-testid="save-later-btn"]').getAttribute('aria-pressed'),
    favorite: window.__STORE__.getState().cart.items[0].isFavorite,
    heartIcon: document.querySelector('[data-testid="save-later-btn"] .heart-icon')?.classList.contains('filled')
  })
`);
// Returns:
// {
//   buttonText: "Saved for Later",
//   buttonAriaPressed: "true",
//   favorite: true,
//   heartIcon: true
// }

// Step 6: Report findings
console.log("✓ Save for Later button works:");
console.log(`  - Text changed: ${buttonState.buttonText}`);
console.log(`  - State updated: favorite = ${buttonState.favorite}`);
console.log(`  - Icon filled: ${buttonState.heartIcon}`);

// Step 7: Verify it persists after page reload
await navigate(sessionId, tabId, "http://localhost:3000/checkout");
await wait_for(sessionId, tabId, selector: "[data-testid='save-later-btn']", ms: 5000);

const afterReload = await evaluate(sessionId, tabId, `
  ({ isFavorite: window.__STORE__.getState().cart.items[0].isFavorite })
`);

if (afterReload.isFavorite) {
  console.log("✓ State persisted after reload");
} else {
  console.log("✗ State was lost — check localStorage/Redux persistence");
}

await close_session(sessionId);
```

**Key Patterns:**
- Use your real Chrome profile (already authenticated)
- Screenshot for visual verification
- `evaluate` with labeled objects for state inspection
- Reload to verify persistence

---

## ICP 2: Power User — Mobile WhatsApp Automation (OpenClaw)

**Goal:** Send a task from WhatsApp via OpenClaw, agent completes it autonomously, results back to phone.

### Scenario
You're on a plane. Send WhatsApp message: *"Check my Jira for any blockers on the release"*

OpenClaw triggers Pagerunner skill, agent:
1. Opens Jira in agent profile (pre-authenticated via snapshot)
2. Reads the release board
3. Extracts blocking tickets
4. Summarizes and sends back via WhatsApp

### Full Workflow

```javascript
// This function runs on message from WhatsApp via OpenClaw

async function checkJiraBlockers(taskMessage) {
  // Step 1: Open pre-authenticated agent session
  const sessionId = await open_session({
    profile: "agent-work",  // Separate profile, never mixed with human
    stealth: true,          // Some sites detect automation
    allowed_domains: ["jira.mycompany.com", "github.com"]
  });

  const tabs = await list_tabs(sessionId);
  const tabId = tabs[0].target_id;

  // Step 2: Navigate to Jira board
  await navigate(sessionId, tabId, "https://jira.mycompany.com/board/release-q2");

  // Step 3: Restore pre-saved auth session
  // (Done during setup — agent logged in once, snapshots saved)
  await restore_snapshot(sessionId, tabId, origin: "https://jira.mycompany.com");

  // Step 4: Wait for board to load
  await wait_for(sessionId, tabId, selector: "[data-testid='board-issues']", ms: 5000);

  // Step 5: Get visible page to understand structure
  const boardContent = await get_content(sessionId, tabId);
  console.log("Board loaded:", boardContent.substring(0, 200), "...");

  // Step 6: Extract blocking issues
  const blockers = await evaluate(sessionId, tabId, `
    Array.from(document.querySelectorAll('[data-testid="blocking-issue"]')).map(issue => ({
      key: issue.querySelector('[data-testid="issue-key"]').textContent,
      title: issue.querySelector('[data-testid="issue-title"]').textContent,
      assignee: issue.querySelector('[data-testid="assignee"]')?.textContent || 'Unassigned',
      priority: issue.querySelector('[data-testid="priority"]').getAttribute('data-priority')
    }))
  `);

  // Step 7: Format summary
  const summary = blockers.length === 0
    ? "✓ No blockers! Release is clear."
    : `⚠️ ${blockers.length} blockers found:\n` +
      blockers
        .map(b => `• ${b.key}: ${b.title} (${b.priority}) - @${b.assignee}`)
        .join("\n");

  // Step 8: Store result in KV for OpenClaw to send back
  await kv_set("results", "jira_blockers", JSON.stringify({
    summary,
    blockers,
    timestamp: new Date().toISOString()
  }));

  // Step 9: Clean up
  await close_session(sessionId);

  return summary;
}

// Usage in OpenClaw:
// WhatsApp: "Check my Jira for blockers"
// → OpenClaw calls this function
// → Agent returns summary
// → WhatsApp: "✓ No blockers! Release is clear."
```

**Key Patterns:**
- Separate agent profile (never touch personal data)
- Pre-authenticated via snapshots (no re-auth)
- Domain allowlist (containment)
- Stealth mode (if site detects automation)
- KV store result for async communication
- Mobile-friendly text summary

---

## ICP 3: Security-Conscious User — PII-Safe HR Workflow

**Goal:** Automatically process HR requests (send offer letters, update employee records) without PII ever reaching Claude.

### Scenario
Process a new hire offer letter template. Agent:
1. Opens HR system with anonymization enabled
2. Reads employee data (all PII tokenized)
3. Works with tokens instead of real values
4. Fills offer letter with tokens
5. Submits (Pagerunner de-tokenizes only when writing to DOM)

### Full Workflow

```javascript
async function processOfferLetter(employeeId) {
  // Step 1: Open session with anonymization mandatory
  const sessionId = await open_session({
    profile: "agent-hr",
    anonymize: true,                    // PII protection
    anonymization_mode: "tokenize",     // Agent gets tokens
    anonymization_profile: "hr-work",   // Uses custom patterns
    allowed_domains: ["hr.company.com"] // Containment
  });

  const tabs = await list_tabs(sessionId);
  const tabId = tabs[0].target_id;

  // Step 2: Navigate to HR system
  await navigate(sessionId, tabId, "https://hr.company.com/offers/new");
  await restore_snapshot(sessionId, tabId, origin: "https://hr.company.com");
  await wait_for(sessionId, tabId, selector: "[data-testid='offer-form']", ms: 5000);

  // Step 3: Get employee data
  // Real page: "Employee: John Smith (john@company.com) | Role: Engineer | Start: 2026-04-01"
  // Agent receives: "Employee: [PERSON:xyz789] ([EMAIL:abc123]) | Role: Engineer | Start: 2026-04-01"
  const employeeData = await get_content(sessionId, tabId);
  console.log("Employee data (anonymized):", employeeData);

  // Step 4: Extract fields using tokens
  const fields = await evaluate(sessionId, tabId, `
    ({
      name: document.querySelector('[data-testid="employee-name"]').textContent,
      email: document.querySelector('[data-testid="employee-email"]').textContent,
      role: document.querySelector('[data-testid="employee-role"]').textContent,
      startDate: document.querySelector('[data-testid="start-date"]').textContent,
      salary: document.querySelector('[data-testid="salary"]').textContent
    })
  `);
  // Returns:
  // {
  //   name: "[PERSON:xyz789]",
  //   email: "[EMAIL:abc123]",
  //   role: "Senior Engineer",
  //   startDate: "2026-04-01",
  //   salary: "$150000"
  // }

  // Step 5: Agent works with tokens (no real values visible)
  // Claude processes: tokens, not real data
  const letterData = {
    recipientName: fields.name,        // Still a token, safe to log
    recipientEmail: fields.email,      // Still a token
    role: fields.role,
    startDate: fields.startDate,
    salary: fields.salary
  };

  console.log("Letter data (safe to log, all PII is tokens):", letterData);

  // Step 6: Fill form with tokens
  // Agent passes token to fill()
  await fill(sessionId, tabId, "input[name='recipient-name']", fields.name);
  // Pagerunner de-tokenizes [PERSON:xyz789] → "John Smith" before typing
  // DOM sees real name, agent never did

  await fill(sessionId, tabId, "input[name='recipient-email']", fields.email);
  // Pagerunner de-tokenizes [EMAIL:abc123] → "john@company.com"

  await fill(sessionId, tabId, "textarea[name='offer-letter']", `
    Dear ${fields.name},

    Congratulations on your offer for ${fields.role} starting ${fields.startDate}.
    Annual salary: ${fields.salary}

    Please confirm by replying to this email.

    Best regards,
    HR Team
  `);
  // All tokens de-tokenized before typing

  // Step 7: Submit
  await click(sessionId, tabId, "[data-testid='submit-btn']");
  await wait_for(sessionId, tabId, selector: "[data-testid='success-message']", ms: 5000);

  // Step 8: Verify submission (without exposing real values)
  const result = await get_content(sessionId, tabId);
  // Returns: "Offer sent to [EMAIL:abc123]" (not "john@company.com")

  console.log("Offer submitted successfully");

  // Step 9: Audit trail (security team can verify)
  // Audit log shows: { event: "get_content", pii_entities: { EMAIL: 1, PERSON: 1 } }
  // Proves PII was encountered but never logged in plaintext

  await close_session(sessionId);

  return {
    success: true,
    message: "Offer letter sent",
    auditProof: "Check ~/.pagerunner/audit.log for compliance trail"
  };
}
```

**Key Patterns:**
- Anonymization mandatory for sensitive data
- Tokenize mode (agent gets tokens, works safely)
- Custom anonymization profiles (domain-specific PII)
- Domain allowlist (strict containment)
- De-tokenization transparent (only at write time)
- Audit log proof (compliance trail)

---

## ICP 4: Server-Side Infrastructure — Scheduled Jira Summary

**Goal:** Daemon-based automation: every morning at 8am, pull Jira board, summarize overnight changes, post to Slack.

### Scenario
Cron job + Pagerunner daemon:
- Multiple agents can connect (no DB lock)
- Agent A: Scrapes Jira, stores in KV
- Agent B: Reads KV, generates summary
- Agent C: Posts to Slack
- All share auth state via snapshots

### Full Workflow

```bash
#!/bin/bash
# Daily Jira standup — run via cron

# Assuming daemon is running:
# pagerunner daemon &
# And Jira snapshot exists:
# pagerunner save-snapshot <session> <tab> https://jira.mycompany.com

# Agent A: Scrape Jira and store snapshot
node agent-a-scraper.js

# Agent B: Read from KV and generate summary
node agent-b-summarizer.js

# Agent C: Post summary to Slack
node agent-c-slack-poster.js
```

**agent-a-scraper.js:**

```javascript
async function scrapeJiraBoard() {
  const sessionId = await open_session({
    profile: "agent-scraper",
    allowed_domains: ["jira.mycompany.com"]
  });

  const tabs = await list_tabs(sessionId);
  const tabId = tabs[0].target_id;

  // Navigate and restore auth
  await navigate(sessionId, tabId, "https://jira.mycompany.com/board/eng-team");
  await restore_snapshot(sessionId, tabId, origin: "https://jira.mycompany.com");
  await wait_for(sessionId, tabId, selector: "[data-testid='board-issues']", ms: 5000);

  // Extract all issues
  const issues = await evaluate(sessionId, tabId, `
    Array.from(document.querySelectorAll('[data-testid="issue"]')).map(el => ({
      key: el.querySelector('[data-testid="key"]').textContent,
      title: el.querySelector('[data-testid="title"]').textContent,
      status: el.querySelector('[data-testid="status"]').textContent,
      updated: el.getAttribute('data-updated')
    }))
  `);

  // Store for Agent B to process
  await kv_set("standup", "raw_issues", JSON.stringify(issues));
  await kv_set("standup", "scraped_at", new Date().toISOString());

  // Store auth checkpoint for Agent B
  const authSnapshot = await save_snapshot(sessionId, tabId, origin: "https://jira.mycompany.com");
  await kv_set("standup", "auth_snapshot_id", authSnapshot);

  await close_session(sessionId);

  console.log(`Scraped ${issues.length} issues`);
}

scrapeJiraBoard();
```

**agent-b-summarizer.js:**

```javascript
async function generateSummary() {
  // Retrieve data from Agent A
  const rawJson = await kv_get("standup", "raw_issues");
  const issues = JSON.parse(rawJson);

  // Filter overnight changes (since last summary)
  const lastSummary = await kv_get("standup", "last_summary_time");
  const recentChanges = issues.filter(issue => {
    const issueTime = new Date(issue.updated);
    return lastSummary ? issueTime > new Date(lastSummary) : true;
  });

  // Generate summary
  const summary = {
    date: new Date().toISOString(),
    totalIssues: issues.length,
    recentChanges: recentChanges.length,
    blocked: issues.filter(i => i.status === "Blocked").length,
    inProgress: issues.filter(i => i.status === "In Progress").length,
    details: recentChanges
      .map(i => `• ${i.key}: ${i.title} → ${i.status}`)
      .join("\n")
  };

  // Store for Agent C
  await kv_set("standup", "summary", JSON.stringify(summary));
  await kv_set("standup", "last_summary_time", new Date().toISOString());

  console.log(`Summary generated: ${recentChanges.length} changes overnight`);
}

generateSummary();
```

**agent-c-slack-poster.js:**

```javascript
async function postToSlack() {
  const summaryJson = await kv_get("standup", "summary");
  const summary = JSON.parse(summaryJson);

  // Slack webhook (stored securely in KV or env)
  const slackWebhook = await kv_get("config", "slack_webhook");

  const message = {
    text: "🌅 Daily Jira Standup",
    blocks: [
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: `*Daily Jira Summary*\n_${summary.date}_\n\n` +
                `Total: ${summary.totalIssues} | Blocked: ${summary.blocked} | In Progress: ${summary.inProgress}`
        }
      },
      {
        type: "section",
        text: {
          type: "mrkdwn",
          text: summary.details.substring(0, 1000)  // Slack limits
        }
      }
    ]
  };

  // Post to Slack
  await fetch(slackWebhook, {
    method: "POST",
    body: JSON.stringify(message)
  });

  console.log("Summary posted to Slack");
}

postToSlack();
```

**Crontab:**

```bash
# Run every morning at 8am
0 8 * * * cd /home/agent && node agent-a-scraper.js && node agent-b-summarizer.js && node agent-c-slack-poster.js
```

**Key Patterns:**
- Daemon for shared state (no DB lock conflicts)
- KV store for inter-agent communication
- Snapshots as auth checkpoints (no re-auth between agents)
- CLI compatibility (no MCP client needed, just Node.js)
- Cron scheduling (standard Unix automation)

---

## Bonus: ICP 4 — Multi-Agent Data Pipeline

**Scenario:** Process a list of competitor sites: scrape, analyze, store results.

Agent A: Scrape 100 competitor URLs (store in KV)
Agent B: Analyze competitor pricing (read from KV, enrich data)
Agent C: Update internal database (read from KV, post to API)

```javascript
// Agent A: Scraper
async function scrapeCompetitors() {
  const urls = [
    "https://competitor-1.com/pricing",
    "https://competitor-2.com/pricing",
    // ... 98 more
  ];

  for (const url of urls) {
    const sessionId = await open_session({ profile: "scraper", stealth: true });
    const [tab] = await list_tabs(sessionId);

    await navigate(sessionId, tab.target_id, url);
    await wait_for(sessionId, tab.target_id, selector: ".pricing-table", ms: 5000);

    const data = await evaluate(sessionId, tab.target_id, `
      ({ url: window.location.href, prices: Array.from(document.querySelectorAll('.price')).map(el => parseFloat(el.textContent)) })
    `);

    await kv_set("pipeline", `pricing_${url}`, JSON.stringify(data));
    await close_session(sessionId);

    console.log(`Scraped: ${url}`);
  }

  // Signal completion
  await kv_set("pipeline", "scrape_complete", "true");
}

// Agent B: Analyzer
async function analyzeCompetitors() {
  // Wait for Agent A to finish
  while (!await kv_get("pipeline", "scrape_complete")) {
    await wait(5000);  // Poll every 5 seconds
  }

  const allKeys = await kv_list("pipeline", prefix: "pricing_");

  for (const { key, value } of allKeys) {
    const data = JSON.parse(value);
    const analysis = {
      url: data.url,
      avgPrice: data.prices.reduce((a, b) => a + b) / data.prices.length,
      minPrice: Math.min(...data.prices),
      maxPrice: Math.max(...data.prices),
      priceRange: Math.max(...data.prices) - Math.min(...data.prices)
    };

    await kv_set("pipeline", `analysis_${key}`, JSON.stringify(analysis));
  }

  await kv_set("pipeline", "analyze_complete", "true");
}

// Agent C: Database updater
async function updateDatabase() {
  // Wait for Agent B
  while (!await kv_get("pipeline", "analyze_complete")) {
    await wait(5000);
  }

  const allKeys = await kv_list("pipeline", prefix: "analysis_");

  for (const { value } of allKeys) {
    const analysis = JSON.parse(value);

    // Post to your own internal API — use kv_get() to retrieve credentials
    const apiKey = await kv_get("config", "internal_api_key");
    const response = await fetch("https://internal-api.company.com/competitors", {
      method: "POST",
      body: JSON.stringify(analysis),
      headers: { "Authorization": `Bearer ${apiKey}` }
    });

    console.log(`Updated database: ${analysis.url}`);
  }

  // Cleanup
  await kv_clear("pipeline");
}
```

**Key Patterns:**
- Agent A → KV (scrape results)
- Agent B waits for A → reads KV → writes analysis to KV
- Agent C waits for B → reads KV → posts to API
- Polling for agent coordination
- Cleanup after completion

---

## Testing Your Workflows

### Before Production

1. **Test with sample data:**
   ```javascript
   const testData = { issues: [...] };
   await kv_set("test", "sample", JSON.stringify(testData));
   ```

2. **Verify selectors:**
   ```javascript
   const elementExists = await evaluate(sessionId, tabId, `
     !!document.querySelector('[data-testid="expected-element"]')
   `);
   ```

3. **Check auth before automation:**
   ```javascript
   const isAuthenticated = await evaluate(sessionId, tabId, `
     !!document.querySelector('[data-testid="user-profile"]')
   `);
   ```

4. **Enable audit logging:**
   ```bash
   tail -f ~/.pagerunner/audit.log | jq .
   ```

---

## Next Steps

Try one of these workflows, adapt to your real URLs, test with small batches first, monitor audit logs, scale gradually.

See PATTERNS.md for technique guides, REFERENCE.md for all tool APIs.
