# Module 24 — Swap Encryption Check

> **Purpose:** Audit whether swap space is encrypted. Unencrypted swap can leak sensitive data: encryption keys, passwords, API tokens, database credentials — anything that was in RAM can end up unencrypted on disk via swap.

## Why This Matters
- RAM contents (passwords, tokens, keys) get paged out to swap
- If swap is unencrypted, an attacker with physical or root access can read swap
- Cloud VM snapshots include swap → data leakage across VM clones
- Forensic recovery of swap is trivial (strings /dev/sdaX)

## Commands
```bash
# Check swap devices and their encryption status
swapon --show 2>/dev/null

# Alternative: read /proc/swaps
cat /proc/swaps 2>/dev/null

# Check if swap is on an encrypted device (LUKS)
swapon --show 2>/dev/null | awk 'NR>1 {print $1}' | while read dev; do
  echo "Swap: $dev"
  # Check if it's a dm-crypt/LUKS device
  dmsetup table 2>/dev/null | grep "$(basename $dev)" && echo "  → ENCRYPTED (dm-crypt)" || echo "  → PLAIN DEVICE"
  # Check if it's on an LVM on LUKS
  lvdisplay "$dev" 2>/dev/null | grep -i "crypt" && echo "  → LVM on LUKS"
done

# Check for cryptswap references
grep -r "cryptswap\|crypt-swap\|encrypted.*swap\|luks.*swap" /etc/crypttab 2>/dev/null || echo "no_crypttab_swap"

# Check if swap file is on encrypted filesystem
swapon --show 2>/dev/null | awk 'NR>1 {print $1}' | while read dev; do
  if [ -f "$dev" ]; then
    echo "Swap file: $dev (on $(df $dev | awk 'NR==2{print $1}'))"
    df "$dev" | awk 'NR==2{print $1}' | grep -q "crypt\|luks" && echo "  → ON ENCRYPTED FS" || echo "  → ON PLAIN FS"
  fi
done

# Check total swap size
free -h | grep Swap

# Check swap priority and usage
sysctl vm.swappiness 2>/dev/null
```

## Checks & Findings

| Condition | Severity | Detail |
|-----------|----------|--------|
| No swap at all | **LOW (Pass)** | No swap = no swap leak. But OOM risk if RAM exhausted |
| Swap on plain/unencrypted partition | **HIGH** | Sensitive RAM data recoverable from disk |
| Swap on LVM without LUKS | **HIGH** | LVM doesn't encrypt underlying data |
| Swap on encrypted device (LUKS/dm-crypt) | **PASS** | Protected at rest |
| Swap file on encrypted filesystem | **PASS** | Inherits FS encryption |
| Swap on ZFS encrypted dataset | **PASS** | Inherits ZFS encryption |
| Swap on cloud ephemeral disk | **MEDIUM** | Ephemeral disks may persist beyond VM lifecycle |
| vm.swappiness > 60 | **LOW** | More swapping = more data at risk |

## Cloud Provider Notes
| Provider | Swap Default | Risk |
|----------|-------------|------|
| AWS EC2 | No swap by default | LOW |
| Google Cloud | No swap by default | LOW |
| Azure | No swap by default | LOW |
| Contabo | May have swap partition | CHECK |
| Hetzner | May have swap partition | CHECK |
| DigitalOcean | No swap by default | LOW |

## Auto-Fix Options (Confirm Required)

### Option A: Encrypt existing swap partition with LUKS
```bash
# WARNING: Destructive to existing swap data
swapoff /dev/sdXN
cryptsetup luksFormat /dev/sdXN
cryptsetup luksOpen /dev/sdXN cryptswap
mkswap /dev/mapper/cryptswap

# Update /etc/crypttab:
echo "cryptswap /dev/sdXN none luks,discard" >> /etc/crypttab

# Update /etc/fstab:
# /dev/mapper/cryptswap none swap sw 0 0
```

### Option B: Use encrypted swap file
```bash
# Create swap file on encrypted filesystem
fallocate -l 2G /secure/swapfile
chmod 600 /secure/swapfile
mkswap /secure/swapfile
swapon /secure/swapfile
```

### Option C: Disable swap entirely (if sufficient RAM)
```bash
swapoff -a
# Remove swap entries from /etc/fstab
```

## Output Format
```
[HIGH] 24-swap: unencrypted_partition | swap: /dev/sda3 | type: partition | encryption: NONE | action_id: ACT-YYYYMMDD-XXX
[HIGH] 24-swap: unencrypted_lvm | swap: /dev/vg0/swap | type: LVM logical volume | encryption: NONE | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 24-swap: cloud_ephemeral | swap: /dev/nvme1n1 | type: ephemeral | risk: snapshot leakage | action_id: ACT-YYYYMMDD-XXX
[PASS] 24-swap: encrypted_dmcrypt | swap: /dev/mapper/cryptswap | encryption: LUKS ✓
[PASS] 24-swap: encrypted_filesystem | swap: /secure/swapfile | FS: LUKS/dm-crypt ✓
[PASS] 24-swap: no_swap | swap: none | swapiness: 60 | note: OOM risk if RAM exhausted
[INFO] 24-swap: summary | total: 2G | encrypted: 2G (100%) | swappiness: 60
```
