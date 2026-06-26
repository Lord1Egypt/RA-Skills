# V1 Schemas

## Agent YAML
Required keys:
- `name`
- `purpose`
- `best_for`
- `avoid_for`
- `default_model_category`
- `input_contract`
- `output_contract`
- `reviewer_for`

## Workflow YAML
Required keys:
- `workflow_id`
- `goal`
- `entry_conditions`
- `phases`
- `completion_conditions`

Optional keys:
- `retry_modes`
- `retry_targets`
- `escalation_rules`

### Phase fields
Required:
- `id`

Optional:
- `agent`
- `output`
- `parallelism`
- `orchestrator_decision`
- `optional_if`

## Run state JSON
Required keys:
- `run_id`
- `workflow`
- `goal`
- `status`
- `phase`
- `phase_index`
- `iteration`
- `active_agents`
- `canonical_artifacts`
- `last_decision`
- `next_action`
- `blockers`
- `history`
- `created_at`
- `updated_at`
- `context`

Optional but recommended keys:
- `project_root`
- `shared_context_files`
- `missing_context_files`

## Review markdown
Use `agent/orchestration/templates/review.md` and keep these headings:
- `## Verdict`
- `## Severity`
- `## Issues`
- `## Minimal fix scope`
- `## Classification`
- `## Recommended next step`

The parser in `scripts/orchestration/apply_review.py` depends on those headings.
