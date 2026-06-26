# Compliance Mapping

This skill's hardening practices map to common security standards. Use for audit evidence.

| Control | CIS Benchmark | PCI-DSS | SOC2 | How This Skill Relates |
|---------|--------------|---------|------|--------------------------|
| Default deny inbound | CIS 3.5.1.x | Req 1.3 | CC6.1 | Automated detection and enforcement |
| Restrict outbound | CIS 3.5.2.x | Req 1.3 | CC6.1 | Supports evidence collection and rule generation |
| Disable unused ports | CIS 2.1.x | Req 2.2 | CC6.2 | Exposure analysis mapping |
| Rate-limit SSH | CIS 5.2.x | Req 1.2 | CC6.1 | Idempotent rate-limit patterns |
| Backup before change | CIS 3.4 | Req 12.10 | CC7.2 | Automated backup and rollback |
| IPv6 symmetric policy | CIS 3.5.3.x | Req 1.3 | CC6.1 | IPv4/IPv6 symmetry validation |
| Log dropped packets | CIS 3.5.1.x | Req 10.2 | CC7.2 | Rate-limited logging |
| fail2ban / intrusion prev | CIS 5.2.x | Req 1.2 | CC6.1 | Backend alignment and verification |
| Docker port exposure | CIS 4.1.x | Req 1.3 | CC6.1 | DOCKER-USER chain enforcement |
| Kernel hardening | CIS 3.3.x | Req 2.2 | CC6.1 | Guard against CNI mutations |

**Note**: Specific control numbers vary by benchmark version (CIS v2.x, v3.x). Always reference the latest version applicable to your OS.
