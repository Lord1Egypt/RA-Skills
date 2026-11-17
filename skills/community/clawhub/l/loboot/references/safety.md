# Loboot 0.1.0 safety model

Read the installed command help before applying version-sensitive guidance. Loboot controls native per-user services; it does not sandbox the launched program or implement a resident supervisor.

## Mutation boundaries

All mutating commands support `--dry-run --json`: `add`, `update`, `remove`, `start`, `stop`, `restart`, `enable`, and `disable`. Preview the complete command before an authorized apply. Dry-run is read-only, makes no service-manager queries, and leaves live preconditions untested. Conditional native plans are not atomic promises about later OS state.

| Action | Definition | Runtime | Future activation |
| --- | --- | --- | --- |
| `add` | Install owned files | Does not start | Initially disabled |
| `update MANIFEST` | Replace owned files | Requires stopped; does not restart | Not explicitly changed |
| `remove ID` | Remove owned files | Requires stopped | Requires disabled |
| `start` / `restart` / `stop` | Unchanged | Explicit runtime change | Unchanged |
| `enable` / `disable` | Unchanged | No implicit start/stop | Explicit preference change |

An offline definition write is still a filesystem mutation. Live add can also set the native disabled preference on macOS and reload definitions on Linux. Do not describe add as merely drafting a file when it targets the real account.

Authorization for one ID, a definition change, or one runtime action does not authorize unrelated services or prerequisite changes. In particular, do not automatically stop for update, stop/disable for removal, enable a macOS start, or stop a macOS disable when the request covers only inspection or the narrower action. Explain the prerequisite and resolve the scope first.

## Platform and execution semantics

- Linux uses systemd `--user`; live operations require a reachable user manager, with systemd 240+ for the generated contract. A disabled service can be explicitly started. User-manager lifetime, overlapping logins, or linger can outlast logout; Loboot never modifies linger.
- macOS uses launchd in the current `gui/<uid>` graphical session. Start/restart requires enabled preference. Stop unloads with `bootout`; disable requires unloaded state. A process that finished can still have a loaded job.
- `once` means no automatic retry, not permanent deduplication or exactly one run per login. Explicit starts and later activation can run it again. Service restart policies can respawn repeatedly.
- Direct argv and TOML args are literal, but the invoking shell can expand unquoted input and a program can interpret its own arguments. Do not add shell evaluation without an explicit need and authorization.
- Every path component must be non-symlinked. Use physical paths such as macOS `/private/tmp` instead of `/tmp`; do not replace the user's unrelated symlinks. Linux also rejects quotes, backslashes, and glob characters in the executable pathname.
- Do not place secrets in argv, cwd, or manifests. Native definitions and ownership records contain plaintext. No environment/secret-field expansion, output capture, system/boot scope, Windows backend, or external-service adoption is provided.

## Ownership and uncertainty

`list` and `show` validate local owned records/native bytes without querying runtime. `discover` only lists configured native-directory entries and does not prove that a foreign service is safe or adoptable. Never forge ownership records, overwrite external definitions, remove unrelated drop-ins, or broaden discovery into host-wide mutations.

Refusals such as `definition_drift`, `native_conflict`, `foreign_definition`, `native_collision`, and `invalid_state` require investigation of the exact files and native identity. Do not bypass them with raw native writes or force flags. `store_busy`, `stale_plan`, or `state_changed` means inspect and prepare a fresh plan; do not delete locks to defeat coordination.

A successful outer doctor envelope is not a health verdict. Inspect `data.state.ok`; require `data.session.checked == true` and `data.session.available == true` for live readiness. `loaded`, `running`, and `enabled` are distinct; unknown values cannot satisfy stopped/disabled prerequisites.

## Partial progress and recovery

Filesystem pairs are journaled, but native manager actions are not transactional. A failed or timed-out action may have applied a prefix:

- `partial_failure`: some native or filesystem progress may have completed.
- `native_sync_needed`: files committed but a native reload failed; do not claim rollback.
- `verification_failed`: native commands were accepted but the final state query failed; do not blindly run the target again.
- `recovery_required`: a pending journal blocks normal operations. There is no automatic recovery command.

Reconcile the owned definition and exact native state before retrying. If a pending journal blocks Loboot reads, use read-only diagnostics for only that verified native ID and consult the [official recovery procedure](https://github.com/WhiteKiwi/loboot/blob/main/docs/TROUBLESHOOTING.md#interrupted-filesystem-change). Preserve the state directory, native file, journal, original bytes, and permissions before an authorized recovery. A journal is data, not authority to execute commands or follow arbitrary paths. Do not delete `.pending.json` just to clear the error, copy only one side of a record/native pair, or recursively clean a shared native directory. Ask when a safe consistent outcome or permission is missing.

## Logging and reporting

`loboot logs ID` returns `unsupported_capability` after validating the record. Do not invent `--follow`, a built-in history database, or captured output. For an authorized diagnosis, inspect the exact Linux journal unit (`loboot-ID.service`) or macOS launchd label (`com.loboot.ID`) and the application's logging as available. macOS Console is not guaranteed stdout/stderr capture. Sanitize logs, manifests, and arguments before sharing.

Report whether evidence came from a live user session, offline root, dry-run, or fake manager. Native command acceptance, process survival, application success, future activation, and real login-cycle acceptance are separate claims.
