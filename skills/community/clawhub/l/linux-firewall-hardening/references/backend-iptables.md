# Backend: iptables (Legacy Fallback)

Use atomic `iptables-restore` instead of `-F` followed by individual `-A` commands. Build a complete ruleset file, then swap it in one operation. Always manage IPv4 (`iptables`) and IPv6 (`ip6tables`) separately.

> **Detect your real SSH port first:** The examples below use port 22 for illustration. If your SSH runs on a different port, replace `22` with your actual port:
> ```bash
> SSH_PORT=$(ss -tlnp | grep -E "sshd|ssh" | awk '{print $NF}' | awk -F: '{print $NF}' | head -1)
> SSH_PORT=${SSH_PORT:-22}
> echo "Detected SSH port: $SSH_PORT"
> ```
> Using the wrong SSH port in the ruleset below will lock you out.

## Key Principle: Atomic Restore

```bash
# Validate syntax first
sudo iptables-restore --test /tmp/iptables-v4.rules
sudo ip6tables-restore --test /tmp/iptables-v6.rules

# Apply atomically
sudo iptables-restore /tmp/iptables-v4.rules
sudo ip6tables-restore /tmp/iptables-v6.rules
```

## Apply: Atomic Rulesets

### Step 1: Build IPv4 Ruleset (`/tmp/iptables-v4.rules`)

```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT
COMMIT
```

### Step 2: Build IPv6 Ruleset (`/tmp/iptables-v6.rules`)

```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p icmpv6 -j ACCEPT
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 80 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT
COMMIT
```

### Step 3: Persist

- **Debian/Ubuntu**: `sudo apt install iptables-persistent`, then `sudo netfilter-persistent save`
- **RHEL/CentOS**: `sudo service iptables save` or migrate to `firewalld`

## Idempotent Single-Rule Pattern

If adding a single rule instead of full restore:

```bash
# Check if rule exists before adding
sudo iptables -C INPUT -p tcp --dport 8080 -j ACCEPT 2>/dev/null ||   sudo iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
```

## Related

- `references/security-profiles.md` — Pre-built iptables configurations
- `references/declarative-policy.md` — YAML-to-iptables rendering
