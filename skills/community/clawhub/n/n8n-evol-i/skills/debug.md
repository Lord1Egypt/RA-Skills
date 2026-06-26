---
description: Investigate a failing or missing n8n workflow execution — from vague symptom to root-cause with evidence.
---

# debug

## When

A workflow's behavior in production is wrong: vague ("I didn't get the email") or pinpointed ("workflow Y errored at 2pm"). Use this skill to investigate the actual cause from execution data, not from inference.

This is the read-only investigation loop. No write operations (`manage_variables`, `stop_executions`, redeploys) until the user has approved the recommended next step in Step 8.

## Inputs (ask if not provided)

- `env` — which environment? (`dev` / `staging` / `prod`)
- `time_window` — date + timezone. Always ask if relative ("around 2pm"). Convert to ISO 8601 UTC before any helper call.
- `symptom` — concrete: "no email in inbox," "report shows 2025 data," "workflow page shows red." If the user named a specific workflow, capture both the user's wording AND a reframed Q1 ("user said X failed but actually Y didn't produce data") so Step 3b's causal-linkage check can falsify a wrong attribution.

The full 8-step investigation rubric — including the three non-negotiable framing rules (existence ≠ causality, don't stop at the first issue, don't guess), the causal-linkage check (Step 3b), the trigger health check (Step 5b, mandatory if no executions found), the time-correlation step (Step 6, mandatory if >1 workflow failing in window), and the sub-agent cross-check (Step 7) — lives in [`skills/patterns/investigation-discipline.md`](patterns/investigation-discipline.md). Read it before invoking any helper.

## Helpers

```bash
# Step 1: dependency graph
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/dependency_graph.py --env <env> --source both

# Step 1.5: 7-day baseline (chronic vs acute, hung counts)
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/list_executions.py --env <env> --started-after <ISO-UTC> --tally

# Step 2: candidate prescreen (keyed)
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/list_executions.py --env <env> --workflow-key <key> \
  --started-after <ISO-UTC> --started-before <ISO-UTC> --limit 100

# Step 3: execution detail
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/inspect_execution.py --env <env> --execution-id <id> \
  [--include-data] [--max-size-kb 50] [--no-truncate]

# Step 6: time-correlation across workflows
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/list_executions.py --env <env> \
  --started-after <T-5min> --started-before <T+5min> --status error --limit 500
```

## See also

- [`skills/patterns/investigation-discipline.md`](patterns/investigation-discipline.md) — the load-bearing 8-step rubric this skill executes.
- [`skills/patterns/agent-api-discipline.md`](patterns/agent-api-discipline.md) — verify `/executions`, `/executions/{id}`, `/executions/stop` shapes via Context7 before invoking.
- [`skills/run.md`](run.md) — for active reproduction once the cause is hypothesized (after user approves a next step).
