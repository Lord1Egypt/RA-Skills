---
name: ocas-mentor
source: https://github.com/indigokarasu/mentor
install: openclaw skill install https://github.com/indigokarasu/mentor
description: Use when managing long-running multi-skill workflows, evaluating skill performance from journals, comparing champion vs challenger variants, or proposing skill improvements to Forge. Trigger phrases: 'manage this project', 'coordinate a multi-step analysis', 'evaluate skill performance', 'run a heartbeat', 'how are skills performing', 'update mentor'. Do not use for web research (use Sift), skill building (use Forge), or user communication (use Dispatch).
metadata: {"openclaw":{"emoji":"🎓"}}
---

# Mentor

Mentor is the system's control plane — in runtime mode it decomposes goals into task graphs, supervises execution across skills, and dynamically repairs failures through a layered escalation policy from local retry up to full strategy replan. In heartbeat mode it reads journals from every skill, scores OKR performance against baselines, and generates improvement proposals that flow to Forge and Fellow for empirical evaluation and promotion.

Mentor and Elephas are parallel journal consumers: Mentor reads journals to evaluate skill performance, Elephas reads them to extract entity knowledge into Chronicle, and neither blocks the other.


## When to use

- Manage a long-running multi-step project
- Coordinate work across multiple skills
- Evaluate skill performance from journal data
- Compare champion vs challenger variant runs
- Generate improvement proposals for Forge


## When not to use

- Web research — use Sift
- Building new skills — use Forge
- User communication — use Dispatch
- Behavioral pattern analysis — use Corvus


## Responsibility boundary

Mentor owns orchestration, evaluation, and the improvement loop.

Mentor does not own: skill building (Forge), behavioral pattern detection (Corvus), behavioral refinement (Praxis), knowledge graph (Elephas), web research (Sift), communications (Dispatch), experimentation execution (Fellow).

Mentor proposes improvements; Forge builds them. Mentor detects regressions; Praxis extracts behavioral lessons from Corvus signals.


## Commands

- `mentor.project.create` — create a project with goal, constraints, and requested output
- `mentor.project.status` — current project state, task graph, execution progress
- `mentor.project.replan` — trigger strategy-level replan
- `mentor.task.list` — tasks with statuses, dependencies, blocking reasons
- `mentor.heartbeat.light` — lightweight pass: ingest journals, update aggregates, queue work
- `mentor.heartbeat.deep` — deep pass: full scoring, trend analysis, proposals
- `mentor.variants.list` — active champion/challenger pairs with evaluation status
- `mentor.variants.decide` — emit promotion decision for a variant (writes VariantDecision to Forge intake)
- `mentor.proposals.list` — pending skill improvement proposals
- `mentor.proposals.create` — generate a VariantProposal for a target skill (writes to Forge intake)
- `mentor.status` — active projects, pending evaluations, self-improvement metrics
- `mentor.journal` — write journal for the current run; called at end of every run
- `mentor.update` — pull latest from GitHub source; preserves journals and data
- `mentor.plan.list` — list available plans with plan_id, version, and description
- `mentor.plan.run {plan_id} [--arg name=value ...]` — execute a named workflow plan
- `mentor.plan.status {plan_run_id}` — current state of a running or recent plan run
- `mentor.plan.resume {plan_run_id}` — continue a paused or failed plan run from the first incomplete step
- `mentor.plan.history [--plan plan_id] [--limit N]` — recent plan run summaries


## Mode A — Runtime orchestration

Triggered by explicit invocation. Creates a project record, builds a task graph, executes and supervises tasks, dynamically replans when blocked.

Task states: pending, ready, running, blocked, failed, complete, archived.

Scheduling: execute only tasks with complete dependencies. Prioritize critical path. Bounded parallelism. Bounded retries.


## Mode B — Heartbeat evolution

Triggered periodically. Pipeline: ingest journals → validate schema → aggregate metrics → pair champion/challenger → score OKRs → detect anomalies → evaluate variants → generate proposals → emit decisions → write journal.

Mentor reads journals from all skills at: `~/openclaw/journals/` (recursive scan). It tracks which run_ids have been ingested via `~/openclaw/data/ocas-mentor/ingestion_log.jsonl`.


## Run completion

After every Mentor command (orchestration or heartbeat):

1. Check `~/openclaw/data/ocas-mentor/intake/` for CycleResult files from Fellow; process and move to `intake/processed/`
2. Persist project state, evaluation results, or proposals to local files
3. For experiment requests: write ExperimentRequest file to `~/openclaw/data/ocas-fellow/intake/{experiment_id}.json`, then invoke `fellow.experiment.run`
4. For variant proposals: write VariantProposal file to `~/openclaw/data/ocas-forge/intake/{proposal_id}.json`
5. For variant decisions: write VariantDecision file to `~/openclaw/data/ocas-forge/intake/{decision_id}.json`
6. Log material decisions to `decisions.jsonl`
7. Write journal via `mentor.journal`

## Layered evaluation loops

- **Layer 1 — Micro Action** (ms-sec): validate single outputs. Retry, local repair, fallback.
- **Layer 2 — Task Execution** (sec-min): ensure task completion. Retry, switch skill, split task.
- **Layer 3 — Strategy** (min-hr): improve active project plan. Reorder, insert, merge, parallelize.
- **Layer 4 — Evolution** (hr-wk): improve skills and policies. Propose variants, promote/archive.


## Failure repair policy

Order: retry with refined framing → alternate skill → split task → revise ordering → escalate to strategy loop. Never retry indefinitely. Every repair action journaled.


## Safety invariants

- Challenger variants never execute side effects
- Comparisons only on identical normalized inputs
- Malformed journals quarantined, not trusted
- Promotion requires sufficient evidence over multiple runs
- Mentor journals its own orchestration decisions


## Inter-skill interfaces

Mentor writes ExperimentRequest files to: `~/openclaw/data/ocas-fellow/intake/{experiment_id}.json`
Written when empirical evaluation is needed. Mentor then invokes `fellow.experiment.run`. Fellow writes the result back.

Mentor receives CycleResult files from Fellow at: `~/openclaw/data/ocas-mentor/intake/{cycle_id}.json`
Read during `mentor.heartbeat.light` and `mentor.heartbeat.deep`. On `decision: promote`, Mentor emits a VariantDecision to Forge.

Mentor writes VariantProposal files to: `~/openclaw/data/ocas-forge/intake/{proposal_id}.json`
Mentor writes VariantDecision files to: `~/openclaw/data/ocas-forge/intake/{decision_id}.json`

See `spec-ocas-interfaces.md` for schemas and handoff contracts.

Mentor reads journals from: `~/openclaw/journals/` (all skills, recursive). This is a read-only scan parallel to Elephas ingestion.


## Storage layout

```
~/openclaw/data/ocas-mentor/
  config.json
  projects/
  evaluations/
  ingestion_log.jsonl
  decisions.jsonl
  intake/
    {cycle_id}.json
    processed/
  plans/
    {plan_id}.plan.md
  plan-runs/
    {plan_run_id}/
      state.json
      decisions.jsonl

~/openclaw/journals/ocas-mentor/
  YYYY-MM-DD/
    {run_id}.json
```


Default config.json:
```json
{
  "skill_id": "ocas-mentor",
  "skill_version": "2.3.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "heartbeat": {
    "light_interval_minutes": 15,
    "deep_interval_hours": 24
  },
  "evaluation": {
    "minimum_runs_for_promotion": 20,
    "non_regression_required": true
  },
  "retention": {
    "days": 0,
    "max_records": 10000
  }
}
```


## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: orchestration_success_rate
    metric: fraction of projects reaching completion without manual rescue
    direction: maximize
    target: 0.85
    evaluation_window: 30_runs
  - name: evaluation_coverage
    metric: fraction of skill journals ingested within one heartbeat cycle
    direction: maximize
    target: 0.99
    evaluation_window: 30_runs
  - name: variant_decision_quality
    metric: fraction of promotions not rolled back within 30 days
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: repair_escalation_rate
    metric: fraction of failures requiring strategy-level escalation
    direction: minimize
    target: 0.10
    evaluation_window: 30_runs
```


## Optional skill cooperation

- Forge — receives VariantProposal and VariantDecision files via intake directory
- Fellow — invoked by Mentor to run controlled benchmark experiments; returns best variant result
- Elephas — Mentor may read Chronicle (read-only) for evaluation context
- Corvus — Mentor may read Corvus pattern data for anomaly context
- All skills — Mentor reads journals from all skills for evaluation


## Journal outputs

Action Journal — every orchestration run, heartbeat pass, variant evaluation, and proposal emission.


## Initialization

On first invocation of any Mentor command, run `mentor.init`:

1. Create `~/openclaw/data/ocas-mentor/` and subdirectories (`projects/`, `evaluations/`, `intake/`, `intake/processed/`, `plans/`, `plan-runs/`)
2. Write default `config.json` with ConfigBase fields if absent
3. Create empty JSONL files: `ingestion_log.jsonl`, `decisions.jsonl`
4. Create `~/openclaw/journals/ocas-mentor/`
5. Ensure `~/openclaw/data/ocas-forge/intake/` exists (create if missing)
6. Ensure `~/openclaw/data/ocas-fellow/intake/` exists (create if missing)
7. Copy bundled plans from skill package `references/plans/*.plan.md` to `~/openclaw/data/ocas-mentor/plans/` -- skip any plan file already present (do not overwrite user-modified plans)
8. Register cron jobs `mentor:deep` and `mentor:update` if not already present (check `openclaw cron list` first)
9. Register heartbeat entry `mentor:light` in `HEARTBEAT.md` if not already present
10. Log initialization as a DecisionRecord in `decisions.jsonl`


## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `mentor:deep` | cron | `0 5 * * *` (daily 5am) | `mentor.heartbeat.deep` — full OKR scoring, trend analysis, variant proposals |
| `mentor:light` | heartbeat | every heartbeat pass | `mentor.heartbeat.light` — ingest journals, update aggregates, queue work |
| `mentor:update` | cron | `0 0 * * *` (midnight daily) | `mentor.update` |

Cron options for `mentor:deep`: `sessionTarget: isolated`, `lightContext: true`, `wakeMode: next-heartbeat`.

Registration during `mentor.init`:
```
openclaw cron list
# If mentor:deep absent:
openclaw cron add --name mentor:deep --schedule "0 5 * * *" --command "mentor.heartbeat.deep" --sessionTarget isolated --lightContext true --wakeMode next-heartbeat --timezone America/Los_Angeles
# If mentor:update absent:
openclaw cron add --name mentor:update --schedule "0 0 * * *" --command "mentor.update" --sessionTarget isolated --lightContext true --timezone America/Los_Angeles
```

Heartbeat registration: append `mentor:light` entry to `~/.openclaw/workspace/HEARTBEAT.md` if not already present.


## Self-update

`mentor.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from `skill.json`
3. Fetch remote version: `gh api "repos/{owner}/{repo}/contents/skill.json" --jq '.content' | base64 -d | python3 -c "import sys,json;print(json.load(sys.stdin)['version'])"`
4. If remote version equals local version → stop silently
5. Download and install:
   ```bash
   TMPDIR=$(mktemp -d)
   gh api "repos/{owner}/{repo}/tarball/main" > "$TMPDIR/archive.tar.gz"
   mkdir "$TMPDIR/extracted"
   tar xzf "$TMPDIR/archive.tar.gz" -C "$TMPDIR/extracted" --strip-components=1
   cp -R "$TMPDIR/extracted/"* ./
   rm -rf "$TMPDIR"
   ```
6. On failure → retry once. If second attempt fails, report the error and stop.
7. Output exactly: `I updated Mentor from version {old} to {new}`


## Visibility

public


## Support file map

| File | When to read |
|---|---|
| `references/schemas.md` | Before creating projects, tasks, proposals, or decisions |
| `references/orchestration_engine.md` | Before goal decomposition, scheduling, or failure repair |
| `references/evaluation_engine.md` | Before journal ingestion, OKR scoring, or champion/challenger pairing |
| `references/evolution_engine.md` | Before improvement detection, proposal generation, or promotion decisions |
| `references/journal.md` | Before mentor.journal; at end of every run |
| `references/workflow_plans.md` | Before any mentor.plan.* command |
| `references/plans/template.plan.md` | When writing a new plan file |
| `references/plans/contact-enrichment.plan.md` | When running the contact enrichment workflow |
