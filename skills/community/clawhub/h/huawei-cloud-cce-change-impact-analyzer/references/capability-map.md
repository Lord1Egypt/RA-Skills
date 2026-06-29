# Capability Map

## Repository Architecture

This repository uses a simplified multi-skill architecture:

- Each skill is independently placed in `skills/<skill>/`.
- Capability implementations are centralized in the root `scripts/huawei_cloud/`.
- `scripts/huawei-cloud.py` serves as the unified CLI entry point.
- `scripts/huawei_cloud/dispatcher.py` maintains the action-to-Python-handler mapping.
- `skill-profile.yaml` declares tool boundaries; `scripts/dev/generate_manifests.py` generates `manifest.json`.

`huawei-cloud-cce-change-impact-analyzer` does not duplicate scripts; it reuses shared capabilities via `skills/huawei-cloud-cce-change-impact-analyzer/scripts -> ../../scripts` symlink.

## Reusable Capabilities

| Capability Domain | Existing Action / Script | Reuse Method |
| --- | --- | --- |
| Audit Changes | `huawei_query_cce_audit_logs` / `cce_app_logs.py` | Retrieve Kubernetes audit create/update/patch/delete change shadows, including actor, verb, resource, namespace, name, requestURI, statusCode, raw audit. |
| K8s Historical Events | `huawei_query_k8s_events_from_lts` / `cce_events_lts.py` | Read historical Events from LTS, overcoming the K8s API short event window. |
| Current Events | `huawei_get_cce_events` / `cce.py` | Query current Events when LTS Events are unavailable. |
| Alarm Correlation | `huawei_analyze_aom_alarms` / `aom.py` | Analyze active + history alarms simultaneously, avoiding missed resource alarms that have already recovered. |
| Rollout Diagnosis | `huawei_workload_rollout_diagnose` / `workload_rollout_diagnosis.py` | Drill down when changes point to Deployment/StatefulSet/DaemonSet rollout failures. |
| Network Diagnosis | `huawei_network_failure_diagnose` / `network_failure_diagnosis.py` | Drill down when changes point to Service/Ingress/NetworkPolicy/ELB connectivity failures. |
| Node Diagnosis | `huawei_node_failure_diagnose` / `node_failure_diagnosis.py` | Drill down when changes point to Node taint, NotReady, scheduling anomalies, or node resource pressure. |
| Current Topology | `huawei_get_cce_pods`, `huawei_get_cce_services`, `huawei_get_cce_ingresses`, `huawei_get_kubernetes_nodes` | Build Pod-Service-Ingress-Node impact scope. |
| Config Snapshots | `huawei_list_cce_configmaps`, `huawei_list_cce_secrets` | Identify CoreDNS, kube-proxy, and business config object current state. |
| Cloud Network Snapshots | `huawei_list_security_groups`, `huawei_list_vpc_acls` | Provide Security Group/ACL current state for report gaps and manual verification. |

The external `pancake0001/cce-skills` `huawei-cloud` skill also covers these directions: unified Huawei Cloud resource queries, CCE resource queries, AOM alarm active+history analysis, LTS logs, network/workload/node diagnosis, auto inspection, and HTML diagnosis reports. This repository has already split these capabilities into finer diagnosers and a shared dispatcher, suitable for reuse in `huawei-cloud-cce-change-impact-analyzer` rather than reimplementing.

## Added Composite Capability

New action: `huawei_change_impact_analyze`.

It is not a single-query tool but a composite orchestration:

1. Generate `Analysis-Trace-ID`.
2. Collect audit logs, K8s historical events, AOM alarms, and current resource snapshots.
3. Apply core change classification and noise elimination on audit write operations.
4. Map changes to current topology and calculate blast radius.
5. Correlate with fault time, events, and alarms.
6. Output structured `top_changes`, full `changes`, and customer-deliverable `report_markdown`.

## Noise Reduction Rules Optimized from Real Cluster Cases

Real clusters have shown `ClusterRole/system:cce:packageversion` updated by `system:masters` / CCE platform components in audit records. This object belongs to CCE self-managed component metadata and should not be output as a customer business anomaly change. The current version excludes the following runtime or platform-managed behaviors from core changes:

- `serviceaccounts/token` sub-resource creation.
- `nodes/status` patch.
- All `/status` sub-resource writes, even when audit logs echo the full spec in requestObject.
- kube-scheduler `pods/binding`.
- deployment/replicaset/statefulset/daemonset controller status-advancement workload writes.
- CCE platform-managed RBAC: `system:cce:*`, `cce:*` where the actor matches CCE/platform components.

RBAC changes by normal users, unknown actors, or non-CCE-managed objects are still retained as high-risk.

## Atomic Capabilities Still Needed

| Gap | Reason | Suggested Action |
| --- | --- | --- |
| CTS/Cloud Audit History | Currently can only reconstruct Kubernetes audit well; cannot reliably reconstruct CCE console, node pool, cluster upgrade, ELB, Security Group, VPC ACL historical changes. | `huawei_query_cts_traces`, supporting service/resource/user/time/filter. |
| Before/After YAML Snapshot | Audit may not record `requestObject`/`patch`; only object-level judgment possible, no strict Semantic Diff. | `huawei_get_k8s_resource_history` or integrate GitOps/backup system. |
| NetworkPolicy Current Topology | Existing network diagnosis has internal policy judgment, but lacks an independent list/parse action. | `huawei_list_cce_networkpolicies`, outputting selector, ingress, egress, and matching Pods. |
| RBAC Current Topology | Missing Role/ClusterRole/Binding queries, cannot evaluate privilege boundary propagation details. | `huawei_list_cce_rbac`, outputting subject → role → verbs/resources. |
| Gateway API Current Topology | Can identify Gateway/HTTPRoute in audit, but current snapshots lack independent query. | `huawei_list_cce_gateway_api_resources`. |
| ConfigMap/Secret Usage Relationships | Currently can only infer by namespace or core component names; lacks "which Pods/Workloads reference this config". | `huawei_find_config_consumers`, scanning volumes/envFrom/env/valueFrom. |
| Node Taint/Toleration Precise Impact | Currently only associates node Pods; lacks Pod tolerations and scheduling constraint simulation. | `huawei_analyze_node_taint_impact`. |
| Cloud Network Change Diff | Only has current SG/ACL snapshot; lacks historical rule changes and actors. | Depends on CTS, plus `huawei_analyze_cloud_network_change`. |

## Gap-Filling Conclusion

The current repository already has the main capabilities for "observation, audit, events, alarms, Workload/Node/Network drill-down" and is sufficient to implement a first-version change impact attribution report. The primary shortcomings are cloud-side historical changes and strict before/after diff; these cannot be filled by composite skill reasoning alone and require subsequent CTS, NetworkPolicy/RBAC/Gateway independent queries, and config reference relationship scanning atomic capabilities.