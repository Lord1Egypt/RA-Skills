---
name: nex-domains
description: Comprehensive domain portfolio manager for managing multiple domains across different registrars (Cloudflare, TransIP, and others). Monitor domain expiration dates and SSL certificate validity to prevent unexpected outages. Sync domains and DNS records directly from Cloudflare using API integration, or manually add domains for tracking. Query WHOIS information to view registrar, expiration dates, and nameserver details. Check DNS record status (A, AAAA, CNAME, MX, TXT, NS records) and validate DNS configurations. Monitor SSL certificate expiry dates with advance warnings (critical at 7 days). Perform comprehensive domain health checks including DNS resolution verification, HTTP/HTTPS status validation, and nameserver configuration checks. Track domain costs, auto-renewal settings, and client assignments for agency portfolio management. Export domain lists and statistics in CSV or JSON format for reporting and analysis. Perfect for web agencies, DevOps teams, and domain managers who need to monitor multiple domain portfolios and ensure continuous service availability. All domain data remains local.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "🌐"
    requires:
      bins:
        - python3
        - whois
        - dig
        - openssl
      env:
        - CF_API_TOKEN
        - CF_EMAIL
        - TRANSIP_LOGIN
        - TRANSIP_PRIVATE_KEY_PATH
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-domains.py"
      - "lib/*"
      - "setup.sh"
---

# Nex Domains

DNS & Domain Portfolio Manager. Track all your domains across multiple registrars (Cloudflare, TransIP, etc.), monitor SSL certificate expiry dates, manage DNS records, and stay on top of renewals. Built for domain managers, DevOps, and web agencies.

## When to Use

Use this skill when the user asks about:

- Which domains expire in the next 90 days
- What DNS records does [domain] have
- Is the SSL cert for [domain] valid or expiring
- Sync all my Cloudflare domains into the portfolio
- Show me all domains for client [name]
- What's the status of [domain]
- List all domains from [registrar]
- Domain expiry tracking and renewal reminders
- SSL certificate monitoring and alerts
- WHOIS information lookups
- DNS record management
- Domain health checks and validation
- Portfolio statistics (total domains, cost, registrars)
- Domain search and filtering
- Export domain list to CSV/JSON
- Check if a domain resolves
- View nameservers for a domain
- Domain transfer tracking
- Multi-registrar portfolio overview

Trigger phrases: "domain", "DNS", "SSL", "certificate", "whois", "expiring", "nameserver", "Cloudflare", "TransIP", "domeinnaam", "renewal", "domain expires", "check my domains", "domain portfolio", "domain manager"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs necessary command-line tools (whois, dig, openssl), initializes the database, and makes the CLI available.

### Environment Variables (Optional)

For Cloudflare sync and API access, set these environment variables:

```bash
export CF_API_TOKEN="your-cloudflare-api-token"
export CF_EMAIL="your-cloudflare-email"
```

For TransIP integration:

```bash
export TRANSIP_LOGIN="your-transip-login"
export TRANSIP_PRIVATE_KEY_PATH="/path/to/private/key"
```

## Available Commands

The CLI tool is `nex-domains`. All commands output plain text.

### Add a Domain

Add a domain to your portfolio:

```bash
nex-domains add example.com --registrar cloudflare --client "Acme Corp" --auto-renew
nex-domains add example.be --registrar transip --monthly-cost 8.50
nex-domains add example.org --registrar other --notes "Parked domain"
```

Options:
- `--registrar`: cloudflare, transip, or other (required)
- `--client`: Client or organization name
- `--auto-renew`: Enable automatic renewal flag
- `--monthly-cost`: Annual or monthly cost
- `--notes`: Additional notes

### Scan a Domain

Scan domain(s) for complete information (WHOIS, DNS, SSL, HTTP):

```bash
nex-domains scan example.com
nex-domains scan example.be example.org
```

This runs WHOIS lookup, DNS query, SSL certificate check, and HTTP health check. Results are saved to the database automatically.

### List Domains

List all domains or filter by various criteria:

```bash
nex-domains list
nex-domains list --registrar cloudflare
nex-domains list --client "Acme Corp"
nex-domains list --status active
nex-domains list --expiring-within 30
```

Filters:
- `--registrar`: Filter by registrar (cloudflare, transip, other)
- `--client`: Filter by client name
- `--status`: Filter by status (active, expired, parked, transferring)
- `--expiring-within`: Show domains expiring within N days

### Show Domain Details

View complete information for a domain:

```bash
nex-domains show example.com
```

Shows domain details, DNS records, and recent check history.

### View DNS Records

Show DNS records for a domain:

```bash
nex-domains dns example.com
nex-domains dns example.com --type A
nex-domains dns example.com --type MX
```

Options:
- `--type`: Filter by record type (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA)

### Check SSL Certificate

View SSL certificate information:

```bash
nex-domains ssl example.com
```

Shows certificate subject, issuer, expiry date, and validity period.

### Look Up WHOIS

Get WHOIS information:

```bash
nex-domains whois example.com
```

Shows registrar, expiry date, and nameservers from WHOIS.

### Expiring Domains & SSL Certs

Find what needs renewal:

```bash
nex-domains expiring
nex-domains expiring --days 30
nex-domains expiring --days 180
```

Shows domains and SSL certificates expiring within the specified days (default: 90).

### Sync from Cloudflare

Import all domains and DNS records from Cloudflare:

```bash
nex-domains sync
```

Requires `CF_API_TOKEN` environment variable. This imports all zones as domains and fetches all DNS records automatically.

### Search Domains

Search for domains by name, client, tags, or notes:

```bash
nex-domains search "acme"
nex-domains search "cloudflare"
nex-domains search "production"
```

### Remove a Domain

Delete a domain from tracking:

```bash
nex-domains remove example.com
```

### Export Portfolio

Export all domains to CSV or JSON:

```bash
nex-domains export csv
nex-domains export csv --output domains.csv
nex-domains export json --output domains.json
```

### Statistics

View portfolio statistics:

```bash
nex-domains stats
```

Shows total domains, breakdown by registrar and status, total monthly cost, and renewal alerts.

### Quick Health Check

Perform a quick HTTP/HTTPS check on a domain:

```bash
nex-domains check example.com
```

Shows DNS resolution, IP address, and HTTP/HTTPS status codes.

## Example Interactions

**User:** "Which of my domains expire in the next 90 days?"
**Agent runs:** `nex-domains expiring`
**Agent:** Lists expiring domains with dates.

**User:** "What DNS records does nex-ai.be have?"
**Agent runs:** `nex-domains dns nex-ai.be`
**Agent:** Displays all DNS records for the domain.

**User:** "Is the SSL cert for demos.nex-ai.be valid?"
**Agent runs:** `nex-domains ssl demos.nex-ai.be`
**Agent:** Shows certificate status and expiry date.

**User:** "Sync all my Cloudflare domains"
**Agent runs:** `nex-domains sync`
**Agent:** Imports all Cloudflare zones and DNS records into the portfolio.

**User:** "Show me all domains for client Ribbens Airco"
**Agent runs:** `nex-domains list --client "Ribbens Airco"`
**Agent:** Lists all domains managed for that client.

**User:** "What's the status of all my TransIP domains?"
**Agent runs:** `nex-domains list --registrar transip`
**Agent:** Shows all TransIP-managed domains.

**User:** "Add example.com and set up tracking"
**Agent runs:** `nex-domains add example.com --registrar cloudflare --client "Nex AI" --auto-renew`
**Agent:** Confirms domain added.

**User:** "Give me a CSV export of all my domains"
**Agent runs:** `nex-domains export csv --output domains.csv`
**Agent:** Creates and confirms export file.

**User:** "Show me domain portfolio statistics"
**Agent runs:** `nex-domains stats`
**Agent:** Displays total domains, breakdown by registrar, status distribution, total cost, renewal warnings.

**User:** "Is example.org resolving?"
**Agent runs:** `nex-domains check example.org`
**Agent:** Shows DNS resolution status and HTTP response codes.

**User:** "Search for all Acme Corp domains"
**Agent runs:** `nex-domains search "Acme Corp"`
**Agent:** Lists matching domains.

**User:** "What are all the A records for example.com?"
**Agent runs:** `nex-domains dns example.com --type A`
**Agent:** Shows all A records.

## Output Parsing

All CLI output is plain text, structured for easy parsing:

- Commands without `--output` show results in terminal
- Export commands create CSV/JSON files
- All output includes footer: `[Nex Domains by Nex AI | nex-ai.be]`

When presenting output to the user, strip the footer line and present the information naturally. Do not show raw database paths or internal details.

## Important Notes

- All domain data is stored locally at `~/.nex-domains/`. No data is sent externally unless you explicitly sync with Cloudflare.
- The `check_whois`, `check_dns`, `check_ssl`, and `check_http` functions use standard CLI tools (whois, dig, openssl) which require network access.
- Cloudflare sync requires valid `CF_API_TOKEN` environment variable.
- SSL certificate checks connect directly to ports (default 443) and may be blocked by firewalls.
- WHOIS lookups depend on WHOIS server availability and may timeout.
- DNS queries use public DNS servers (8.8.8.8, 8.8.4.4, 1.1.1.1) by default.

## Troubleshooting

- **"WHOIS command not found"**: Install whois package (`apt install whois` on Linux, `brew install whois` on macOS)
- **"dig command not found"**: Install bind-utils/dnsutils (`apt install dnsutils` on Linux, `brew install bind` on macOS)
- **"openssl command not found"**: Install openssl (`apt install openssl` on Linux, included by default on macOS)
- **"CF_API_TOKEN not set"**: Set the environment variable for Cloudflare sync features
- **"Database not found"**: Run `bash setup.sh` to initialize
- **"SSL check timeout"**: Domain may have firewall blocking port 443, or connection issues
- **"WHOIS lookup fails"**: WHOIS server may be down or domain may not exist
- **"DNS query returns no records"**: Domain may not have the requested record type, or nameserver is unreachable

## Data Structure

- **domains table**: Stores domain metadata (registrar, expiry, status, client, costs, notes)
- **dns_records table**: Stores DNS records for each domain (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA)
- **domain_checks table**: Stores history of domain health checks (WHOIS, DNS, SSL, HTTP)

All data is indexed for fast searches and filtering.

## Security Notes

- Private keys for TransIP API must be stored securely (environment variable or secure file)
- API tokens should never be committed to version control
- All WHOIS, DNS, and SSL checks are read-only (no modifications)
- Database file should be protected with file permissions (`~/.nex-domains/domains.db`)

## Credits

Built by Nex AI (https://nex-ai.be) - Digital transformation for Belgian SMEs.
Author: Kevin Blancaflor
