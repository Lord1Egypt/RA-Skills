---
name: osop-review
description: Review .osop/.osoplog for security risks, permission gaps, and destructive commands
version: 1.2.0
emoji: "\U0001F6E1\uFE0F"
homepage: https://osop.ai
argument-hint: <path-to-osop-or-osoplog-file>
metadata:
  openclaw:
    requires:
      bins:
        - bash
      config:
        - ~/.osop/config.yaml
    install: []
    always: false
user-invocable: true
disable-model-invocation: false
---

# OSOP Workflow Reviewer

Review a workflow or execution log for risks and issues.

## Target file

$ARGUMENTS

## What to do

1. **Read the file** specified in the argument (`.osop` or `.osoplog.yaml`)

2. **Analyze for risks** — check each node for:
   - `security.risk_level: high|critical` without preceding `approval_gate`
   - `security.permissions` containing broad patterns (`write:*`, `admin:*`, `delete:*`)
   - `cli` nodes with destructive commands (`rm -rf`, `kubectl delete`, `terraform destroy`, `DROP TABLE`)
   - Hardcoded secrets (strings starting with `sk-`, `ghp_`, `xoxb-`, API keys)
   - Agent nodes without `cost.estimated` (unbounded cost exposure)
   - Missing `timeout_sec` on external call nodes (`api`, `cli`, `agent`, `infra`, `mcp`)
   - Missing error handling (no `fallback`/`error` edge) on medium+ risk nodes

3. **Compute risk score** (0-100):
   - Each node: `type_weight * risk_multiplier * mitigation_factor`
   - Type weights: cli=2, infra=2, db=1.5, agent=1.5, docker=1.5, cicd=1.5, api=1, others=0.5-1
   - Risk multiplier: low=1, medium=2, high=4, critical=8
   - Mitigations: approval_gate=-50%, retry_policy=-10%, fallback_edge=-20%
   - Finding penalty: low=+2, medium=+5, high=+10, critical=+20

4. **Present findings** in a clear table:
   ```
   Risk Score: XX/100 — VERDICT (safe/caution/warning/danger)

   | Severity | Finding | Node | Suggestion |
   |----------|---------|------|------------|
   | CRITICAL | ... | ... | ... |
   ```

5. **Summarize**:
   - Total permissions required
   - Secrets referenced
   - Estimated cost (if any)
   - Whether approval gates exist
   - Final verdict: is this safe to run?

## For .osoplog files

If reviewing an execution log, also check:
- Which tools were actually used and how many calls
- Whether any nodes failed and why
- AI reasoning decisions — were they sound?
- Sub-agent hierarchy — was the spawning appropriate?
- Total execution time and cost
