---
name: ocas-custodian
source: https://github.com/indigokarasu/custodian
install: openclaw skill install https://github.com/indigokarasu/custodian
description: Use when checking system health, fixing log errors, reviewing cron failures, initializing skills, registering missing background tasks, or running overnight maintenance. Trigger phrases: 'check system health', 'fix log errors', 'why is X failing', 'initialize skills', 'clean up errors', 'show open issues', 'what time does custodian run', 'update custodian'. Do not use for skill OKR analysis (use Mentor/Corvus), skill rebuilding (use Forge), knowledge graph queries (use Elephas), social graph queries (use Weave), or research tasks (use Scout/Sift).
metadata: {"openclaw":{"emoji":"🧹"}}
---

# Custodian

Custodian detects, classifies, and repairs OpenClaw operational failures autonomously during quiet hours so the user wakes to clean logs, initialized skills, and registered background tasks -- surfacing only what it could not fix.

## When to use

- Asked to check system health, fix log errors, review cron failures
- Asked to initialize skills or register missing background tasks
- Asked why OpenClaw or a specific skill is failing
- Running overnight maintenance or a system audit
- Invoked automatically via heartbeat or cron

## Responsibility Boundary

**Owns:** gateway log scanning and error fingerprinting, cron job registry health, skill journal completeness, OCAS data directory health, skill initialization, background task conformance, Tier 1 auto-repair, activity model and schedule optimization, escalation signaling, fix effectiveness tracking.

**Does not own:** OKR trend analysis (Corvus, Mentor), skill design evaluation or rebuilding (Mentor, Forge), behavioral lesson extraction (Praxis), briefing delivery (Vesper), entity knowledge (Elephas), social graph (Weave). Never modifies any file inside a skill package directory.

## Optional Skill Cooperation

- **Vesper** -- writes InsightProposals to `~/openclaw/data/ocas-vesper/intake/` after deep scans. Without Vesper, issues stay in `issues.jsonl`.
- **Mentor** -- journals tagged `escalation_needed: true` are readable by Mentor heartbeat. Without Mentor, escalated issues await manual review.
- **Corvus** -- if installed, reads Corvus observation journals for `routine_prediction` InsightProposals. Blended 70% Corvus / 30% own model. Functions normally without Corvus.

## Commands

- `custodian.init` -- create storage, register background tasks idempotently, copy bundled plan to Mentor plans dir, build initial activity model
- `custodian.scan.light` -- tail gateway log (last 100 lines), check cron registry, retry open `fix_attempted_failed` items, check for uninitialized skills, write Observation Journal
- `custodian.scan.deep` -- full sweep: all light steps + full JSONL scan, doctor diagnostic, journal health, skill conformance, skill init pass, activity model rebuild, schedule optimization, repair pass, web search pass, escalation pass, report, Vesper signal
- `custodian.verify {fix_id}` -- verify fix outcome, update record, escalate if failed twice
- `custodian.repair.auto` -- apply all pending Tier 1 fixes from last scan
- `custodian.repair.plan` -- generate structured repair plan for Tier 2/3 issues
- `custodian.issues.list` -- list open issues with tier, status, age, recurrence
- `custodian.issues.resolve {issue_id}` -- mark issue resolved manually
- `custodian.status` -- emit SkillStatus JSON
- `custodian.schedule.show` -- display current and target scan schedule with optimization confidence
- `custodian.update` -- pull latest from GitHub source (preserves journals and data)

## Execution Loop -- Light Scan

Runs every heartbeat. Must be fast (seconds). No web search, doctor, or report.

1. Read `~/.openclaw/cron/jobs.json` -- find jobs with `enabled: false` that were previously enabled in `skill_conformance.jsonl`. Re-enable (Tier 1).
2. Tail `/tmp/openclaw/openclaw-YYYY-MM-DD.log` -- last 100 lines. Fingerprint ERROR entries against `references/known_issues.json` then `learned_issues.jsonl`. Apply Tier 1 fixes. Open issues for Tier 3/4.
3. Check `issues.jsonl` for `status: fix_attempted_failed`. Retry Tier 1 up to 3 times before escalating.
4. Check for uninitialized skills (data dir or config.json missing). Initialize immediately.
5. Write Observation Journal.

## Execution Loop -- Deep Scan

Runs on optimized 6-hour cron schedule. Isolated session, lightContext.

1. **Load context** -- own journals (7 days), `fix_effectiveness.jsonl`. Identify recurring fingerprints, known-failed fixes, already-searched queries.
2. **Collect** -- full day gateway log, cron run logs, skill journals from scan window, all OCAS data dirs, `openclaw doctor --non-interactive`.
3. **Fingerprint + classify** -- match against `references/known_issues.json` then `learned_issues.jsonl`. Unknowns default Tier 3.
4. **Rebuild activity model** -- parse gateway log `message.processed` events (`source: user` vs `source: cron|heartbeat`). Blend Corvus if present (70/30). Update `activity_model.json`. Determine `current_state`.
5. **Optimize schedule** -- score current schedule against activity model. If score < 6, compute better schedule. Shift max 30 min per slot. Update cron if changed.
6. **Skill conformance** -- scan installed skills, parse `## Background tasks`, cross-reference against `openclaw cron list` and `HEARTBEAT.md`. Register missing (Tier 1). Surface mismatches (Tier 2).
7. **Skill init pass** -- initialize any skill missing data dir, config.json, or journal dir.
8. **Repair pass** -- all Tier 1 fixes. Activity-aware: if active, only urgent fixes (failure in last 5 min); defer rest. Register verify jobs. Execute prior deferred fixes if now quiet.
9. **Web search pass** -- for unknown fingerprints with `recurrence_count >= 1`, run next mutation query (see Web Search Protocol).
10. **Escalation pass** -- Tier 3/4 open issues: write InsightProposal to Vesper intake. Tag journal `escalation_needed: true`.
11. **Report** -- `~/openclaw/data/ocas-custodian/reports/YYYY-MM-DD-HHMM.md`. If all clean and previous cycle also clean: suppress Vesper signal.
12. **Write journal** -- Action (if fixes applied) or Observation (scan-only).

## Fix Safety Envelope

Every autonomous fix must satisfy all four:

1. **Non-destructive** -- no delete, overwrite, or permanent alteration
2. **Reversible** -- pre-fix state restorable without backup
3. **Minimal scope** -- smallest surface to address symptom
4. **Functionality-preserving** -- cannot reduce capability

Hard constraints: never modify skill package files, never delete files, never modify another skill's data dir, never restart gateway, never change user settings without acknowledgment.

## Tier Classification

| Tier | Label | Action |
|---|---|---|
| 1 | Auto-fix | Apply immediately, register verify job, log fix record |
| 2 | Plan | Surface with proposed change, do not apply |
| 3 | Escalate | Write to escalation journal + Vesper intake, invoke Mentor plan if available |
| 4 | Alert only | Cannot fix -- surface with diagnostics |

High-recurrence override: if `recurrence_after_fix / successes > 0.5`, auto-promote next occurrence from Tier 1 to Tier 3.

## Tier 1 Auto-Fix Registry

All Tier 1 fixes defined in `references/known_issues.json`. Read at start of every scan. Pre-seeded fingerprints:

| Fingerprint | Fix |
|---|---|
| `oc_cron_disabled_transient` | Re-enable cron job |
| `oc_cron_stuck_missed` | Force-run missed job |
| `oc_intake_dir_missing` | Create directory |
| `oc_journal_dir_missing` | Create directory |
| `oc_skill_data_dir_missing` | Create directory + default config.json |
| `oc_jsonl_oversized` | Rotate with date suffix |
| `oc_jsonl_malformed_lines` | Quarantine to `.error` file |
| `oc_gateway_token_missing` | `openclaw doctor --generate-gateway-token` |
| `oc_oauth_token_expiring` | OAuth refresh (token still valid, expiry <= 12h) |
| `oc_background_task_missing` | Register cron or heartbeat entry per SKILL.md |
| `oc_skill_uninitialized` | Create storage dirs, default config, empty JSONL |

## Fix Verification

Every Tier 1 fix registers a one-shot cron job `custodian:verify:{fix_id}` with delay per fix type (2-15 min). On verification failure: set `outcome: fix_attempted_failed`. Two consecutive failures: promote to Tier 3. Fix records appended to `fixes.jsonl` with `fix_id`, `issue_id`, `command`, `reversibility`, `pre_fix_state`, `post_fix_state`, `outcome`.

## Post-Fix Cleanup

After successful verification, run fix-specific cleanup (check backoff, confirm next run, validate permissions). Record in `cleanup_events.jsonl`.

## Skill Conformance Checking

On every deep scan: scan `~/.openclaw/workspace/skills/`, parse each SKILL.md `## Background tasks`, cross-reference against `openclaw cron list` and `HEARTBEAT.md`. Missing tasks: Tier 1 fix. Schedule mismatches: Tier 2. Orphaned `custodian:*` jobs: Tier 2. Write `skill_conformance.jsonl` per skill.

## Skill Initialization

Uninitialized when: data dir missing, config.json missing, or journal dir missing. Sequence (additive only, never overwrite):

1. Create `~/openclaw/data/{skill-name}/` if missing
2. Write default config.json with ConfigBase fields -- only if absent
3. Create `~/openclaw/journals/{skill-name}/` if missing
4. Create declared intake dirs if missing
5. Run conformance check for background tasks
6. Register missing tasks (Tier 1, subject to parameter availability)
7. Register verify job (15 min delay)
8. Append DecisionRecord

Do not run the skill's own `{skill}.init` command.

## Activity Model

Maintained in `activity_model.json`, rebuilt every deep scan from 14-day gateway log window. Confidence per hour: `active_days / total_days` (>= 0.75 high, >= 0.40 med, < 0.40 low). `current_state: active` if hour confidence >= med and in active window, else `quiet`.

Repair rules: quiet = all Tier 1; active = urgent only (failure in last 5 min), defer rest; low confidence = execute but suppress noisy effects. Cold start: `01:00, 07:00, 13:00, 19:00 PT`. Optimization begins after 7 days.

## Schedule Optimization

Exactly 4 runs/day, min 2h gap, max 30 min shift per cycle. Score each run time against activity model (-2 to +2 per slot, max +8). If score >= 6: no change. If < 6: find candidate maximizing score, shift toward target. Update cron registration.

Confidence gate: high = optimize freely, med = only if score <= 2, low = hold.

## Web Search Protocol

Fire when: fingerprint unknown, recurrence increased since last search, last search not actionable, not escalated/suppressed, < 5 attempts.

Query mutation sequence: (1) `{error} openclaw`, (2) `{error} {tech_context}`, (3) `{error_pattern} fix`, (4) `{component} {failure_mode}`, (5) `{failure_mode} root cause diagnosis`.

On actionable result: attempt fix, append to `learned_issues.jsonl` if successful. On no result: record and continue mutation on next recurrence.

## Self-Improvement

`fix_effectiveness.jsonl`: per-fingerprint tracking of attempts, successes, failures, recurrence. High-recurrence escalation: `recurrence_after_fix / successes > 0.5` promotes to Tier 3.

Custodian OKRs (every journal): `success_rate`, `issues_detected`, `issues_auto_fixed`, `fix_success_rate`, `mean_time_to_fix_ms`, `open_residuals`, `escalations`, `high_recurrence_fingerprints`, `skills_initialized`, `background_tasks_registered`, `schedule_score`, `journal_completeness`.

## Escalation Path

Tier 3: append `status: escalated` to `issues.jsonl`, tag journal `escalation_needed: true`, write InsightProposal (`anomaly_alert`) to `~/openclaw/data/ocas-vesper/intake/`. If Mentor present, note `mentor.plan.run custodian-repair --arg issue_id={id}` available.

Clean state: zero open issues + previous cycle clean = suppress Vesper signal. First run of day or issues now resolved = emit clean bill of health.

## Journal Outputs

- **Observation Journal** -- scan-only runs, no fixes applied
- **Action Journal** -- any run with Tier 1 fixes or cron registrations

Both include full Custodian OKR block. Path: `~/openclaw/journals/ocas-custodian/YYYY-MM-DD/{run_id}.json`

## Background tasks

| Job | Mechanism | Schedule | Command |
|---|---|---|---|
| `custodian:light` | heartbeat | every heartbeat cycle | `custodian.scan.light` |
| `custodian:deep` | cron | optimized 6h (initial: `0 1,7,13,19 * * *` PT) | `custodian.scan.deep` |
| `custodian:update` | cron | `0 0 * * *` (midnight daily) | Self-update from GitHub source |

Registration during `custodian.init` (idempotent -- check `openclaw cron list` first).

## Storage Layout

```
~/openclaw/data/ocas-custodian/
  config.json                  -- ConfigBase + scan_window_minutes, optimization settings
  issues.jsonl                 -- issue lifecycle records
  fixes.jsonl                  -- fix attempt records with pre/post state
  cleanup_events.jsonl         -- post-fix cleanup records
  fix_effectiveness.jsonl      -- per-fingerprint outcome tracking
  learned_issues.jsonl         -- runtime-learned fingerprints from web search
  skill_conformance.jsonl      -- per-skill background task conformance
  activity_model.json          -- rolling 14-day activity pattern (rebuilt each deep scan)
  deferred_fixes.jsonl         -- fixes queued for next quiet window
  schedule_state.json          -- current/target schedule, optimization history
  decisions.jsonl              -- DecisionRecord entries
  reports/
    YYYY-MM-DD-HHMM.md         -- deep scan summaries (7-day retention)
~/openclaw/journals/ocas-custodian/
  YYYY-MM-DD/{run_id}.json
```

## Support File Map

| File | Purpose | When to read |
|---|---|---|
| `references/known_issues.json` | Pre-seeded fingerprint registry with tier, fix, reversibility | Start of every scan before classifying errors |
| `references/plans/custodian-repair.plan.md` | Mentor Workflow Plan for Tier 3 multi-step repair | Copied to Mentor plans dir during init; referenced in escalation |
