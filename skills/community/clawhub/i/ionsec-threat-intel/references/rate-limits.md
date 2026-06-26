# Rate Limits Reference

This skill implements service-specific throttling, retries, and response caching.

## Implemented Service Limits

| Service | Auth | Requests / Minute | Cache TTL |
|---------|------|-------------------|-----------|
| VirusTotal | Required | 4 | 60 minutes |
| GreyNoise | Required | 1 | 30 minutes |
| Shodan | Required | 60 | 60 minutes |
| AlienVault OTX | Required | 60 | 60 minutes |
| AbuseIPDB | Required | 5 | 30 minutes |
| URLscan | Optional | 60 | 60 minutes |
| Spur.us | Required | 60 | 60 minutes |
| Validin | Required | 60 | 60 minutes |
| MalwareBazaar | No | 60 | 60 minutes |
| URLhaus | No | 60 | 60 minutes |
| Pulsedive | No | 30 | 30 minutes |
| DNS0 / Google DNS / Cloudflare DNS | No | 60 | 60 minutes |

## Behavior

- Requests are delayed automatically to respect each service limit.
- HTTP `429` responses trigger retry handling.
- `Retry-After` headers are honored when present.
- Successful responses are cached to reduce duplicate API calls.
- Temporary server errors may be retried with exponential backoff.

## Practical Guidance

- For quick triage without keys, start with `pulsedive`, `urlhaus`, `malwarebazaar`, or DNS services.
- For premium enrichment, add `virustotal`, `greynoise`, `shodan`, `otx`, `abuseipdb`, `spur`, or `validin`.
- Use `openclaw threat-intel --rate-limits` to display the current built-in limits.
