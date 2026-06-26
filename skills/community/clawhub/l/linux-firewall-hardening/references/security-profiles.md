# Security Profiles

Pre-built hardened firewall configurations for common server roles.
Each profile includes rules for ufw, firewalld, nftables, and iptables.
Choose the profile that matches your server's purpose, then adapt port numbers and subnets to your environment.

---

## Profile: public-web-server

**Use case**: Public-facing web server (Nginx, Apache, Caddy).
**Open ports**: 22 (SSH), 80 (HTTP), 443 (HTTPS).
**Extras**: SSH rate-limited. ICMP allowed for path MTU discovery.

### UFW

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Exact port match: awk extracts column 1, grep -qx prevents substring false-positives (e.g. 8022 matching "22/tcp")
sudo ufw status | awk '{print $1}' | grep -qx "22/tcp"  || sudo ufw allow 22/tcp
sudo ufw status | awk '{print $1}' | grep -qx "80/tcp"  || sudo ufw allow 80/tcp
sudo ufw status | awk '{print $1}' | grep -qx "443/tcp" || sudo ufw allow 443/tcp

sudo ufw limit 22/tcp
sudo ufw --force enable
```

### firewalld

```bash
ZONE=$(sudo firewall-cmd --get-default-zone)

# IMPORTANT: --add-service=ssh always maps to port 22. If your SSH runs on a non-standard
# port, replace --add-service=ssh with --add-port=<port>/tcp below.
SSH_PORT=$(ss -tlnp | grep -E "sshd|ssh" | awk '{print $NF}' | awk -F: '{print $NF}' | head -1)
SSH_PORT=${SSH_PORT:-22}

if [[ "$SSH_PORT" == "22" ]]; then
    sudo firewall-cmd --zone="$ZONE" --query-service=ssh   >/dev/null 2>&1 || sudo firewall-cmd --permanent --zone="$ZONE" --add-service=ssh
else
    sudo firewall-cmd --zone="$ZONE" --query-port="${SSH_PORT}/tcp" >/dev/null 2>&1 || sudo firewall-cmd --permanent --zone="$ZONE" --add-port="${SSH_PORT}/tcp"
fi

sudo firewall-cmd --zone="$ZONE" --query-service=http  >/dev/null 2>&1 || sudo firewall-cmd --permanent --zone="$ZONE" --add-service=http
sudo firewall-cmd --zone="$ZONE" --query-service=https >/dev/null 2>&1 || sudo firewall-cmd --permanent --zone="$ZONE" --add-service=https

# Rich rule for SSH rate limiting — use explicit port if non-standard
if [[ "$SSH_PORT" == "22" ]]; then
    sudo firewall-cmd --zone="$ZONE" --query-rich-rule='rule service name=ssh limit value=3/m accept' >/dev/null 2>&1 || \
      sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule='rule service name=ssh limit value=3/m accept'
else
    sudo firewall-cmd --zone="$ZONE" --query-rich-rule="rule family=ipv4 port port=${SSH_PORT} protocol=tcp limit value=3/m accept" >/dev/null 2>&1 || \
      sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule="rule family=ipv4 port port=${SSH_PORT} protocol=tcp limit value=3/m accept"
fi

sudo firewall-cmd --reload
```

### nftables

Save to `/etc/nftables.conf`:

```nft
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
        # Set-based accept for web ports + SSH (no rate limit on set)
        # SSH rate limiting: skip set match for port 22 so the rate-limited rule applies
        tcp dport { 80, 443 } accept
        tcp dport 22 ct state new limit rate 10/second burst 20 packets accept
        # Fallback: allow any remaining SSH in case rate limit doesn't match
        tcp dport 22 accept
        log prefix "nft-drop: " limit rate 5/second
        drop
    }

    chain forward { type filter hook forward priority 0; policy drop; }
    chain output  { type filter hook output  priority 0; policy accept; }
}
```

Apply:
```bash
sudo nft -c -f /etc/nftables.conf && sudo nft -f /etc/nftables.conf
sudo systemctl enable nftables
```

### iptables (atomic restore)

**IPv4** (`/tmp/web-v4.rules`):
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

**IPv6** (`/tmp/web-v6.rules`):
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

Apply:
```bash
sudo iptables-restore --test /tmp/web-v4.rules && sudo iptables-restore /tmp/web-v4.rules
sudo ip6tables-restore --test /tmp/web-v6.rules && sudo ip6tables-restore /tmp/web-v6.rules
```

---

## Profile: internal-database

**Use case**: Database server (MySQL, PostgreSQL, MongoDB) in a private subnet.
**Open ports**: 22 from mgmt subnet only, DB port from app subnet only.
**Assumptions**: MGMT_SUBNET=10.0.1.0/24, APP_SUBNET=10.0.2.0/24, DB_PORT=3306.

### UFW

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

# ufw is idempotent for source-restricted rules — re-running prints "Skipping adding existing rule"
sudo ufw allow from 10.0.1.0/24 to any port 22 proto tcp
sudo ufw allow from 10.0.2.0/24 to any port 3306 proto tcp
sudo ufw --force enable
```

### firewalld

```bash
ZONE=$(sudo firewall-cmd --get-default-zone)

# Detect actual SSH port — --add-service=ssh always maps to 22
SSH_PORT_DB=$(ss -tlnp | grep -E "sshd|ssh" | awk '{print $NF}' | awk -F: '{print $NF}' | head -1)
SSH_PORT_DB=${SSH_PORT_DB:-22}

if [[ "$SSH_PORT_DB" == "22" ]]; then
    sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule='rule family=ipv4 source address=10.0.1.0/24 service name=ssh accept'
else
    sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule="rule family=ipv4 source address=10.0.1.0/24 port port=${SSH_PORT_DB} protocol=tcp accept"
fi
sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule='rule family=ipv4 source address=10.0.2.0/24 port port=3306 protocol=tcp accept'
sudo firewall-cmd --reload
```

### nftables

```nft
#!/usr/sbin/nft -f

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        iif lo accept
        ct state established,related accept
        ct state invalid drop
        ip protocol icmp accept
        ip6 nexthdr icmpv6 accept

        ip saddr 10.0.1.0/24 tcp dport 22 accept
        ip saddr 10.0.2.0/24 tcp dport 3306 accept

        log prefix "nft-drop: " limit rate 5/second
        drop
    }

    chain forward { type filter hook forward priority 0; policy drop; }
    chain output  { type filter hook output  priority 0; policy accept; }
}
```

### iptables

**IPv4** (`/tmp/db-v4.rules`):
```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT -s 10.0.1.0/24 -p tcp --dport 22 -j ACCEPT
-A INPUT -s 10.0.2.0/24 -p tcp --dport 3306 -j ACCEPT
COMMIT
```

> IPv6: adapt source addresses to your IPv6 subnets or drop IPv6 if not used.

---

## Profile: bastion-host

**Use case**: Jump box / bastion. SSH only. Aggressive rate limiting.
**Open ports**: 22 only.
**Extras**: Geo-restriction optional (requires additional tooling like `ipset` + country block lists).

### UFW

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Exact port match: awk extracts column 1 to avoid substring false-positives (e.g., 8022 matching 22/tcp)
sudo ufw status | awk '{print $1}' | grep -qx "22/tcp" || sudo ufw allow 22/tcp
sudo ufw limit 22/tcp
sudo ufw --force enable
```

### firewalld

```bash
ZONE=$(sudo firewall-cmd --get-default-zone)

# Detect actual SSH port — --add-service=ssh always maps to 22
SSH_PORT=$(ss -tlnp | grep -E "sshd|ssh" | awk '{print $NF}' | awk -F: '{print $NF}' | head -1)
SSH_PORT=${SSH_PORT:-22}

if [[ "$SSH_PORT" == "22" ]]; then
    sudo firewall-cmd --permanent --zone="$ZONE" --add-service=ssh
    sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule='rule service name=ssh limit value=3/m accept'
else
    sudo firewall-cmd --permanent --zone="$ZONE" --add-port="${SSH_PORT}/tcp"
    sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule="rule family=ipv4 port port=${SSH_PORT} protocol=tcp limit value=3/m accept"
fi
sudo firewall-cmd --reload
```

### nftables

```nft
#!/usr/sbin/nft -f

table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        iif lo accept
        ct state established,related accept
        ct state invalid drop
        ip protocol icmp accept
        ip6 nexthdr icmpv6 accept

        tcp dport 22 ct state new limit rate 5/minute burst 10 packets accept

        log prefix "nft-drop: " limit rate 5/second
        drop
    }

    chain forward { type filter hook forward priority 0; policy drop; }
    chain output  { type filter hook output  priority 0; policy accept; }
}
```

### iptables

**IPv4** (`/tmp/bastion-v4.rules`):
```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
-A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 4 -j DROP
-A INPUT -p tcp --dport 22 -j ACCEPT
COMMIT
```

---

## Profile: zero-trust-node

**Use case**: High-security node. Default deny all inbound AND outbound.
**Approach**: Explicit allow-list only. Requires full dependency inventory.

### UFW

```bash
sudo ufw default deny incoming
sudo ufw default deny outgoing

sudo ufw allow out 53/udp
sudo ufw allow out 123/udp
sudo ufw allow out 80/tcp
sudo ufw allow out 443/tcp

# Allow inbound SSH from specific subnet only
sudo ufw allow from 10.0.1.0/24 to any port 22 proto tcp

sudo ufw --force enable
```

### nftables

```nft
#!/usr/sbin/nft -f

table inet filter {
    set allowed_in_tcp {
        type inet_service
        flags interval
        elements = { 22 }
    }

    chain input {
        type filter hook input priority 0; policy drop;
        iif lo accept
        ct state established,related accept
        ct state invalid drop
        ip saddr 10.0.1.0/24 tcp dport @allowed_in_tcp accept
        log prefix "nft-drop: " limit rate 5/second
        drop
    }

    chain forward { type filter hook forward priority 0; policy drop; }

    chain output {
        type filter hook output priority 0; policy drop;
        oif lo accept
        ct state established,related accept
        udp dport 53 accept
        udp dport 123 accept
        tcp dport 80 accept
        tcp dport 443 accept
        log prefix "nft-out-drop: " limit rate 5/second
        drop
    }
}
```

> **Warning**: Zero-trust outbound rules are easy to break. Verify DNS resolver IPs, NTP servers, package mirrors, monitoring endpoints, and certificate authority OCSP/CRL URLs before enabling `OUTPUT DROP`.

---

## Customization Guide

When adapting a profile:

1. Replace placeholder subnets (e.g., `10.0.1.0/24`) with your real network ranges.
2. Replace placeholder ports (e.g., `3306`) with your actual service ports.
3. Run the idempotent detection pattern from the main SKILL.md before applying.
4. Always schedule a rollback timer before the first apply.
5. Verify with `ss -tulpn` and external `nmap` scan after applying.
