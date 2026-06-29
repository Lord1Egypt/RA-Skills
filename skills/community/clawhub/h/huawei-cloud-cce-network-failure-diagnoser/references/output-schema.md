# Output Schema

`huawei_network_failure_diagnose` returns structured JSON with an embedded `report_markdown`.

```json
{
  "success": true,
  "action": "huawei_network_failure_diagnose",
  "region": "cn-north-4",
  "cluster_id": "cluster-id",
  "namespace": "default",
  "conclusion": "high signal conclusion",
  "confidence": "High",
  "pipeline_pruned": false,
  "findings": [
    {
      "stage": "Stage 3: East-West Routing and Policy Layer",
      "type": "NetworkPolicyBlocked",
      "title": "NetworkPolicy selects target Pod but does not allow source Pod labels or target port",
      "confidence": 1.0,
      "severity": "critical",
      "evidence": [],
      "recommendation": [],
      "prune": false
    }
  ],
  "top_causes": [],
  "snapshot": {
    "inputs": {},
    "nodes": [],
    "pods": [],
    "services": [],
    "ingresses": [],
    "endpoint_slices": [],
    "network_policies": [],
    "events": [],
    "logs": {},
    "cloud": {
      "elb_ids": [],
      "elbs": {},
      "eips": {},
      "nat": {},
      "security_groups": {},
      "vpc_acls": {}
    }
  },
  "report_markdown": "# CCE Network Failure Automated Diagnosis Report\n..."
}
```

## Markdown Sections

`report_markdown` must contain the following headings:

- `# CCE Network Failure Automated Diagnosis Report`
- `## 1. Diagnosis Overview`
- `## 2. Investigation Process`
- `## 3. Link Topology`
- `## 4. Key Object Snapshot`
- `## 5. Evidence Matrix`
- `## 6. Diagnosis Conclusion`
- `## 7. Recommended Actions and Verification Criteria`

## Finding Types

Common `type` values:

| Type | Description |
|------|-------------|
| `NodeUnhealthy` | Node Ready=False or Unknown |
| `NodePressure` | Node memory/disk/PID/network pressure |
| `PodDNSConfigMissing` | Pod dnsPolicy=None with no dnsConfig |
| `KubeDnsNoEndpoint` | kube-dns EndpointSlice 0 ready endpoints |
| `CoreDNSRestarting` | CoreDNS OOMKilled / probe failure / BackOff |
| `CoreDNSNxDomain` | CoreDNS logs show NXDOMAIN |
| `CoreDNSUpstreamTimeout` | CoreDNS logs show upstream timeout |
| `NetworkPolicyBlocked` | NetworkPolicy blocks source Pod (confidence 100%) |
| `ServiceNoReadyEndpoint` | Service EndpointSlice 0 ready endpoints |
| `ServiceSelectorMismatch` | Service selector matches no Pods |
| `ReadinessFlapping` | Backend readiness probe flapping |
| `BackendOverloaded` | Application OOM / connection pool exhausted |
| `LoadBalancerProvisioningFailed` | LoadBalancer Ingress status empty with CCM errors |
| `ELBBackendUnhealthy` | ELB member unhealthy, K8s Pod Ready |
| `IngressUpstreamError` | Ingress controller 502/504 logs |