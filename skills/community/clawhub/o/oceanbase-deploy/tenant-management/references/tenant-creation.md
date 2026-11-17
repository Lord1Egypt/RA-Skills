# Tenant Creation

Use this workflow to plan, create, or inspect an OceanBase tenant. Read the installed `obd cluster tenant create --help` and `show --help` before constructing a command; option names, defaults, supported modes, and resource semantics vary by OBD and component version.

## Use OBD Defaults for Unspecified Settings

Creating a tenant requires an explicit user request. That request does not need to enumerate ordinary tenant settings. Separate the request into:

- **explicit overrides:** values the user actually supplied;
- **unspecified settings:** options to omit so the installed OBD workflow applies its own defaults.

Do not ask the user to choose an unspecified tenant name, mode, zone list, locality, replica policy, primary zone, Unit count, CPU, memory, log disk, IOPS, time zone, charset/collation, tablegroup, workload optimization, variables, network allowlist, or password. Do not replace omission with agent-generated values. Explicit overrides take precedence only for the named settings.

The reviewed OBD 4.7-era minimal-create baseline behaves as follows. Confirm the active installed build before execution and report any material difference; do not hard-code the table into options when omission produces the same result.

| Setting | OBD default baseline when omitted |
|---|---|
| Tenant name | `test` |
| Compatibility mode | `mysql` |
| Zone list | All active zones |
| Primary zone | `RANDOM` |
| Replica count | Number of selected zones |
| Log-only replicas | `0` |
| Units per zone | Minimum active Observer count across active zones in the reviewed implementation; with the default zone list this covers the same complete zone set |
| Maximum CPU | Minimum currently tenant-allocatable CPU across the selected servers |
| Minimum CPU | Same as the default maximum CPU |
| Memory size | Minimum currently tenant-allocatable memory across the selected servers |
| Log-disk size | Minimum currently tenant-allocatable log disk across the selected servers |
| IOPS, charset/collation, time zone, optimization, and other omitted options | Installed OBD/database defaults |
| `ob_tcp_invited_nodes` | `%` |
| Tenant password | Empty password |

Record the exact deployment, OceanBase product form and component, cluster identity, explicit overrides, installed-default evidence, and the expected effective plan. Check database-side capacity in every defaulted or explicitly selected zone, including:

- available CPU and memory;
- log-disk capacity and required headroom;
- Unit and resource-pool occupancy;
- eligible OBServer nodes and zone placement;
- existing tenant, Unit, resource-pool, or account objects with the effective names.

The default resource path can consume all resources OBD currently considers tenant-allocatable. Show that expected effect in the creation plan, but do not ask the user to choose another size merely because no resource override was supplied. Stop when the effective locality cannot be satisfied, a selected zone lacks the resources required by OBD's computed default, or the effective tenant identity conflicts with an existing or partial earlier attempt. Do not silently choose a different name, topology, or smaller resource plan.

## Apply the Allowlist Default Without a Prompt

When the user supplies an allowlist, pass that final value in the initial tenant-create request through the installed command's supported variables syntax. Prove that the installed create workflow carries it into initial tenant creation; never create with a temporary `%` and tighten it afterward.

When the user omits the allowlist, do not ask for client addresses or synthesize CIDRs. Omit the allowlist variable and use the installed OBD default. In the reviewed OBD baseline that final default is `%`; state that expected exposure in the redacted plan and verify the effective value after creation. It is the intended final default, not a temporary broad value requiring post-create correction.

If a user-supplied allowlist cannot be applied atomically by the installed workflow, stop. Do not discard the override and fall back to `%`.

## Apply the Password Default Without a Prompt

When the user omits the tenant password, omit the credential option. The reviewed OBD baseline creates the tenant with an empty password; preserve that as the final requested default. Do not ask for a password, generate one in the agent, describe it as OBD-random, or set a password immediately after creation. State the empty-password result accurately in the redacted plan and final report without fabricating a secret.

When the user explicitly supplies a password, determine how the installed build accepts it. Prefer a protected interactive input, permission-controlled file, or supported secret reference. If the only supported path is a command argument such as `--password`, disclose process-list and shell-history exposure and use an approved local execution procedure; never print the value. Do not invent stdin, file-descriptor, environment-variable, or file options that the installed interface does not support.

Verify authentication with the expected credential state after creation: an empty password when omitted, or the explicit protected value when supplied. Tenant existence with a failed expected login is a partial result, not success.

## Construct and Execute

Use only options confirmed by the installed help. The same OBD tenant-create workflow applies to community and commercial distributed OceanBase; do not add an edition gate to tenant creation or its ordinary options. Compatibility mode is a real product-capability distinction: the V4.6.0 guide documents Community Edition as MySQL-only, while a commercial product may expose MySQL and Oracle modes. Preserve the default `mysql` mode when the user omitted it, and validate an explicit mode against the installed product/plugin. For OceanBase 4.0 and later use `--memory-size` rather than the legacy min/max-memory options. The documented minimum log-disk size is 2G, and `--optimize` requires a supporting OceanBase release (documented as 4.2.5 or later in this guide).

Choose one internally consistent placement model from installed help when the user supplied placement overrides; do not combine explicit locality, replica-count, zone-list, and primary-zone values that describe different topologies. With no overrides, preserve the minimal OBD command rather than expanding defaults into guessed flags:

```bash
obd cluster tenant create <deploy_name>
```

Add only user-supplied overrides using option names confirmed by installed help. If the user supplied an allowlist, include the corresponding shell-quoted variables option in the initial request. If the user supplied a password, include the version-supported credential option only through the approved local procedure. Otherwise omit both and retain OBD's `%` and empty-password defaults.

Show the redacted effective plan, distinguishing explicit overrides from OBD defaults, before execution. Existing authorization to create the tenant covers use of unspecified OBD defaults; do not turn each default into another configuration question. Authorization does not cover changing an explicit override or adding a tenant when the user requested only cluster deployment.

Preserve the ordinary read-only inspection command from the installed interface:

```bash
obd cluster tenant show <deploy_name>
```

Use the version-supported tenant selector when the installed help exposes one. This output proves only OBD/database-reported tenant state; apply the database-side and data-plane checks below before declaring the tenant usable.

## Accept the Result

Verify all applicable layers:

1. the OBD task reached a successful terminal state and `tenant show` identifies exactly one intended tenant;
2. database-side tenant status is terminal and healthy rather than creating or deleting;
3. locality, replicas, primary zone, Units, resource pool, and effective resource values match the explicit overrides or resolved installed OBD defaults;
4. the effective `ob_tcp_invited_nodes` value equals the explicit allowlist when supplied, otherwise the installed default (expected `%` in the reviewed baseline);
5. the intended account authenticates using the explicit password when supplied, otherwise an empty password, and can execute a bounded identity query in the effective compatibility mode, following [version-adaptive SQL evidence](../../references/sql-evidence.md);
6. no unexplained partial Unit, pool, user, or tenant object remains.

If the client times out or disconnects, do not classify the create as failed and do not submit it again. Under the same controller identity, correlate the Trace/task, `tenant show`, database tenant/Unit/pool objects, effective allowlist, and authenticated SQL state within a bounded deadline. Accept a server-side success only when the exact tenant passes every required layer; otherwise classify it as failed, still running, or unknown through the shared failure-recovery workflow.

If creation fails after any object appears, freeze retries and inventory the tenant, Units, pools, accounts, variables, trace, and real SQL state. Do not rerun creation or drop the partial tenant as generic cleanup; follow the shared failure-recovery reference.
