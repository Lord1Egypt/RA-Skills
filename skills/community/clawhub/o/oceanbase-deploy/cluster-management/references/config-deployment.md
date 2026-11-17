<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="config-file-deployment"></a>
<a id="deploy-with-config-file"></a>

# Configuration-File Deployment

Use a reviewed configuration file for reproducible community or commercial OceanBase deployment. This workflow registers a deployment and installs component artifacts; starting it is a separate state transition.

<a id="cluster-operations-after-deployment"></a>
<a id="edit-config"></a>
<a id="reload-config"></a>
<a id="upgrade-component"></a>
<a id="add-delete-component"></a>
<a id="add--delete-component"></a>

## Legacy Operation Links

Published 2.x links for post-deployment operations resolve here. Continue with the matching dedicated workflow:

- `edit-config` or `reload-config`: [edit or reload configuration](configuration-changes.md)
- `upgrade-component`: [upgrade a component](upgrade.md)
- `add-delete-component` or `add--delete-component`: [add or delete components](component-changes.md)

<a id="component-selection"></a>

## Select the Product Blueprint

Resolve the product form before writing YAML, then read exactly one blueprint:

- [Community distributed](deployment-templates/community.md)
- [Commercial distributed](deployment-templates/commercial-distributed.md)

The blueprints are intentionally schema-gated. They identify required decisions and configuration structure without claiming that fields from one OBD/plugin version are valid in another. Produce an executable YAML only after validating every key against the selected installed plugin.

Community and commercial distributed are one OBD operating family. Their blueprints preserve different component/package identities and acquisition boundaries, but use the same named-server/global structural model and ordinary deploy/start/lifecycle workflow unless installed evidence proves a real difference. Do not require a separate commercial implementation path for a generic distributed operation, and do not read both distributed blueprints for one deployment.

## Discover the Controller and Existing Cluster

Apply the shared [default controller, SSH, and cluster discovery rule](../../references/operation-contract.md#default-controller-ssh-and-cluster-discovery) before package acquisition or YAML construction. This rule is identical for configuration-file, interactive, autodeploy, demo, and perf workflows: OBD stays on a cluster target host by default, and if every target is proved to have no OBD, install it on the first supplied host with package-manager non-interactive acceptance and without asking the user to choose or approve the install command. Use the user's supplied SSH login user on every deployment machine; if no login user is specified, use `root`, and if no authentication material is supplied, use passwordless SSH. After login, retain that login-session user for every operation, including OBD ownership and controller-to-node SSH. If passwordless controller-to-node access is absent, directly append the controller login user's public key to the same login user's `authorized_keys` through already-verified access without another prompt.

Do not ask whether the cluster is already deployed or whether the machines are clean. Inspect candidate OBD controllers, all target runtimes, listeners, services, relevant paths, and reachable database identity, then classify the observed state. A new deployment can proceed only after the intended name, paths, ports, and machine identities are proved non-conflicting; a registered, stopped, partial, or unmanaged cluster is discovered state to report and handle through its owning workflow, not a question to delegate back to the user.

## Default Maximum-Utilization Sizing

If the user supplies resource values, a cap, reserve, or a non-maximum profile, preserve that sizing. Otherwise, do not ask the user to choose a deployment size and do not fall back to mini, demonstration, or arbitrary OBD defaults. Select the [maximum-utilization workflow](maximum-utilization.md) and derive the largest verified configuration that fits the resolved target hosts, installed product/plugin behavior, filesystem commitments, and required operational reserves.

This default changes resource sizing only. It does not infer additional hosts, replicas, optional components, tenants, or unneeded persistent host mutations. For a new distributed deployment with multiple user-supplied Observer hosts and no explicit zone mapping, assign each distinct host to a distinct new zone in deterministic host order without asking; preserve any explicit mapping. For multi-node sizing, derive every node's candidate independently and take the minimum across all target nodes separately for each resource key. When a target is shared and safe maximum sizing requires an unknown reserve or cap, inspect existing commitments first and ask only for the missing reserve/cap decision if it cannot be derived; do not ask the user to choose a general deployment profile.

## Default Deployment Base Directory

Apply this default only to a new deployment when the user did not specify the relevant deployment or storage paths. Preserve every explicit user path. Never apply it to an existing registered, stopped, partial, or unmanaged deployment, and never relocate an initialized `home_path`, `data_dir`, `redo_dir`, log path, or other owned path as a repair or optimization.

Resolve the base independently on every target while logged in as the same login-session user that will run OBD and own the deployment:

1. Enumerate canonical mounted filesystems and their available bytes, inode capacity, mount options, quota visible to the login user, persistence, and underlying mount identity. Rank candidates by usable free bytes after known commitments and required reserves—not by directory entry count, `du`, nominal device size, or a remembered path name.
2. Exclude read-only, virtual, pseudo, volatile-memory, package-image, container-overlay, network/shared, inaccessible, unknown-ownership, symlinked, non-empty deployment, or conflicting filesystems and paths from this tested automatic-selection workflow.
3. On each remaining filesystem, resolve a safe canonical parent that the login-session user can read, write, and traverse. In implementation mode, prove those effective permissions with a bounded uniquely named create/remove probe in that parent before rendering YAML. Do not `chmod` or `chown` an existing directory merely to make a larger filesystem win.
4. Select the eligible filesystem with the greatest usable free capacity. On an exact tie, prefer the candidate with greater usable inode capacity, then the lexically first canonical parent for determinism. Do not fall back to the login user's home while a larger eligible filesystem exists, and do not assume that `/data/1`, `/data`, or `/mnt` exists or is largest without inspection.
5. Create new, empty, non-symlinked, deployment-specific paths beneath the selected parent, owned by the login-session user. Resolve component `home_path`, `data_dir`, `redo_dir`, log, cache, and temporary paths as the installed schema and component layout permit. For Observer defaults, make home, data, and redo disjoint siblings such as `<base>/home`, `<base>/data`, and `<base>/redo`; when an eligible separate redo filesystem is selected, use a deployment-specific redo path on that filesystem instead of forcing it under the home/data filesystem. When the schema supports host-specific paths, retain each host's independently selected paths; when it requires one common path string, use a path that is eligible on every target and record that constraint.

Record the selected canonical base, filesystem, usable free bytes, ownership, mode, quota, and rejected larger candidates for each host. If no eligible persistent parent has enough capacity for the verified deployment commitments, stop and request a path or permission decision instead of silently using a smaller or unwritable location.

<a id="observer-storage-path-invariant"></a>

### Observer Storage-Path Invariant

Apply this invariant before creating directories or rendering any Observer YAML, including generated maximum-utilization input:

- Treat `<home_path>/store` as OBD's canonical Observer data entry. If `data_dir` is omitted and the installed plugin defaults it to `<home_path>/store`, that path may be the real data root. If an explicit `data_dir` differs from the default, keep `<home_path>/store` available for OBD to make it resolve to that data directory, normally through a symlink.
- Never set `data_dir` or `redo_dir` below `<home_path>/store`, and never pre-create `<home_path>/store` as the parent of either one. An explicit `data_dir` may equal `<home_path>/store` when the installed plugin supports that direct-root layout; `redo_dir` may equal it only when it intentionally equals that same data root in a plugin-supported single-root layout. Reject any other layout that requires the same path to be both a real parent directory and OBD's canonical data alias. In particular, `<home_path>/store/data` and `<home_path>/store/redo` are invalid custom-path defaults.
- For automatically derived custom paths, use disjoint sibling paths. A safe shape is `<base>/home`, `<base>/data`, and `<base>/redo`; with a separate log mount, use `<log-parent>/<deploy-name>/redo` while keeping home and data under their selected parents. Canonicalize path boundaries and reject cycles or ancestor relationships that would make OBD initialization, linking, or cleanup traverse another owned path.
- A plugin/schema that accepts `redo_dir` supports a separate redo topology unless version-matched authoritative behavior proves a narrower constraint. The observer command's `-d <home_path>/store` is the canonical entry point, not proof that `redo_dir` is ignored. Do not collapse a valid separate redo path onto the data filesystem merely because the start command uses that entry point.

For example:

```text
invalid:
  home_path = /data/1/demo
  data_dir  = /data/1/demo/store/data
  redo_dir  = /data/1/demo/store/redo

valid siblings on one filesystem:
  home_path = /data/1/demo/home
  data_dir  = /data/1/demo/data
  redo_dir  = /data/1/demo/redo

valid separate redo filesystem:
  home_path = /data/1/demo/home
  data_dir  = /data/1/demo/data
  redo_dir  = /data/log1/demo/redo
```

## Database Bootstrap Password Default

For a new OceanBase cluster, default every OBD-generated database bootstrap credential—especially the initial `root`/`sys` password—to OBD ownership. Unless the user explicitly supplied an override, do not ask for a password, generate one in the agent, or render the password key with an empty, null, placeholder, or guessed value. Prove that the installed deployment workflow generates a random value when the field is absent, then omit that field from the source YAML and let OBD materialize and retain the credential through its normal controller configuration path, treating that path as secret-bearing evidence.

When the user explicitly supplies an override, preserve that choice and pass it only through the approved protected local procedure; do not replace it with an OBD-generated value. If the installed build cannot prove the required random-generation path, report that version limitation instead of asking the user to invent a password or silently creating an empty-password database.

After deployment, verify without displaying the value that OBD generated or retained a non-empty credential, the controlling metadata/configuration has appropriate ownership and permissions, and an authenticated identity query succeeds. This default applies only to new-cluster database bootstrap credentials that the installed OBD workflow owns; it does not fabricate SSH, existing-database, tenant-create, storage, KMS, or external-service credentials.

## Static Component Inspection

When the user says “static analysis only,” “do not deploy,” or equivalent, treat that as a hard boundary. Inspect only supplied/local package metadata and file lists, an installed read-only OBD/plugin tree, and source/configuration artifacts. If extraction is necessary, use a new isolated temporary directory and record the artifact path and checksum.

By default, this static boundary permits only that isolated local scratch write; it keeps the inspected artifact, installed tree, controller state, target hosts, and deployments read-only. If the user explicitly requires strict zero-write analysis, do not extract or create temporary files. Report any conclusion that would require extraction as unresolved instead.

Do not install/uninstall a package, mutate a mirror or repository, register a deployment, run any deploy/start/component/lifecycle/plugin workflow, connect to a live database, or change a target host merely to test a prediction. Never execute extracted plugin, pre/post-install, bootstrap, start, or cleanup code. If a branch depends on runtime state, report it as conditional or unknown.

Classify the report explicitly:

1. **Packaged files** present before deployment.
2. **Controller metadata** OBD would maintain locally.
3. **Deploy-time target paths** an inspected workflow explicitly creates or copies.
4. **Runtime-conditional paths** created only after start or when an option is enabled.
5. **Unknown/not established statically** behavior requiring supported runtime or authoritative version-matched evidence.

Identify host role, owner when derivable, persistence/cleanup boundary, and evidence source for every path or effect. Remove only the isolated extraction directory created for this inspection, then verify that no deployment, process, listener, repository entry, service unit, or target-host path was created. Report the result as static, never deployment-tested.

## Build the Deployment Manifest

Before resolving artifacts, expand the selected topology through the shared [deployment package closure](../../references/deployment-package-sets.md). Record primary component packages, companion runtime packages, selected conditional utilities, image archives, and external prerequisites separately. The YAML component list alone is not the package closure.

Record these inputs before downloading artifacts or writing YAML:

| Area | Required inputs |
|---|---|
| Controller | host, user, exact OBD executable/build, `OBD_HOME`, active tasks |
| Product | product form, exact component key, component/plugin version |
| Artifacts | component, version, release, operating-system suffix when applicable, architecture, hash, source, dependency closure |
| Topology | deployment name, app/cluster identity, zones, server-to-component mapping |
| SSH | target machine identity, management IP, SSH user/port/key and privilege boundary |
| Paths | explicit user paths, or each host's verified largest writable persistent deployment base and the canonical home, data, log, redo, cache, and temporary paths beneath or associated with it as applicable |
| Network | management, SQL, RPC, obshell, proxy, monitoring, OCP, and component-specific addresses/ports |
| Resources | CPU, memory, disk, inode, filesystem/mount, cgroup/container limits, and headroom; explicit user sizing when supplied, otherwise the verified maximum-utilization derivation |
| Persistent host behavior | user-requested auto-start only; otherwise keep it disabled/unset without asking, and route an explicit request through the lifecycle systemd gate |
| Optional scope | requested OBProxy, OBAgent, monitoring, OCP, or Config Server |
| SQL acceptance tool | exact existing compatible controller-side client, or the pre-acquired `obclient` + matching `libobclient` closure when none exists |
| Database bootstrap credential | OBD-generated by default; protected user override only when explicitly supplied |
| Other secrets | approved protected input source and redaction plan; never literal reusable values |

Every component in the manifest must map to a requested outcome or a proved package/plugin dependency. A demo, repository listing, all-in-one bundle, or old YAML is not permission to deploy all contained components or create a tenant.

## Preflight

1. Read `obd --version`, the selected `obd cluster deploy --help`, and the installed public component schema/validation surface. Inspect a packaged workflow only when those interfaces cannot establish an execution-critical behavior.
2. Confirm exactly one compatible artifact for every required entry in the expanded deployment package closure, not only every YAML component. Record version, release, operating-system suffix, architecture, hash, and repository source; repository presence alone does not prove compatibility. Apply the shared exact-suffix, EL8, then EL7 compatibility fallback. Apply the [fixed mirror-source order](../../obd-administration/references/mirror-and-repositories.md#fixed-online-package-source-order) only to public/community artifacts. For commercial (Enterprise Edition) and standalone/centralized artifacts, use only an exact complete closure already in the controller's OBD local repository; if any entry is missing, ask the user to provide it and do not download it automatically. Verify every fallback's runtime dependencies.
3. Prove each target's hostname/machine identity, management address, OS, architecture, runtime libraries, time synchronization, routes, firewall boundary, and SSH behavior. Record the successful login-session user with `id -un`, retain it as the OBD and host-operation user, and complete the shared bounded passwordless bootstrap from that controller user to the same user on every target without a separate permission prompt when access is absent.
4. Resolve every path canonically. When paths were omitted for a new deployment, first apply the default deployment-base selection above under the login-session user. For Observer, enforce the [storage-path invariant](#observer-storage-path-invariant) before any directory creation: prove that data/redo paths do not descend from `<home_path>/store`, validate any direct-root equality against the installed plugin, and ensure every selected home/data/redo path maps to the intended filesystem without a cycle or conflicting ancestor. Inspect owner, effective read/write/traverse access, mode, free space, inode capacity, mount identity, quota, symlinks, non-empty contents, overlap with other deployments, and cleanup ownership.
5. Map every proposed port to its host and namespace. Check real listeners and processes, not only registered deployments.
6. Check available CPU, memory, log/data capacity, cgroup/container constraints, and topology failure domains. Do not infer usable resources from host totals alone. When the user supplied no sizing, complete the maximum-utilization workflow before rendering resource values.
7. Determine existing cluster state yourself by correlating OBD registrations with remote package/service records, processes, listeners, deployment paths, and SQL/obshell identity when reachable. The deployment name, app identity, paths, and ports must not collide with an existing, stopped, partial, or unmanaged service. Do not ask the user whether deployment already happened in place of these checks.
8. Run only the public version-supported precheck/strict-check path. In reusable deployment instructions spell `--strict-check` in full when the installed command exposes it; never transfer the short option `-S` from another subcommand.
9. Prove the controller-side SQL acceptance path before deployment. If no compatible client exists, acquire and verify the `obclient` + matching `libobclient` closure now. Do not defer this inventory until after the cluster is running or assume OBD's Python environment provides a usable SQL module.

<a id="host-environment-initialization"></a>

### Initialize the Host Environment Before Deployment

Do not wait for `deploy`, `start`, or integrated `autodeploy` to fail before preparing the targets. Read the installed help and run the public OBD precheck for every target under the same user and login mechanism the deployment will use. The new-deployment capability family can include `obd host precheck`, `obd host user init`, and `obd host init`, but these commands do not have an interchangeable mutation boundary. Start with precheck, map each failure to its owning setting, and choose the narrowest supported remediation.

Do not default to `obd host init` for `nofile`, `nproc`, `vm.max_map_count`, or another isolated limit/kernel failure. Inspected builds can also change ownership or mode on existing data paths. Before any `host init`, inspect the exact installed workflow and record every file, directory, package, service, kernel value, limit, owner, and mode it can change. Use it only when that complete diff is bounded and every affected path is either newly created for this deployment or explicitly included in the authorized scope. If the scope cannot be proved, use the narrow documented manual remediation for the exact precheck finding and rerun precheck. Treat `cluster init4env` and general-purpose host administration as separate workflows with their own scope and evidence; this deployment preflight neither invokes nor replaces them.

If an initializer prompts, use the real-PTY rules in [automation execution](../../references/automation-execution.md), not an ordinary input pipe. Immediately before and after an authorized initializer, compare every approved setting and path plus the owner/mode of all existing deployment data paths; an unapproved ownership or permission change is a failed initialization even when the command exits zero. Derive required and recommended values from the installed OBD/plugin output rather than hard-coding one test run's thresholds. Verify current kernel values directly, verify their persistent configuration, and establish a new SSH/login session as the deployment user before accepting PAM limits such as `nofile` or `nproc`; an old shell does not prove the persisted limit. Complete this flow before an integrated `autodeploy`, because that command can register or initialize deployment state before a later environment/start check fails.

If the installed public initializer is unavailable or reaches a proved failure, use manual remediation only for the exact reported setting and documented value. Preserve the prior value and persistence owner, apply the narrow equivalent change on every affected target, open a fresh deployment-user session when required, and rerun the public precheck. Do not replace this with broad guessed `sysctl`, limits, firewall, SELinux, repository, or path changes.

Declare the package-resolution mode before execution. In online mode, select the effective artifact source before the mechanism, prove the exact expected remote winner and final package URL, and retain source, mechanism, and attempt evidence for each exhausted source; do not require a local download when an enabled repository is proved to resolve the right source and candidate. If one online mechanism fails, keep the current source while trying another applicable controller-local `curl`, `wget`, package-manager, or OBD path. If an explicit download or bounded relay obtains the exact artifact, switch the complete closure to local-package mode. In a remote workflow, `local-package` and `local closure` mean controller-local, not relay- or runner-local. In local-package mode, prove the complete local closure, disable participating remote repositories through the reviewed mirror workflow, immediately verify their disabled state and the local winning hashes, and keep that isolation through the final package-selecting stage. Stop rather than allowing unresolved local/remote competition. Restore a temporary remote-mirror change after the workflow unless persistent disablement was separately requested.

Stop when the plugin schema, artifact closure, product compatibility, host identity, path ownership, or topology cannot be proved. Do not use `--force`, `redeploy`, path deletion, `init4env`, or a community package as a preflight workaround.

## Render and Review YAML

Render values from the approved manifest and selected plugin schema. For every field, record whether it is required by the schema, derived by the plugin, or explicitly chosen by the user.

Review the rendered file semantically:

- exact product/component keys and dependency relationships;
- server and zone identity, management versus service addresses; for a named-server distributed configuration, require one sibling section per listed server name and keep `zone` in that named section rather than inside a `servers` list item;
- canonical per-server paths and ports, including the Observer storage-path invariant and intended data/redo mount separation;
- version/release constraints and the separately locked artifact hashes;
- resource values and units;
- the database bootstrap-password field absent unless the user explicitly supplied an override, and every displayed credential value redacted;
- no unrequested component stanza, tenant creation, auto-start, telemetry change, or cleanup behavior.

A syntactically valid YAML is not enough. For an executable plan, use the installed OBD/plugin parsing and precheck path; do not install or start a component merely to discover whether a key exists. In static-review mode, do not invoke OBD parsing, plugin precheck, or any workflow: report schema/runtime validation as not performed and keep every unsupported conclusion conditional.

Before Observer bootstrap, compare the intended and effective server-to-zone map. When using the separated configuration-file path, inspect the registered/effective configuration after `deploy` and before `start`; require every intended distinct zone to remain distinct. A parser success that silently discarded placement is a failed pre-bootstrap gate, not permission to start and repair through destroy/rebuild.

Keep `enable_auto_start` or an equivalent plugin option false or unset unless persistent startup was explicitly requested. If proposed, read the [automatic-startup and systemd gate](lifecycle.md#automatic-startup-and-systemd) before rendering or executing the configuration.

<a id="storage-initialization-invariants"></a>

### Preserve the Initialized Storage Topology

Treat `home_path`, `data_dir`, and `redo_dir` as initialization-time storage topology, not ordinary retry knobs. Before deployment, retain their canonical parent paths, mount identities, expected ownership, and empty-state evidence. After the deploy stage initializes the component and before a separate start, compare the registered configuration and deploy trace with the actual version-matched layout. When `data_dir` is omitted and defaults to `<home_path>/store`, verify that canonical data root directly. When an explicit `data_dir` differs, verify that `<home_path>/store` resolves to it rather than remaining a conflicting real parent directory. Verify the data path's `sstable` location, and when the installed plugin maps redo separately, verify that the canonical data-side `clog` path resolves to the plugin-derived redo-side `clog` path; verify `slog` according to that same version-matched initializer. Record every link target, owner, mode, mount identity, and content boundary.

Do not invoke `start` until this graph matches the registered deploy-time values. A start command containing `-d <home_path>/store` is expected canonical behavior and does not establish that `redo_dir` is unsupported. If the graph is missing, cyclic, or contradictory, classify deployment initialization as incomplete or the manifest as path-conflicting; preserve evidence and enter failure recovery without one unchanged start attempt.

Changing or deleting a registered storage-path value after deploy does not prove that OBD will rerun initialization or migrate the existing layout during start. Do not remove custom `data_dir` or `redo_dir`, replace initialized symlinks, delete an empty-looking `store`, or manually create `store/{clog,slog,sstable}` as a generic way around a start error. If the storage topology differs from the deploy-time configuration, preserve both states and use the [failed-initial-start recovery](../../references/failure-recovery-and-evidence.md#failed-initial-start-and-storage-topology) before another command.

## Execute

Use the syntax confirmed by the installed command help:

```bash
obd cluster deploy <deploy_name> --config=<reviewed_config.yaml>
obd cluster start <deploy_name> --strict-check
```

When this workflow is entered from an intentionally created `configured` registration, use the stored configuration only after revalidating its parsed semantics and checksum against the approved candidate. If the installed help supports deployment from a registered configuration, use `obd cluster deploy <deploy_name>` without `--config`; do not replace or silently accept different stored content. Keep `start` separate and invoke it only after deployment acceptance.

Use `--strict-check` only when the installed `cluster start --help` exposes it; OBD V4.6.0 documents it on start, not deploy. Preserve the configuration checksum and trace ID for each command. After `deploy`, establish what was registered, copied, installed, or initialized and verify the [initialized storage topology](#storage-initialization-invariants) before deciding whether `start` is safe. Do not blindly issue `start` after a partial deploy.

<a id="interactive-deploy"></a>

### Interactive Deployment

Interactive deployment is a human-operated terminal wizard. The Agent must not launch, drive, script, or answer this wizard on the user's behalf. When the user asks about this deployment mode, confirm the installed build exposes the option and tell the user to run it in their own interactive terminal:

```bash
obd cluster deploy <deploy_name> --interactive
```

Explain that the wizard collects configuration and can continue through deployment, startup, host initialization, credential choices, and optional tenant creation; it is not merely a configuration generator. Before handing off the command, tell the user to choose a unique deployment name, check that the proposed paths and ports do not collide with existing deployments, and review every prompt before accepting it. The Agent may inspect and explain the resulting registered/runtime state afterward only when the user asks, but must not replace the user's interaction with a PTY driver, piped answers, automatic confirmation, browser automation, or inferred choices.

The maximum-utilization workflow uses `autodeploy` as an integrated configuration-generation, deployment, and startup path. Use it only through [maximum-utilization.md](maximum-utilization.md), after completing bounded host-environment remediation and checking name/path/port collisions, complete package closure, generated defaults, and all three transitions.

### Autodeploy

Treat `autodeploy` as an integrated mutating workflow, not a YAML generator. Inspected implementations always run configuration generation, deployment, and startup in sequence. Use it only when all three transitions and their exact targets are authorized, after checking name/path/port collisions and all generated defaults. If the user wants only a draft or review, produce a non-executable blueprint or use the static-review boundary instead.

`autodeploy` is the OBD maximum-specification deployment path. When a new distributed cluster defaults to maximum utilization because the user supplied no resource values, cap, or non-maximum profile, select `autodeploy` without requiring the user to name the command. Official V4.6.0 documentation says it generates maximum-specification values from target resources, can overwrite modified configuration values, and then deploys and starts. Use the installed consistent-generation option for a multi-node cluster, validate every non-generated input before launch, and verify the generated configuration and topology afterward; do not replace this default with separate `deploy` and `start` merely to insert an inspection point.

Keep optional destructive/convenience branches absent unless their exact installed behavior is separately requested and authorized. In the inspected command:

- `--force` permits overwriting `home_path`, while `--clean` cleans a `home_path` judged to belong to the invoking user; either branch also suppresses the normal cluster-status check;
- `--auto-create-tenant` creates a tenant named `test` using all resources the workflow considers available; use it only after the user explicitly requests tenant creation, apply the tenant default workflow without asking for omitted settings, and require data-plane acceptance;
- `--force-delete` deletes the registered cluster and is a separate destructive operation, not a name-collision convenience.

Display the canonical paths, existing registration, processes/listeners, tenant/resource outcome, and the equivalent health evidence that would replace any suppressed status check. Do not add any of these options to make the workflow unattended or to repair a partial deployment.

If `autodeploy` returns non-zero, times out, or disconnects, do not submit it again. Reconcile the same deployment name, trace, registered configuration checksum, selected artifacts, processes/listeners, paths, and data plane, then continue only from the proved state:

| Reached state | Narrow next action |
|---|---|
| Running and healthy with the intended effective configuration | Accept and verify; do not rerun. |
| Fully deployed, not running, exact artifacts/configuration/paths intact, no mixed process state | Run the ordinary reviewed `cluster start` path after all start and topology gates; do not rerun `autodeploy`. |
| Configured only, with no target installation/runtime mutation and the generated configuration fully reviewed | Use the ordinary reviewed `cluster deploy` and then separated `start` path when the installed build supports that registered configuration. |
| Partially deployed, mixed/unknown runtime, contradictory registration, or unverified generated configuration | Stop under the shared failure-recovery workflow. Do not force, clean, destroy, redeploy, delete paths, or guess the completed stage. |

### Maximum-Utilization Default

Use the maximum-utilization workflow when the user explicitly requests it or when a new-cluster request omits resource sizing. Its ordinary distributed execution path is `autodeploy`; an explicit user resource plan or non-maximum profile overrides this default. If the request names `obd perf`, route that exact single-node shortcut through [lifecycle.md](lifecycle.md#quick-deploy-shortcuts); do not replace it with `autodeploy`. For dedicated-host or capped multi-node maximum sizing, read and follow [maximum-utilization.md](maximum-utilization.md). It preserves deterministic per-node candidate calculation, per-key minima across all nodes, 8-core behavior, disk commitment checks, common resource verification, and post-deployment equality checks. “Use all resources” never means zero safety reserve or permission to initialize the host automatically.

## Accept or Recover

Verify the registered component manifest and actual installed artifact identity, every selected process/listener/path, OceanBase topology and server state through SQL, authenticated SQL readiness using the protected OBD-generated or user-supplied credential, and relevant optional-component data planes. Confirm that unselected services were not added and no unexplained partial registration or path remains.

On failure, preserve the trace, registered configuration, generated files, remote processes, listeners, paths, and artifact state. Classify the stage before continuing. Do not delete the registered deployment, remove directories, redeploy, or retry until the shared failure-recovery rules identify the safe next action.
