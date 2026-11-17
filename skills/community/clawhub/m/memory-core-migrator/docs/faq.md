# FAQ

## Does the migrator export every memory-lancedb-pro scope?

No. It consumes explicit export files; it does not invoke the source plugin.
Current plugin CLIs may require one export per scope and may cap exports at
1,000 records. Discover all scopes, capture each one, and pass every file with
`--input`. Automatic `--all-scopes` orchestration is deferred to v0.2.0.

## Why is `--dry-run` optional if docs mention it?

Every command is dry-run unless `--apply` is present, including `run-init` and
`approve`. `--dry-run` is an explicit alias and cannot be combined with
`--apply`. `run-init --apply` creates only a local run-state file.
`approve --apply` issues one local, one-use token. Neither command writes
memory files, exports, or OpenClaw databases. A dry-run of either command
prints the intended action and writes nothing.

## Where is the CLI after a ClawHub install?

Install with `openclaw skills install memory-core-migrator`, then resolve the
skill directory via `openclaw skills info memory-core-migrator --json` and run
`node <skill-dir>/bin/openclaw-memory-migrator.js`. The ClawHub slug and the
repository Skill id differ only in naming.

## Why does `openclaw ltm` fail on my host?

`ltm` is registered by the installed `@openclaw/memory-lancedb` plugin. A bare
OpenClaw core install may report an unknown command. Install or enable the
official LanceDB plugin before capturing list JSON for the
`lancedb-official-list-beta` adapter.

## How do I know an approximate duplicate audit is complete?

Read `completeness.approximate_audit_complete` and
`approximate_comparisons.coverage`. A truncated audit is only evidence about
the compared candidate pairs. Increase `--max-comparisons`, or use
`--require-complete-approximate` to make truncation exit with status 2.

## What do parsed, accepted, skipped, and rejected mean?

- `parsed`: source items or Markdown sections examined.
- `accepted`: canonical records produced.
- `skipped`: structurally valid items intentionally producing no record, such
  as an empty Markdown section.
- `rejected`: items individually rejected while processing continues.

The current adapters fail closed on malformed records, so a successful run
normally reports `rejected: 0`; a malformed input fails the command instead of
silently increasing this count. `redactions` counts removed secret-like and
vector fields.

## Does rollback readiness mean rollback was rehearsed?

No. Readiness means the required backup, source data, configuration, restart
path, and evidence are available. A rehearsal means the rollback was actually
executed and verified. Report these separately.

## Is a healthy post-migration search a before/after benchmark?

No. A health check proves that target retrieval works at one point in time. A
paired comparison requires a frozen query set and source results collected
before migration, then target results collected under matching conditions.

## Why can OpenClaw text and JSON status disagree?

OpenClaw may expose transient or differently timed text and JSON values for
dirty state and chunk counts. This is upstream behavior. Record both, wait for
the indexing quiet window, and use the installed version's documented
machine-readable status as the automation input.

## How is private data handled?

Keep exports, canonical JSONL, audit reports, queries, snippets, paths,
hostnames, credentials, and backup hashes outside indexed workspaces and out
of public issues. Share only redacted counts, versions, adapter names, and
structured error codes.
