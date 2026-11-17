<!-- Compatibility anchors retained for published 2.x deep links. -->
<a id="monitoring-setup-prometheus-grafana"></a>
<a id="monitoring-setup-prometheus--grafana"></a>

# Monitoring

Use this workflow for OBAgent collection, Prometheus storage/query, and Grafana visualization. Treat each as optional; deploy only the subset required for the requested outcome.

## Resolve Scope and Compatibility

1. Record OBD build, deployment/product form, selected component plugins, registered components, and current monitoring integrations.
2. Confirm exact component keys, versions, releases, architectures, hashes, dependency graph, and incremental add/delete/upgrade support from installed plugins and repositories.
3. Establish compatibility among OceanBase, OBAgent metric schema/authentication, Prometheus scrape/auth, Grafana datasource/dashboards, OBD, OS, and architecture.
4. Record per-component hosts, ports, canonical home/data/log paths, retention, disk/inode growth budget, CPU/memory, credentials, TLS, datasource, network ingress/egress, and co-location impact.
5. Identify existing OBAgent endpoints and configuration ownership. Derive endpoint, path, authentication, and labels from the installed plugin and effective configuration; do not guess a universal scrape URL.

Repository availability does not establish compatibility. Do not copy a monitoring YAML from another product form/version or expose generated credentials in a report.

## Schema-Gated Incremental Configuration

Validate every field with the installed component schema. The rendered incremental YAML must include only requested monitoring components and required dependencies. In particular, resolve:

- OBAgent target OceanBase endpoints, credentials/secret references, metric listener, and ownership;
- Prometheus listener, data path, retention, scrape targets, and authentication/TLS;
- Grafana listener, persistent data, administrator credential source, Prometheus datasource, and dashboard compatibility;

Do not treat placeholders as deployable YAML. Validate the complete rendered configuration with the selected plugins before execution.

## Official V4.6.0 Example Baselines

Prefer the examples shipped by the resolved OBD installation, normally under `/usr/obd/example/` for RPM/direct installs or the selected All-in-One installation's `obd/usr/obd/example/` directory:

- `prometheus/distributed-with-obagent-and-prometheus-example.yaml`;
- `grafana/all-components-with-prometheus-and-grafana.yaml`;
- `grafana/prometheus-and-grafana.yaml`;
- component-specific examples under `obagent/`, `prometheus/`, and `grafana/`.

Record the example checksum and copy it to a reviewed work path. The minimum real-key dependency chain in the V4.6.0 released examples is:

```yaml
obagent:
  depends:
    - oceanbase-ce
  servers:
    - name: server1
      ip: CHANGE_ME_OBSERVER_IP
  global:
    home_path: CHANGE_ME_OBAGENT_HOME

prometheus:
  depends:
    - obagent
  servers:
    - CHANGE_ME_PROMETHEUS_HOST
  global:
    home_path: CHANGE_ME_PROMETHEUS_HOME

grafana:
  depends:
    - prometheus
  servers:
    - CHANGE_ME_GRAFANA_HOST
  global:
    home_path: CHANGE_ME_GRAFANA_HOME
    login_password: CHANGE_ME_PROTECTED_LOCAL_VALUE
```

This is an official V4.6.0 structural baseline, not a universal schema or complete production configuration. Preserve the installed example's component-specific authentication, ports, storage/retention, and per-server mappings after review. Render secrets only through a protected local procedure.

<a id="scenario-1-obagent-not-deployed"></a>
<a id="scenario-2-obagent-already-deployed"></a>

For an existing cluster, choose the V4.6.0 documented branch before rendering:

1. **No existing OBAgent:** the guide creates a separate deployment containing OBAgent, Prometheus, and Grafana, with OBAgent explicitly mapped to the observed OceanBase servers. Do not claim a cross-deployment `depends` edge; fill its OceanBase endpoint, cluster, zone, path, and credential fields from effective configuration.
2. **Existing OBAgent:** create only Prometheus and Grafana, populate Prometheus scrape configuration from the observed OBAgent authentication/endpoints, and preserve the required rule files. Do not deploy a duplicate OBAgent.
3. **Multiple clusters or dynamic OBAgent membership:** use the installed schema for Prometheus `file_sd_configs` and OBAgent `target_sync_configs`; verify the target directory, SSH/authentication, generated target files, and reload/restart behavior. All collected OBAgents must use compatible authentication, or use separate scrape jobs.

<a id="authentication"></a>

The released V4.6.0 monitoring flow can enable Prometheus basic authentication and expose the generated access identity through the effective configuration or `obd cluster display`. Preserve that tested discovery path without printing its password: inspect it only through the approved local secret-handling procedure, record the non-secret endpoint/user identity with the value redacted, and verify the credentials against the intended Prometheus endpoint. Do not treat display output as permission to copy the credential into chat, logs, or another deployment.

Do not silently copy rules or configuration between deployment-owned directories. Enumerate source/destination paths, owners, modes, overwrite behavior, and future synchronization ownership, then authorize that file mutation separately.

## Optional Incremental Add

The official V4.6.0 existing-cluster paths above create a separate monitoring deployment. Use an in-place incremental component workflow only when the installed OBD help and selected plugins explicitly prove it is supported for the current running product form, exact component set, and restart behavior. When proved, the command is commonly:

```bash
obd cluster component add <deploy_name> --config=<monitoring_increment.yaml>
```

Never use redeploy as the default way to add monitoring: it destroys and rebuilds deployment-owned state. If the installed build lacks a safe incremental path, stop and present that limitation; do not edit `.obd` metadata or replace the full deployment configuration.

For an existing OBAgent, add only the requested downstream components and configure them against the observed endpoints. Do not deploy a duplicate agent merely to match an example.

Before `component add`, read the restart and path-cleaning gate in [component-changes.md](component-changes.md#add-a-component). OBD V4.6.0 can prompt to restart the deployment after adding a component; `--confirm` skips that prompt and does not mean “no restart.” Do not add `--confirm`, `--force`, or `--clean` to make automation non-interactive. Display the exact restart set and any work-directory deletion first, or stop.

## Layered Acceptance

Verify each requested layer independently:

1. component is registered exactly once and its process/listener/path belongs to the intended deployment;
2. OBAgent exposes current OceanBase metrics for the intended cluster/tenant scope;
3. every intended Prometheus target is healthy and an expected OceanBase series returns current samples;
4. Grafana uses the intended datasource and a compatible dashboard returns current data;
5. existing OceanBase, OBProxy, OCP, and client paths remain healthy.

Prometheus `/-/ready` or a Grafana login page proves only that local service layer. Neither proves collection, query, or visualization end to end.

When Grafana API access is available and within scope, prefer an additional datasource-proxy evidence chain:

1. query the installed version's `/api/health` endpoint;
2. list datasources and identify the intended Prometheus datasource by UID, type, and redacted URL;
3. use that version's supported datasource-proxy route to submit a bounded Prometheus query for an OceanBase metric, and verify the returned cluster/tenant labels and sample freshness;
4. use dashboard search or a dashboard-UID endpoint to prove the intended compatible dashboard exists.

Keep the direct Prometheus target/query check as separate evidence: the proxy query proves the Grafana-to-datasource-to-Prometheus path rather than replacing collector validation. Determine whether the installed Grafana uses an ID- or UID-based proxy route and how it authenticates; do not hard-code one API shape or expose credentials. If that build does not expose a safe proxy API, record the limitation and use an equivalent version-proved UI/API check instead of treating a remembered route as universal.

<a id="component-deletion-order"></a>

## Upgrade and Removal

Derive upgrade order and rollback from the selected versions and dependency graph. Preserve dashboards, datasource configuration, and retention data when required.

Before deletion, list every dependant and consumer and show retained data. Migrate or remove references first, then use the installed component-delete workflow in the derived order. Do not assume one fixed Grafana/Prometheus/OBAgent order across releases. Verify processes, listeners, registered configuration, references, and explicitly retained data afterward.

For the released V4.6.0 dependency chain shown above, the preserved observed order is to remove Grafana before Prometheus, then remove OBAgent only after no remaining scrape or dashboard dependency uses it. After revalidating the installed graph and authorizing the exact components, the public command path commonly has this shape:

```bash
obd cluster component del <deploy_name> grafana prometheus
obd cluster component del <deploy_name> obagent
```

Do not apply this order blindly to a different version, a deployment with other dependants, or a shared OBAgent.

## Failure Recovery

Preserve trace, before/after configuration, artifact identities, processes/listeners, OBAgent endpoint evidence, Prometheus target/query state, and Grafana datasource state. Do not delete components, directories, monitoring data, or redeploy as generic cleanup; choose recovery from the observed failed layer.
