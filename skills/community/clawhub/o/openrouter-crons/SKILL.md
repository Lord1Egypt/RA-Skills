---
name: openrouter-crons
description: Collaboratively migrate specific OpenClaw cron jobs onto popular OpenRouter models. Audit cron usage, fetch the current OpenRouter rankings via curl, propose top 4 cheap models, edit the chosen crons, and verify by running them plus checking OpenRouter usage.
---

# OpenRouter Cron Migration & Verification Skill

You are the OpenClaw/OpenRouter tuning partner. Work with the user to decide which cron jobs should move to cheaper OpenRouter models, based on **actual cron usage** and the current **OpenRouter popularity rankings**. You do not auto-migrate everything—only the crons the user approves. Every change must be verified (config + live run + cost check).

**Key references**
- OpenClaw cron CLI: https://docs.openclaw.ai/cli/cron
- OpenClaw cron concepts: https://docs.openclaw.ai/automation/cron-jobs
- OpenClaw ↔ OpenRouter integration: https://openrouter.ai/docs/guides/coding-agents/openclaw-integration
- OpenRouter rankings API (curl-able): https://openrouter.ai/api/v1/models?orderby=rank

---

## Collaboration principles
1. **Check first:** confirm the gateway is up and the user has (or can supply) an OpenRouter key.
2. **Usage-driven decisions:** gather run history so the user can prioritize expensive/high-frequency jobs.
3. **Live popularity data:** always pull the latest ranking data before recommending models. Assume yesterday’s advice is stale.
4. **Offer options:** provide at least two (ideally 3–4) popular, inexpensive models from the ranking output and explain trade-offs.
5. **Explicit approval:** document which cron → model mappings the user approved before editing.
6. **Verification:** after each change, show the updated cron payload, re-list crons, run the cron, and surface any errors.
7. **Cost awareness:** optionally check OpenRouter credits/activity so the user sees the impact.

---

## Phase 0: Make sure OpenClaw is reachable

1. `openclaw status` → ensure the gateway isn’t “unreachable”. If it is, guide the user to run `openclaw gateway install && openclaw gateway run` (or `launchctl bootstrap …`).
2. Quick health ping: `openclaw cron status` should return without connection errors before proceeding.

If the gateway stays down, stop and help fix it before touching cron jobs.

---

## Phase 1: Confirm OpenRouter provider access

### Step 1.1: Check provider + credentials
```bash
openclaw providers list 2>/dev/null | rg -i openrouter || echo "OpenRouter provider missing"
grep -i OPENROUTER ~/.openclaw/.env 2>/dev/null || echo "No OPENROUTER_API_KEY in .env"
cat ~/.openclaw/agents/main/agent/auth-profiles.json 2>/dev/null | rg -i openrouter || echo "No OpenRouter auth profile"
```
Summarize what you found. If no key is set, ask the user for their OpenRouter API key.

### Step 1.2: Onboard (if needed)
```bash
openclaw onboard --auth-choice apiKey --token-provider openrouter --token "$OPENROUTER_API_KEY"
```
Fallback: edit `~/.openclaw/openclaw.json` or set the env var manually, per the OpenRouter integration doc.

### Step 1.3: Verification
```bash
openclaw providers list | rg -i openrouter
curl -s https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  | python3 -m json.tool | head -20 || echo "OpenRouter API call failed"
```
If the API call fails, stop and resolve authentication before migrating any cron.

---

## Phase 2: Usage-based cron triage

Goal: help the user pick which jobs to move by showing frequency, success rate, and current model.

### Step 2.1: Inventory crons
```bash
openclaw cron list --json 2>/dev/null | python3 - <<'PY'
import json, sys
raw = sys.stdin.read()
start = raw.find('[') if '[' in raw else raw.find('{')
data = json.loads(raw[start:])
jobs = data if isinstance(data, list) else [data]
print(f"{'Job ID':<12}{'Name':<28}{'Schedule':<16}{'Session':<12}{'Model':<45}")
print('-'*115)
for job in jobs:
    schedule = job.get('schedule', {})
    freq = schedule.get('cron') or schedule.get('expr') or schedule.get('everyMs') or schedule.get('at') or 'unknown'
    model = job.get('payload', {}).get('model', 'agent default')
    session = job.get('session', {}).get('kind', '?')
    print(f"{job.get('id','?'):<12}{job.get('name','?'):<28}{freq:<16}{session:<12}{model:<45}")
PY
```
Ask the user which of these look expensive or redundant.

### Step 2.2: Pull run history for candidates
For each interesting job:
```bash
openclaw cron runs <JOB_ID> --limit 25 --json 2>/dev/null | python3 - <<'PY'
import json, sys
from datetime import datetime
runs = [json.loads(line) for line in sys.stdin if line.strip()]
if not runs:
    print('No runs logged.'); exit()
success = sum(1 for r in runs if r.get('status') == 'success')
print(f"Runs analyzed: {len(runs)} · Success: {success}/{len(runs)}")
latencies = [r.get('durationMs', 0) for r in runs if r.get('durationMs')]
if latencies:
    avg = sum(latencies)/len(latencies)
    print(f"Avg duration: {avg/1000:.1f}s · Max: {max(latencies)/1000:.1f}s")
print('Most recent prompts/models:')
for r in runs[:3]:
    print(f"- {datetime.fromisoformat(r['createdAt']).isoformat()} · model={r.get('model','default')} · status={r.get('status')}")
PY
```
Discuss with the user which jobs run often enough (or cost enough) to justify moving to a cheaper model.

Record the agreed list: `job_id -> desired outcome` (e.g., “job foo: migrate to cheaper general model”).

---

## Phase 3: Pick popular, inexpensive OpenRouter models

### Step 3.1: Fetch live rankings (curl only)
```bash
curl -s 'https://openrouter.ai/api/v1/models?orderby=rank' \
  | python3 - <<'PY'
import json, sys
rows = json.load(sys.stdin).get('data', [])
print(f"{'Rank':<5}{'Model ID':<42}{'Provider':<14}{'Context':>8}{'In $/M':>10}{'Out $/M':>10}")
print('-'*100)
for idx, row in enumerate(rows[:20], start=1):
    pricing = row.get('pricing', {})
    prompt = float(pricing.get('prompt','0') or 0)*1_000_000
    completion = float(pricing.get('completion','0') or 0)*1_000_000
    provider = row['id'].split('/',1)[0]
    print(f"{idx:<5}{row['id']:<42}{provider:<14}{row.get('context_length',0):>8}{prompt:>10.2f}{completion:>10.2f}")
PY
```
This gives you the current popularity order plus price info. Note which of the **top ~10** are cheap and suitable (e.g., DeepSeek V3.x, Gemini Flash, GPT-4o mini, Xiaomi MiMo).

### Step 3.2: Offer at least three concrete options
For each cron the user wants to migrate:
- Pair its workload (prompt complexity, tool use, latency requirements) with **3–4 models** from the ranking table, prioritizing lower cost.
- Example script snippet to highlight the top four cheapest popular models:
```bash
curl -s 'https://openrouter.ai/api/v1/models?orderby=rank' \
  | python3 - <<'PY'
import json, sys
rows = json.load(sys.stdin).get('data', [])
choices = []
for row in rows:
    pricing = row.get('pricing', {})
    prompt = float(pricing.get('prompt','0') or 0)
    completion = float(pricing.get('completion','0') or 0)
    if prompt == 0 or completion == 0:
        continue
    if prompt*1_000_000 > 1.00:  # skip expensive (> $1/M input) options
        continue
    choices.append((prompt, {
        'id': row['id'],
        'name': row.get('name', row['id']),
        'ctx': row.get('context_length', 0),
        'out': completion
    }))
choices.sort()
print('Top cheap popular models:')
for prompt, info in choices[:4]:
    print(f"- {info['id']} · {info['name']} · ctx {info['ctx']} · ${prompt*1_000_000:.2f}/M in · ${info['out']*1_000_000:.2f}/M out")
PY
```
Explain why each candidate fits (e.g., “DeepSeek V3.2 ranks #8, great for summaries, ~\$0.26/M in”). Ask the user to choose which model each cron should use.

### Step 3.3: Finalize migration plan
Write down the explicit approvals, e.g.:
- `daily-news-digest` → `openrouter/deepseek/deepseek-v3.2`
- `rss-monitor` → `openrouter/google/gemini-2.5-flash-lite`

You’ll use this plan in the next phase.

---

## Phase 4: Apply edits + verify immediately

For each approved cron:

1. **Edit the model**
   ```bash
   openclaw cron edit <JOB_ID> --model "openrouter/<provider>/<model>"
   ```
2. **Show the updated payload**
   ```bash
   openclaw cron show <JOB_ID> --json | rg -i model
   ```
3. **Re-list crons** (optional summary table reuse from Phase 2) to confirm the new model appears.
4. **Run the cron manually**
   ```bash
   openclaw cron run <JOB_ID> --expect-final --timeout 180000
   ```
   Review output carefully. If the cheaper model fails or quality drops, tell the user and offer to revert (`openclaw cron edit <JOB_ID> --model "<previous>"`).
5. **Log the result**: job name, old → new model, run status, observations.

Repeat for every cron in the plan.

---

## Phase 5: Optional — monitor OpenRouter spend

If the user wants visibility into cost impact:

1. **Credits/balance**
   ```bash
   curl -s https://openrouter.ai/api/v1/credits \
     -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -m json.tool
   ```
2. **Daily activity**
   ```bash
   DATE=$(date +%Y-%m-%d)
   curl -s "https://openrouter.ai/api/v1/activity?date=$DATE" \
     -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     | python3 - <<'PY'
import json, sys
rows = json.load(sys.stdin).get('data', [])
if not rows:
    print('No activity for this date.'); exit()
print(f"{'Model':<45}{'Cost($)':<10}{'Requests':<10}{'Tokens':<14}")
print('-'*80)
for row in rows:
    tokens = (row.get('prompt_tokens',0) or 0) + (row.get('completion_tokens',0) or 0)
    print(f"{row.get('model','?'):<45}{row.get('usage',0):<10.4f}{row.get('requests',0):<10}{tokens:<14}")
PY
   ```
3. Share the results and note any anomalies (spikes, zero usage, etc.).

---

## Quick reference
- `openclaw status` — confirm gateway reachability
- `openclaw providers list` — ensure OpenRouter provider loaded
- `curl -s https://openrouter.ai/api/v1/models?orderby=rank` — live popularity + price data
- `openclaw cron list --json` — cron inventory
- `openclaw cron runs <JOB_ID> --limit 25 --json` — usage history
- `openclaw cron edit <JOB_ID> --model "openrouter/..."` — set per-cron models
- `openclaw cron run <JOB_ID> --expect-final` — verification run
- `curl -s https://openrouter.ai/api/v1/credits` — balance check
- `curl -s https://openrouter.ai/api/v1/activity?date=YYYY-MM-DD` — per-day usage

Stay collaborative, data-driven, and explicit about every change.
