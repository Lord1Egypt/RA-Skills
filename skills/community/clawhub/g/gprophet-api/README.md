---
name: gprophet-api
description: AI-powered stock prediction and market analysis for global markets
homepage: https://www.gprophet.com
metadata:
  clawdbot:
    emoji: "📈"
    requires:
      env: ["GPROPHET_API_KEY"]
    primaryEnv: "GPROPHET_API_KEY"
---

# G-Prophet API Skills

AI-powered stock prediction and market analysis for US, CN, HK, and Crypto markets.

## Authentication

All requests require `X-API-Key: gp_sk_...` header. Get your key at https://www.gprophet.com/settings/api-keys

Store in environment variable: `export GPROPHET_API_KEY="gp_sk_..."`

## Quick Example

```bash
curl -X POST "https://www.gprophet.com/api/external/v1/predictions/predict" \
  -H "X-API-Key: $GPROPHET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "market": "US", "days": 7}'
```

## Python SDK

```bash
pip install gprophet
```

```python
from gprophet import GProphet
client = GProphet(api_key="gp_sk_...")
result = client.predict("AAPL", market="US", days=7)
```

## MCP Server

```json
{
  "mcpServers": {
    "gprophet": {
      "command": "uvx",
      "args": ["--from", "gprophet", "gprophet-mcp"],
      "env": { "GPROPHET_API_KEY": "gp_sk_..." }
    }
  }
}
```

## Full Documentation

See [SKILL.md](./SKILL.md) for all endpoints, parameters, response formats, and MCP tool definitions.

## Support

- Dashboard: https://www.gprophet.com/dashboard
- Support: support@gprophet.com
