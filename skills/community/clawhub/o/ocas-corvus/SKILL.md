---
name: ocas-corvus
source: https://github.com/indigokarasu/corvus
install: openclaw skill install https://github.com/indigokarasu/corvus
description: Use when analyzing behavioral patterns, detecting routines, finding anomalies in the knowledge graph, or running exploration cycles across accumulated activity signals. Detects routines, emerging interests, stalled threads, and cross-domain opportunities. Trigger phrases: 'analyze patterns', 'detect routines', 'find anomalies', 'what patterns do you see', 'exploration cycle', 'run analysis', 'update corvus'. Do not use for web research (use Sift), person investigations (use Scout), or system architecture changes (use Mentor).
metadata: {"openclaw":{"emoji":"🐦‍⬛"}}
---

# Corvus

Corvus is the system's curiosity engine — it continuously scans the knowledge graph and skill journals to surface behavioral patterns, emerging interests, stalled threads, and cross-domain opportunities that no single skill would notice on its own. It works by forming hypotheses, testing them against accumulated signals, and emitting validated proposals downstream to Praxis and Vesper for action and briefing.

## When to use

- Detect recurring behavioral patterns and routines
- Identify emerging interests from activity clusters
- Discover anomalies or meaningful deviations from established patterns
- Find cross-domain opportunities connecting previously unrelated entities
- Monitor stalled threads and incomplete activity clusters
- Run periodic analysis during idle cycles

## When not to use

- Web research or fact-checking — use Sift
- OSINT investigations on people — use Scout
- System architecture changes or skill evaluation — use Mentor
- Storing user preferences — use Taste
- Direct communication — use Dispatch

## Responsibility boundary

Corvus owns exploratory pattern analysis across the knowledge graph and skill journals.

Corvus does not own: skill evaluation (Mentor), behavioral refinement (Praxis), web research (Sift), knowledge graph writes (Elephas), preference persistence (Taste), browsing interpretation (Thread).

Corvus emits BehavioralSignal files to Praxis and InsightProposal files to Vesper. Corvus receives research thread signals from Thread.

## Commands

- `corvus.analyze.light` — run a light analysis cycle: routine detection, thread monitoring, interest clustering
- `corvus.analyze.deep` — run a deep exploration cycle: cross-domain traversal, hypothesis testing, model refinement
- `corvus.proposals.list` — list current insight proposals with confidence scores
- `corvus.proposals.detail` — show full evidence and reasoning for a specific proposal
- `corvus.hypotheses.list` — list active hypotheses under investigation
- `corvus.status` — return current analysis state: patterns detected, proposals pending, graph coverage
- `corvus.journal` — write journal for the current run; called at end of every run
- `corvus.update` — pull latest from GitHub source; preserves journals and data

## Operation modes

### Light Analysis Cycle
Runs frequently during idle periods. Focuses on routine detection, thread monitoring, and interest clustering. Low cost, fast execution.

### Deep Exploration Cycle
Runs less frequently during extended idle periods. Performs cross-domain graph traversal, hypothesis testing, and model refinement. Higher cost, produces richer insight proposals.

## Curiosity engine

Corvus prioritizes graph regions for exploration using three internal drives:

- **Novelty** — prefer regions that recently appeared or changed
- **Uncertainty** — prefer entities with many signals but incomplete understanding
- **Prediction error** — prefer patterns where predicted outcomes diverge from observed events

Each drive generates hypotheses. Hypotheses are tested through graph queries and evidence gathering. Validated hypotheses become insight proposals.

Read `references/curiosity_engine.md` for drive mechanics and priority scoring.

## Pattern validation rules

Patterns must pass all validation checks before becoming proposals:

- Minimum signal count met
- Temporal consistency confirmed
- Cross-domain corroboration present
- Falsification attempt completed without contradiction

Patterns failing validation remain internal hypotheses for future evaluation.

Read `references/pattern_engines.md` for per-engine detection criteria and validation rules.

## Insight proposal format

Each proposal includes: proposal_id, proposal_type, description, confidence_score, supporting_entities, supporting_relationships, predicted_outcome, suggested_follow_up.

Proposal types: routine_prediction, thread_continuation, opportunity_discovery, anomaly_alert, behavioral_signal.

Read `references/schemas.md` for exact proposal schema.

## Analysis cycle completion

After every analysis cycle (light or deep):

1. Persist hypotheses, patterns, and proposals to local JSONL files
2. For each validated pattern with `proposal_type: behavioral_signal`: write a BehavioralSignal file to `~/openclaw/data/ocas-praxis/intake/{signal_id}.json`
3. For each validated proposal reaching sufficient confidence (all types except `behavioral_signal`): write an InsightProposal file to `~/openclaw/data/ocas-vesper/intake/{proposal_id}.json`
4. Check `~/openclaw/data/ocas-corvus/intake/` for Thread research signals; process and move to `intake/processed/`
5. Write journal via `corvus.journal`

## Inter-skill interfaces

Corvus writes BehavioralSignal files to: `~/openclaw/data/ocas-praxis/intake/{signal_id}.json`
Written when a validated pattern has proposal_type: behavioral_signal.

Corvus writes InsightProposal files to: `~/openclaw/data/ocas-vesper/intake/{proposal_id}.json`
Written when a validated proposal reaches sufficient confidence (excludes behavioral_signal type).

Corvus receives research thread signals from Thread at: `~/openclaw/data/ocas-corvus/intake/{thread_id}.json`
Read during analysis cycles as additional signal context.

See `spec-ocas-interfaces.md` for schemas and handoff contracts.

## Storage layout

```
~/openclaw/data/ocas-corvus/
  config.json
  hypotheses.jsonl
  patterns.jsonl
  proposals.jsonl
  decisions.jsonl
  intake/
    {thread_id}.json
    processed/
  reports/

~/openclaw/journals/ocas-corvus/
  YYYY-MM-DD/
    {run_id}.json
```


Default config.json:
```json
{
  "skill_id": "ocas-corvus",
  "skill_version": "2.3.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "curiosity": {
    "novelty_weight": 0.4,
    "uncertainty_weight": 0.3,
    "prediction_error_weight": 0.3
  },
  "validation": {
    "min_signal_count": 3,
    "min_confidence_for_proposal": 0.5
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
  - name: proposal_precision
    metric: fraction of proposals confirmed as useful within 30 days
    direction: maximize
    target: 0.70
    evaluation_window: 30_runs
  - name: pattern_validation_rate
    metric: fraction of detected patterns passing all validation checks
    direction: maximize
    target: 0.80
    evaluation_window: 30_runs
  - name: graph_coverage
    metric: fraction of active graph regions analyzed within one deep cycle
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: false_anomaly_rate
    metric: fraction of anomaly alerts dismissed as noise
    direction: minimize
    target: 0.15
    evaluation_window: 30_runs
```

## Optional skill cooperation

- Elephas — read Chronicle (read-only) for graph context during pattern analysis
- Thread — receives research thread signals via intake directory
- Vesper — receives InsightProposal files via Vesper intake directory
- Praxis — receives BehavioralSignal files via Praxis intake directory
- Mentor — Mentor may read Corvus data for evaluation context

## Journal outputs

Observation Journal — all analysis cycles (light and deep).

## Initialization

On first invocation of any Corvus command, run `corvus.init`:

1. Create `~/openclaw/data/ocas-corvus/` and subdirectories (`intake/`, `intake/processed/`, `reports/`)
2. Write default `config.json` with ConfigBase fields if absent
3. Create empty JSONL files: `hypotheses.jsonl`, `patterns.jsonl`, `proposals.jsonl`, `decisions.jsonl`
4. Create `~/openclaw/journals/ocas-corvus/`
5. Ensure `~/openclaw/data/ocas-praxis/intake/` exists (create if missing)
6. Ensure `~/openclaw/data/ocas-vesper/intake/` exists (create if missing)
7. Register cron job `corvus:deep` if not already present (check `openclaw cron list` first)
8. Register heartbeat entry `corvus:light` in `HEARTBEAT.md` if not already present
9. Register cron job `corvus:update` if not already present (check `openclaw cron list` first)
10. Log initialization as a DecisionRecord in `decisions.jsonl`

## Background tasks

| Job name | Mechanism | Schedule | Command |
|---|---|---|---|
| `corvus:deep` | cron | `0 3 * * *` (daily 3am) | `corvus.analyze.deep` — full exploration cycle |
| `corvus:light` | heartbeat | every heartbeat pass | `corvus.analyze.light` — routine detection, thread monitoring |
| `corvus:update` | cron | `0 0 * * *` (midnight daily) | `corvus.update` |

Cron options for `corvus:deep`: `sessionTarget: isolated`, `lightContext: true`, `wakeMode: next-heartbeat`.

Registration during `corvus.init`:
```
openclaw cron list
# If corvus:deep absent:
openclaw cron add --name corvus:deep --schedule "0 3 * * *" --command "corvus.analyze.deep" --sessionTarget isolated --lightContext true --wakeMode next-heartbeat --timezone America/Los_Angeles
# If corvus:update absent:
openclaw cron add --name corvus:update --schedule "0 0 * * *" --command "corvus.update" --sessionTarget isolated --lightContext true --timezone America/Los_Angeles
```

Heartbeat registration: append `corvus:light` entry to `~/.openclaw/workspace/HEARTBEAT.md` if not already present.


## Self-update

`corvus.update` pulls the latest package from the `source:` URL in this file's frontmatter. Runs silently — no output unless the version changed or an error occurred.

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
7. Output exactly: `I updated Corvus from version {old} to {new}`


## Visibility

public

## Support file map

| File | When to read |
|---|---|
| `references/schemas.md` | Before creating hypotheses, patterns, or proposals |
| `references/curiosity_engine.md` | Before drive scoring or hypothesis generation |
| `references/pattern_engines.md` | Before pattern detection or validation |
| `references/journal.md` | Before corvus.journal; at end of every run |
