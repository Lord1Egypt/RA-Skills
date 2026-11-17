# exchangerate — ExchangeRate.host (Currency Exchange Rates)

## What this source has

ExchangeRate.host provides current and historical foreign exchange rates. Data includes:

- Latest exchange rates for 150+ currencies
- Historical rates by date
- Currency conversion
- Time-series data for date ranges

Use exchangerate for: currency conversion, historical exchange rate lookups, financial calculations involving multiple currencies, and complementing FRED's economic data with direct forex rates.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

Free tier requires no API key. Paid tiers offer higher rate limits and additional features.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | throttle to <1/sec |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `latest` | Latest exchange rates | none (optional: `base`, `symbols`) |
| `historical` | Rates for a specific date | `date` (YYYY-MM-DD) |
| `convert` | Convert between currencies | `from`, `to`, `amount` |
| `timeseries` | Rates over a date range | `start_date`, `end_date` |

## Worked examples

```bash
# Get latest rates (USD base)
python3 scripts/reach.py query exchangerate latest '{}'

# Get latest rates with specific base and symbols
python3 scripts/reach.py query exchangerate latest '{"base": "EUR", "symbols": "USD,GBP,JPY"}'

# Get historical rates for a date
python3 scripts/reach.py query exchangerate historical '{"date": "2024-01-01"}'

# Convert currency
python3 scripts/reach.py query exchangerate convert '{"from": "USD", "to": "EUR", "amount": 100}'

# Get time series
python3 scripts/reach.py query exchangerate timeseries '{"start_date": "2024-01-01", "end_date": "2024-01-31", "base": "USD", "symbols": "EUR,GBP"}'
```

## Response shape

**Latest** returns:
```json
{
  "motd": { "msg": "...", "url": "..." },
  "success": true,
  "base": "USD",
  "date": "2024-01-15",
  "rates": {
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 148.50
  }
}
```

**Historical** uses the date as path parameter: `/{date}`.

**Convert** returns:
```json
{
  "success": true,
  "query": { "from": "USD", "to": "EUR", "amount": 100 },
  "result": 92.00
}
```

## Pitfalls

- **Default base is USD.** Use the `base` parameter to change. Free tier may limit base currency options.
- **Historical dates must be weekdays.** Weekend/holiday rates may not be available (markets closed).
- **Rate data is from European Central Bank (ECB).** Updated daily around 4pm CET.
- **Free tier has limited features.** No key needed but some advanced features (crypto, metals, etc.) may require paid tier.
- **Complements Alpha Vantage.** Alpha Vantage has forex with 25/day cap; ExchangeRate.host has no documented cap for basic rates.

## Source links

- API docs: https://exchangerate.host/#/
- GitHub: https://github.com/Formicka/exchangerate.host
