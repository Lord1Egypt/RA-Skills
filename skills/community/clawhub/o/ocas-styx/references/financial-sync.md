# Financial Sync — Bank API Integration

Styx is the enrichment layer. This is the sync layer that feeds it.

## Data Flow

```
Bank APIs → plaid_sync.py → transactions.db (raw)
                                 ↓
                           Styx enrichment pipeline
                           (SearXNG + LLM)
                                 ↓
                      styx.db (enriched merchants,
                               transaction links)
```

## Provider: Plaid (current, active)

- **URL**: https://portal.plaid.com — self-serve, no business verification
- **Free tier**: Up to 100 linked accounts for personal use
- **Supports**: 12,000+ institutions including Capital One and Chase
- **Auth**: Plaid Link flow → access token
- **Python SDK**: `plaid-python`
- **Production base URL**: `https://production.plaid.com`

### Plaid Credentials

- **Client ID**: `6a0d516ea0443c000dedf2a2`
- **Secret**: stored in `<hermes-home>/secrets/plaid.env`
- **DB**: SQLite at `<hermes-home>/data/transactions.db`

### Connected Institutions (May 2026)

Capital One, Chase, Citi, SF Fire Credit Union, Shaka, Wealthfront
- 9 accounts, 896 transactions loaded
- Apple Card NOT available via Plaid (Goldman Sachs doesn't expose it)

### Plaid Link Server Pattern

Plaid Link requires HTTPS. Self-signed cert + Python HTTPS server:

```bash
openssl req -x509 -newkey rsa:4096 -keyout <hermes-home>/secrets/plaid-link.key \
  -out <hermes-home>/secrets/plaid-link.crt -days 365 -nodes \
  -subj "/CN=<SERVER_IP>"
```

Server: `<hermes-home>/plaid-link/server.py`
- `GET /` → serves Plaid Link page
- `POST /api/create-link-token` → `/link/token/create` with `products: ['transactions']`
- `POST /api/exchange-token` → `/item/public_token/exchange` + `/accounts/get` → SQLite

SQLite schema: `plaid_items`, `accounts`, `transactions`, `sync_cursor`

## Sync Scripts

| Script | Purpose |
|--------|---------|
| `<hermes-home>/scripts/plaid_sync.py` | Cursor-based incremental + balance update (daily 7 AM) |
| `<hermes-home>/scripts/plaid_history.py` | Full 24-month historical pull via `/transactions/get` |

## Cron

- **Job**: `a418e00ee21e` at 7:00 AM daily
- **Mode**: `no_agent: true` (script-only, no LLM tokens, no rate limit risk)
- **Requirement**: runs `<hermes-home>/scripts/plaid_sync.py`

## Provider Comparison

### Why Plaid over Teller/SimpleFIN/OFX

| Provider | Cost | Real Banks? | Notes |
|----------|------|-------------|-------|
| Plaid Portal | Free (personal, ≤100 accounts) | Yes | Recommended path |
| Teller | $0.30/enrollment/month | Yes (production) | Free sandbox = fake banks only |
| SimpleFIN Bridge | $15/year | Yes | Bridge fine; bank-access repo uses screen scraping (bad) |
| OFX Direct Connect | Free | Dead | Capital One & Chase OFX endpoints are NXDOMAIN |

### Teller Details (_not used_)

- Free tier = sandbox only, fake banks
- Production requires mTLS (client cert + private key) + user access tokens
- Dashboard is Phoenix LiveView SPA — doesn't render in regular browser tool
- Teller Connect JS requires HTTPS → needs self-signed cert + Cloudflare tunnel or similar

### SimpleFIN Details (not used)

- Bridge at `bridge.simplefin.org`, $15/year
- Plain HTTP + JSON, no SDK needed
- The `bank-access` GitHub repo uses screen scraping — NOT suitable for full history

## Security

- API tokens and certificates in `<hermes-home>/secrets/` (excluded from git)
- Environment variables, never hardcoded in scripts

## State File

`<hermes-home>/data/banksync.md` — full project state for cross-session continuity.

## Lessons

1. **Plaid signup has bot detection** — user must sign up manually at https://dashboard.plaid.com/signup (personal use). Agent browser gets blocked.
2. **Cron must use `no_agent: true`** for script-only jobs. Agent-driven crons hit provider rate limits at scale.
3. **OFX Direct Connect is dead** for consumer Chase/Capital One. Don't waste time.