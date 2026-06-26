---
name: osint-daily-brief
description: Generate a daily OSINT intelligence brief on any target — domain, company, IP, person, or keyword — using Tavily web search, WHOIS, DNS recon, and Shodan. Delivers a structured markdown report with threat indicators, exposed assets, and news mentions. Use for competitive intelligence, brand monitoring, pre-engagement recon, or daily threat awareness. Requires TAVILY_API_KEY. Shodan and WHOIS optional.
---

# OSINT Daily Brief

Automated open-source intelligence report for any target.

Pulls from Tavily AI search, DNS records, WHOIS, and optionally Shodan.
Structures findings into a daily brief you can read in under 2 minutes.

Use for: competitive intel, brand monitoring, pre-engagement recon, daily threat feeds.

---

## Prerequisites

```bash
# Required
TAVILY_API_KEY=your_key_here        # tavily.com → free: 1,000 searches/month

# Optional — for richer results
SHODAN_API_KEY=your_key_here        # shodan.io → free tier available
```

---

## Workflow

### 1. Web intelligence (Tavily)

```python
import os, requests

def tavily_search(query: str, max_results: int = 5) -> list[dict]:
    """AI-optimized web search — returns full page content, not just snippets."""
    r = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key":     os.environ["TAVILY_API_KEY"],
            "query":       query,
            "max_results": max_results,
            "search_depth": "advanced",
        },
        timeout=15,
    )
    return r.json().get("results", [])

# Example: monitor a target
target = "example.com"
news   = tavily_search(f"{target} security breach data leak 2026")
tech   = tavily_search(f"{target} technology stack infrastructure")
```

### 2. DNS recon

```python
import subprocess

def dns_recon(domain: str) -> dict:
    results = {}
    for record_type in ["A", "MX", "NS", "TXT"]:
        try:
            r = subprocess.run(
                ["dig", "+short", record_type, domain],
                capture_output=True, text=True, timeout=5
            )
            results[record_type] = r.stdout.strip().split("\n")
        except Exception:
            results[record_type] = []
    return results
```

### 3. WHOIS

```python
def whois_lookup(domain: str) -> str:
    try:
        r = subprocess.run(
            ["whois", domain],
            capture_output=True, text=True, timeout=10
        )
        # Extract key fields only
        lines = r.stdout.split("\n")
        relevant = [l for l in lines if any(k in l.lower() for k in
            ["registrar", "created", "expires", "registrant", "name server"])]
        return "\n".join(relevant[:15])
    except Exception as e:
        return f"WHOIS error: {e}"
```

### 4. Shodan (optional)

```python
def shodan_lookup(ip_or_domain: str) -> dict:
    key = os.environ.get("SHODAN_API_KEY")
    if not key:
        return {"error": "SHODAN_API_KEY not set"}
    try:
        r = requests.get(
            f"https://api.shodan.io/shodan/host/{ip_or_domain}",
            params={"key": key},
            timeout=10
        )
        data = r.json()
        return {
            "ports":   data.get("ports", []),
            "org":     data.get("org", ""),
            "country": data.get("country_name", ""),
            "vulns":   list(data.get("vulns", {}).keys())[:5],
        }
    except Exception as e:
        return {"error": str(e)}
```

### 5. Format the brief

```
OSINT DAILY BRIEF — [target] — YYYY-MM-DD
─────────────────────────────────────────
THREAT INDICATORS
  ⚠️  [finding] — [source]
  ✅  No breach mentions in last 30 days

DNS PROFILE
  A:   [IPs]
  MX:  [mail servers]
  NS:  [nameservers]
  TXT: [SPF/DKIM/verification records]

WHOIS
  Registrar: [name]
  Created:   [date]
  Expires:   [date]
  Name Servers: [list]

EXPOSED ASSETS (Shodan)
  Open ports: [list]
  Org:        [org name]
  CVEs:       [list or "none detected"]

NEWS & WEB MENTIONS (last 30 days)
  1. [title] — [source] — [url]
  2. ...

SUMMARY
  Risk level: [LOW/MEDIUM/HIGH]
  Key concern: [one sentence]
  Recommended: [1–2 actions]
─────────────────────────────────────────
Sources: Tavily, WHOIS, DNS, Shodan
```

---

## Scheduling — daily brand/target monitoring

```bash
# Monitor your own domain daily
openclaw cron add \
  --name "osint-brief:daily-self" \
  --cron "0 6 * * *" \
  --prompt "Run osint-daily-brief skill on target: yourdomain.com. Send report to Telegram."

# Monitor a competitor
openclaw cron add \
  --name "osint-brief:daily-competitor" \
  --cron "0 6 * * *" \
  --prompt "Run osint-daily-brief skill on target: competitor.com. Flag any new exposed ports, CVEs, or breach mentions."
```

---

## Use cases

| Use case | Target | Frequency |
|----------|--------|-----------|
| Brand monitoring | your domain | daily |
| Competitive intel | competitor domains | weekly |
| Pre-engagement recon | client domain | one-time |
| Threat actor tracking | IP ranges | daily |
| Dark web mentions | brand keywords | weekly |

---

## Privacy & ethics

- Only investigate targets you own or have explicit authorization to research
- All data comes from public sources (Tavily, DNS, WHOIS, Shodan)
- No social engineering, credential testing, or active probing
- WHOIS and Shodan data is public by design — this skill reads it, does not generate it
- Comply with applicable laws in your jurisdiction

---

## Notes

- Tavily free tier: 1,000 searches/month. Each run uses ~3–5 searches.
- Shodan free tier: limited to 1 result per query on some endpoints
- DNS recon requires `dig` installed: `sudo apt install dnsutils`
- WHOIS requires `whois` installed: `sudo apt install whois`
- For dark web mentions, pair with Tor proxy (Ahmia search via SOCKS5)
