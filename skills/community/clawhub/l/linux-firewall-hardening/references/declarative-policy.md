# Declarative Firewall Policy

This document defines a machine-readable YAML schema for expressing firewall policy independent of the backend implementation. AI agents and CI/CD pipelines can use this schema to generate backend-specific configurations for ufw, firewalld, nftables, and iptables.

## Design Principles

1. **Backend-agnostic**: The policy describes intent, not implementation.
2. **Idempotent by design**: Rendering the same policy twice produces the same ruleset.
3. **Atomic application**: Rendered output uses atomic replace (`iptables-restore`, `nft -f`) where possible.
4. **Validation-integrated**: The policy includes success criteria that the verifier uses.
5. **Fail hard on unknown fields**: Unrecognized schema keys or unsupported feature/backend combinations produce an error, not silent ignorance. This prevents the dangerous assumption that a field was processed when it wasn't.

## Schema Version

Current version: **2.0**. Renderers must refuse to process policies with a higher major version.

| Version | Changes |
|---------|---------|
| 1.0 | Initial schema (deprecated) |
| 2.0 | Added `schema_version`, `metadata` block. Hard-fail on unknown fields. Added `backend_compat` field-level hints. |

## JSON Schema

A formal JSON Schema for validation is available at `references/policy-schema.json`. Renderers should validate policy input against this schema before rendering.

## Schema

```yaml
schema_version: "2.0"          # Required. Must be exactly "2.0".
metadata:                       # Optional. Tagging and auditing.
  name: "web-server-policy"
  description: "Public web server firewall policy"
  author: "ops-team"
  last_modified: "2026-05-11"

backend: auto                   # Optional. auto | ufw | firewalld | nftables | iptables
                                # "auto" detects and picks the best available backend.
                                # Explicit backend restricts rendering to that target.

inbound:
  default: deny                 # Required. deny | accept
  rules:
    - proto: tcp                # tcp | udp | icmp | icmpv6 | any
      port: 22                  # integer or "any"
      action: accept            # accept | drop | reject
      source: any               # any | CIDR | [CIDR, CIDR]
      rate_limit: "10/min"      # Optional. e.g. "10/min", "3/sec"
      comment: "SSH access"     # Optional. Maps to log prefix or rule comment
      backend_compat:           # Optional. Override which backends support this rule.
        ufw: true               # Default: true for all. Set false to skip.
        firewalld: true
        nftables: true
        iptables: true

    - proto: tcp
      port: 443
      action: accept
      source: any

    - proto: udp
      port: 53
      action: accept
      source: "10.0.0.0/8"

outbound:
  default: accept               # Required. deny | accept
  rules: []                     # Optional. Same structure as inbound

forward:
  default: deny                 # Required. deny | accept

icmp:
  ipv4: accept                  # accept | deny
  ipv6: accept                  # accept | deny

logging:
  dropped: true                 # Log dropped packets
  rate_limit: "5/sec"           # Prevent log flood
  prefix: "fw-drop"             # Log prefix string

validation:
  ssh_must_reachable: true
  intended_ports_only: true
  ipv6_symmetric: true
  rules_persist_after_reboot: true
```

## Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | Yes | Schema version. Current: `"2.0"` |
| `metadata` | map | No | Human-readable tagging (name, description, author, last_modified) |
| `backend` | enum | No | Target backend: `auto`, `ufw`, `firewalld`, `nftables`, `iptables`. Default: `auto` |
| `inbound.default` | enum | Yes | `deny` or `accept` |
| `inbound.rules` | list | No | Ordered list of allow/deny rules |
| `outbound.default` | enum | Yes | `deny` or `accept` |
| `outbound.rules` | list | No | Ordered list of allow/deny rules |
| `forward.default` | enum | Yes | `deny` or `accept` |
| `icmp.ipv4` | enum | Yes | `accept` or `deny` |
| `icmp.ipv6` | enum | Yes | `accept` or `deny` |
| `logging.dropped` | bool | No | Whether to log dropped packets |
| `logging.rate_limit` | string | No | Rate limit for log entries |
| `logging.prefix` | string | No | Prefix string for log lines |
| `validation` | map | No | Success criteria flags |

## Rule Object

```yaml
- proto: tcp              # Required: tcp | udp | icmp | icmpv6 | any
  port: 80                # Required for tcp/udp: integer or "any"
  action: accept          # Required: accept | drop | reject
  source: any             # Optional: any (default) | CIDR | list of CIDRs
  rate_limit: "10/min"    # Optional: rate string
  comment: "HTTP"         # Optional: human description
  backend_compat:         # Optional: per-backend enable/disable
    ufw: true
    firewalld: false      # Skip this rule on firewalld
    nftables: true
    iptables: true
```

## Backend Feature Differences

Not all features are available on all backends. The renderer must hard-fail when a requested feature is unsupported for the target backend, rather than silently ignoring it.

| Feature | ufw | firewalld | nftables | iptables |
|---------|-----|-----------|----------|----------|
| Rate limiting | Yes (ufw limit) | Yes (rich rule) | Yes (limit rate) | Yes (recent + hashlimit) |
| Source CIDR restriction | Yes | Yes | Yes | Yes |
| Source range (list of CIDRs) | Yes | Yes (multiple rich rules) | Yes (concatenated) | Yes (multiple rules) |
| Logging dropped packets | Yes (built-in) | Yes (--set-log-denied) | Yes (log statement) | Yes (LOG target) |
| Custom log prefix | No | No | Yes | Yes |
| IPv6 (same ruleset as IPv4) | Yes | Yes (separate zone) | Yes (inet family) | No (separate ip6tables) |
| Sets/maps for port groups | No | No | Yes | No (use multiport) |
| Connection tracking state | No (implicit) | Yes (rich rule) | Yes (ct state) | Yes (conntrack) |
| Atomic ruleset replacement | No | Yes (--reload) | Yes (nft -f) | Yes (iptables-restore) |
| Zone-based rules | No | Yes | No | No |

## Validation Rules

Renderers MUST apply these validation rules before rendering:

1. **Unknown top-level keys**: If the policy contains keys not in the schema, fail with error listing the unknown keys.
2. **Unknown rule fields**: If a rule object contains fields not in the rule schema, fail.
3. **Unsupported feature for target backend**: If a rule uses a feature (e.g., custom log prefix) and `backend_compat` is not explicitly set to `false` for that backend, fail with a message like: "log_prefix is not supported on ufw. Set `backend_compat.ufw: false` to skip this rule, or remove the unsupported field."
4. **Missing required fields**: Fail if `inbound.default`, `outbound.default`, `forward.default`, `icmp.ipv4`, or `icmp.ipv6` are missing.
5. **Invalid action values**: Fail if `action` is not one of `accept`, `drop`, `reject`.
6. **Schema version mismatch**: Fail if `schema_version` major version is higher than the renderer supports.

## Rendering to Backends

### ufw Renderer

```bash
# Generated from policy inbound.default = deny
sudo ufw --force default deny incoming
sudo ufw --force default allow outgoing

# Rule: proto=tcp port=22 action=accept
sudo ufw allow 22/tcp

# Rule: proto=tcp port=22 rate_limit="10/min"
sudo ufw limit 22/tcp

# Rule: proto=tcp port=443 action=accept
sudo ufw allow 443/tcp

# Rule: proto=udp port=53 source="10.0.0.0/8"
sudo ufw allow from 10.0.0.0/8 to any port 53 proto udp
```

### firewalld Renderer

```bash
ZONE=$(sudo firewall-cmd --get-default-zone)

# Service rules map to --add-service if known, else --add-port
sudo firewall-cmd --permanent --zone="$ZONE" --add-service=ssh
sudo firewall-cmd --permanent --zone="$ZONE" --add-service=https

# Rate limit maps to rich rule
sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule='rule service name=ssh limit value=10/min accept'

# Source restriction maps to rich rule
sudo firewall-cmd --permanent --zone="$ZONE" --add-rich-rule='rule family=ipv4 source address=10.0.0.0/8 port port=53 protocol=udp accept'

sudo firewall-cmd --reload
```

### nftables Renderer

```nft
#!/usr/sbin/nft -f

table inet filter {
    set allowed_tcp_ports {
        type inet_service
        flags interval
        elements = { 22, 443 }
    }

    chain input {
        type filter hook input priority 0; policy drop;

        iif lo accept
        ct state established,related accept
        ct state invalid drop

        ip protocol icmp accept
        ip6 nexthdr icmpv6 accept

        # Source-restricted UDP
        ip saddr 10.0.0.0/8 udp dport 53 accept

        # Allowed TCP ports from set
        tcp dport @allowed_tcp_ports accept

        # Rate-limited SSH
        tcp dport 22 ct state new limit rate 10/minute accept

        # Logging
        log prefix "fw-drop: " limit rate 5/second
        drop
    }

    chain forward { type filter hook forward priority 0; policy drop; }
    chain output  { type filter hook output  priority 0; policy accept; }
}
```

### iptables Renderer

**IPv4** (`iptables-v4.rules`):
```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT -s 10.0.0.0/8 -p udp --dport 53 -j ACCEPT
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT
COMMIT
```

**IPv6** (`iptables-v6.rules`):
```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p icmpv6 -j ACCEPT
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -p tcp --dport 443 -j ACCEPT
COMMIT
```

Apply:
```bash
sudo iptables-restore --test /tmp/iptables-v4.rules && sudo iptables-restore /tmp/iptables-v4.rules
sudo ip6tables-restore --test /tmp/iptables-v6.rules && sudo ip6tables-restore /tmp/iptables-v6.rules
```

## Golden Test Fixtures

These test fixtures verify that the policy renderer produces the expected output for each backend. Run these after any renderer change.

### Fixture: public-web-server -> ufw

**Input** (`fixtures/public-web-server.yaml`):
```yaml
schema_version: "2.0"
inbound:
  default: deny
  rules:
    - proto: tcp
      port: 22
      action: accept
      rate_limit: "10/min"
    - proto: tcp
      port: 80
      action: accept
    - proto: tcp
      port: 443
      action: accept
outbound:
  default: accept
forward:
  default: deny
icmp:
  ipv4: accept
  ipv6: accept
logging:
  dropped: true
  rate_limit: "5/sec"
```

**Expected ufw output** (`fixtures/public-web-server.ufw.expected`):
```
sudo ufw --force default deny incoming
sudo ufw --force default allow outgoing
sudo ufw limit 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```

### Fixture: public-web-server -> nftables

**Expected nftables output** (`fixtures/public-web-server.nftables.expected`):
```nft
#!/usr/sbin/nft -f
table inet filter {
    set allowed_tcp_ports {
        type inet_service
        flags interval
        elements = { 22, 80, 443 }
    }
    chain input {
        type filter hook input priority 0; policy drop
        iif lo accept
        ct state established,related accept
        ct state invalid drop
        ip protocol icmp accept
        ip6 nexthdr icmpv6 accept
        tcp dport @allowed_tcp_ports accept
        tcp dport 22 ct state new limit rate 10/minute accept
        log prefix "fw-drop: " limit rate 5/second
        drop
    }
    chain forward { type filter hook forward priority 0; policy drop }
    chain output { type filter hook output priority 0; policy accept }
}
```

### Fixture: bastion-host -> iptables (v4)

**Input** (`fixtures/bastion-host.yaml`):
```yaml
schema_version: "2.0"
inbound:
  default: deny
  rules:
    - proto: tcp
      port: 22
      action: accept
      rate_limit: "5/min"
outbound:
  default: accept
forward:
  default: deny
icmp:
  ipv4: accept
  ipv6: accept
logging:
  dropped: true
  rate_limit: "5/sec"
  prefix: "bastion-drop"
```

**Expected iptables v4 output** (`fixtures/bastion-host.iptables-v4.expected`):
```
*filter
:INPUT DROP [0:0]
:FORWARD DROP [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -i lo -j ACCEPT
-A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
-A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --set
-A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -m recent --update --seconds 60 --hitcount 6 -j DROP
-A INPUT -p tcp --dport 22 -j ACCEPT
-A INPUT -m limit --limit 5/sec -j LOG --log-prefix "bastion-drop: "
COMMIT
```

## Example Policies

### Public Web Server (v2.0)

```yaml
schema_version: "2.0"
metadata:
  name: "public-web-server"
  description: "Standard web server with SSH, HTTP, HTTPS"

backend: auto

inbound:
  default: deny
  rules:
    - proto: tcp
      port: 22
      action: accept
      rate_limit: "10/min"
      comment: "SSH rate-limited"
    - proto: tcp
      port: 80
      action: accept
    - proto: tcp
      port: 443
      action: accept

outbound:
  default: accept

forward:
  default: deny

icmp:
  ipv4: accept
  ipv6: accept

logging:
  dropped: true
  rate_limit: "5/sec"
  prefix: "fw-drop"
```

### Bastion Host (v2.0)

```yaml
schema_version: "2.0"
metadata:
  name: "bastion-host"
  description: "SSH-only jump box with aggressive rate limiting"

inbound:
  default: deny
  rules:
    - proto: tcp
      port: 22
      action: accept
      rate_limit: "5/min"

outbound:
  default: accept

forward:
  default: deny

icmp:
  ipv4: accept
  ipv6: accept

logging:
  dropped: true
  rate_limit: "5/sec"
```

### Internal Database (v2.0)

```yaml
schema_version: "2.0"
inbound:
  default: deny
  rules:
    - proto: tcp
      port: 22
      action: accept
      source: "10.0.1.0/24"
    - proto: tcp
      port: 3306
      action: accept
      source: "10.0.2.0/24"

outbound:
  default: accept

forward:
  default: deny

icmp:
  ipv4: accept
  ipv6: accept
```

### Zero Trust Node (v2.0)

```yaml
schema_version: "2.0"
metadata:
  name: "zero-trust-node"
  description: "Default deny all inbound and outbound with explicit allowlist"

inbound:
  default: deny
  rules:
    - proto: tcp
      port: 22
      action: accept
      source: "10.0.1.0/24"

outbound:
  default: deny
  rules:
    - proto: udp
      port: 53
      action: accept
    - proto: udp
      port: 123
      action: accept
    - proto: tcp
      port: 80
      action: accept
    - proto: tcp
      port: 443
      action: accept

forward:
  default: deny

icmp:
  ipv4: accept
  ipv6: accept
```

## Future Enhancements

- GeoIP restrictions (`source_geo: ["US", "CA"]`)
- Time-based rules (`time_range: "09:00-17:00"`)
- Connection limits (`max_connections: 100`)
- Custom chains and forwarding rules for complex topologies
- Integration with cloud security group APIs (AWS, GCP, Azure)
- Policy diff tool (compare two policies, show backend-specific rule differences)
- `hermes skill render-policy` CLI command to validate and render a policy file
