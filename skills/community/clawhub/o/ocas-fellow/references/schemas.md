# Fellow Schemas

This file contains the full YAML/JSON schemas referenced by the Fellow skill.
Keep this file alongside SKILL.md — it is the canonical source for experiment
invocation contracts, cycle outputs, configuration defaults, and OKR definitions.

---

## Invocation contract

Fellow is invoked only by Mentor. Invocation payload structure:

```yaml
target: <component_identifier>
program_id: <experiment_program>
objective: <primary_metric>
benchmark: <benchmark_identifier>
budget:
  type: wall_clock | task_count | token_budget | simulation_window
  value: <number>
constraints:
  max_variants: <number>
  max_cycles: <number>
  mutation_surface: [<path_or_field>]
  protected_surface: [<path_or_field>]
promotion:
  threshold: <minimum_improvement>
  automatic: <boolean>
  rollback_on_regression: true
runner:
  type: command | function | workflow
  entrypoint: <runner_entrypoint>
  timeout_seconds: <number>
metric_extractor:
  type: json | regex | function | structured_output
  source: <artifact_source>
  selector: <metric_path>
```

---

## Cycle output

At completion Fellow emits:

```yaml
cycle_id:
target:
baseline_score:
best_variant_id:
best_variant_score:
improvement:
decision: promote | no_change | abort
artifacts_ref:
rollback_ref:
```

---

## Storage layout

```
{agent_root}/commons/data/ocas-fellow/
  config.json
  experiments.jsonl
  decisions.jsonl
  requests_processed.jsonl
  intents.jsonl
  evidence.jsonl
  results/
    {cycle_id}.json
  runs/
    {cycle_id}/
      baseline/
      variant-001/
      variant-002/

{agent_root}/commons/journals/ocas-fellow/
  YYYY-MM-DD/
    {run_id}.json
```

---

## Default config.json

```json
{
  "skill_id": "ocas-fellow",
  "skill_version": "2.4.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "defaults": {
    "improvement_threshold": 0.03,
    "max_variants_per_cycle": 20,
    "max_cycles_per_target": 5,
    "max_parallel_runs": 1,
    "plateau_window": 5
  },
  "retention": {
    "days": 90,
    "max_records": 10000
  }
}
```

---

## OKRs

Universal OKRs from spec-ocas-journal.md apply to all runs.

```yaml
skill_okrs:
  - name: experiment_completion_rate
    metric: fraction of experiment cycles completing without abort
    direction: maximize
    target: 0.90
    evaluation_window: 30_runs
  - name: promotion_rate
    metric: fraction of completed experiments producing a promotable variant
    direction: maximize
    target: 0.30
    evaluation_window: 30_runs
  - name: baseline_stability
    metric: fraction of baselines completing successfully
    direction: maximize
    target: 0.99
    evaluation_window: 30_runs
  - name: schedule_adherence
    metric: fraction of cron runs executing within 5 minutes of scheduled time
    direction: maximize
    target: 0.95
    evaluation_window: 30_days
  - name: data_integrity
    metric: fraction of experiment records with complete, non-corrupted evidence
    direction: maximize
    target: 0.99
    evaluation_window: 30_runs
```

---

## Self-update procedure

`fellow.update` pulls the latest package from the `source:` URL in this file's frontmatter.

1. Read `source:` from frontmatter → extract `{owner}/{repo}` from URL
2. Read local version from SKILL.md frontmatter `metadata.version`
3. Fetch remote version from SKILL.md frontmatter:
   ```bash
   gh api "repos/{owner}/{repo}/contents/SKILL.md" --jq '.content' | base64 -d | grep 'version:' | head -1 | sed 's/.*"\(.*\)".*/\1/'
   ```
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
7. Output exactly: `I updated Fellow from version {old} to {new}`
