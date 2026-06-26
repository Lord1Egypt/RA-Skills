---
name: httpstat
description: Pretty HTTP response statistics with timing waterfall. Use when asked to check a URL's response time, debug slow requests, measure TTFB, or get HTTP timing breakdown. Like curl -v but readable. Zero dependencies.
---

# httpstat ⚡

Pretty HTTP timing statistics. Shows DNS, TCP, TLS, TTFB, and transfer times.

## Usage

```bash
# Basic timing
python3 scripts/httpstat.py https://example.com

# With headers
python3 scripts/httpstat.py https://api.github.com -H "Accept: application/json"

# POST request
python3 scripts/httpstat.py https://httpbin.org/post -X POST -d '{"key":"value"}'
```

## Output
Shows a visual waterfall of: DNS Lookup → TCP Connection → TLS Handshake → Server Processing → Content Transfer
