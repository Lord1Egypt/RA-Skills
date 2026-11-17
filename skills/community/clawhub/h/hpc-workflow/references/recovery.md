# Recovery and upgrades

Inspect through the user's supported connection. Preserve stable request IDs,
logs and private profiles. Do not infer job completion from a disconnect.

| Observation | Action |
| --- | --- |
| Authentication unavailable | Use the installation's explicit login operation once; notify the user of MFA and wait. Ordinary operations must not initiate another challenge. |
| Scheduler query fails | Keep state unknown. Retry read-only observation; do not allocate replacement resources. |
| Submission outcome unclear | Reconcile the same request with queue, owner/comment and accounting evidence. Preserve the reservation if no terminal result can be established. |
| Job running, compute unreachable | Inspect the allocation pane, route identity and recorded node. Reconnect to the same job; do not kill tmux or request another GPU. |
| No active allocation | Compute/autosave/storage checks are not performed. A zero command exit alone does not prove a healthy workspace. |
| Autosave stopped or stale | Inspect autosave logs, current host/PID/start identity and space/quota. Start through the same snapshot helper only when no other writer owns the archive. |
| Incremental requests compaction | Allow the immediate full-save fallback. This is maintenance; a failed full-save fallback is a real backup failure. |
| Newest generation corrupt | Restore uses a verified older family. Keep corruption evidence and report the restored generation; preserve complete experiment checkpoints separately. |
| Space/quota insufficient | Report paths, sizes, limits and required working space. Adjust scoped storage configuration; do not delete research data or reduce retention silently. |
| Deployment interrupted | Inspect `~/.local/state/SITE-gpu/deployment.json`. Replay the same frozen bundle when quiescent; the installer first restores the interrupted prior installation. |

Upgrade with a new immutable staging directory. Verify the profile and hashes;
do not change account, archive, namespace or transport as an incidental upgrade.
`uv run --no-project --python 3.12 python scripts/common/deploy_bundle.py BUNDLE`
validates locally. `--apply`
installs after scheduler/request/lease checks. The result includes an exact backup.

To restore a completed upgrade's prior installation:

```sh
uv run --no-project --python 3.12 python scripts/common/deploy_bundle.py BUNDLE --rollback REMOTE_BACKUP
uv run --no-project --python 3.12 python scripts/common/deploy_bundle.py BUNDLE --rollback REMOTE_BACKUP --apply
```

Backups are accepted only below the remote user's `~/.local/state/hpc-core-backups`.
All prior bytes are verified before rollback. Missing prior files are restored as
absent; modes and the prior manifest are restored. A failed or forcibly interrupted
rollback leaves a journal and blocks new allocation until recovery succeeds.
Recover the same site using its original connection and inspect installed hashes.
These operations replace helpers/configuration, not workspace archives.

Before expensive staging, inspect free disk space, inodes and site quota for both
local disk and the persistent archive. Full publication temporarily holds a new
pack alongside retained families; size the budget for that overlap. The default
deadline margin is 120 seconds: increase it if a measured full save takes longer.
The private profile can set `snapshot.interval`, `compact_seconds`, `end_margin`,
`generations_keep`, `full_families_keep`, `max_incremental_ratio` and
`home_budget_gb` as integer policy values. Retention requires at least two
generations and two independent full families. Measure disposable data on a
permitted worker with `uv run --no-project --python 3.12 python scripts/common/tests/benchmark_snapshot.py
--size-mib 1024 --files 10000`; it does not establish another filesystem's speed.
Do not advertise the five-minute autosave cadence as a guaranteed loss bound;
recovery is limited to successfully committed generations.

For a support report, include installed version/hashes, adapter, request/task IDs,
requested and observed resources, structured status/doctor checks, journal phase,
and relevant error lines. Redact usernames, project paths and authentication
material before posting a public issue. Full task logs may contain private data.
