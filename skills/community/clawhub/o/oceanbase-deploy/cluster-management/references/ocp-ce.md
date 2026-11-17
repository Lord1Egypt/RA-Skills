<a id="ocp-ce-deployment-and-takeover"></a>

# OCP Community Edition Deployment

Use this reference only after product selection resolves OCP Community Edition. The official OBD V4.6.0 guide documents management of OCP CE 4.2.1 or later and uses the component key `ocp-server-ce`; verify the installed OBD/plugin and repository because another build can differ. Commercial OCP uses a separate artifact/component and follows [the common OCP workflow](ocp.md), not this template.

<a id="terminology"></a>

For the OCP CE/commercial OCP/obshell terminology and selection behavior, read [OCP product selection](ocp.md#product-selection). Do not substitute one product for another.

<a id="ocp-ce-deployment"></a>

## Start from the Released Example

Use the example shipped by the resolved OBD installation:

- external/existing MetaDB: `example/ocp/ocp-only-example.yaml`;
- OceanBase, OBProxy, and OCP in one deployment: `example/ocp/distributed-with-obproxy-and-ocp-example.yaml`.

For an RPM/direct installation, examples are normally under `/usr/obd/example/`; for All-in-One, use that installation's `~/.oceanbase-all-in-one/obd/usr/obd/example/`. Copy one example to a new reviewed path and record its checksum. Do not mix the two topologies or use an example from another OBD installation.

## Choose Exactly One MetaDB Topology

For a MetaDB managed in the same deployment, prove the installed capabilities before choosing the takeover sequence:

| Installed capability | Required path after deployment | OceanBase `mysql_port` compatibility |
|---|---|---|
| The exact installed start workflow proves that it schedules takeover and exposes a reconcilable task | `start`, then verify that exact automatic takeover result | Use server scope only when the installed takeover implementation is also proved to read it |
| Automatic takeover is absent or unproved | Start all services, then run the reviewed `check4ocp` and `export-to-ocp` workflow | Put the effective value in `global` before the first deployment and keep any server values identical |

Do not infer either capability from `OBD >= 4.7.0`; automatic takeover and server-scoped `mysql_port` support were introduced through separate implementation changes and are not provenance-mapped here to every package in a version family. Do not apply this table to an existing cluster being exported to an independently deployed OCP; that remains the manual takeover case.

### Existing or External MetaDB

The official V4.6.0 concrete-key baseline is:

```yaml
user:
  username: CHANGE_ME_SSH_USER
  key_file: CHANGE_ME_PRIVATE_KEY_PATH

ocp-server-ce:
  version: CHANGE_ME_OCP_CE_VERSION
  package_hash: CHANGE_ME_EXACT_OCP_PACKAGE_HASH
  servers:
    - CHANGE_ME_OCP_HOST
  global:
    home_path: CHANGE_ME_OCP_HOME
    soft_dir: CHANGE_ME_OCP_SOFTWARE_DIR
    log_dir: CHANGE_ME_OCP_LOG_DIR
    ocp_site_url: CHANGE_ME_REVIEWED_SITE_URL
    port: CHANGE_ME_OCP_PORT
    admin_password: CHANGE_ME_PROTECTED_LOCAL_VALUE
    memory_size: CHANGE_ME_OCP_MEMORY
    jdbc_url: CHANGE_ME_EXACT_METADB_JDBC_URL
    jdbc_username: CHANGE_ME_METADB_USER
    jdbc_password: CHANGE_ME_PROTECTED_LOCAL_VALUE
    ocp_meta_tenant:
      tenant_name: CHANGE_ME_META_TENANT
      max_cpu: CHANGE_ME_META_CPU
      memory_size: CHANGE_ME_META_MEMORY
    ocp_meta_username: CHANGE_ME_META_USER
    ocp_meta_password: CHANGE_ME_PROTECTED_LOCAL_VALUE
    ocp_meta_db: CHANGE_ME_META_DATABASE
    ocp_monitor_tenant:
      tenant_name: CHANGE_ME_MONITOR_TENANT
      max_cpu: CHANGE_ME_MONITOR_CPU
      memory_size: CHANGE_ME_MONITOR_MEMORY
    ocp_monitor_username: CHANGE_ME_MONITOR_USER
    ocp_monitor_password: CHANGE_ME_PROTECTED_LOCAL_VALUE
    ocp_monitor_db: CHANGE_ME_MONITOR_DATABASE
```

Before rendering, verify whether the selected plugin expects the named tenants/databases/users to exist or uses a privileged JDBC identity to create any of them. The V4.6.0 guide describes pre-creation for standalone OCP but also exposes tenant-definition fields, so do not infer behavior from YAML alone. Enumerate every database object and grant the workflow can create or change; stop if installed plugin evidence does not resolve the branch.

### MetaDB Managed in the Same Deployment

For this branch, the OCP component depends on the exact local components and must not contain `jdbc_url`, `jdbc_username`, or `jdbc_password`; the V4.6.0 guide says those fields conflict with dependency-derived MetaDB configuration.

```yaml
ocp-server-ce:
  version: CHANGE_ME_OCP_CE_VERSION
  package_hash: CHANGE_ME_EXACT_OCP_PACKAGE_HASH
  depends:
    - oceanbase-ce
    - obproxy-ce
  servers:
    - CHANGE_ME_OCP_HOST
  global:
    home_path: CHANGE_ME_OCP_HOME
    soft_dir: CHANGE_ME_OCP_SOFTWARE_DIR
    log_dir: CHANGE_ME_OCP_LOG_DIR
    ocp_site_url: CHANGE_ME_REVIEWED_SITE_URL
    port: CHANGE_ME_OCP_PORT
    admin_password: CHANGE_ME_PROTECTED_LOCAL_VALUE
    memory_size: CHANGE_ME_OCP_MEMORY
```

The associated `oceanbase-ce` stanza owns `ocp_meta_tenant`, `ocp_monitor_tenant`, their account/database settings, and the database resource budget in the V4.6.0 released example. Build those fields from the installed community schema and [community deployment blueprint](deployment-templates/community.md); do not duplicate them under `ocp-server-ce`. Add `obproxy-ce` only when the selected example/plugin requires it and the user accepted that component.

Unless the exact installed takeover workflow is proved to read server-scoped ports, render the same effective SQL port in the OceanBase component's `global` section before deployment:

```yaml
oceanbase-ce:
  global:
    mysql_port: CHANGE_ME_EFFECTIVE_SQL_PORT
```

Keep any per-server value identical. An OCP takeover request containing a null `port`, commonly followed by an OCP HTTP 400 response, is evidence that the selected workflow did not resolve the required scope. Do not edit hidden OBD metadata to repair an already registered deployment. If a supported edit of a running production deployment is rejected as an immutable or redeploy-required port change, follow the [configuration-scope classification](configuration-changes.md#serialized-effective-and-runtime-values) rather than forcing a reload or redeploy. Remove the compatibility duplication only when the exact installed takeover implementation proves that server scope is supported.

## Preflight, Execute, and Accept

In addition to the common deployment gate, verify `clockdiff`, Java/runtime requirements, OCP host resources, AVX/LSE rules for any bundled OceanBase nodes, exact artifact hashes, MetaDB capacity/backup, site URL/listener exposure, and every secret-bearing field. Render credentials only through the approved protected local procedure into a permission-controlled file.

Use the installed long-option syntax:

```bash
obd cluster deploy <deploy_name> --config=<reviewed_ocp_config.yaml>
obd cluster start <deploy_name> --strict-check
```

Use `--strict-check` only if installed start help supports it. Verify exact OCP artifact/process/listener/path ownership, authenticated administrator login, MetaDB connectivity and expected objects, OCP background tasks, and the requested management function. For same-deployment MetaDB, also verify OceanBase/OBProxy health and that exactly one intended OCP management relationship exists.

When automatic takeover is proved for the exact installed workflow, treat it as part of start acceptance: wait for the associated OCP task to finish, then confirm exactly one intended `ob_cluster` record in `RUNNING` state and reconcile its zones, servers, and compute hosts with the deployed topology. Do not append a manual export after this acceptance succeeds. Otherwise, establish component health first and then follow the manual takeover workflow.

When OCP login is unavailable or inconvenient, a protected read-only MetaDB check can provide independent takeover evidence. Inspect the installed OCP MetaDB schema before selecting columns, then reconcile the intended record across `ob_cluster`, `ob_zone`, `ob_server`, and `compute_host`. This proves registration and topology state; it does not replace authenticated OCP UI/API or a representative management operation.

For UI delivery diagnosis, an HTTP 200 response for `/` plus successful retrieval of its referenced JavaScript and CSS proves only that static assets are being served. To conclude that the UI is not blank, render it in a browser and verify visible DOM content and the absence of fatal console or asset-loading errors.

On partial failure, preserve the OBD trace, OCP task/logs, rendered configuration, MetaDB objects, account/grant state, processes/listeners, and current OCP records. Do not recreate tenants, switch MetaDB topology, load another package, delete an OCP record, or redeploy as generic recovery.

<a id="ocp-takeover"></a>

## Existing Cluster Takeover

This deployment reference does not replace the previously supported OCP takeover path. For an already running OBD-managed OceanBase cluster, use [Export an OBD Cluster to OCP](ocp.md#export-an-obd-cluster-to-ocp), including its utility-installation, credential-egress, task-state, and acceptance gates.

<a id="step-1-check-conditions"></a>

First apply that workflow's version-checked `check4ocp` conditions and classify any utility installation as a separate mutation.

<a id="step-2-export-to-ocp"></a>

Then use its protected, version-confirmed `export-to-ocp` procedure and verify the resulting OCP-managed cluster rather than treating command exit as takeover completion.
