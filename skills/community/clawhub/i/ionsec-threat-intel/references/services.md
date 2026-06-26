# Service Documentation

## Implemented Services

### VirusTotal
- Types: IP, Domain, URL, Hash
- Purpose: Multi-engine reputation and malware context
- Env: `VT_API_KEY`

### GreyNoise
- Types: IP
- Purpose: Internet background noise and scanner classification
- Env: `GREYNOISE_API_KEY`

### Shodan
- Types: IP
- Purpose: Open ports, banners, and exposed services
- Env: `SHODAN_API_KEY`

### AlienVault OTX
- Types: IP, Domain, URL, Hash
- Purpose: Community threat intelligence and pulses
- Env: `OTX_API_KEY`

### AbuseIPDB
- Types: IP
- Purpose: Abuse reports and confidence scoring
- Env: `ABUSEIPDB_API_KEY`

### URLscan
- Types: URL
- Purpose: URL scanning and scan result retrieval
- Env: `URLSCAN_API_KEY`

### MalwareBazaar
- Types: Hash
- Purpose: Malware sample reputation
- Env: none

### URLhaus
- Types: URL
- Purpose: Malicious URL reputation
- Env: none

### Pulsedive
- Types: IP, Domain, URL
- Purpose: Community threat intelligence lookup
- Env: none

### DNS0 / Google DNS / Cloudflare DNS
- Types: Domain
- Purpose: DNS resolution and related enrichment
- Env: none

### Spur.us
- Types: IP
- Purpose: VPN, proxy, TOR, and hosting detection
- Env: `SPUR_API_KEY`

### Validin
- Types: IP, Domain, Hash
- Purpose: Passive DNS, subdomains, and WHOIS enrichment
- Env: `VALIDIN_API_KEY`

## Selection Tips

- Use `pulsedive` for free IP or domain triage.
- Use `malwarebazaar` for free hash reputation checks.
- Use `urlhaus` for free malicious URL lookups.
- Use `virustotal`, `greynoise`, `shodan`, and `otx` for deeper paid or registered-service enrichment.
- Use `spur` and `validin` when infrastructure profiling matters.
