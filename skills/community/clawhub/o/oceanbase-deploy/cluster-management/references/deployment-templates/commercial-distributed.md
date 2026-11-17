# Commercial Distributed Artifact Overlay and Deployment Blueprint

Use this blueprint for an authorized commercial distributed OceanBase artifact set. The component is commonly named `oceanbase`, but the installed OBD plugin and repository are authoritative.

Commercial distributed and community distributed OceanBase use the same OBD deployment model and distributed YAML structure by default. This page contains the complete commercial overlay and shared structural shape; do not read the community blueprint as an additional prerequisite. Differences here are artifact identity/acquisition and any feature actually exposed by the commercial product, not a second generic OBD lifecycle. Commercial support does not permit substituting public community packages or fabricating proprietary fields.

## Required User and Artifact Inputs

- an exact complete commercial package closure already registered in the selected controller's OBD local repository, or user-provided files/an existing accessible path with provenance and access/license boundary; do not automatically download from Enterprise Software Download, a software center, support, a private repository, or a community mirror;
- exact OceanBase version, release, architecture, hash, plugin/workflow identity, and full dependency closure;
- supported upgrade/deployment compatibility evidence for OBD, OS/runtime, and only the OBProxy, OBAgent, OCP, or Config Server actually selected;
- cluster identity, target hosts, any explicit zone/failure-domain mapping, paths, ports, resources, non-database credential sources, and any explicitly supplied database bootstrap-password override; when no mapping is supplied for multiple Observer hosts, assign each distinct host to a distinct new zone in deterministic host order without asking, and do not request a password override when none was supplied;
- keep persistent auto-start false or unset unless the user requested it; do not ask for an auto-start choice merely because the schema exposes one;
- use the ordinary local/shared-nothing distributed layout proved by the selected installed plugin and package set.

If a required artifact, schema, dependency, or entitlement cannot be inspected, stop. Do not create a hybrid commercial/community deployment.

## Version Gate

Start with the installed public help/schema and version-matched distributed example. The reviewed OBD implementation groups `oceanbase` and `oceanbase-ce` under the common OceanBase plugin family, so a generic distributed field or lifecycle command does not need a second edition-specific proof. Inspect the packaged plugin only for a still-unresolved required field, proprietary feature, or version-specific behavior. Record the exact difference rather than treating the whole workflow as commercially unique.

## Schema-Gated Structure

This blueprint is intentionally non-executable until every bracketed item is replaced from the installed schema. The structural rule is mandatory: `servers` contains only server identity records; `global` holds values common to every server; and each server-specific override belongs in the sibling section named for that server. In the reviewed distributed schema, `zone` belongs in that named-server section. A `zone` key nested inside a `servers` list item can be silently ignored by affected builds and must never be used.

```yaml
user:
  username: <approved_ssh_user>
  <schema-supported-auth-key>: <protected_ssh_credential_reference>

<verified-commercial-distributed-component-key>:
  version: <locked_version_if_supported_here>
  release: <locked_release_if_supported_here>
  servers:
    - name: server1
      ip: <server1_management_ip>
    - name: server2
      ip: <server2_management_ip>
    - name: server3
      ip: <server3_management_ip>
  global:
    cluster_id: <unique_cluster_id>
    appname: <cluster_name>
    cpu_count: <reviewed_common_cpu_count>
    memory_limit: <reviewed_common_memory_limit>
    system_memory: <reviewed_common_system_memory>
    datafile_size: <reviewed_common_datafile_size>
    datafile_maxsize: <reviewed_common_datafile_maxsize>
    datafile_next: <reviewed_common_datafile_next>
    log_disk_size: <reviewed_common_log_disk_size>
    # Omit the verified database bootstrap-credential key by default so the
    # proved OBD workflow generates it; add it only for an explicit protected override.
  server1:
    zone: <server1_zone>
    <verified-home-path-key>: <server1_canonical_home_path>
    <verified-data-layout-keys>: <server1_approved_local_storage_values>
    <verified-log-layout-keys>: <server1_approved_values>
    <verified-service-address-and-port-keys>: <server1_approved_values>
  server2:
    zone: <server2_zone>
    <verified-home-path-key>: <server2_canonical_home_path>
    <verified-data-layout-keys>: <server2_approved_local_storage_values>
    <verified-log-layout-keys>: <server2_approved_values>
    <verified-service-address-and-port-keys>: <server2_approved_values>
  server3:
    zone: <server3_zone>
    <verified-home-path-key>: <server3_canonical_home_path>
    <verified-data-layout-keys>: <server3_approved_local_storage_values>
    <verified-log-layout-keys>: <server3_approved_values>
    <verified-service-address-and-port-keys>: <server3_approved_values>
```

Maintain a separate artifact lock manifest containing component, version, release, architecture, hash, source, and plugin identity. Prove the repository resolves to it before deployment and verify the installed binaries afterward.

## Pre-Bootstrap Topology Gate

Before any command that can bootstrap Observer:

1. Compare the `servers` list with the sibling named-server sections. Require one unique section for every listed name, no orphan section, and the intended management IP-to-name mapping.
2. Require the effective `zone` for every Observer to come from its named-server section or another placement accepted by the exact installed schema. For the reviewed distributed structure above, reject a zone placed only inside the list item.
3. Run the installed public parser/validation or precheck path. For a separated deployment, inspect the registered/effective configuration and confirm the exact server-to-zone map before `start`; YAML syntax success alone is insufficient.
4. For a maximum deployment, use `autodeploy` and validate the complete source mapping before launch. Its integrated generate/deploy/start sequence has no between-stage inspection point, so verify the generated mapping immediately afterward rather than substituting a different deployment command.

For a separated deployment, stop before start if the effective map is wrong or cannot be observed. For `autodeploy`, a wrong post-run map is a failed deployment result: preserve the trace and generated configuration and stop without autonomously using `destroy` or a full rebuild. Never bootstrap a disposable cluster merely to discover schema placement.

## Commercial Acceptance

In addition to ordinary cluster checks, verify the exact commercial component identity, intended topology and failure domains, actual package hashes, and every selected feature data plane. Generic process, listener, SQL, topology, tenant, lifecycle, and upgrade acceptance is the same as for community distributed OceanBase. Do not declare support or success merely because OBD parsed the YAML or found a package with the same version string.
