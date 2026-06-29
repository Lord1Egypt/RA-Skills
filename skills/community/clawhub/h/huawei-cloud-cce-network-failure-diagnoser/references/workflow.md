# Workflow

## Reuse Priorities

Existing capabilities must be reused first:

- K8s objects: `huawei_get_cce_services`, `huawei_get_cce_ingresses`, `huawei_get_cce_pods`, `huawei_get_kubernetes_nodes`, `huawei_get_cce_events`, `huawei_get_pod_logs`.
- Cloud network: `huawei_list_elb`, `huawei_list_elb_listeners`, `huawei_get_elb_metrics`, `huawei_list_eip`, `huawei_get_eip_metrics`, `huawei_list_nat`, `huawei_get_nat_gateway_metrics`, `huawei_list_security_groups`, `huawei_list_vpc_acls`.
- Legacy comprehensive diagnosis: `huawei_network_diagnose`, `huawei_network_diagnose_by_alarm` — can still be used for workload-level link and monitoring coarse diagnosis.
- Logging & observability: existing LTS/AOM logs, Pod logs, AOM metrics capabilities are available; do not re-implement log or metrics platforms.

New thin-layer capabilities added by this skill:

- `huawei_network_failure_diagnose`: one-shot collection of Service, Ingress, EndpointSlice, NetworkPolicy, Node, Pod, Events, CoreDNS/Ingress logs and cloud ELB backend health, directly generating a Markdown report.
- `huawei_get_elb_backend_status`: reads ELB pool/member/health monitor/load balancer status, filling the gap where ELB metrics alone cannot confirm specific backend health.

What this skill still does NOT do:

- Does not execute `kubectl exec` for active probing; does not modify security groups/ACLs/ELB/Ingress/Service.
- Does not replace `huawei-cloud-cce-pod-failure-diagnoser`, `huawei-cloud-cce-node-failure-diagnoser`, or `huawei-cloud-cce-workload-failure-diagnoser`; when Pod/Node/deployment root causes are found, it only cross-references them.

## Input and Collection

Minimum input: `region`, `cluster_id`, `namespace`. Provide as many of the following as possible:

- `failure_symptom`: `domain_unresolvable`, `in_cluster_service_unreachable`, `service_intermittent`, `external_access_failed`, `ingress_502_504`.
- `target_kind` + `target_name`: Pod, Service, Ingress, etc.
- `service_name`, `ingress_name`, `source_pod`, `destination_pod`, `domain`, `elb_id`.

Default: call `huawei_network_failure_diagnose` first. It creates a near-simultaneous read-only context snapshot and returns:

- `snapshot`: raw objects and cloud-side context.
- `findings` / `top_causes`: structured diagnosis hits.
- `report_markdown`: the final complete Markdown report delivered to the customer.

## Layered Diagnosis Pipeline

### 1. Infrastructure and Node Layer

Check target source/destination Pods, backend Pods, and CoreDNS/Ingress Controller nodes first:

- `Ready=False` or `Ready=Unknown`: output node infrastructure failure directly and prune (skip) upper application-layer diagnosis.
- `MemoryPressure`, `DiskPressure`, `PIDPressure`, `NetworkUnavailable=True`: correlate with `OOMKilled`, `KubeletNotReady`, `Evicted`, `FailedCreatePodSandBox` events. If overlapping with the failure window, prune.

### 2. DNS Path

Trigger condition: `failure_symptom` contains DNS, domain, resolution, NXDOMAIN, etc.

Path: Client Pod → `kube-dns` Service → CoreDNS Pods → upstream DNS / cluster Service DNS.

Assertions:

- Client Pod `dnsPolicy=None` with no `dnsConfig`: output Pod DNS configuration missing.
- `kube-dns` EndpointSlice has 0 ready endpoints: output CoreDNS backend unavailable.
- CoreDNS Events contain `OOMKilled`, `Liveness probe failed`, `Unhealthy`, `BackOff`: output CoreDNS restart/probe failure causing resolution flapping.
- CoreDNS logs contain `NXDOMAIN`: output service name typo, namespace suffix, or non-existent service.
- CoreDNS logs contain `i/o timeout` / timeout: output upstream DNS or out-of-cluster network failure candidate.

### 3. East-West Service and Policy Layer

Trigger condition: in-cluster Service unreachable, intermittent, flapping, or default check when no external path is specified.

Path: Source Pod → NetworkPolicy → Service → EndpointSlice → Destination Pod.

Assertions:

- Target Pod selected by NetworkPolicy but rules do not allow source Pod labels, namespace labels, or port: output NetworkPolicy blocking (confidence 100%).
- Service selector matches no Pods, or EndpointSlice has 0 ready endpoints: output Service selector/backend topology broken.
- Backend Pod Events show dense `Readiness probe failed` or `Unhealthy`: output readiness flapping causing backend removal.
- Backend application logs show OOM, connection pool exhausted, connection refused: output application overloaded/refusing connections candidate.

### 4. North-South Ingress/ELB Layer

Trigger condition: external domain/IP access failure, Ingress 502/504, ELB backend abnormal.

Path: External request → Cloud ELB/EIP → Ingress Controller → Service → EndpointSlice → Pod.

Assertions:

- Ingress or LoadBalancer Service `status.loadBalancer.ingress` is empty: correlate with CCM/CCE Events showing ELB creation failure, quota exceeded, insufficient permissions, security group/subnet errors.
- ELB member/pool status unhealthy while K8s backend Pod is Ready: output cloud security group not allowing NodePort, health check port mismatch, or node IPVS/Iptables/kube-proxy sync anomaly candidates.
- Ingress Controller logs show `502 Bad Gateway`, `504 Gateway Timeout`: output Ingress-to-backend or backend application response anomaly; continue checking Service/Endpoint and application timeout.

## Report Requirements

The Markdown report must include:

1. **Diagnosis Overview**: target, symptom, conclusion, confidence, collection time, pruned stages.
2. **Investigation Process**: four-stage per-item status — checked, abnormal, or pruned/skipped.
3. **Link Topology**: output DNS, east-west, or north-south path based on failure type.
4. **Key Object Snapshot**: Service, EndpointSlice, Backend Pods, Ingress, NetworkPolicy, Cloud ELB.
5. **Evidence Matrix**: stage, type, confidence, evidence summary.
6. **Top Root Causes**: max 3, each backed by evidence.
7. **Recommended Actions and Verification Criteria**: read-only verification steps or change suggestions to hand off to the remediation skill.