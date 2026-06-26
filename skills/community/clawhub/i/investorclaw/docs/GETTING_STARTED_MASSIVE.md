# InvestorClaw — Get Started (Massive Edition)

A deterministic portfolio-analysis engine that prices equities, ETFs, bonds,
and **CME futures** through the [Massive](https://massive.com) (massive.com)
market-data API. It ships as a prebuilt container — **no source build, no
private dependencies to clone.** All foundation primitives (incl. `clio`) and
the engine are baked into the image.

> You will need: **Docker**, and a **Massive API key** with the Futures
> entitlement. If you drive InvestorClaw through an agent (Claude or OpenClaw),
> that agent installs the skill and brings the container up for you.

---

## Install

Pick the path that matches how you work. All three run the **same** container —
the agent paths just automate the Docker steps and wire up the MCP connection.

### A. From Claude (Claude Code / Claude Desktop)

Ask Claude to install it **directly from the Git repo** — no ClawHub needed:

1. Add the repo as a plugin marketplace, then install:

   ```text
   /plugin marketplace add argonautsystems/InvestorClaw
   /plugin install investorclaw
   ```

   (or just say: "Install InvestorClaw from github.com/argonautsystems/InvestorClaw".)

2. Then ask Claude:

   > "Set up InvestorClaw and show me my holdings."

   Claude runs the skill's setup, which **pulls `ghcr.io/argonautsystems/ic-engine:4.7.7-cpu`**
   and starts it (MCP-HTTP on `localhost:18090`, dashboard on `localhost:18092`).
   No build, no `uv`, no source clone.

3. Give it your Massive key once (Claude writes it to the container's mounted
   keys file, never to the image):

   > "Add my Massive API key: `<key>`"

   or manually: `echo 'MASSIVE_API_KEY=<key>' >> ~/.investorclaw/data/keys.env`

### B. From OpenClaw / ZeroClaw

OpenClaw installs from ClawHub:

```bash
clawhub install investorclaw
```

OpenClaw then walks the skill's `install.yaml` (container-first): it checks for
Docker, pulls the image, and `docker compose up`s the service. ZeroClaw on
recent builds can also do `zeroclaw services install <compose-url>`. Then ask
the agent any portfolio question. Add `MASSIVE_API_KEY` to the mounted
`keys.env` the same way as above.

### C. Direct Docker (no agent)

Pull the public image (no registry login required):

```bash
docker pull ghcr.io/argonautsystems/ic-engine:4.7.7-cpu
```

Use it via the one-shot CLI (below) or run the full service (§"Full service").

---

## Try it with the sample portfolio

We ship a fully de-identified sample, `ubs_sample_cleansed.csv` (every quantity
normalized to 1, all account names and dollar balances stripped). It exercises
every asset class: top-50 tech equities, broad/sector ETFs, 10
municipal/treasury bonds, and **5 live CME futures contracts** (`ESH7`, `NQM6`,
`CLN6`, `GCF7`, `ZBM6`).

```bash
mkdir -p ic-data/portfolios ic-data/reports
cp ubs_sample_cleansed.csv ic-data/portfolios/
```

Run a holdings snapshot forced through Massive:

```bash
docker run --rm \
  -e INVESTORCLAW_PRICE_PROVIDER=massive \
  -e MASSIVE_API_KEY="$MASSIVE_API_KEY" \
  -e INVESTORCLAW_PORTFOLIO_DIR=/data/portfolios \
  -e INVESTOR_CLAW_PORTFOLIO_DIR=/data/portfolios \
  -e IC_PORTFOLIO_DIR=/data/portfolios \
  -v "$PWD/ic-data:/data" \
  --entrypoint /opt/ic-engine/.venv/bin/investorclaw \
  ghcr.io/argonautsystems/ic-engine:4.7.7-cpu holdings
```

`INVESTORCLAW_PRICE_PROVIDER=massive` forces **Massive as the only data
provider** — no yfinance fallback. Your key is read at runtime; it is never
baked into the image.

### Expected result

A JSON summary on stdout. The futures section is priced via Massive's
`/futures/vX` feed, with correct CME notional (price × contract multiplier ×
contracts):

```
provider_used: massive
positions: {equity: 249, bond: 10, cash: 19, futures: 5, metals: 1}
top_futures:
  NQM6  E-mini Nasdaq-100   ≈ price × 20
  ESH7  E-mini S&P 500      ≈ price × 50
  GCF7  COMEX Gold          ≈ price × 100
  ZBM6  US T-Bond           ≈ price × 1000
  CLN6  WTI Crude           ≈ price × 1000
```

`provider_used: massive` + five `top_futures` entries = the Massive futures
path works end-to-end.

---

## Full service — MCP + dashboard

The default entrypoint serves an MCP-HTTP API and an interactive dashboard:

```bash
docker run --rm -p 18090:8090 -p 18092:8092 \
  -e INVESTORCLAW_PRICE_PROVIDER=massive \
  -v "$PWD/ic-data:/data" \
  ghcr.io/argonautsystems/ic-engine:4.7.7-cpu
# health: curl http://localhost:18090/healthz   • dashboard: http://localhost:18092
```

Drop your key into `ic-data/keys.env` (`MASSIVE_API_KEY=...`) and the service
resolves it at startup — keys live only in your mounted volume.

---

## Massive support reference

InvestorClaw treats Massive (massive.com) as its **primary paid market-data
provider** across the whole surface:

| Capability | How Massive is used |
|---|---|
| **Batch equity/ETF quotes** | One call for all symbols — required for 100+ symbol portfolios where the free yfinance path rate-limits |
| **CME futures** | `/futures/vX` snapshot + history (CBOT/CME/NYMEX/COMEX). The **only** provider routed for futures |
| **Notional valuation** | Engine carries the CME dollar-multiplier map; a contract symbol values to `price × multiplier × contracts` automatically |
| **History / aggregates** | Daily OHLCV for equities and futures |

**Provider selection**

- `INVESTORCLAW_PRICE_PROVIDER=massive` — force Massive only (no fallback).
- `INVESTORCLAW_PRICE_PROVIDER=auto` (default) — Massive is auto-pinned when
  `MASSIVE_API_KEY` is set; otherwise free yfinance.

**Futures ticker format** — standard `<product><month-code><year>`, e.g. `ESH7`
(E-mini S&P, Mar '27), `GCF7` (gold, Jan '27). Broker slash/at prefixes
(`/ESZ25`, `@GCZ25`) are accepted. Covered products include ES/MES, NQ/MNQ,
YM, RTY, CL/MCL, NG, GC/MGC, SI, HG, the ZT/ZF/ZN/ZB rate complex, 6E/6J FX,
grains, and CME crypto.

**Keys** — set `MASSIVE_API_KEY` (env or the mounted `keys.env`). `MASSIVE_API_KEY`
is accepted as an alias. Keys are read at runtime and never baked into the image.

---

## Notes

- **No build step.** Engine + `clio` foundation library are in the image. You
  never clone a source repo or run `uv sync`.
- **Other brokers.** Swap in any Schwab / Fidelity / Vanguard / UBS CSV, XLS,
  or PDF export — the setup wizard auto-detects the format.
- **Source.** Engine: <https://github.com/argonautsystems/ic-engine> ·
  Primitives: <https://github.com/argonautsystems/clio> ·
  Skill: `clawhub install investorclaw`
