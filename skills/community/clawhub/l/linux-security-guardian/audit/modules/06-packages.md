# Module 06 — Package Updates

## Commands

### Debian/Ubuntu
```bash
apt update -qq 2>/dev/null

# Total pending updates
apt list --upgradable 2>/dev/null | grep -v "Listing..." | wc -l

# Security updates specifically
apt list --upgradable 2>/dev/null | grep -i security | wc -l

# List security updates
apt-get --just-print upgrade 2>/dev/null | grep "^Inst" | grep -i security

# Held packages
apt-mark showhold
```

### RHEL/CentOS/Rocky
```bash
yum check-update --security -q 2>/dev/null
yum updateinfo list security 2>/dev/null | tail -20
dnf check-update --security 2>/dev/null
```

## Checks & Findings

### Pending Security Updates
- 0 security updates → PASS
- 1-5 security updates → MEDIUM
- > 5 security updates → HIGH
- Any kernel security update → HIGH + confirm required

### Total Update Lag
- 0-10 packages behind → LOW
- 10-50 packages behind → MEDIUM
- > 50 packages behind → HIGH (neglected system)

### Held Packages
- Any held package with known CVE → HIGH

### Auto-Update Config
- Check if unattended-upgrades is configured
- Not configured → MEDIUM advisory

### Unattended-Upgrades Auto-Enable
If unattended-upgrades not installed:
```bash
# Check if installable
which apt >/dev/null 2>&1 || { echo "Not Debian/Ubuntu — skip"; exit 0; }

# Check if installed
dpkg -l unattended-upgrades 2>/dev/null | grep -q "^ii" || echo "not installed"
```

If not installed → queue install (confirm required):
```bash
# apt install -y unattended-upgrades
```

If installed but not configured for security-only updates:
```bash
# Check current config
cat /etc/apt/apt.conf.d/50unattended-upgrades 2>/dev/null | grep -E "Allowed-Origins|Automatic-Reboot|Remove-Unused"

# Check if enabled
cat /etc/apt/apt.conf.d/20auto-upgrades 2>/dev/null
```

### Recommended Config (security-only)
Write to /etc/apt/apt.conf.d/20auto-upgrades (confirm required):
```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
```

Write to /etc/apt/apt.conf.d/50unattended-upgrades (confirm required):
```
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
};
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Automatic-Reboot-Time "03:00";
```

### Auto-Enable Flow
1. Check if unattended-upgrades installed → if not, queue install
2. Check if 20auto-upgrades has Unattended-Upgrade "1" → if not, queue config
3. Check if 50unattended-upgrades restricts to security-only → if not, queue config
4. After config → verify with: `unattended-upgrades --dry-run --debug 2>&1 | head -20`
5. Log action to actions/auto-done/<client>/<server>/

### Output Format (unattended-upgrades)
```
[MEDIUM] 06-packages: unattended_upgrades_not_installed | action: install_queued | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 06-packages: unattended_upgrades_not_enabled | action: config_queued | action_id: ACT-YYYYMMDD-XXX
[PASS] 06-packages: unattended_upgrades | security-only updates enabled ✓
```

## Output Format
```
[HIGH] 06-packages: security_updates_pending | count: 12 | kernel_update: yes | action_id: ACT-XXX
[MEDIUM] 06-packages: no_auto_updates | unattended-upgrades not configured
```
