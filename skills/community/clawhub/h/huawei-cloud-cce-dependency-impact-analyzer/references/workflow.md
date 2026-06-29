# Workflow

1. Scope: confirm region, cluster_id, namespace, target_name/workload_name/app_name/name, or label_selector.
2. Snapshot: collect Pods, Services, Ingresses, and Nodes from the current cluster state.
3. Target matching: find target Pods by label selector first, then by Pod name prefix, ownerReference, or label value matching the target name.
4. Upstream mapping: find Services whose selectors match target Pod labels; find Ingress rules/default backends that point to those Services.
5. Propagation paths: model external traffic as Ingress -> Service -> Pods and cluster traffic as Service DNS -> Pods.
6. Impact scoring: combine target Pod readiness, Service exposure, Ingress exposure, and number of propagation paths.
7. Evidence and limits: output Pod health, Service selector, Ingress backend, path table, Mermaid topology, and confidence limitations.
8. Handoff: if the target is unhealthy, pass root cause to `huawei-cloud-cce-root-cause-analyzer`; if remediation is needed, pass action to `huawei-cloud-cce-auto-remediation-runner`.
