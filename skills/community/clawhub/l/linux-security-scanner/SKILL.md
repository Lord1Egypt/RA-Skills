---
name: linux-security-scanner
description: Linux security auditing tool that checks SSH configuration, open/listening ports, firewall rules (ufw/iptables/nftables), failed login attempts, sudoers permissions, world-writable files, and SUID binaries. Use when a user needs a security posture assessment, hardening audit, or compliance check on a Linux host — run individual checks or a full comprehensive audit with a formatted report.
---

# Linux Security Scanner

## Script

`scripts/security-audit.sh` — the single entry point for all checks.

The script is self-contained, portable, and works on any modern Linux system. It auto-detects available tools (ss/netstat, ufw/iptables/nftables, journalctl) and gracefully skips unavailable ones.

## Quick Start

Run a full audit:

```bash
bash scripts/security-audit.sh --all
```

Or with no arguments (same as `--all`):

```bash
bash scripts/security-audit.sh
```

## Individual Checks

Run any single check by name:

| Command | What it checks |
|---|---|
| `--ssh` | PermitRootLogin, PasswordAuthentication, Port, Protocol in sshd_config |
| `--ports` | Listening TCP ports (ss or netstat) |
| `--firewall` | ufw status, iptables filter rules, nftables ruleset |
| `--failed-logins` | lastb output and journalctl SSH auth failures (last 24h) |
| `--sudoers` | Sudoers file permissions (must be 440), files present, NOPASSWD entries, full sudo access grants |
| `--world-writable` | World-writable files in /etc, /tmp, /var, /home, /opt (depth 3) |
| `--suid` | All SUID binaries, risk assessment, unusual path detection |

Example:

```bash
bash scripts/security-audit.sh --ssh --failed-logins
```

## Full Audit Workflow

1. Run `bash scripts/security-audit.sh --all`
2. The script outputs a colorized report to stdout
3. A structured markdown report is stored in the `$REPORT` variable (accessible within the same shell session)
4. For programmatic use, redirect output to a file

## Common Findings & Recommendations

- **SSH hardening**: Disable root login, disable password auth, use key-only auth, change default port
- **Firewall**: Ensure only necessary ports are open; prefer deny-by-default
- **Sudoers**: Avoid NOPASSWD where possible; keep permissions at 440; audit who has full sudo access
- **SUID**: Review unusual SUID paths; minimize SUID binaries; check for known CVEs on common ones (pkexec, sudo, etc.)
- **World-writable files**: These are security risks — investigate why they're writable and restrict permissions

## Notes

- Requires root/sudo for some checks (failed-logins reads /var/log/btmp, ss shows process info)
- Runs entirely in the shell — no external dependencies beyond standard Linux tools
- Respects permission boundaries — non-accessible checks are noted, not forced
