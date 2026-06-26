---
name: linux-security-guardian-pre-action
description: Safety check before executing ANY action on the server. Must pass all checks before proceeding.
---

# Pre-Action Safety Check

## For Every Action — Run This First

```
1. Is this action in SERVER_PROFILE.md auto-actions whitelist?
   NO → STOP. Queue for confirmation.

2. Is this action reversible?
   NO → STOP. Never auto-execute irreversible actions.

3. Does this action modify a network or firewall rule?
   YES → STOP. Always require confirmation.

4. Does this action stop/start a service?
   If restart_<service>: true in profile → proceed
   Otherwise → STOP. Queue for confirmation.

5. Does this action modify /etc/ssh/ or PAM config?
   YES → STOP. Always require confirmation (lockout risk).

6. Does this action patch/upgrade a package?
   YES → STOP. Always require confirmation.

7. Snapshot current state:
   → Save to actions/<client>/<server>/history/<action-id>-BEFORE.txt
   → Generate rollback command
   → Save to actions/<client>/<server>/history/<action-id>-ROLLBACK.sh

8. All checks passed → PROCEED
```

## Auto-Actions That Are ALWAYS Safe
(From SERVER_PROFILE.md whitelist only)
- `chmod 1777 /tmp` — /tmp permissions
- `systemctl start auditd` — start audit daemon
- `systemctl start fail2ban` — start fail2ban
- `passwd -l <user>` — lock empty-password account

## Auto-Actions That Are NEVER Safe (no exceptions)
- Any iptables/nftables/ufw command
- Any apt-get upgrade / yum update
- Any sshd_config modification
- Stopping any running service
- Any user deletion
- Any kernel parameter change via sysctl -w
