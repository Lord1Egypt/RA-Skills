# Recovery Procedures

## Recovery Priority Order

1. **Wait for auto-rollback.** The rollback timer scheduled during Validate state will restore access.
2. **Use your second SSH session.** If open, undo changes manually.
3. **Use cloud serial console.** AWS EC2 Serial Console, GCP Serial Port, Azure Serial Console.
4. **Use hypervisor console.** VNC, IPMI, iDRAC, Proxmox noVNC.
5. **Transaction rollback** — restore known-good backup:
   ```bash
   sudo iptables-restore < "$BACKUP_DIR/iptables-v4.rules"
   sudo ip6tables-restore < "$BACKUP_DIR/iptables-v6.rules"
   sudo nft -f "$BACKUP_DIR/nftables.rules"
   sudo ufw reset && sudo ufw disable
   ```
6. **Emergency ACCEPT** — LAST RESORT only:
   ```bash
   sudo iptables -P INPUT ACCEPT; sudo iptables -F
   sudo ip6tables -P INPUT ACCEPT; sudo ip6tables -F
   sudo nft flush ruleset
   sudo ufw disable
   sudo firewall-cmd --panic-off
   ```
   **Warning**: Exposes host completely. Use only for rescue, then re-apply proper rules immediately. Schedule an auto-revert timer: `echo "sudo iptables -P INPUT DROP" | at now + 10 minutes`

## Rollback Mechanism

The rollback timer (scheduled during Validate state) supports two backends:

### at-based

```bash
ROLLBACK_JOB_ID=$(echo "$ROLLBACK_SCRIPT" | at now + 5 minutes 2>&1 | grep -oP 'job \\K\\d+')
atq     # Verify scheduled
atrm <jobid>   # Cancel after successful verification
```

### systemd-run fallback

```bash
systemd-run --on-active=5m --unit="firewall-rollback-$$" --user ...
systemctl --user list-units 'firewall-rollback-*'   # Verify
systemctl --user stop firewall-rollback-<pid>       # Cancel
```

## What the Rollback Does

1. Restore iptables v4 from backup → if unavailable, set INPUT ACCEPT + flush
2. Restore iptables v6 from backup → if unavailable, set INPUT ACCEPT + flush
3. Restore nftables from backup → if unavailable, flush ruleset
4. Disable ufw (if active)
5. Disable firewalld panic mode (if active)

This preserves Docker NAT, K8s CNI rules, and pre-existing configurations.
