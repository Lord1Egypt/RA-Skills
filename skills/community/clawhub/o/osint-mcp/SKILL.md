---
name: osint-mcp
description: Run OSINT investigations from chat — email, username, domain, IP, phone, photo geolocation, plus news, social, and link-graph intelligence — using the osint-mcp tools.
homepage: https://github.com/snuri00/osint-mcp
---

# osint-mcp

This skill drives the **osint-mcp** tool suite for open-source intelligence
(OSINT). The tools are provided by the osint-mcp MCP server; register it once
(see Setup), then follow this playbook to decide which tool to call.

## Setup (one-time)

The tools come from the osint-mcp MCP server. Install and register it with
OpenClaw:

```bash
pip install "git+https://github.com/snuri00/osint-mcp"
openclaw mcp add osint-mcp --command osint-mcp-server
```

Most tools are keyless and work immediately. Optional API keys (Shodan,
VirusTotal, HaveIBeenPwned, Picarta, ...) unlock premium sources — set them in
the MCP server's `env`. See the project README and `examples/openclaw.json`.

## When to use which tool

Entity / person:
- Email — search_email, then search_breach or search_xposed (breaches),
  search_gravatar (profile)
- Username — search_username, search_paste, search_github
- Domain — search_whois, search_dns, search_domain, search_crt
- IP address — search_ip, search_ipgeo, search_abuseipdb, search_shodan
- Phone — search_phone
- Any target — generate_dorks for ready-made search queries

Event / news (journalist-style):
- A topic or "what's happening" — search_news (source-tier + propaganda flags)
  and search_events (global coverage volume and tone)
- A country or region — monitor_country for a one-call situational brief
- Natural disasters — search_disasters; humanitarian situation — search_reliefweb

Social / community:
- "What are people saying about X" — search_social (Reddit, Hacker News,
  Polymarket, GitHub; engagement-ranked)

Photo geolocation:
- A photo path or URL — geolocate_image (EXIF GPS is exact; GeoCLIP/Picarta are
  estimates with a confidence indicator)

Visualize:
- After linking several identifiers — build_graph for an entity link graph

## Rules

- Prefer keyless tools first; use keyed tools only when their key is configured.
- Corroborate findings across independent sources; clearly flag estimates
  (especially image geolocation) and low-confidence results.
- If the user restricts scope (e.g. "only on X" / "only the news"), call only
  the matching tool(s).
- Authorized, lawful, ethical use only: security research, CTF, journalism, and
  auditing your own footprint.
- Refuse misuse: decline requests whose evident purpose is to stalk, dox,
  harass, surveil, locate, or harm a specific private individual without consent
  (e.g. "find where this person lives", "track my ex"). Explain the boundary and
  offer a legitimate alternative. Treat geolocation/breach results as estimates,
  never as proof — a wrong result can harm an innocent person.
