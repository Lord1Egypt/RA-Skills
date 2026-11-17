# Module 23 — /proc hidepid Enforcement

> **Purpose:** Audit whether `/proc` is mounted with `hidepid=2` to prevent users from seeing each other's processes. Without hidepid, any user can `ps aux` and see all processes, command-line arguments (which may contain passwords/tokens), and process environments.

## Background
- **hidepid=0** (default): Everyone sees everything — no protection
- **hidepid=1**: Users only see their own processes; root sees all
- **hidepid=2**: Users only see their own processes; `/proc/PID/` entries hidden from other users. Most secure.
- **gid=** option: Members of this group can still see all processes (e.g., monitoring user)

## Commands
```bash
# Check /proc mount options
mount | grep "proc on /proc" 

# Check hidepid status
cat /proc/mounts | grep proc | head -5

# Alternative: check via findmnt
findmnt /proc -o OPTIONS 2>/dev/null || mount | grep "proc on /proc"

# Check if hidepid=2 is active
mount | grep "proc on /proc" | grep "hidepid=2" && echo "HIDEPID_ENFORCED" || echo "HIDEPID_MISSING"

# Verify by checking if non-root user can see other processes
# (Run as non-root test; if this returns data, hidepid is NOT working)
sudo -u nobody ps aux 2>/dev/null | wc -l || echo "cannot_test"

# Check systemd proc-sys-fs-binfmt_misc.automount (sometimes overrides /proc options)
systemctl list-units --type=mount | grep proc

# Check /etc/fstab for persistent /proc mount options
grep "proc" /etc/fstab 2>/dev/null || echo "proc_not_in_fstab"
```

## Checks & Findings

| Condition | Severity | Detail |
|-----------|----------|--------|
| hidepid=0 or missing | **HIGH** | All users see all processes — passwords in `ps aux` visible |
| hidepid=1 | **MEDIUM** | Basic protection but /proc/PID still browsable via `ls /proc` |
| hidepid=2 with gid= | **LOW (Pass)** | Best practice; monitoring group can still see |
| hidepid=2 without gid= | **PASS** | Maximum isolation |
| /proc mount using `defaults` in fstab | **HIGH** | Not explicitly set; defaults to hidepid=0 |
| GID for monitoring group not set | **MEDIUM** | If hidepid=2 but no gid= set, even monitoring tools break |

## Practical Impact
Without hidepid=2:
```bash
# Any user can see these sensitive things:
ps aux | grep mysql    # Database passwords in command line
cat /proc/1/environ    # Environment variables of PID 1
ls -la /proc/*/cmdline # All running commands
```

With hidepid=2:
```bash
# Non-root users only see:
ps aux    # Only their own processes
ls /proc  # Only their own PID directories
```

## Auto-Fix Eligible (Confirm Required)

### Option A: /etc/fstab (reboot persistent)
```bash
# Add to /etc/fstab:
# proc  /proc  proc  defaults,hidepid=2  0  0

# Apply immediately without reboot:
mount -o remount,hidepid=2 /proc
```

### Option B: systemd (for systems where systemd manages /proc)
```bash
mkdir -p /etc/systemd/system/proc-hidepid.service.d/
cat > /etc/systemd/system/proc-hidepid.service.d/override.conf << 'EOF'
[Service]
ExecStartPre=/bin/mount -o remount,hidepid=2 /proc
EOF
systemctl daemon-reload
```

### With Monitoring Group (Best Practice)
```bash
# Create monitoring group
groupadd -r procmon 2>/dev/null
# Add monitoring users to group
usermod -aG procmon nagios 2>/dev/null || true
usermod -aG procmon zabbix 2>/dev/null || true

# /etc/fstab entry:
# proc  /proc  proc  defaults,hidepid=2,gid=$(getent group procmon | cut -d: -f3)  0  0
```

## Container/Docker Notes
- Docker containers use their own /proc namespace → hidepid on host doesn't affect inside-container /proc
- Each container should also be checked if it runs with privileged `/proc`

## Output Format
```
[HIGH] 23-proc: hidepid_disabled | /proc mounted without hidepid | all processes visible to all users | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 23-proc: hidepid_partial | /proc mounted with hidepid=1 | PIDs still browsable | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 23-proc: no_monitoring_gid | hidepid=2 set but no gid= | monitoring tools may break | action_id: ACT-YYYYMMDD-XXX
[PASS] 23-proc: hidepid_enforced | /proc mounted with hidepid=2,gid=<num> ✓
[INFO] 23-proc: summary | hidepid: 2 | gid: 994 | protection: FULL
```
