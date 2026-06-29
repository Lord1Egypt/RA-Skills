# Workflow

## 1. Collection Scope

Use `huawei_scan_cce_availability_risk` as the primary action. Common parameters:

- `region`, `cluster_id`: Required.
- `exclude_namespaces`: Defaults to `kube-system`; core addons are still individually identified.
- `gateway_keywords`: Defaults to `nginx,gateway,ingress,proxy,kong,apisix,traefik`.
- `metrics_hours`: Defaults to 24, used for master/node CPU and memory trends.
- `output_dir`: Outputs `availability-risk-summary.json` and `availability-risk-report.md`.

## 2. Control Plane and Node Risks

Check items:

- Visible master/control-plane node count is less than 3.
- Visible master nodes are not spread across multiple AZs.
- Master CPU/memory average values are too high.
- Ready nodes are concentrated in a single AZ, or one AZ has an excessively high proportion.
- Node pool/node AZ distribution does not match the business HA goals.

If the CCE managed control plane does not expose master nodes, you must mark it as a data gap in the report — do not assume master high availability.

## 3. Workload Risks

Check Deployments, StatefulSets, DaemonSets:

- Single replica: Business or gateway workloads with replica count less than 2.
- Missing PDB: Multi-replica business or gateway workloads without a matching PodDisruptionBudget.
- Pod distribution: Multiple replicas concentrated on a single node, or in a multi-AZ cluster concentrated in a single AZ.
- Health checks: Missing readinessProbe or livenessProbe.
- Affinity: Hard affinity binding to a single AZ, single node, or a specific node pool, or missing anti-affinity/topology spread constraints.
- Core addons: Whether CoreDNS, nginx-ingress, ingress-nginx have multi-replica anti-affinity or topology spread.
- Gateway applications: Whether nginx, gateway, ingress, proxy, kong, apisix, traefik are evenly deployed, configured with PDB and health checks.

## 4. Resource Overcommit

Check request/limit:

- Missing request: Marked as medium risk because scheduling, HPA, eviction, and capacity assessment become unreliable.
- CPU limit/request ratio greater than the default 4: Marked as low risk; confirm whether this is intentional burst design.
- Memory limit/request ratio greater than the default 2: Marked as medium risk; prioritize assessment of OOM and bin-packing risks.
- Aggregate cluster request and limit as proportions of allocatable capacity, to detect overall overcommit or capacity illusions.

## 5. Output and Remediation

Output order:

1. Overall risk level and issue count.
2. Control plane, node AZ, Pod AZ, and resource overcommit summary.
3. Top risk issue list.
4. Gateway and core addon specific issues.
5. Data gaps.
6. Remediation suggestions and authorized execution plan.

Remediation must first receive explicit customer authorization, then generate or apply PDB, probes, anti-affinity, topology spread, replica scaling, or resource request/limit adjustments. For execution, hand off to `huawei-cloud-cce-auto-remediation-runner` with proper safeguards and user confirmation.