# Security & Hardening

## Security Domains
1. **Host Security** — OS hardening, firewall, SSH, updates
2. **Application Security** — Code review, dependency scanning
3. **Network Security** — Port scanning, traffic analysis
4. **Data Security** — Encryption, secrets management
5. **Access Control** — Authentication, authorization, MFA

## Tools

### Host Security (Use `healthcheck` skill)
- Firewall: iptables, nftables, ufw
- SSH hardening: key-only auth, disable root, fail2ban
- Updates: apt upgrade, unattended-upgrades
- Audit: Lynis, OpenSCAP

### Network Tools
```bash
ss -tlnp                    # Open ports
nmap localhost              # Port scan
curl -I https://example.com # HTTP security headers
openssl s_client -connect host:443  # TLS inspection
```

### Secrets Management
- 1Password CLI (`op`) for secret storage
- Environment variables for runtime secrets
- Never commit secrets to git
- Use `.env` files with `.gitignore`

### Code Security
- Dependency scanning: `npm audit`, `pip-audit`
- Static analysis: semgrep, bandit (Python)
- Secret detection: trufflehog, gitleaks

## Security Checklist
- [ ] All services on latest versions
- [ ] Firewall configured (deny by default)
- [ ] SSH key-only authentication
- [ ] No default passwords
- [ ] TLS/SSL on all web services
- [ ] Secrets in vault, not code
- [ ] Regular security updates
- [ ] Logging and monitoring enabled
- [ ] Backups encrypted and tested
- [ ] Access audit trail maintained

## Incident Response
1. Identify the breach
2. Contain the damage
3. Eradicate the threat
4. Recover systems
5. Document lessons learned

## OpenClaw-Specific
- Gateway tokens use HMAC
- Loopback-only binding on KiloClaw
- Per-user token isolation
- See: https://blog.kilo.ai/p/how-kiloclaw-is-built-to-be-secure
