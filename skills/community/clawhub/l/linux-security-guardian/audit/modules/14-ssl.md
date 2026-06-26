# Module 14 — SSL/TLS Certificate Check

## Commands
```bash
# Check certificate expiry for each domain in SERVER_PROFILE.md
# For each domain:
echo | openssl s_client -connect <domain>:443 -servername <domain> 2>/dev/null \
  | openssl x509 -noout -dates 2>/dev/null

# Local certs (nginx/apache config)
grep -r "ssl_certificate\|SSLCertificateFile" /etc/nginx/ /etc/apache2/ 2>/dev/null | grep -v ".key"
# For each cert file found:
openssl x509 -in <cert-file> -noout -dates -subject 2>/dev/null

# Check TLS version (deprecated TLS 1.0/1.1)
openssl s_client -connect <domain>:443 -tls1 2>&1 | grep "Protocol"
openssl s_client -connect <domain>:443 -tls1_1 2>&1 | grep "Protocol"

# Check for weak ciphers
nmap --script ssl-enum-ciphers -p 443 <domain> 2>/dev/null | head -30
```

## Checks & Findings

### Cert Expiry
- > 30 days remaining → PASS
- 15-30 days → MEDIUM (plan renewal)
- 7-15 days → HIGH (urgent renewal)
- < 7 days → CRITICAL (immediate renewal)
- Expired → CRITICAL (service broken)

### TLS Version
- TLS 1.0 or 1.1 accepting connections → HIGH
- SSLv3 accepting → CRITICAL

### Cert for Right Domain
- CN mismatch → HIGH

## Update soul [SSL CERTIFICATES] with results

## Output Format
```
[CRITICAL] 14-ssl: cert_expired | domain: api.example.com | expired: 2025-01-01
[HIGH] 14-ssl: cert_expiring | domain: example.com | expires_in: 12 days
[PASS] 14-ssl: cert_valid | domain: app.example.com | expires: 2026-06-15 (180 days)
```
