---
name: linux-firewall-hardening
title: Linux Firewall Hardening
description: Safe Linux firewall hardening with backend detection, idempotent atomic rules, rollback protection, and AI-executable state-machine workflows. Covers ufw, firewalld, nftables, iptables, Docker, Kubernetes CNI awareness, and fail2ban with compliance mapping to CIS/PCI-DSS/SOC2.
license: Dual MIT / Apache-2.0
skill_version: 2.5.0
schema_version: 2
tags: [security, firewall, ufw, iptables, nftables, firewalld, hardening, docker, fail2ban, policy-as-code, devsecops, ipv6]
---

# Linux Firewall Hardening

## When to Use

- Check if a Linux server has active firewall protection.
- Enable and configure a firewall without locking yourself out of SSH.
- Audit existing rules, troubleshoot connectivity, or apply a security profile.
- Automate firewall hardening via an AI agent or CI/CD pipeline.

## When NOT to Use

| Condition | Alternative |
|-----------|-------------|
| Kubernetes worker node | Use NetworkPolicies / CiliumNetworkPolicy |
| Firewall managed by Terraform/Ansible/Puppet/Chef | Update IaC source of truth |
| Cloud workload with Security Group / NSG only | Use cloud provider's firewall API |
| Inside a container | Escalate to host operator |
| WSL2, macOS, or shared/managed hosting | See `references/special-environments.md` |

> **Support files**: `scripts/audit-firewall.sh` (run first), `scripts/firewall-plan.sh` (dry-run), `scripts/firewall-verify.sh` (post-apply).
> Detailed backend guides, Docker/K8s policies, observability, compliance, and recovery are in `references/`.

## 🚨 Emergency: I'm Locked Out — What Now?

If you just applied firewall rules and lost SSH connectivity:

1. **Wait 5 minutes** — the auto-rollback timer (scheduled during VALIDATE) will restore access. Don't panic and don't take destructive actions.
2. **Use your second SSH session** — if you opened one (pre-flight checklist), switch to it and fix the rules manually.
3. **Cloud serial console** — AWS EC2 Serial Console, GCP Serial Port, Azure Serial Console, or hypervisor VNC/IPMI/iDRAC.
4. **Restore from backup via console** — once connected: `sudo iptables-restore < ~/firewall-backup-*/iptables-v4.rules`
5. **Emergency ACCEPT (LAST RESORT)** — `sudo iptables -P INPUT ACCEPT; sudo iptables -F; sudo ufw disable`. This exposes the host completely. Re-harden immediately.

Full procedures: `references/recovery.md`.

---

## Prerequisites

- Root or sudo access.
- An active SSH session (risk of lockout).
- Know which ports your services use.

---

## NEVER DO (14 Rules)

1. **Never flush iptables/nftables on Kubernetes nodes.** CNI plugins manage netfilter.
2. **Never run `iptables -F` or `nft flush ruleset` without a verified backup.** Docker/K8s networking will break.
3. **Never disable firewalld and use raw iptables simultaneously.** Undefined behavior.
4. **Never set `DROP` policy on INPUT before allowing your current SSH port.** Immediate lockout.
5. **Never disable Docker's `iptables` management without replacement NAT/routing rules.**
6. **Never restart `networking.service` or `NetworkManager` remotely without console access.**
7. **Never apply cloud SG and host firewall changes simultaneously without testing.**
8. **Never enable logging on high-traffic DROP rules without `limit rate`.** Disk flood.
9. **Never manage nftables/iptables directly when ufw or firewalld owns the policy.** Split-brain state.
10. **Never apply outbound default-deny without explicitly allowing DNS, NTP, package mirrors.**
11. **Never restore firewall backups from a different host, kernel version, or backend mode.**
12. **Never assume IPv4 rules protect IPv6.** Verify both stacks separately.
13. **Never change sysctl hardening values on K8s/CNI hosts without explicit CNI profile support.**
14. **Never enable verbose packet logging without rate limits and log rotation.**

---

## State Machine

Follow states in order. Do not skip.

```
DETECT → SELECT → PLAN → VALIDATE → APPLY → VERIFY
```

### State: DETECT

Run the audit script:

```bash
bash scripts/audit-firewall.sh           # Human-readable
bash scripts/audit-firewall.sh --json    # Machine-readable
```

**Key outputs**: `confidence`, `risk_tier`, `recommended_backend`, `halt_reasons`, `k8s_node`, `iac_owner`.

### Risk Tiers & Confidence Gating

| Tier | Confidence | Agent Behavior |
|------|-----------|----------------|
| `auto` | ≥ 90% | Proceed automatically to PLAN |
| `confirmed` | 70–89% | Proceed but require human confirmation before APPLY |
| `manual` | 50–69% | Audit-only mode. Generate recommendations, do not apply. |
| `halt` | < 50% | Stop immediately. Escalate findings to operator. |

**Additional halt triggers** (regardless of confidence): containerized, K8s node, IaC managed, no rollback mechanism available.

### Decision Tree

| Condition | Path | Detail |
|-----------|------|--------|
| Risk tier = `halt` | **STOP** | Resolve blockers first |
| Inside container | **STOP** | Escalate to host operator |
| K8s node detected | **STOP** | `references/k8s-policy.md` |
| Ubuntu/Debian + ufw active | **Phase: UFW** | `references/backend-ufw.md` |
| ufw + firewalld both active | **STOP** | Resolve conflict |
| RHEL/Rocky/Alma + firewalld active | **Phase: firewalld** | `references/backend-firewalld.md` |
| nftables active, no frontend | **Phase: nftables** | `references/backend-nftables.md` |
| iptables only | **Phase: iptables** | `references/backend-iptables.md` |
| Docker host | Apply **Docker Hardening** after phase above | `references/docker-hardening.md` |

### Ownership Boundary

Before modifying rules, verify no IaC tool manages the firewall. If Terraform/Ansible/Puppet/Chef/cloud-init is detected → do not mutate. Update the source of truth instead. Full detection logic is in `scripts/audit-firewall.sh`.

---

### State: SELECT

Optionally load a pre-built security profile (`references/security-profiles.md`):

| Profile | Use Case |
|---------|----------|
| `public-web-server` | Open 22, 80, 443. Rate-limit SSH. |
| `internal-database` | SSH from mgmt subnet only. DB port from app subnet only. |
| `bastion-host` | SSH only. Aggressive rate limiting. |
| `zero-trust-node` | Default deny all inbound and outbound. |

Or use declarative YAML (`references/declarative-policy.md`):

```
Imperative (state machine) → Ad-hoc hardening, incident response
Declarative (YAML)        → GitOps, multi-host, reproducible
Mixed                     → YAML as source-of-truth, state machine for verification
```

---

### State: PLAN

Generate a dry-run diff before applying:

```bash
bash scripts/firewall-plan.sh --profile public-web-server
bash scripts/firewall-plan.sh --ports 22,80,443
bash scripts/firewall-plan.sh --json     # Machine-readable diff with approval_token
bash scripts/firewall-plan.sh --refresh-audit --json  # Force re-audit + plan
```

Review the output. If `risk_tier` is `confirmed`, present the plan and wait for human confirmation before APPLY.

**Plan JSON schema** (matches `firewall-plan.sh --json` output):

```json
{
  "backend": "ufw",
  "active_frontend": "ufw",
  "profile": "public-web-server",
  "target_ports": [22, 80, 443],
  "diff": {
    "add":    [{"port": 80, "proto": "tcp", "source": "any"}],
    "skip":   [{"port": 22, "proto": "tcp", "reason": "already_exists"}],
    "remove": []
  },
  "risk_assessment": "low",
  "estimated_disruption": "none",
  "approval_token": "sha256:abc123...",
  "audit_cached": false,
  "audit_cache_file": "/tmp/firewall-audit.json"
}
```

**Approval gate:** PLAN output includes an `approval_token` (hash of plan content). APPLY must be called with `--approved-plan=<token>`. Token mismatch → exit code 41. This forces explicit human confirmation before Apply.

**Audit caching:** `firewall-plan.sh` internally calls `audit-firewall.sh --json` and caches to `/tmp/firewall-audit.json` (TTL 5 min). Use `--refresh-audit` to force refresh.

---

### State: VALIDATE

#### 1. Create Backup (Mandatory)

```bash
BACKUP_DIR="$HOME/firewall-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

sudo iptables-save > "$BACKUP_DIR/iptables-v4.rules" 2>/dev/null || true
sudo ip6tables-save > "$BACKUP_DIR/iptables-v6.rules" 2>/dev/null || true
sudo nft list ruleset > "$BACKUP_DIR/nftables.rules" 2>/dev/null || true
sudo ufw status verbose > "$BACKUP_DIR/ufw-status.txt" 2>/dev/null || true
sudo firewall-cmd --list-all --zone=$(sudo firewall-cmd --get-default-zone) > "$BACKUP_DIR/firewalld-default.txt" 2>/dev/null || true

echo "Backup saved to $BACKUP_DIR"
```

#### 2. Schedule Rollback (Mandatory for Remote)

The rollback restores from backup — not just disables the firewall — so Docker NAT and pre-existing rules are preserved. Dual-backend: `at` preferred, `systemd-run` fallback.

```bash
# Build rollback script from backup dir
ROLLBACK_SCRIPT=$(cat <<'RB'
#!/bin/bash
BACKUP_DIR="REPLACE_ME"
[ -f "$BACKUP_DIR/iptables-v4.rules" ] && sudo iptables-restore < "$BACKUP_DIR/iptables-v4.rules" || { sudo iptables -P INPUT ACCEPT; sudo iptables -F; }
[ -f "$BACKUP_DIR/iptables-v6.rules" ] && sudo ip6tables-restore < "$BACKUP_DIR/iptables-v6.rules" || { sudo ip6tables -P INPUT ACCEPT; sudo ip6tables -F; }
[ -f "$BACKUP_DIR/nftables.rules" ] && sudo nft -f "$BACKUP_DIR/nftables.rules" || sudo nft flush ruleset
systemctl is-active ufw &>/dev/null && sudo ufw disable
sudo firewall-cmd --panic-off 2>/dev/null
RB
)
ROLLBACK_SCRIPT="${ROLLBACK_SCRIPT/REPLACE_ME/$BACKUP_DIR}"

# Schedule (at preferred, systemd-run fallback)
if command -v at &>/dev/null; then
    ROLLBACK_JOB_ID=$(echo "sudo bash -c '$ROLLBACK_SCRIPT'" | at now + 5 minutes 2>&1 | grep -oP 'job \K\d+')
    echo "Rollback scheduled: at job $ROLLBACK_JOB_ID (cancel with: atrm $ROLLBACK_JOB_ID)"
elif command -v systemd-run &>/dev/null; then
    UNIT_NAME="firewall-rollback-$$"
    echo "$ROLLBACK_SCRIPT" > /tmp/firewall-rollback-$$.sh
    chmod +x /tmp/firewall-rollback-$$.sh
    systemd-run --on-active=5m --unit="$UNIT_NAME" --user /tmp/firewall-rollback-$$.sh
    echo "Rollback scheduled: systemd unit $UNIT_NAME (cancel with: systemctl --user stop $UNIT_NAME)"
fi
```

See `references/recovery.md` for advanced recovery scenarios.

#### 3. Pre-Flight Checklist

- [ ] Backup created successfully
- [ ] Rollback scheduled (verify with `atq` or `systemctl --user list-units`)
- [ ] **Second SSH session open and tested** — open a second terminal, SSH in, and confirm you can run `sudo whoami`. This is your emergency console if the primary session loses connectivity. Keep it open until VERIFY passes. **Why**: existing ESTABLISHED conntrack entries usually keep your current session alive, but if conntrack is flushed or the policy change drops your session silently, this second session is your only way back in.
- [ ] Real SSH port identified (not assumed to be 22)
- [ ] Confidence ≥ 70% and risk_tier is `auto` or `confirmed`
- [ ] Ownership verified — no IaC managing firewall
- [ ] Change window appropriate (maintenance window or low traffic)
- [ ] PLAN output reviewed and approved

---

### State: APPLY

Apply firewall rules using the approved plan from PLAN state.

```bash
# Get the approval_token from firewall-plan.sh --json output
bash scripts/firewall-apply.sh --approved-plan=sha256:abc123...
bash scripts/firewall-apply.sh --approved-plan=sha256:abc123... --dry-run
```

**Apply behavior:**
- Verifies `approval_token` matches current plan (exit 41 on mismatch — plan changed since approval)
- Checks for active rollback timer (exit 40 if VALIDATE was skipped)
- Supports all backends: ufw, firewalld, nftables, iptables
- Automatically runs `firewall-verify.sh` after applying
- Passes `--dry-run` for preview-only mode

**Idempotent inline commands** (for manual/scriptless use):

| Backend | Pattern |
|---------|---------|
| ufw | `sudo ufw status \| awk '{print $1}' \| grep -qx "22/tcp" \|\| sudo ufw allow 22/tcp` |
| firewalld | `sudo firewall-cmd --query-service=ssh \|\| sudo firewall-cmd --permanent --add-service=ssh` |
| iptables | `sudo iptables -C INPUT -p tcp --dport 22 -j ACCEPT 2>/dev/null \|\| sudo iptables -A ...` |
| nftables | Atomic ruleset: `nft -c -f /etc/nftables.conf.new && nft -f /etc/nftables.conf.new` |

#### Docker Hosts

Docker bypasses ufw by default. Use DOCKER-USER chain. Full guide: `references/docker-hardening.md`.

#### Kubernetes Nodes

**Default: AUDIT-ONLY**. Never modify host firewall. Full policy: `references/k8s-policy.md`.

---

### State: VERIFY

Run post-hardening checks:

```bash
bash scripts/firewall-verify.sh
```

**Success criteria** (all must pass):
1. SSH remains reachable from current and second session
2. Only intended ports are externally reachable
3. Rules survive reboot (verified via service persistence)
4. IPv6 exposure matches IPv4 policy
5. Docker-published ports are intentional (no accidental `0.0.0.0`)
6. fail2ban jails active (if installed) with correct backend
7. Rollback timer cancelled after successful verification

**Verify behavior contract:**
- Verify MUST complete within the rollback timer window (default 5 min)
- If verify times out before completion → timer auto-fires rollback (system-level protection)
- If verify FAILS but timer was already cancelled → manual rollback from the backup directory. Restore commands (in priority order):
  1. `sudo iptables-restore < "$BACKUP_DIR/iptables-v4.rules"`
  2. `sudo ip6tables-restore < "$BACKUP_DIR/iptables-v6.rules"`
  3. `sudo nft -f "$BACKUP_DIR/nftables.rules"`
  4. `sudo ufw reset && sudo ufw disable`
  See `references/recovery.md` for full recovery procedures including emergency ACCEPT fallback.
- The rollback is triggered by the timer (systemd-run/at), NOT by verify.sh itself — verify.sh exits with code 60 to signal failure, and the calling agent/scheduler handles the rollback decision

## Exit Codes (Core Contract)

| Code | Meaning | Agent Action |
|------|---------|-------------|
| 0 | Success | Continue |
| 10 | Backend conflict | Halt; resolve manually |
| 11 | Backend detection failed | Halt; check firewall stack |
| 12 | Multiple backends active | Halt; resolve conflict |
| 20 | IaC-managed | Halt; update IaC source |
| 21 | Inside container | Halt; escalate to host operator |
| 22 | K8s node detected | Halt; audit-only mode |
| 30 | Low confidence (<70%) | Drop to audit-only mode |
| 31 | No rollback capability | Halt; ensure at or systemd-run |
| 40 | Preflight failed | Halt; check prerequisites |
| 41 | Plan approval mismatch | Halt; re-run PLAN with approval |
| 42 | RESERVED (Backup failed) | Halt; resolve disk/permissions |
| 50 | RESERVED (Apply failed) | Auto-rollback triggered |
| 51 | Apply partial | Auto-rollback triggered; verify backup |
| 60 | Verify failed | Auto-rollback triggered |
| 61 | RESERVED (State file conflict) | Abort; resolve stale state |

---

## fail2ban Integration

If fail2ban is installed:

| Host Firewall | Recommended `backend` |
|--------------|----------------------|
| ufw | `ufw` or `systemd` |
| firewalld | `firewalld` |
| nftables | `nftables` |
| iptables | `auto` (default) |

After changing backend: `sudo fail2ban-client restart && sudo fail2ban-client status sshd`.

---

## Recovery

If you lose connectivity, priority order:
1. Wait for auto-rollback (scheduled during VALIDATE)
2. Use second SSH session
3. Cloud serial console / hypervisor console
4. Restore from backup
5. Emergency ACCEPT (last resort — exposes host completely)

Full procedures: `references/recovery.md`.

## State Persistence & Interrupt-Resume

For agent interrupt-resume scenarios (e.g., Apply failed mid-run, agent restarted), the state machine writes a lightweight state file to enable recovery without starting from Detect:

```bash
STATE_DIR="$HOME/.firewall-hardening"
STATE_FILE="$STATE_DIR/state.json"
```

**State file structure:**

```json
{
  "state": "validate",
  "started_at": "2026-05-11T16:00:00Z",
  "backend": "ufw",
  "risk_tier": "auto",
  "backup_dir": "/home/user/firewall-backup-20260511-160000",
  "rollback_timer_id": "firewall-rollback-12345",
  "plan_hash": "sha256:abc123..."
}
```

**Resume logic:**
- If `state.json` exists and `started_at` is within 1 hour → resume from that state
- If `state.json` is stale (>1 hour) → delete it and start fresh from Detect
- The file is advisory-only; agent can always restart from Detect

> State persistence is optional. The skill defaults to restarting from Detect each run. Enable by creating `$STATE_DIR` before starting.

---

## Cloud Security Group Reminder

The host firewall is your **second** layer. Verify cloud SGs are aligned:

| Cloud | Outer Firewall |
|-------|---------------|
| AWS | Security Groups |
| GCP | VPC Firewall Rules |
| Azure | Network Security Groups |
| DigitalOcean/Linode/Vultr | Cloud Firewall |

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
| Docker host | ✅ DOCKER-USER chain | ✅ `docker-hardening.md` | ✅ `docker-hardening.md` | ✅ `docker-hardening.md` | Full |
| LXC/LXD container | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | Partial |
| systemd-nspawn | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | Partial |
| WSL2 | ❌ Not supported | ❌ Not supported | ❌ Not supported | ❌ Not supported | None |

> Container environments: Docker host is fully supported via DOCKER-USER chain. LXC/LXD/systemd-nspawn have limited support (kernel shares netfilter with host). WSL2 is explicitly unsupported. See `references/special-environments.md`.

---

## Observability

Establish baselines after hardening: conntrack usage, dropped packet rates, fail2ban ban rate. Monitor for anomalies. Full guide: `references/observability.md`.

## Compliance

Practices map to CIS, PCI-DSS, and SOC2 controls. Full mapping: `references/compliance.md`.

## Quick Reference

| Task | Command |
|------|---------|
| Audit environment | `bash scripts/audit-firewall.sh --json` |
| Plan changes | `bash scripts/firewall-plan.sh --profile web` |
| Verify after apply | `bash scripts/firewall-verify.sh` |
| Allow port (ufw, idempotent) | `sudo ufw status \| awk '{print $1}' \| grep -qx "80/tcp" \|\| sudo ufw allow 80/tcp` |
| View ufw rules | `sudo ufw status numbered` |
| View nft rules | `sudo nft list ruleset` |
| View iptables rules | `sudo iptables -L -n -v` |
| View ip6tables rules | `sudo ip6tables -L -n -v` |
| Atomic iptables replace | `sudo iptables-restore < /tmp/rules.v4` |
| Dry-run nftables | `sudo nft -c -f /etc/nftables.conf` |
| Backup rules | `sudo iptables-save > ~/iptables.backup` |
| fail2ban status | `sudo fail2ban-client status sshd` |
| Cancel rollback (at) | `atrm <jobid>` |
| Cancel rollback (systemd-run) | `systemctl --user stop firewall-rollback-<pid>` |

## See Also

- `references/backend-ufw.md` — Full UFW phase
- `references/backend-firewalld.md` — Full firewalld phase
- `references/backend-nftables.md` — Full nftables phase
- `references/backend-iptables.md` — Full iptables phase
- `references/docker-hardening.md` — Docker firewall hardening
- `references/k8s-policy.md` — Kubernetes node policy
- `references/security-profiles.md` — Pre-built configurations
- `references/declarative-policy.md` — YAML policy schema
- `references/observability.md` — Monitoring and baselines
- `references/compliance.md` — CIS/PCI-DSS/SOC2 mapping
- `references/recovery.md` — Recovery procedures
- `references/special-environments.md` — WSL2, containers, exit codes
- `scripts/audit-firewall.sh` — Environment detection
- `scripts/firewall-plan.sh` — Dry-run diff
- `scripts/firewall-verify.sh` — Post-apply verification
