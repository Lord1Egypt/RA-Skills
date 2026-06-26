---
name: n8n-pilot
version: 0.1.0
description: "Design, build, deploy, test, and secure advanced n8n workflows. Architecture patterns, flow logic, dangerous pattern detection, self-hosting, credential management, and workflow recipes. Not an API wrapper — a workflow architect."
changelog: "v0.1.0 MVP: design patterns, flow logic, self-hosting, credentials, testing, security, dangerous pattern detection, 3 core recipes"
metadata: {"clawdbot":{"emoji":"⚙️","requires":{"env":["N8N_API_KEY","N8N_BASE_URL"]},"primaryEnv":"N8N_API_KEY"}}
---

# n8n Pilot ⚙️

Design, build, deploy, test, and secure advanced n8n workflows. Not an API wrapper — a workflow architect that guides you from intent to production.

## When to Use

Use when the task involves n8n — designing workflows, building automations, deploying instances, diagnosing failures, optimizing performance, or securing webhooks/credentials.

## Companion Skills

- `clawhub install n8n` — API client for CRUD operations (list/create/activate workflows)
- `clawhub install docker-pilot` — Container lifecycle management for deploying n8n

---

## Safety Architecture ⚠️

### Dangerous Pattern Detection

Before deploying ANY workflow, scan for these patterns:

| Pattern | Risk | Detection |
|---------|------|-----------|
| Loop without max iteration | 🔴 Infinite execution | Split In Batches without `batchSize`, or Code node with `while(true)` |
| Delete without filter | 🔴 Data destruction | Database delete/HTTP DELETE without WHERE/filter parameters |
| Webhook without auth | 🟡 Anyone can trigger | Webhook node with `authentication=none` |
| HTTP to private IPs | 🟡 SSRF risk | HTTP Request to `10.x`, `172.16-31.x`, `192.168.x`, `localhost` |
| Email/Send without limit | 🟡 Mass spam | Loop + email/Send node without max cap |
| No error handling | 🟡 Silent failures | Workflow with no Error Trigger or error branches |
| Hardcoded secrets | 🔴 Credential exposure | Code node containing API keys, passwords, tokens in plaintext |

**Rule:** Workflows with 🔴 patterns MUST be fixed before deployment. 🟡 patterns require user acknowledgment.

### Confirmation Gates

- **New workflow deployment:** Show logic map → confirm → deploy inactive → test → activate
- **Workflow modification:** Show diff (what changed) → confirm → deploy
- **Destructive operations** (delete workflow, prune executions): Full audit + explicit confirmation

### Kill Switch

If a workflow goes haywire:
```bash
# Deactivate all workflows immediately
python3 scripts/n8n_api.py list-workflows --active true | \
  python3 -c "import sys,json; [print(w['id']) for w in json.load(sys.stdin)['data']]" | \
  xargs -I{} python3 scripts/n8n_api.py deactivate --id {}
```

---

## Workflow Design: Intent → Logic Map → JSON

### Step 1: Understand Intent

Before building, articulate the workflow in plain language:

```
"I want to be notified on Telegram when an important email arrives from my boss."
```

### Step 2: Create Logic Map

Translate intent into a logic map (show to user for confirmation):

```
📧 Email Trigger (new email)
  → 🧠 IF node (sender contains "boss@company.com")
    → ✅ Yes: Summarize email content
      → 📱 Telegram notification (summary)
    → ❌ No: Skip
```

### Step 3: Generate Workflow JSON

Convert the logic map into n8n workflow JSON structure:

```json
{
  "name": "Boss Email → Telegram Alert",
  "nodes": [...],
  "connections": {...},
  "settings": {
    "executionOrder": "v1",
    "timezone": "Europe/Berlin"
  }
}
```

**Key JSON fields:**
- `typeVersion` — must match the node version installed in your n8n instance
- `position` — [x, y] coordinates for UI rendering (required by API)
- `credentials` — embedded as `{credential_type: {id, name}}`, not just an ID
- `parameters` — node-specific config, use `=` prefix for expressions
- `settings.executionOrder` — must be `"v1"` for modern n8n
- `pinData` — inject mock data per-node for testing

---

## Flow Logic Patterns

### Branching (IF / Switch)

```
Trigger → IF (condition)
  → True branch: [process A]
  → False branch: [process B or Stop]
```

**IF Node config:**
```json
{
  "type": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "boolean": [{
        "value1": "={{ $json.sender }}",
        "operation": "contains",
        "value2": "boss@company.com"
      }]
    }
  }
}
```

**Switch Node** (multi-way branching):
```json
{
  "type": "n8n-nodes-base.switch",
  "parameters": {
    "rules": [
      { "output": 0, "conditions": {...} },
      { "output": 1, "conditions": {...} }
    ]
  }
}
```

### Merging (Merge Node)

```
Branch A → Merge → Continue
Branch B ↗
```

**Modes:**
- `append` — combine all items from all inputs
- `mergeByPosition` — zip items by index
- `mergeByKey` — join on a shared field (like SQL JOIN)

### Looping (Split In Batches / Loop Over Items)

```
Large Dataset → Split In Batches (size=100)
  → Process batch
  → Loop back
→ Continue when done
```

**⚠️ Always set `batchSize`** — prevents memory exhaustion on large datasets.

### Sub-Workflows (Execute Workflow Node)

```
Main Workflow → Execute Workflow (sub-workflow ID)
  → Use sub-result in main flow
```

**Use cases:** Reusable logic (e.g., "send notification" sub-workflow called by 5 different main workflows), breaking complex flows into manageable pieces.

**Important:** Sub-workflow must have a trigger that accepts calls from parent (`Workflow Trigger` node).

### Error Handling (Error Trigger + Error Branches)

**Pattern 1: Error Trigger Node**
```
[Separate workflow]
Error Trigger → Notify (Telegram/Email) with error details
```

**Pattern 2: Per-node error branch**
```
HTTP Request → [on error] → Log error + fallback action
             → [on success] → Continue normal flow
```

### Retry with Exponential Backoff

n8n has no built-in retry with backoff. Implement in Code node:

```javascript
// In a Code node, wrapping an API call
const maxRetries = 3;
const baseDelay = 1000; // 1 second

for (let attempt = 1; attempt <= maxRetries; attempt++) {
  try {
    const response = await this.helpers.httpRequest({
      url: 'https://api.example.com/data',
      method: 'GET',
    });
    return [{ json: response }];
  } catch (error) {
    if (attempt === maxRetries) throw error;
    const delay = baseDelay * Math.pow(2, attempt - 1);
    await new Promise(resolve => setTimeout(resolve, delay));
  }
}
```

---

## Core Node Catalog

### Trigger Nodes (Start a Workflow)

| Node | Use When | Key Config |
|------|----------|------------|
| Manual Trigger | Testing, one-off runs | No config — click "Execute" |
| Webhook | External systems calling n8n | Path, method (GET/POST), authentication |
| Schedule Trigger | Recurring (cron) tasks | Cron expression or interval |
| Email Trigger (IMAP) | New email arrives | IMAP credentials, folder, filter |
| Polling Trigger | Check API periodically | URL, interval, pagination |

### Flow Control Nodes

| Node | Use When | Key Config |
|------|----------|------------|
| IF | Binary branching | Conditions (boolean/string/number) |
| Switch | Multi-way branching | Rules with output indices |
| Merge | Combining branches | Mode (append/mergeByPosition/mergeByKey) |
| Split In Batches | Process large datasets in chunks | Batch size (always set this!) |
| Loop Over Items | Process items one at a time | Can use Split In Batches instead |
| Wait | Delay execution | Time (seconds) or specific time |
| No Operation | Placeholder / passthrough | Does nothing — useful for routing |

### Action Nodes

| Node | Use When | Key Config |
|------|----------|------------|
| HTTP Request | Any REST/GraphQL API | URL, method, headers, auth, body |
| Code (JavaScript) | Custom logic, transformation | Input items, access via `$input` |
| Set | Add/modify fields | Field assignments, expressions |
| Date & Time | Timezone conversion, formatting | Format string, timezone |
| Crypto | Hash, encrypt, sign | Algorithm, key |
| Spreadsheet File | Read/write Excel/CSV | File format, options |

### App Nodes (Common Integrations)

| Node | For | Auth Type |
|------|-----|-----------|
| Gmail | Send/read emails | OAuth2 |
| Google Sheets | Read/write spreadsheets | OAuth2 |
| Google Calendar | Event management | OAuth2 |
| Telegram | Send messages, bots | Bot token |
| Slack | Messages, channels | OAuth2 or Bot token |
| PostgreSQL | Database queries | Connection string |
| MySQL | Database queries | Connection string |
| MongoDB | Document queries | Connection string |
| Redis | Key-value operations | Connection string |
| GitHub | Repos, issues, PRs | Personal access token or OAuth2 |
| Discord | Messages, webhooks | Bot token |

---

## Self-Hosting Guide

### Development (Single Container)

```yaml
# docker-compose.yml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_ENCRYPTION_KEY=<generate-a-random-32-char-key>
      - WEBHOOK_URL=http://localhost:5678
      - TZ=Europe/Berlin
    volumes:
      - n8n_data:/home/node/.n8n
      - /etc/localtime:/etc/localtime:ro

volumes:
  n8n_data:
```

### Production (Queue Mode — PostgreSQL + Redis)

```yaml
# docker-compose.yml — production
services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: n8n
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: n8n
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U n8n"]
      interval: 30s
      timeout: 5s
      retries: 3

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 5s
      retries: 3

  n8n-main:
    image: docker.n8n.io/n8nio/n8n
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${DB_PASSWORD}
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      - N8N_ENCRYPTION_KEY=${ENCRYPTION_KEY}
      - WEBHOOK_URL=https://n8n.example.com
      - TZ=Europe/Berlin
      - EXECUTIONS_DATA_PRUNE=true
      - EXECUTIONS_DATA_MAX_AGE=336
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - n8n_data:/home/node/.n8n

  n8n-worker:
    image: docker.n8n.io/n8nio/n8n
    restart: unless-stopped
    command: worker --concurrency=5
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=${DB_PASSWORD}
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      - N8N_ENCRYPTION_KEY=${ENCRYPTION_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

volumes:
  pgdata:
  redis_data:
  n8n_data:
```

### Critical Environment Variables

| Variable | Purpose | Default | Production |
|----------|---------|---------|------------|
| `N8N_ENCRYPTION_KEY` | AES-256 key for credentials | Auto-generated | **Must be set and shared across all nodes** |
| `EXECUTIONS_MODE` | `regular` or `queue` | `regular` | `queue` for production |
| `DB_TYPE` | Database backend | SQLite | `postgresdb` for queue mode |
| `WEBHOOK_URL` | Public URL for webhooks | `http://localhost:5678` | `https://n8n.example.com` |
| `EXECUTIONS_DATA_PRUNE` | Auto-delete old executions | `false` | `true` |
| `EXECUTIONS_DATA_MAX_AGE` | Retention in hours | 336 (14d) | Set per policy |
| `N8N_GRACEFUL_SHUTDOWN_TIMEOUT` | Worker drain time (seconds) | 30 | 60+ for long workflows |
| `QUEUE_HEALTH_CHECK_ACTIVE` | Worker health endpoints | `false` | `true` |

### ⚠️ Queue Mode Requirements

- **PostgreSQL required** — SQLite does NOT work in queue mode
- **N8N_ENCRYPTION_KEY must be identical** across main + all workers
- **Community nodes must be installed on ALL containers** (main + every worker)

### Backup Strategy

```bash
# What to back up:
# 1. PostgreSQL database (pg_dump)
docker exec postgres pg_dump -U n8n n8n > n8n_backup_$(date +%Y%m%d).sql

# 2. n8n data volume (encryption key, config)
docker cp n8n:/home/node/.n8n ./n8n_data_backup/

# 3. .env file with passwords and encryption key
```

**Critical:** If you lose `N8N_ENCRYPTION_KEY`, ALL credentials become permanently unrecoverable. Back it up securely.

---

## Credential Management

### Creating Credentials

Credentials can be created via the REST API (`POST /credentials`) but **OAuth2 credentials require browser interaction** for the consent flow.

```bash
# Create an API key credential via API
curl -X POST "${N8N_BASE_URL}/api/v1/credentials" \
  -H "X-N8N-API-KEY: ${N8N_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My API Key",
    "type": "httpHeaderAuth",
    "data": {
      "name": "Authorization",
      "value": "Bearer sk-xxx"
    }
  }'
```

### OAuth2 Credentials

OAuth2 requires a browser redirect. **Cannot be fully automated.** Steps:
1. Create credential via API with `clientId` and `clientSecret`
2. User completes OAuth consent flow in browser
3. n8n stores the refresh/access tokens

### Encryption Key Management

- **CRITICAL:** `N8N_ENCRYPTION_KEY` encrypts ALL credentials with AES-256-GCM
- If lost, credentials are permanently unrecoverable — no reset possible
- Must be identical across main + all workers in queue mode
- Store in a password manager or `.env` file (never in docker-compose.yml in production)
- Rotating the key requires re-creating all credentials

### Credential Types

| Type | Auth Method | Automatable? |
|------|------------|-------------|
| `httpHeaderAuth` | Header-based (Bearer token) | ✅ Yes |
| `httpBasicAuth` | Username + password | ✅ Yes |
| `oAuth2Api` | OAuth2 flow | ❌ Requires browser |
| `telegramBotApi` | Bot token | ✅ Yes |
| `postgresApi` | Connection string | ✅ Yes |
| `mysqlApi` | Connection string | ✅ Yes |
| `smtpAccount` | SMTP credentials | ✅ Yes |
| `slackApi` | Bot token | ✅ Yes |

---

## Testing Strategy

### Pre-Deployment Checklist

1. **Validate structure** — all nodes have name, type, valid connections
2. **Check for dangerous patterns** (see Safety Architecture)
3. **Set `pinData`** — mock input data for testing without real triggers
4. **Deploy inactive** — never activate a new workflow without testing
5. **Manual trigger test** — run with test data, verify output
6. **Error branch test** — intentionally trigger error paths
7. **Activate** — only after all tests pass

### Mock Data with pinData

```json
{
  "nodes": [{
    "name": "Webhook",
    "type": "n8n-nodes-base.webhook",
    "parameters": { "path": "test-webhook" }
  }],
  "pinData": {
    "Webhook": [{ "json": { "email": "test@example.com", "subject": "Test" } }]
  }
}
```

`pinData` lets you test downstream nodes without the trigger actually firing.

### Validation Command

```bash
python3 scripts/n8n_tester.py validate --file workflow.json --pretty
```

### Test Execution

```bash
# Execute with test data
python3 scripts/n8n_api.py execute --id <workflow-id> --data '{"key": "value"}'

# Check result
python3 scripts/n8n_api.py get-execution --id <execution-id> --pretty
```

**⚠️ Note:** n8n has no native dry-run. `execute_workflow` runs the workflow for real. Always deploy workflows in inactive state and test with manual triggers before activating.

---

## Webhook Patterns

### Incoming Webhook (External → n8n)

```
External Service → POST https://n8n.example.com/webhook/my-path → n8n Workflow
```

**Security options:**
- `none` — no auth (⚠️ anyone can trigger)
- `headerAuth` — require specific header
- `basicAuth` — username + password
- `jwtAuth` — JWT token verification

**Best practice:** Always use at least `headerAuth`:

```json
{
  "type": "n8n-nodes-base.webhook",
  "parameters": {
    "path": "my-secure-webhook",
    "authentication": "headerAuth",
    "headerAuth": {
      "name": "X-Webhook-Secret",
      "value": "={{ $env.WEBHOOK_SECRET }}"
    }
  }
}
```

### Responding to Webhooks

By default, n8n responds immediately with `{"message": "Workflow was started"}`. To send custom responses:

```json
{
  "type": "n8n-nodes-base.respondToWebhook",
  "parameters": {
    "respondWith": "json",
    "responseBody": "={{ JSON.stringify({ status: 'ok', id: $json.id }) }}"
  }
}
```

### Webhook URL Construction

- **Production:** `{WEBHOOK_URL}/webhook/{path}`
- **Test:** `{WEBHOOK_URL}/webhook-test/{path}`
- Test webhooks only work when the workflow editor is open in the browser

---

## Workflow Recipes

### Recipe 1: Email → AI Summarize → Telegram

**"The Executive Assistant"**

```
📧 Email Trigger (IMAP)
  → 🧠 Code Node (extract sender, subject, body)
  → 🤖 OpenAI Node (summarize: "Summarize this email in 2 sentences")
  → 📱 Telegram Node (send summary)
  → 🏷️ Set Node (mark email as read)
```

**Logic map:**
"When a new email arrives, extract the content, use AI to summarize it, send the summary to my Telegram, and mark the email as read."

### Recipe 2: Webhook Receiver → Process → Respond

**"The API Processor"**

```
🌐 Webhook (POST /process)
  → 🧪 Validate input (Code node: check required fields)
  → ↔️ IF node (valid input?)
    → ✅ Yes: Process data (HTTP Request to external API)
      → 📤 Respond to Webhook (success + result)
    → ❌ No: Respond to Webhook (400 + error message)
  → 🚨 Error Trigger → Log + notify
```

**Logic map:**
"Receive a webhook, validate the input, process it if valid (or return an error), and respond to the caller."

### Recipe 3: Scheduled Data Sync

**"The Data Synchronizer"**

```
⏰ Schedule Trigger (every 6 hours)
  → 📥 HTTP Request (fetch from source API)
  → 🔀 Split In Batches (batch size: 100)
    → 🗃️ PostgreSQL Node (upsert records)
  → 🧮 Code Node (count synced records)
  → 📱 Telegram Node (sync summary: "Synced 847 records")
  → 🚨 Error Trigger → Log + retry notification
```

**Logic map:**
"Every 6 hours, fetch data from the source API, batch-upsert into the database, and send me a summary on Telegram."

---

## n8n API Gaps (What Requires UI)

| Task | API? | Workaround |
|------|------|------------|
| Create API key credentials | ✅ | `POST /credentials` |
| Install community nodes | ❌ | `npm install` in container + restart |
| OAuth2 consent flow | ❌ | Browser required — no automation |
| User management | ❌ | Internal API `/rest/users` or direct DB |
| Project CRUD | ❌ | UI only |
| Workflow variables | ❌ | Use `staticData` in Code nodes |
| License management | ❌ | UI only |

---

## Integration with OpenClaw Ecosystem

### Docker Pilot

Delegate n8n deployment to Docker Pilot:
- n8n-pilot provides the Compose files
- Docker Pilot handles container lifecycle (start/stop/restart/health checks)
- Docker Pilot protects the n8n container as a critical service

### Council of LLMs

Use n8n webhooks to trigger Council deliberations:
```
n8n Webhook → HTTP Request to OpenClaw → Spawn Council → Return result → n8n continues
```

### Thrift-Cycle

n8n as the execution engine for periodic eBay data collection:
```
Schedule Trigger → Run Thrift-Cycle pipeline → Parse results → Alert on hot items
```

---

## Quick Reference

| Task | Command / Pattern |
|------|-------------------|
| List workflows | `python3 scripts/n8n_api.py list-workflows --pretty` |
| Get workflow | `python3 scripts/n8n_api.py get-workflow --id ID --pretty` |
| Create workflow | `python3 scripts/n8n_api.py create --from-file workflow.json` |
| Activate | `python3 scripts/n8n_api.py activate --id ID` |
| Deactivate | `python3 scripts/n8n_api.py deactivate --id ID` |
| Execute | `python3 scripts/n8n_api.py execute --id ID --data '{}'` |
| Validate | `python3 scripts/n8n_tester.py validate --file workflow.json --pretty` |
| Check executions | `python3 scripts/n8n_api.py list-executions --limit 10 --pretty` |
| Performance | `python3 scripts/n8n_optimizer.py analyze --id ID --pretty` |
| Create credential | `curl -X POST BASE_URL/api/v1/credentials -H "X-N8N-API-KEY: KEY"` |
| Backup DB | `docker exec postgres pg_dump -U n8n n8n > backup.sql` |
| Install community node | `docker exec n8n npm install n8n-nodes-NAME && docker restart n8n` |

---

## First-Run Setup

When activating n8n-pilot on a new machine:

1. **Detect n8n instance** — check if port 5678 is listening, or scan Docker containers
2. **Verify API access** — test `GET /api/v1/workflows` with API key
3. **Audit existing workflows** — list all, check for failures, run dangerous pattern scan
4. **Configure credentials** — set up essential credentials (Telegram bot, email, database)
5. **Deploy if missing** — use Docker Pilot to deploy n8n with the self-hosting Compose files
6. **Enable monitoring** — set up health checks and execution pruning

---

## Credits

Extends the `n8n` skill by thomasansems (v2.0.0). This skill adds:
- ⚙️ Workflow design patterns (branching, merging, looping, sub-workflows)
- 🛡️ Dangerous pattern detection and safety architecture
- 🐳 Self-hosting guide (dev + production queue mode)
- 🔑 Credential management (creation, OAuth, encryption key)
- 🧪 Testing strategy (pinData, validation, pre-deployment checklist)
- 🔒 Webhook security patterns
- 📋 3 core workflow recipes
- 🚀 First-run setup and integration with Docker Pilot