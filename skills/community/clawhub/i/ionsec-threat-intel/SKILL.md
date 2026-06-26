---
name: threat-intel
description: Query multiple threat intelligence services for IOC enrichment including IP reputation, domain analysis, URL scanning, hash lookups, and malware detection. Use when investigating observables (IP, domain, URL, hash) to gather context from external sources like VirusTotal, GreyNoise, Shodan, AbuseIPDB, AlienVault OTX, and more. Supports both API-key services and free services.
---

# Threat Intel

## Overview

Query multiple external threat intelligence services to enrich observables (IPs, domains, URLs, hashes). Aggregates data from security vendors, open-source feeds, and specialized platforms to provide comprehensive IOC context.

**Supported Observable Types:**
- **IP addresses** - Reputation, geolocation, ASN, open ports, malicious activity
- **Domains** - WHOIS, DNS records, reputation, phishing detection
- **URLs** - Scan reports, redirects, phishing detection, screenshot analysis
- **Hashes (MD5/SHA1/SHA256)** - Malware detection, file analysis, known samples

## Quick Start

### Basic Usage

```bash
# Check an IP across multiple services
openclaw threat-intel ip 8.8.8.8 --services greynoise,abuseipdb,virustotal

# Check a domain
openclaw threat-intel domain evil.com --services all

# Check a hash
openclaw threat-intel hash a3b2c1d4e5f6... --services virustotal,otx

# Check a URL
openclaw threat-intel url http://suspicious.site/payload.exe --services urlscan

# View rate limit status
openclaw threat-intel --rate-limits
```

### API Key Management

Most services require API keys. Configure them interactively:

```bash
openclaw threat-intel setup
```

Or set environment variables:
```bash
export VT_API_KEY="your_virustotal_key"
export GREYNOISE_API_KEY="your_greynoise_key"
export SHODAN_API_KEY="your_shodan_key"
export OTX_API_KEY="your_otx_key"
export ABUSEIPDB_API_KEY="your_abuseipdb_key"
export URLSCAN_API_KEY="your_urlscan_key"
export SPUR_API_KEY="your_spur_key"
export VALIDIN_API_KEY="your_validin_key"
```

See [references/api-keys.md](references/api-keys.md) for full list of required keys per service.

## Available Services

### Free Services (No API Key Required)

| Service | Observable Types | Description |
|---------|-----------------|-------------|
| **MalwareBazaar** | Hash | Malware sample database |
| **URLhaus** | URL | Malicious URL database |
| **DNS0** | Domain | DNS resolver with threat detection |
| **Google DNS** | Domain | Public DNS resolver |
| **Cloudflare DNS** | Domain | Public DNS resolver |
| **Pulsedive** | IP, Domain, URL | Threat intelligence with rate limits |

### Services Requiring API Keys

| Service | Observable Types | Best For |
|---------|-----------------|----------|
| **VirusTotal v3** | IP, Domain, URL, Hash | Comprehensive malware detection |
| **GreyNoise** | IP | Internet background noise and scanner classification |
| **Shodan** | IP | Open ports, services, and exposed systems |
| **AlienVault OTX** | IP, Domain, URL, Hash | Threat community data |
| **AbuseIPDB** | IP | IP reputation and reported abuse |
| **URLscan** | URL | Live URL scanning and screenshot |
| **Spur.us** | IP | VPN, proxy, and hosting detection |
| **Validin** | IP, Domain, Hash | Passive DNS, subdomains, and WHOIS |

See [references/services.md](references/services.md) for complete service documentation.

## Workflows

### IOC Investigation

When investigating a suspicious observable, use this pattern:

1. **Quick triage** - Check free services first
   ```bash
   openclaw threat-intel ip <target> --services pulsedive
   ```

2. **Deep enrichment** - Add premium services for known-bad indicators
   ```bash
   openclaw threat-intel ip <target> --services virustotal,greynoise,shodan
   ```

3. **Correlate** - Cross-reference with multiple sources
   ```bash
   openclaw threat-intel ip <target> --services all
   ```

### Bulk Enrichment

Process multiple observables from a file:

```bash
openclaw threat-intel bulk iocs.txt --output results.json
```

Format: one observable per line, optionally prefixed with type:
```
ip:8.8.8.8
domain:evil.com
hash:a3b2c1...
```

## Scripts

Use these scripts directly for programmatic access:

- `scripts/threat_intel.py` - Main CLI tool
- `scripts/check_ip.py` - IP-focused helper script
- `scripts/bulk_check.py` - Bulk processing
- `scripts/setup.py` - Explicit interactive API key configuration

## Output Formats

### Default (Table)
```
Service        | Result | Score | Details
---------------|--------|-------|--------
VirusTotal     | ⚠️ Suspicious | 12/71 | 12 vendors flagged
GreyNoise      | ✅ Benign  | 0%    | Classified as benign
AbuseIPDB      | ⚠️ Suspicious | 85%   | 12 reports
```

### JSON (for automation)
```bash
openclaw threat-intel ip 8.8.8.8 --format json
```

### Markdown (for reports)
```bash
openclaw threat-intel ip 8.8.8.8 --format markdown
```

## References

- [API Keys Setup Guide](references/api-keys.md)
- [Service Documentation](references/services.md)
- [Rate Limits](references/rate-limits.md)