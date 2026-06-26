# Observability & Performance

## nftables Counters

```bash
# Per-rule counters and handles
sudo nft list ruleset -a
sudo nft list chain inet filter input
```

## Connection Tracking

```bash
cat /proc/sys/net/netfilter/nf_conntrack_count
cat /proc/sys/net/netfilter/nf_conntrack_max

sudo conntrack -L 2>/dev/null | wc -l

echo "Conntrack usage: $(cat /proc/sys/net/netfilter/nf_conntrack_count) / $(cat /proc/sys/net/netfilter/nf_conntrack_max)"
```

## Dropped Packet Monitoring

```bash
# ufw
sudo tail -f /var/log/ufw.log

# iptables LOG target
sudo dmesg | grep -i "iptables\\|nf_log"

# nftables log prefix
sudo journalctl -k -f | grep "nft-drop"
```

## fail2ban Metrics

```bash
sudo fail2ban-client status
sudo fail2ban-client status sshd
grep "Ban" /var/log/fail2ban.log 2>/dev/null | tail -20
```

## Recommended Baselines

Record after hardening:
- `nf_conntrack_count` at idle and peak load
- `nft list ruleset` counter values after 24h
- UFW log volume per hour
- fail2ban ban rate per day

## Performance Risks

| Risk | Symptom | Mitigation |
|------|---------|------------|
| **conntrack exhaustion** | `nf_conntrack: table full` | Increase max or use stateless rules |
| **logging flood** | syslog high CPU, disk full | Always `limit rate` on log rules |
| **huge ipsets** | Slow rule evaluation | Use `flags interval`, split sets |
| **SYN flood** | High half-open connections | Enable `tcp_syncookies`, use SYNPROXY |
| **rule evaluation order** | High CPU per packet | Place most-hit rules early |

## Kernel Tuning

```bash
# Enable reverse path filtering
sudo sysctl -w net.ipv4.conf.all.rp_filter=1
# Enable SYN cookies
sudo sysctl -w net.ipv4.tcp_syncookies=1
# Ignore redirects
sudo sysctl -w net.ipv4.conf.all.accept_redirects=0
sudo sysctl -w net.ipv6.conf.all.accept_redirects=0
# Persist
sudo tee -a /etc/sysctl.d/99-firewall-hardening.conf << 'EOF'
net.ipv4.conf.all.rp_filter=1
net.ipv4.conf.default.rp_filter=1
net.ipv4.tcp_syncookies=1
net.ipv4.conf.all.accept_redirects=0
net.ipv6.conf.all.accept_redirects=0
net.ipv4.icmp_echo_ignore_broadcasts=1
EOF
sudo sysctl --system
```

> **Warning**: sysctl changes affect the entire TCP/IP stack. Test on non-production first. Never change sysctl hardening values on K8s/CNI hosts without explicit CNI profile support.
