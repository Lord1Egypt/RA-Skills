# Module 20 — systemd-analyze Security Audit

> **Purpose:** Assess per-service sandboxing via systemd-analyze security. Single command covers 80+ security settings per service. Exposes misconfigured ProtectSystem, NoNewPrivileges, PrivateTmp, and other systemd hardening directives.

## Prerequisite
```bash
# Check if systemd is the init system
[ -d /run/systemd/system ] || { echo "Not systemd — module skip"; exit 0; }
```

## Commands
```bash
# Full security analysis of all running services (JSON output for parsing)
systemd-analyze security --json=short 2>/dev/null

# Per-service detailed view (pick services with low scores)
systemd-analyze security <unit-name> 2>/dev/null

# Quick check: list services with exposure level
systemd-analyze security --json=short 2>/dev/null | python3 -c "
import json, sys
data = json.load(sys.stdin)
for unit in data:
    score = unit.get('exposure', unit.get('score', 999))
    name = unit.get('unit', unit.get('id', 'unknown'))
    if score is not None and score > 5.0:
        print(f'{score:.1f} | {name}')
" 2>/dev/null || systemd-analyze security 2>/dev/null | head -60

# List all running services
systemctl list-units --type=service --state=running --no-legend | awk '{print $1}'
```

## Key Hardening Directives to Check

| Directive | Secure Value | What It Does |
|-----------|-------------|-------------|
| ProtectSystem | `full` or `strict` | Read-only access to /usr and /etc |
| ProtectHome | `true` or `read-only` | Prevents access to /home, /root |
| PrivateTmp | `true` | Service gets private /tmp (no sharing) |
| NoNewPrivileges | `true` | Prevents privilege escalation via SUID |
| PrivateDevices | `true` | No access to physical devices |
| ProtectKernelTunables | `true` | No access to /proc/sys, /sys |
| ProtectKernelModules | `true` | Can't load/unload kernel modules |
| ProtectKernelLogs | `true` | Can't access kernel log buffer |
| ProtectControlGroups | `true` | Can't modify cgroup hierarchy |
| ProtectHostname | `true` | Can't change hostname |
| ProtectClock | `true` | Can't change system clock |
| RestrictAddressFamilies | `AF_UNIX AF_INET AF_INET6` | Limit socket families |
| RestrictNamespaces | `~CLONE_NEWUSER CLONE_NEWNET` | Block namespace creation |
| LockPersonality | `true` | Prevents changing execution domain |
| MemoryDenyWriteExecute | `true` | W^X policy (no writable+exec memory) |
| RestrictRealtime | `true` | Prevents real-time scheduling |
| RestrictSUIDSGID | `true` | Prevents SUID/SGID creation |
| RemoveIPC | `true` | Clean up IPC objects on exit |
| PrivateUsers | `true` | User namespace isolation |
| CapabilityBoundingSet | `~CAP_SYS_ADMIN ...` | Drop unnecessary capabilities |
| AmbientCapabilities | `""` or empty | No ambient capabilities |
| UMask | `027` or `077` | Restrictive file creation mask |
| SystemCallFilter | `~@privileged @mount ...` | Restrict allowed syscalls |
| SystemCallArchitectures | `native` | Block 32-bit syscalls on 64-bit |
| IPAddressDeny | `any` | Block all network access (if not needed) |
| DeviceAllow | `/dev/null rw` (minimal) | Restrict device access |

## Exposure Score Interpretation

| Score | Risk Level | Action |
|-------|-----------|--------|
| 0.0–2.0 | 🟢 SAFE | Well-sandboxed service, no action |
| 2.1–4.0 | 🟡 MEDIUM | Review hardening directives |
| 4.1–6.0 | 🟠 HIGH | Significant exposure, queue fix |
| 6.1–9.9 | 🔴 CRITICAL | Almost no sandboxing, harden ASAP |

## Checks & Findings

### High Exposure Services
- Any service with exposure score > 5.0 → HIGH (flag for hardening)
- Services exposed to network (bound to 0.0.0.0) with high exposure → CRITICAL

### Missing Critical Directives
- NoNewPrivileges=no → HIGH for network-facing services
- ProtectSystem=no or ProtectSystem=full (not strict) → MEDIUM
- PrivateTmp=no → MEDIUM
- MemoryDenyWriteExecute=no → HIGH (W^X violation)
- ProtectHome=no → MEDIUM for services running as root
- RestrictAddressFamilies not set → MEDIUM for network services

### Custom vs Vendor Default
- Services installed from repos → compare against known-good template
- Custom services → evaluate based on exposure score

## Auto-Fix Eligible
- None (service unit files are package-managed or custom — modifying without knowing the service's needs can break it)
- All issues → advisory/report only, confirm required before any override drop-in

## Override Drop-in Template (per service)
For confirmed fixes, create drop-in snippet (doesn't modify original unit):

```bash
mkdir -p /etc/systemd/system/<service>.service.d/
cat > /etc/systemd/system/<service>.service.d/security-hardening.conf << 'EOF'
[Service]
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/<app> /var/log/<app>
MemoryDenyWriteExecute=yes
RestrictRealtime=yes
RestrictSUIDSGID=yes
RemoveIPC=yes
EOF
systemctl daemon-reload
systemctl restart <service>
```

## Output Format
```
[CRITICAL] 20-systemd: high_exposure | service: nginx | exposure: 8.2 | needs hardening | action_id: ACT-YYYYMMDD-XXX
[HIGH] 20-systemd: missing_nnp | service: mysqld | NoNewPrivileges=no | exposure: 6.5 | action_id: ACT-YYYYMMDD-XXX
[HIGH] 20-systemd: w_x_violation | service: redis | MemoryDenyWriteExecute=no | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 20-systemd: missing_privatetmp | service: apache2 | PrivateTmp=no | action_id: ACT-YYYYMMDD-XXX
[PASS] 20-systemd: well_sandboxed | service: sshd | exposure: 0.8 ✓
[INFO] 20-systemd: summary | 12 services checked | 3 HIGH | 5 MEDIUM | 4 SAFE
```
