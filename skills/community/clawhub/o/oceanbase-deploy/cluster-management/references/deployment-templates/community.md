# Community Distributed Deployment Blueprint

Use this blueprint only after the installed OBD build proves the community distributed component, commonly `oceanbase-ce`, and its exact plugin/schema. It is a rendering contract, not copy-paste production YAML.

The distributed server/global structure and ordinary OBD workflows are shared with commercial distributed `oceanbase` unless installed evidence proves a difference. This page locks the community artifact identity and gives the concrete `oceanbase-ce` rendering; it is not evidence that a generic distributed OBD function is community-only.

## Required Inputs

- approved OceanBase Community Edition version, release, architecture, artifact hash, repository source, and plugin identity;
- one-node development or multi-node availability topology, target hosts, and any explicit zone/failure-domain mapping; when no mapping is supplied for multiple Observer hosts, assign each distinct host to a distinct new zone in deterministic host order without asking;
- target host identities, SSH account, canonical paths, and ports, plus any explicitly supplied resource values or caps; when paths are omitted, derive each host's base through the [largest writable persistent filesystem rule](../config-deployment.md#default-deployment-base-directory), and when sizing is omitted, derive the resource budget through the default maximum-utilization workflow;
- any user-specified initial cluster/administrator password override and any explicitly requested tenant behavior; do not request an override when none was supplied because OBD owns random generation by default;
- keep persistent auto-start false or unset unless the user requested it; do not ask for an auto-start choice merely because the schema exposes one;
- optional OBProxy/OBAgent/monitoring components, each separately justified.

## Version Gate

Inspect the selected community plugin's parameter definition and examples. Confirm:

1. the component key and supported configuration style;
2. server/global field placement and override precedence;
3. required identity, path, port, zone, resource, and bootstrap parameters;
4. which values the plugin generates and which must be supplied;
5. whether the selected package supports the target OS/runtime and intended topology.

Do not mix artifact identities from `oceanbase` or another release into this `oceanbase-ce` manifest. The shared `oceanbase`/`oceanbase-ce` distributed structure may be reused when the installed schema agrees, while package names and proved edition-specific features remain separate.

The V4.6.0 guide shows both `el7` and `el8` OceanBase packages for x86 and ARM. Apply the shared package policy without changing component/version/release/architecture: prefer the suffix matching the target OS major version, then EL8 when that artifact is absent, then EL7 when both earlier candidates are absent. Inspect the exact RPM requirements and target runtime, including loader, GLIBC, and required libraries, before using either fallback; suffix order alone does not prove compatibility.

## Start from the Released Example

For OBD V4.6.0, resolve the version-matched installed example root rather than reconstructing the schema from memory:

- direct/RPM installation: `/usr/obd/example/`;
- All-in-One installation: `~/.oceanbase-all-in-one/obd/usr/obd/example/` under that installation's resolved root.

Select the complete example that matches the requested topology:

- `mini-single-example.yaml` for a low-resource single Observer;
- `mini-distributed-example.yaml` for a low-resource multi-Observer layout, or `distributed-example.yaml` for the ordinary distributed baseline;
- `distributed-with-obproxy-example.yaml` when community OBProxy is explicitly required;
- `obagent/distributed-with-obproxy-and-obagent-example.yaml` when both OBProxy and OBAgent are explicitly required;
- `all-components-min.yaml` only for an explicitly requested disposable multi-component demonstration after removing no required dependency and rejecting every unrequested component.

Copy the complete selected example to a new reviewed work path, record its checksum and source OBD build, retain every component-specific field until the installed schema/dependency review proves whether it is required, then change only values justified by the deployment manifest. Mini and `all-components-min` examples are low-resource/development baselines with non-production choices; they are not production sizing recommendations. Do not use an example shipped by a different OBD installation or product form.

## V4.6.0 Concrete-Key Baseline

The released V4.6.0 community distributed examples use the following real key structure. Values marked `CHANGE_ME` must be replaced, resource sizes must be recalculated, and every key must still be checked against the installed `oceanbase-ce` plugin before execution.

Before replacing the path placeholders, apply the [Observer storage-path invariant](../config-deployment.md#observer-storage-path-invariant). For explicit custom paths, use disjoint home/data/redo siblings and never place `data_dir` or `redo_dir` below `<home_path>/store`; that path is reserved as OBD's canonical data entry. A direct-root equality is valid only in the installed plugin's supported data/single-root layout. Keep a separately selected redo filesystem separate when the installed schema accepts `redo_dir`.

```yaml
# Configure this block only for remote login.
user:
  username: CHANGE_ME_SSH_USER
  key_file: CHANGE_ME_PRIVATE_KEY_PATH
  port: 22

oceanbase-ce:
  version: CHANGE_ME_VERSION
  package_hash: CHANGE_ME_EXACT_PACKAGE_HASH
  servers:
    - name: server1
      ip: CHANGE_ME_SERVER1_MANAGEMENT_IP
    - name: server2
      ip: CHANGE_ME_SERVER2_MANAGEMENT_IP
    - name: server3
      ip: CHANGE_ME_SERVER3_MANAGEMENT_IP
  global:
    cluster_id: CHANGE_ME_UNIQUE_CLUSTER_ID
    appname: CHANGE_ME_CLUSTER_NAME
    memory_limit: CHANGE_ME_MEMORY_LIMIT
    system_memory: CHANGE_ME_SYSTEM_MEMORY
    datafile_size: CHANGE_ME_INITIAL_DATAFILE_SIZE
    datafile_next: CHANGE_ME_DATAFILE_GROWTH_STEP
    datafile_maxsize: CHANGE_ME_DATAFILE_MAX_SIZE
    log_disk_size: CHANGE_ME_LOG_DISK_SIZE
    cpu_count: CHANGE_ME_CPU_COUNT
    production_mode: CHANGE_ME_BOOLEAN
    enable_syslog_wf: false
    max_syslog_file_count: CHANGE_ME_RETENTION_COUNT
    # Omit root_password by default so the proved OBD workflow generates it.
    # Add the schema-confirmed key only for an explicitly supplied protected override.
  server1:
    mysql_port: CHANGE_ME_SQL_PORT
    rpc_port: CHANGE_ME_RPC_PORT
    obshell_port: CHANGE_ME_OBSHELL_PORT
    # Use disjoint paths; never put data_dir or redo_dir under home_path/store.
    home_path: CHANGE_ME_CANONICAL_HOME_PATH
    data_dir: CHANGE_ME_CANONICAL_DATA_PATH
    redo_dir: CHANGE_ME_CANONICAL_REDO_PATH
    zone: zone1
  server2:
    mysql_port: CHANGE_ME_SQL_PORT
    rpc_port: CHANGE_ME_RPC_PORT
    obshell_port: CHANGE_ME_OBSHELL_PORT
    home_path: CHANGE_ME_CANONICAL_HOME_PATH
    data_dir: CHANGE_ME_CANONICAL_DATA_PATH
    redo_dir: CHANGE_ME_CANONICAL_REDO_PATH
    zone: zone2
  server3:
    mysql_port: CHANGE_ME_SQL_PORT
    rpc_port: CHANGE_ME_RPC_PORT
    obshell_port: CHANGE_ME_OBSHELL_PORT
    home_path: CHANGE_ME_CANONICAL_HOME_PATH
    data_dir: CHANGE_ME_CANONICAL_DATA_PATH
    redo_dir: CHANGE_ME_CANONICAL_REDO_PATH
    zone: zone3
```

`package_hash` is documented for exact package selection in V4.6.0 examples/FAQ; use it only when the installed plugin schema accepts it. Confirm `obshell_port` support for the selected OceanBase version. On a multi-homed host, resolve the installed `local_ip`/`devname` rules instead of relying on automatic selection. If a key is unsupported, return to the installed example/schema; do not rename it by analogy.

In this named-server structure, do not move `zone` into a `servers` list item. Require one sibling `serverN` section per listed name and verify the effective server-to-zone map before bootstrap; affected builds can parse an unknown list-item field while silently falling back every Observer to `zone1`.

The V4.6.0 community schema documents `2881` as the default SQL port, `2882` as the default RPC port, and `2886` as the default obshell operation port. Preserve those familiar defaults when they fit the reviewed topology, but still treat them as explicit per-host manifest values and prove they are free. The guide warns not to change SQL or RPC ports after the cluster has started; route an existing identity change through the version-supported network/lifecycle workflow instead of editing the YAML in place.

Keep the artifact hash in the execution manifest even when the selected schema cannot express `package_hash`. Before execution, prove repository resolution selects that exact hash without refreshing to an unreviewed candidate set.

## Topology Variants

- A one-node topology is suitable only when the user accepts its failure-domain and availability limits.
- For a multi-node topology, preserve an explicit zone/failure-domain mapping. Otherwise assign each distinct Observer host to its own new zone in deterministic host order without asking. Keep per-host paths/ports distinct; do not clone one server's network identity into all entries or claim physical high availability from logical zone names alone.
- Add community OBProxy only when the client routing design requires it. Direct SQL access is valid when it satisfies the request.
- Add OBAgent or the monitoring chain only through the monitoring workflow; they are not database prerequisites.

Accept the deployment only after artifact, process, listener, SQL identity, server topology, and unrequested-component checks pass.
