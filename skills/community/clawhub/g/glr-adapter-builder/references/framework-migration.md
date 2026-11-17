# Framework upgrade and migration contract

Use this procedure whenever an agent upgrades GLR or its downstream packages.
Read the project's `QUALITY.md` and `MIGRATIONS.md` first. Dependency installation
is not data migration. Do not invent migration commands absent from the release.

For a module split, read `ARCHITECTURE.md` and record old/new ownership and import
edges. Check serialized Python module/class references, configuration entrypoints,
and observation/action ordering before moving code. A source-only rename can
break old checkpoints even when dependency versions have not changed.

## Establish source and target

Record installed GLR version and import origin, application revision, Python,
lockfile digest, CLI/host/provider versions, configuration and run-store schemas,
dataset schema, and checkpoint format. A source checkout can be older than the
downstream installation: never downgrade implicitly to match it.
Resolve an explicit target and inspect release notes, schema definitions, API
changes, and supported migration tools for every crossed version.

For Python APIs/imports, optional dependencies, CLI/protocol, configurations,
durable history/cursors, dataset provenance, and checkpoint/optimizer/RNG state,
record `unchanged`, `compatible`, `migration-required`, or `unsupported` with
evidence. Unknown compatibility is a gap, not permission to invent a converter.

## Preserve baseline and data

Preserve unrelated working-tree changes; isolate code/lockfile edits. Capture
offline baseline tests and fixtures. Inventory data read-only and record schema,
counts, sizes, and hashes; keep private backup paths out of public reports.
Use the supported consistent backup API for live stores, including SQLite.
Copying only a live database file can omit WAL state. Coordinate writer pauses
and model checkpoints where consistency requires them; do not kill or restart
active training as a package-installation side effect. Verify restoration into
an isolated destination before relying on the backup.

## Stage explicit conversion

Converters belong in named, tested Python packages, separate from normal imports
or training startup. Declare accepted source/target schemas, preserved invariants,
and unsupported cases. Provide dry-run and validation modes. Write to a new
staging destination; reject unknown schemas and nonempty destinations by default.
Define atomic completion, interrupted-run recovery, and repeat-run behavior:
identical output or an explicit already-migrated refusal, never duplicate rows.

Preserve IDs, timestamps, lineage, references, checksums, authoritative/advisory
provenance, and terminal-outcome meaning. Document intentional transformations
and loss. Never relabel failed or unknown trajectories as expert demonstrations.
Update code APIs, callers, import namespaces, metadata, and lockfiles together.
Validate both old and new configuration schemas; changing version labels alone
is not conversion.

Checkpoint migration verifies architecture, shapes/dtypes, model/config versions,
optimizer/scheduler state, and seeds/RNG state. If these cannot be preserved,
report a warm start instead of exact resume. Keep incompatible weights with
their original environment; never silently reset or discard them.

## Validate and cut over

Run the quality gates against the target wheel outside the checkout. Add golden
old-to-new fixtures and negative tests for unsupported versions, malformed input,
repeat execution, and interrupted writes. Verify counts, IDs/references, hashes,
provenance, queries/replay, finite tensors, and bounded offline checkpoint resume.
A deserialized model is not proof of resumed learning. Keep live acceptance as
a separate evidence gate.

Pause writers for the agreed cutover, switch to the validated destination, and
verify readback before resuming writes. Retain the previous wheel, lockfile,
configuration, and consistent data snapshot. On validation failure, leave the
original data and application configuration usable.

## Rollback and migration receipt

Record rollback triggers and verified restore commands. Do not point an older
runtime at a newer schema without proven backwards compatibility. A snapshot
restore can lose post-cutover writes: preserve them separately and state the
reconciliation/loss boundary. Backups alone do not prove lossless rollback.
Destructive in-place conversion requires explicit authorization after a concrete,
reviewable conversion and recovery plan is prepared.

Complete `MIGRATIONS.md` with source/target versions, converter revision, private
backup references, compatibility table, commands and outcomes, count/hash checks,
known losses, rollback results, and deferred live evidence. Only mark completion
after required gates pass. Unsupported migrations must remain explicit gaps.
