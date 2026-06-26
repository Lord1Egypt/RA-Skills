# MerkleMap OSINT Skill for OpenClaw

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skill Version](https://img.shields.io/badge/version-3.0.0-brightgreen.svg)](#)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-compatible-purple.svg)](https://openclaw.ai)
[![OpenCode Compatible](https://img.shields.io/badge/OpenCode-compatible-orange.svg)](#)
[![Anthropic Agent 1.0](https://img.shields.io/badge/Anthropic_Agent-1.0-black.svg)](#)

**Turn any OpenClaw agent into a professional OSINT analyst.** Subdomain discovery, certificate auditing, typosquatting detection, real-time CT monitoring, risk scoring, and beautiful HTML reports — all through natural language.

---

## What Can It Do?

| Capability | Description |
|-----------|-------------|
| **Subdomain Enumeration** | Discover all known subdomains via Certificate Transparency logs |
| **Typosquatting Detection** | Find lookalike/phishing domains using Levenshtein fuzzy matching |
| **Certificate Audit** | List all certs for a host, flag expired, weak, or expiring ones |
| **Certificate Deep Dive** | Full X.509 details, issuer chain, CT log presence for any cert |
| **Live CT Monitoring** | Real-time SSE stream of newly discovered hostnames |
| **Risk Scoring** | Automatic 0–100 risk score based on scan findings |
| **Subdomain Categorization** | Auto-classify hosts (mail, api, admin, dev, cdn, auth...) |
| **CA Trust Analysis** | Detect unusual CAs, self-signed certs, CA sprawl |
| **Temporal Anomaly Detection** | Spot suspicious bursts of new subdomains |
| **Wildcard Cert Mapping** | Map which subdomains are covered by wildcard certs |
| **Change Detection** | Diff current scan vs previous report — catch what changed |
| **Multi-Domain Scanning** | Batch scan multiple domains with comparison table |
| **Executive Summaries** | Non-technical summaries for management and stakeholders |
| **HTML Report Export** | Professional dark-themed dashboard, print-ready |
| **JSON Export** | Machine-readable output for SIEMs and automation pipelines |

---

## Quick Start

### 1. Install

```bash
git clone https://github.com/laikhtman/merklemap-openclaw-skill.git ~/.openclaw/skills/merklemap-osint
```

### 2. Configure

Get your API key at [merklemap.com/user-profile/api](https://www.merklemap.com/user-profile/api), then:

```bash
export MERKLEMAP_API_KEY='your_api_token_here'
```

### 3. Use

Restart OpenClaw and start talking:

```
> Do a full recon on tesla.com and generate a report
```

That's it. The skill handles everything — subdomain discovery, certificate checks, risk analysis, categorization, and outputs a professional HTML report.

---

## Usage Examples

### Surface Mapping
```
Find all subdomains of example.org
Do a full recon on tesla.com
Scan tesla.com, spacex.com, and boring.co
```

### Certificate Auditing
```
What certificates are active for mail.proton.me?
Are there any expired certs on api.example.com?
Show me the full details of cert with SHA-256 ab12cd34...
```

### Typosquatting & Phishing Detection
```
Check for typosquatting domains targeting mybrand.com
Find lookalike domains for openai.com
```

### Real-Time Monitoring
```
Monitor new certificates being issued for example.com
Show me the live CT log stream
```

### Reports & Exports
```
Full recon on example.com — generate report
Audit certs for mail.example.com and export as HTML and JSON
Generate a report for the typosquatting scan on mybrand.com
```

### Change Detection
```
What changed on example.com since the last scan?
Compare current state of tesla.com with previous report
```

---

## Smart Workflows

The skill doesn't just call APIs — it **thinks**. When you say "full recon", it automatically:

1. Enumerates all subdomains (with auto-pagination)
2. Categorizes every hostname (mail, api, admin, dev...)
3. Pulls certificates for key infrastructure
4. Analyzes CA diversity and trust
5. Maps wildcard certificate coverage
6. Detects temporal anomalies in discovery dates
7. Calculates a risk score (0–100)
8. Writes an executive summary
9. Flags all security issues by severity
10. Generates a beautiful HTML dashboard

---

## HTML Reports

Professional, self-contained HTML reports with zero external dependencies.

**What's included:**
- Risk score banner (color-coded 0–100)
- Executive summary for non-technical stakeholders
- Summary metric cards
- Key findings ranked by severity (HIGH / MEDIUM / INFO)
- Subdomain table with category badges
- Discovery timeline
- Certificate Authority analysis
- Wildcard certificate coverage map
- Full certificate table with status badges
- Change detection diff (when comparing scans)
- Typosquatting results with risk ratings

**Features:**
- Dark theme by default, light theme on request
- Print-ready (`@media print` styles) for PDF export
- Mobile responsive
- Sticky table headers

Reports are saved as `merklemap-report-{domain}-{date}.html`.

---

## Risk Scoring

Every scan produces a **0–100 risk score** based on real findings:

| Score | Rating | Meaning |
|-------|--------|---------|
| 0–20 | Low | Well-managed infrastructure |
| 21–40 | Moderate | Some attention needed |
| 41–60 | Elevated | Significant issues found |
| 61–80 | High | Immediate attention recommended |
| 81–100 | Critical | Serious security concerns |

Factors include: expired certs, weak keys, self-signed certs, exposed dev/staging hosts, unusual CAs, subdomain bursts, typosquatting domains, and more.

---

## Compatibility

| Platform | Status |
|----------|--------|
| OpenClaw | Fully supported |
| OpenCode | Fully supported |
| Anthropic Agent SDK 1.0 | Compatible |
| Claude Code | Compatible via skill loading |

---

## API Reference

This skill uses the [MerkleMap API](https://www.merklemap.com/documentation):

| Endpoint | Description |
|----------|-------------|
| `GET /v1/search` | Subdomain search (wildcard + Levenshtein) |
| `GET /v1/certificates/{hostname}` | List certificates for a hostname |
| `GET /v1/certificates/hash/{sha256}` | Get full certificate details |
| `GET /v1/live-tail` | Real-time CT log stream (SSE) |

A paid MerkleMap subscription is required. [Get your API key here.](https://www.merklemap.com/user-profile/api)

---

## Contributing

Contributions are welcome! Feel free to:
- Open an issue for bugs or feature requests
- Submit a PR with improvements
- Share your use cases

---

## License

MIT - see [LICENSE](LICENSE) for details.

---

**Built by [@laikhtman](https://github.com/laikhtman)** | Powered by [MerkleMap](https://www.merklemap.com)
