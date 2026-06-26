---
name: firewall-change-template
---

# <FW-YYYYMMDD-NNN>

## Meta
- ID:       FW-YYYYMMDD-NNN
- Status:   pending | approved | denied
- Queued:   YYYY-MM-DD
- Type:     add-rule | delete-rule | change-policy | block-ip | open-port | close-port

## Current Firewall State (relevant part)
```
[paste current iptables/nft/ufw rule]
```

## Proposed Change
```bash
# Exact command to run:
<iptables/nft/ufw command>
```

## What This Achieves
[Why this change improves security]

## Impact
[What traffic will this affect — what could break]

## Rollback
```bash
# Exact undo command:
<rollback command>
```

## Test Before Applying
```bash
# How to verify the change works correctly:
<test command>
```

## Reply: APPROVE FW-YYYYMMDD-NNN
