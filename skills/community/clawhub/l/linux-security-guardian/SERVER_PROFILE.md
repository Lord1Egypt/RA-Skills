# Server Profile — Multi-Client

*Agent reads this on every audit. Loops per client, then per server.*

---

## SSH MCP (REQUIRED — hard dependency)
- ssh_mcp_version: v2
- shared_key: ~/.ssh/id_ed25519  # All servers use same root key

## Email Accounts
- default: ""     # The account used for ALL outgoing reports and alerts
- admin: ""       # Personal admin account. NEVER use for automated reports.
- rule: "Always use default account. Never specify --account admin."

---

## Client: client-1
- client_id: c1
- notification_email: ""   # Per-client alert email (overrides global if set)

### Server Fleet

| Server Name | Host | Port | Username | Key Path | Connection ID |
|-------------|------|------|----------|----------|---------------|
| server-01 |  | 22 | root | ~/.ssh/id_ed25519 |  |
| server-02 |  | 22 | root | ~/.ssh/id_ed25519 |  |
| server-03 |  | 22 | root | ~/.ssh/id_ed25519 |  |
| server-04 |  | 22 | root | ~/.ssh/id_ed25519 |  |
| server-05 |  | 22 | root | ~/.ssh/id_ed25519 |  |
| server-06 |  | 22 | root | ~/.ssh/id_ed25519 |  |
| server-07 |  | 22 | root | ~/.ssh/id_ed25519 |  |

### Per-Server Config

| Server | Expected Ports | Expected Services | Sudo Users | SSL Domains |
|--------|---------------|-------------------|------------|-------------|
| server-01 | 22, 80, 443 | sshd, nginx | | |
| server-02 | 22, 80, 443 | sshd, nginx | | |
| server-03 | 22 | sshd | | |
| server-04 | 22, 443 | sshd, docker | | |
| server-05 | 22, 80, 443 | sshd, apache2 | | |
| server-06 | 22 | sshd | | |
| server-07 | 22, 443 | sshd, docker | | |

### Firewall Policy
- Default incoming: DROP
- Default outgoing: ACCEPT
- Management interface: [IP range]

### Auto-Actions Allowed
- fix_tmp_permissions: true
- restart_auditd: true
- restart_fail2ban: true
- lock_empty_password_accounts: true
- cleanup_old_logs: false
- auto_patch_security: false

### Notification
- immediate_alert_on: CRITICAL
- daily_report: true
- weekly_summary: true

### Package Manager
- apt

### CVE Scan
- local_method: debsecan
- external_sources:
  - cisa_kev: true
  - osv_dev: true
  - nvd_api: false
  - nvd_api_key: ""
- high_priority_packages:
  - linux, openssl, openssh, sudo, nginx, curl, bash, glibc, systemd, docker

---

## Client: [NEXT-CLIENT-NAME]
- client_id: [c2]
- notification_email: [email]

### Server Fleet
| Server Name | Host | Port | Username | Key Path | Connection ID |
|-------------|------|------|----------|----------|---------------|

### Per-Server Config
| Server | Expected Ports | Expected Services | Sudo Users | SSL Domains |
|--------|---------------|-------------------|------------|-------------|

[Copy per-client sections as needed for additional clients]
