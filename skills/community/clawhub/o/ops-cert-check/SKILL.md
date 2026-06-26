---
name: ops-cert-check
description: SSL/TLS Certificate Check & Renewal SOP. Covers certificate validation (PEM/CRT/JKS), Nginx certificate update, Let's Encrypt wildcard application, and emergency response for expired certificates.
triggers:
  - "ssl certificate"
  - "tls certificate"
  - "certificate expired"
  - "https certificate"
  - "jks certificate"
  - "lets encrypt"
  - "wildcard certificate"
  - "certbot"
  - "nginx ssl"
  - "certificate renewal"
category: ops
tags: [ssl, tls, certificate, nginx, certbot, lets-encrypt, security]
version: 1.0.0
created: 2026-05-06
---

# SSL/TLS Certificate Check & Renewal SOP

## Scenario 1: Validate Existing Certificate

### Method A: Linux OpenSSL (Recommended)
```bash
# Check PEM/CRT certificate
openssl x509 -in certificate.crt -noout -dates

# Check JKS certificate
keytool -list -v -keystore keystore.jks -storepass <password>
```

### Method B: Online Verification
Open the certificate file directly in browser to view validity period and issuer.

### Method C: Remote Check via Request
```bash
# Check Nginx certificate (port 443)
echo "" | openssl s_client -connect domain:443 -servername domain 2>/dev/null | openssl x509 -noout -dates

# Check game server JKS certificate (port +3 offset)
echo "" | openssl s_client -connect game.domain:port+3 2>/dev/null | openssl x509 -noout -dates
```

---

## Scenario 2: Nginx Certificate Update (Standard Flow)

Applicable to: Web services, reverse proxies, CDN frontends, and any Nginx-hosted SSL termination.

### Standard Steps

**1. Replace certificate files**
Login to target server, replace files in `/etc/nginx/ssl/`:
- Certificate file (`.crt`)
- Certificate key file (`.key`)

**2. Validate configuration**
```bash
nginx -t
```

**3. Reload Nginx**
```bash
nginx -s reload
```

**4. Verify the update**
Send HTTP/HTTPS request to confirm the new certificate is being served.

**5. Update certificate monitoring records**
Login to ops backend → Asset Management → Domain Assets → Domain Monitoring → Add record → Upload new certificate.

**6. Commit to version control**
> ⚠️ **禁止将 `.key` 私钥文件提交到版本库**。私钥应保留在服务器安全路径（如 `/etc/nginx/ssl/`）或密钥管理系统中。仅提交证书文件（`.crt`）或元数据。

Submit updated certificates to the version control repository.

### Role Responsibilities

| Role | Scope |
|------|-------|
| Ops/Infra | Replace Nginx certificates, validate, reload, update monitoring |
| Third-party vendor | Cloud services, load balancers, middleware certificates |

---

## Scenario 3: Game Server JKS Certificate Update

Applicable to: Java-based game servers that use JKS (Java KeyStore) format certificates.

### Flow

```
Ops provides certificate and private key
         ↓
Dev team compiles into Java certificate (JKS)
         ↓
Ops uploads JKS to ops server
         ↓
Game server auto-replaces on next update
         ↓
Verify: request game server domain on port+3
```

### JKS Certificate Verification
```bash
keytool -list -v -keystore game.jks -storepass <password>
```

---

## Scenario 4: Let's Encrypt Wildcard Certificate

Applicable to: Self-managed services using Let's Encrypt certificates (e.g., internal tools, dev environments, small-scale deployments).

### Prerequisites
- Linux server with internet access
- Root/sudo access
- Domain DNS already pointing to the server
- DNS provider with API access (Alibaba Cloud DNS, Cloudflare, Route53, etc.)

### DNS-01 Challenge for Wildcard
```bash
# Install certbot with DNS plugin (Alibaba Cloud example)
yum install -y certbot-dns-aliyun

# Configure Alibaba Cloud CLI authentication
# Reference: https://help.aliyun.com/zh/cli/configure-credentials

# Apply for wildcard certificate
certbot certonly \
  --manual \
  --preferred-challenges dns \
  --dns-aliyun \
  -d "*.example.com" \
  -d "example.com"
```

For other DNS providers, use the corresponding plugin:
- Cloudflare: `certbot-dns-cloudflare`
- Route53: `certbot-dns-route53`
- Generic: `--manual --preferred-challenges dns`

### Install Certificate on Nginx
```bash
# Switch to cert directory
cd /etc/letsencrypt

# Generate DH parameters (enhanced security)
openssl dhparam -out dhparam.pem 2048

# Add SSL configuration
vim /etc/letsencrypt/options-ssl-nginx.conf

# Configure Nginx
# ... add ssl_certificate, ssl_certificate_key, etc. ...

# Reload Nginx
nginx -s reload
```

### Auto-Renewal
```bash
# Set up cron job (runs every 2 days)
crontab -e
# 0 0 */2 * * certbot renew --deploy-hook "/root/your-hook.sh"

# Manual dry-run (doesn't actually renew)
certbot renew --dry-run
```

**Note**: Let's Encrypt certificates are valid for 90 days. `certbot renew` only actually renews within 30 days of expiry.

---

## Scenario 5: Expired Certificate Emergency Response

**Emergency**: Certificate expired, business impacted (e.g., payments failing, users locked out).

**Immediate actions**:
1. Identify which domains are affected: `openssl s_client -connect domain:443`
2. Contact responsible party (internal team or third-party vendor)
3. Replace certificate file and reload: `nginx -s reload`
4. Notify stakeholders of recovery

**Prevention**:
- Monitoring alerts + notification (Slack/email/PagerDuty, etc.)
- Cron job with certificate expiry check
- Alert 30 days before expiry

---

## Certificate Quick Reference

| Item | Type | Renewal | Notes |
|------|------|---------|-------|
| Project certificate (purchased) | Commercial CA | Vendor/Third-party | Contact issuer directly |
| JKS certificate | Java KeyStore | Dev team compiles | Ops uploads to server |
| Let's Encrypt | ACME | certbot auto-renewal | 90-day validity |
| Wildcard certificate | DNS-validated | certbot with DNS plugin | Required for `*.domain.com` |

---

## Command Cheatsheet

```bash
# Check certificate validity
openssl x509 -in cert.crt -noout -dates

# Check JKS certificate
keytool -list -v -keystore game.jks

# Nginx config test
nginx -t

# Reload Nginx
nginx -s reload

# Apply Let's Encrypt (DNS challenge)
certbot certonly --manual --preferred-challenges dns -d "*.domain.com"

# Auto-renewal dry-run
certbot renew --dry-run

# Check remote certificate
echo "" | openssl s_client -connect domain:443 -servername domain 2>/dev/null | openssl x509 -noout -dates
```

---

## Notes

1. **JKS certificate update requires dev team involvement** — ops cannot do this alone
2. **Third-party vendor projects** typically have the vendor handle certificate renewal
3. **Let's Encrypt certificates are 90 days** — auto-renewal must be configured
4. **Game server certificates and Nginx certificates are separate** — game servers use JKS, Nginx uses PEM/CRT
5. **certbot certificate path**: `/etc/letsencrypt/live/domain/`
