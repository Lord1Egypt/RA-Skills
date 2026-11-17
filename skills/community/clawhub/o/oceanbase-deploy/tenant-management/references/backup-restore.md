<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="backup-restore"></a>
<a id="backup--restore"></a>
<a id="setting-up-backup"></a>
<a id="step-1-configure-backup-paths"></a>
<a id="step-2-run-backup"></a>
<a id="restoring-from-backup"></a>
<a id="notes"></a>

# Tenant Backup and Restore

Use this workflow for archive/backup configuration, backup execution and inspection, or tenant restore. Read the installed public help for every selected subcommand. Inspect the version-matched packaged component workflow only when the public interface, version-matched documentation, and observed state leave an execution-critical behavior unresolved. The command shapes below preserve useful current OBD forms but are not a substitute for that capability check.

## Fix the Identities

For backup, record the source deployment, cluster ID, tenant ID/name, tenant role, OceanBase version, backup mode, data-backup URI, archive-log URI, storage identity, encryption/KMS material source, and retention objective.

For restore, also record the chosen backup set/manifest, source cluster and tenant IDs, start/end SCN and time coverage, target deployment and tenant, target compatibility mode, zones/resources, recovery timestamp or SCN, and whether the target tenant already exists.

Do not identify a backup only by a directory name or wall-clock label. Preserve a manifest containing the source identities, backup-set identity, SCN/time range, data and log URIs, encryption method, OBD/OceanBase versions, completion state, and integrity evidence.

## Validate Storage from Every Required Node

Resolve each URI according to its storage type. Verify that every Observer or worker used by the installed workflow reaches the same storage account, bucket/prefix or canonical mount, region/scope, and underlying filesystem identity. Check read/write/list permissions, ownership, free capacity, quotas, network path, TLS policy, and expected throughput.

For a `file:` or NFS-backed target, identical path strings do not prove identical storage. Compare the real mount/source identity on every required node and detect symlinks or local directories accidentally shadowing a mount.

Keep access keys, URI credentials, encryption passwords, decryption keys, and KMS material out of commands and reports whenever a protected input or credential reference exists. If the selected command accepts a required secret only in an argument, disclose process-list/shell-history exposure and use an approved permission-controlled local procedure; do not describe that path as protected.

## Archive and Backup State Machine

Treat archive configuration, archive readiness, backup execution, and archive retention/stop as distinct states:

1. configure the reviewed data and archive destinations;
2. verify archive logging reaches the version-specific ready/doing state and advances;
3. start the selected full or incremental backup;
4. poll the OBD task and database-side backup views to a successful terminal state;
5. record the backup-set identity and SCN/time coverage and validate the manifest;
6. retain or stop archive logging according to the recovery policy through a separately reviewed operation.

Before querying database-side backup or archive state, follow [version-adaptive SQL evidence](../../references/sql-evidence.md): confirm the OceanBase version and inspect the actual view/column surface before choosing a query. Do not assume one release's backup/archive fields exist in another, and do not classify a task as failed merely because a remembered query is unsupported.

Do not invent an archive-enable/disable command when the installed OBD workflow does not expose one. Use the installed help and database-side state to determine what `set-backup-config` actually changes.

Version-supported command shapes include:

```bash
obd cluster tenant set-backup-config <deploy_name> <tenant_name> \
  --data_backup_uri=<data_uri> \
  --archive_log_uri=<log_uri> \
  [version-supported policy options]

obd cluster tenant backup <deploy_name> <tenant_name> \
  --backup_mode=<full_or_incremental> \
  [version-supported encryption credential option; value supplied only through the approved local procedure]

obd cluster tenant backup-show <deploy_name> <tenant_name>
```

Some versions expose a combined data-and-log option such as `--plus_archive`; use it only after confirming its exact coverage and recovery semantics.

## Cancel a Backup or Restore Task

Cancellation is a separate mutation, not an error-handling default and not implied by permission to start the task. Before either command, identify the exact deployment, tenant, task type and ID when exposed, current task status, storage or target-tenant effects, and the state that will prove cancellation complete. Re-read the installed help and workflow because accepted states and post-cancel visibility can differ by version.

For a backup whose observed status is cancelable, the V4.6.0 command shape is:

```bash
obd cluster tenant backup-cancel <deploy_name> <tenant_name>
obd cluster tenant backup-show <deploy_name> <tenant_name>
```

The V4.6.0 documented boundary permits cancellation only before `COMPLETED` and requires a later `backup-show` result of `CANCELED`. Treat the cancel command's return as request submission only. Poll `backup-show` within a defined deadline and report `unknown` or `not canceled` if the task does not reach the required state; do not delete backup objects or retry the backup while its state is unresolved.

For a restore whose observed status is cancelable, the V4.6.0 command shape is:

```bash
obd cluster tenant restore-cancel <deploy_name> <target_tenant_name>
obd cluster tenant show <deploy_name>
obd cluster tenant restore-show <deploy_name> <target_tenant_name>
```

The V4.6.0 documented boundary permits cancellation only before `SUCCESS`; its acceptance check is that the target tenant is absent and the restore query has no corresponding task. Reconfirm those semantics in the installed version. If the target tenant or task remains, or either query is ambiguous, cancellation is not complete. Do not drop a remaining tenant as an implicit continuation of `restore-cancel`.

The inspected 4.7 cancellation plugin submits its OBShell patch/delete and returns without polling the final state. Its exception text also says `restore` for both task types, so a backup-cancel failure can be mislabeled. Classify the operation from the invoked command, recorded task type, and post-command state—not from that error noun—and never redirect recovery to a restore task solely because of the message.

## Restore Plan and Authorization

Prove that the selected data backup and archive logs form a continuous recovery chain through the requested target. Choose exactly one recovery target form accepted by the installed command, such as `--timestamp` or `--scn`; do not pass both or silently use the latest point.

The official V4.6.0 flow and inspected current plugin restore into a new tenant and refuse an existing target. Preflight the name before submission; if it already exists, stop rather than dropping it, inventing an overwrite mode, or converting restore authorization into tenant-deletion authorization. Reconfirm this behavior for the installed plugin, and treat any future build that exposes replacement semantics as a different destructive workflow requiring its own documented evidence and authorization.

Define the restore resource plan explicitly: selected zones, primary zone/replica policy, Units per zone, minimum/maximum CPU, memory, log disk, and IOPS settings supported by the installed command. Do not omit values and inherit capacity-maximizing defaults. Verified current code selects every zone when `--zone` is absent. Its shared resource checker reads a different `zone_list` option, so even when restore `--zone` is present it can calculate omitted CPU/memory defaults across all active zones and choose the minimum remaining capacity among those servers. Treat that mismatch as implementation evidence: pass explicit resource values and verify the resulting Unit Config rather than relying on defaults.

Inspect pre-submit and failure behavior. Verified current restore code creates a timestamp-named `restore_unit_config*` before submitting the restore DAG; later failure can leave that object. When the DAG fails or times out, the workflow can automatically issue `ROLLBACK` and then `PASS` if rollback itself fails. Disclose these automatic state transitions as part of restore authorization and record the expected resource-object cleanup/retention. They are distinct from a later user-requested task cancellation.

A version-supported restore command is shaped as:

```bash
obd cluster tenant restore <deploy_name> <target_tenant_name> \
  <data_backup_uri> <archive_log_uri> \
  [--timestamp=<target> | --scn=<target>] \
  --zone=<reviewed_zones> \
  --primary-zone=<reviewed_primary_zone> \
  --unit-num=<reviewed_units_per_zone> \
  --max-cpu=<reviewed_cpu> \
  --min-cpu=<reviewed_min_cpu> \
  --memory-size=<reviewed_memory> \
  --log-disk-size=<reviewed_log_disk> \
  [version-supported --max-iops/--min-iops values] \
  [version-supported replica-policy option with a verified usable spelling] \
  [other reviewed topology options] \
  [version-supported decryption or KMS option; value supplied only through the approved local procedure]

obd cluster tenant restore-show <deploy_name> <target_tenant_name>
```

Before execution, show the source backup identity, target tenant, target point, resources, expected data-loss window, storage reads/writes, existing-target behavior, and rollback boundary.

## Completion

For backup, require a successful terminal task, database-side backup success, a complete manifest/catalog entry, verified SCN/time coverage, accessible artifacts from the required nodes, and integrity checks supported by that version.

For restore, require a successful terminal task, a healthy target tenant with the intended source identity and recovery point, correct resources and allowlist, authenticated login, and a bounded representative data check. Inventory every generated restore Unit Config/resource pool and verify that each is owned by and attached to the intended tenant or otherwise disposed of exactly as the reviewed workflow specifies. Do not expose business data in the report.

## Failure, Retry, and Retention

On failure or timeout, preserve the OBD trace, task/DAG rows and automatic `ROLLBACK`/`PASS` outcome, archive state, version-proved backup/restore view results, manifests, storage object listing, target-tenant state, every `restore_unit_config*`/pool created by the attempt, and the completed stage. Reconcile a caller timeout through the shared succeeded/failed/still-running/unknown state workflow. Determine whether the task is cancelable, resumable, or requires a documented recovery action before retrying. Route an authorized cancellation through the explicit state and acceptance workflow above; do not infer completion from the cancel command's exit status.

Do not delete a failed backup prefix, archive pieces, partial restore tenant, or prior valid backup as generic cleanup. Decide before execution which manifests, backup sets, archive logs, generated configuration, and temporary files must be retained. Apply storage retention or deletion only as a separate, precisely scoped operation after proving that the recovery window and dependent restores remain valid.

## Sources

- Official OBD V4.6.0 Command Guide tenant backup/restore command sections.
- Official OBD V4.6.0 User Guide section 29.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `plugins/oceanbase/4.2.1.4/backup.py`, `restore.py`, and backup/restore task query/cancel plugins in the exact inspected checkout.
