# Server Security Baseline
*Created on first audit run. Updated only on owner command.*
*Agent compares every audit against this file.*

## Baseline Date
Created: [YYYY-MM-DD — set on first run]
Last updated: [YYYY-MM-DD]

## Expected Users With Login Shell
[Populated on first run]

## Expected UID 0 Accounts
- root

## Expected Sudo Users
[From SERVER_PROFILE.md]

## Expected Running Services
[Populated on first run from systemctl]

## Expected Open Ports
[Populated on first run from ss -tulpn]

## Expected SUID Binaries
[Populated on first run from find / -perm -4000]

## Key Binary Hashes (for integrity check)
[Populated on first run — sha256sum of critical binaries]

## Firewall Baseline
[Snapshot on first run]

## Kernel Parameters Baseline
[sysctl values on first run]

## Cron Jobs Baseline
[All cron jobs on first run]

---
*To update baseline: tell agent "update security baseline"*
*Agent will update on next audit after your confirmation*
