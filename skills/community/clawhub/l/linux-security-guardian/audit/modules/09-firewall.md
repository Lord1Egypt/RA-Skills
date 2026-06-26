# Module 09 — Firewall Audit

## Commands
```bash
# Detect firewall type
which ufw    >/dev/null 2>&1 && echo "ufw"
which nft    >/dev/null 2>&1 && echo "nftables"
iptables -L  >/dev/null 2>&1 && echo "iptables"

# UFW
ufw status verbose 2>/dev/null

# iptables
iptables -L -n -v 2>/dev/null
iptables -L INPUT -n -v 2>/dev/null
iptables -L OUTPUT -n -v 2>/dev/null
iptables -L FORWARD -n -v 2>/dev/null
ip6tables -L -n -v 2>/dev/null   # IPv6

# nftables
nft list ruleset 2>/dev/null

# Save current snapshot
iptables-save 2>/dev/null > /tmp/fw-snapshot.txt
```

## Snapshot
Save full firewall state to: network/firewall-snapshots/YYYY-MM-DD-rules.txt
Compare against last snapshot — any unexpected changes → HIGH

## Checks & Findings

### No Firewall Active
- No ufw/iptables/nftables active → CRITICAL
- Queue confirm to enable: `ufw enable` or `systemctl start iptables`

### Default Policy
- INPUT default ACCEPT → HIGH (should be DROP or REJECT)
- FORWARD default ACCEPT (if not router) → MEDIUM

### Overly Permissive Rules
- Any rule allowing from 0.0.0.0/0 to sensitive ports (DB, admin) → HIGH
- Broad ACCEPT rules with no source restriction → MEDIUM

### Rule Changes Since Last Audit
- Diff current snapshot against previous
- Any addition/deletion → HIGH (confirm: expected or not?)

### IPv6 Firewall
- iptables protected but ip6tables not → MEDIUM (IPv6 bypass possible)

## All Proposed Changes
NEVER apply firewall changes automatically.
For every suggested change, write to network/proposed-changes/FW-YYYYMMDD-NNN.md:
```
Command: [exact command]
Reason: [why needed]
Risk: [what could go wrong]
Rollback: [exact undo command]
```

## Output Format
```
[CRITICAL] 09-firewall: no_firewall | no active firewall detected | action: FW-001 confirm
[HIGH] 09-firewall: default_accept | INPUT chain default ACCEPT | action: FW-002 confirm
[HIGH] 09-firewall: rule_changed | new rule detected vs yesterday snapshot | confirm: expected?
```
