# OlaXBT Nexus Data API Skill

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)
![OpenClaw](https://img.shields.io/badge/OpenClaw-2026.3.0%2B-orange)

Official OlaXBT Nexus Data API integration for OpenClaw agents. This skill uses a **JWT only** (no private key in the skill). Obtain the JWT via the [Nexus auth flow](https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md); then set `NEXUS_JWT` and use the client.

## Features

- **🔐 JWT-only**: No private key in the skill; use a pre-obtained JWT from the Nexus auth flow
- **📊 14 API Endpoints**: Full coverage of OlaXBT Nexus data services
- **⚡ Real-time Data**: Live market insights and analysis
- **🛡️ Minimal permissions**: Only reads `NEXUS_JWT` and optional `NEXUS_*` URLs
- **📈 Advanced Analytics**: Technical indicators and smart money tracking

## Installation

### For OpenClaw Users
```bash
# Install from ClawHub
openclaw skill install olaxbt-nexus-data
```

### For Python Developers
```bash
pip install olaxbt-nexus-data
```

### Required environment variable
```bash
# Obtain JWT via the Nexus auth flow (see skills/nexus/SKILL.md), then:
export NEXUS_JWT="<your-jwt-token>"
```

## API vs this Python package

The OlaXBT Nexus API is **HTTP**. You can use it with **any client** (curl, fetch, Postman, etc.) by following the [Nexus Skills API spec](https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md): `POST /auth/message` → sign the message with your wallet → `POST /auth/wallet` → get JWT → call `https://api-data.olaxbt.xyz/api/v1/...` with `Authorization: Bearer <JWT>`. No Python or OpenClaw required.

**This repo** is a **Python wrapper** for that same API. Use it if you want a `pip install` / `openclaw skill install` client instead of hand-rolling HTTP and signing. OpenClaw is an agent framework; it can use either the HTTP spec (curl-style) or this Python skill. Both talk to the same backend.

## Quick Start

```python
from olaxbt_nexus_data import NexusClient

# Set NEXUS_JWT in env (obtain via Nexus auth flow), then:
client = NexusClient()
client.authenticate()

# Get latest crypto news
news = client.news.get_latest(limit=10)
for item in news:
    print(f"📰 {item['title']}")

# Get market overview
market = client.market.get_overview()
print(f"📈 Total Market Cap: ${market['total_market_cap']:,.0f}")

# Get KOL heatmap for Bitcoin
kol_data = client.kol.get_heatmap(symbol="BTC")
print(f"👥 KOL Activity: {kol_data['total_mentions']} mentions")
```

## API Endpoints

| Endpoint | Description | Credits Required |
|----------|-------------|------------------|
| **AIO Assistant** | Market analysis & trading signals | Yes |
| **Ask Nexus** | AI crypto chat & analysis | Yes |
| **News API** | Crypto news aggregation | No |
| **KOL API** | Key Opinion Leader tracking | No |
| **Technical Indicators** | Trading signals & analysis | No |
| **Smart Money** | Institutional money tracking | No |
| **Liquidations** | Liquidation data & OI history | No |
| **Market Divergence** | Market divergence detection | No |
| **Sentiment** | Market sentiment analysis | No |
| **ETF** | ETF inflow/outflow tracking | No |
| **Market Overview** | Comprehensive market overview | No |
| **Open Interest** | OI rate-of-change & rankings | No |
| **Coin Data** | Per-coin data & metrics | No |
| **Credits Management** | Balance & purchase verification | N/A |

## Authentication

### Base URLs
- **Auth Domain**: `https://api.olaxbt.xyz/api`
- **Data Domain**: `https://api-data.olaxbt.xyz/api/v1`

### Obtaining a JWT
The skill does **not** handle private keys. Get a JWT using the [Nexus Skills API auth flow](https://github.com/olaxbt/olaxbt-skills-hub/blob/main/skills/nexus/SKILL.md):
1. `POST https://api.olaxbt.xyz/api/auth/message` with `{"address": "0x..."}`
2. Sign the returned message with your wallet (e.g. OpenClaw or one-time sign-in)
3. `POST https://api.olaxbt.xyz/api/auth/wallet` with address, signature, message, nonce → receive `token` (JWT)
4. Set `export NEXUS_JWT="<token>"` and use the client

```python
client = NexusClient()  # reads NEXUS_JWT from env
jwt = client.auth.get_token()
```

## Security
- **No private key in skill:** Only `NEXUS_JWT` (and optional `NEXUS_AUTH_URL`, `NEXUS_DATA_URL`) are read.
- **Network:** Only talks to `api.olaxbt.xyz` and `api-data.olaxbt.xyz`. No telemetry.
- **HTTPS and rate limiting** are enforced.

## Examples

Check the `examples/` directory for complete implementations:

### `examples/basic_usage.py`
Basic authentication and API calls demonstration.

### `examples/news_monitor.py`
Real-time news monitoring with filtering and alerts.

### `examples/market_analysis.py`
Comprehensive market analysis with multiple data sources.

### `examples/wallet_auth.py`
Advanced wallet authentication and JWT management (obtain JWT outside the skill, then pass it in).

## Configuration

### Environment Variables
```bash
# Required
NEXUS_JWT="<your-jwt-from-nexus-auth-flow>"

# Optional
NEXUS_AUTH_URL="https://api.olaxbt.xyz/api"
NEXUS_DATA_URL="https://api-data.olaxbt.xyz/api/v1"
```

### Client Configuration
```python
from olaxbt_nexus_data import NexusClient

client = NexusClient(
    jwt_token="...",  # optional, else uses NEXUS_JWT
    auth_url="https://api.olaxbt.xyz/api",
    data_url="https://api-data.olaxbt.xyz/api/v1",
    timeout=30,
    max_retries=3,
    rate_limit=1000,
)
```

## Error Handling

```python
from olaxbt_nexus_data import NexusClient, NexusError

client = NexusClient()

try:
    data = client.news.get_latest(limit=10)
except NexusError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
    # Re-authenticate or check credentials
except RateLimitError as e:
    print(f"Rate limit exceeded: {e.message}")
    print(f"Reset in: {e.reset_in} seconds")
```

## Testing

```bash
# Install development dependencies
pip install olaxbt-nexus-data[dev]

# Run tests
pytest tests/

# Run with coverage
pytest --cov=olaxbt_nexus_data tests/

# Type checking
mypy src/
```

## Publishing to ClawHub

To publish this skill to [ClawHub](https://clawhub.ai), see **[PUBLISHING.md](PUBLISHING.md)** for step-by-step instructions (account, CLI, permissions, and updates).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Support

- **Documentation**: [https://olaxbt.xyz/skill.md](https://olaxbt.xyz/skill.md)
- **GitHub Issues**: [https://github.com/olaxbt/olaxbt-nexus-data/issues](https://github.com/olaxbt/olaxbt-nexus-data/issues)
- **Email**: hello@olaxbt.xyz

## License

MIT License - See [LICENSE](LICENSE) file for details.

---

**Official OlaXBT Skill** • **Enterprise Grade** • **Production Ready**