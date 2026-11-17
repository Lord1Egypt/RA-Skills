# Operations and Safety

Use this reference for lifecycle maintenance, privacy expectations, concurrency limits, backup, and recovery.

## Contents

- [Storage layout](#storage-layout)
- [Visibility is not a security boundary](#visibility-is-not-a-security-boundary)
- [Concurrent access](#concurrent-access)
- [Archive lifecycle](#archive-lifecycle)
- [Backups and corrupt JSON](#backups-and-corrupt-json)
- [Direct JSON fallback](#direct-json-fallback)
- [Routine maintenance](#routine-maintenance)

## Storage layout

| Layer | Default path | Default visibility | Use for |
|---|---|---|---|
| global | `~/.memory-store/` | `global` | stable cross-project preferences and knowledge |
| workspace | `{workspace}/.agents/memory-store/` | `shared` | project decisions, progress, fixes, and handoffs |

Each store contains an active `memories.json`; archived data is moved to `archive/archived_YYYYMM.json`. The global path is shared by supported Agent platforms on the same user account. The workspace path may be unavailable in read-only or managed workspaces; in that case use a writable approved location or the global store only when the content truly belongs there.

`config.json` is separate from memory data. Installation creates it only after an interactive profile choice or an explicit `--memory-profile` option. A workspace policy overrides the global policy; without either file, the effective profile is `explicit`.

## Visibility is not a security boundary

`private`, `shared`, and `global` are application-level cooperation labels:

- CLI access to a private record requires an Agent identity matching `owner_agent`.
- Search, list, recall, update, delete, revive, and merge should all preserve the same identity rule.
- A user or process with filesystem access can still open the JSON files directly.
- The files are plaintext and are not encrypted at rest.
- The CLI does not detect, redact, or classify secrets, credentials, tokens, or personal information.

Therefore:

1. Never store passwords, API keys, private keys, session tokens, or raw personal data.
2. Redact sensitive source material before summarizing.
3. Treat `private` as “hide from cooperating Agents using the CLI,” not “secure from readers of this machine.”
4. Use operating-system permissions or an encrypted secret manager for real confidentiality.

## Concurrent access

Writes use a unique temporary file followed by an atomic rename. This prevents readers from seeing a half-written JSON file and avoids temporary-name collisions.

It does **not** provide a transaction lock around the complete read-modify-write cycle. Two writers can load the same old snapshot and the later rename can overwrite the earlier writer's update. Tags and memory types do not prevent this lost-update race.

For high-contention workflows:

- serialize writes to the same scope when possible;
- keep write batches small;
- use separate workspace scopes for unrelated projects;
- back up before bulk merge, archive, or delete;
- do not promise lossless concurrent writes until file locking or compare-and-swap is implemented.

## Archive lifecycle

Archive removes records from the active store and writes them to monthly archive files. Candidates can be selected by TTL, age, importance, or decay depending on the command flags.

Use `--scope all` for the same policy across both stores, or run the scopes separately when they need different thresholds:

```bash
node scripts/memory_cli.js archive --scope all --apply-decay --min-decay 0.15 --stdout

# Different policies can be run separately
node scripts/memory_cli.js archive --scope global --apply-decay --min-decay 0.15 --stdout
node scripts/memory_cli.js archive --scope workspace --apply-decay --min-decay 0.15 --stdout
```

Inspect and restore with the supported archive workflow:

```bash
node scripts/memory_cli.js list --scope all --status archived --as-agent <agent-id> --stdout
node scripts/memory_cli.js recall --id mem_xxx --as-agent <agent-id> --stdout
node scripts/memory_cli.js restore --id mem_xxx --as-agent <agent-id> --stdout
```

`revive` is a compatibility alias for `restore`. Archived records are excluded from ordinary active search. There is no need to depend on an undocumented `--include-archived` switch.

Priority affects decay: P1 retains value more slowly than P2, and P2 more slowly than P3. Treat decay as a maintenance heuristic, not a proof that a memory is obsolete. Review important archives before permanent deletion.

## Backups and corrupt JSON

Before destructive or bulk operations, copy these items to a safe location:

- `memories.json`
- `memories.index.json`, if present
- the `archive/` directory

If active or archive JSON is malformed, the CLI must fail closed with a non-zero exit. It must not reinterpret a corrupt file as an empty store or overwrite it during a later write.

Recovery sequence:

1. Stop writers targeting that store.
2. Copy the damaged file before editing it.
3. Restore the most recent known-good backup, or repair the JSON in a separate file.
4. Validate that the top-level value is an array and entries follow [memory_schema.json](memory_schema.json).
5. Replace the damaged file only after validation, then run a read-only `list` or `stats` check.

## Direct JSON fallback

Prefer the CLI. Direct JSON access bypasses validation, identity filtering, index updates, archive rules, and atomic-write conventions.

If Node.js is unavailable:

- read-only inspection is safer than direct writes;
- for a necessary write, first back up the entire store and ensure no other writer is active;
- preserve the schema and update the index consistently;
- never use direct access as a way to bypass private visibility.

Large stores also consume substantial model context when read directly. Use targeted CLI results instead of loading the full file whenever possible.

## Routine maintenance

A practical schedule is weekly or when search quality degrades:

1. Run `stats --scope all` and inspect growth.
2. Archive both scopes together, or separately when they need different conservative thresholds.
3. Review archived P1 decisions before any permanent deletion.
4. Merge only entries that truly describe the same reusable knowledge.
5. Keep backups outside the live store.

Maintenance is explicit; there is no daemon or background scanner. “Automatic” in Agent workflows means the Agent chooses when to call the CLI, not that a persistent process monitors conversations.
