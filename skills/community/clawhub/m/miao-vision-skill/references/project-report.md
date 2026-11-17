# Project periodic reports

Use this workflow for a single project's weekly or monthly task report. Require a complete task snapshot, stable task IDs, explicit status mappings and date boundaries. Incremental event exports are not full snapshots.

Start from `test_data/project_reports/config.json` in repository development, or ask the user for source column names and explicit status meanings. Save a local `project-config.json` with schemaVersion 1, projectId, name, IANA timezone, fields and statusMapping. Required field mappings are task_id, title, status, due_date. Optional mappings are start_date, owner, completed_at, stage, is_milestone, next_action, action_due_date and blocker. Mapped columns must exist; optional values may be empty. Dates are YYYY-MM-DD; real XLSX date cells are normalized. Milestones accept true/false or 1/0. Status targets are todo, in_progress, done, blocked and cancelled.

First report:

```bash
miao-viz data analyze ./tasks.csv --project-config ./project-config.json \
  --period-start 2026-10-01 --period-end 2026-10-07 --output ./context.json
miao-viz data profile ./tasks.csv > ./profile.json
miao-viz spec block instantiate project-status --context ./context.json --output ./report.yaml
miao-viz spec validate --spec ./report.yaml --profile ./profile.json --context ./context.json --verify
miao-viz render report --input ./tasks.csv --spec ./report.yaml --context ./context.json --output ./report.html
miao-viz report init ./delivery-weekly --input ./tasks.csv --spec ./report.yaml \
  --context ./context.json --project-config ./project-config.json --period 2026-W40 \
  --period-start 2026-10-01 --period-end 2026-10-07
```

For XLSX, specify `--sheet` when analyzing and initializing. It is saved for future updates. With typed XLSX dates, the ordinary profile may classify date cells as numbers; the explicitly temporal project encodings still undergo project date validation.

Later periods reuse the saved configuration and report structure:

```bash
miao-viz report update ./delivery-weekly --input ./tasks-next.csv --period 2026-W41 \
  --period-start 2026-10-08 --period-end 2026-10-14
```

Use `--format html,pdf` to request matching HTML and PDF. PDF uses the existing Playwright/Chromium export path. Missing browser dependencies return structured errors; do not silently report a failed PDF as delivered.

The report includes a read-only kanban grouping tasks by todo, in progress, blocked and done, with owners, deadlines, blockers and recorded changes. Cancelled tasks are excluded from the board; completed tasks beyond the first six can be expanded. It also includes a task-count completion ratio, status distribution, Gantt, milestones, completion facts, task changes, problems and source-provided actions. Date points represent tasks without start dates. Tasks without due dates appear as unscheduled. The main Gantt prioritizes milestones, blocked and overdue tasks and shows up to 15 entries. The full schedule is expandable and paginated for print. Pale bars are the frozen first-run baseline, not actual duration. Completion status is not client acceptance. Never call task completion ratio overall project completion progress.

Dates are evaluated at the supplied reporting cutoff, not the execution date. Completed tasks without completion dates cannot be assigned to this period. Missing task IDs in a later snapshot require review and are never interpreted as completed or cancelled. Source issues and evidence references remain available in the report; run-level files stay local.

Inspect `value.status`, `value.projectBrief` and `review.json` before sharing. `ready` means material and rule validation passed, not that the project has no business risk. No automatic owner, deadline, cause, critical path or forecast is invented.

Historical reports do not move the latest pointer backward. To correct an existing logical period, use a new safe run ID and `--replaces-run <previous-run-id>` with the same date boundaries; previous artifacts remain intact. Revision branches are rejected. Comparison uses the most recent earlier non-overlapping successful period with matching configuration; superseded revisions are ignored. A baseline needing review is identified in the report.

Use `report info`, `report history` and `report clean` as for ordinary recurring reports. Source material is copied only with `--copy-input`; normalized snapshots and frozen baseline schedules are stored locally regardless, because they are needed for task comparisons. Changing saved configuration or baseline files invalidates their hashes; create a new project for a new task identity or reporting meaning.
