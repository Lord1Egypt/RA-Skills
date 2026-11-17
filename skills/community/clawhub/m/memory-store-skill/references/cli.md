# CLI Reference

Memory Store v1.1.0 uses `memory-store <command>` (or `node scripts/memory_cli.js <command>` from the installed skill directory) with Node.js 18 or newer.

## Contents

- [Install and update the skill](#install-and-update-the-skill)
- [Guided terminal and short commands](#guided-terminal-and-short-commands)
- [Configure the memory policy](#configure-the-memory-policy)
- [Output and identity](#output-and-identity)
- [Initialize and store](#initialize-and-store)
- [Search and inspect](#search-and-inspect)
- [Update, delete, and merge](#update-delete-and-merge)
- [Archive and revive](#archive-and-revive)
- [Statistics, compression, and migration](#statistics-compression-and-migration)
- [Accepted values](#accepted-values)

## Install and update the skill

Install the npm package, then explicitly install the skill for a platform:

```bash
npm i memory-store-skill
npx memory-store setup --agent codex --mode explicit
```

To update, explicitly upgrade the npm package and then sync existing Agent-platform copies:

```bash
npm i memory-store-skill@latest
npx memory-store setup --sync
```

npm installation has no lifecycle installer and does not modify Agent directories. The updater reads only from the current local package, updates existing installations, verifies copied artifacts, and does not download or execute remote code or modify memory data.

```bash
npx memory-store setup --sync --dry-run
npx memory-store setup --sync --agent codex
npx memory-store setup --sync --target /path/to/memory-store
```

From a source checkout, run `node scripts/install.js --update` with the same selectors to refresh existing installations from that checkout. `--update` fails instead of creating a missing target.

The legacy `memory-store-install` and `memory-store-update` binaries remain compatible throughout v1.x.

## Guided terminal and short commands

Run without arguments in a real terminal to open the zero-dependency numbered menu:

```bash
memory-store
```

It covers setup, search, adding a memory, profile changes, status, and maintenance preview. Interactive writes print a summary and require an explicit `y`; Enter cancels. When stdin or stdout is not a TTY, no-argument execution prints compact help and exits without waiting.

Use the intent-oriented commands for Agents, CI, and direct terminal commands:

```bash
# workspace + shared + explicit by default
memory-store remember decision "Database choice" "Use SQLite for local single-user deployment" --workspace

# text searches all stores; a mem_... value recalls one record
memory-store recall "database choice" --json
memory-store recall mem_xxx --json

# effective profile, global default, and workspace override
memory-store mode
memory-store mode balanced --global
memory-store mode explicit --workspace
memory-store mode --reset --workspace

# combined version/profile/path/count view
memory-store status
memory-store status --json

# preview by default; mutate only with --apply
memory-store maintain
memory-store maintain --apply
```

`remember` accepts the memory type as its first positional value and defaults to `decision`. Use `--global` for `global + global`, or `--private --agent-id <id>` for a private workspace record. `--auto --source-conv-id <id>` maps to policy-governed automatic storage. The facade hides routine `scope + visibility + intent + stdout` combinations; advanced flags and v1 commands remain available through `memory-store help --advanced`.

## Configure the memory policy

The effective profile is the workspace profile when present, otherwise the global profile, otherwise the safe `explicit` default.

```bash
memory-store mode --json
memory-store mode balanced --global --json
memory-store mode explicit --workspace --json
memory-store mode --reset --workspace --json
```

Profiles are `off`, `explicit`, `balanced`, and `proactive`. Explicit user requests use `--intent explicit`. Policy-driven `search` and `store` calls use `--intent automatic`; automatic stores also require `--source-conv-id`. The CLI enforces allowed types and per-conversation limits for automatic writes.

## Output and identity

Commands that return data print JSON to stdout by default.

```bash
node scripts/memory_cli.js search --query "release workflow" --scope all --stdout
node scripts/memory_cli.js search --query "release workflow" --scope all --output results.json
```

- Omit both flags for normal stdout output.
- Use `--stdout` when a host needs an explicit stdout flag.
- Use `--output <file>` only when a durable intermediate file is useful.
- Use a stable `--agent-id` when storing and `--as-agent` when reading or mutating. `MEMORY_AGENT_ID` can provide the identity when the command supports identity filtering.

## Initialize and store

Initialize one store at a time:

```bash
node scripts/memory_cli.js init --scope global --stdout
node scripts/memory_cli.js init --scope workspace --stdout
```

Store a memory:

```bash
node scripts/memory_cli.js store \
  --type decision \
  --title "Database choice" \
  --summary "Use SQLite for the local single-user deployment." \
  --tags "database,architecture" \
  --importance 0.85 --priority P1 \
  --scope workspace --visibility shared \
  --agent-id agent-a --intent explicit --stdout
```

Required fields are `--type`, `--title`, and `--summary`. `--title` and `--summary` must not be empty. `--importance`, when supplied, must be between 0 and 1; it defaults to `0.5`. `--ttl-days`, when supplied, must be a positive integer.

Defaults:

- scope: `global`
- visibility: `global` in the global store, `shared` in the workspace store
- priority: inferred from importance (`P1` at 0.8+, `P2` at 0.5+, otherwise `P3`)

## Search and inspect

Search across both stores:

```bash
node scripts/memory_cli.js search \
  --query "database choice" --scope all \
  --type decision,debug_solution \
  --visibility shared,global \
  --as-agent agent-b --limit 5 --stdout
```

`--type` and `--visibility` accept comma-separated values. Search combines keyword, tag, type, freshness, and importance signals; Chinese queries also use n-gram matching.

Search is read-only by default. Add `--touch` only when the returned matches were actually consumed and their access counters should be updated:

```bash
node scripts/memory_cli.js search \
  --query "release workflow" --scope all \
  --as-agent agent-b --limit 5 --touch --stdout
```

List active memories:

```bash
node scripts/memory_cli.js list \
  --scope all --status active \
  --type decision,state --as-agent agent-b --stdout
```

Recall one memory and increment its access count:

```bash
node scripts/memory_cli.js recall --id mem_xxx --as-agent agent-b --stdout
```

Private records are returned only when the supplied identity matches `owner_agent`. This is a CLI cooperation rule, not encryption; see [operations.md](operations.md).

## Update, delete, and merge

Update mutable fields:

```bash
node scripts/memory_cli.js update \
  --id mem_xxx --importance 0.9 --priority P1 \
  --visibility shared --as-agent agent-a --stdout
```

Delete one active memory:

```bash
node scripts/memory_cli.js delete --id mem_xxx --as-agent agent-a --stdout
```

Merge related active memories in the same store:

```bash
node scripts/memory_cli.js merge \
  --ids mem_xxx,mem_yyy --scope workspace \
  --as-agent agent-a --stdout
```

Back up the store before bulk delete or merge. Merge is a structural operation; the Agent should first verify that the records express the same durable fact or decision.

## Archive and revive

Archive both stores with `--scope all`, or process each scope separately when they need different thresholds. Without `--apply-decay`, use an explicit age criterion; with decay enabled, the CLI also considers TTL and decay score.

```bash
node scripts/memory_cli.js archive \
  --scope all --apply-decay --min-decay 0.15 --stdout

# Or maintain the stores separately
node scripts/memory_cli.js archive \
  --scope global --apply-decay --min-decay 0.15 --stdout

node scripts/memory_cli.js archive \
  --scope workspace --apply-decay --min-decay 0.15 --stdout
```

List archived records and recall one by ID:

```bash
node scripts/memory_cli.js list \
  --scope all --status archived --as-agent agent-a --stdout

node scripts/memory_cli.js recall \
  --id mem_xxx --as-agent agent-a --stdout
```

Restore an archived record to its original store:

```bash
node scripts/memory_cli.js restore --id mem_xxx --as-agent agent-a --stdout
# `revive` is a compatibility alias for `restore`.
```

Archive files live under `<store>/archive/archived_YYYYMM.json`. Archived records are not included in ordinary active search. Do not advertise or depend on `--include-archived`; use `list --status archived`, `recall`, and `restore` instead.

## Statistics, compression, and migration

```bash
# Aggregate active-store statistics
node scripts/memory_cli.js stats --scope all --stdout

# Extract transcript candidates; an Agent must still summarize and classify them
node scripts/memory_cli.js compress --input transcript.jsonl --stdout

# Inspect migration behavior before consolidating legacy stores
node scripts/memory_cli.js migrate --dry-run --stdout
```

`compress` is candidate extraction, not automatic semantic memory creation or sensitive-data detection.

Print CLI help or version:

```bash
node scripts/memory_cli.js help
node scripts/memory_cli.js version
```

## Accepted values

| Field | Values |
|---|---|
| profile | `off`, `explicit`, `balanced`, `proactive` |
| intent | `explicit`, `automatic` |
| scope | `global`, `workspace`; read-only aggregate commands may accept `all` |
| visibility | `private`, `shared`, `global` |
| priority | `P1`, `P2`, `P3` |
| type | `fact`, `decision`, `preference`, `workflow`, `debug_solution`, `state`, `event`, `relation` |
| status | `active`, `archived` where documented |

Invalid enumerations, malformed numbers, and corrupt store JSON fail with a non-zero exit instead of silently creating or overwriting data.
