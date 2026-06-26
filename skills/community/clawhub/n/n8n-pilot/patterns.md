# Workflow Design Patterns & Recipes — n8n

Proven patterns for common automation scenarios. Each pattern includes a logic map, node types, and gotchas.

---

## Pattern 1: Linear Pipeline

**Use when:** Simple A → B → C → D data processing

```
Trigger → Transform → Process → Output
```

**Example:** RSS feed → filter → summarize → save
```
Schedule Trigger (every 2h)
  → HTTP Request (fetch RSS)
  → XML (parse feed)
  → Filter (keywords match?)
  → OpenAI (summarize article)
  → Google Sheets (append row)
```

**Gotchas:**
- Each node receives the output of the previous node as `$input`
- If any node returns multiple items, downstream nodes process each item independently
- Use Set node to restructure data between incompatible nodes

---

## Pattern 2: Conditional Branching

**Use when:** Different actions based on data content

```
Trigger → IF/Switch
  → Branch A: Process one way
  → Branch B: Process another way
  → (optional) Branch C: Fallback
```

**Example:** Email triage
```
Email Trigger
  → Switch (by sender domain)
    → "company.com": → AI classify → Add to CRM
    → "linkedin.com": → Archive
    → Default: → Mark unread + Telegram alert
```

**Gotchas:**
- Switch outputs are indexed (0, 1, 2...) — map connections carefully
- IF has only two outputs (true/false)
- Both branches can merge later using Merge node

---

## Pattern 3: Fan-Out / Fan-In

**Use when:** Parallel processing of the same data

```
Trigger → Split into N branches → Process in parallel → Merge results
```

**Example:** Multi-API enrichment
```
Webhook (user signup)
  → Branch 1: Enrich with Clearbit API
  → Branch 2: Check fraud with IP API
  → Branch 3: Add to Mailchimp
  → Merge (wait for all)
  → Save enriched record to database
```

**Gotchas:**
- n8n automatically runs independent branches in parallel
- Merge node waits for all inputs by default
- Use `mergeByKey` to join results from different APIs on a shared field

---

## Pattern 4: Loop with Pagination

**Use when:** Processing paginated APIs or large datasets

```
HTTP Request (page 1)
  → Code node (check if more pages)
  → IF (has more?)
    → Yes: HTTP Request (next page) → loop back
    → No: Continue
```

**Better approach — Split In Batches:**
```
HTTP Request (fetch all records)
  → Split In Batches (size: 50)
    → Process batch
  → Continue (all done)
```

**Gotchas:**
- Always set `batchSize` in Split In Batches — default may be too large
- For API pagination, use Code node to track `next_cursor` or `offset`
- Add a safety counter in Code nodes to prevent infinite loops

---

## Pattern 5: Error Handling with Fallback

**Use when:** Critical workflows that must not fail silently

```
Trigger → Process
  → Success: Continue
  → Error: Error branch → Fallback action → Notify
```

**Implementation:**
1. Add Error Trigger node in a **separate** monitoring workflow
2. In main workflow, enable "Continue on Fail" on risky nodes
3. Use IF node to check `$json.error` after risky operations
4. Error Trigger workflow sends Telegram/Slack alert with error details

**Gotchas:**
- "Continue on Fail" means the node passes error data downstream — you must check for it
- Error Trigger captures ALL workflow errors, not specific nodes
- Always include the workflow name and execution ID in error notifications

---

## Pattern 6: Sub-Workflow Orchestration

**Use when:** Reusable logic called from multiple workflows

```
Main Workflow A → Execute Workflow ("Send Notification") → Continue
Main Workflow B → Execute Workflow ("Send Notification") → Continue
```

**Sub-workflow setup:**
1. Create sub-workflow with Workflow Trigger node
2. In main workflow, use Execute Workflow node referencing sub-workflow ID
3. Pass data to sub-workflow via `items` parameter
4. Sub-workflow returns data to main flow

**Gotchas:**
- Sub-workflow must have a Workflow Trigger node (not Manual or Webhook)
- Changes to sub-workflow affect ALL calling workflows — test carefully
- Sub-workflows can be nested but avoid deep nesting (>3 levels)

---

## Pattern 7: Scheduled Batch Processing

**Use when:** Periodic data processing (ETL, syncs, reports)

```
Schedule Trigger → Fetch data → Split in batches → Process → Aggregate → Notify
```

**Example:** Daily sales report
```
Schedule Trigger (daily 8am)
  → PostgreSQL (query yesterday's sales)
  → Code (calculate totals, top products, trends)
  → Google Sheets (update dashboard)
  → Telegram (send summary: "€4,230 revenue, +12% vs yesterday")
```

**Gotchas:**
- Use timezone in Schedule Trigger settings
- Set `EXECUTIONS_DATA_PRUNE=true` to avoid execution history bloat
- Add Wait nodes between API calls if rate-limited

---

## Pattern 8: Webhook → Process → Respond

**Use when:** Building API endpoints with n8n

```
Webhook (POST /api/endpoint)
  → Validate input
  → IF (valid?)
    → Yes: Process → Respond to Webhook (200 + data)
    → No: Respond to Webhook (400 + error)
```

**Gotchas:**
- Default webhook responds immediately with `{"message": "Workflow was started"}`
- Use "Respond to Webhook" node to send custom responses
- Set webhook `responseMode: "lastNode"` to wait for workflow completion before responding
- Always validate input before processing

---

## Advanced Recipes

### The AI Email Classifier

```
Email Trigger (IMAP)
  → Code (extract sender, subject, body, attachments)
  → OpenAI (classify: "Classify this email as: urgent, newsletter, spam, follow-up, or other")
  → Switch (by classification)
    → "urgent": Telegram alert + Calendar event
    → "newsletter": Archive + label
    → "spam": Delete
    → "follow-up": Add to task list
    → "other": Mark read
```

### The GitHub PR Sentinel

```
GitHub Trigger (new PR)
  → HTTP Request (fetch diff)
  → OpenAI (review: "Review this PR for security issues and code quality")
  → IF (score < 7?)
    → Yes: GitHub comment (review feedback) + label "needs-work"
    → No: Label "approved" + notify channel
```

### The Price Tracker

```
Schedule Trigger (every 6h)
  → HTTP Request (fetch product price API)
  → Code (compare with stored price in Redis)
  → IF (price drop > 10%?)
    → Yes: Telegram alert + update stored price
    → No: End
```

### The Database Sync Pipeline

```
Schedule Trigger (every hour)
  → PostgreSQL Source (query new/updated records)
  → Split In Batches (size: 100)
    → IF (record exists in target?)
      → Yes: PostgreSQL Target (update)
      → No: PostgreSQL Target (insert)
  → Code (count synced records)
  → Telegram (sync summary)
```

### The Monitoring Alert Pipeline

```
Schedule Trigger (every 5 min)
  → HTTP Request (health check endpoint)
  → IF (status != 200 or response time > 5s?)
    → Yes:
      → IF (first failure?)
        → Yes: Telegram alert ("Service X down")
        → No: Increment failure counter
      → IF (3 consecutive failures?)
        → Yes: PagerDuty / urgent alert
    → No: Reset failure counter
```