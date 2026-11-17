# Cluster Lifecycle

Use this workflow for display, start, stop, restart, destroy, redeploy, prune, `demo`, and `perf`. Refresh deployment and real runtime state immediately before every mutation.

## Existing-Deployment Fast Path

After routing an existing deployment's display/start/stop/restart/redeploy or automatic-start request here, do not load configuration-deployment, installation, mirror, tenant, testing, diagnostic, or sibling-skill references merely because they exist. Use the shared operation contract and completion criteria, add automation execution only for unattended or measured work, and add cleanup boundaries only for destroy/redeploy/prune or another actual removal. Read configuration-deployment only for a first start, failed-initial-start recovery, or a requested configuration/path change; read package acquisition only when the requested operation actually needs a new artifact. A concrete dependency such as OCP, standby tenants, or monitoring still routes to its owning reference.

For a healthy, already registered deployment with no package or configuration change, the compact sequence is: resolve the exact target and installed command form; capture OBD plus real process/listener/data-plane state; execute the one requested transition; verify the intended state at all applicable layers; then stop. Do not turn this fast path into a broad health audit or an excuse to skip destructive authorization.

## Resolve the Target

Record the controller, deployment, product form, component/plugin and artifact identities, registered servers, paths, ports, current OBD status, actual processes/listeners, SQL/API health, active tasks, tenants, backups, and external dependants.

Read the exact selected subcommand help. If server, component, or service selectors are available, resolve them to an explicit target list and show selected and unselected objects. Short options are command-scoped; prefer long names and never reuse `-S` from a deployment example in another command.

## List and Display

Preserve the ordinary logical-inventory path before choosing a lifecycle mutation:

```bash
obd cluster list
obd cluster display <deploy_name>
```

Confirm these forms with the installed help. They can initialize or reconcile controller-local `OBD_HOME` state and write a trace; treat that as ordinary CLI bookkeeping unless the user explicitly requires strict zero-write inspection. Their output describes controller registration and reported status, not proof that every process, listener, dependency, or data plane is healthy. For a status-only request, stop after the requested inventory unless the user separately asks for diagnosis or a state change.

## Start, Stop, and Restart

Before start, establish whether the deployment is fully installed or partially initialized, whether ports and paths remain owned by it, and whether dependencies are ready. For the first start or recovery from a failed initial start, apply the configuration-deployment [host-environment](config-deployment.md#host-environment-initialization) and [storage-topology](config-deployment.md#storage-initialization-invariants) rules; do not change initialized storage paths or create Observer-internal directories as a retry shortcut. Before stop/restart, identify application routing, active workload, replication/management relationships, and the acceptable outage.

For unattended execution or measured availability, read [non-interactive automation execution](../../references/automation-execution.md). Record command events separately from the last successful authenticated probe, listener loss, expected PID transition, listener recovery, and first successful authenticated probe; command duration is not database downtime.

Inspect the version-matched stop and restart workflows for a pre-stop compaction stage. In the inspected `ob-deploy` tree, the OceanBase 4.2.1.4 workflows add `connect` and `compaction` before stop or restart unless an internal `skip_compaction` input is set. The matched compaction plugin issues minor freezes for `sys`, `all_user`, and `all_meta`; a connection failure or an individual SQL failure is warned and the workflow can continue. Disclose the freeze and possible I/O/compaction impact before execution, preserve each warning, and verify the freeze/compaction outcome independently instead of inferring it from the later stop or restart exit.

Do not invent, expose, or recommend the internal `skip_compaction` input as a user option. Use it only if the installed public command help explicitly exposes a supported equivalent and its consistency and recovery impact has been reviewed.

Run only the reviewed command form:

```bash
obd cluster start <deploy_name> [version-supported selectors]
obd cluster stop <deploy_name> [version-supported selectors]
obd cluster restart <deploy_name> [version-supported selectors]
```

Do not widen a scoped request to the whole deployment. Afterward, verify every selected target reached the intended state, every unselected target remained unchanged, dependency order is healthy, and the applicable SQL/API/data-plane check passes. Report mixed states explicitly.

Before a scoped `restart`, require the deployment to be fully running and healthy and inspect the selected build's status branch. Inspected OBD implementations can accept a stopped deployment and call a whole-deployment start before applying restart component/server selectors when state is stopped or unhealthy. Therefore, never issue a scoped restart against a stopped, partially running, or unhealthy deployment unless that implicit full start and every affected component have been separately displayed and authorized. If the request must remain scoped, stop and use a version-proved alternative.

Treat `reload` according to its own installed help rather than borrowing restart selectors. Current inspected OBD HEAD exposes no component/server selector for reload and applies the workflow across the deployment; on a stopped or unhealthy deployment it can first start the whole deployment. Present and authorize reload as a whole-deployment configuration/availability operation, or stop when the requested scope is narrower.

## Automatic Startup and systemd

Treat a plugin field such as `enable_auto_start` as a persistent privileged host mutation, not an ordinary runtime parameter. Before enabling or disabling it, inspect the exact installed plugin script and record the service account, unit name/content, executable and PID paths, start/stop/restart policy, sudo path, files copied, permission changes, marker files, `systemctl` operations, and behavior during reload and destroy.

Verified current OceanBase plugin code can copy an `auto_start.sh` helper, create an `obd_oceanbase_<appname>.service` unit, run `daemon-reload` and `enable`, configure `Restart=on-failure`, and recursively make the deployment `tmp` directory world-readable/writable/executable. It can also feed an SSH password to `sudo -S`. Treat these as version-specific implementation evidence. If the broad permission or credential exposure violates policy, stop; do not enable auto-start and do not “fix” the shipped workflow by silently editing it.

Enable or disable automatic startup only when the user requested that outcome. The request authorizes the exact reviewed per-host persistent diff; show and record its collision/privilege/security impact, but do not ask for a second confirmation merely because it persists. Verify the installed unit's checksum/content, owner/mode, enabled/active state, PID ownership, marker/helper paths, effective directory permissions, and agreement with OBD and SQL health. Do not reboot merely to test it unless reboot was also requested.

Enabling a unit and placing an already running Observer under that unit are separate states. In the tested OceanBase plugin path, OBD creates and enables `obd_oceanbase_<appname>.service` but does not attach an Observer that OBD already started. The unit can therefore be `enabled` yet `inactive`; `systemctl stop` in that state can return success while stopping nothing. Do not report the service as operational merely because the unit exists, is enabled, or a no-op stop returned zero.

When the user requested an operational systemd test but did not authorize a host reboot, use this bounded ownership transition after verifying the installed unit and acceptable outage:

| Stage | Action and required evidence |
|---|---|
| Unit creation | Enable `enable_auto_start` through the supported configuration/reload path; verify the exact unit, marker/helper, `is-enabled`, content, owner/mode, and unchanged running Observer. An initially inactive unit is expected when OBD owns the current process. |
| systemd start | Stop the deployment through OBD and prove the Observer/listener/SQL transition down; then start the exact unit with `systemctl` and prove `active`, `MainPID`/cgroup ownership, Observer listener recovery, and authenticated SQL. |
| systemd stop | Stop the exact unit and prove its managed PID, listener, and SQL transition down. A zero exit without those changes is a no-op, not PASS. |
| Restore | Start the deployment through OBD, verify OBD/runtime/SQL health, then disable automatic start through the supported configuration/reload path when the requested final state is disabled. |

After a systemd-owned transition, OBD's cached label can lag the real process. Reconcile registration, process/cgroup, listener, obshell, and SQL evidence before issuing the next lifecycle command; do not repair a cache/runtime disagreement with force, manual PID deletion, or redeploy.

Disabling the setting, reloading configuration, and destroying a deployment can remove different subsets of the marker, enabled state, helper, and unit. Inspect the selected version's cleanup path first. Disabling automatic startup alone must not stop a currently running database process; stop it only when a separately reviewed stop or destroy scope has been authorized. Afterward verify `systemctl` state, unit-file absence/presence as intended, daemon state, processes, and retained permission changes. Never remove a similarly named unit or recursively rewrite permissions as generic cleanup.

## Destroy and Prune

Read [cleanup and ownership boundaries](../../references/cleanup-boundaries.md) before defining either removal set. Destroying runtime/data state and pruning controller metadata are separate operations.

`destroy` can stop services and delete deployment-owned data. Before requesting confirmation, show:

- exact deployment/component/server identity;
- all canonical home, data, log, and external paths and their ownership;
- tenants, backup state, replication/OCP/monitoring/client dependencies;
- what the installed destroy workflow removes and retains;
- recovery boundary and separately owned data that must remain.

Obtain destructive authorization immediately before the exact command. Do not add an ignore, force, or standby-bypass option automatically.

A deployment created in the current run, an empty business-tenant inventory, or discovery of a wrong zone/topology does not by itself authorize destroy and rebuild. Stop and report the current state unless the user already authorized that exact removal/recovery outcome. Never reinterpret a deployment defect as implicit cleanup consent.

Before launching `destroy`, establish whether the caller has a controllable TTY. In a non-interactive runner, use only a public command-local confirmation form whose installed help and observed semantics prove that it acknowledges this exact prompt without widening deletion, forcing process termination, or changing standby behavior. Otherwise require a real PTY; an ordinary input pipe is not an interactive-session substitute. Do not enable controller-wide automatic confirmation, pipe generic `yes`, or substitute a force option. If neither safe form exists, stop before launch.

If an earlier invocation is already waiting for confirmation, identify its caller-owned PID and children and determine whether destruction began. Interrupt only that waiting invocation through its caller/session boundary, then reconcile registration, tasks, processes, listeners, and paths before another attempt; do not leave it running or assume that terminating the client rolled back server-side work.

After that authorization, preserve the installed public command shape. In an interactive session use the ordinary prompt; in a non-interactive session, reviewed V4.6.0 builds expose `--confirm` as the command-local acknowledgement for the already-authorized deployment:

```bash
obd cluster destroy <deploy_name>
obd cluster destroy <deploy_name> --confirm  # non-interactive, only when installed semantics match
```

Do not use `-f` as confirmation. On this command it means `--force-kill` and changes process-termination behavior; it requires its own proved need and authorization.

After destroy, report independently whether deployment-owned processes/listeners/data paths were removed; empty deployment parent directories remain; OBD registration/configuration and traces remain; local mirror/package repositories remain; and any unexpected process, listener, data, unit, task, or reference remains. Expected controller evidence or an empty parent directory is not a failed data-destruction result, and destroy does not authorize `prune-config` or repository cleanup.

If the cluster was managed or taken over by OCP, do not infer that deployment destroy removed the node-local OCP Agent. Inspect every former managed node for agent processes, listeners, service state, packages, directories, saved package-manager configuration, and OCP-side tasks/records. Classify any residue separately from the deployment runtime/data result and follow the [OCP Agent cleanup boundary](../../references/cleanup-boundaries.md#ocp-agent-residue); destroy authorization does not include that cleanup.

Use `prune-config` only after proving the deployment is in a version-supported metadata-only state and inspecting what the installed command removes. Inspected implementations allow `destroyed` or `configured`; do not use it for a deployed or running state. Permission to destroy does not authorize metadata pruning. Verify absence of the exact authorized objects and preservation of unrelated deployments and paths.

```bash
obd cluster prune-config <deploy_name>
```

Ordinary test cleanup does not prune controller metadata by default. If the user explicitly requests complete removal of this run's unique named deployment and the displayed removal set includes both runtime/data destruction and controller registration, that exact authorization may cover the staged `destroy` followed by `prune-config`; do not treat the default separation as a prohibition. After destroy, re-prove an eligible metadata-only state, confirm the exact deployment name through the PTY/confirmation rules above, prune only that registration, and verify all unrelated deployments remain. “Complete removal” of a deployment does not implicitly include mirror packages, repository definitions, the OBD installation, external storage, or unrelated traces unless those objects were separately enumerated and authorized.

## Redeploy

Redeploy is a destructive rebuild, not a repair, reload, component-add, or monitoring-install shortcut. Require the normal destroy evidence plus the exact replacement artifacts/configuration, backups and recovery plan, outage, tenant outcome, and post-rebuild identity expectations.

If OCP is present, read [ocp.md](ocp.md) and classify its MetaDB and takeover relationship before authorization. Prove separately what redeploy will and will not erase from every external data path.

After the complete destructive-rebuild plan is authorized, use only the installed public form:

```bash
obd cluster redeploy <deploy_name>
```

After redeploy, verify the replacement artifact/configuration, process/listener state, authenticated data plane, tenant/data outcome, and every management/monitoring relationship. A newly healthy process does not prove data or control-plane continuity.

## Quick-Deploy Shortcuts

`obd demo` and `obd perf` are integrated mutating convenience workflows, not configuration generators. Their deployment names are fixed to `demo` and `perf`. Use either only when the user explicitly chooses that exact shortcut and accepts its installed behavior.

Before execution, read installed help/workflow; inspect the matching registered name, target paths, ports, processes, and component set; and explain every object that can be overwritten or removed. In the inspected current source, `demo` internally enables force, clean, force-delete, and force-kill, while `perf` enables force, clean, force-delete, and maximum-resource generation. These are implicit implementation behaviors even when the user does not type those flags. Reconfirm them for the installed build and bind authorization to the complete collision and deletion set. Prefer a uniquely named config deployment whenever ownership is unclear.

`perf` is the official maximum-specification local quick-deploy command, not an alias for `autodeploy`. It defaults to a build-defined component set and a fixed `perf` namespace. Do not silently substitute `autodeploy`, use it as a general production or multi-node deployment path, or assume “maximum” consumes every byte safely. The reviewed build advertises community component keys for this shortcut, but that is a build-specific command surface rather than a rule that quick deployment is inherently community-only; use a commercial component only when the installed `perf` help explicitly lists it. Reserve OS and operational headroom and review the generated topology and resources before execution.

Resolve the generated home path before the first shortcut invocation. In the tested command implementation, the base is the selected SSH username's home when one is supplied, otherwise the controller process's `HOME`, and OBD appends the component key. A root-local `oceanbase-ce` shortcut therefore defaults to `/root/oceanbase-ce`. This default can land on a small root filesystem even when a larger writable persistent filesystem is mounted elsewhere.

Before either shortcut, check free bytes and ownership on the actual generated home/data/log mount rather than only the machine-wide disk inventory. Tested OceanBase CE shortcut generation can require roughly 24 GiB before deployment and reports an `OBD-2003` insufficient-disk error when the selected mount cannot satisfy its generated data/log minimum. Treat that result first as a path/capacity failure, not a package or network failure. The exact threshold remains component/plugin/version dependent.

When the default path is unsuitable, select the current user's largest writable persistent deployment filesystem using the normal directory rule and pass only an installed-command-proved component-scoped override. The tested dynamic option shape is:

```bash
obd demo --components=oceanbase-ce --oceanbase-ce.home_path=<reviewed_writable_path>
obd perf --components=oceanbase-ce --oceanbase-ce.home_path=<reviewed_writable_path>
```

Confirm the option against the installed shortcut parser or an already tested identical build; permissive unknown-option parsing is version behavior, not a universal CLI contract. Prove the fixed deployment name, generated path, component set, ports, and deletion/collision set again after generation. For `perf`, also require that the target is suitable for exclusive maximum-resource use and that the generated allocation preserves the required operating reserve.

For multi-node maximum utilization, do not repeat `perf` per host. Follow the cluster-consistent workflow in [maximum-utilization.md](maximum-utilization.md).

For a database-only demo scope, prefer the explicit long form with the resolved component when installed help confirms that component. The reviewed V4.6.0 example is:

```bash
obd demo --components=oceanbase-ce
```

Do not infer from that example that every build excludes `oceanbase`; equally, do not substitute `oceanbase` unless the installed shortcut help exposes it.

After execution, verify the registered `demo` component list, real processes/listeners, exact paths, and authenticated SQL/HTTP data planes that apply. Report cleanup or overwritten state separately from the new demo result.

For `perf`, perform the same checks against the registered `perf` deployment and verify the actual resource allocation and component set rather than inferring them from the command name.

## Failure Handling

Preserve trace IDs and inspect registered state, real processes, listeners, paths, and component health before retrying. A caller timeout may leave a running OBD process or remote task; reconcile it as succeeded, failed, still running, or unknown before another invocation. A non-zero exit may follow a partial stop or start. Never use redeploy, destroy, broad restart, or path deletion as generic cleanup.

## Sources

- Official OBD V4.6.0 Command Guide sections 1.1–1.2 and the cluster lifecycle command group.
- Official OBD V4.6.0 Quick Start section 2.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `_cmd.py` `DemoCommand` and `PrefCommand`; version-matched lifecycle workflows under `workflows/` in the exact inspected checkout.
