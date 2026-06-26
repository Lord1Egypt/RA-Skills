---
name: n8n-autopilot
description: >
  AI-powered n8n workflow builder and deployer by Dr. FIRAS.
  Generates production-ready n8n workflow JSON from natural language, validates
  structure and logic, then auto-deploys to any n8n instance via REST API.
  Use this skill whenever the user wants to create, build, design, generate,
  deploy, or publish an n8n workflow — even from a plain description like
  "automate my Stripe payments to Slack". Also triggers when the user pastes
  n8n workflow JSON for review, debugging, optimization, or redeployment.
  Covers: workflow generation, structural validation, auto-deployment,
  activation, execution monitoring, and performance diagnostics.
  LinkedIn: https://www.linkedin.com/in/doctor-firass/
metadata: {"openclaw":{"emoji":"🚀","requires":{"env":["N8N_API_KEY","N8N_BASE_URL"]},"primaryEnv":"N8N_API_KEY"}}
---

# n8n Autopilot — AI Workflow Builder & Deployer

> **By Dr. FIRAS** — [LinkedIn](https://www.linkedin.com/in/doctor-firass/)

Build complete n8n workflows from natural language, validate them, and deploy
them to your n8n instance — all in one step. No placeholders, no TODOs,
no manual assembly required.

---

## Golden Rules

**ALWAYS:**
1. Generate every node with real, configured parameters (URLs, paths, expressions)
2. Wire all connections explicitly in the `connections` object
3. Include exactly one trigger node per workflow
4. Assign node positions for a clean canvas layout (~200 px spacing)
5. Validate the workflow before presenting it to the user
6. Offer to deploy automatically when `N8N_API_KEY` is configured

**NEVER:**
- Output placeholder nodes ("configure this later", "add your logic here")
- Leave `url`, `path`, or `jsCode` fields empty
- Create disconnected nodes
- Present partial flows expecting manual completion

---

## Setup

Two environment variables are needed:

| Variable | Where to find it |
|---|---|
| `N8N_API_KEY` | n8n UI → Settings → API → Create API Key |
| `N8N_BASE_URL` | Your instance URL, e.g. `https://n8n.example.com` |

Set them via OpenClaw settings (`~/.config/openclaw/settings.json`):
```json
{
  "skills": {
    "n8n-autopilot": {
      "env": {
        "N8N_API_KEY": "your-key",
        "N8N_BASE_URL": "https://your-n8n.example.com"
      }
    }
  }
}
```

Verify connectivity:
```bash
python3 scripts/n8n_deploy.py ping
```

---

## Workflow Generation Pipeline

Follow these steps for every workflow request:

### Step 1 — Understand the intent

Determine four things before writing JSON:
- **Trigger**: webhook, schedule, manual, or external event?
- **Data source**: webhook body, API, database, file?
- **Processing**: transforms, conditionals, enrichment?
- **Output**: API call, notification, database write, webhook response?

If the request is clear, skip to generation. Do not over-ask.

### Step 2 — Plan the node chain

Map the flow mentally:
```
Trigger → [Ingest] → [Transform] → [Branch?] → [Act] → [Respond/Store]
```

### Step 3 — Generate the JSON

Use the `WorkflowForge` builder (see `scripts/workflow_forge.py`) or write
raw JSON. Output a single valid JSON object ready for n8n's "Import from JSON".

### Step 4 — Self-validate

Run through the validation checklist below. Fix every issue before showing
the user. You can also call:
```bash
python3 scripts/workflow_inspector.py check --file workflow.json
```

### Step 5 — Deploy (if API is configured)

```bash
python3 scripts/n8n_deploy.py push --file workflow.json
python3 scripts/n8n_deploy.py push --file workflow.json --activate
```

### Step 6 — Explain

Provide a brief node-by-node table and import/credential instructions.

---

## JSON Skeleton

```json
{
  "name": "Descriptive Workflow Name",
  "nodes": [],
  "connections": {},
  "active": false,
  "settings": { "executionOrder": "v1" }
}
```

### Node structure
```json
{
  "id": "unique-uuid-v4",
  "name": "Human Readable Name",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4,
  "position": [500, 300],
  "parameters": { ... },
  "credentials": { "httpHeaderAuth": { "id": "1", "name": "My Auth" } }
}
```

### Connection structure
```json
{
  "connections": {
    "Source Node Name": {
      "main": [
        [{ "node": "Target Node Name", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

- Keys = node **names** (not IDs)
- `main` = array of arrays (outer = output index, inner = targets)
- IF nodes: index 0 = true, index 1 = false
- Terminal nodes must NOT appear as keys

---

## Node Catalog (Quick Ref)

### Triggers
| Type | Ver | Purpose |
|------|-----|---------|
| `n8n-nodes-base.manualTrigger` | 1 | Testing / manual runs |
| `n8n-nodes-base.webhook` | 2 | HTTP webhook receiver |
| `n8n-nodes-base.scheduleTrigger` | 1 | Cron / interval |

### Logic & Transform
| Type | Ver | Purpose |
|------|-----|---------|
| `n8n-nodes-base.code` | 2 | JavaScript / Python |
| `n8n-nodes-base.set` | 3 | Map / rename / add fields |
| `n8n-nodes-base.if` | 2 | Conditional branch |
| `n8n-nodes-base.switch` | 3 | Multi-way routing |
| `n8n-nodes-base.merge` | 3 | Combine streams |
| `n8n-nodes-base.splitInBatches` | 3 | Loop / batch |
| `n8n-nodes-base.noOp` | 1 | No-op terminus |

### HTTP & Response
| Type | Ver | Purpose |
|------|-----|---------|
| `n8n-nodes-base.httpRequest` | 4 | Any REST call |
| `n8n-nodes-base.respondToWebhook` | 1 | Webhook reply |

### Popular Integrations
| Type | Ver | Purpose |
|------|-----|---------|
| `n8n-nodes-base.slack` | 2 | Slack messages |
| `n8n-nodes-base.gmail` | 2 | Gmail |
| `n8n-nodes-base.googleSheets` | 4 | Google Sheets |
| `n8n-nodes-base.notion` | 2 | Notion |
| `n8n-nodes-base.postgres` | 2 | PostgreSQL |
| `n8n-nodes-base.telegram` | 2 | Telegram |

### AI / LLM
| Type | Ver | Purpose |
|------|-----|---------|
| `@n8n/n8n-nodes-langchain.openAi` | 1 | OpenAI completions |
| `@n8n/n8n-nodes-langchain.lmChatOpenAi` | 1 | OpenAI chat model |

For full credential mapping, see `references/node-catalog.md`.

---

## Expression Cheat Sheet

| Pattern | Meaning |
|---------|---------|
| `={{ $json.field }}` | Current item field |
| `={{ $json["field-name"] }}` | Hyphenated field |
| `={{ $node["Name"].json.field }}` | Upstream node field |
| `={{ $input.all() }}` | All items (Code node) |
| `={{ $input.first().json.f }}` | First item field |
| `={{ $now.toISO() }}` | Current ISO timestamp |
| `={{ $vars.MY_VAR }}` | Environment variable |

---

## Validation Checklist

Before outputting any workflow, verify:

**Structure:**
- [ ] `nodes` array exists and is non-empty
- [ ] `connections` covers every non-terminal node
- [ ] Every node has `id`, `name`, `type`, `typeVersion`, `position`, `parameters`

**Integrity:**
- [ ] Exactly one trigger node
- [ ] Node names are unique
- [ ] Node IDs are unique UUIDs
- [ ] No required parameter is empty (`url`, `path`, `jsCode`)

**Graph:**
- [ ] Every connection target matches a real node name
- [ ] IF/Switch nodes define all expected output branches
- [ ] No unreachable (disconnected) nodes
- [ ] No cycles in the execution graph

**Credentials:**
- [ ] Nodes that need auth include a `credentials` block
- [ ] Credential type names are correct for their node

**Expressions:**
- [ ] `={{ ... }}` references point to fields that upstream nodes produce

---

## CLI Reference

### Deployment (`n8n_deploy.py`)
```bash
# Connectivity check
python3 scripts/n8n_deploy.py ping

# List workflows
python3 scripts/n8n_deploy.py ls [--active]

# Push (create) a workflow
python3 scripts/n8n_deploy.py push --file workflow.json [--activate]

# Inspect a deployed workflow
python3 scripts/n8n_deploy.py inspect --id <wf-id>

# Activate / deactivate
python3 scripts/n8n_deploy.py on --id <wf-id>
python3 scripts/n8n_deploy.py off --id <wf-id>

# Trigger manual execution
python3 scripts/n8n_deploy.py run --id <wf-id> [--payload '{"key":"val"}']

# View recent executions
python3 scripts/n8n_deploy.py history --id <wf-id> [--limit 10]

# Execution details
python3 scripts/n8n_deploy.py exec-detail --id <exec-id>

# Execution statistics
python3 scripts/n8n_deploy.py stats --id <wf-id> [--days 7]

# Delete workflow
python3 scripts/n8n_deploy.py rm --id <wf-id>
```

### Validation & Diagnostics (`workflow_inspector.py`)
```bash
# Validate a local file
python3 scripts/workflow_inspector.py check --file workflow.json

# Validate a deployed workflow
python3 scripts/workflow_inspector.py check --id <wf-id>

# Full diagnostic report (structure + performance)
python3 scripts/workflow_inspector.py diagnose --id <wf-id> [--days 14]

# Optimization suggestions only
python3 scripts/workflow_inspector.py optimize --id <wf-id>
```

### Programmatic Builder (`workflow_forge.py`)
```bash
# Build from a recipe YAML and deploy
python3 scripts/workflow_forge.py build --recipe recipe.yaml --deploy

# Export as JSON
python3 scripts/workflow_forge.py build --recipe recipe.yaml --output wf.json
```

---

## Optimization Heuristics

Apply when generating workflows:

1. **Fan-out over chaining**: independent API calls should branch in parallel,
   not run sequentially.
2. **Batch large datasets**: use `splitInBatches` instead of Code-node loops.
3. **Error paths**: add an Error Trigger or IF-based error branch for
   workflows with external API calls.
4. **Timeouts**: set `executionTimeout` in `settings` for long-running flows.
5. **Avoid duplicate fetches**: fetch once, reshape with Set/Code.
6. **Split at 15 nodes**: suggest sub-workflows via Execute Workflow node.

---

## Output Formatting

Every workflow response must include:

1. A one-sentence summary of the workflow's purpose
2. The complete JSON in a fenced code block
3. A node explanation table:

| # | Node | Type | What it does |
|---|------|------|--------------|
| 1 | Webhook Trigger | webhook | Receives POST requests |
| 2 | Parse Input | set | Extracts email and name |

4. Import instructions: "Open n8n → Workflows → Import from JSON → paste"
5. Credentials the user must configure post-import
6. (If API is configured) an offer to auto-deploy

---

## Common Flow Patterns

### Webhook → Transform → Respond
```
Webhook → Set (extract) → Code (transform) → Respond to Webhook
```

### Schedule → Fetch → Store
```
Schedule → HTTP Request (fetch) → Code (process) → Google Sheets (append)
```

### Webhook → Branch → Multi-action
```
Webhook → IF →  true: Slack notify  → NoOp
              false: Email alert   → NoOp
```

### Polling with error handling
```
Schedule → HTTP Request → IF (ok?) →  true: Process → Store
                                    false: Slack error alert
```

---

## File Layout

```
n8n-autopilot/
├── SKILL.md                     # This file
├── README.md                    # Project overview
├── scripts/
│   ├── n8n_deploy.py           # API client + deployment CLI
│   ├── workflow_forge.py       # Programmatic workflow builder
│   └── workflow_inspector.py   # Validation + diagnostics
└── references/
    └── node-catalog.md         # Node types & credential mapping
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `N8N_API_KEY not set` | Export the variable or add to OpenClaw settings |
| `HTTP 401 Unauthorized` | Regenerate API key in n8n Settings → API |
| `Connection refused` | Check `N8N_BASE_URL` — include protocol and port |
| Validation: cycle detected | Break circular connections; use sub-workflows |
| Execution timeout | Add `executionTimeout` in settings; optimize slow nodes |
| Rate limit (429) | Insert Wait nodes; use batch processing |
