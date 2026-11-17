---
license: MIT
name: ocas-multipass
description: 'Accomplishes tasks that need tools the agent does not have. Plans approaches, fills capability gaps with sandboxed tools, executes within an isolated session. Disposable identity, parallel discovery, incremental checkpoints, graceful degradation. Output: task result plus replay script. No global installs, no real identity, clean state in and out. Do not use for tasks solvable with installed skills, permanent skill installs, skill builds (use Forge), or general web research (use Sift).'
source: https://github.com/<agent-handle>/multipass
includes:
- references/**
- scripts/**
metadata:
  author: Indigo Karasu (indigokarasu)
  version: "4.2.0"
tags:
- sandbox
- capability-gap
- tools
- isolated-execution
triggers:
- capability gap
- sandboxed tools
- fill tool gaps
- task needs tools
---

# Multipass

Accomplish tasks that require tools you don't have. Fire and forget. User invokes `multipass.run {task}`, Multipass runs to completion, user gets the output. No check-ins, no approval gates, no escalation.

Everything happens inside a session directory. Nothing touches the rest of the agent platform.

## Interactive Menu

When invoked interactively, present a two-level menu. See `references/interactive-menu.md` for the full menu structure.

## When to Use

- Tasks requiring tools not currently installed
- Sandboxed execution with disposable identity
- Parallel discovery across multiple surfaces
- When the agent is about to say "I can't do that"
- Reproducible recipe generation for uncommon workflows

## When NOT to Use

- Tasks solvable with installed OCAS skills
- Permanent skill installation (use platform skill install)
- Skill building (use Forge)
- General web research (use Sift)

## Isolation Rules

- All files in session dir: `{agent_root}/commons/data/ocas-multipass/sessions/{session_id}/`
- No global skill installs. No global MCP config changes. No real identity.
- No env vars, secrets, or config written outside session dir.
- If a capability requires breaking isolation, skip it silently and find an alternative.

## Autonomy Rules

Once invoked, Multipass runs to completion without user interaction.

- No "Proceed?" gates. No "Should I...?" questions. No escalation.
- Every decision is made by the skill. If a choice is ambiguous, pick the safest sandboxable option and log the reasoning.
- If everything fails, produce a failure report documenting what was tried and why each path failed. A useful failure report is still an output.
- The only user-facing moments are invocation and the final result.

## Loop Prevention

See `references/loop-prevention.md` for the full set of circuit breakers and anti-stall rules every worker must follow.

## Workflow

Four phases. Task first, tools second, execution third, report last. See `references/workflow.md` for the full phase-by-phase procedure (Plan, Fill Gaps, Execute, Report).

## Commands

- `multipass.run {task description}` -- full autonomous lifecycle
- `multipass.search {description}` -- discovery only
- `multipass.sessions` -- list recent sessions
- `multipass.replay {session_id}` -- re-execute replay script (new session, new identity)
- `multipass.status` -- config, source health

## Responsibility Boundary

**Multipass does**: plan, discover, provision identity, resolve, execute, checkpoint, report. All autonomously.

**Multipass does not**: install anything globally, use real identity, persist secrets, build skills, ask the user for help mid-run.

If a user runs the same replay 3+ times, suggest permanent installation or a Forge-built skill.

## Optional Skill Cooperation

- **ivangdavila/api**: Check 147-service reference before discovery.
- **ivangdavila/reverse-engineering**: TRACE protocol for probing candidates.
- **Sift**: Deeper candidate research. If absent, use `web_search`.
- **Forge**: Suggest after completion if user needs a permanent solution.
- **mcporter**: Check existing connections. Call by URL for sandboxed access.

## Journal Outputs

**Action Journal** -- after every `multipass.run`.
**Research Journal** -- after every `multipass.search`.

Path: `{agent_root}/commons/journals/ocas-multipass/YYYY-MM-DD/{run_id}.json`

## Recovery Behavior

This skill implements the recovery contract from `spec-ocas-recovery.md`.

- **Evidence**: Every multipass.run writes an evidence record to `{agent_root}/commons/data/ocas-multipass/evidence.jsonl`, including failed runs. The `not_activity_reason` field is mandatory when no side effects occur.
- **Gap detection**: Not applicable — on-demand only.
- **Degraded mode**: When sandbox tools are unavailable, logs `degraded: <tool>` and attempts fallback approaches per existing resilience patterns.
- **Log compaction**: Session logs older than 30 days compacted to summaries. Last 7 days retained.

## Storage Layout

See `references/storage-layout.md` for the full directory structure.

**Token storage discipline** (per `spec-ocas-skill-improvements.md` §5.1): Session tokens and service credentials are stored at the standard path `~/.hermes/{service}_token.json` with the following validation before every request:
1. **Freshness check** — compare `expires_at` against `now + 5min`; if expired or expiring within 5 minutes, refresh the token before executing the multiplexed request. Do not send a stale token.
2. **Shape validation** — verify the file is valid JSON with `{access_token, token_type, expires_at}` fields. A corrupt or missing token file is logged as `token_error` and the request fails with `auth_failure` — never attempt a request with an empty/invalid token.
3. **Cleanup** — after a refresh, atomically write the new token to the standard path before releasing dependents. Do not leave a mix of old/new tokens per service.

## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs. See `references/okrs.md` for skill-specific targets (tool invocation success, spawn depth efficiency, isolation violation rate, schedule adherence, data integrity).

## Initialization

On first run (`multipass.init`):

1. Create dirs and default `config.json`
2. Check `maxSpawnDepth`, log parallel mode availability
3. Check mcporter availability, log MCP access mode (mcporter / direct HTTP / unavailable)
4. Verify session dir is writable
5. Log initialization as DecisionRecord

## Ontology Types

Multipass does not extract entities and does not emit Chronicle signals.

## Visibility

Public.

## Gotchas

Error handling in multipass follows a strict isolation contract: never leak session state, never install globally, and never retry the same failure path twice.

- **No global installs, no real identity** — Multipass must not install skills globally, modify MCP configs, or use the real user identity. If a capability requires breaking isolation, skip it silently and find an alternative.
- **Duplicate drafts/waits are forbidden** — Same action + same result = move on immediately. Two identical failures on the same endpoint is the maximum. No folk theories, no "waiting for the server," no invented timing explanations.
- **Identity provisioning is disposable** — Throwaway email accounts from the BotEmail cascade are temporary. If all identity providers fail, Multipass restricts itself to no-auth candidates without surfacing the failure to the user.
- **Failure reports are valid outputs** — If all approaches fail, the manifest documents every tried path and failure reason. A complete failure report is still a useful artifact and counts as task completion.
- **Session isolation is absolute** — All files must stay within the session directory. Nothing leaks to the platform, global config, or other sessions. An isolation violation is a serious incident.

## Self-Update

`multipass.update` pulls the latest version from GitHub. See `references/self-update.md`.

## Support File Map

| File | When to read |
|------|-------------|
| `references/workflow.md` | Before executing a multipass run. Full 4-phase procedure (Plan, Fill Gaps, Execute, Report). |
| `references/orchestration.md` | Before Phase 1 (plan) config check; before spawning workers; when setting up checkpoints or recovery logic |
| `references/surfaces.md` | During Phase 2 (fill gaps) discovery; when searching for candidate tools or APIs |
| `references/scoring.md` | During Phase 2 candidate evaluation; when scoring and ranking discovered tools |
| `references/resilience.md` | When an endpoint fails or returns an error; when provisioning throwaway identity; when hitting CAPTCHA/gates; when applying reframing tactics |
| `references/loop-prevention.md` | Before any worker execution; when enforcing circuit breakers and anti-stall rules |
| `references/okrs.md` | During OKR evaluation. Skill-specific targets for tool invocation, spawn depth, isolation, schedule, data integrity. |
| `references/self-update.md` | When running `multipass.update`. |
| `references/interactive-menu.md` | When invoked interactively via `/` command. |
| `references/storage-layout.md` | When creating or inspecting session directories. |
