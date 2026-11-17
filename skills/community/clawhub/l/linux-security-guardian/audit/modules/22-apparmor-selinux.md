# Module 22 — AppArmor / SELinux Audit

> **Purpose:** Audit Mandatory Access Control (MAC) status. AppArmor (Debian/Ubuntu) or SELinux (RHEL/CentOS/Fedora) provide kernel-level process confinement. Without MAC, a compromised service can access everything its user can read.

## Prerequisite Check
```bash
# Determine which MAC system is in use
if command -v aa-status >/dev/null 2>&1; then
  echo "MAC_TYPE=apparmor"
elif command -v sestatus >/dev/null 2>&1; then
  echo "MAC_TYPE=selinux"
else
  echo "MAC_TYPE=none"
fi
```

## AppArmor Commands
```bash
# Check AppArmor status
aa-status 2>/dev/null || echo "apparmor_not_installed"

# List loaded profiles (confined vs unconfined)
aa-status 2>/dev/null | grep -A20 "profiles are loaded" | head -25

# Check processes in enforce mode vs complain mode
aa-status 2>/dev/null | grep -E "processes are|profiles are|enforce|complain"

# Check if AppArmor is enabled in kernel
cat /sys/module/apparmor/parameters/enabled 2>/dev/null || echo "apparmor_module_not_loaded"

# List unconfined processes (processes with no AppArmor profile)
aa-unconfined 2>/dev/null | head -20 || aa-status 2>/dev/null | grep -A50 "unconfined"

# Check AppArmor parser
which apparmor_parser 2>/dev/null && dpkg -l apparmor 2>/dev/null | grep "^ii"
```

## SELinux Commands
```bash
# Check SELinux status
sestatus 2>/dev/null || echo "selinux_not_installed"

# Get enforcing mode
getenforce 2>/dev/null

# List SELinux booleans
getsebool -a 2>/dev/null | head -20

# Check SELinux policy
semodule -l 2>/dev/null | head -20

# Audit denials
ausearch -m avc -ts recent 2>/dev/null | tail -20
```

## Checks & Findings

### No MAC System Installed
- Neither AppArmor nor SELinux installed → **HIGH** (no process confinement)

### AppArmor Specific
| Check | Severity if Failed |
|-------|-------------------|
| AppArmor module not loaded (enabled=Y missing) | **CRITICAL** |
| AppArmor installed but service stopped | **HIGH** |
| > 5 processes in complain mode (logging only) | **MEDIUM** |
| > 50% processes unconfined | **HIGH** |
| No custom profiles (only vendor defaults) | **MEDIUM** |
| Docker containers running without AppArmor profile | **HIGH** |

### SELinux Specific
| Check | Severity if Failed |
|-------|-------------------|
| getenforce = Disabled | **HIGH** |
| getenforce = Permissive (logging only) | **MEDIUM** |
| SELinux installed but service error | **HIGH** |
| Many AVC denials in audit log | **MEDIUM** (check if legitimate) |

### Docker + AppArmor
- Docker uses AppArmor `docker-default` profile by default
- Check: `docker info 2>/dev/null | grep -i "apparmor"`
- If AppArmor not loaded but Docker running → **HIGH**

## Recommended States

### For Debian/Ubuntu (AppArmor)
```
aa-status → "apparmor module is loaded"
aa-status → "X profiles are loaded, Y profiles are in enforce mode"
aa-status → "Z processes are confined by AppArmor"
```

### For RHEL/CentOS (SELinux)
```
sestatus → "SELinux status: enabled"
sestatus → "Current mode: enforcing"
getenforce → "Enforcing"
```

## Auto-Fix Eligible
- AppArmor not installed → `apt-get install -y apparmor apparmor-profiles apparmor-utils` (confirm required)
- AppArmor module not loaded → check kernel boot params (`apparmor=1 security=apparmor`) — confirm + reboot required

## Docker AppArmor Template
For containers without explicit profiles, Docker applies `docker-default`:
```bash
# Verify Docker AppArmor integration
docker info 2>/dev/null | grep -A2 "Security Options"
# Expected: "  apparmor"
```

## Output Format
```
[HIGH] 22-mac: no_mac_installed | Neither AppArmor nor SELinux installed | all processes unconfined | action_id: ACT-YYYYMMDD-XXX
[CRITICAL] 22-mac: apparmor_module_disabled | /sys/module/apparmor/parameters/enabled = N | action_id: ACT-YYYYMMDD-XXX
[HIGH] 22-mac: high_unconfined | 60% processes unconfined (18/30) | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 22-mac: complain_profiles | 8 profiles in complain mode (not enforcing) | action_id: ACT-YYYYMMDD-XXX
[PASS] 22-mac: apparmor_enforcing | 22 profiles loaded, 22 in enforce mode, 28 processes confined ✓
[INFO] 22-mac: summary | MAC: AppArmor | profiles: 22 enforce, 0 complain | processes: 28/30 confined (93%)
```
