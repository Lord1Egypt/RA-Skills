---
name: openclaw-memory-migrator
description: Safely migrates OpenClaw memory from LanceDB Pro, official LanceDB list captures, QMD, or Markdown into memory-core. Use when an owner asks to migrate, audit, deduplicate, benchmark, cut over, or roll back an OpenClaw memory backend.
disable-model-invocation: true
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins:
        - node
        - openclaw
---

# OpenClaw Memory Migrator

Move the memory. Keep the proof.

Use this Skill when an owner wants a safer, verifiable, and practical path
from a third-party memory backend back to OpenClaw's official memory-core.

## Safety rules

1. Run only in an authenticated owner DM, Control UI, or local operator shell. Refuse execution from group or channel chats.
2. Default to read-only discovery. Every CLI command, including `run-init` and
   `approve`, is dry-run unless `--apply` is set. `--dry-run` is an explicit
   alias and conflicts with `--apply`. `run-init --apply` writes only a local
   run-state file. `approve --apply` issues one local token. Neither writes
   memory, exports, or OpenClaw databases.
3. Never copy source vectors into memory-core SQLite. Export authoritative text and metadata, then let memory-core rebuild derived indexes.
4. Never delete a source database, SQLite file, WAL/SHM sidecar, Markdown file, or backup.
5. Before writes, require a verified OpenClaw backup and a run-bound approval:
   `APPROVE <ACTION> <RUN_ID>`.
6. A previous approval, an approval for another action, or an approval from another run is invalid.
7. Stop on count, ID, hash, scope, agent, configuration, or capability drift.
8. Keep state and reports outside indexed memory paths.
9. Do not enable two dreaming writers during cutover.
10. Do not publish logs or fixtures containing user memory, credentials, channel IDs, or personal data.

## Supported paths

- Stable: memory-lancedb-pro JSON capture to memory-core Markdown.
- Stable: Markdown or QMD-owned Markdown to memory-core Markdown.
- Beta: captured official memory-lancedb `ltm list` JSON to memory-core Markdown
  (requires the installed `@openclaw/memory-lancedb` plugin; bare OpenClaw has
  no `ltm` command).
- Unsupported: direct opaque LanceDB database parsing, vector transfer, arbitrary backend-to-backend sync.

Read [references/compatibility.md](references/compatibility.md) before selecting an adapter.
For operator questions and copyable workflows, see
[docs/faq.md](docs/faq.md) and [docs/recipes.md](docs/recipes.md).
Compatibility refresh notes:
[docs/compatibility-matrix-2026-11-11.md](docs/compatibility-matrix-2026-11-11.md).

## Invoke the CLI

From this repository:

```bash
node bin/openclaw-memory-migrator.js --help
```

After ClawHub install (`openclaw skills install memory-core-migrator`), resolve
the skill directory with `openclaw skills info memory-core-migrator --json` and
run:

```bash
node <skill-dir>/bin/openclaw-memory-migrator.js --help
```

The ClawHub slug is `memory-core-migrator`; the Skill/package id remains
`openclaw-memory-migrator`.

These commands execute only the JavaScript already in this package. They do
not download code. Reviewable sources:

- [bin/openclaw-memory-migrator.js](bin/openclaw-memory-migrator.js)
- [lib/cli.js](lib/cli.js)
- [lib/state.js](lib/state.js)
- [lib/operations.js](lib/operations.js)

## Workflow

### 1. Discover

Resolve rather than assume:

- OpenClaw version and executable path
- state directory, agents, workspaces, memory slot
- source plugin version and CLI help
- source scopes and record counts
- memory-core availability
- whether `openclaw ltm` exists (official LanceDB plugin only)
- embedding provider/model/dimensions
- dreaming jobs and maintenance window
- free disk and backup destination

Run preflight against explicit export files. Keep the surrounding run directory
outside the workspace:

```bash
node bin/openclaw-memory-migrator.js preflight \
  --input export/global.json \
  --output canonical/memory-records.jsonl
```

If a required capability is unknown, stop. Do not invent a command.

### 2. Back up

Use the current OpenClaw backup CLI. A backup is accepted only when:

- command exit is zero;
- JSON reports `verified: true`;
- the exact returned `archivePath` exists;
- SHA-256 is recorded and verifies.

Also inventory source databases and configured agent roots. Follow
[references/operations.md](references/operations.md).

### 3. Export read-only

Select one adapter:

```bash
node bin/openclaw-memory-migrator.js normalize --dry-run \
  --adapter lancedb-pro \
  --input export/global.json \
  --input export/main.json \
  --expected-total <trusted-snapshot-total> \
  --output canonical/memory-records.jsonl
```

For LanceDB Pro, inspect `memory-pro export --help` and export every non-empty
scope separately. Set an explicit limit only when that installed version
supports it. `memory-lancedb-pro` v1.1.0-beta.10 export is capped at 1,000
records; when a scope exceeds the detected cap, paginate `memory-pro list`
with `--limit` and `--offset`. Exported totals must equal the immediately
preceding scoped stats.

For QMD and Markdown, migrate the authoritative Markdown rather than QMD's
derived index. OpenClaw 2026.9.x retired QMD backend configuration, so use the
official Doctor migration where applicable rather than restoring legacy QMD
keys. Official LanceDB has no export command in verified 2026.9.x releases;
capture `openclaw ltm list --agent <id>` for every agent and wrap each array in
the versioned `lancedb-official-list-beta` manifest documented in
`references/compatibility.md`. Never reverse-engineer a live database.

### 4. Audit

```bash
node bin/openclaw-memory-migrator.js audit --dry-run \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl \
  --max-comparisons 10000
```

Require:

- source/export/canonical non-empty counts reconcile;
- source IDs reconcile where the source supplies IDs;
- no silent empty-text drops;
- exact duplicates and approximate duplicate groups are reported;
- secret-like metadata is rejected or redacted.

Always inspect `completeness`, `approximate_comparisons.coverage`, and
`warnings`. A truncated approximate scan is not a complete near-duplicate
conclusion. Use `--require-complete-approximate` when completeness is a gate.
Normal JSON remains on stdout; warnings and errors remain on stderr. Callers
that need structured errors can add `--json-errors`.

Deduplication is report-only in v0.1. Never delete automatically.

### 5. Render for memory-core

```bash
node bin/openclaw-memory-migrator.js render --dry-run \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl \
  --output staged-memory/imports/<source>
```

Render durable records separately from dated records. Do not append imports
directly to root `MEMORY.md`. Review generated Markdown before cutover.

### 6. Establish recall baseline

Create at least eight owner-approved queries covering:

- durable identity or preference
- recent event
- source-only fact
- multilingual/CJK phrase
- operational rule
- channel or agent-scoped fact

Record top-k source, score, latency, and expected evidence. Never index the
evaluation report as memory. Follow
[`docs/benchmark-methodology.md`](docs/benchmark-methodology.md).

### 7. Request cutover approval

Write the proposed configuration diff, affected agents, backup SHA, manifest
SHA, baseline, rollback commands, and maintenance window into the run report.

Request exactly:

```text
APPROVE CUTOVER <RUN_ID>
```

After receiving it, re-run preflight. If anything material changed, invalidate
the approval and generate a new run.

### 8. Cut over

Follow [references/operations.md](references/operations.md):

1. Enable memory-core and validate a staged config.
2. Disable the old memory writer and old dreaming schedules.
3. Change the single memory slot.
4. Restart through the verified service owner.
5. Confirm channel and Gateway health before indexing.
6. Build memory-core indexes for every configured agent.
7. Run the baseline and source-only probes.

If health or recall gates fail, stop and request:

```text
APPROVE ROLLBACK <RUN_ID>
```

### 9. Soak and retire

Keep source data cold and plugins disabled during the soak period. Verify
channels, indexes, recall, dreaming output, and long-term file diffs daily.

Request `APPROVE PROMOTION <RUN_ID>` before the first promotion-capable
dreaming run. Request `APPROVE RETIRE <RUN_ID>` before uninstalling plugins.
Retirement still preserves source data for the declared rollback window.

## Report contract

Every phase report includes:

- run ID, phase, timestamps, host fingerprint
- versions, adapter, agents, scopes
- backup path and SHA-256
- source/export/canonical/rendered counts
- duplicate and rejected-record counts
- slot, indexing, channel, and recall status
- rollback readiness, and separately whether a rollback rehearsal was executed
- exact next approval or blocker

Never describe a partial or unverified result as successful.
