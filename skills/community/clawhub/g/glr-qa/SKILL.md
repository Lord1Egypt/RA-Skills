---
name: glr-qa
description: Run goal-driven GameLearningRuntime QA against an authorized game, training adapter, replay, or live probe and produce a dated JSON plus self-contained HTML report. Use when a player asks whether a game works well, wants bug discovery, regression checks, or evidence from bounded training runs.
license: MIT
---

# GLR QA

Turn a plain-language objective into bounded, inspectable QA evidence. Preserve the
boundary between deterministic checks, scripted replay, training metrics, and
live-host acceptance; a passing smoke command is not proof that the whole game is
complete.

1. Restate the goal and identify the authorized project/adapter and evidence scope.
   Resolve the nearest `glr-project.toml` or legacy `glr-project.json`; do not infer
   a root from an adapter folder name. Reject ambiguous manifests. Keep machine
   paths and local overrides out of shared reports, even when doctor prints them.
2. Choose finite checks (for example adapter doctor, deterministic regression,
   replay, and an explicitly bounded training probe). Never invent credentials,
   game internals, or unrestricted automation.
3. Run the checks with `python -m game_learning_runtime.qa` or call
   `game_learning_runtime.qa.run_qa`. Use `--project` for the adapter working
   directory and one or more `--check NAME COMMAND...` arguments.
4. Inspect `result.json` and open `index.html` from the generated
   `.glr-qa/YYYY-MM-DD/<time>/` directory. Report failures with their command
   output, duration, and likely next investigation; report missing live evidence
   as an evidence gap.

Example:

```powershell
# Install GLR and the downstream package in the selected environment first.
python -m game_learning_runtime.qa "inspect the whole game for bugs" `
  --project . `
  --check doctor glr --project . doctor `
  --check regression python -m pytest tests/test_runtime_integration.py -q `
  --check training python -m your_adapter.train --steps 1000
```

Do not claim release quality from this report alone. Keep proprietary traces and
secrets out of artifacts; publish only evidence the project owner authorized.

For trained-stage installers, read `USER_RELEASE.md`. Verify installation,
startup without source/system Python, inference parity, frozen mode, missing
prerequisites, offline operation, version rollback, and uninstall preserving user
data. Report synthetic installer tests separately from real application and
authorized live-game acceptance.

## Verify workbench collection

- Inspect the installed `glr --json telemetry schema` before assuming a view or
  reporting feature exists. Read the `glr-cli` Skill's
  `references/data-collection.md` when that Skill is installed.
- Read back `glr --json telemetry state RUN_ID` and
  `glr --json runs trace RUN_ID --events-after -1 --metrics-after 0` with complete
  cursor traversal. Match run/environment, source, episode and step before
  correlating events, metrics, capture frames or evaluator outcomes.
- Inspect legacy JSONL through Process logs or `glr --json runs log RUN_ID
  --path trainer.log --offset 0`. Continue byte cursors; a rendered 64 KiB tail,
  filtered record set or browser export is not the complete history. Confirm
  truncated/partial records are labelled rather than silently dropped.
- Check one actual event/metric, source-state update and registered artifact.
  Reopen the observer and verify a completed-run backup to test persistence.
  Do not fabricate diagnostics or start a live game merely to populate cards.
- A successful ingest, rendered workbench, or process receipt does not establish
  action success, effective learning or capture alignment. Report missing source
  instrumentation separately from frontend rendering defects.

## Training capture profile

For imported projects, use the sibling [package workflow](../glr-cli/references/packages.md).
Record package validity separately from dependency readiness, synthetic conformance,
live acceptance and model quality. Import does not execute a QA check, and
`package conformance` is not a QA result: it verifies the envelope, the
materialized tree, the declared locks and the prerequisites, and reports
`training`, `live_acceptance` and `policy_quality` as `not-evaluated`. Exit `0`
means the synthetic conformance check passed; `4` means reproduction is blocked
and `blockers` names the axis. A blocked reproduction is still a valid, fully
materialized package — report both halves rather than one verdict. A `model`
group admitted into a package proves artifact identity, not policy quality.

Before configuring or running recorded training, read the sibling
[GLR CLI recording contract](../glr-cli/SKILL.md#recording-and-training-data).
Resolve `glr capture preset` and `glr capture layout` from the authorized project.
Use `training-balanced` by default and verify the actual finalized video and
checksummed frame index before claiming training-data readiness.

For downstream training projects, inspect their `QUALITY.md` and include static,
installed-wheel, offline training-regression, and applicable logging/monitoring
checks. Missing packaging, source-path injection, or untested queue/rotation
failure paths are quality gaps even when existing source-tree tests pass.
