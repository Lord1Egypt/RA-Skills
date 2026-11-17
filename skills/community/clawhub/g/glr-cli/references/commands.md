# GLR CLI command and contract reference

## Install and inspect the standalone distribution

Download `glr-{version}-{rust-target}.zip` and `SHA256SUMS` from the matching
GitHub Release, verify the archive digest, extract it, and put `glr` plus
`glr-hostd` on `PATH`. The archive also contains all three repository-owned Skills (`glr-cli`, `glr-adapter-builder`, `glr-qa`)
under `skills/`; no Python installation is required to run the CLI.

Start every project operation with:

```powershell
glr --version
glr --project . --json doctor
glr --json update --check
```

`doctor` verifies the strict project file, bridge path, data directory, and
configured executable roles. It also resolves each configured role's declared
`environment` table and exits non-zero when a declared variable cannot be
resolved. It does not prove a live bridge handshake or game acceptance.

Only after an explicit user update request, apply the exact-target release:

```powershell
glr --json update
glr --json update --skills-dir .agents/skills
glr --json update --no-skills
```

The default update scope is the CLI, sibling Runtime Host, and project Skills.
Outside a discoverable project, an apply request fails before downloading unless
`--skills-dir` or `--no-skills` is supplied. `--check` remains project-independent.
`--skills-dir` must name an explicitly selected project Skills directory; it
does not update a user-level Agent Plugin installation. Use the host's plugin
manager to replace a plugin package, or copy the package's `skills/` payload
into the project directory intentionally before running a project update.
The updater requires HTTPS, a matching target manifest, and the published
`SHA256SUMS`; it never runs an installer script or changes project/trainer data.
The former `--yes` form remains accepted for compatibility.
When binaries are already current, an explicitly resolved project Skills
directory is still synchronized from the verified release archive.
Re-run `--version`, `doctor`, and `update --check` after an update.

The public release check uses GitHub's latest-release asset link instead of the
REST API, so it does not consume anonymous API quota. The updater derives the
version, exact target archive, and digest from the published `SHA256SUMS`.

### Automatic version notices

Normal subcommands run a best-effort background release check. The cache at
`~/.glr/cache/update-check.json` is scoped to binary version and platform target:
24 hours after success, one hour after failure. Notifications go to stderr,
including with `--json`; stdout and command exit codes are unchanged. Completion
waits at most one second for the worker (the HTTP request has an 800 ms timeout).
Offline failures are silent. Set `GLR_NO_UPDATE_CHECK=1` to disable automatic
checks; presence of `CI` also disables them. Help, version, parse errors, and the
explicit `update` command do not start a second automatic check.

A notice never installs anything. `glr update` performs its own fresh checksum
verification and synchronizes the selected project's bundled skills, including
at an equal version; a newer local binary never installs older release skills.

## Project configuration

New projects use `glr-project.toml`, with the same strict `glr.project.v1` schema
as legacy `glr-project.json`. Discovery searches upward from any project
subdirectory and stops at the nearest manifest. Two manifests in one directory,
symlinked manifests, and unknown fields are rejected. In TOML, omit optional
roles or capture tables instead of writing JSON `null`.

Every command is a fixed argv array executed without a shell; placeholders
occupy a whole argv element. Paths are manifest-relative and remain inside the
project. The following JSON example is retained for existing configurations;
new projects should use the equivalent TOML layout below.

```json
{
  "schema_version": "glr.project.v1",
  "environment_id": "example.adventure-v1",
  "environment_family": "action-rpg",
  "protocol_version": "1.0",
  "data_dir": ".glr",
  "bridge_path": "bridge",
  "environment": {"RENDER_DEVICE": "cpu", "DATASET_ROOT": "${LOCAL_DATA_CACHE}/v1"},
  "runtime": {"argv": ["python", "tools/runtime.py", "{bridge_path}"]},
  "trainer": {
    "argv": ["python", "tools/train.py"],
    "environment": {"RENDER_DEVICE": "cuda"}
  },
  "player": {"argv": ["python", "tools/play.py", "{bundle}"]},
  "researcher": {"argv": ["python", "tools/research.py", "{research_path}"]},
  "planner": {"argv": ["python", "tools/plan.py", "{trial_path}"]},
  "evaluator": {"argv": ["python", "tools/evaluate.py", "{evaluation_path}"]},
  "capture": {
    "argv": ["python", "tools/record_window.py", "{capture_video}", "{capture_index}"],
    "required": true,
    "stop": "stdin-q",
    "video_file": "capture.mp4",
    "index_file": "capture-index.jsonl",
    "codec": "h264",
    "frame_rate": 30,
    "width": 1920,
    "height": 1080
  },
  "lifecycle": {
    "schema_version": "glr.lifecycle.v1",
    "configs": [
      {"owner": "training", "path": "training.json", "schema_version": "glr.training.v1"},
      {"owner": "reward", "path": "reward-safety.json", "schema_version": "glr.reward-safety.v1"}
    ],
    "modes": ["train", "goal-evaluate", "frozen-playback"]
  }
}
```

The optional `environment` table declares what a role receives. A literal passes
through unchanged; `${NAME}` is interpolated from the process environment; a
missing reference fails the run before the role starts. A role table overrides
the project table key by key. The real process environment outranks both, and
`GLR_*` keys are rejected at load time because the CLI owns that namespace.

`lifecycle.configs` gives each project input exactly one owner. `doctor` rejects
missing files, schema drift, duplicate owners, shared paths with conflicting
owners, unsupported modes, and duplicate required role entrypoints. Its JSON
output includes a SHA-256 manifest of the files it actually loaded. Existing
`glr.project.v1` files without `lifecycle` remain compatible, but generated
projects always include it.

The example recorder argv is illustrative. A real recorder must target the reviewed game window
and write the paths provided by `GLR_CAPTURE_VIDEO` and `GLR_CAPTURE_INDEX`. Do not insert window
discovery, arbitrary scripts, secrets, or shell expressions into the config.

Project roles receive `GLR_PROJECT_ROOT`, `GLR_BRIDGE_PATH`, `GLR_RUN_ID`, `GLR_RUN_DIR`,
`GLR_STORE_PATH`, environment identity variables, and role-specific `GLR_*_PATH` variables.
They also receive `GLR_PROJECT_MANIFEST`, with the selected absolute manifest
path, and may use the whole-argument `{project_manifest}` placeholder. These
machine-local paths are process context, not publishable training evidence.
On Windows, canonical paths can use extended-length or UNC syntax. Compare
filesystem identity with `Path.samefile()` when files exist, not raw strings.
If a reviewed legacy launcher requires another spelling, adapt it only at that
launcher boundary. A path-format or identity-check failure is not evidence that
the game is absent and must never cause an automatic second launch.

### Portable layout, extensions, and local paths

```toml
schema_version = "glr.project.v1"
environment_id = "example.environment-v1"
environment_family = "example-family"
protocol_version = "1.0"
data_dir = ".glr"
bridge_path = "src/example_adapter"

[runtime]
argv = ["uv", "run", "--frozen", "python", "-m", "example_runtime"]
[trainer]
argv = ["uv", "run", "--frozen", "python", "-m", "example_training"]
[player]
argv = ["uv", "run", "--frozen", "python", "-m", "example_playback", "{bundle}"]

[extensions.example]
config = "config/runtime.toml"
```

Each extension has exactly one `config` field: an existing, portable relative,
non-symlink file inside the project. GLR checks the mount; the named extension
owns the file's strict schema and actions. Python exposes the resolved file as
`load_project(path).extensions["example"]`. No arbitrary plugin import or script
execution is loaded from an extension reference.

Keep a default game directory such as `game` in the extension config. If a
different installation is required, let that extension accept only an explicit
`[game] directory` override in `config/runtime.local.toml`, ignored by version
control. Do not recursively merge arbitrary local fields, commands, credentials,
policy, or reward settings. GLR does not automatically load local overrides.
`resolve_game_directory(project.root, configured_directory)` accepts an existing
project-owned relative directory or an explicitly configured absolute directory;
relative escapes are rejected. It never installs, discovers, or launches games.

### Startup readiness for a cold host

The runtime role may declare a bounded startup window instead of re-implementing
one with a private settle constant:

```toml
[runtime]
argv = ["uv", "run", "--frozen", "python", "-m", "example_runtime"]

[runtime.readiness]
timeout_seconds = 300
poll_interval_seconds = 5
file = "runtime-readiness.json"
```

`timeout_seconds` is required, positive, and at most one hour; the poll interval
and receipt name default to `5` and `runtime-readiness.json`. Without the table,
`runtime start` invokes the role once and the role exit code decides the run.

Within the window, each invocation receives `GLR_READINESS_PATH` and
`GLR_READINESS_ATTEMPT` and publishes one `glr.environment-readiness.v1` receipt
at that path: `{"schema_version", "state", "reason", "checked_at_ns"}` where
`state` is `ready`, `not_ready`, or `unavailable`. Only `not_ready` means "come
back". `ready` with a non-zero exit, `unavailable`, an off-schema, unreadable,
oversized, or absent receipt are terminal on first observation; never retry
those. A role that brings up a cold host should refuse with a named non-zero
code plus a `not_ready` receipt rather than sleeping inside itself.

The verdict is durable evidence: one `readiness.attempt` event per invocation
and one `readiness.outcome` event in the run, plus a `readiness` object in the
`runtime.start` payload. An exhausted window returns exit code `78` (host still
parking: retry later); every other verdict keeps the role exit code. Read
`glr runs show` before concluding that a start is broken.

Commit the root manifest, package metadata, dependency locks, generic default
config, tests, and project-owned setup instructions. Do not copy a virtualenv:
recreate it from the lock after clone. Keep adapters as importable semantic
packages, not owners of hidden shared environments. Before removing an old
environment, verify the new interpreter/module origins and run synthetic tests,
`doctor`, bounded training, and artifact verification from a different checkout
path and a nested working directory. Game payloads, local paths, credentials,
private traces, and licensed assets are not implied to be redistributable.

Fresh-clone acceptance has separate gates: dependency setup; config/doctor;
synthetic training/reproduction; authorized live runtime binding; whole-match
evidence. Report which gate ran. TOML source support must be built/released and
adopted by the consumer before claiming its installed GLR is compatible.

### Pinned entry point and single-owner invariants

A project may pin the one entry point allowed to launch it, so a fresh agent
context cannot drift onto a stale launcher:

```toml
[entry_point]
schema_version = "glr.entry-point.v1"
id = "campaign-driver"
command = "python -m campaign.driver"
version = "1.4.0"
strict = false

[[entry_point.invariants]]
id = "single-learner"
root = "src"
suffix = ".py"
marker = "class Learner"
```

`command` is provenance text GLR reports; it never executes it. The launching
process claims its door with `GLR_ENTRY_ID` and optional `GLR_ENTRY_VERSION`.
The attestation is `undeclared` (nothing declared, nothing compared), `matched`,
or `entry_drift` — a run that claims nothing at all is drift, not an unknown.

An invariant asserts that exactly one file under `root` contains the literal,
case-sensitive `marker`. It reports `ok`, `missing`, `multiple`, or `truncated`,
and `multiple` names every matching path. The scan stays inside the project,
skips `.git`/`target`/`node_modules`/`.venv`/`__pycache__`, never follows
symlinks, and is bounded (32 invariants, 32 levels, 20 000 files, 64 MiB total,
1 MiB per file); exceeding a bound is `truncated` and fails closed.

Invariant results always decide `glr doctor`'s verdict: exit `0` when every
included check passes, `4` when any fails. The attestation is **reported, and
gates only when `strict = true`** — `doctor` is a diagnosis, not a run, so it
never carries `GLR_ENTRY_ID`, and a non-strict project must not fail every round
for pinning an entry point. Read `doctor.data.entry_point` for `status`,
`declared`, `observed`, `strict`, `ready`, `invariants`, and `elapsed_ms`;
`doctor.data.last_run` carries the previous run's verdict with its own
`entry_point` attestation, and is reported without gating. With `strict = true`,
a drifting run is refused before the run row is created, with exit code `79`;
nothing is recorded and no budget is consumed. Absent an `[entry_point]` table,
every project behaves exactly as before.

## Commands

Use `--json` for compact `glr.cli-output.v1` output.

```powershell
glr --project . --json doctor
glr --project . --json capture preset
glr --project . --json capture layout
glr --project . --json runtime start
glr --project . --context config/contexts/ranked.toml --json doctor
glr --project . --context config/contexts/ranked.toml --json train
glr --project . --json task list
glr --project . --json task show season
glr --project . --json task run season --set profile=example/default
glr --project . --json train
glr --project . --json train --no-capture
glr --project . --json goal run --goal goals/reach-destination.json
glr --project . --context config/contexts/ranked.toml --json goal set --goal goals/reach-destination.json
glr --project . --json goal show
glr --project . --json goal list
glr --project . --json goal use goal.reach-destination
glr --project . --json goal run
glr --project . --json runs list --status succeeded --limit 20
glr --project . --json runs show run-0123456789abcdef
glr --project . --json query entities --world forest --kind shrine --name 土地庙
glr --project . --json query routes --world forest --to-entity shrine.forest-1
glr --project . --json query research --tag navigation --category strategy
glr --project . --json query research --verified-only
glr --project . --json knowledge export --output .glr/exports/knowledge/spatial-knowledge.json
glr --project . --json knowledge import --input .glr/exports/knowledge/spatial-knowledge.json
glr --project . --json play --bundle .glr/exports/model-bundles/model-bundle
glr --project . --json report build run-0123456789abcdef
glr --project . --json package plan --manifest selection.json
glr --project . --json package export --manifest selection.json --output source.zip
glr --json package inspect source.zip
glr --json package import source.zip --destination NEW_DIRECTORY --expected-environment ENVIRONMENT_ID --expected-contract SHA256
glr --project NEW_DIRECTORY --json package conformance source.zip
```

`package` is the offline handoff lane: `plan` (dry run) → `export` →
`inspect` → `import` → `conformance`. No subcommand executes, installs,
downloads, or deserializes, and `import` refuses a destination that already
exists. Read [packages.md](packages.md) for both selection profiles, the
deny-by-default `model` / `dataset` / `knowledge` / `report` groups, the
`glr.package-audit.v1` receipt, the refusal categories, and the exit codes
(`0` pass, `4` blocked).

Use `.glr/runs/<run-id>/` for run evidence and `.glr/exports/` for durable model,
loader-package, and knowledge exports. `knowledge export` rejects destinations
outside the project export root.

Project-local `glr.toml` tasks use strict `glr.tasks.v1`. Prefer
`runner = "vx"` and an argv beginning with `uv`, `run` for Python workflows so
VX resolves the locked toolchain and environment. GLR rejects shell strings,
partial placeholders, dependency cycles, unknown parameters, unsafe paths, and
unbounded timeouts. Task receipts under `.glr/tasks/` record process outcomes;
they are not authoritative gameplay or learning evidence.

Invocation-scoped `glr.run-context.v1` files bind generic labels and owned
JSON/TOML inputs to `doctor`, `runtime start`, `train`, `goal run`, or `play`.
GLR freezes and re-verifies source/input hashes, exports `GLR_RUN_CONTEXT` plus
`GLR_RUN_CONTEXT_SHA256`, and persists `run-context.json` with the run. Use
`load_inherited_run_context(project)` in Python roles. Keep product-specific
setup and status policy in VX tasks rather than adding core subcommands.

`train` and `goal run` record lifecycle, events, metrics, logs, capture artifacts, and hashes under
the configured data directory. Training tensors and transitions remain checksummed artifacts or
JSONL datasets; SQLite is the query projection, not the tensor store.

Goal runs keep promoted model bytes under
`.glr/checkpoints/<environment-id>/<goal-id>/best.checkpoint` and atomically
write `glr.learning-checkpoint.v1` control-state snapshots after research,
planning, training, and evaluation under the same goal namespace. These
snapshots record learning status and paths; learner-owned model, optimizer, and
replay-buffer bytes remain in the candidate or promoted checkpoint.

## Recording presets and storage layout

Use one run store for CLI and Python roles. Current CLI source accepts store
schemas 1 and 2 without downgrading Python's version stamp. Released CLI 0.18.0
rejects schema 2: upgrade to a release containing the compatibility fix before
mixing writers. Never reset `PRAGMA user_version` or create a second data root
to hide a schema failure; `checkpoint migrate` does not migrate SQLite stores.

Follow [VX recording and acceptance](recording.md) for encoder preflight,
fixed-argv recorder integration, synchronized labels, and finalized media QA.

Run `glr --project . --json capture preset` to get the default `training-balanced`
FFmpeg output arguments. They specify H.264/libx264, CRF 18, `fast`, 30 FPS CFR,
1920x1080, yuv420p, GOP 30, fixed keyframes, fast-start metadata, and no audio.
The project recorder owns the exact-window input and replaces `{capture_video}` with
`GLR_CAPTURE_VIDEO`. Use `capture preset --list` to discover alternatives.

Run `glr --project . --json capture layout` to resolve the canonical local paths.
Keep each run's logs, video, index, datasets, and report below
`.glr/runs/<run-id>/`, shared checkpoints below `.glr/checkpoints/`, and the query
projection at `.glr/runs.sqlite3`. Do not create game-specific top-level recording,
log, training-data, or report roots. A video without a valid checksummed
`glr.capture-frame.v1` index remains review media, not training data.

## Offline run reports

`report build` renders `glr.run-report.v1` as a self-contained HTML review
projection under the selected run directory:

```powershell
glr --project . --json report build <run-id>
glr --project . --json report build <run-id> --output review/report
```

The report builder rejects missing, symlinked, out-of-run, size-mismatched, or
SHA-256-mismatched evidence artifacts before writing. It omits prior
`run-report` outputs to avoid a self-referential hash, registers the generated
page as `run-report`, and remains safe to rerun. Its timeline and panels are driven only
by persisted events: `navigation.route_sample` for route traces,
`progression.item_unlocked` / `progression.catalog_snapshot` for unlocks, and
`match.result` for completed matches. Treat `match_kind=pvp` as meaningful only
when the adapter has an authoritative PvP result. Screenshot and video links
must point to authorized checksummed artifacts; no report panel is a claim of
live-game acceptance.

## Goal loop files

The input is `glr.agent-goal.v1`. It must declare:

- a stable goal ID and objective;
- the environment family;
- one or more metric/operator/target/source success criteria;
- maximum trials, training steps, wall seconds, and research sources;
- allowed media from official rules, text guides, video tutorials, or runtime traces.

The researcher writes `glr.research-bundle.v1`. On later failed trials it receives
`GLR_PREVIOUS_RESEARCH_PATH` and `GLR_PREVIOUS_EVALUATION_PATH` so it can gather additional allowed
evidence within the same global source budget.

The planner writes `glr.trial-plan.v1`. Reward terms contain only names, metric IDs, bounded numeric
weights, rationales, and referenced finding IDs. They cannot contain expressions or import paths.

The evaluator writes `glr.goal-evidence.v1`. Every evidence item must match a metric already saved
to `GLR_STORE_PATH` during the current trial, including value, source, and authority. Only
`authoritative` runtime evidence can satisfy a goal criterion.

## Default goal bindings

`goal set` validates a `glr.agent-goal.v1` file, requires its `environment_family` to match the
project, and saves it as the active default goal in `<data_dir>/goal-binding.json`
(`glr.goal-binding.v1`) together with a project-relative path and a SHA-256 of the goal file.
`goal set` with the global `--context` flag additionally binds the `glr.run-context.v1` file that
makes the goal executable.

Once a goal is bound, `goal run` reads the default when `--goal` is omitted, and `train` inherits
the bound context when `--context` is omitted. An explicit `--goal` or `--context` always wins, so
existing invocations are unchanged.

Use `goal list` to enumerate saved goals, `goal show [goal-id]` to inspect one (`source_status` is
`unchanged` / `changed` / `missing`, `context_status` is `unbound` / `bound` / `unresolved`), and
`goal use <goal-id>` to move the active pointer. A binding only selects a goal and a context: the
goal stays structured metadata, is copied into the run directory as an auditable receipt, and never
shapes rewards or judges completion.

Run receipts record `goal_binding.source` as `default` or `explicit`, plus
`goal_binding.context_source` (`explicit` / `default` / `none`) and, for a default goal,
`goal_binding.source_status`. An explicit `--goal` can still inherit the context bound to the
active goal, so `context_source` names where the context came from. Stored paths are re-checked
when the store is loaded: a hand-edited `goal_path` or `context_path` that is absolute, escapes
the project, or names a link is refused instead of opened.

## Reuse and reproduction gates

- `knowledge import` requires exact `environment_id` and `protocol_version`; imported entities and
  routes are advisory.
- `query research` returns exact-environment, same-family, and generic findings, excluding rejected
  findings. Use `--verified-only` when a decision requires prior runtime confirmation.
- `play` verifies every model-bundle byte and requires exact environment/protocol compatibility.
  Run live evaluation again in the new game instance; do not report reproduction from load success.

Stop when a declared budget is exhausted, a required role/capture fails, the runtime identity is
uncertain, or authoritative success evidence is missing. Return the failed gate and the relevant
run ID rather than relaxing the contract.

## Embedded Dashboard and durable trace commands

Bridge diagnostics share `glr.bridge-telemetry.v1`: `glr telemetry schema`,
`glr telemetry ingest --file FILE [--jsonl]` (`-` for stdin), and
`glr telemetry state RUN_ID`. Dashboard offers authenticated
`POST /api/v1/telemetry` and read-only `GET /api/v1/telemetry/state?run=ID`.
Preserve batch IDs when retrying and drain pending data before a run terminates.
Never print or archive `GLR_TELEMETRY_TOKEN`; status and metrics are diagnostic.

```powershell
glr --project . dashboard
glr --json dashboard catalog
glr --json dashboard presets
glr --json dashboard save-preset --file preset.json
glr --json dashboard run train.example
glr --json dashboard jobs
glr --json dashboard jobs --before JOB_ID
glr --json dashboard job-log JOB_ID --stream stderr
glr --json dashboard instances
glr --json dashboard instances --all
glr --json dashboard instances --all --prune
glr --json dashboard stop --instance INSTANCE_ID
glr --json dashboard stop --port 7432
glr --json dashboard stop --all
glr observe --port 7432
glr --json observe
glr --json runs trace RUN_ID --events-after 1000 --metrics-after 500 --limit 250
glr --json runs log RUN_ID --path capture.log --offset 0
glr --json backup create --output ../backups/run-history
glr --json backup verify ../backups/run-history
glr --json backup restore ../backups/run-history --output ../restored-history
glr observe --archive ../restored-history
```

Dashboard presets use `glr.training-preset.v1` with `id`, `title`, `description`,
and `argv` (train, goal run, or task run). Presets and job receipts persist in
SQLite. Operation forms reuse CLI argument definitions; requests never run a
shell or change the server project. Jobs use stable request IDs and one project
lock. A nonterminal record after service restart is unverified, not resumable.

Ports are no longer a single shared literal. Without `--port`, a server prefers
7432, then a stable per-project port derived from the data directory, then any
free port; `--port 0` asks the OS. An explicit `--port` is used exactly as given
and fails rather than silently moving. Start a second project without `--port`
to give it its own address.

Each running server publishes an instance lease (instance ID, project root, data
directory digest, executable, PID, port, URL, read-only flag, version, start
time) into a per-user registry (`GLR_STATE_DIR` overrides it), and
`/api/v1/health` returns the same object under `instance`. `glr.dashboard.instances.v1`
lists them: `dashboard instances` scopes to the current project, `--all` covers
everything this user started, `--prune` also drops stale leases. A lease is only
a hint — liveness is decided by asking the port and comparing `instance_id`. A
non-answering lease is `stale`; a port answering as another instance is `foreign`
and is never listed as yours or stopped. `dashboard stop` requires one explicit
target (`--instance`, `--port`, or `--all`) when the project has several live
servers; it asks the server to shut down gracefully and never kills a process,
so a foreign or unresponsive target is reported, not terminated.

Read-only HTTP: `/api/v1/health`, `/api/v1/runs?before=RUN_ID`,
`/api/v1/snapshot?run=ID&events_after=-1&metrics_after=0&limit=250`,
`/api/v1/log?run=ID&path=capture.log&offset=0`. Envelopes use
`glr.observation.v1`. POST controls exist only in Dashboard mode and require
same-origin JSON. All assets and Axum are embedded in the CLI.

Backups use `glr.observation-backup.v1`: a consistent SQLite snapshot, verified
completed-run files, completed-job logs and file hashes. Active run files and
active job logs are excluded; the manifest identifies database-only active runs.
Restores require a new destination and do not establish model/game compatibility.
