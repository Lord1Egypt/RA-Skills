# JSON Output Samples

Compact examples for parser orientation. Use `SKILL.md` for protected signal schema rules and `references/command-reference.md` for full command parameters.

## News

```bash
methodalgo news --type article --limit 1 --json
```

```json
[
  {
    "type": "article",
    "title": { "en": "Bitcoin market update", "zh": "比特币市场更新" },
    "excerpt": { "en": "Summary...", "zh": "摘要..." },
    "description": { "en": "Full body...", "zh": "正文..." },
    "analysis": { "en": "AI analysis...", "zh": "AI 分析..." },
    "publish_date": "2026-03-30T19:15:56+00:00",
    "url": "https://..."
  }
]
```

`breaking`, `onchain`, and `report` can omit article-style fields or return them as empty strings. Treat empty `excerpt`, `description`, `analysis`, or `url` as absent content.

## Signals

Standard channels such as `breakout-*`, `liquidation`, `exhaustion-*`, `golden-pit-*`, `etf-tracker`, and `market-today` return an array.

```json
[
  {
    "id": "1488261183843864617-0-0",
    "timestamp": 1774899516784,
    "attachments": [],
    "image": "https://m.methodalgo.com/tmp/xxx.webp",
    "signals": [
      {
        "title": "Breakout For NIGHTUSDT.P",
        "description": "Symbol: NIGHTUSDT.P\nType: Break-Down\nTimeFrame: 1h",
        "direction": "bear",
        "details": {
          "Symbol": "NIGHTUSDT.P",
          "TimeFrame": "1h",
          "Type": "DOWN",
          "BreakPrice": "0.04284",
          "Exchange": "BINANCE"
        }
      }
    ]
  }
]
```

`token-unlock` returns an object with a root `signals` array.

```json
{
  "signals": [
    {
      "ts": 1774915176617,
      "symbol": "OP",
      "perc": 1.52,
      "progress": "40.91%",
      "circSup": "6.79 B OP",
      "countDown": "0Day23Hr30Min",
      "marketCap": "$218.99 M",
      "unlockToken": "32.21 M",
      "unlockTokenVal": "$3.36 M (1.52% of M.Cap)"
    }
  ],
  "updatedAt": 1774915176617
}
```

`market-today` is a Discord-style summary stream. For structured BTC Dominance, ETH Dominance, Total Market Cap, Fear & Greed, and Altseason Index values, use `methodalgo totals --json`.

## Snapshot

```bash
methodalgo snapshot SOLUSDT.P 60 --url --json
```

```json
{
  "symbol": "SOLUSDT.P",
  "tf": "60",
  "url": "https://m.methodalgo.com/tmp/xxx.webp",
  "timestamp": 1774899516784
}
```

## Calendar

```bash
methodalgo calendar --countries US --json
```

```json
[
  {
    "title": "Non Farm Payrolls",
    "country": "US",
    "indicator": "Jobs",
    "period": "Mar",
    "actual": "275K",
    "forecast": "198K",
    "previous": "229K",
    "importance": 1,
    "date": "2026-04-03T12:30:00.000Z",
    "source": "Bureau of Labour Statistics",
    "source_url": "http://www.bls.gov"
  }
]
```

## Totals

```bash
methodalgo totals --json
```

```json
{
  "command": "totals",
  "convert": "USD",
  "source": "coinmarketcap+defillama",
  "updatedAt": 1780286619755,
  "metrics": {
    "btcDominance": {
      "metric": "btcDominance",
      "label": "BTC 占比",
      "value": 58.4,
      "displayValue": "58.40%",
      "raw": 58.4
    },
    "fearAndGreed": {
      "metric": "fearAndGreed",
      "label": "恐惧贪婪指数",
      "value": 32,
      "displayValue": "32 Fear",
      "raw": { "value": 32, "classification": "Fear" }
    }
  }
}
```

History metrics include a time series when `--history 30d|90d|1y` is used.

## Macro

```bash
methodalgo macro liquidity --tail 2 --json
```

```json
{
  "command": "macro liquidity",
  "series": [
    {
      "date": "2026-03-20",
      "netLiquidity": 6123456789012,
      "fedAssets": 7123456789012,
      "rrp": 123456789012,
      "tga": 876543210987
    }
  ],
  "meta": {
    "formula": "Fed Assets - RRP - TGA"
  }
}
```

Other macro commands can return dashboards, scorecards, latest values, changes, spreads, z-scores, or comparison series. If upstream macro/FRED requests fail, the CLI may print `✖ 网络错误: fred request failed`.

## Binance Public Market Data

```bash
methodalgo binance price BTCUSDT.P --json
```

```json
{
  "symbol": "BTCUSDT",
  "market": "futures",
  "price": "98765.43",
  "changePercent": "1.23",
  "high": "99000.00",
  "low": "96000.00",
  "quoteVolume": "1234567890.12",
  "closeTime": 1774899516784
}
```

`movers` is normalized by the CLI:

```json
{
  "market": "futures",
  "gainers": [{ "symbol": "ABCUSDT", "pctChange": 18.5, "rankType": "gainer", "direction": "bull" }],
  "losers": [{ "symbol": "XYZUSDT", "pctChange": -12.2, "rankType": "loser", "direction": "bear" }],
  "timestamp": "2026-06-01T04:03:09.428Z"
}
```

For order book, klines, funding, OI, sentiment, basis, exchange-info, and raw endpoint samples, infer from Binance API field names and the command table in `references/command-reference.md`; do not assume a shared wrapper across all subcommands.
