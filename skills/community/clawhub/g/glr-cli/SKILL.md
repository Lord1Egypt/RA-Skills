---
name: glr-cli
description: Configure and operate the GameLearningRuntime agent-first CLI for bridge startup, bounded goal-driven research and training, concurrent review capture, run queries, spatial knowledge transfer, and verified model playback. Use for operating an existing GLR project; use glr-adapter-builder when implementing the game adapter itself.
---

# GLR CLI

Operate GLR through the standalone Rust control plane while preserving the
adapter/learner boundary. The `glr` executable is the canonical deployment and
Agent entrypoint; Python is an optional SDK for project roles, not a CLI runtime
dependency.

## Resolve bundled files portably

This Skill is distributed from both GLR releases and Agent Plugin packages.
Resolve its `references/` directory relative to the directory containing this
`SKILL.md`; do not assume a repository checkout or a user-profile install
path. The `--skills-dir` option below is a project-owned destination for an
explicit update and is separate from the host's installed plugin directory.

Read [references/commands.md](references/commands.md) before creating a project config,
running a goal, transferring knowledge, or claiming reproduction.

## Select the correct boundary

- For a trained-stage installer, read the project's `USER_RELEASE.md`,
  `ARCHITECTURE.md`, and migration records. Use the adapter-builder release
  reference if absent. Source import and model checksums do not prove that an
  installed inference application works. Keep versions immutable and migrations
  explicit; do not invent unsupported release CLI commands.

- Use this Skill when the project already has a reviewed runtime bridge and needs CLI setup or
  operation.
- Use `glr-adapter-builder` when implementing or changing observation, action, lifecycle,
  transport, target binding, or post-action verification.
- Never make the game adapter import a learner algorithm. The configured trainer, planner,
  researcher, evaluator, recorder, and player remain explicit project-owned processes.

## Operate agent-first

1. Run `glr --version`, resolve the nearest `glr-project.toml` (legacy JSON is
   also supported), and run
   `glr --project . --json doctor`; do not guess a bridge path or game target.
2. Inspect the strict project roles and exact `environment_id`, `environment_family`, and
   `protocol_version` before execution.
3. When `doctor.data.lifecycle` is present, treat it as the loaded-input manifest:
   verify every config owner, path, schema version, and SHA-256, then use only the
   listed lifecycle modes. A missing mode is a shared GLR capability gap; do not
   create a project-local `run_*.py` lifecycle wrapper to bypass it.
4. When one invocation selects a configuration set, pass a reviewed
   `--context config/contexts/NAME.toml`. Treat `doctor.data.run_context` as the
   frozen `glr.run-context.v1` receipt. Python roles must call
   `load_inherited_run_context(project)` before consuming selected inputs.
5. Use `glr runtime start` only for the configured fixed-argv runtime command. Its process exit
   proves command completion, not a live bridge handshake or gameplay success. When the project
   declares `runtime.readiness`, an exit code of `78` means the declared window expired while the
   role still reported `not_ready`: the host was starting, not broken, so wait and retry instead of
   reporting a defect.
6. Express the user objective as `glr.agent-goal.v1` with machine-readable success criteria and
   hard trial, step, time, and research-source budgets.
7. Run `glr goal run`. Let the project researcher gather only allowed sources; let the planner
   emit declarative reward terms; require the trainer/runtime to persist metrics; accept success
   only when evaluator evidence matches those persisted authoritative metrics.
8. Inspect `glr runs show` and query entities, routes, or research before deciding the next action.
   Route and guide results are hints; re-observe and verify postconditions in the live runtime.
9. Use a verified model bundle for playback. A valid hash proves artifact integrity and config
   identity, not policy quality, hardware determinism, or successful live gameplay.

## Pin the project entry point

When `doctor.data.entry_point.status` is not `undeclared`, the project pins one
entry point and the launching process should claim it with `GLR_ENTRY_ID` — a
non-strict project still runs and records `entry_drift`. A
`entry_drift` verdict means the run did not come through the declared door; never
work around it by editing the manifest to match whatever command you happened to
run. `doctor` reports the drift but only fails on it when `strict = true` — it is
a diagnosis, not a run, so it never carries `GLR_ENTRY_ID`. With `strict = true`
the run is refused with exit code `79` before any run row exists — fix the
launcher, then retry. An invariant reporting `multiple`
names every offending path; converge on one home rather than deleting the
constraint. Read [references/commands.md](references/commands.md) for the
declaration form.

## Run project-local tasks through VX

- When the project contains `glr.toml`, run `glr --project . --json task list`
  before assuming a project workflow is missing.
- Inspect a task with `glr task show NAME`, then pass only declared values with
  repeated `--set NAME=VALUE` arguments.
- Prefer `runner = "vx"` with `argv = ["uv", "run", ...]` for Python training
  workflows. VX owns Python/tool versions and the project environment; GLR owns
  validation, dependency ordering, timeouts, logs, and receipts.
- A project task is not a core GLR command. Successful `glr task run season`
  proves process completion only; require authoritative run/evaluator evidence
  before claiming the season or gameplay objective succeeded.
- Keep season, ruleset, league, experiment, and campaign concepts in task
  parameters or context labels. Do not invent top-level product-specific CLI
  commands for them.
- Never rewrite a fixed argv task as a shell string or execute a remote task
  catalog. Treat `glr.toml` as trusted repository configuration.

## Keep the managed runtime current

- Before a framework upgrade, read the project's `QUALITY.md`,
  `FRAMEWORK_MIGRATION.md`, and `MIGRATIONS.md`. If absent, use the
  `glr-adapter-builder` migration reference to establish these contracts first.
  Record installed/target versions, code/config/data/checkpoint compatibility,
  consistent backups, staged validation, and rollback. Updating a CLI binary
  alone does not prove downstream migration. Do not implicitly downgrade a
  project to match an older checkout or modify a live store with active writers.


- Ordinary commands check for newer releases in the background and print a
  `glr update` hint to stderr. Successful checks are cached for 24 hours;
  failures cool down for one hour. Command completion waits at most one second
  for the notice, and failures do not change the command exit code or JSON stdout.
  Set `GLR_NO_UPDATE_CHECK=1` to disable; CI skips automatic checks.
- `glr update --check` is a read-only release check and is safe to use when
  diagnosing version drift.
- Run `glr update` only when the user explicitly asks to update GLR. It
  verifies the exact platform archive and `SHA256SUMS`, then updates the `glr`
  executable, its sibling `glr-hostd`, and the repository-owned `glr-cli`,
  `glr-adapter-builder`, and `glr-qa` Skills.
- If the binaries are already current, `glr update` still synchronizes the
  configured project Skills from the verified release archive.
- Use `--skills-dir` only for an explicitly selected project Skills directory.
  Use `--no-skills` when the user requested binary-only maintenance.
- Without a discoverable project, update requires `--skills-dir` or the explicit
  `--no-skills` opt-out; never report skills updated unless `skills_updated` is
  true. Invalid or ambiguous project manifests must be fixed, not ignored.
- The updater does not modify game code, project role dependencies, Python
  environments, models, datasets, project manifests, or trainer configuration.
- SHA-256 protects same-release artifact integrity; it is not publisher
  signature verification. Report the first unified-release smoke boundary when
  no matching target archive exists yet.
- Public checks use GitHub's latest-release asset link rather than the REST API,
  so they do not consume anonymous API quota. The updater derives the version,
  exact target archive, and digest from the published `SHA256SUMS`.

## Preserve knowledge scope

On a knowledge-enabled decision, persist the injector's query fingerprint,
trigger/hit counts, selection counts, and rejection counters with the step.
No invocation, a valid zero-hit lookup, and a rejected stale source are distinct
states. Knowledge-file presence is not a trigger or a hit; a hit is not learning.

- Environment-scoped positions and routes transfer only across the exact environment and protocol.
  Imports are downgraded to advisory until the new runtime observes them again.
- Family-scoped tutorial/guide findings may inform a similar game, but never transfer coordinates,
  action authority, or model compatibility.
- Keep public source provenance, access time, compact paraphrases, confidence, volatility, and
  runtime-verification status. Never store credentials or full copied guides.
- Exclude rejected findings. Treat unverified findings as hypotheses, never authoritative reward
  or success evidence.

## Portable project handoff

For offline handoff, follow [packages](references/packages.md). It covers both
the source-only profile (`glr.source-package.v1`) and the group-scoped profile
(`glr.training-package.v1`), which adds the deny-by-default `model`, `dataset`,
`knowledge` and `report` groups behind per-group admission proofs.

The workflow is `plan` → `export` → `inspect` → `import` → `conformance`, and
none of them executes, installs, downloads or deserializes. Import refuses an
existing destination. Report package validity, dependency setup, synthetic
reproduction, live acceptance and model quality as separate results: a valid
package is never a successful training run, and a checksum proves integrity,
not publisher trust.

New projects use a single `glr-project.toml`. Before migration, verify the
installed CLI and Python SDK support TOML; unreleased source changes do not
upgrade installed tools. Never leave JSON and TOML manifests side by side.
Use `GLR_PROJECT_MANIFEST` or `find_project()` to locate the project; resolve
relative config paths from its parent, not cwd or a fixed number of parents.
Read the portable layout and clone gates in [commands.md](references/commands.md)
when scaffolding, migrating environments, or handing a project to another user.

## Recording and training data

Read [VX recording and acceptance](references/recording.md) before configuring
capture or declaring recorded material ready for training or agent QA. Run all
FFmpeg/ffprobe operations through `vx ffmpeg` / `vx ffprobe`.

When capture is configured, keep it enabled for `glr train` and `glr goal run` unless the user
explicitly opts out. The recorder is a concurrent project-owned sidecar and must emit both an
H.264 MP4 and `glr.capture-frame.v1` step/frame index. A video without a valid checksummed index is
review media, not supervised-learning data.

Before wiring or operating capture, run `glr --project . --json capture preset` and
`glr --project . --json capture layout`. Use `training-balanced` unless measurements justify
another preset. Keep video, frame index, logs, datasets, and reports below the returned run
directory; durable model, loader, and knowledge exports belong below the returned
`.glr/exports/` root. Do not invent game-specific recording, export, or report roots.

The default `training-balanced` profile is 1920x1080, 30 FPS CFR, H.264/libx264,
CRF 18, `fast`, yuv420p, GOP 30 with fixed keyframes, MP4 fast-start, and no audio.
Treat `capture preset` output as authoritative and apply its output arguments to
the recorder; config width/height/frame_rate fields alone do not configure a provider.
Preserve the game aspect ratio when fitting the output canvas.

Before training, verify the exact game-window binding and a nonblank captured frame.
For DCC-CUA UI operations, report provider, runtime version, PID, and HWND before
observation or input. Keep these machine-local identifiers out of public artifacts.
After capture stops cleanly, inspect the actual stream with ffprobe for codec,
dimensions, pixel format, frame rate, duration, and audio absence; inspect frames
for readable UI and correct framing. Validate the checksummed step/frame index
against the run before classifying video as training data. Configuration or an
active recording flag alone is not successful recording evidence.

Do not claim live-game acceptance from synthetic tests, process exit, video presence, run status,
or model hashes. Report the exact remaining runtime acceptance boundary.

## Build an offline run report

Generate a self-contained, interactive review page from one completed run:

```powershell
glr --project . --json report build <run-id>
glr --project . --json report build <run-id> --output review/report
```

The default output is `.glr/runs/<run-id>/report/index.html`; a custom output
must remain inside that run directory. Before writing, GLR verifies every
registered evidence artifact's portable path, byte size, and SHA-256 digest,
omits prior `run-report` outputs to avoid self-referential hashes, then
registers the HTML as a `run-report` artifact. The page is offline and
filterable: it summarizes metrics, renders `navigation.route_sample` points,
shows `progression.*` unlock/catalog events, lists explicit `match.result`
records (including `match_kind=pvp`), and links authorized screenshots or
videos by their checksummed artifact paths.

Reports are projections over the run store, not a second source of truth. They
do not mutate training data, infer missing unlocks or wins, widen action masks,
or establish live-game acceptance. Keep unsupported panels empty and return to
the adapter/runtime boundary when authoritative evidence is missing.

## Dashboard, telemetry, and durable history

Read [data collection and rendering](references/data-collection.md) before wiring
Bridge/learner reporting, interpreting process output, adding workbench panels,
or diagnosing missing data. It covers HTTP/CLI/SDK ingestion, media registration,
legacy JSONL, FFmpeg output, cursor readback and backup boundaries.

- Start `glr dashboard` for human controls; agent commands remain the same CLI
  contracts. Dashboard forms are derived from clap. `train` and `goal run` start
  a command-lifetime read-only observation server unless `--no-observe` is explicit.
- Inspect `glr dashboard presets`, `glr dashboard jobs`, and `glr runs trace RUN_ID`.
  Continue independent event/metric cursors until `more` is false; the browser's
  5000-record window is not a complete export. `runs log` supports byte offsets.
- Python learners can use `Telemetry.from_env()` for explicit learning updates
  and routes. `execute_decision(..., step_id=...)` records choices/receipts when
  GLR run bindings exist. Diagnostic metrics never establish runtime success.
- Keep recorder stderr connected so capture.log exposes FFmpeg diagnostics.
  `GLR_LOG_STDERR=0` only disables terminal mirroring, not durable storage.
- Use `backup create --output PATH`, `backup verify PATH`, and `backup restore PATH
  --output NEW_PATH` for history. Active runs are database-only; make another
  backup after completion for finalized capture/checkpoint files. No automatic
  deletion, scheduling, live-state restore, or retraining is implied.
- Use `observe --archive PATH` and `runs trace RUN_ID --archive PATH` for verified
  archive inspection. Source project packaging remains `package export/import`;
  include exported preset JSON explicitly in the source selection. After a
  recipient imports into a new directory, `package conformance ARCHIVE` reports
  package validity, materialization, ignored local overrides, declared locks and
  prerequisites as separate axes, and carries the `glr.package-audit.v1` receipt
  naming every admitted non-source file. It never installs, resolves or trains,
  and it never reports a package as training success. Exit `0` means the
  synthetic conformance check passed; `4` means reproduction is blocked.
- A crashed Dashboard can leave an unverified job and active child. Inspect and
  reconcile, never resubmit automatically or treat process exit as learning success.
