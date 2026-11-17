---
name: jev-gate
description: Ask a hosted judge before risky agent actions. Returns approve, hold, or escalate with a confidence number and the rule that fired, and keeps a reviewable decision log. Use before deleting data, spending money, touching production, or messaging customers.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - JEV_GATE_KEY
      bins:
        - curl
        - python3
    primaryEnv: JEV_GATE_KEY
    envVars:
      - name: JEV_GATE_KEY
        required: true
        description: API key from https://jev-gate.fly.dev (14-day free trial, card required, not charged during the trial).
      - name: JEV_GATE_URL
        required: false
        description: Override the gate base URL. Defaults to https://jev-gate.fly.dev.
    homepage: https://jev-gate.fly.dev
    emoji: "🚦"
---

# jev-gate — ask before you act

Run this **before** an action you would not want to take unsupervised: deleting or
overwriting data, moving money, touching production, messaging a customer, changing
credentials. The gate answers with a verdict, a confidence number, and the rule that
fired — and keeps the decision in a log a human can review later.

## Setup (once)

1. Get a key at https://jev-gate.fly.dev — 14-day free trial, card required and not
   charged during the trial; cancel any time in the billing portal.
2. Export it:

```bash
export JEV_GATE_KEY=jgate_...
```

That is the whole install: one key, one HTTPS call. No package, no dependencies
beyond `curl`.

## Check an action

```bash
scripts/jev-gate-check "about to delete 1,204 rows from the staging events table"
```

Exit codes, which is all an agent needs:

| code | verdict | what to do |
|---|---|---|
| 0 | approve | continue with the action |
| 2 | hold | **pause** this action and queue it for routine human review; do not retry |
| 3 | escalate | **stop**, tell the user a human decision is required |
| 1 | error | the gate could not answer — treat as blocked, never guess |

The raw call, if you would rather do it yourself:

```bash
curl -s https://jev-gate.fly.dev/v1/gate \
  -H "Authorization: Bearer $JEV_GATE_KEY" \
  -H 'content-type: application/json' \
  -d '{"transcript":"agent is about to drop the orders table in production","tool_calls":["psql drop"]}'
```

```json
{
  "action": "escalate",
  "confidence": 0.38,
  "violation": 0.71, "needs_human": 0.72, "risk": 2.4,
  "reasons": ["risk 2.40 ≥ 2.00", "needs_human 0.72 > 0.60"],
  "latency_ms": 474
}
```

Branch on `action` — never on the prose. `reasons` is the rule that fired, and it is what
makes the decision explainable to the human who reviews it.

## Reading the log

Every call lands in the account's dashboard at https://jev-gate.fly.dev/dashboard with the
transcript, the verdict, the reasons, and the latency. There you can tune the four
thresholds it branches on (`approve if confidence ≥`, `hold if violation >`,
`escalate if needs_human >`, `escalate if risk ≥`), work the review queue for the muddy
middle, and export CSV/JSON. Reviews are closeable: mark reviewed, annotate, reopen.

## Going further

- **MCP**: `curl -sO https://jev-gate.fly.dev/client/jev_gate_mcp.py`, then point your MCP
  config at that file — the gate becomes a `check_action` tool.
- **Python, any framework**: `from jev_gate_mcp import guarded` wraps your tool dispatcher so
  held and escalated calls raise before the side effect.
- **Claude Code**: `curl -sO https://jev-gate.fly.dev/client/claude_code_hook.py` and wire it
  as a `PreToolUse` hook; exit 2 blocks the call.
- All client files: https://jev-gate.fly.dev/client

## Rules of thumb

- Gate the action, not the thought: pass what is about to happen and the context behind it.
- A `hold` is not a failure — it is the product working. Queue it and keep moving.
- If the gate is unreachable, block. A firewall that guesses is not a firewall.
