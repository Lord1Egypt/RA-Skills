# OpenClaw Memory Migrator

**Move the memory. Keep the proof.**

A safety-gated OpenClaw Skill and CLI toolkit for moving authoritative memory
from LanceDB Pro, official LanceDB list captures, QMD, or Markdown into
`memory-core`.

Memory migrations can truncate exports, miss scopes, duplicate content, and
leave no proof that recall or rollback still works. This toolkit makes those
risks visible with dry-run manifests, count/ID/hash reconciliation, reviewable
Markdown staging, and approval-gated cutover.

[中文说明](README.zh-CN.md)

## Why

Changing a memory backend is not a file-copy problem. A trustworthy migration
must prove what was exported, avoid transferring incompatible vectors, protect
credentials, preserve rollback, and compare recall before retiring the source.

This project gives users returning from third-party memory backends to
OpenClaw's official memory-core a safer, verifiable, and practical migration
path.

OpenClaw Memory Migrator supplies that control plane:

- versioned, inspectable JSONL interchange records;
- source-aware count, ID, hash, and duplicate audits;
- memory-core Markdown rendering without rewriting `MEMORY.md`;
- run-bound approval tokens for production actions;
- resumable phase state and rollback evidence;
- a reproducible recall benchmark workflow;
- no direct writes to OpenClaw SQLite internals.

## Support status

- Stable: version-gated memory-lancedb-pro JSON capture
- Stable: Markdown and QMD-owned Markdown
- Beta: official `memory-lancedb` `ltm list` JSON wrapped in the versioned
  per-agent capture manifest
- Target: memory-core through Markdown and official indexing

Opaque database parsing, vector copying, and automatic deletion are not
supported.

Important: memory-lancedb-pro v1.1.0-beta.10 `export` is capped at 1,000
records. The operator workflow must compare every scoped export with fresh
stats and paginate `list --offset` when required.

## Try with fixtures first

Requires Node.js 22+. There are no runtime dependencies. This path uses
synthetic fixtures only. Do not substitute a live export here.

```bash
node bin/openclaw-memory-migrator.js --help
mkdir -p canonical reports staged-memory/imports
node bin/openclaw-memory-migrator.js preflight \
  --input test/fixtures/lancedb-pro.json \
  --output canonical/memory-records.jsonl
node bin/openclaw-memory-migrator.js normalize --dry-run \
  --adapter lancedb-pro \
  --input test/fixtures/lancedb-pro.json \
  --output canonical/memory-records.jsonl
# Optional smoke audit against the source fixture (no write):
node bin/openclaw-memory-migrator.js audit --dry-run \
  --adapter lancedb-pro \
  --input test/fixtures/lancedb-pro.json
node bin/openclaw-memory-migrator.js render --dry-run \
  --adapter lancedb-pro \
  --input test/fixtures/lancedb-pro.json \
  --output staged-memory/imports/lancedb-pro
```

Install from ClawHub after the fixture dry-run succeeds:

```bash
openclaw skills install memory-core-migrator
openclaw skills info memory-core-migrator --json
# Then run the CLI from the reported skill directory:
node <skill-dir>/bin/openclaw-memory-migrator.js --help
```

ClawHub slug `memory-core-migrator` and repo/Skill id `openclaw-memory-migrator`
refer to the same toolkit. Then file counts, not memory, through the
[dry-run Issue Form](https://github.com/airbing11/openclaw-memory-migrator/issues/new?template=dry-run-report.yml).

## Quick start with your own export

```bash
node bin/openclaw-memory-migrator.js --help
mkdir -p canonical reports staged-memory/imports
node bin/openclaw-memory-migrator.js preflight \
  --input export/global.json \
  --input export/main.json \
  --output canonical/memory-records.jsonl
node bin/openclaw-memory-migrator.js normalize --dry-run \
  --adapter lancedb-pro \
  --input export/global.json \
  --input export/main.json \
  --expected-total <trusted-snapshot-total> \
  --output canonical/memory-records.jsonl
# After an approved normalize --apply writes canonical JSONL:
node bin/openclaw-memory-migrator.js audit --dry-run \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl
node bin/openclaw-memory-migrator.js render --dry-run \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl \
  --output staged-memory/imports/lancedb-pro
```

Commands default to local, non-destructive transformations. `--dry-run` is an
explicit alias for that default and conflicts with `--apply`. Read
[`SKILL.md`](SKILL.md) before production use.

Recall comparisons follow
[`docs/benchmark-methodology.md`](docs/benchmark-methodology.md).
See also the [FAQ](docs/faq.md) and [operator recipes](docs/recipes.md).

## Safety model

- Owner-only execution
- Dry-run first
- Verified backup before writes
- Approval bound to action and run ID
- Stop on drift or count mismatch
- Reports stored outside indexed memory paths
- Source data retained through the rollback window

See [`references/operations.md`](references/operations.md) and
[`SECURITY.md`](SECURITY.md).

## Repository status

This project is an early release candidate. Use synthetic fixtures or a copied
export first. Production cutover remains operator-reviewed.

## Evidence, not promises

An anonymized run reconciled 1,533 exported and canonical records and produced
29 staged Markdown files. Its 8/8 Hit@5 result was a post-migration health
check, not a paired before/after benchmark; its retained recovery artifacts
proved rollback readiness, not a rollback rehearsal. The approximate audit
also stopped at 10,000 of 1,174,211 candidate pairs. See the bounded
[dogfood evidence](docs/dogfood-2026-09-18.md); none of these observations is a
guarantee for other installations.

## Feedback

This RC is looking for anonymized dry-run counts from supported sources, not
raw memory. Use the Issue Forms:

- [Anonymized dry-run report](https://github.com/airbing11/openclaw-memory-migrator/issues/new?template=dry-run-report.yml)
- [Compatibility bug](https://github.com/airbing11/openclaw-memory-migrator/issues/new?template=compatibility-bug.yml)

Do not attach exports, JSONL, screenshots, hostnames, or memory text. See
[`docs/community-launch-plan.md`](docs/community-launch-plan.md) for the
privacy redlines.

## Development

```bash
npm test
npm run check
```

## License

The GitHub source repository is MIT licensed; see [`LICENSE`](LICENSE).
The Skill copy distributed through ClawHub is MIT-0 under ClawHub's publishing
terms.
