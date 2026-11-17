# Operator recipes

These examples operate on copied exports. Keep the run directory outside every
OpenClaw indexed workspace.

## Reconcile multiple LanceDB Pro scopes

1. Use the installed plugin's stats command to record a count per scope.
2. Export or page each non-empty scope separately.
3. Normalize all captured files with an exact total:

```bash
node bin/openclaw-memory-migrator.js normalize --dry-run \
  --adapter lancedb-pro \
  --input export/global.json \
  --input export/main.json \
  --input export/other-scope.json \
  --expected-total 1533 \
  --output canonical/memory-records.jsonl
```

Do not treat a ±1 difference as automatically acceptable. Preserve before and
after source snapshots and explain any concurrent write explicitly.

## Require a complete approximate audit

For `n` records, the upper bound is `n * (n - 1) / 2` candidate pairs before
exact-text pairs are removed. Run dry first:

```bash
node bin/openclaw-memory-migrator.js audit --dry-run \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl \
  --max-comparisons 2000000 \
  --require-complete-approximate
```

Review `total_candidates`, `performed`, `coverage`, and `warnings`. Increase
the budget only when local runtime and memory permit.

## Consume machine-readable output safely

Normal JSON is written only to stdout. Warnings and errors go to stderr. Add
`--json-errors` when a caller needs `{code,message,next_action,details}`:

```bash
node bin/openclaw-memory-migrator.js audit \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl \
  --json-errors >reports/audit.stdout.json 2>reports/audit.stderr.jsonl
```

Never merge streams before parsing JSON.

## Page a capped source export

Source pagination is an operator responsibility in v0.1. Read the installed
plugin's `list --help`, use stable scope/limit/offset values, retain every page,
and verify no IDs are missing or duplicated after merging. The migrator does
not claim that page capture is an official plugin export.

## Error-to-action quick map

- `COUNT_MISMATCH`: recapture counts or correct `--expected-total`.
- `SCOPE_MISSING`: capture every scope or add the required manifest identity.
- `MANIFEST_INVALID`: regenerate and validate the source manifest.
- `AUDIT_INCOMPLETE`: increase `--max-comparisons`.
- `APPROVAL_INVALID`: repeat dry-run and issue a new action/run-bound approval.
- `OUTPUT_CONFLICT` / `SYMBOLIC_LINK`: choose a new regular output path.

## Privacy redline

Do not paste real memory, snippets, queries, exports, JSONL, audit files,
screenshots, hostnames, agent/channel IDs, private paths, tokens, or backup
hashes into issues or chat. Use synthetic fixtures to reproduce defects.
