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

## Output Format
```
[HIGH] 06-packages: security_updates_pending | count: 12 | kernel_update: yes | action_id: ACT-XXX
[MEDIUM] 06-packages: no_auto_updates | unattended-upgrades not configured
```
