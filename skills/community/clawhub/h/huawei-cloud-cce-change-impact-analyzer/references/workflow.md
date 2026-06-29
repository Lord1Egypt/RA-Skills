# Workflow

## 1. Scope & Ingestion

1. Collect `region`, `cluster_id`, `namespace` or cluster-wide scope, target object, fault symptoms, `fault_time`, `start_time`/`end_time` or `hours`.
2. Generate `Analysis-Trace-ID`; the report and structured output must preserve this ID.
3. Collect four categories of change shadow data in parallel:
   - Application and configuration changes: Deployment/StatefulSet/DaemonSet, ConfigMap, Secret write operations in CCE audit logs.
   - Network and routing changes: Service, Ingress, Gateway API, HTTPRoute/TCPRoute write operations.
   - Security policy changes: NetworkPolicy, Role, ClusterRole, RoleBinding, ClusterRoleBinding, ServiceAccount write operations.
   - Infrastructure changes: Node write operations, taint/cordon/drain indications, current node pool snapshot, cluster plugin/core configuration snapshot.
4. Simultaneously collect response signals: K8s historical events from LTS, AOM active+history alarms, current Pod/Service/Ingress/Node/ConfigMap/Secret/Security Group/VPC ACL snapshots.

## 2. Filtering & Categorization

1. Only retain write operations: `create`, `update`, `patch`, `delete`, `replace`.
2. Noise reduction — drop the following:
   - Lease, Event, TokenReview, SubjectAccessReview, Pod status, Endpoint/EndpointSlice routine controller writes.
   - ServiceAccount token sub-resource creation, Node status patch, NPD/kubelet heartbeat and other runtime status writes.
   - kube-scheduler Pod binding, and deployment/replicaset/statefulset/daemonset controller status-advancement writes; these are control-plane closed-loop operations, not user changes.
   - All `/status` sub-resource writes; audit logs may echo the full spec in requestObject, but the status sub-resource itself is not a configuration change.
   - Workload updates where HPA or controller only modifies `replicas`.
   - Ephemeral token Secrets and other short-lifecycle objects.
   - CCE platform-managed RBAC such as `system:cce:*`, `cce:*` where the actor matches CCE/platform components; RBAC changes by normal users or unknown objects are still retained as high-risk.
3. Semantic field retention:
   - Workload: `image`, `env`, `resources`, `readinessProbe`, `livenessProbe`, `ports`, `selector`, `affinity`, `tolerations`.
   - Config: `data`, `stringData`, CoreDNS `Corefile`, upstream DNS.
   - Network: Service `ports/selector`, Ingress/Gateway `rules/tls/backend`.
   - Security: NetworkPolicy `ingress/egress/policyTypes`, RBAC `roleRef/subjects`.
   - Node: `taints`, `unschedulable`, scheduling-related fields.

## 3. Impact & Blast Radius Modeling

1. Service changes: use selector to find matching Pods, reverse-query Ingress referencing this Service.
2. Ingress/Gateway changes: extract backend Service, infer external entry point to backend microservice path.
3. Workload changes: associate current Pods by workload name, then check Service selectors.
4. ConfigMap/Secret changes: regular objects scoped by namespace impact; CoreDNS/kube-proxy/core plugin configs treated as cluster-wide.
5. Node changes: associate Pods on that node; taint/unschedulable associate with Pending, FailedScheduling, Evicted events.
6. NetworkPolicy/RBAC changes: weighted by security boundary span; current version correlates via audit object and event/alarm keywords; future version will add current policy topology queries.

## 4. Risk Scoring

Base scores:

| Change Category | Typical Core Operations | Scope | Base Risk |
| --- | --- | --- | --- |
| Core Configuration | CoreDNS / kube-proxy / core plugin config | Global | Critical / 90 |
| Security Policy | NetworkPolicy / RBAC privilege escalation or restriction | Cross-service or cross-namespace | High / 75 |
| Infrastructure | Node taint / cordon / drain / node pool change | Node and scheduling path | High / 70 |
| Network Routing | Ingress / Gateway / Service port or backend change | Entry to microservice | Medium / 60 |
| Config Object | ConfigMap / Secret | Namespace-scoped dependent objects | Medium / 55 |
| Workload | Image, probe, resource, environment variable | Single service and upstream/downstream | Low-Medium / 45 |

Boost factors:

- Temporal proximity to `fault_time`: +0 to 15.
- Related K8s events in post-change window: +0 to 10.
- Related AOM alarms in post-change window: +0 to 12.
- More impacted entities in current topology: +0 to 12.
- Matches user target object or target namespace: +4 to 8.

## 5. Reporting

The report must include:

1. Analysis summary and `Analysis-Trace-ID`.
2. Investigation process: what each of the four stages did.
3. Data source collection status and gaps.
4. Core change timeline.
5. Top N highest risk alerts.
6. Blast radius and propagation paths.
7. Evidence matrix.
8. Conclusion, confidence, and read-only verification suggestions for next steps.