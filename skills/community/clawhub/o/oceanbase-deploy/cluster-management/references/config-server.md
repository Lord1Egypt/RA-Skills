# OceanBase Config Server

Use this workflow for the OBD component commonly named `ob-configserver`. It supplies registered OceanBase cluster metadata to supported consumers; component process health, metadata registration, and consumer retrieval are separate outcomes.

## Capability and Scope Gate

1. Verify the exact component key, installed plugin/schema/workflow, package version/release/architecture/hash, and repository source.
2. Establish version compatibility with the selected community or commercial OceanBase product, OBProxy/ODP, and the exact metadata protocol expected by each consumer.
3. Record deployment, Config Server nodes, listen and advertised addresses, ports, canonical home/log/storage paths, resources, TLS/authentication or network-access boundary, and every intended consumer.
4. Check host identity, path/port conflicts, disk/resources, network reachability, metadata-store ownership, and exposure boundary.
5. Decide whether this is a combined new deployment, incremental component add, Config-Server-only deployment, restart/reload, address replacement, or deletion. Use only the installed supported workflow.

Do not add Config Server solely because it appears in a bundle or an unrelated product error; first prove that the requested consumer and version require it.

## V4.6.0 Structural Baseline

Derive every executable value and key from the installed `ob-configserver` schema. The released V4.6.0 example and plugin establish this real-key structural baseline:

```yaml
ob-configserver:
  servers:
    - CHANGE_ME_CONFIG_SERVER_IP
  global:
    listen_port: 8080
    server_ip: CHANGE_ME_REVIEWED_BIND_ADDRESS
    home_path: CHANGE_ME_CONFIG_SERVER_HOME
    log_level: info
    log_maxsize: 30
    log_maxage: 7
    log_maxbackups: 10
    log_localtime: true
    log_compress: true
    storage:
      database_type: sqlite3
      # connection_url: CHANGE_ME_ABSOLUTE_SQLITE_URI
```

This fragment is not deployable until every placeholder, host, path, exposure decision, and installed-schema default is reviewed. In the V4.6.0 schema, `storage.database_type` supports `sqlite3` or `mysql`. A SQLite URL can be omitted to use the version's derived database under `home_path`; a MySQL or OceanBase MetaDB URL can contain a username and password, so construct it only in a protected local procedure and never place the literal URI in reusable YAML, chat, or reports. Verify the MetaDB database and least-privilege DDL/DML account separately.

## Select One V4.6.0 Topology Branch

### Combined OceanBase, ODP, and Config Server

The official V4.6.0 community example uses these dependency edges:

```yaml
oceanbase-ce:
  depends:
    - ob-configserver
  global:
    appname: CHANGE_ME_NONEMPTY_CLUSTER_NAME

obproxy-ce:
  depends:
    - oceanbase-ce
    - ob-configserver
```

Use the exact database and proxy component keys exposed for the selected community or commercial product; do not rename the community example speculatively. A non-empty database `appname` is required for registration in this branch. Omit `rs_list` when the reviewed intent is for ODP to start through the Config Server URL; verify the installed proxy schema derives that URL and preserves the required database/proxy authentication relationship.

### Add Config Server to an Existing OBD Deployment

Use a config file containing only the reviewed Config Server stanza and the installed long option:

```bash
obd cluster component add <deploy_name> --config=<config_server.yaml>
```

Do not redeploy merely to add Config Server. In the V4.6.0 documented flow, a deployment with ODP can prompt to restart `obproxy-ce,oceanbase-ce` so ODP changes from root-server-list mode to the Config Server URL; declining leaves the prior ODP mode in place. Resolve the exact installed restart set, outage, and consumer transition, then authorize it separately.

Do not add `--confirm` as a generic non-interactive flag. In inspected implementations it can accept restart-causing behavior rather than mean “do not restart”; without a proved selector, an empty restart selection can widen to the whole deployment. Stop when the exact transition cannot be controlled.

### Deploy Config Server Alone

Deploy and start the reviewed `ob-configserver` configuration as its own OBD deployment. It does not register an existing database merely by becoming healthy. Register only an already running, identified OceanBase cluster through the version-supported `obconfig_url`/SQL workflow, then configure each intended ODP with the reviewed `obproxy_config_server_url`. Treat the database reload/restart and ODP route change as separate availability/configuration operations. Preserve the previous endpoint or `rs_list` route until rollback is proved.

## Acceptance

After deployment or change, verify:

1. exact OBD registration, artifact, process, listener, bind/advertised address, path ownership, and metadata-store identity;
2. a bounded request for the supported `GetObProxyConfig` action returns the expected registered cluster identity, with approved TLS/authentication when supported and network access restricted when it is not;
3. the intended database is registered under the exact non-empty application/cluster identity and stale or unrequested clusters are absent;
4. every intended ODP retrieves the current metadata and its authenticated SQL data plane reaches the intended cluster;
5. direct database access and unrelated consumers remain healthy.

Initialization or registration may be asynchronous. Poll a documented bounded status with a deadline and preserve intermediate errors; do not use an unexplained fixed sleep or infer readiness from an open port.

## Version-Gated Removal

Before address replacement or removal, list every configuration, runtime, database, ODP, and external reference; migrate consumers first and preserve the prior endpoint/configuration as rollback. The official V4.6.0 Web component guide states that uninstalling Config Server is not supported there. Do not infer that the generic CLI component-delete path provides a complete lifecycle.

Config Server addition can insert reverse dependency references such as `oceanbase-ce.depends: [ob-configserver]`, and other database or proxy components can also depend on it. Use this guarded sequence for an installed version that exposes component deletion:

1. Capture the complete dependency graph, both OBD configuration files, Config Server process/listener/path state, registered clusters, and every ODP or external consumer.
2. Migrate consumers away from the endpoint and verify their replacement route and authenticated data plane.
3. Use the reviewed [configuration-change workflow](configuration-changes.md) to remove every `ob-configserver` dependency reference, not only the first database reference. Validate the edited graph before applying it.
4. If the installed version requires reload or restart for that dependency/route change, display and authorize the exact affected set, apply it, and verify consumers again before deletion.
5. Inspect the installed Config Server plugin/workflow inventory for `delete_component_pre` and `delete_component`. For ordinary removal, stop if the workflow needed to stop and clean the component is absent. An explicitly authorized compatibility test may continue only after displaying the expected partial-state risk and recovery boundary.
6. Run the version-proved `component del` command only after all remaining reverse dependencies are gone. Correlate its Trace with the workflow inventory, then independently verify `config.yaml`, `inner_config.yaml`, OBD registration, process/PID, listener, and canonical work/data paths.

In the reviewed 4.7 development checkout, `ob-configserver` exposes add/start/stop/restart workflows but no `delete_component` workflow, while the generic deletion path can ignore that missing stage and still remove the component from registered configuration. Treat this as version-specific implementation evidence. If registration disappears while the process or listener remains, report `FAIL — lifecycle gap`; do not report a complete removal or kill/delete the residual runtime without a separately authorized recovery action. Apply [cleanup and ownership boundaries](../../references/cleanup-boundaries.md) to every supported removal.

On failure preserve trace, plugin/configuration, component logs, actual endpoint, metadata response, registration state, and consumer errors. Do not remove the component, edit consumer files ad hoc, or redeploy until the failed layer is identified.
