# moomoo / Futu OpenD Setup Guide

## Overview

Architecture: **your scripts -> OpenD -> moomoo/Futu servers -> exchanges**

OpenD is required for all quote and trading API calls. This skill assumes `127.0.0.1:11111` unless you override `--host` / `--port`.

## 1. Install OpenD

Official resources:
- moomoo OpenAPI download page: <https://www.moomoo.com/download/OpenAPI>
- moomoo OpenAPI docs: <https://openapi.moomoo.com/moomoo-api-doc/en/>
- Futu OpenAPI docs: <https://openapi.futunn.com/futu-api-doc/en/>

According to the official docs, Visualization OpenD and Command Line OpenD are available on macOS, Windows, Ubuntu, and CentOS.

Version hygiene matters:
- Keep OpenD reasonably close to the Python SDK version you install.
- moomoo publishes minimum OpenD version requirements alongside SDK releases on the download page.
- If the SDK is newer than OpenD, upgrade OpenD first.

## 2. Log in to OpenD

1. Start Visualization OpenD or Command Line OpenD.
2. Log in with your moomoo/Futu account.
3. Confirm quote and trading permissions inside the OpenD UI.
4. Check that the socket service is listening on the host/port you expect.

Default settings:
- Host: `127.0.0.1`
- Port: `11111`

## 3. Install the Python SDK

Pick one package:

```bash
pip install futu-api
# import path: futu
```

```bash
pip install moomoo-api
# import path: moomoo
```

The bundled scripts auto-detect either package at runtime.

## 4. Verify the connection

```bash
python3 scripts/setup_check.py
```

That script validates:
- quote connectivity (`get_global_state()`)
- discovered trading accounts (`get_acc_list()`)
- simulated account access (`accinfo_query(trd_env=SIMULATE)`)

## 5. Simulated vs live trading

| Feature | Simulated | Live |
|---------|-----------|------|
| CLI env flag | `--env sim` | `--env real` |
| API enum | `TrdEnv.SIMULATE` | `TrdEnv.REAL` |
| Unlock required | No | Yes, `unlock_trade(...)` |
| Script guardrails | None | `--confirm` + unlock password env var |
| Capital at risk | No | Yes |

The bundled `trade.py` script unlocks only for the requested live action and then immediately re-locks the account.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| `ImportError` / `Neither futu-api nor moomoo-api is installed` | SDK missing | Install `futu-api` or `moomoo-api` |
| Connection refused | OpenD not running or wrong port | Start OpenD, verify `--host` / `--port` |
| `unlock_trade failed` | Wrong password, no live-trading permission, or account not available in OpenD | Verify the password and permissions in OpenD / app |
| Empty quote data | Market closed, no quote entitlement, or bad ticker | Check market hours, entitlements, and `MARKET.CODE` format |
| Order rejected | Buying power, market session, lot size, ticker, or market mismatch | Check funds, session, and `--market` / ticker prefix |
| `--help` works but real commands fail | Lazy imports are fine; runtime dependency or OpenD is still missing | Install the SDK and verify OpenD login |
