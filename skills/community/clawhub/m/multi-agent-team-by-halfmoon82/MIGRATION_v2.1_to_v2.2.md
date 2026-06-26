# Migration Guide: v2.1 → v2.2

For users who already installed `coding-team-setup@2.1.x`.

## What changed in v2.2

### 1) Mandatory timeout governance for subagent fan-out
v2.2 adds a production guardrail: do **not** run bare `sessions_spawn` fan-out checks in production.

Recommended baseline:
- Simple tasks: 60s, retry 2
- Normal tasks: 120s, retry 3
- Complex tasks: 180s, retry 3

Standard failure classes:
- `SPAWN_REJECTED`
- `TIMEOUT`
- `NO_CHANNEL_503`
- `RATE_LIMIT`
- `UNKNOWN`

### 2) Allowlist guardrail
`allowAgents` must be merged into `main.subagents.allowAgents` with append + dedupe semantics.
Never blindly overwrite.

---

## Upgrade steps (existing v2.1 users)

### Step 0 — Backup config
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d-%H%M%S)
```

### Step 1 — Upgrade skill
```bash
clawhub install coding-team-setup@2.2.0 --force
```

### Step 2 — Validate allowlist wiring
Confirm your team agents are visible:
```bash
openclaw agents list
```
(or from agent tools: `agents_list`)

If missing, re-run setup wizard for that team:
```bash
node ~/.openclaw/workspace/skills/coding-team-setup/wizard/setup.js --team <team-name>
```

### Step 3 — Apply timeout governance in your runbooks
Replace bare fan-out snippets with governed execution wrapper in operational docs/scripts.

Minimum requirement: enforce graded timeout + retries + unified failure reporting.

### Step 4 — Restart gateway after config changes
```bash
openclaw gateway restart
```

### Step 5 — Smoke test
Run one lightweight health-check fan-out and verify report includes:
1. spawn accepted/rejected
2. fallback trace (primary → fallback1 → fallback2)
3. final failure type (+ request id if available)

### Step 6 — One-command self-check (NEW)
Run the following checks as a minimum acceptance gate:

```bash
# 1) allowlist visibility
openclaw agents list

# 2) gateway health
openclaw gateway status

# 3) doctor quick scan
openclaw doctor
```

Pass criteria:
- Target team agents are visible in agent list
- Gateway RPC probe is `ok`
- No blocking session/config integrity errors

Operational note (for runbook owners):
- Health-check report template must always include:
  - spawn status
  - fallback trace
  - final failure class (`SPAWN_REJECTED` / `TIMEOUT` / `NO_CHANNEL_503` / `RATE_LIMIT` / `UNKNOWN`)

---

## Rollback
If needed:
```bash
cp ~/.openclaw/openclaw.json.bak.<timestamp> ~/.openclaw/openclaw.json
openclaw gateway restart
```

---

## FAQ

### Q1: We already had fallback in v2.1. Why v2.2?
A: v2.1 had fallback config, but lacked a mandatory operational governance standard (timeout tiers/retry/circuit-breaker/failure typing) for production fan-out stability.

### Q2: Do I need to recreate all teams?
A: Usually no. Re-run wizard only if allowlist visibility is broken or role/model mappings are outdated.

### Q3: Does this apply to non-coding teams (e.g., wealth)?
A: Yes. The governance model is team-agnostic by design.
