# Scout Default Config

Default `config.json` for `{agent_root}/commons/data/ocas-scout/config.json`:

```json
{
  "skill_id": "ocas-scout",
  "skill_version": "3.0.0",
  "config_version": "1",
  "created_at": "",
  "updated_at": "",
  "waterfall": {
    "enabled_tiers": [1, 2]
  },
  "paid_sources": {
    "enabled": false
  },
  "brief": {
    "format": "markdown"
  },
  "person_tools": {
    "theHarvester": true,
    "maigret": true,
    "holehe": true,
    "h8mail": true,
    "ghunt": true,
    "phoneinfoga": true,
    "emailrep": true,
    "opensanctions": true
  },
  "dark_web_tools": {
    "onionclaw": {
      "enabled": false,
      "path": "{agent_root}/tools/onionclaw",
      "requires_tor": true,
      "tor_socks_host": "127.0.0.1",
      "tor_socks_port": 9050
    }
  },
  "mcp_discovery": {
    "enabled": true,
    "registry_url": "https://nothumansearch.ai",
    "cache_ttl_hours": 24,
    "rate_limit_per_minute": 10
  },
  "retention": {
    "days": 90,
    "max_records": 10000
  }
}
```

## Field descriptions

| Field | Description |
|---|---|
| `waterfall.enabled_tiers` | Which source tiers are active. Default: `[1, 2]` |
| `paid_sources.enabled` | Whether Tier 3 (paid) sources are allowed. Requires explicit permission grant per request. |
| `brief.format` | Output format for briefs. Default: `markdown` |
| `person_tools.*` | Enable/disable individual person-specific OSINT tools |
| `dark_web_tools.onionclaw` | OnionClaw dark web search configuration. Requires Tor SOCKS proxy. |
| `mcp_discovery` | Dynamic MCP server discovery settings (registry URL, cache TTL, rate limit) |
| `retention` | Data retention policy (days, max records) |
