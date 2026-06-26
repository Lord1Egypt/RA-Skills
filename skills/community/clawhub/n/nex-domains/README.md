# Nex Domains

DNS & Domain Portfolio Manager - Track domains, monitor SSL certificates, manage DNS records, and stay on top of renewals across multiple registrars.

**Built by Nex AI** | [nex-ai.be](https://nex-ai.be)

## Overview

Nex Domains is a command-line tool for managing domain portfolios across multiple registrars (Cloudflare, TransIP, etc.). Track domain expiry dates, SSL certificate validity, DNS records, and maintain a centralized database of all your domains and their metadata.

Perfect for:
- Domain managers and registrars
- DevOps teams with multi-domain infrastructure
- Web agencies managing client domains
- System administrators tracking domain portfolio

## Key Features

- **Multi-registrar support**: Cloudflare, TransIP, and others
- **Domain tracking**: Registration date, expiry, auto-renewal status, monthly cost
- **SSL monitoring**: Certificate expiry alerts and issuer tracking
- **DNS management**: View, search, and manage DNS records
- **WHOIS lookups**: Get registrar and nameserver info
- **Health checks**: HTTP/HTTPS validation and DNS resolution
- **Cloudflare sync**: Import all zones and DNS records with one command
- **Client tracking**: Organize domains by client/organization
- **Portfolio analytics**: Statistics, costs, expiring domains
- **Export**: CSV and JSON exports for analysis

## Installation

### Requirements

- Python 3.9+
- `whois` command-line tool
- `dig` (bind-utils/dnsutils)
- `openssl`

### Quick Setup

```bash
bash setup.sh
```

This will:
1. Create a data directory at `~/.nex-domains/`
2. Initialize the SQLite database
3. Install the `nex-domains` CLI command
4. Check for required tools

### Platform-Specific Installation

#### Ubuntu/Debian

```bash
sudo apt install whois dnsutils openssl
bash setup.sh
```

#### macOS

```bash
brew install whois bind
bash setup.sh
```

#### CentOS/RHEL

```bash
sudo yum install bind-utils openssl
sudo yum install whois  # or install separately
bash setup.sh
```

## Quick Start

```bash
# Add a domain
nex-domains add example.com --registrar cloudflare --client "Acme Corp" --auto-renew

# Scan for complete information
nex-domains scan example.com

# List all domains
nex-domains list

# Show domains expiring in 90 days
nex-domains expiring

# Sync Cloudflare domains (requires CF_API_TOKEN env var)
nex-domains sync

# Show portfolio statistics
nex-domains stats
```

## Usage

```
nex-domains add DOMAIN --registrar {cloudflare|transip|other} [--client NAME] [--auto-renew] [--monthly-cost COST] [--notes TEXT]
nex-domains scan DOMAIN [DOMAIN2...]
nex-domains list [--registrar REGISTRAR] [--client CLIENT] [--status STATUS] [--expiring-within DAYS]
nex-domains show DOMAIN
nex-domains dns DOMAIN [--type RECORD_TYPE]
nex-domains ssl DOMAIN
nex-domains whois DOMAIN
nex-domains expiring [--days DAYS]
nex-domains sync
nex-domains search QUERY
nex-domains remove DOMAIN
nex-domains export {csv|json} [--output FILE]
nex-domains stats
nex-domains check DOMAIN
```

## Commands

### add
Add a domain to tracking database.

```bash
nex-domains add nex-ai.be --registrar cloudflare --client "Nex AI" --auto-renew --monthly-cost 0
```

### scan
Scan domain(s) for complete information (WHOIS, DNS, SSL, HTTP). Updates the database automatically.

```bash
nex-domains scan nex-ai.be example.com
```

### list
List domains with optional filters by registrar, client, status, or expiry.

```bash
nex-domains list --registrar cloudflare --client "Acme Corp" --expiring-within 30
```

### show
Show complete domain information including DNS records and check history.

```bash
nex-domains show nex-ai.be
```

### dns
Display DNS records for a domain, optionally filtered by type.

```bash
nex-domains dns nex-ai.be --type A
nex-domains dns nex-ai.be --type MX
```

### ssl
Show SSL certificate information (subject, issuer, expiry).

```bash
nex-domains ssl nex-ai.be
```

### whois
Look up WHOIS information (registrar, nameservers, expiry date).

```bash
nex-domains whois nex-ai.be
```

### expiring
Show domains and SSL certificates expiring within N days (default 90).

```bash
nex-domains expiring
nex-domains expiring --days 30
```

### sync
Import all Cloudflare zones and DNS records into the portfolio.

```bash
nex-domains sync
```

Requires `CF_API_TOKEN` environment variable.

### search
Search for domains by name, client, tags, or notes.

```bash
nex-domains search "acme"
```

### remove
Delete a domain from tracking.

```bash
nex-domains remove old-domain.com
```

### export
Export all domains to CSV or JSON format.

```bash
nex-domains export csv --output domains.csv
nex-domains export json --output domains.json
```

### stats
Show portfolio statistics (total domains, by registrar, by status, total cost, expiring).

```bash
nex-domains stats
```

### check
Perform quick HTTP/HTTPS health check on a domain.

```bash
nex-domains check example.com
```

## Environment Variables

### Optional: Cloudflare Integration

```bash
export CF_API_TOKEN="your-cloudflare-api-token"
export CF_EMAIL="your-cloudflare-email"
```

Enable Cloudflare sync and API operations.

### Optional: TransIP Integration

```bash
export TRANSIP_LOGIN="your-transip-login"
export TRANSIP_PRIVATE_KEY_PATH="/path/to/private/key"
```

For TransIP-specific operations (future releases).

## Data Storage

All data is stored locally at `~/.nex-domains/`:

- `domains.db` - SQLite database with all domain data
- `nex-domains.log` - Application logs

No data is sent externally unless you explicitly sync with Cloudflare.

## Database Schema

### domains
- domain (unique, indexed)
- registrar (cloudflare, transip, other)
- registration_date
- expiry_date (indexed)
- auto_renew (boolean)
- nameservers (JSON)
- ssl_expiry
- ssl_issuer
- dns_provider
- hosting_provider
- client (indexed)
- monthly_cost
- status (active, expired, parked, transferring)
- tags
- notes
- last_checked
- created_at, updated_at

### dns_records
- domain_id (foreign key)
- record_type (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA)
- name
- content
- ttl
- proxied (Cloudflare-specific)
- priority (MX records)

### domain_checks
- domain_id (foreign key)
- check_type (whois, dns, ssl, http)
- status
- details (JSON)
- checked_at

## Examples

### Check which domains expire in 90 days
```bash
nex-domains expiring
```

### Find all domains for a specific client
```bash
nex-domains list --client "Ribbens Airco"
```

### Check SSL certificate status
```bash
nex-domains ssl demos.nex-ai.be
```

### View all MX records
```bash
nex-domains dns nex-ai.be --type MX
```

### Sync all Cloudflare domains
```bash
export CF_API_TOKEN="your-token"
nex-domains sync
```

### Get portfolio overview
```bash
nex-domains stats
```

### Export domains for backup
```bash
nex-domains export csv --output backup.csv
```

## Troubleshooting

### "whois command not found"
Install with: `apt install whois` (Linux) or `brew install whois` (macOS)

### "dig command not found"
Install with: `apt install dnsutils` (Linux) or `brew install bind` (macOS)

### "openssl command not found"
Install with: `apt install openssl` (Linux) or already included on macOS

### "SSL check timeout"
The domain's firewall may be blocking port 443, or there's a network connectivity issue.

### "WHOIS lookup fails"
The WHOIS server may be down, or the domain may not exist. Try again later.

### "CF_API_TOKEN not set"
Set the environment variable to use Cloudflare sync:
```bash
export CF_API_TOKEN="your-cloudflare-api-token"
```

### Database not initialized
Run setup again:
```bash
bash setup.sh
```

## License

MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Built by [Nex AI](https://nex-ai.be) - Digital transformation for Belgian SMEs.
