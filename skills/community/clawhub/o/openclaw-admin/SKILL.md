---
name: openclaw-admin
description: Manage and inspect the OpenClaw multi-agent gateway — list agents, check model health, view routing rules, manage crons, inspect context budgets, and run system diagnostics.
---

# OpenClaw Admin — Gateway Management Skill

Use this skill when you need to:
- List or inspect active agents and their models
- Check which Ollama models are running
- View or modify routing rules, crons, or triggers
- Inspect context budget allocations
- Run gateway health diagnostics
- Hot-reload the gateway after config changes

## Config File Locations

| File | Purpose |
|------|---------|
| `../openclaw.json` | Master gateway config (agents, channels, scheduler, tools) |
| `config/ROUTING.json` | Deterministic keyword → agent routing |
| `config/CRONS.json` | Scheduled jobs (heartbeat, reports) |
| `config/TRIGGERS.json` | Webhook-triggered actions |
| `config/CONTEXT_BUDGETS.json` | Token budgets per model |
| `config/agents/*.md` | Agent prompt files |

## Commands

### List All OpenClaw Agents
```bash
cat ../openclaw.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
agents = data.get('agents', {})
print(f'{'ID':<20} {'Role':<35} {'Model':<45} {'Provider':<12} {'Enabled'}')
print('-' * 130)
for aid, a in agents.items():
    enabled = '❌' if a.get('enabled') == False else '✅'
    print(f'{aid:<20} {a.get(\"role\",\"\"):<35} {a.get(\"model\",\"\"):<45} {a.get(\"provider\",\"\"):<12} {enabled}')
print(f'\nTotal: {len(agents)} agents')
"
```

### Check Ollama Models Running
```bash
ollama list 2>/dev/null || echo "Ollama not running"
```

### List Active Crons
```bash
cat config/CRONS.json | python3 -c "
import json, sys
crons = json.load(sys.stdin)
print(f'{'Name':<30} {'Schedule':<20} {'Enabled'}')
print('-' * 60)
for c in crons:
    enabled = '✅' if c.get('enabled', False) else '❌'
    print(f'{c[\"name\"]:<30} {c[\"schedule\"]:<20} {enabled}')
"
```

### List Routing Rules
```bash
cat config/ROUTING.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
routes = data.get('routes', [])
print(f'{'Route':<25} {'Primary Agent':<20} {'Keywords (first 5)'}')
print('-' * 80)
for r in routes:
    name = r.get('name', '')
    primary = r.get('agents', [''])[0] if r.get('agents') else ''
    keywords = ', '.join(r.get('keywords', [])[:5])
    print(f'{name:<25} {primary:<20} {keywords}')
print(f'\nTotal: {len(routes)} routes')
chains = data.get('chains', [])
if chains:
    print(f'\nChains: {len(chains)}')
    for c in chains:
        steps = ' → '.join(c.get('steps', []))
        print(f'  {c[\"name\"]}: {steps}')
"
```

### View Context Budgets
```bash
cat config/CONTEXT_BUDGETS.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
models = data.get('models', {})
print(f'{'Model':<50} {'Window':<12} {'Budget':<10} {'Slot'}')
print('-' * 100)
for m, v in models.items():
    print(f'{m:<50} {v[\"context_window\"]:<12} {v[\"budget\"]:<10} {v.get(\"_slot\",\"\")}')
"
```

### List Active Triggers
```bash
cat config/TRIGGERS.json | python3 -c "
import json, sys
triggers = json.load(sys.stdin)
print(f'{'Name':<25} {'Watch Path':<20} {'Enabled'}')
print('-' * 55)
for t in triggers:
    enabled = '✅' if t.get('enabled', False) else '❌'
    print(f'{t[\"name\"]:<25} {t.get(\"watch_path\",\"\"):<20} {enabled}')
"
```

### Gateway Health Check (Full)
```bash
bash ./status.sh
```

### Check Scheduled Jobs in openclaw.json
```bash
cat ../openclaw.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
jobs = data.get('plugins', {}).get('scheduler', {}).get('jobs', [])
print(f'{'Name':<30} {'Cron':<18} {'Timezone':<18} {'Enabled'}')
print('-' * 80)
for j in jobs:
    enabled = '❌' if j.get('enabled') == False else '✅'
    print(f'{j[\"name\"]:<30} {j[\"cron\"]:<18} {j.get(\"timezone\",\"\"):<18} {enabled}')
print(f'\nTotal: {len(jobs)} scheduled jobs')
"
```

### Quick Agent Count Summary
```bash
echo "=== Agent Ecosystem Summary ==="
echo ""
echo "OpenClaw agents (openclaw.json):"
cat ../openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); a=d['agents']; e=[k for k,v in a.items() if v.get('enabled')!=False]; print(f'  {len(e)} active / {len(a)} total')"
echo ""
echo "Routing agents (ROUTING.json):"
cat config/ROUTING.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'  {len(d.get(\"routes\",[]))} routes, {len(d.get(\"chains\",[]))} chains')"
echo ""
echo "Crons (CRONS.json):"
cat config/CRONS.json | python3 -c "import json,sys; c=json.load(sys.stdin); e=[x for x in c if x.get('enabled')]; print(f'  {len(e)} active / {len(c)} total')"
echo ""
echo "Triggers (TRIGGERS.json):"
cat config/TRIGGERS.json | python3 -c "import json,sys; t=json.load(sys.stdin); e=[x for x in t if x.get('enabled')]; print(f'  {len(e)} active / {len(t)} total')"
echo ""
echo "Ollama models:"
ollama list 2>/dev/null | tail -n +2 | wc -l | xargs -I{} echo "  {} models loaded"
echo ""
echo "Skills:"
ls -d skills/*/ 2>/dev/null | wc -l | xargs -I{} echo "  {} skills installed"
```

## Rules
- Always use `python3 -c` for JSON parsing — never use `jq` (not guaranteed installed).
- All config paths are relative to the `clawdbot/` workspace root.
- `openclaw.json` is one level up at `../../openclaw.json` (relative to skill dir) or `../openclaw.json` (relative to workspace).
- Never modify `openclaw.json` without explicit user approval.
- When reporting agent status, always distinguish between OpenClaw agents and ROUTING.json agents — they are separate systems.
- After any config modification, remind the user to hot-reload: the gateway picks up changes on next request, or restart with `npx thepopebot`.
