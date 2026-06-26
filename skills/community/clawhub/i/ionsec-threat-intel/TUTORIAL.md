# IONSEC Threat Intel Tutorial

> Complete walkthrough for using the IONSEC Threat Intel skill with OpenClaw

## 📋 Table of Contents

1. [Installation](#installation)
2. [First Run Setup](#first-run-setup)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Real-World Scenarios](#real-world-scenarios)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Step 1: Install the Skill

Download the skill from Clawhub and install:

```bash
# Download from Clawhub (or copy from source)
cp threat-intel.skill ~/.openclaw/skills/

# Verify installation
openclaw skills list | grep threat-intel
```

### Step 2: Check Installation

```bash
# View skill help
openclaw threat-intel --help
```

---

## First Run Setup

### Configure API Keys

While many services work without keys, you'll get better results with API keys.

#### Option A: Interactive Setup (Recommended)

```bash
openclaw threat-intel setup
```

This will prompt you for each service:
```
🔧 IONSEC Threat Intel Setup

Some services require API keys for full functionality.
Leave blank to skip a service.

Enter VirusTotal API Key: [your-key-here]
Enter GreyNoise API Key: [your-key-here]
...
```

#### Option B: Environment Variables

Add to your shell profile (`~/.bashrc` or `~/.zshrc`):

```bash
# VirusTotal - 500 requests/day free
export VT_API_KEY="your_virustotal_key"

# AlienVault OTX - Unlimited free
export OTX_API_KEY="your_otx_key"

# GreyNoise - 50 requests/day free
export GREYNOISE_API_KEY="your_greynoise_key"

# Shodan - 100 requests/month free
export SHODAN_API_KEY="your_shodan_key"

# AbuseIPDB - 1000 requests/day free
export ABUSEIPDB_API_KEY="your_abuseipdb_key"

# Spur.us - Paid only
export SPUR_API_KEY="your_spur_key"

# Validin - Free tier available
export VALIDIN_API_KEY="your_validin_key"
```

Then reload:
```bash
source ~/.bashrc
```

---

## Basic Usage

### Check an IP Address

```bash
# Using free services only
openclaw threat-intel ip 192.0.2.1 --services pulsedive

# Using multiple services (requires keys)
openclaw threat-intel ip 192.0.2.1 --services virustotal,greynoise,shodan

# Check with all available services
openclaw threat-intel ip 192.0.2.1 --services all
```

**Example Output:**
```
Service        | Status       | Result          | Details
--------------------------------------------------------------------------------
VirusTotal     | success      | ✅ Benign       | 0/71 vendors flagged
GreyNoise      | success      | ✅ Benign       | Not in GreyNoise dataset
Shodan         | success      | ℹ️ Info         | Ports: 22, 80, 443
AbuseIPDB      | success      | ✅ Benign       | 0 reports, confidence 0%
Pulsedive      | success      | ✅ Benign       | Risk: none
```

### Check a Domain

```bash
# DNS and reputation check
openclaw threat-intel domain evil.com --services all

# Focus on specific services
openclaw threat-intel domain evil.com --services virustotal,otx
```

### Check a Hash

```bash
# Malware hash lookup
openclaw threat-intel hash d41d8cd98f00b204e9800998ecf8427e --services all

# Use only free services
openclaw threat-intel hash d41d8cd98f00b204e9800998ecf8427e --services malwarebazaar
```

### Check a URL

```bash
# URL analysis
openclaw threat-intel url http://suspicious.com/malware.exe --services urlscan

# Multiple services
openclaw threat-intel url http://suspicious.com/malware.exe --services virustotal,urlhaus,urlscan
```

### Output Formats

```bash
# JSON output (for automation)
openclaw threat-intel ip 8.8.8.8 --services all --format json > results.json

# Markdown output (for reports)
openclaw threat-intel ip 8.8.8.8 --services all --format markdown > report.md

# Default table output
openclaw threat-intel ip 8.8.8.8 --services all
```

---

## Advanced Features

### Bulk Processing

Create an IOC file:

```bash
cat > iocs.txt << 'EOF'
# IPs
ip:192.0.2.1
ip:198.51.100.5

# Domains
domain:suspicious.com
domain:evil-site.ru

# Hashes
hash:d41d8cd98f00b204e9800998ecf8427e
hash:5d41402abc4b2a76b9719d911017c592

# URLs
url:http://phishing.com/login
url:https://malware.net/payload.exe
EOF
```

Process in bulk:

```bash
# JSON output
openclaw threat-intel bulk iocs.txt --output results.json

# Markdown report
openclaw threat-intel bulk iocs.txt --output report.md --format markdown
```

### Script Usage

Use directly from Python:

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, "/path/to/skill/scripts")

from threat_intel import load_config, query_all_services

config = load_config()

# Query single IP
results = query_all_services(
    observable="8.8.8.8",
    obs_type="ip",
    services=["pulsedive"],
    config=config
)

print(results)
```

---

## Real-World Scenarios

### Scenario 1: Phishing Investigation

**Situation:** User reports suspicious email with link.

```bash
# Extract URL from email and check
openclaw threat-intel url https://b4nk-secure-login.com/verify --services urlscan,virustotal,urlhaus

# Check the domain
openclaw threat-intel domain b4nk-secure-login.com --services virustotal,otx

# Check if IP is flagged
openclaw threat-intel ip 203.0.113.45 --services abuseipdb,pulsedive
```

### Scenario 2: Malware Analysis

**Situation:** Found suspicious executable, need to check reputation.

```bash
# Get file hash
sha256sum suspicious.exe

# Check hash across databases
openclaw threat-intel hash a3b2c1d4e5f6... --services virustotal,malwarebazaar,otx

# Check download URL if known
openclaw threat-intel url http://cdn.evil.com/payload.exe --services urlscan
```

### Scenario 3: Network Intrusion

**Situation:** IDS alert for suspicious IP connection.

```bash
# Comprehensive IP check
openclaw threat-intel ip 198.51.100.100 --services all --format json > ip_report.json

# Check for VPN/proxy (if you have Spur.us)
openclaw threat-intel ip 198.51.100.100 --services spur

# Check passive DNS (if you have Validin)
openclaw threat-intel ip 198.51.100.100 --services validin
```

### Scenario 4: Threat Hunt

**Situation:** Proactive hunting for known bad infrastructure.

```bash
# Create list of suspicious domains
cat > domains.txt << 'EOF'
domain:c2-server.com
domain:data-exfil.net
domain:malware-dl.xyz
EOF

# Bulk check
openclaw threat-intel bulk domains.txt --output hunt_results.json

# Filter results (requires jq)
cat hunt_results.json | jq '.[] | select(.classification == "malicious")'
```

---

## Troubleshooting

### Service Returns 404/Not Found

This usually means the observable isn't in the service's database.

```bash
# Try multiple services to get coverage
openclaw threat-intel ip 67.213.209.1 --services virustotal,otx,shodan
```

### Rate Limit Errors

The skill automatically handles rate limits:

```bash
# Check rate limit status for all services
openclaw threat-intel --rate-limits

# Example output:
# ======================================================================
# 🚦 Rate Limit Status
# =======================================================================
#
# Service             Rate (req/min)  Cache TTL    Status
# ----------------------------------------------------------------------
# virustotal          4               1h           🔴 Needs API key
# greynoise           1               30m          🔴 Needs API key
# pulsedive           30              30m          🟢 Ready
# malwarebazaar       10              24h          🟢 Ready
# =======================================================================
```

**Automatic Rate Limit Handling:**
- Request throttling - enforces minimum interval between API calls
- Retries on 429 errors with exponential backoff
- Response caching (30 min - 24 hours depending on service)
- Reads `Retry-After` headers when available

**If you still hit limits:**
```bash
# Use fewer services at once
openclaw threat-intel ip 8.8.8.8 --services pulsedive,malwarebazaar

# Use free services only (higher limits)
openclaw threat-intel domain evil.com --services pulsedive
```

### API Key Not Working

```bash
# Verify key is set
echo $VT_API_KEY

# Check config file
cat ~/.openclaw/workspace/skills/threat-intel/config.json

# Re-run setup
openclaw threat-intel setup
```

### Missing Services

```bash
# Check available services per observable type
openclaw threat-intel ip 8.8.8.8 --services invalid_service
# Error message will list available services
```

---

## 🏢 About IONSEC

This skill is developed by **IONSEC** - your incident response partner.

- 🌐 **Website:** https://IONSEC.io
- 💼 **Services:** Incident Response | Threat Intelligence | DFIR

---

**Need help?** Contact us at https://IONSEC.io
