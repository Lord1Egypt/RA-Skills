# aeon/ibkr-investing

Invest in stocks and ETFs on Interactive Brokers from aeon, gated by the same explicit human-in-the-loop confirmation as `aeon/okx-trading`. Defaults to **paper trading**.

> Bootstrapped on top of [amuletxheart/ibkr-openclaw](https://clawhub.ai/amuletxheart/ibkr-openclaw) — that skill provided the read-only `ib_async` connection patterns we re-used. Adds the propose→YES→execute gate, guardrails, snapshot with day-over-day delta, drawdown-reserve trigger, and audit log.

## What's new in v0.1.1

- `ibkr_propose_trade.py` prints an absolute `Pending file: /...` line alongside the proposal id. The LLM must use that path verbatim with `file_read` rather than guessing `~/.aeon/ibkr/pending/<id>.json` — the tilde-expansion was ambiguous when aeon runs as a service user. Mirrors the okx-trading v0.3.2 fix.

## What it does

- Read-only: NAV, balances, positions with mark, quotes (delayed-frozen by default), historical OHLCV with RSI/SMA, gateway status.
- Trade-with-confirmation: propose → user replies `YES <id>` in chat → execute. Supports market and limit orders, fractional shares for eligible securities.
- DCA: scheduled recurring propose for fixed-USD buys of ETFs.
- Drawdown reserve: watcher recommends a dip-buy when NAV drops ≥ 30 % from ATH; token-gated like everything else.

## One-time setup

The skill talks to a running **IB Gateway** — IBKR's own software. You need to run it before any script will work.

### 1. Install Docker

```bash
curl -fsSL https://get.docker.com | sh
docker --version
```

### 2. Pull and configure IB Gateway Docker

```bash
mkdir -p ~/.aeon/ibkr-runtime && cd ~/.aeon/ibkr-runtime
git clone https://github.com/gnzsnz/ib-gateway-docker.git
cd ib-gateway-docker
```

Create a `.env` next to the cloned `docker-compose.yml`:

```env
TWS_USERID=your_ibkr_username
TWS_PASSWORD=your_ibkr_password
TRADING_MODE=paper                # or 'live' once you're ready
READ_ONLY_API=no                  # MUST be 'no' for trade placement
TWS_ACCEPT_INCOMING=auto
TWS_MASTER_CLIENT_ID=1
TWOFA_DEVICE=IB Key               # see IBKR web portal → Settings → Security
TWOFA_TIMEOUT_ACTION=exit
TIME_ZONE=America/New_York
TZ=America/New_York
SAVE_TWS_SETTINGS=yes
AUTO_RESTART_TIME=23:45
```

`READ_ONLY_API=no` is the flag that lets us actually place orders. The skill's gate (propose → YES → execute) is what makes that safe.

### 3. Start the Gateway

```bash
docker compose up -d
docker logs algo-trader-ib-gateway-1 --tail 30   # check it's authenticating
```

Approve the 2FA prompt on your **IBKR Mobile app** when it pops up. Once the logs say "API Server is ready", the API is live on:

| Mode | Port |
|---|---|
| Paper | `4002` |
| Live | `4001` |

The Gateway auto-restarts daily at 23:45 (your `TIME_ZONE`); plan your scheduled tasks around this — anything firing at the restart minute will fail.

### 4. Install the skill's Python deps

```bash
pip3 install -r ~/.aeon/skills/aeon/ibkr-investing/requirements.txt
```

If your distro pushes back with `externally-managed-environment`, use the venv pattern from your OKX setup:

```bash
~/.aeon/venv/bin/pip install -r ~/.aeon/skills/aeon/ibkr-investing/requirements.txt
```

### 5. Smoke-test the connection

```bash
~/.aeon/venv/bin/python3 ~/.aeon/skills/aeon/ibkr-investing/scripts/ibkr_gateway_status.py
```

Expected:

```
IBKR env: PAPER (127.0.0.1:4002)
  TCP connect to 127.0.0.1:4002 OK
  IBKR API handshake OK; managed accounts: ['DUxxxxxxx']
```

If reachability fails, the script tells you which step to debug (Docker container, 2FA, port mapping).

### 6. Add IBKR env vars to aeon

Edit `~/.aeon/.env`:

```bash
export IBKR_LIVE_MODE=0                                   # paper
export IBKR_DEFAULT_EXCHANGE=SMART
export IBKR_DEFAULT_CURRENCY=USD
export IBKR_ALLOWED_SYMBOLS=VOO,VTI,QQQ,BND               # tight allow-list to start
export IBKR_MAX_NOTIONAL_USD_PER_TRADE=200
export IBKR_MAX_DAILY_NOTIONAL_USD=1000
```

`chmod 600 ~/.aeon/.env`. Then either restart aeon or `source ~/.aeon/.env` if running interactively.

## Going live

When you're confident in the paper flow:

1. In `ib-gateway-docker/.env`, change `TRADING_MODE=live`.
2. `docker compose down && docker compose up -d`.
3. Re-approve 2FA on the IBKR Mobile app.
4. In `~/.aeon/.env`, change `IBKR_LIVE_MODE=1`.
5. Lower the caps to whatever you're willing to lose to a bug:
   ```bash
   export IBKR_MAX_NOTIONAL_USD_PER_TRADE=50
   export IBKR_MAX_DAILY_NOTIONAL_USD=200
   ```
6. Restart aeon.

The same skill code runs against both modes — only the `flag` and the connection port differ.

## State on disk

```text
~/.aeon/ibkr/
  pending/<id>.json         # proposed trades awaiting YES
  notional_log.jsonl        # append-only log of executed notional (for daily cap)
  snapshots/<date>.json     # daily account snapshots
  audit.jsonl               # lifecycle audit log (proposals, fills, rejects)
  dca_dip_state.json        # drawdown-trigger state
```

Files are 0600 so the confirmation token is not world-readable. Pending proposals expire automatically after 10 minutes.

## What the user types in chat

- "What's my IBKR balance?" → `ibkr_get_balance.py`.
- "What's VOO at?" → `ibkr_get_quote.py --symbol VOO`.
- "Buy $50 of VOO." → `ibkr_propose_trade.py`, posts proposal, you reply `YES abc12345`.
- "DCA $200 of VOO monthly on the 1st at 9:30 ET." → agent registers a `schedule_create` with the propose script.
- "Show me yesterday's IBKR snapshot." → `ibkr_snapshot.py --no-write`.

## Limitations in v0.1.0

- US ETFs / stocks on SMART exchange in USD work cleanly. Other exchanges and currencies are accepted but not extensively tested.
- Options, futures, mutual funds, and forex are out of scope. The shared client functions can be extended for them in v0.2.0.
- Multi-currency NAV math is not normalised — `BASE` currency is whatever your IBKR account is denominated in.
- Only daily-bar history is fetched for snapshots. Intraday bars require a paid market-data subscription.

## Credits

- [amuletxheart/ibkr-openclaw](https://clawhub.ai/amuletxheart/ibkr-openclaw) — read-only `ib_async` patterns and IB Gateway Docker setup recipe.
- [gnzsnz/ib-gateway-docker](https://github.com/gnzsnz/ib-gateway-docker) — the IB Gateway Docker image.
- [ib_async](https://github.com/ib-api-reloaded/ib_async) — Python IBKR API wrapper (maintained fork of `ib_insync`).
