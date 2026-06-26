# 🔍 IONSEC Threat Intel

> **Multi-Source Threat Intelligence Enrichment for Incident Response**
> 
> Powered by [IONSEC.io](https://IONSEC.io) | Built for OpenClaw

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://clawhub.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](references/LICENSE.md)
[![Services](https://img.shields.io/badge/Services-14+-orange)](SKILL.md)

## 🎯 What It Does

IONSEC Threat Intel aggregates intelligence from **14+ external threat intelligence services** to enrich observables (IPs, domains, URLs, hashes) during incident response investigations. Get comprehensive IOC context in seconds.

**Key Capabilities:**
- 🌐 **IP Reputation** - VPN/proxy detection, geolocation, ASN, malicious activity
- 🔗 **Domain Analysis** - WHOIS, DNS history, subdomains, phishing detection  
- 🔍 **URL Scanning** - Live analysis, screenshots, redirects
- 🦠 **Hash Lookups** - Malware detection across multiple databases
- 🚦 **Smart Rate Limiting** - Automatic throttling, caching, and retry logic

## ⚡ Quick Start

```bash
# Check an IP across multiple services
openclaw threat-intel ip 8.8.8.8 --services all

# Check a domain
openclaw threat-intel domain suspicious-site.com --services virustotal,greynoise

# Check a hash
openclaw threat-intel hash a3b2c1d4e5f6... --services malwarebazaar,virustotal

# Bulk check from file
openclaw threat-intel bulk iocs.txt --output report.json

# View rate limit status
openclaw threat-intel --rate-limits
```

## 📦 Installation

1. **Download** the `.skill` file from [Clawhub](https://clawhub.ai)
2. **Install** to OpenClaw:
   ```bash
   cp threat-intel.skill ~/.openclaw/skills/
   ```
3. **Optional:** configure API keys for premium services:
   ```bash
   openclaw threat-intel setup
   ```

The skill does not auto-run setup and does not prompt for API keys unless you explicitly run the setup command.

## 🔑 Supported Services

### Free Services (No API Key Required)
| Service | Observable | Description |
|---------|------------|-------------|
| **Pulsedive** | IP, Domain, URL | Community threat intelligence |
| **MalwareBazaar** | Hash | Malware sample database |
| **URLhaus** | URL | Malicious URL database |
| **DNS0** | Domain | DNS with threat detection |

### Premium Services (API Key Required)
| Service | Observable | Best For | Rate Limit |
|---------|------------|----------|------------|
| **VirusTotal** | All | Comprehensive detection | 4/min (free) |
| **GreyNoise** | IP | Botnet/internet noise | 1/min (free) |
| **Shodan** | IP | Exposed services | 1/min (free) |
| **Spur.us** | IP | VPN/proxy detection | 60/min |
| **Validin** | IP, Domain | Passive DNS history | 30/min |
| **AbuseIPDB** | IP | Abuse reports | 5/min (free) |
| **AlienVault OTX** | All | Community IOCs | 60/min |
| **URLscan** | URL | Live URL scanning | 1/min (free) |

## 🚦 Rate Limiting

The skill automatically handles rate limits:

- **Request Throttling** - Enforces minimum interval between API calls
- **Automatic Retries** - Retries on 429 (rate limit) and 5xx errors
- **Response Caching** - Caches results to reduce duplicate API calls
- **Exponential Backoff** - Smart retry delays on failures

```bash
# View current rate limit status
openclaw threat-intel --rate-limits
```

## 🛠️ Configuration

### Environment Variables
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

### Interactive Setup
```bash
openclaw threat-intel setup
```

## 📖 Documentation

- [API Key Setup Guide](references/api-keys.md)
- [Service Documentation](references/services.md)
- [Rate Limits](references/rate-limits.md)
- [Tutorial](TUTORIAL.md)

## 🏢 About IONSEC

**IONSEC** provides incident response and threat intelligence solutions for security teams.

🌐 **Website:** [IONSEC.io](https://IONSEC.io)
💼 **Services:** Incident Response | Threat Hunting | IOC Enrichment

## 🤝 Contributing

This skill is maintained by the IONSEC team. For issues or feature requests:
- Open an issue on [GitHub](https://github.com/ionsec/openclaw-threat-intel)
- Contact us at [IONSEC.io](https://IONSEC.io)

## 📄 License

MIT License - See [references/LICENSE.md](references/LICENSE.md) for details.

---

<p align="center">
  <b>Built with 💜 by IONSEC for the security community</b><br>
  <a href="https://IONSEC.io">IONSEC.io</a> | <a href="https://clawhub.ai">Clawhub</a>
</p>