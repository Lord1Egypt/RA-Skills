---
name: pattern-investigation-discipline
description: 8-step rubric for investigating a failing or missing n8n workflow execution. Causal-linkage check, trigger health check, time-correlation, sub-agent cross-check, structured report. Read-only loop until Step 8.
user-invocable: false
---

# Pattern: investigation-discipline

This pattern is the load-bearing playbook for [`skills/debug.md`](../debug.md). It's deliberately separated because the rubric is long (≈250 lines) and the skill markdown stays terse so the agent can route to it from a vague symptom in one read.

The investigation is **read-only** until Step 8 has been delivered to the user and the user has approved the recommended next step. No `manage_variables`, no `stop_executions`, no redeploys during the loop.

## Three non-negotiable framing rules

These are the framing the agent applies at every step — they come BEFORE the step-by-step flow.

**Rule 1 — Existence ≠ causality.** Every fetched execution must pass the causal-linkage check (Step 3b) before it counts as evidence. `status=success` is the most dangerous case to skim past — n8n marks an execution `success` when it completes without throwing, NOT when the side-effect happened. An If node that bypassed the email-sending node leaves `status=success` on an execution that did NOT send the email.

**Rule 2 — Don't stop at the first issue.** A failed execution might be symptom, not cause. After identifying a candidate, look for upstream failures, related sub-workflows, and time-correlated incidents (Step 6 is mandatory when >1 workflow fails in the window) before closing.

**Rule 3 — Don't guess.** Every claim in the report must be backed by execution data, not inference. Label hypotheses as such until confirmed. If you find yourself writing "probably" in the report, you owe more data — go back to Step 3 with `--include-data`, or escalate to Step 7.

## Investigation flow

### Step 0 — API verification (always first, ~30 seconds)

Drift between training-data assumptions and the live API is the most common silent-failure mode. Verify before invoking:

```
mcp__context7__query-docs
  libraryId: "/n8n-io/n8n-docs"
  query: "GET /api/v1/executions parameters cursor nextCursor pagination response shape"
```

If shapes have drifted, flag and adapt. If Context7 is unavailable, note "API verification skipped" in the final report and proceed.

→ Proceed to Step 1.

### Step 1 — Build the dependency graph

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/dependency_graph.py --env <env> --source both
```

`--source both` reads workspace templates AND live `GET /workflows`. Three adjacency outputs:

- `calls` — Execute Workflow edges (caller → target).
- `error_handlers` — `settings.errorWorkflow` plus `common.yml.error_source_to_handler` pairings.
- `credential_groups` — credential id → list of workflows referencing it.

→ Proceed to Step 1.5.
→ If no candidates identifiable from the symptom: use `n8n_client.list_workflows()` to search by name, then return.

### Step 1.5 — Baseline (chronic vs acute, plus saturation)

A 7-day baseline frames every other step. Walk every page of `/executions` across every in-scope workflow and tally statuses while iterating — single source of truth, no two-call drift:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/list_executions.py --env <env> --started-after <7-days-ago-ISO> --tally
```

`--tally` walks all pages (ignores `--limit`) and emits a status histogram plus three derived signals:

- `failure_rate = error_count / total_count`. Sustained `>10%` → chronic, look for structural flaws. `~0%` until incident → acute, look for a specific recent change.
- `crash_count` — non-zero suggests worker instability or OOM; surfaces in trigger health (Step 5b).
- `hung_count = waiting_count + queued_count + (running_count_started_>1h_ago)`. Non-zero means queue saturation or runaway loops. **A "healthy" `failure_rate` with high `hung_count` is the runaway-loop / lock-contention signature** — investigation must NOT close on `failure_rate ≈ 0%` alone.

If `total_count < 20`: mark baseline `insufficient-data` and skip the chronic/acute label (avoids noisy ratios on cold workflows).

→ Proceed to Step 2 with framing noted (chronic / acute / insufficient-data + hung/crash signals).
→ Skip Step 1.5 if user provided an execution id directly.

### Step 2 — Pre-screen candidates (≤ 7 before Step 3)

Two paths depending on whether the user named a specific workflow.

**Path A — keyed symptom** (user said "workflow Y failed"):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/list_executions.py \
  --env <env> --workflow-key <key> \
  --started-after "ISO-UTC" --started-before "ISO-UTC" \
  --limit 100
```

**Path B — keyless symptom** (user said "alerts silent" / "everything's slow" / "data didn't update"):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/list_executions.py \
  --env <env> \
  --started-after "ISO-UTC" --started-before "ISO-UTC" \
  --limit 500
```

Cluster results by `workflowId`. Use Step 1's dependency graph to filter candidates whose nodes plausibly produce the symptom (e.g., for "no email" → workflows containing email-sending nodes; for "everything's slow" → workflows with `status=waiting`/`running` started long ago, or whose Wait nodes hold locks). If the keyless query returns zero distinct workflows but baseline `hung_count > 0` (Step 1.5), the symptom is likely lock/queue saturation — surface this as a candidate cluster.

**Stable rank** (Path A or Path B):

Sort by composite key: `(status==error desc, abs(startedAt - symptom_time_center) asc, retryOf is null desc, executionId desc)`. Take top 7. Ties broken by `executionId` descending (newest first).

If `>7` candidates all match `status=error` and the same workflow_key, the cap may discard the explanatory candidate. **Tiebreaker escalation**: take top 7 OR all `status=error` with `retryOf is null` for the keyed workflow, whichever is larger.

→ No executions in window: go to Step 5b (trigger health).
→ All `status=success` (Path A): proceed to Step 3 with `--include-data` mandatory.
→ ≤ 7 ranked candidates: proceed to Step 3.
→ Path B with no clear cluster + baseline `hung_count > 0`: proceed to Step 3 on the longest-running execution as primary candidate (lock-holder hypothesis).

### Step 3 — Get execution detail

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/inspect_execution.py \
  --env <env> --execution-id <id> \
  [--include-data] [--max-size-kb 50] [--no-truncate]
```

`--include-data` is mandatory for `status=success` (because the surface-level "success" is a lie until you verify the side-effect node ran); recommended for `status=error` if the list-level error message isn't specific enough.

→ Proceed to Step 3b.
→ If `retryOf` is set: run Step 3 on the original execution first, then the retry.

### Step 3b — Causal-linkage check (mandatory; cannot skip)

Write this block, verbatim, for every Step-3 execution:

```
### Causal-linkage check — execution <id>
- Q1 (symptom): <user's concrete symptom — verbatim AND reframed if user mis-named the workflow>
- Q2 (execution): <status, nodes ran, terminal node return>
- Q2b (branches): <If/Switch nodes hit; branch taken; condition value that triggered it; nodes BYPASSED>
- Q3 (does Q2+Q2b explain Q1?): yes / no / unclear — evidence: <node output, branch condition, bypassed-node names, value>
- Q4 (verdict): match / non-match / continue searching
```

**Why Q2b matters**: `status=success` failure modes hinge on a branching node bypassing the side-effect. Without Q2b, an agent reading only Q2's "terminal node return" can mark a side-effect-skipped success as `match` and close prematurely.

**Truncation escalation**: if Q4=unclear on a `status=success` execution AND the helper printed a truncation warning to stderr ("TRUNCATED — pass --no-truncate for full payload"), re-run Step 3 with `--no-truncate` BEFORE marking as non-match. The truncated tail is exactly where the bypassed-side-effect evidence often lives.

Q4=non-match: discard, do NOT include in findings. Q4=match: proceed to Step 4. Q4=unclear: next candidate (after truncation escalation if applicable).

### Step 4 — Upstream / downstream recursion

If the confirmed execution calls a sub-workflow: extract child execution id, repeat Steps 2–3b on the child. Recursion stops at: non-success confirmed, depth 5, or leaf reached. Note depth limit in the report if hit.

If an error handler is registered (per Step 1's `error_handlers` map): check the handler's executions in the same window.

→ If sub-workflow OR error handler involved: complete the recursion / handler check, then proceed to Step 5b.
→ Otherwise (leaf workflow, no sub-call, no handler): proceed to Step 5b directly.

### Step 5 — Widen or redirect (reachable from Step 5b "trigger looks healthy but symptom unexplained")

No executions in window AND Step 5b found trigger healthy → double the time window, re-run Step 2.

All Step 3b candidates cleared (symptom unexplained) → re-examine Step 1's graph for symptom-relevant nodes in OTHER workflows. **Crucial**: the `dependency_graph` only models `executeWorkflow` and credential-sharing edges. Producer-consumer dependencies via shared DB tables, file drops, queue messages, or shared Redis/variable keys are INVISIBLE to the graph. If the symptom's data flow goes through such an external state store, manually identify candidate producers by their node types (Postgres write, S3 put, Queue publish) and re-enter Step 2 with each as the candidate.

If the user-named workflow's `status=success` and Q3 cleared with the reframed Q1 ("user said X failed but actually Y didn't produce data"): re-enter Step 2 with the producer workflow as the keyed candidate.

→ Proceed to Step 6.

### Step 5b — Trigger health check (mandatory if Step 2 found no executions; also recommended on unexplained `success` symptoms)

The most common cause for "I didn't get X" is the trigger never fired. Via `n8n_client.get_workflow(wf_id)`:

- `active` field — `false` = trigger never fires; this is the answer.
- Schedule trigger: print `cronExpression` / `rule` and ASK the user to confirm it matches their expectation. The agent has no oracle for "correct."
- Webhook: print the webhook URL and check it against `--env`'s `n8n.instanceName` — flag if mismatch (e.g., webhook points at `*.staging.example.com` while `--env prod`).
- `settings.errorWorkflow` — handler registered? cross-check against `dependency_graph`'s `error_handlers` map.
- Compare `last successful execution timestamp` to baseline expectations from Step 1.5. Gap > 2× expected interval = missed trigger.

→ If trigger issue found AND Step 2 had no executions: jump to Step 8 — report the trigger issue as HIGH finding, recommend fix. No need for Steps 6 / 7 (the trigger issue IS the cause; widening or correlating won't add evidence).
→ If trigger looks healthy AND Step 2 had no executions: jump to Step 5 (widen window).
→ Otherwise: proceed to Step 6.

### Step 6 — Time-correlate across workflows (precondition: count distinct failing workflows in window first)

Before invoking, count the distinct workflows that failed in the symptom window. If Step 2 was Path A (keyed), run an env-scoped error-only fetch:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/helpers/list_executions.py --env <env> \
  --started-after <T-5min> --started-before <T+5min> \
  --status error --limit 500
```

If Step 2 was Path B, this data is already in hand from the keyless fetch — filter for `status=error` and group by `workflowId`.

Anchor `T` is: the user's reported symptom time if specified; else the Step 1.5 baseline window's end; else `now`. Window default ±5min, but expand to ±15min if `failure_rate` baseline is acute (sudden change) — slow-rolling deploys can stretch the failure cluster beyond 5 minutes.

**Mandatory if the count is >1 distinct workflow.** Skip if only one workflow appears.

Cross-check Step 1's graph: connected via `calls` OR `credential_groups` → shared cause likely. Unrelated → coincidence; correlation, not causation. Note: external-state coupling (DB / queue / shared variable) is invisible to the graph (per Step 5 caveat); flag this in the report rather than asserting independence.

→ Proceed to Step 6b.

### Step 6b — Blast-radius enumeration

After root cause is confirmed:

- **Credential failure**: list all workflows in `dependency_graph`'s `credential_groups` sharing the credential id. Filter to those with executions in the symptom window (intersect with Step 6's env-scoped fetch). Surface "currently-running executions from those" as a separate count via `list_executions --status running`.
- **Sub-workflow failure**: list all callers from the `calls` adjacency list.
- **Lock contention** — DEFERRED. v2.1 drops this bullet because no helper currently surfaces lock-scope membership. Lock-wrapping is encoded at template-edit time in `add_lock_to_workflow.py`, not in any list endpoint. If lock contention is suspected (Step 1.5 `hung_count > 0`, queue saturation), recommend the user inspect `skills/patterns/locking.md` and the workflows using the `lock_acquisition` primitive — the agent should NOT attempt to enumerate lock blast radius programmatically. A future helper (`dependency_graph --include-locks`) could close this gap; out of scope for now.

Include affected scope in the report's "Blast radius" section.

→ Proceed to Step 7 if competing hypotheses remain. Otherwise Step 8.

### Step 7 — Cross-check hypothesis (sub-agent)

**MUST spawn** at:

- (a) Two competing hypotheses, neither falsified by data.
- (b) Plausible hypothesis but execution data ambiguous.
- (c) Conclusion formed early and not re-examined since new data arrived.

Invocation:

```
Tool: Agent
subagent_type: "general-purpose"
prompt: <see template below>
```

Prompt template:

```
You are a fresh-eyes analyst with no prior context on this investigation.

Given the following evidence, what is the most likely cause of the reported
symptom? Show your reasoning step by step. Do not assume any prior hypothesis
is correct.

SYMPTOM (verbatim from user):
<symptom>

DEPENDENCY GRAPH:
<dependency_graph output, verbatim>

EXECUTION RECORDS (redacted of secrets):
<JSON from inspect_execution.py, verbatim>

EVIDENCE GATHERED (Q1, Q2, Q2b, Q3 from each Step 3b block — Q4 verdict line REDACTED):
<paste each check block from Step 3b BUT strip the "Q4 (verdict): ..." line>
<also include all candidates examined, including those the primary agent cleared as "non-match" — the sub-agent must see the full evidence set, not the curated subset>

QUESTION: What is the most likely root cause? What would you check next if uncertain?
```

**Do NOT include the primary agent's hypothesis.** Two operational rules:

1. Strip every `Q4 (verdict): ...` line before pasting. Q4 IS the primary agent's hypothesis in compressed form.
2. Pass ALL candidates' Q1–Q3 blocks (matches AND non-matches AND unclears) — filtering to only "match" candidates communicates the primary's hypothesis through filter selection.

Compare: agreement → raise confidence. Divergence → collect more data, do not close.

**Fallback if Agent tool unavailable**: note "sub-agent cross-check skipped — Agent tool not available in this runtime." Confidence capped at MED.

→ Proceed to Step 8.

### Step 8 — Report

```markdown
## Inspection report: <workflow_key> / <env> / <time_window UTC>

### Summary
<1-2 sentence root cause, or "root cause not determined">

### Baseline
- 7-day failure rate: <rate>% (chronic / acute / insufficient-data)

### Findings (ordered by confidence)
1. [HIGH] <finding>
   Evidence: execution <id>, node <name>, error: "<msg>"
   Causal-linkage: confirmed — <Q3 answer>
2. [MED] ...
3. [LOW] ...

### Trigger health
<Active: yes/no. Schedule: correct/misconfigured. Webhook: correct env.>

### Blast radius
<Workflows sharing root cause; running executions from those.>

### What was checked
- Workflows examined: <list>
- Executions inspected: <list>
- Causal-linkage checks: <N total — M confirmed, K cleared>
- Recursion depth: <N hops>
- Time window: <ISO UTC range>
- API verification: completed / skipped
- Sub-agent cross-check: yes (agree/diverge) / no (reason)

### Remaining ambiguity
<What would falsify or confirm remaining hypotheses>

### Recommended next step
<One concrete action. No mutation until user approves.>
```

After the user approves the recommended next step, the read-only invariant lifts. Until then: investigation only.

## Why this discipline exists

A naive "look at the failing execution" loop fails on three predictable shapes:

1. **`status=success` side-effect skips.** Without Step 3b's Q2b (branches/bypassed nodes), an agent closes on a branching-If that skipped the email-send and reports "execution succeeded — symptom must be downstream" when in fact the workflow itself didn't deliver.
2. **Hypothesis anchoring.** First plausible failure becomes the answer. Step 7's mandatory sub-agent spawn (with the primary's hypothesis stripped) is the antidote — fresh eyes, no priors.
3. **Time-correlated incidents misread as the workflow's fault.** Step 6 is mandatory when >1 workflow fails in the window so the agent doesn't pin the cause on the first symptom-matching one. Connected via `calls` / `credential_groups` → likely shared cause; unrelated → coincidence.

The 8-step structure trades raw speed for these three failure modes being addressed each time, regardless of how confident the agent feels at Step 3.
