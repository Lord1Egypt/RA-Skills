# Backend: nftables (Modern Dual-Stack)

nftables is the modern replacement for iptables. It supports IPv4 and IPv6 in a single `inet` table, has atomic ruleset replacement, and uses a cleaner syntax.

> **Detect your real SSH port first:** The examples below use port 22 for illustration. Replace with your actual port:
> ```bash
> SSH_PORT=$(ss -tlnp | grep -E "sshd|ssh" | awk '{print $NF}' | awk -F: '{print $NF}' | head -1)
> SSH_PORT=${SSH_PORT:-22}
> ```

## Detection

```bash
sudo nft list ruleset
# Shows current rules if active
```

## Key Principle: Atomic Replacement

Build a new ruleset file, validate with `nft -c`, then apply in one shot. **Never `flush ruleset` manually** on a production host without a backup.

## Apply: Atomic Ruleset

### Step 1: Build Ruleset File

```bash
sudo tee /etc/nftables.conf.new << 'EOF'
#!/usr/sbin/nft -f

table inet filter {
    set allowed_tcp_ports {
        type inet_service
        flags interval
        elements = { 22, 80, 443 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        iif lo accept
        ct state established,related accept
        ct state invalid drop

        ip protocol icmp accept
        ip6 nexthdr icmpv6 accept

        tcp dport @allowed_tcp_ports accept

        # Rate limit new SSH connections
        tcp dport 22 ct state new limit rate 10/second burst 20 packets accept

        # Log with rate limit to prevent syslog flood
        log prefix "nft-drop: " limit rate 5/second
        drop
    }

    chain forward {
        type filter hook forward priority 0; policy drop;
    }

    chain output {
        type filter hook output priority 0; policy accept;
    }
}
EOF
```

> **Warning**: Excessive logging can overwhelm syslog/journald on high-traffic systems. Always use `limit rate` on log rules and monitor after enabling.

### Step 2: Dry-Run (Validate Syntax)

```bash
sudo nft -c -f /etc/nftables.conf.new
```

If this returns errors, fix the file and re-validate. **Do not proceed until dry-run passes.**

### Step 3: Atomic Apply

```bash
# Backup current ruleset (belt-and-suspenders)
sudo nft list ruleset > "$BACKUP_DIR/nftables-pre-apply.rules" 2>/dev/null || true

# Atomic replace
sudo nft -f /etc/nftables.conf.new
sudo mv /etc/nftables.conf.new /etc/nftables.conf

# Enable persistence
sudo systemctl enable nftables
sudo systemctl restart nftables
```

### Step 4: Verify

```bash
sudo nft list ruleset
```

## Related

- `references/security-profiles.md` — Pre-built nftables configurations
- `references/declarative-policy.md` — YAML-to-nftables rendering
