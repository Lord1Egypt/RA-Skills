# OCP Deployment, Takeover, and Redeploy Integration

Treat OCP Community Edition, commercial OCP, and obshell dashboard as different products. Resolve the requested product before selecting a package or component key.

## Product Selection

- In an explicitly community context, an unqualified new OCP request normally means OCP Community Edition; confirm the installed component key, commonly `ocp-server-ce`, then read the [OCP CE V4.6.0 baseline and topology gate](ocp-ce.md).
- In a commercial context, resolve the commercial OCP artifact and component, commonly `ocp-server`; do not substitute CE.
- If context is ambiguous or the user has an existing product, identify it from deployment/plugin/artifact evidence instead of silently migrating it.
- obshell dashboard can be offered for a lightweight UI when it meets the goal, but only as an explicit product choice.

Do not use the obsolete, unverified key `ocp-ce` merely because an old example contains it.

## Artifact and Topology Gate

Record exact OBD/OCP/plugin identities and resolve one compatible artifact set including required runtime dependencies. Verify provenance, version/release/architecture/hash, repository source, Java/runtime requirements, OS, target resources, ports, paths, time synchronization, privileges, and network access.

Classify MetaDB before rendering configuration:

- **Managed internal MetaDB:** OCP depends on an OceanBase component in the same deployment and the effective OCP configuration does not select an external JDBC endpoint.
- **External MetaDB:** OCP uses a separately managed MetaDB endpoint or has no dependency on the local OceanBase component.

Confirm this from the installed OCP/OceanBase plugins and rendered effective configuration. Component names alone are insufficient. For internal MetaDB, calculate tenant CPU/memory/log capacity and define backup/recovery of OCP metadata. For external MetaDB, verify database identity, schema, account privilege, TLS/network, backup ownership, and lifecycle independence.

## Choose Automatic or Manual Takeover

For a managed internal MetaDB in the same deployment, select the takeover path from the exact installed workflow, not from the OBD major/minor version alone. A version string, development source commit, or newer-looking example does not prove that a released package both triggers takeover after start and reads every required value from the intended configuration scope.

Before execution, independently establish these capabilities from the selected installed package and plugin:

1. whether the owning `start` or redeploy/start workflow schedules OCP takeover after all components become healthy;
2. how that workflow obtains the effective Observer SQL port, including whether it can read a server-scoped value or requires the component `global` value;
3. how to identify and wait for the exact takeover task and reconcile its terminal result.

If automatic takeover is proved, use `deploy -> start -> verify takeover` as the main path. Do not append `check4ocp` or `export-to-ocp` merely because those commands exist. If automatic takeover is absent or cannot be proved for the installed build, establish component health and use the manual `check4ocp -> export-to-ocp -> verify takeover` path below. Treat SQL-port scope as a separate capability: when server-scope support is not proved before the first deployment, place the same effective `mysql_port` in the component `global` section and keep any server value identical.

Exporting an existing OBD cluster to an independently deployed or external OCP remains a manual takeover workflow regardless of the OBD version.

## Schema-Gated Configuration

For OCP Community Edition, use [ocp-ce.md](ocp-ce.md), which contains the official V4.6.0 real-key baselines for external and same-deployment MetaDB topologies. The generic structure below is only a decision scaffold for a commercial or otherwise version-different plugin whose formal schema is available; it is not a substitute for the CE reference.

Do not use placeholder comments as a deployment plan. Render the exact version's schema from these required decisions:

```yaml
<verified-ocp-component-key>:
  version: <locked_version_if_supported_here>
  release: <locked_release_if_supported_here>
  servers:
    - ip: <approved_ocp_server>
  global:
    <verified-home-and-data-keys>: <canonical_paths>
    <verified-listener-keys>: <approved_addresses_and_ports>
    <verified-java-or-runtime-keys>: <approved_runtime>
    <verified-admin-credential-key>: <protected_secret_reference>
    <verified-internal-metadb-or-jdbc-keys>: <approved_topology_values>
    <verified-resource-and-log-keys>: <approved_values>
```

This is non-executable until every bracketed key is replaced from the installed schema and repository resolution is pinned to reviewed hashes. Include no OceanBase cluster or tenant creation unless that internal-MetaDB topology was explicitly accepted.

Use the version-supported config deployment or incremental component-add workflow. Never redeploy an existing OceanBase cluster merely to add OCP.

## Credential Boundary

Prefer version-supported protected input. If a public OBD command only accepts an OCP password in argv, disclose process-list/history exposure and require an approved secure local procedure. Do not put a literal password in reusable examples, invent an environment variable, or “repair” exposure by deleting shell history or unrelated logs.

Resolve takeover host type and SSH credential identity before export. Inspected `export-to-ocp` workflows create a host type and credential when no matching values are supplied; they can upload an SSH password or read and upload the controller's SSH private key, falling back to the controller account's default private-key path. Prefer a reviewed existing OCP credential and a version-proved option that prevents secret upload and asset creation. If the installed workflow cannot prevent them, stop unless the exact secret egress, destination, new OCP assets, and rollback are separately authorized. Never run it merely to discover the default.

<a id="export-an-obd-cluster-to-ocp"></a>

## Manual Export of an OBD Cluster to OCP

Use this workflow for an existing OBD cluster that must be taken over by an independently deployed or external OCP, or for a same-deployment internal-MetaDB topology whose installed start workflow does not prove automatic takeover. OBD cluster takeover and OCP takeover are different. For OCP export:

1. verify source cluster identity/health, OCP product/version/health, account privilege, address format, network/TLS, existing OCP records/tasks, and compatibility;
2. read installed `check4ocp` and `export-to-ocp` help and inspect their workflows before execution;
3. classify `check4ocp` as a mutation when the selected version installs utilities on source servers. Inspected code resolves and installs `oceanbase-ce-utils` after the checks, and an installation failure may be only a warning. Before running it, lock the utility artifact/hash, servers, destination paths, privileges, and cleanup boundary and obtain host/package-mutation authorization; do not use it as a read-only probe. Utilities installed below the deployment `home_path`, commonly under its `bin` tree, can disappear when that deployment is destroyed, so re-prove or reinstall them before a later check/export instead of relying on an earlier successful run;
4. show the exact source cluster, destination OCP, utility installation, credential/SSH-secret exposure, OCP host-type and credential creation, duplicate/retry semantics, and recovery boundary before authorization;
5. execute the public export command with protected credentials where supported;
6. poll any task to a successful terminal state and verify utility installation separately from the OCP check, then verify exactly one correct managed-cluster record, the intended host type/credential reuse or creation, and an authenticated OCP management operation.

After the gates above, preserve the established public command path using the long options exposed by the installed build. OBD V4.6.0 commonly uses these shapes:

```bash
obd cluster check4ocp <deploy_name> --version=<ocp_version> [--components=<reviewed_components>]
obd cluster export-to-ocp <deploy_name> \
  --address=<reviewed_ocp_url> \
  --user=<reviewed_ocp_user> \
  --password=<redacted_private_terminal_input> \
  [--host_type=<reviewed_existing_or_new_type>] \
  [--credential_name=<reviewed_existing_credential>]
```

The V4.6.0 export interface places the OCP password in process arguments. The second block is therefore a redacted command shape, not a command for the agent to execute or paste with a real secret. If the installed build has no protected input path, require the approved private-terminal procedure described above.

An accepted request or successful OBD exit is not takeover completion. A timeout, interruption, or duplicate-object response such as `to be taken over already exists` is also not sufficient to classify the original request as failed or successful. Apply the shared [asynchronous-task reconciliation](../../references/failure-recovery-and-evidence.md#reconcile-caller-timeouts-and-asynchronous-tasks): correlate the original task and target, then verify the unique OCP cluster record, task terminal state, and runtime identity before deciding whether any retry is needed. Never delete an OCP record merely to manufacture a retryable state.

## OCP-Aware Redeploy

When a deployment contains OceanBase and OCP, follow the normal destructive redeploy gate and re-resolve the effective MetaDB topology.

For managed internal MetaDB, explain that redeploy can destroy the MetaDB and that the rebuilt OceanBase must be taken over by the rebuilt OCP. Apply the same installed-capability gate above: a proved automatic-takeover workflow must complete takeover in the owning redeploy/start path; otherwise use the reviewed manual takeover after the rebuilt services are healthy. Afterward require OceanBase SQL health, OCP authenticated API/UI and MetaDB health, exactly one management record, terminal takeover task, and usable management function.

For external MetaDB, preserve the external ownership and existing relationship. Do not automatically export the local cluster merely because both components are present.

If healthy services remain without the required internal takeover, preserve trace/task/error evidence and use public `check4ocp`/`export-to-ocp` only when version-specific preconditions and retry identity are clear and the credential-bearing recovery is separately authorized. Do not redeploy again as takeover repair.

## Acceptance and Failure

Verify artifact identity, process/listener/path ownership, authenticated OCP API/UI, MetaDB connectivity, administrator login, terminal background tasks, and the requested management function. Report OceanBase and OCP health separately.

On failure preserve OBD trace, OCP task/report, rendered configuration, MetaDB identity, processes/listeners, logs, and current OCP records. Do not switch OCP products, change MetaDB topology, recreate tenants, clear metadata, or redeploy without a new reviewed plan.
