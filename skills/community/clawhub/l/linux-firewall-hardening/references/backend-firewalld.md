# Backend: firewalld (RHEL / Rocky / Alma / Fedora)

firewalld is zone-aware. Always specify the zone. Default on most servers is `public`.

> **Detect your real SSH port first:** The examples below use port 22 for illustration. Replace with your actual port:
> ```bash
> SSH_PORT=$(ss -tlnp | grep -E "sshd|ssh" | awk '{print $NF}' | awk -F: '{print $NF}' | head -1)
> SSH_PORT=${SSH_PORT:-22}
> ```

## Detection

```bash
sudo firewall-cmd --state
# "running" or "not running"
```

## Prerequisites

- firewalld must be active but with known rules.
- No other frontend (ufw) must be active.
- Never modify iptables/nftables directly when firewalld owns the policy.

## Apply: Idempotent Zone Rules

### Step 1: Identify Active Zone

```bash
DEFAULT_ZONE=$(sudo firewall-cmd --get-default-zone)
echo "Default zone: $DEFAULT_ZONE"
sudo firewall-cmd --get-active-zones
```

### Step 2: Add Rules

```bash
ZONE="${DEFAULT_ZONE:-public}"
SSH_PORT=$(ss -tlnp | grep -E "sshd|ssh" | awk -F: '{print $NF}' | head -1)
SSH_PORT=${SSH_PORT:-22}

# SSH (service definition)
sudo firewall-cmd --zone="$ZONE" --query-service=ssh >/dev/null 2>&1 ||   sudo firewall-cmd --permanent --zone="$ZONE" --add-service=ssh

# HTTP / HTTPS
sudo firewall-cmd --zone="$ZONE" --query-service=http >/dev/null 2>&1 ||   sudo firewall-cmd --permanent --zone="$ZONE" --add-service=http
sudo firewall-cmd --zone="$ZONE" --query-service=https >/dev/null 2>&1 ||   sudo firewall-cmd --permanent --zone="$ZONE" --add-service=https

# Custom port
# sudo firewall-cmd --zone="$ZONE" --query-port=8080/tcp >/dev/null 2>&1 || #   sudo firewall-cmd --permanent --zone="$ZONE" --add-port=8080/tcp

# Rate-limit SSH (rich rule)
sudo firewall-cmd --zone="$ZONE" --query-rich-rule='rule service name=ssh limit value=3/m accept' >/dev/null 2>&1 ||   sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule='rule service name=ssh limit value=3/m accept'

# Apply
sudo firewall-cmd --reload
```

### Step 3: Verify

```bash
sudo firewall-cmd --list-all --zone="$ZONE"
```

## Zone Commands Quick Reference

```bash
# List all zones
sudo firewall-cmd --get-zones

# List all zones with rules
sudo firewall-cmd --list-all-zones

# Change default zone
sudo firewall-cmd --set-default-zone=drop

# Move interface to different zone
sudo firewall-cmd --zone=internal --change-interface=eth1
```

## Related

- `references/security-profiles.md` — Pre-built firewalld configurations
- `references/declarative-policy.md` — YAML-to-firewalld rendering
