# Security policy

## Data sensitivity

Memory exports, manifests, reports, backups, and logs may contain credentials,
personal data, private conversations, health information, channel identifiers,
and operational secrets. Treat every run directory as production-sensitive.

The project is local-first and must not add telemetry or network upload without
an explicit, separately reviewed feature.

## Production invariants

- Owner-only execution; never authorize from a group or channel.
- Dry-run before write operations.
- Approval tokens bind action and run ID.
- Verified backup before cutover, promotion, retirement, or rollback.
- No direct writes to OpenClaw SQLite internals.
- No vector transfer across embedding spaces.
- No automatic deletion or mutation-based deduplication.
- Snapshot every output ancestor and revalidate its identity immediately before
  publishing an atomic file or render tree.
- Stop if counts, hashes, capabilities, configuration, agents, or scopes drift.

## Export hygiene

- Do not commit real exports, run reports, backups, or evaluation queries.
- Synthetic fixtures must contain invented people and infrastructure.
- Redact values matching secret-like key names before writing canonical records.
- Preserve rejected-field counts so redaction cannot become silent loss.
- Keep reports outside OpenClaw indexed memory directories.

## Archive and path safety

Only consume trusted local exports. Validate paths before extraction or render:

- reject absolute and drive-qualified archive members;
- reject traversal (`..`) and escaping symlinks;
- never restore into live state in place;
- require a fresh staging directory.

Use OpenClaw's supported online SQLite backup facilities. Never copy a live
SQLite database and its WAL/SHM files as an ad-hoc backup.

## Reporting vulnerabilities

Do not open a public issue containing real memory or credentials. Use the
repository's private security-advisory channel after one is configured.
Until then, contact the maintainer privately and provide the smallest synthetic
reproduction possible.

## Supported versions

Security support applies only to released versions listed in the compatibility
matrix. Unknown source schemas fail closed.
