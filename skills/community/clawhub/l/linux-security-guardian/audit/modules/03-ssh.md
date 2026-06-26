# Module 03 — SSH Configuration

## Commands
```bash
sshd -T 2>/dev/null          # full effective SSH config (best method)
cat /etc/ssh/sshd_config     # raw config file
grep -v "^#\|^$" /etc/ssh/sshd_config
```

## Checks — 20+ SSH Security Parameters

| Parameter | Secure Value | Finding if Wrong |
|---|---|---|
| PermitRootLogin | no | HIGH → confirm to set no |
| PasswordAuthentication | no | HIGH → confirm to set no |
| PubkeyAuthentication | yes | HIGH |
| PermitEmptyPasswords | no | CRITICAL → auto-fix |
| X11Forwarding | no | MEDIUM |
| MaxAuthTries | ≤ 4 | MEDIUM |
| LoginGraceTime | ≤ 60 | LOW |
| AllowAgentForwarding | no | LOW |
| AllowTcpForwarding | no | MEDIUM |
| ClientAliveInterval | 300 | LOW |
| ClientAliveCountMax | 2 | LOW |
| Protocol | 2 (implicit modern) | CRITICAL if 1 |
| Port | not 22 | INFO (advisory) |
| UsePAM | yes | MEDIUM if no |
| IgnoreRhosts | yes | HIGH if no |
| HostbasedAuthentication | no | HIGH |
| PermitUserEnvironment | no | MEDIUM |
| StrictModes | yes | HIGH if no |
| MaxSessions | ≤ 4 | LOW |
| Banner | set | INFO |
| LogLevel | VERBOSE or INFO | MEDIUM if silent |
| AllowUsers/AllowGroups | set | INFO (advisory) |

## Auto-Fix Eligible (from whitelist only)
- PermitEmptyPasswords no → AUTO-FIX (sed in place)

## Confirm Required
- PermitRootLogin no → confirm (could lock out if no key auth)
- PasswordAuthentication no → confirm (MUST have key auth working first)
- All others → queue confirm

## Output Format
```
[HIGH] 03-ssh: PermitRootLogin | value: yes | expected: no | action_id: ACT-YYYYMMDD-001
[PASS] 03-ssh: MaxAuthTries | value: 3 ≤ 4
```
