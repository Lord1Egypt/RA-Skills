# Module 08 — Network Audit

## Commands
```bash
# All listening ports and which process
ss -tulpn
# Alternative: netstat -tulpn

# Active connections
ss -tnp | grep ESTABLISHED | head -20

# Network interfaces
ip addr show
ip link show

# Routing table
ip route

# ARP table (unexpected entries?)
arp -n

# DNS config
cat /resolv.conf 2>/dev/null || cat /etc/resolv.conf

# Check for promiscuous mode (sniffing)
ip link | grep PROMISC

# Network sockets stats
ss -s
```

## Checks & Findings

### Unexpected Open Ports
- Compare ss output against SERVER_PROFILE.md expected ports
- Any unlisted port open on 0.0.0.0 or :: → HIGH
- Queue firewall rule to close: FW-YYYYMMDD-NNN

### Management Ports on Public Interface
- SSH (22) or database ports (3306, 5432, 27017) on 0.0.0.0 → HIGH
- Should be bound to 127.0.0.1 or private IP

### Promiscuous Mode
- Any interface in promiscuous mode → HIGH (possible packet sniffing)

### Unexpected Active Connections
- Outbound connections to unknown external IPs → MEDIUM
- Long-lived connections to suspicious IPs → HIGH

### IP Forwarding
- cat /proc/sys/net/ipv4/ip_forward
- Enabled when not expected → MEDIUM

### IPv6 Management
- IPv6 enabled but not managed → MEDIUM advisory

## Output Format
```
[HIGH] 08-network: unexpected_port | port: 8080 | process: python3 | bound: 0.0.0.0 | action: FW-XXX confirm
[PASS] 08-network: expected_ports | all ports match profile
```
