# Backend: UFW (Recommended for Ubuntu / Debian)

UFW (Uncomplicated Firewall) is the easiest path for Ubuntu and Debian. It handles IPv4 and IPv6 together, uses simple commands, and is managed by a systemd service.

## Detection

```bash
sudo ufw status
# "Status: active" or "Status: inactive"
```

## Prerequisites

- UFW must be installed but inactive (or with known rules).
- No other frontend (firewalld) must be active.
- Never modify iptables/nftables directly when ufw owns the policy.

## Apply: Idempotent Rules

### Step 1: Default Policies

```bash
# Idempotent — safe to repeat
sudo ufw --dry-run default deny incoming
sudo ufw --dry-run default allow outgoing

# Apply
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### Step 2: SSH (Detect Real Port)

```bash
SSH_PORT=$(ss -tlnp | grep -E "sshd|ssh" | awk -F: '{print $NF}' | head -1)
SSH_PORT=${SSH_PORT:-22}

# Idempotent — check before add, exact port match
sudo ufw status | awk '{print $1}' | grep -qx "${SSH_PORT}/tcp" || sudo ufw allow "${SSH_PORT}/tcp"
```

### Step 3: Service Rules

```bash
# HTTP / HTTPS (uses exact port match to avoid matching 8080 when checking 80)
sudo ufw status | awk '{print $1}' | grep -qx "80/tcp"  || sudo ufw allow 80/tcp
sudo ufw status | awk '{print $1}' | grep -qx "443/tcp" || sudo ufw allow 443/tcp

# Custom ports (same pattern)
# sudo ufw status | awk '{print $1}' | grep -qx "8080/tcp" || sudo ufw allow 8080/tcp
```

### Step 4: Enable

```bash
# --force prevents interactive prompt during automation
sudo ufw --force enable
```

### Step 5: Verify

```bash
sudo ufw status verbose
sudo ufw status numbered
```

## Outbound Policy

UFW defaults to `allow outgoing`. For high-security environments:

```bash
# WARNING: restrict OUTPUT only after inventorying all outbound dependencies
sudo ufw default deny outgoing
sudo ufw allow out 53/udp      # DNS
sudo ufw allow out 123/udp     # NTP
sudo ufw allow out 80/tcp
sudo ufw allow out 443/tcp
```

## Related

- `references/security-profiles.md` — Pre-built UFW configurations
- `references/declarative-policy.md` — YAML-to-UFW rendering
