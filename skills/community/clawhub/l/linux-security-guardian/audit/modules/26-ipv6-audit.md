# Module 26 — IPv6 Security Audit

> **Purpose:** Comprehensive IPv6 security audit including RA (Router Advertisement) acceptance, IPv6 forwarding, privacy extensions, and NDP hardening. IPv6 is often enabled by default but unconfigured, creating an unmonitored attack surface.

## Background: Why IPv6 Matters
- **Enabled by default** on most modern Linux distributions (Debian, Ubuntu, RHEL)
- **Often unmonitored** — firewall rules, IDS, and monitoring tools typically IPv4-only
- **Dual-stack vulnerability**: IPv4 firewall perfect, IPv6 completely open
- **Link-local attacks**: NDP spoofing, RA flooding, SLAAC hijacking
- **Privacy leak**: EUI-64 MAC-based addresses expose hardware identity

## Commands
```bash
# Check if IPv6 is enabled at all
sysctl net.ipv6.conf.all.disable_ipv6 2>/dev/null
# 0 = enabled, 1 = disabled

# Check IPv6 addresses on all interfaces
ip -6 addr show 2>/dev/null

# Check IPv6 routes
ip -6 route show 2>/dev/null

# IPv6 listening services
ss -tulpn 2>/dev/null | grep -E "tcp6|udp6"

# IPv6 firewall rules
ip6tables -L -n 2>/dev/null | head -20
ip6tables -L -n 2>/dev/null | grep "Chain" | grep "policy"

# Check if ip6tables is installed
which ip6tables 2>/dev/null || echo "ip6tables_not_found"

# Comprehensive IPv6 kernel parameters
sysctl -a 2>/dev/null | grep "net.ipv6.conf" | grep -E "accept_ra|accept_redirects|forwarding|autoconf"

# Check IPv6 privacy extensions
sysctl net.ipv6.conf.all.use_tempaddr 2>/dev/null
sysctl net.ipv6.conf.default.use_tempaddr 2>/dev/null

# Check if UFW manages IPv6
grep "IPV6" /etc/default/ufw 2>/dev/null || echo "ufw_ipv6_not_configured"
```

## Checks & Findings — IPv6 Security Matrix

### 1️⃣ IPv6 Disabled vs Enabled

| Condition | Severity | Detail |
|-----------|----------|--------|
| IPv6 disabled (disable_ipv6=1) | **PASS (Recommended)** | No IPv6 attack surface |
| IPv6 enabled, no firewall | **HIGH** | Services exposed on IPv6 without firewall |
| IPv6 enabled, firewall default ACCEPT | **HIGH** | IPv6 traffic unrestricted |

### 2️⃣ Router Advertisement (RA) Security

| Parameter | Secure Value | Severity if Wrong | Detail |
|-----------|-------------|-------------------|--------|
| accept_ra | 0 | **HIGH** | Attacker can send RA → MITM, DoS |
| accept_ra_pinfo | 0 | **MEDIUM** | RA processing enabled |
| accept_ra_defrtr | 0 | **MEDIUM** | Accept default route from RA |
| accept_ra_rtr_pref | 0 | **MEDIUM** | Router preference from RA |
| autoconf | 0 | **MEDIUM** | SLAAC address auto-config |

### 3️⃣ Redirect Security

| Parameter | Secure Value | Severity |
|-----------|-------------|----------|
| accept_redirects | 0 | **HIGH** | Attacker redirects traffic |

### 4️⃣ Forwarding / Routing

| Parameter | Secure Value | Severity |
|-----------|-------------|----------|
| forwarding | 0 (unless router) | **HIGH** | Server acting as IPv6 router |

### 5️⃣ Privacy Extensions

| Parameter | Secure Value | Severity |
|-----------|-------------|----------|
| use_tempaddr | 2 | **MEDIUM** | MAC-based EUI-64 address leaks hardware ID |
| temp_prefered_lft | 86400 | **LOW** | Temp address lifetime |

### 6️⃣ NDP (Neighbor Discovery Protocol) Hardening

| Parameter | Secure Value | Severity |
|-----------|-------------|----------|
| accept_ra (all interfaces) | 0 | **HIGH** |
| router_solicitations | 0 | **MEDIUM** |
| dad_transmits | 1 | **LOW** |

### 7️⃣ IPv6 Listening Services
- Any service listening on `::` or `::0` → **compare against profile**
- Services like SSH, web servers listening on IPv6 without firewall → **HIGH**
- Database ports (3306, 5432, 27017, 6379) on IPv6 → **CRITICAL**

## Recommended Configuration

### Option A: Disable IPv6 Entirely (Simplest, Most Secure)
```bash
cat > /etc/sysctl.d/99-disable-ipv6.conf << 'EOF'
# Disable IPv6 entirely
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
EOF
sysctl -p /etc/sysctl.d/99-disable-ipv6.conf
```
**⚠️ Warning:** Some applications (Java, certain Docker containers) may break. Test first.

### Option B: Harden IPv6 (If IPv6 Is Required)
```bash
cat > /etc/sysctl.d/99-ipv6-security.conf << 'EOF'
# IPv6 hardening (for servers that need IPv6)
net.ipv6.conf.all.accept_ra = 0
net.ipv6.conf.default.accept_ra = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0
net.ipv6.conf.all.autoconf = 0
net.ipv6.conf.default.autoconf = 0
net.ipv6.conf.all.forwarding = 0
net.ipv6.conf.default.forwarding = 0
net.ipv6.conf.all.use_tempaddr = 2
net.ipv6.conf.default.use_tempaddr = 2
net.ipv6.conf.all.accept_ra_pinfo = 0
net.ipv6.conf.default.accept_ra_pinfo = 0
net.ipv6.conf.all.accept_ra_defrtr = 0
net.ipv6.conf.default.accept_ra_defrtr = 0
net.ipv6.conf.all.accept_ra_rtr_pref = 0
net.ipv6.conf.default.accept_ra_rtr_pref = 0
net.ipv6.conf.all.router_solicitations = 0
net.ipv6.conf.default.router_solicitations = 0
net.ipv6.conf.all.dad_transmits = 1
net.ipv6.conf.default.dad_transmits = 1
EOF
sysctl -p /etc/sysctl.d/99-ipv6-security.conf
```

### Option C: IPv6 Firewall Rules (With ip6tables)
```bash
# Default deny incoming, allow outgoing
ip6tables -P INPUT DROP
ip6tables -P FORWARD DROP
ip6tables -P OUTPUT ACCEPT
ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A INPUT -i lo -j ACCEPT
ip6tables -A INPUT -p ipv6-icmp -j ACCEPT
# Allow specific services (SSH, HTTP, etc.)
ip6tables -A INPUT -p tcp --dport 22 -j ACCEPT
# Save rules
ip6tables-save > /etc/iptables/rules.v6
```

## Auto-Fix Eligible (Confirm Required)
- Disable IPv6 if server doesn't need it → apply Option A
- Fix accept_redirects=1 → apply Option B sysctl
- Fix accept_ra=1 → apply Option B

## Output Format
```
[HIGH] 26-ipv6: ra_accept_enabled | net.ipv6.conf.all.accept_ra=1 | risk: RA spoofing/MITM | action_id: ACT-YYYYMMDD-XXX
[HIGH] 26-ipv6: no_ip6tables_firewall | IPv6 enabled but ip6tables not present | services exposed on IPv6 | action_id: ACT-YYYYMMDD-XXX
[HIGH] 26-ipv6: redirects_enabled | net.ipv6.conf.all.accept_redirects=1 | action_id: ACT-YYYYMMDD-XXX
[HIGH] 26-ipv6: forwarding_enabled | net.ipv6.conf.all.forwarding=1 | not a router | action_id: ACT-YYYYMMDD-XXX
[CRITICAL] 26-ipv6: database_on_ipv6 | port 27017 listening on :: | MongoDB exposed on IPv6 without firewall | action_id: ACT-YYYYMMDD-XXX
[MEDIUM] 26-ipv6: eui64_privacy | use_tempaddr=0 | MAC address exposed in IPv6 address | action_id: ACT-YYYYMMDD-XXX
[PASS] 26-ipv6: ipv6_disabled | net.ipv6.conf.all.disable_ipv6=1 ✓
[PASS] 26-ipv6: hardened | all accept_ra=0, accept_redirects=0, firewall active ✓
[INFO] 26-ipv6: summary | IPv6: enabled | RA: blocked | redirects: blocked | forwarding: 0 | services on IPv6: 3 | firewall: active
```
