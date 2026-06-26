---
name: longbridge-stock
description: Real-time stock quotes and account queries for Longbridge (长桥证券) users. Query US/HK/China stocks, account balance, and positions. Use whenever user mentions stock prices, market data, checking portfolio value, or asking about specific stocks like Apple, Tencent, or Tesla—even if they don't name Longbridge explicitly. Supports AAPL.US, 700.HK, 600519.SH formats.
---

# Longbridge Stock Queries

## Prerequisites

```bash
pip3 install longport
```

## Scripts

Run from the skill directory:

| Script | Usage | Description |
|--------|-------|-------------|
| `quote.py` | `python3 scripts/quote.py AAPL.US GOOGL.US` | Real-time stock quotes |
| `balance.py` | `python3 scripts/balance.py` | Account balance and buying power |
| `positions.py` | `python3 scripts/positions.py` | Portfolio positions |

## Stock Symbol Format

| Market | Format | Examples |
|--------|--------|----------|
| US | `<TICKER>.US` | `AAPL.US`, `GOOGL.US`, `TSLA.US` |
| Hong Kong | `<NUMBER>.HK` | `700.HK` (腾讯), `9988.HK` (阿里) |
| Shanghai A-share | `<CODE>.SH` | `600519.SH` (茅台) |
| Shenzhen A-share | `<CODE>.SZ` | `300750.SZ` (宁德时代) |

See [symbols.md](references/symbols.md) for common stock codes.

## Configuration

Create `.longbridge_config` in one of these locations (priority order):

1. Environment variable: `LONGBRIDGE_CONFIG=/path/to/.longbridge_config`
2. `<skill-dir>/.longbridge_config`
3. `<skill-dir>../../../.longbridge_config` (workspace root)
4. `~/.longbridge_config` or `~/.config/longbridge/.longbridge_config`

Config file format:

```bash
LONGPORT_APP_KEY=<your_app_key>
LONGPORT_APP_SECRET=<your_app_secret>
LONGPORT_ACCESS_TOKEN=<your_access_token>
LONGPORT_REGION=cn
LONGPORT_HTTP_URL=https://openapi.longportapp.cn
LONGPORT_QUOTE_WS_URL=wss://openapi-quote.longportapp.cn
LONGPORT_TRADE_WS_URL=wss://openapi-trade.longportapp.cn
```

Get credentials from https://open.longport.com/

For detailed setup, see [config.md](references/config.md).

## Troubleshooting

| Error | Solution |
|-------|----------|
| `配置文件不存在` | Create `.longbridge_config` |
| `配置文件缺少: LONGPORT_ACCESS_TOKEN` | Add all required fields to config |
| `ModuleNotFoundError: No module named 'longport'` | Run `pip3 install longport` |
| `You do not have access to market's Open API data` | Check Longbridge subscription |
