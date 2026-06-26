# Publish Listing: linux-firewall-hardening

## Short Description (150 chars)
Safe Linux firewall hardening with backend detection, idempotent atomic rules, rollback protection, dry-run planning, risk-tier gating, and AI-executable state-machine workflows.

## When to Use

- Check if a Linux server has active firewall protection
- Enable and configure a firewall without locking yourself out of SSH
- Audit existing rules, troubleshoot connectivity, or apply a security profile
- Automate firewall hardening via an AI agent or CI/CD pipeline

## When NOT to Use

- Kubernetes worker node → use NetworkPolicies / CiliumNetworkPolicy
- Firewall managed by Terraform/Ansible/Puppet/Chef → update IaC source of truth
- Cloud workload with Security Group / NSG only → use cloud provider's firewall API
- Inside a container → escalate to host operator
- WSL2 / macOS / shared hosting → see `references/special-environments.md`

## Full Description

`linux-firewall-hardening` is an AI-native DevSecOps playbook for auditing, configuring, and hardening Linux firewalls across all major backends: **ufw**, **firewalld**, **nftables**, and **iptables**.

Unlike traditional tutorials, this skill is structured as a **state machine** that AI agents can execute safely and repeatably:

| State | What Happens |
|-------|-------------|
| **Detect** | Auto-detect firewall stack, containerization (Docker/Podman/K8s), cloud provider (AWS/GCP/Azure), SSH port, exposure, ownership manager (Terraform/Ansible/Puppet/Chef/cloud-init), fail2ban. Computes confidence score and risk tier (`auto`/`confirmed`/`manual`/`halt`). |
| **Select** | Choose backend path from decision tree. Load security profile (web-server, database, bastion, zero-trust) or define custom ruleset. Validate ownership — stop if IaC-managed. |
| **Plan** | Dry-run diff with JSON schema (`add`/`skip`/`remove` arrays, `approval_token`, `risk_assessment`). Required review gate for `confirmed` risk tier. Cache audit results (/tmp/firewall-audit.json, TTL 5min). Outputs `approval_token` hash for APPLY verification. |
| **Validate** | Snapshot current rules, schedule auto-rollback timer (at + systemd-run dual-backend), verify idempotency, confirm change window. Optional state persistence (`~/.firewall-hardening/state.json`). Mandatory pre-flight checklist. |
| **Apply** | Apply rules idempotently (check-before-set). Requires `--approved-plan=<token>` matching PLAN output. Atomic replacement where supported (`nft -f`, `iptables-restore`). Persist across reboots. |
| **Verify** | Run `firewall-verify.sh`: SSH reachable, intended ports only, IPv4/IPv6 symmetry, persistence, Docker exposure, fail2ban active. MUST complete within rollback timer window (default 5 min). Timeout → auto-rollback. Cancel rollback only after all checks pass. |

Key features:

- **Environment auto-detection**: `scripts/audit-firewall.sh` with `--json` output including confidence score, risk tier (`auto`/`confirmed`/`manual`/`halt`), recommended backend, halt reasons, rollback capability detection.
- **Risk-tier gating**: Auto (≥90% confidence) → proceed; Confirmed (70–89%) → plan review required; Manual (50–69%) → audit-only; Halt (<50%) → stop immediately.
- **Dry-run planning**: `scripts/firewall-plan.sh` generates a diff before applying — showing which rules will be added, skipped, or removed. Supports `--profile`, `--ports`, `--json`.
- **Backend ownership rules**: When ufw or firewalld owns the policy, prohibits direct nftables/iptables mutation — prevents split-brain state.
- **Ownership boundary detection**: Detects Terraform, Ansible, Puppet, Chef, cloud-init, Kubernetes CNI — halts if manual mutation would conflict with IaC.
- **Idempotent commands**: Every rule uses check-before-set patterns, safe for CI/CD and repeated runs.
- **Atomic rule changes**: `nft -c` dry-run and `iptables-restore` atomic swap instead of dangerous `-F` / `-A`.
- **Auto-rollback**: Rescue timer (at + systemd-run fallback) restores from backup first, falling back to emergency open — preserving Docker NAT, CNI rules, and pre-existing configurations.
- **Observability**: nftables counters, conntrack monitoring, dropped-packet logs, fail2ban metrics, and recommended baselines for anomaly detection.
- **Performance & compliance**: conntrack exhaustion, SYN flood, sysctl tuning; maps controls to CIS, PCI-DSS, SOC2.
- **Declarative policy (v2.0)**: YAML schema with `schema_version`, `metadata`, `backend_compat` hints, hard-fail validation, golden fixtures — renders to all four backends from one source of truth.
- **Security profiles**: Pre-built hardened configs for public-web-server, internal-database, bastion-host, zero-trust-node.
- **Standardized exit codes**: 15 codes (0–61) with agent action mapping — backend conflicts, IaC management, confidence failures, approval mismatch, preflight/apply/verify failures. Full table in SKILL.md. Enables CI/CD branching decisions.
- **Plan approval gate**: `approval_token` (hash of plan content) required for APPLY step. Token mismatch → exit 41. Forces explicit confirmation before changes.
- **Interrupt-resume**: Optional state persistence (`~/.firewall-hardening/state.json`) records state machine position, backup path, and rollback timer ID — enables agent recovery after interruption without restarting from Detect.

## Usage Instructions

### 1. Run the audit script first
```bash
bash scripts/audit-firewall.sh
# Or for machine-readable output:
bash scripts/audit-firewall.sh --json
```
Detects the firewall stack, Docker, cloud provider, ownership manager, rollback capability. Outputs confidence score, risk tier, and halt reasons.

### 2. Plan before applying
```bash
bash scripts/firewall-plan.sh --profile public-web-server
bash scripts/firewall-plan.sh --ports 22,80,443
bash scripts/firewall-plan.sh --json     # Machine-readable diff
```
Review the output. If risk tier is `confirmed`, get human approval before proceeding.

### 3. Follow the state machine in SKILL.md

**Detect** → Determine backend path and risk tier from audit output.  
**Select** → Optionally load a security profile or define custom ruleset.  
**Plan** → Generate and review dry-run diff.  
**Validate** → Create backup, schedule rollback timer, complete pre-flight checklist.  
**Apply** → Use idempotent, atomic commands for your backend (see `references/backend-*.md`).  
**Verify** → Run the verification script:
```bash
bash scripts/firewall-verify.sh
```

### 4. For policy-as-code workflows
Define your intent in `references/declarative-policy.md` YAML format, then render it to your backend of choice. Validate against `references/policy-schema.json` before rendering.

### 5. Recovery (if connectivity is lost)
1. Wait for auto-rollback timer (scheduled during Validate state)
2. Use your second SSH session if still open
3. Cloud serial console (AWS/GCP/Azure)
4. Hypervisor console (VNC/IPMI/iDRAC)
5. Transaction rollback — restore from backup before emergency open (see `references/recovery.md`)
6. Emergency ACCEPT only as last resort (exposes host completely)

## File Map

| File | Purpose |
|------|---------|
| `SKILL.md` | Main playbook — state machine, decision tree, NEVER DO, quick reference (305 lines) |
| **Scripts** | |
| `scripts/audit-firewall.sh` | Environment detection, confidence scoring, risk tier, `--json` |
| `scripts/firewall-plan.sh` | Dry-run diff — shows rules to add/skip/remove, `--json` |
| `scripts/firewall-verify.sh` | Post-hardening verification checklist (8 checks) |
| **Backend References** | |
| `references/backend-ufw.md` | Full UFW phase commands |
| `references/backend-firewalld.md` | Full firewalld phase commands |
| `references/backend-nftables.md` | Full nftables phase commands (atomic ruleset) |
| `references/backend-iptables.md` | Full iptables phase commands (atomic restore) |
| **Domain References** | |
| `references/docker-hardening.md` | Docker firewall hardening (DOCKER-USER chain) |
| `references/k8s-policy.md` | Kubernetes node policy (CNI-specific, audit-only default) |
| `references/security-profiles.md` | Pre-built configs: web-server, db, bastion, zero-trust |
| `references/declarative-policy.md` | YAML policy schema v2.0 + backend renderers + golden fixtures |
| `references/observability.md` | Monitoring, conntrack, baselines, perf risks |
| `references/compliance.md` | CIS/PCI-DSS/SOC2 control mapping |
| `references/recovery.md` | Recovery procedures and rollback mechanics |
| `references/special-environments.md` | When NOT to use, containers, K8s, WSL2, exit codes |
| **Meta** | |
| `references/remaining-improvements.md` | Roadmap for future enhancements |
| `references/policy-schema.json` | JSON Schema for declarative policy validation |
| `problems.txt` | External review with rationale and scoring |

## Prerequisites

- Root or sudo access
- Linux host (Ubuntu/Debian/RHEL/Rocky/Alma/Fedora/Alpine/Arch)
- Active SSH session (or serial console access for remote hosts)
- One of: `ufw`, `firewalld`, `nftables`, or `iptables`
- Rollback capability: `at` (with `atd` running) or `systemd-run`

## Tags

`security`, `firewall`, `ufw`, `iptables`, `nftables`, `firewalld`, `hardening`, `docker`, `fail2ban`, `policy-as-code`, `devsecops`, `ipv6`

## Version

`skill_version: 2.2.0` | `schema_version: 2`

## Changelog

### v2.2.0 — SkillOpt Double-Epoch Optimization (2026-05-21)

Optimized via Microsoft SkillOpt ReflACT pipeline with Claude Opus 4.7 as optimizer, DeepSeek V4 as agent. Two epochs, 20 test cases (15 training + 5 held-out validation). Baseline: 20/20 functional. All patches were quality/documentation/correctness improvements — functionality remained 100% throughout.

**Epoch 1 (LR=0.7, 7 patches):**

| # | Priority | Issue | Fix |
|---|:--------:|-------|-----|
| 1 | P0 | Exit code tables diverged between SKILL.md and special-environments.md (21=K8s vs 21=Container swapped) | Synced special-environments.md to SKILL.md canonical table + added source-of-truth annotation |
| 2 | P0 | Rollback section referenced dead "see previous version" | Replaced with complete at/systemd-run scheduling script inline |
| 3 | P0 | VERIFY referenced non-existent `scripts/manual-rollback.sh` | Replaced with actual restore command sequence (iptables-restore → nft -f → ufw reset) |
| 4 | P1 | iptables/nftables/firewalld backend refs all hardcoded SSH port 22 | Added SSH_PORT detection preamble to all three non-UFW backends |
| 5 | P1 | Pre-flight "Second SSH session open and idle" unexplained | Expanded with verification step (`sudo whoami`) + conntrack survival explanation |
| 6 | P1 | remaining-improvements.md claimed state persistence both implemented AND not implemented | Clarified: schema documented but no auto-generation script exists |
| 7 | P2 | Locked-out operator had to read 3 sections for recovery steps | Added 🚨 Emergency quick-nav header after "When NOT to Use" |

**Epoch 2 (LR=0.3, 3 patches):**

| # | Priority | Issue | Fix |
|---|:--------:|-------|-----|
| 8 | P1 | Security profiles used `grep -q "22/tcp"` (substring match — false-positives on 8022/2200) | All UFW profiles upgraded to `awk '{print $1}' \| grep -qx` exact match (consistent with main SKILL.md APPLY section) |
| 9 | P1 | `firewall-verify.sh` exited code 1 on failure but SKILL.md exit code contract specifies 60 | Changed to `exit 60` + updated header comment |
| 10 | P2 | Security profiles: firewalld hardcoded `--add-service=ssh` (port 22), nftables had dead rate-limiting code (accept before limit rule) | Added SSH_PORT detection + branching; fixed nftables rule ordering (split web ports + rate-limited SSH) |

**Meta-learning from this optimization:**
- Epoch 1 caught doc↔doc inconsistencies (cross-file drift from iterative development)
- Epoch 2 caught code↔doc contract violations (implementation didn't match specification)
- Pattern: surface fixes reveal deeper structural issues — each epoch peels one layer

## Compatibility Matrix

| Distro/Env | ufw | firewalld | nftables | iptables | Coverage |
|------------|-----|-----------|----------|----------|----------|
| Ubuntu 22.04/24.04 | Primary | — | Backend | Fallback | Full |
| Debian 12 | Primary | — | Backend | Fallback | Full |
| RHEL 9 | — | Primary | Native | Backend | Full |
| Rocky/Alma 9 | — | Primary | Native | Backend | Full |
| Fedora 40+ | — | Primary | Native | Backend | Partial |
| Alpine 3.18+ | — | — | Native | Fallback | Partial |
| Arch | — | — | Native | Fallback | Community |
| Docker host | ✅ DOCKER-USER | ✅ `docker-hardening.md` | ✅ `docker-hardening.md` | ✅ `docker-hardening.md` | Full |
| LXC/LXD | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | Partial |
| WSL2 | ❌ | ❌ | ❌ | ❌ | None |

## Example Session

```bash
# Step 1: Detect (machine-readable)
$ bash scripts/audit-firewall.sh --json
{
  "confidence": 95,
  "risk_tier": "auto",
  "recommended_backend": "ufw",
  "ssh_port": 22,
  "at_available": false,
  "systemd_run_available": true,
  "halt_reasons": []
}

# Step 2: Plan (dry-run)
$ bash scripts/firewall-plan.sh --profile public-web-server
=== UFW Plan ===
Backend: ufw (active: Status: active)
Rules to be added:
  [SKIP] 22/tcp (already exists)
  [ADD]  80/tcp
  [ADD]  443/tcp

# Step 3: Validate (backup + rollback)
$ BACKUP_DIR="$HOME/firewall-backup-$(date +%Y%m%d-%H%M%S)"
$ mkdir -p "$BACKUP_DIR"
$ sudo iptables-save > "$BACKUP_DIR/iptables-v4.rules"
$ sudo nft list ruleset > "$BACKUP_DIR/nftables.rules"
$ systemd-run --on-active=5m --user sh -c "sudo iptables-restore < '$BACKUP_DIR/iptables-v4.rules'; sudo ufw disable"

# Step 4: Apply (idempotent ufw commands)
$ SSHP=$(ss -tlnp | grep sshd | awk -F: '{print $NF}' | head -1); SSHP=${SSHP:-22}
$ sudo ufw status | awk '{print $1}' | grep -qx "${SSHP}/tcp" || sudo ufw allow "${SSHP}/tcp"
$ sudo ufw status | awk '{print $1}' | grep -qx "80/tcp"  || sudo ufw allow 80/tcp
$ sudo ufw status | awk '{print $1}' | grep -qx "443/tcp" || sudo ufw allow 443/tcp
$ sudo ufw --force enable

# Step 5: Verify
$ bash scripts/firewall-verify.sh
All critical checks passed.

# Step 6: Cancel rollback
$ systemctl --user stop firewall-rollback-<pid>

# Step 7: Record baselines
$ cat /proc/sys/net/netfilter/nf_conntrack_count
$ sudo fail2ban-client status sshd
```

### firewalld / RHEL 9 Example

```bash
# Step 1: Detect
$ bash scripts/audit-firewall.sh --json
{
  "confidence": 93,
  "risk_tier": "auto",
  "recommended_backend": "firewalld",
  "default_zone": "public",
  "at_available": true,
  "halt_reasons": []
}

# Step 2: Plan
$ bash scripts/firewall-plan.sh --profile public-web-server
=== firewalld Plan ===
Backend: firewalld (default zone: public)
Services to add:
  [SKIP] ssh (already enabled)
  [ADD]  http
  [ADD]  https
Rich rules: none needed

# Step 3: Validate
$ BACKUP_DIR="$HOME/firewall-backup-$(date +%Y%m%d-%H%M%S)"
$ mkdir -p "$BACKUP_DIR"
$ sudo firewall-cmd --list-all --zone=public > "$BACKUP_DIR/firewalld-default.txt"

# Step 4: Apply (idempotent firewalld)
$ sudo firewall-cmd --query-service=http  || sudo firewall-cmd --permanent --add-service=http
$ sudo firewall-cmd --query-service=https || sudo firewall-cmd --permanent --add-service=https
$ sudo firewall-cmd --reload

# Step 5: Verify + Cancel rollback
$ bash scripts/firewall-verify.sh
```

## Never Do (Safety Guardrails — 14 Rules)

1. **Never flush iptables/nftables on Kubernetes nodes.** CNI plugins manage netfilter rules. Use NetworkPolicies.
2. **Never run `iptables -F` or `nft flush ruleset` without a verified backup and a second session.**
3. **Never disable firewalld and use raw iptables simultaneously.** Undefined behavior.
4. **Never set `DROP` policy on INPUT before allowing your current SSH port.**
5. **Never disable Docker's `iptables` management without replacement NAT/routing rules.**
6. **Never restart `networking.service` or `NetworkManager` remotely without console/serial access.**
7. **Never apply cloud security group changes and host firewall changes simultaneously without testing.**
8. **Never enable logging on high-traffic DROP rules without `limit rate`.**
9. **Never manage nftables/iptables directly when ufw or firewalld owns the policy.** Split-brain state.
10. **Never apply outbound default-deny without explicitly allowing DNS, NTP, package mirrors, monitoring agents, and IaC agents.**
11. **Never restore firewall backups from a different host, kernel version, or backend mode.**
12. **Never assume IPv4 rules protect IPv6.** Verify both stacks independently.
13. **Never change sysctl network hardening values on Kubernetes/CNI hosts without explicit profile support.**
14. **Never enable verbose packet logging without rate limits and log rotation.**

## See Also

- `man ufw` / `man iptables` / `man ip6tables` / `man nft` / `man firewall-cmd`
- [Ubuntu UFW Community Docs](https://help.ubuntu.com/community/UFW)
- [firewalld Documentation](https://firewalld.org/documentation/)
- [nftables Wiki](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page)
- `references/backend-ufw.md` — Full UFW phase
- `references/backend-firewalld.md` — Full firewalld phase
- `references/backend-nftables.md` — Full nftables phase
- `references/backend-iptables.md` — Full iptables phase
- `references/security-profiles.md` — Pre-built hardened configurations
- `references/declarative-policy.md` — YAML policy schema v2.0
- `references/special-environments.md` — When NOT to use, exit codes

## License

Dual-licensed under MIT OR Apache-2.0.
