---
name: open-exchange-rate
description: Get real-time exchange rates and currency conversion using free public ExchangeRate-API. No API key required. Use when users ask for current exchange rates, currency conversion calculations, or need to check currency prices.
---

# open-exchange-rate

## Overview

A simple skill for getting real-time exchange rate information and performing currency conversion using the public ExchangeRate-API. No API key required for requests.

## Features

- **Get latest exchange rates**: Retrieve up-to-date exchange rates for all currencies
- **Currency conversion**: Convert an amount from one currency to another
- **List all available currencies**: Show a complete list of supported currency codes

## Usage

### Get latest rates for base currency
```bash
python3 scripts/get_rates.py --base USD
```

### Convert currency
```bash
python3 scripts/convert.py --from USD --to EUR --amount 100
```

### List all available currencies
```bash
python3 scripts/list_currencies.py
```

## Resources

### scripts/
- `get_rates.py` - Get latest exchange rates with optional base currency
- `convert.py` - Convert amount between two currencies
- `list_currencies.py` - List all available currency codes and names

