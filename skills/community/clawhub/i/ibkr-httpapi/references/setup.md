# ibkr-httpapi setup

HTTP wrapper over Interactive Brokers via `ib_async` + a Linux-native IB
Gateway container. Unlike mt5-httpapi (Windows-only MT5 wheel → needs a
Windows VM), IBKR's IB Gateway runs Linux-native, so the whole stack is just
Linux containers. No KVM, no Windows ISO.

## Requirements

- **IBKR Pro account.** IBKR **Lite** accounts have the TWS API disabled
  entirely, so the bridge cannot connect.
- Linux host with Docker + Docker Compose.
- IBKR login credentials (username + password) for the gateway's unattended
  auto-login.
- IBKR Mobile paired to the account (for the once-per-week 2FA push and the
  daily relogin).
- Optional: an **OPRA / per-exchange market-data subscription** (about $5 to $15 a month
  non-pro) for real-time quotes + option Greeks. Free delayed data
  (15 to 20 min) works for swing timeframes.
- A locally built IB Gateway image (see Licensing below).

## Quick Install

```bash
git clone https://github.com/psyb0t/ibkr-httpapi
cd ibkr-httpapi

cp config/config.yaml.example config/config.yaml   # set api_token, gateway, market_data_type
cp .env.ibkr.example .env.ibkr                     # IBKR login for the gateway auto-login
cp docker-compose.yml.example docker-compose.yml   # stack template (loopback default)

make up
```

First boot pulls/builds images, starts the IB Gateway container, IBC logs
into IBKR (paper or live per `TRADING_MODE`), and the API process connects
over the TWS API socket on port `4002` (paper) or `4001` (live). Verify:

```bash
curl -s -H "Authorization: Bearer $API_TOKEN" http://localhost:8889/v1/ping
# {"status":"ok","connected":true,...}
```

`connected: true` means the gateway socket is live.

## Configuration

Two files, split by concern:

### `config/config.yaml`: the API process config

Copy from `config.yaml.example` and fill in. Key fields:

```yaml
# Bearer token clients send in `Authorization: Bearer ...`.
# Empty string = NO AUTH (open to anyone who can reach the socket).
api_token: ""

# IB Gateway TWS API endpoint.
gateway:
  host: "ibgateway"   # compose service name; 127.0.0.1 from the host
  port: 4002          # 4002 = paper, 4001 = live (TWS uses 7497/7496)
  client_id: 1        # unique int per concurrent socket on the same login
  account: ""         # IBKR account to scope to; empty = gateway default
  connect_timeout: "20s"
  reconnect_backoff: "5s"
  reconnect_max_backoff: "60s"

# ib_async reqMarketDataType:
#   1 = live (needs OPRA / per-exchange subscription)
#   2 = frozen   3 = delayed (15-20 min, free)   4 = delayed-frozen (free)
market_data_type: 1   # set to 3 if you have no market-data subscription

# Optional wickworks TA sidecar (POST /<class>/<symbol>/rates/ta).
# Empty url disables the TA endpoint; it returns 503.
wickworks:
  url: "http://wickworks:8000/"
  timeout: "30s"

# Per-asset-class default exchange/currency/multiplier so callers don't
# repeat them on every request. Futures MUST set exchange explicitly.
contract_defaults:
  stocks:  { exchange: "SMART", currency: "USD" }
  options: { exchange: "SMART", currency: "USD", multiplier: "100" }
  futures: { exchange: "",      currency: "USD" }
  cfd:     { exchange: "SMART", currency: "USD" }
  forex:   { exchange: "IDEALPRO" }
  crypto:  { exchange: "PAXOS", currency: "USD" }
```

`config.yaml` also carries the `pacing` tiers (preemptive rate limits;
defaults sit below IBKR's caps), plus the disk-cache toggles
(`history_cache`, `historian`, `meta_cache`, `exec_history`). Leave the
defaults unless you know why you're changing them.

> **`api_token` must be a strong random value before this server is reachable
> by anything other than localhost.** An empty `api_token` disables auth
> entirely: any process that can reach the listening socket can read account
> state, place orders, and cancel trades on a **real** brokerage account.
> Generate one with `openssl rand -hex 32` and keep it out of git. This is
> non-negotiable before binding to a non-loopback interface or exposing via a
> tunnel.

### `.env.ibkr`: IBKR login for the gateway (gitignored)

Loaded into the **gateway container only** via `env_file:`. Never put these in
`config.yaml`.

```bash
TWS_USERID=your_ibkr_username
TWS_PASSWORD=your_ibkr_password
TRADING_MODE=paper            # paper | live
# READ_ONLY_API=yes           # uncomment to block the trading API entirely
```

### Environment variables

Config values can be overridden at run time (env wins over `config.yaml` for
these):

| Env var | Overrides | Default |
|---|---|---|
| `API_TOKEN` | `config.yaml:api_token` | `""` (no auth) |
| `API_HOST` / `API_PORT` | API bind inside the container | `0.0.0.0` / `8889` |
| `IBKR_GATEWAY_HOST` / `IBKR_GATEWAY_PORT` | `gateway.host` / `gateway.port` | `ibgateway` / `4002` |
| `IBKR_CLIENT_ID` | `gateway.client_id` | `1` |
| `IBKR_ACCOUNT` | `gateway.account` | `""` |
| `WICKWORKS_URL` / `WICKWORKS_TIMEOUT` | `wickworks.url` / `.timeout` | from config |
| `API_HOST_BIND` / `API_HOST_PORT` | nginx host publish (compose) | `127.0.0.1` / `8889` |
| `IBKR_GATEWAY_IMAGE` | gateway image ref (compose) | `ghcr.io/gnzsnz/ib-gateway:stable` |
| `LOG_LEVEL` | log verbosity | `INFO` |
| `TWS_USERID` / `TWS_PASSWORD` / `TRADING_MODE` | gateway login (`.env.ibkr`) |  |

## Ports

| Port | Service | Notes |
|---|---|---|
| `8889` | HTTP API entry (nginx → api) | override with `API_HOST_PORT`; bound to `127.0.0.1` by default |
| `5900` | IB Gateway VNC | `127.0.0.1` only; watch the gateway desktop |
| `8001` | IB Gateway IBC control | `127.0.0.1` only |

nginx is the loopback-published edge; it proxies everything to the `api`
container on internal port `8889`. All client traffic is
`http://localhost:8889/v1/...`. The gateway's TWS API socket (`4001`/`4002`)
stays on the internal `backend` network and is never host-published.

## Management

```bash
make up        # copy config, build/pull images, compose up
make down      # compose down
make logs      # tail compose logs
make build     # rebuild the prod api image
make lint      # ruff + bandit + pyright (dev container)
make test      # pytest (dev container)
make audit     # pip-audit against the hash-locked requirements.txt
```

## Licensing

- **Build the IB Gateway image locally.** IBKR's installer license forbids
  redistributing pre-built images containing their binary.
  [`gnzsnz/ib-gateway-docker`](https://github.com/gnzsnz/ib-gateway-docker)
  builds with a checksum-verified download at build time. Clone it, build it,
  push to your own private registry if you need to share across hosts. Set
  `IBKR_GATEWAY_IMAGE` to your built ref.
- **Daily restart:** IBKR forces a logout once a day (~01:00 ET). IB Gateway
  974+ + IBC 3.15+ handle the relogin unattended; the API reconnects via its
  backoff loop. During the gap every request, `/v1/ping` included, waits for
  the reconnect instead of failing.
- **Weekly 2FA:** IBKR may push a 2FA prompt once per week; accept it from
  the paired IBKR Mobile app.
- **Market-data licensing:** IBKR's terms restrict redistribution of raw OHLC.
  Internal backtesting / model training on the local cache is fine; selling
  raw bars likely violates OPRA/exchange redistributor licenses. Sell derived
  analysis (signals, backtests, aggregated stats) instead.

## OpenClaw / ClawHub config

Consumers configure this skill with the base URL (including `/v1`) and, if the
server has auth, the token:

```bash
export IBKR_HTTPAPI_URL=http://localhost:8889/v1   # primaryEnv
export API_TOKEN=<token>                           # if api_token is set server-side
```

The skill's `openclaw` metadata declares `primaryEnv: IBKR_HTTPAPI_URL` and
requires the `docker` + `curl` binaries. The agent must obtain `API_TOKEN`
from the environment variable the user set or from the user directly, never
by reading `config/config.yaml`, `.env.ibkr`, or any other repository file.

## Public exposure (optional)

The stack ships with commented-out `cloudflared` and `tailscale` sidecars in
`docker-compose.yml.example`. Before exposing publicly:

1. **Set a strong `api_token`.** An empty token + a public path = anyone can
   trade your real account. Catastrophic.
2. **Add a second auth layer** (Cloudflare Access / tailnet ACLs) on the
   public hostname.
3. **Use a paper account** (`TRADING_MODE=paper`) until the auth chain is
   verified end-to-end from a separate network.
4. **Treat the token as a high-value secret.** Losing it is equivalent to
   losing the brokerage account password. Rotate after testing.
