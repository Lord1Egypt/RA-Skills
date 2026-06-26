# n8n Autopilot — AI Workflow Builder & Deployer

> **By Dr. FIRAS** — [LinkedIn](https://www.linkedin.com/in/doctor-firass/)

An OpenClaw skill that transforms natural language descriptions into
production-ready n8n workflows and deploys them to your instance in one step.

Inspired by the [n8n AI Workflow Builder](https://docs.n8n.io/advanced-ai/ai-workflow-builder/),
this skill brings the same power directly into your Claude conversations.

## What it does

1. **Builds** complete n8n workflow JSON from a plain description
2. **Validates** structure, connections, credentials, and detects cycles
3. **Deploys** to any n8n instance via REST API
4. **Activates** workflows automatically (optional)
5. **Monitors** executions and identifies performance bottlenecks
6. **Optimizes** with actionable suggestions

## Quick start

```bash
# 1. Configure
export N8N_API_KEY="your-api-key"
export N8N_BASE_URL="https://your-n8n.example.com"

# 2. Test connectivity
python3 scripts/n8n_deploy.py ping

# 3. Deploy a workflow
python3 scripts/n8n_deploy.py push --file my-workflow.json --activate

# 4. Validate before deploying
python3 scripts/workflow_inspector.py check --file my-workflow.json

# 5. Build from a recipe
python3 scripts/workflow_forge.py build --recipe recipe.json --deploy
```

## Architecture

```
n8n-autopilot/
├── SKILL.md                     # Skill definition & generation rules
├── README.md                    # This file
├── scripts/
│   ├── n8n_deploy.py           # API gateway + deployment pipeline
│   ├── workflow_forge.py       # Programmatic workflow builder
│   └── workflow_inspector.py   # Validation + performance diagnostics
└── references/
    └── node-catalog.md         # Node types & credential mapping
```

### Three modules, clear responsibilities

| Module | Role |
|--------|------|
| **n8n_deploy** | Talks to the n8n API — CRUD, execute, monitor |
| **workflow_forge** | Builds workflow JSON programmatically from Python or recipe files |
| **workflow_inspector** | Validates structure, detects anti-patterns, scores performance |

## Programmatic builder

The `WorkflowForge` provides a fluent Python API:

```python
from scripts.workflow_forge import Workflow

wf = (Workflow("Stripe to Slack")
      .add_webhook_trigger("/stripe-events")
      .add_code_node("Parse Event", '''
          const items = $input.all();
          return items.map(i => ({
              json: { amount: i.json.amount / 100, customer: i.json.customer }
          }));
      ''')
      .add_slack_message("Notify", "#payments",
                         "Payment: ${{ $json.amount }} from {{ $json.customer }}")
      .add_respond_webhook("Ack", status=200)
      .chain_all()
      )

# Export or deploy
wf.save("stripe-to-slack.json")
wf.deploy(activate=True)
```

## Recipe files

Define workflows declaratively in JSON:

```json
{
  "name": "Daily Report",
  "timeout": 120,
  "nodes": [
    {"kind": "schedule", "name": "Every Morning", "field": "hours", "interval": 24},
    {"kind": "http", "name": "Fetch Data", "url": "https://api.example.com/report", "method": "GET"},
    {"kind": "code", "name": "Format", "code": "return $input.all().map(i => ({json: {summary: i.json.title}}));"},
    {"kind": "slack", "name": "Post", "channel": "#reports", "text": "={{ $json.summary }}"}
  ],
  "wiring": "chain"
}
```

```bash
python3 scripts/workflow_forge.py build --recipe daily-report.json --deploy --activate
```

## Validation

The inspector catches issues before they hit production:

- Missing nodes, names, types
- Broken connections (non-existent targets)
- Cycles in the execution graph
- Missing required parameters (URL, path, code)
- Incomplete IF/Switch branches
- Credential hints

```bash
python3 scripts/workflow_inspector.py check --file workflow.json
# Inspection: PASSED  (0 errors, 1 warnings)
# ----------------------------------------------------------
#   [!] CREDS_HINT: [Call API] Node may need credentials after import.
```

## Performance diagnostics

```bash
python3 scripts/workflow_inspector.py diagnose --id 42 --days 14
```

Produces a health score (0-100) with bottleneck detection and
optimization suggestions like parallel branching, caching, batching,
timeout configuration, and sub-workflow splitting.

## CLI cheat sheet

| Command | What it does |
|---------|-------------|
| `n8n_deploy.py ping` | Test API connection |
| `n8n_deploy.py ls` | List all workflows |
| `n8n_deploy.py push --file f.json` | Deploy workflow |
| `n8n_deploy.py on --id 42` | Activate |
| `n8n_deploy.py run --id 42` | Manual trigger |
| `n8n_deploy.py history --id 42` | Recent executions |
| `n8n_deploy.py stats --id 42` | Execution stats |
| `workflow_inspector.py check --file f.json` | Validate |
| `workflow_inspector.py diagnose --id 42` | Full report |
| `workflow_inspector.py optimize --id 42` | Suggestions |
| `workflow_forge.py build --recipe r.json` | Build from recipe |

## Zero dependencies

All scripts use only the Python standard library (`urllib`, `json`, `uuid`).
No `pip install` required. YAML recipe support is optional (install `pyyaml`
if you want `.yaml` recipes; `.json` always works).

## License

Open source, part of the OpenClaw skill ecosystem.

---

**Author:** Dr. FIRAS — [LinkedIn](https://www.linkedin.com/in/doctor-firass/)
