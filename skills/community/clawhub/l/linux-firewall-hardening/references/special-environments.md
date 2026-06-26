# Special Environments & When NOT to Use

## When NOT to Use This Skill

| Condition | Why | Alternative |
|-----------|-----|-------------|
| **Kubernetes worker node** | CNI plugins (Calico, Cilium, Flannel) manage netfilter. Host firewall changes break pod networking. | Use NetworkPolicies / CiliumNetworkPolicy |
| **Firewall managed by Terraform/Ansible/Puppet/Chef** | Manual changes will be overwritten on next IaC run. | Update `.tf` / playbook / manifest / cookbook |
| **Cloud workload with Security Group / NSG only** | This skill is host-level. Cloud firewall is often the better layer. | Use cloud provider's firewall API |
| **Inside a container** | Containers share the host's netfilter. Cannot modify from inside. | Escalate to host operator |
| **CI/CD pipeline ephemeral runner** | Firewall rules on ephemeral runners don't persist and can break pipeline networking. | Use pipeline-level network controls |
| **Shared hosting / managed hosting** | Provider controls the firewall; changing it may violate ToS. | Use provider's firewall panel |
| **WSL2 (Windows Subsystem for Linux)** | WSL2 networking is NAT'd through Windows. netfilter modules are often incomplete or absent. iptables may fail silently. nftables support is experimental. | Use Windows Defender Firewall or cloud VM |
| **macOS** | BSD `pf` firewall, not Linux netfilter. This skill is Linux-only. | Use `pfctl` or GUI firewall |

## Container Environments

### Docker Host vs Docker-in-Docker

| Scenario | Is Host Firewall Accessible? | Safe to Use This Skill? |
|----------|---------------------------|------------------------|
| Bare-metal / VM running Docker | Yes | Yes — follow Docker Hardening section |
| Docker-in-Docker (DinD) | Depends on privileged mode | No — outer host rules invisible |
| Rootless Docker | Partial — user namespaces limit netfilter access | No — use host-level firewall |
| Podman (rootless) | No — user namespace isolation | No — use host-level firewall |

### LXC / LXD Containers

LXC containers may have restricted netfilter capabilities:
- **Privileged containers**: Usually can manage netfilter, but conflicts with host rules.
- **Unprivileged containers**: netfilter modules often not loaded. `nf_tables` kernel module may be absent.
- **Detection**: `lsmod | grep nf_tables` in container. If empty, host firewall management is impossible.

**Recommendation**: Always manage firewall from the LXC/LXD **host**, not from inside containers.

### systemd-nspawn

Similar to LXC — netfilter access depends on capabilities and kernel module availability. Test with `sudo nft list ruleset` before assuming access.

## Kubernetes-Specific Guidance

### CNI Plugin Details

| CNI | Dataplane | Host Firewall Safe? | Alternative |
|-----|----------|---------------------|-------------|
| Cilium | eBPF (below netfilter) | **NO** — eBPF programs run before iptables | CiliumNetworkPolicy |
| Calico (eBPF mode) | eBPF | **NO** | Calico GlobalNetworkPolicy |
| Calico (iptables mode) | iptables | **PARTIAL** — never flush, only add to user chains | NetworkPolicy + Calico-specific annotations |
| Flannel | iptables (MASQUERADE only) | **LIMITED** — preserve MASQUERADE rules | NetworkPolicy |
| Weave | Custom fast datapath | **NO** | NetworkPolicy |
| kube-router | iptables + BGP | **PARTIAL** — preserve kube-router chains | NetworkPolicy |
| Antrea | OVS / eBPF | **NO** | Antrea NetworkPolicy |

### kube-proxy Modes

| Mode | Impact of Host Firewall Change |
|------|-------------------------------|
| iptables | Flushing iptables destroys all Service ClusterIP DNAT. Pods lose Service discovery. |
| ipvs | IPVS rules survive iptables flush, but auxiliary iptables rules (SNAT, NodePort) may break. |
| nftables | `nft flush ruleset` destroys all Service networking. |
| eBPF | Host netfilter changes have minimal impact. Still, do not modify — use eBPF-native policies. |

### What YOU CAN Do on K8s Nodes

Even on K8s nodes, these limited changes are usually safe:
- Restrict SSH access (change sshd_config, not firewall)
- Add fail2ban for SSH (does not modify netfilter chains used by CNI)
- Harden kernel parameters (ONLY values verified safe for your CNI)
- Monitor dropped packets (read-only)

## WSL2

WSL2 runs a real Linux kernel but with important limitations:

- **Network architecture**: WSL2 network is NAT'd behind Windows. The Windows host is the real network edge.
- **iptables/nftables**: Partially functional. Some modules (e.g., conntrack helpers) may be disabled.
- **Persistence**: Firewall rules survive WSL2 session restarts but not Windows reboots (unless configured in `/etc/wsl.conf`).
- **Port forwarding**: Windows auto-forwards `localhost` ports but not LAN ports by default.

**Recommendation**: Use Windows Defender Firewall for edge protection. Use WSL2 iptables/nftables only for inter-WSL2-distro isolation or container-in-WSL2 scenarios.

## Confidence Implications

Environment detection that finds any of the above conditions should:
1. Set `risk_tier` to `halt` or `manual` (see confidence gating in SKILL.md).
2. Include the specific reason in `halt_reasons[]`.
3. Exit with the appropriate exit code (see exit codes table below).

## Exit Codes (Standardized)

> **Canonical source**: SKILL.md § Exit Codes (Core Contract). This table is a reference copy and must match.

| Code | Name | Meaning |
|------|------|---------|
| 0 | SUCCESS | Operation completed successfully |
| 1 | FAIL | Generic failure |
| 10 | BACKEND_CONFLICT | Multiple active firewall frontends detected |
| 11 | BACKEND_ABSENT | No firewall backend could be detected |
| 12 | BACKEND_UNKNOWN | Multiple backends active — cannot determine primary |
| 20 | IAC_MANAGED | Firewall managed by external IaC (Terraform, Ansible, etc.) |
| 21 | CONTAINERIZED | Inside a container — cannot modify host firewall |
| 22 | K8S_NODE | Kubernetes node detected — use NetworkPolicies |
| 30 | CONFIDENCE_LOW | Confidence below 70% — audit-only mode |
| 31 | NO_ROLLBACK | No rollback mechanism available (install at or use systemd-run) |
| 40 | PREFLIGHT_FAIL | Pre-flight checks failed |
| 41 | PLAN_MISMATCH | Plan approval token mismatch — re-run PLAN |
| 42 | BACKUP_FAIL | Could not create backup |
| 50 | APPLY_FAIL | Rule application failed — auto-rollback triggered |
| 51 | APPLY_PARTIAL | Partial apply — auto-rollback triggered |
| 60 | VERIFY_FAIL | Post-apply verification failed |
| 61 | STATE_CONFLICT | State file conflict — resolve stale state |
