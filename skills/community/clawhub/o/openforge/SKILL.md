---
name: openforge
description: >
  Staged, multi-model PRD execution for OpenClaw. Write a PRD with phased sections,
  model routing, and validation gates — OpenForge executes it across local and cloud
  models with automatic escalation, scope verification, quality checks, and learning
  accumulation. Route simple tasks to cheap models, hard tasks to powerful ones, and
  reviews to premium reasoning.
version: 2.2.0
---

# OpenForge v2

**PRD-to-implementation pipeline for OpenClaw.**

OpenForge takes a structured PRD (Product Requirements Document) and executes it through staged phases: parallel where possible, with model routing, quality gates, and automatic review-to-fix loops. No Python, no custom agent registration, no install step — runs entirely through native OpenClaw tools (`sessions_spawn`, `exec`, `read`, `write`).

---

## What OpenForge Does

1. **Parses** a PRD markdown file into phases and tasks
2. **Spawns sub-agents** for phases that can run in parallel
3. **Routes** each task to the right model tier (Haiku → Sonnet/GPT → Opus)
4. **Gates** each phase: pass/fail check after completion
5. **Auto-fixes**: when a review phase finds issues, a fix agent is spawned and the review re-runs (up to 3 cycles)
6. **Escalates** when retries are exhausted or a gate fails hard

---

## What OpenForge Does NOT Do

- Does not run a CLI — it IS the agent execution loop
- Does not add an OS-level sandbox beyond the agent's existing workspace constraints
- Does not require or manage custom agent registration

---

## Safety & Scope

- OpenForge operates within the user's configured workspace directory
- Sub-agents inherit the same workspace constraints as the orchestrator
- **PRD trust model:** PRDs define what code to write and what shell commands to run as gates. Review PRDs before execution — they have the same trust level as code you would run. Do not execute PRDs from untrusted sources.
- **Secret safety:** Never include secrets, API keys, or credentials in PRD files. PRD content is passed to sub-agents verbatim. OpenForge does not scan for embedded secrets — keep them in environment variables.
- **Gate commands:** Gate commands are run via `exec` in the working directory. Only build/test/lint commands are expected — for example: `npm test`, `npm run build`, `pytest`, `cargo test`, `go test`, `ruff check`. Before executing any gate, OpenForge validates that the command does not contain shell metacharacters (`;`, `&&`, `||`, `|`, `$(`, backticks, `>`, `<`) unless the PRD explicitly marks the phase with `Shell-Gate: true`. Gates that fail this check are rejected with an error. Review all gate commands in your PRD before execution.
- No credentials are bundled, stored, or transmitted by OpenForge
- All execution is local to the OpenClaw agent environment
- No data is sent to external endpoints beyond your configured AI model providers

---

## PRD Format

A PRD is a markdown file. OpenForge reads it top-to-bottom and extracts phases.

### Minimal PRD

```markdown
# PRD: My Feature

## Objective
Build a CSV export endpoint for the API.

## Phases

### Phase: scaffold [parallel]
**Model:** sonnet
**Tasks:**
- Create the route handler in `src/routes/export.ts`
- Write the CSV serializer in `src/lib/csv.ts`

**Gate:** `npm run build` must pass

### Phase: test [depends: scaffold]
**Model:** sonnet
**Tasks:**
- Write unit tests for the CSV serializer
- Write integration test for the export endpoint

**Gate:** `npm test` must pass

### Phase: review [depends: test]
**Model:** opus
**Type:** review
**Tasks:**
- Review the full implementation for correctness, edge cases, and security
- Check error handling on malformed input

**Gate:** Review must find zero blocking issues
```

### PRD Fields

| Field | Required | Values | Meaning |
|-------|----------|--------|---------|
| `Model:` | No | `haiku`, `sonnet`, `gpt`, `opus` | Model tier for this phase |
| `Type:` | No | `impl`, `review`, `extract` | Phase type; controls prompting style |
| `[parallel]` | No | Flag in phase header | Phase can run alongside other `[parallel]` phases |
| `depends:` | No | Phase name(s) | This phase waits for named phases to complete |
| `Gate:` | No | Shell command or description | Must pass before next phase starts |
| `Max-Retries:` | No | Integer (default: 2) | Gate failure retries before escalation |
| `Shell-Gate:` | No | `true` | Allow shell metacharacters in gate command (use only for trusted, reviewed gates) |

### Phase Types

- **`impl`** (default) — implementation work; agent writes code, files, configs
- **`review`** — evaluative; agent produces a structured findings report; triggers auto-fix loop if issues found
- **`extract`** — lightweight parsing or summarization; routed to Haiku

---

## Model Routing

| Alias | Maps To | Use For |
|-------|---------|---------|
| `haiku` | `claude-haiku` / cheapest available | Extraction, parsing, structured output |
| `sonnet` | `claude-sonnet` | Implementation, research, multi-file work |
| `gpt` | `gpt-4o` or equivalent | Alternative implementation path |
| `opus` | `claude-opus` | Judgment, review, final quality gate |

OpenForge maps these aliases to whatever models are configured in your OpenClaw instance. If a model alias isn't available, Sonnet is used as the safe fallback.

---

## Execution Protocol

When OpenForge is triggered, follow this exact sequence:

### Step 1 — Parse the PRD

Read the PRD file. Extract:
- Title and objective
- All phases in order, with their model, type, dependencies, gate, and task list
- Identify which phases are `[parallel]` and which have `depends:` constraints

Build a dependency graph. Phases with no `depends:` and tagged `[parallel]` can be spawned simultaneously.

**Horizon-Bounded Decomposition:** Estimate the total step count across all phases. If the PRD contains > 40 estimated steps, decompose complex phases into sub-phases of ≤ 20 steps each before execution. If 20–40 steps, insert a midpoint quality checkpoint between phases. Under 20 steps, execute directly. This prevents accuracy collapse on long-horizon tasks (research: LORE benchmark shows accuracy → 0 past 120 steps).

### Step 2 — Pre-flight check

Before spawning anything:
- Confirm the PRD has at least one phase
- Confirm all `depends:` references name real phases
- Confirm the working directory exists (if specified)
- If any check fails: halt and report the problem clearly

### Step 3 — Execute phases

For each wave of phases (phases whose dependencies are all satisfied):

**If multiple phases are `[parallel]`:** spawn them as sub-agents simultaneously using `sessions_spawn`. Pass each sub-agent:
- The full PRD context
- Its specific phase tasks
- The model to use
- The gate command (if any)
- The working directory

**If a phase has `depends:`:** wait for all named phases to complete before spawning.

**Sequential phases** (no `[parallel]` tag): run one at a time in declaration order.

### Step 4 — Gate evaluation

After each phase completes:
1. If a gate command is specified:
   - **Validate the gate command first.** Reject commands containing shell metacharacters (`;`, `&&`, `||`, `|`, `$(`, `` ` ``, `>`, `<`) unless the phase includes `Shell-Gate: true`. This prevents accidental or malicious arbitrary shell execution from PRD content.
   - Run the validated gate command with `exec`
2. **Erosion check (code phases):** If the phase produced code, measure structural complexity. If cyclomatic complexity mass in high-CC functions (CC > 10) increased > 5% compared to the prior phase's baseline, flag for review or force a refactoring sub-phase before proceeding. This prevents quality degradation across sequential phases (research: SlopCodeBench shows structural erosion in 80% of agent trajectories).
3. If the gate passes (exit 0): mark phase complete, proceed
4. If it fails: retry the phase up to `Max-Retries` times (default: 2), passing the failure output as context
5. If retries exhausted: escalate to Corbin and halt

### Step 5 — Review-to-fix loop

For phases with `Type: review`:
1. The review agent produces a structured findings report
2. Parse the report for blocking/required issues
3. If issues exist:
   - Spawn a **fix sub-agent** (same model tier as the implementation phase, or Sonnet default) with the findings as context
   - After fix agent completes, re-run the review phase
   - Repeat up to 3 cycles
4. If issues persist after 3 cycles: escalate with full findings history
5. If no blocking issues: mark review phase complete

**Review agent prompt structure:**
```
You are performing a structured code review.

Context:
{phase tasks and objective}

Working directory: {cwd}

Produce a report in this exact format:

## Findings

### Blocking
- [issue description] — [file:line if known]

### Required Changes
- [issue description]

### Suggestions
- [issue description]

### Summary
PASS | FAIL

If PASS: no Blocking or Required Changes items.
If FAIL: at least one Blocking or Required Changes item exists.
```

**Fix agent prompt structure:**
```
You are implementing fixes identified in a code review.

Review findings:
{findings report}

Fix all Blocking and Required Changes items. Do not change anything not listed.
Working directory: {cwd}

When complete, summarize what you changed.
```

### Step 6 — Completion

When all phases pass their gates:
1. Write a completion summary to `.openforge/run-{timestamp}.md` in the working directory (if a cwd was specified)
2. Report success with phase outcomes and any escalations that occurred
3. If any phases were skipped or escalated, report them explicitly

---

## Sub-agent Prompting

When spawning a sub-agent for a phase, include:

```
You are executing Phase: {phase_name} of an OpenForge PRD run.

## Objective
{PRD objective}

## Your Tasks
{task list}

## Working Directory
{cwd or "not specified — use judgment"}

## Prior Phase Outputs
{summaries from completed phases, if any}

## Gate
After completing your tasks, the following command will be run to validate your work:
{gate command or "none"}

## Constraints
- Only modify files relevant to your tasks
- Do not expose credentials, API keys, or secrets
- Write a brief summary of what you did when complete

## Model
You are running as: {model alias}
```

---

## Escalation Protocol

Escalate to the human (Corbin / operator) when:

1. A gate fails after all retries are exhausted
2. A review-to-fix loop hits 3 cycles without reaching PASS
3. The PRD has structural errors that prevent execution
4. A phase sub-agent returns an error that can't be recovered
5. A phase declares `escalate: true` explicitly

Escalation message format:
```
⚠️ OpenForge Escalation

PRD: {title}
Phase: {phase_name}
Reason: {specific failure reason}

What happened:
{summary of attempts}

Gate output (if applicable):
{last gate failure output, truncated to 500 chars}

Recommended next step:
{specific suggestion — fix the gate command, revise the PRD, or manual intervention}
```

---

## Security Constraints

- Sub-agents run with the same permissions as the parent agent within the workspace directory
- Gate commands are run with `exec` in the working directory. Review gate commands before running against production systems. Avoid destructive commands (e.g., `rm -rf`).
- OpenForge writes one artifact (`.openforge/run-{timestamp}.md`) to the working directory. No other writes are made by the orchestrator itself.
- No network connections are made by OpenForge itself — only your configured AI model providers are contacted via the OpenClaw agent interface

---

## Example: Full Parallel PRD

```markdown
# PRD: Auth Refactor

## Objective
Replace the custom session cookie system with JWT-based auth.

## Phases

### Phase: research [parallel]
**Model:** haiku
**Type:** extract
**Tasks:**
- Read `src/auth/` and summarize all current auth entry points
- List all routes that call `req.session`

### Phase: design [parallel]
**Model:** opus
**Type:** review
**Tasks:**
- Design the JWT strategy: token structure, expiry policy, refresh approach
- Identify migration risks

### Phase: implement [depends: research, design]
**Model:** sonnet
**Tasks:**
- Implement JWT middleware in `src/auth/jwt.ts`
- Replace session calls in all routes identified in research phase
- Update `src/auth/index.ts` to export new middleware

**Gate:** `npm run build && npm test`
**Max-Retries:** 3

### Phase: security-review [depends: implement]
**Model:** opus
**Type:** review
**Tasks:**
- Review JWT implementation for common vulnerabilities (alg confusion, weak secret, missing expiry check)
- Review token storage and transmission

**Gate:** Review must find zero Blocking issues
```

In this PRD:
- `research` and `design` run **in parallel** (no dependencies, both tagged `[parallel]`)
- `implement` waits for both, then runs with Sonnet
- `security-review` runs last with Opus, triggers auto-fix loop if issues are found

---

## Limitations (v2)

- Parallel phase results are collected via sub-agent completion events — if a sub-agent times out, that phase's output may be missing
- Review-to-fix loops use the same working directory; if the fix agent introduces regressions, OpenForge will catch them at the gate but won't automatically revert
- Gate commands run in the working directory with no isolation — avoid destructive commands (e.g., `rm -rf`)
- No persistent run state across sessions — if the parent agent session ends mid-run, the run cannot be resumed (sub-agents completing after session end will still announce results but the orchestrator won't act on them)
- Model alias resolution depends on your OpenClaw instance's configured models; if `opus` isn't available, Sonnet will be used silently

---

## Quick Reference

| What you want | How to trigger |
|---------------|---------------|
| Run a PRD | "Run this PRD: [paste or path]" |
| Dry-run (plan only) | "Plan this PRD without executing" |
| Run a single phase | "Run only the `implement` phase of this PRD" |
| Skip a phase | Add `Skip: true` to the phase header |
| Force a model | Add `Model: opus` to any phase |
| Cap retries | Add `Max-Retries: 1` to a phase |
| Parallel phases | Add `[parallel]` to phase header |
