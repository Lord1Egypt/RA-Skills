---
name: nasdaq100-futures-node
description: Fetch the latest Nasdaq-100 futures quote (default NQ=F) via Yahoo Finance chart API using Node.js and return price, change, percent change, and timestamp. Use when the user asks for Nasdaq-100 futures, NQ futures, NQ=F, 纳指100期货, or wants the latest quote and change metrics.
---

# Nasdaq-100 Futures Quote (Node.js)

## Quick Start

This is an OpenClaw/ClawHub-style **Node.js** skill. The runtime entrypoint is `scripts/main.handler` (see `manifest.json`), and the exposed function is `get_nasdaq100_futures`.

Use this skill when you need the **latest** quote for Nasdaq-100 futures (or another Yahoo Finance symbol), including:
- **regularMarketPrice**
- **previousClose**
- **change** and **changePercent**
- **timestamp** (formatted)

## How to Call

Call the function `get_nasdaq100_futures` (as declared in `manifest.json`) with optional parameters:

- **symbol** (string, optional): Yahoo Finance symbol. Default is `NQ=F` (Nasdaq-100 futures).

### Invocation Contract (Agent skill calling shape)

The handler expects the OpenClaw event shape (function parameters wrapped under `parameters`):

```json
{
  "parameters": {
    "symbol": "NQ=F"
  }
}
```

If `parameters.symbol` is omitted, it defaults to `NQ=F`.

## Output

On success, returns a JSON object with these keys:
- **symbol**: the requested symbol (e.g. `NQ=F`)
- **price**: latest price (string, 2 decimals)
- **change**: price change vs previous close (string, signed, 2 decimals)
- **changePercent**: percent change vs previous close (string, signed, 2 decimals)
- **time**: formatted timestamp string
- **message**: human-readable Chinese summary

On failure, returns:
- **error**: true
- **message**: error message

## Examples

### Example: Default Nasdaq-100 futures

Input:

```json
{
  "parameters": {}
}
```

Output (example):

```json
{
  "symbol": "NQ=F",
  "price": "15780.50",
  "change": "+120.25",
  "changePercent": "+0.77",
  "time": "2025-06-10 14:30:00",
  "message": "纳斯达克100期货最新价: $15780.50 (+120.25 / +0.77%) 数据时间: 2025-06-10 14:30:00"
}
```

### Example: Custom symbol

Input:

```json
{
  "parameters": {
    "symbol": "ES=F"
  }
}
```

## Notes

- Data source is Yahoo Finance chart API (`query1.finance.yahoo.com`). Results depend on market hours and network availability.
- Requires Node.js **>= 18** (uses built-in `fetch`).
- If you need a different data provider, adjust `scripts/main.js` accordingly.

## Additional resources

- OpenClaw runtime details: [references/openclaw.md](references/openclaw.md)