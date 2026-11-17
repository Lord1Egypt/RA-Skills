---
name: multi-agent-governor
description: Govern any task that uses or considers multiple agents, subagents, delegation, parallel work, or speed-first execution. Use whenever the user says "多派 Agent", "并行", "省时间", "不用省 token", "many agents", or asks several agents to work or review simultaneously. Convert the request into bounded parallel lanes, route mechanical work to tools/scripts, issue minimal context capsules, enforce agent and QA limits, protect artifact freshness, wait for long-running sessions correctly, and report actual time and token usage.
---

# Multi-Agent Governor

Treat parallelism as an execution budget, not an agent-count target. Optimize for elapsed time and correctness while preventing duplicated work, stale reviews, full-history forks, and unbounded QA loops.

## Hard Limits

- Use at most 3 first-wave agents.
- Use at most 2 final QA agents.
- Use at most 5 agents total and 4 concurrently.
- Use 1 QA wave by default; allow a second only for a verified blocking defect.
- Do not let subagents spawn descendants.
- Keep one integration owner: the main agent.
- Disable full-history inheritance; use `fork_context: false` when the platform supports it.
- Keep each context capsule at or below 6 KB.
- Close completed agents immediately.

User phrases such as "多多多派 Agent" or "不用省 token" raise urgency and evidence coverage. They do not override these limits.

## Choose the Execution Primitive

Before spawning, classify every work item:

| Work item | Execute with |
|---|---|
| Independent expert judgment or bounded writing | Agent |
| File reads, searches, API calls, shell commands | Approved parallel/batch tool calls |
| Counting, hashing, schema checks, formulas, overflow, string scans | Deterministic script |
| Critical path, conflict resolution, final edits | Main agent |

Do not use agents merely to parallelize I/O. If fewer than 2 independent reasoning lanes exist, keep the task local or use only 1 sidecar agent even when the user asks for many.

Read [references/orchestration-policy.md](references/orchestration-policy.md) when decomposition or model routing is non-obvious.

## Run Protocol

### 1. Define the run

Identify:

- concrete objective and newest user instruction;
- immutable source files and their hashes;
- critical path owned by the main agent;
- independent lanes with disjoint ownership;
- deterministic acceptance tests;
- user deadline and quality posture.

Create a manifest:

```bash
python3 scripts/init_run.py \
  --objective "<objective>" \
  --source /absolute/path/to/input \
  --mode fast-deep \
  --deadline-minutes 90
```

Use `--main-thread-id` when the current platform exposes a stable thread id. Store temporary run state under `/tmp/multi-agent-runs/`; do not place it beside user deliverables.

### 2. Build minimal capsules

Create one capsule per independent lane:

```bash
python3 scripts/add_capsule.py \
  --manifest /tmp/multi-agent-runs/<run-id>/run-manifest.json \
  --lane-id evidence-qa \
  --role explorer \
  --objective "Verify financing and source claims" \
  --input /absolute/path/to/workbook.xlsx \
  --deliverable "Structured findings only" \
  --acceptance "Every finding includes file/sheet/range evidence" \
  --exclusion "Do not edit source files"
```

Pass the capsule path and necessary file paths to the agent. Do not paste the long conversation, entire file contents, intended conclusion, or another agent's diagnosis. See [references/agent-contracts.md](references/agent-contracts.md).

### 3. Execute wave one

- Spawn only the lanes that can proceed independently.
- Keep urgent blocking work local instead of delegating it and waiting.
- Assign disjoint file or responsibility ownership.
- Continue meaningful main-agent work immediately after spawning.
- Reuse an existing agent only when the new task depends on its prior local context.
- Register agent ids with `scripts/update_run.py agent-start`.

When a command returns a session id, register it and poll that exact session until `exit_code` is present. Never rerun a command merely because the first call returned no output.

### 4. Integrate once

The main agent reviews findings, resolves conflicts, and writes the integrated artifact once. Agents must not concurrently edit the same deliverable.

Register the integrated build and hashes:

```bash
python3 scripts/update_run.py build \
  --manifest /tmp/multi-agent-runs/<run-id>/run-manifest.json \
  --artifact /absolute/path/to/output
```

### 5. Run deterministic gates first

Run format, schema, test, count, hash, formula, overflow, link, and prohibited-language checks before asking agents to review. Domain skills supply their own gates.

Then verify build freshness:

```bash
python3 scripts/check_freshness.py \
  --manifest /tmp/multi-agent-runs/<run-id>/run-manifest.json \
  --include-sources
```

### 6. Run one QA wave

Use no more than 2 non-overlapping QA lenses, such as:

- factual/data consistency;
- visual/narrative/user-perspective quality.

Every QA capsule must include the current `build_id` and artifact hashes. Do not edit artifacts while QA is running. Discard a result if freshness fails. Fix verified blockers in one batch. Do not spawn another broad review wave for cosmetic suggestions.

Read [references/quality-gates.md](references/quality-gates.md) for severity and stop rules.

### 7. Close and report

- Close every agent as soon as its result is integrated.
- Confirm every registered command session has an exit code.
- Mark the run complete only after acceptance tests pass.
- Collect elapsed time and usage from the platform's native telemetry when available. When running inside Codex, the bundled adapter can read local thread metrics:

```bash
python3 scripts/collect_usage.py \
  --manifest /tmp/multi-agent-runs/<run-id>/run-manifest.json \
  --write
```

- Report gross tokens, cached input, fresh non-cached input plus output, agent count, and wall time when the platform exposes them. Never fabricate unavailable metrics.

## Stop Conditions

Stop when all deterministic acceptance tests pass and no blocking QA finding remains. Do not continue because another reviewer might produce a different preference.

Escalate to the user before exceeding 5 agents, starting a second QA wave, changing frozen source files, or resolving a genuine product/business judgment that cannot be inferred safely.

## Failure Prevention

- Do not accept reviews without matching build hashes.
- Do not mix findings produced against different artifact versions.
- Do not ask multiple agents the same broad question.
- Do not use a high-reasoning model for mechanical verification.
- Do not mark a run complete while agents or command sessions remain active.
- Do not treat cached-token volume as fresh-token consumption; report both.
