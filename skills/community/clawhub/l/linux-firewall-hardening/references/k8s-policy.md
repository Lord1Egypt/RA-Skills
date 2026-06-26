# Kubernetes Node Firewall Policy

**CRITICAL**: Kubernetes nodes manage their own netfilter rules through the CNI plugin and kube-proxy. Manual host firewall changes can break pod networking, Service load balancing, and NetworkPolicy enforcement.

## Detection

```bash
# Is this a K8s node?
[[ -f /etc/kubernetes/kubelet.conf ]] && echo "Control plane or worker node"
[[ -d /etc/cni/net.d ]] && echo "CNI configuration present"

# Detect CNI plugin
ls /etc/cni/net.d/ 2>/dev/null
ps aux | grep -E "cilium|calico|flannel|kube-proxy" | grep -v grep

# Check kube-proxy mode
kubectl get configmap kube-proxy -n kube-system -o yaml 2>/dev/null | grep -i mode
curl -s http://localhost:10249/proxyMode 2>/dev/null
```

## CNI-Specific Guidance

| CNI | Dataplane | Action |
|-----|----------|--------|
| **Cilium** | eBPF (below netfilter) | Do NOT modify host netfilter. Use CiliumNetworkPolicy. |
| **Calico (eBPF)** | eBPF | Do NOT modify. Use Calico GlobalNetworkPolicy. |
| **Calico (iptables)** | iptables | Never flush. Use NetworkPolicy. |
| **Flannel** | iptables MASQUERADE | Never flush. Preserve MASQUERADE rules. |
| **kube-proxy (iptables)** | iptables Service DNAT | Never flush. |
| **kube-proxy (ipvs)** | IPVS + auxiliary iptables | Never flush iptables. |
| **kube-proxy (nftables)** | nftables Services | Never flush ruleset. |

## Required Policy: AUDIT-ONLY Mode

On any detected Kubernetes node, default to audit-only:
```bash
bash scripts/audit-firewall.sh --json
```

If `k8s_node: true`, do NOT proceed with host firewall changes. Recommend:
1. **NetworkPolicies** for pod-to-pod traffic
2. **Cloud security groups / VPC firewall** for node-level access
3. Narrow host-level changes ONLY for kubelet API (port 10250) and SSH — and only after staging cluster testing.

## Host Firewall vs NetworkPolicy

| Layer | Managed By | Controls |
|-------|-----------|---------|
| Host firewall (this skill) | ufw, firewalld, nftables, iptables | Traffic to the node's own IP |
| NetworkPolicy | CNI plugin | Traffic between pods |
| Cloud firewall / SG | Cloud provider API | Traffic entering/exiting VPC |

A properly secured K8s cluster uses **all three layers**.
