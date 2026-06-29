# Risk Rules

- Automated R1 read-only queries are allowed: nodes, Pods, Deployments, StatefulSets, DaemonSets, Services, Ingresses, PDBs, ReplicaSets, node metrics, and report generation.
- The scanner is prohibited from automatically modifying replica counts, PDBs, probes, affinity rules, topology spread constraints, request/limit settings, node pools, master configurations, or addon configurations.
- Any real remediation must be explicitly authorized by the customer, with documented impact scope, rollback method, and verification metrics.
- Regular workloads in `kube-system` are not treated as business risks by default, but core addons such as CoreDNS, nginx-ingress, and ingress-nginx must be checked for anti-affinity and distribution risks.
- When the managed control-plane master nodes are not visible, do not assume master high availability; mark it as a data gap and recommend verification via the CCE console/API.
- Remediation for single-replica, stateful, or gateway services must first confirm that the business supports multi-replica operation, session persistence, storage binding, and traffic entry policies.
- Before modifying health checks, confirm the probe path, port, timeout, initial delay, and failure threshold to avoid incorrect probes causing batch restarts.
- Before modifying affinity or topology spread, confirm node pool capacity, AZ resource availability, storage AZ binding, taints, and tolerations configuration.