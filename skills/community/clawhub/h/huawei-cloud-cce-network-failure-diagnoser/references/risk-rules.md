# Risk Rules

- Allowed: automatic read-only queries for Service, Ingress, EndpointSlice, NetworkPolicy, Pod, Node, Events, Pod logs, ELB, EIP, NAT, security groups, and ACLs.
- Allowed: generating Markdown diagnosis reports and read-only verification command suggestions.
- Not allowed: modifying Service, Ingress, NetworkPolicy, CoreDNS ConfigMap, security groups, ACLs, ELB listeners, ELB backends, EIP bindings, or NAT rules.
- Not allowed: executing `kubectl exec`, packet capture, stress testing, or active traffic injection unless the user explicitly requests and acknowledges the risk.
- `huawei_network_verify_pod_scheduling` is for verification only; it does not replace scaling execution.
- Any network change suggestion must describe impact scope, rollback method, and verification criteria, and be handed off to `huawei-cloud-cce-auto-remediation-runner` for preview.