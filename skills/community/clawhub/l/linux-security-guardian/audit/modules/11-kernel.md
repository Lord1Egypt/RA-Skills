# Module 11 — Kernel Security Parameters

## Commands
```bash
# Read all relevant sysctl values
sysctl -a 2>/dev/null | grep -E "net.ipv4|net.ipv6|kernel|fs.suid"

# Key individual checks:
sysctl net.ipv4.ip_forward
sysctl net.ipv4.conf.all.accept_redirects
sysctl net.ipv4.conf.all.send_redirects
sysctl net.ipv4.conf.all.accept_source_route
sysctl net.ipv4.conf.all.log_martians
sysctl net.ipv4.tcp_syncookies
sysctl net.ipv4.icmp_echo_ignore_broadcasts
sysctl kernel.randomize_va_space
sysctl kernel.dmesg_restrict
sysctl kernel.kptr_restrict
sysctl kernel.sysrq
sysctl fs.suid_dumpable
sysctl net.ipv6.conf.all.accept_redirects
```

## Checks — 15 Critical Kernel Parameters

| Parameter | Secure Value | Severity if Wrong |
|---|---|---|
| net.ipv4.ip_forward | 0 (unless router) | MEDIUM |
| net.ipv4.conf.all.accept_redirects | 0 | MEDIUM |
| net.ipv4.conf.all.send_redirects | 0 | MEDIUM |
| net.ipv4.conf.all.accept_source_route | 0 | MEDIUM |
| net.ipv4.conf.all.log_martians | 1 | LOW |
| net.ipv4.tcp_syncookies | 1 | HIGH (SYN flood protection) |
| net.ipv4.icmp_echo_ignore_broadcasts | 1 | LOW |
| kernel.randomize_va_space | 2 | HIGH (ASLR must be full) |
| kernel.dmesg_restrict | 1 | MEDIUM |
| kernel.kptr_restrict | 2 | MEDIUM |
| kernel.sysrq | 0 | LOW |
| fs.suid_dumpable | 0 | MEDIUM |
| net.ipv6.conf.all.accept_redirects | 0 | MEDIUM |
| net.ipv4.conf.default.rp_filter | 1 | MEDIUM |
| net.ipv4.conf.all.rp_filter | 1 | MEDIUM |

## For Each Wrong Value
- Generate proposed sysctl fix
- Write to /etc/sysctl.d/99-security-hardening.conf (proposed)
- Confirm required before applying

## Output Format
```
[HIGH] 11-kernel: aslr_disabled | kernel.randomize_va_space=1 | expected: 2 | action_id: ACT-XXX
[MEDIUM] 11-kernel: accept_redirects | net.ipv4.conf.all.accept_redirects=1 | action_id: ACT-YYY
[PASS] 11-kernel: tcp_syncookies | value: 1 ✓
```
