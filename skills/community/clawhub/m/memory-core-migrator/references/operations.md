# Operations and rollback

This reference governs production actions. Adapter scripts remain read-only
until a reviewed run report and run-bound approval exist.

## Run directory

Use a directory outside all indexed workspaces:

```text
~/openclaw-memory-migrations/<run-id>/
├── state.json
├── preflight.json
├── backup.json
├── export/
├── canonical/
├── staged-memory/
├── reports/
└── rollback/
```

Protect it as sensitive data. Canonical records can contain personal memory.

The final render output directory must not already exist. The renderer builds
all files in a private sibling directory and publishes the completed tree with
one atomic rename. An interruption may leave an unpublished dot-prefixed
temporary directory, but never a partially published render tree.

## Verified backup gate

Prefer the installed official backup CLI and its online SQLite snapshot logic.
Do not copy live SQLite, WAL, SHM, or journal files as a backup.

Accept a full archive only when:

1. process exit is zero;
2. machine-readable output says `verified: true`;
3. the exact reported archive exists;
4. `sha256sum -c` succeeds;
5. configured external agent roots are covered by the manifest.

Keep backup destinations outside the state directory to avoid recursive
archives. Treat credentials in full archives as production secrets.

Default LanceDB storage beneath `~/.openclaw` is normally covered by the state
asset. A custom `dbPath` outside included state/workspace/agent roots is not
guaranteed to appear in the archive manifest. Inventory it separately and use
a conservative quiesced copy because crash-consistent live LanceDB backup
semantics are undocumented.

## Staged configuration

Never edit production JSON in place with regex or partial text replacement.

1. Read and parse the current configuration.
2. Write a temporary candidate.
3. show a redacted structural diff;
4. validate the candidate with the installed CLI;
5. record hashes of current and candidate;
6. request the run-bound approval;
7. immediately before replacement, ensure the current hash still matches.

Do not hard-code provider URLs, API keys, service names, or agent lists.

## Service-owner rule

Discover the actual supervisor before restart. A CLI reporting a user service
does not prove that the live Gateway is user-scoped. Record the listening PID,
process cgroup, systemd FragmentPath/DropInPaths, and effective ExecStart.

For remote cutovers, start the cutover and rollback monitor outside the Gateway
cgroup so it survives the restart.

## Cutover gates

Proceed only when all are true:

- verified backup and manifest SHA recorded;
- export/canonical/rendered counts reconcile;
- every source scope is represented;
- generated Markdown was reviewed;
- baseline exists;
- source backend remains recoverable;
- old and new dreaming writers cannot overlap;
- approval matches action and run ID.

After changing the slot, verify in this order:

1. Gateway process and health endpoint;
2. expected OpenClaw/runtime versions;
3. memory-core loaded and owns the slot;
4. channels return to runtime healthy state;
5. FTS, vector extension, embedding provider, and dimensions;
6. per-agent indexed files/chunks;
7. baseline recall and source-only probes.

When text and machine-readable memory status disagree during an indexing
debounce window, preserve both observations, wait for the documented quiet
period, and use the installed version's settled machine-readable status for
automation. Treat this as an upstream status-interface limitation, not proof
that the migrator changed the index incorrectly.

Do not use `memory reset`, delete SQLite, or apply promotion as a generic fix.

## Rollback

Prepare rollback before cutover:

- original config and SHA;
- source plugin enablement and slot;
- old dreaming job IDs and states;
- actual service-owner restart command;
- source stats command and expected counts;
- baseline queries;
- long-term memory files that promotion could modify.

This checklist establishes **rollback readiness** only. Report a **rollback
rehearsal** only when the restore, restart, source-count validation, and recall
checks below were actually executed. Never infer a rehearsal from the presence
of backups or a plausible recovery path.

Rollback restores the configuration/slot and source writer, restarts through
the service owner, verifies source counts, then reruns the baseline. Preserve
new daily Markdown created after cutover; restore only files proven to have
been rewritten incorrectly.

Rollback never deletes staged imports or target indexes. Mark the run
`ROLLED_BACK` with evidence.

## Soak

Recommended default: seven days.

Daily checks:

- all agents have complete, healthy indexes;
- representative recall remains above its accepted baseline;
- channels pass actual inbound/outbound tests;
- only the intended dreaming writer runs;
- promotion diffs do not remove durable facts;
- duplicate growth and retrieval latency remain bounded.

Keep the source database cold for at least 30 days after retirement.
