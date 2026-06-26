---
name: india-price-tracker
description: Track and compare product prices across popular Indian stores (Amazon India, Flipkart, Reliance Digital, Croma, Vijay Sales, Tata CLiQ, and more), compute effective prices after offers/cashback, detect arbitrage opportunities, and monitor price history with alerts.
metadata: {"openclaw":{"emoji":"🇮🇳","homepage":"https://clawhub.ai/Michael-laffin/price-tracker","requires":{"bins":["python3"]}}}
---

# India Price Tracker

## Overview

Track prices across major Indian ecommerce stores and compare true payable cost, not just listed price.

Primary stores:

- Amazon India
- Flipkart
- Reliance Digital
- Croma
- Vijay Sales
- Tata CLiQ

Additional stores:

- JioMart
- Myntra
- AJIO
- Nykaa
- Snapdeal

## Disclaimer

This skill provides tracking and comparison workflows only. It does not execute purchases. Store APIs, policies, and pricing terms can change. You are responsible for complying with each platform's Terms of Service and applicable laws.

Use at your own risk. The skill author/publisher/developer is not liable for direct or indirect loss, trading losses, missed opportunities, scraping/API bans, account restrictions, or other damages arising from use or misuse of this guidance.

## What is improved vs generic price trackers

1. **India-first store adapters**
   - Store list and naming normalized for Indian catalogs.

2. **Effective price modeling**
   - Calculates final payable estimate:
   - `effective_price = listing_price - instant_discount - coupon_discount - card_cashback + shipping`

3. **Pincode-aware availability**
   - Supports regional availability and shipping variance inputs.

4. **Arbitrage with fee model**
   - Computes net margin after platform fees and shipping.

5. **History + trend flags**
   - Tracks 30/60/90 day movement and volatility.

6. **Alerting modes**
   - Price-drop threshold
   - Margin threshold
   - Restock + price condition

## Setup

On first use, read [setup.md](setup.md), then run scripts in `mock` mode first.

## Core workflows

### 1) Compare prices across stores

```bash
python3 scripts/compare_prices.py \
  --keyword "iPhone 15 128GB" \
  --stores amazon_in,flipkart,reliance_digital,croma,vijay_sales,tata_cliq \
  --report markdown
```

### 2) Track a product with threshold alerts

```bash
python3 scripts/track_product.py \
  --product "Sony WH-1000XM5" \
  --stores amazon_in,flipkart,croma \
  --alert-below 24999 \
  --alert-margin 0.18 \
  --pincode 560001
```

### 3) Bulk monitor from CSV

```bash
python3 scripts/bulk_monitor.py \
  --csv examples/products.india.csv \
  --margin-threshold 0.15 \
  --output reports/alerts.txt
```

### 4) Price history analysis

```bash
python3 scripts/price_history.py \
  --product "Samsung Galaxy S24" \
  --days 60 \
  --stores amazon_in,flipkart \
  --trend-analysis
```

## Strategy rules

- Prefer **effective price** over headline price.
- Compare same SKU/variant only (storage, color, seller condition).
- Flag uncertain matches for manual review.
- Never assume stock parity across stores.
- Respect platform policies if implementing live adapters.

## Output format

When asked to analyze products, return:

1. best store by effective price
2. next best alternative
3. arbitrage opportunity (if margin above threshold)
4. confidence notes (match quality, availability, shipping)

## Files

- `scripts/compare_prices.py`
- `scripts/track_product.py`
- `scripts/bulk_monitor.py`
- `scripts/price_history.py`
- `scripts/config.py`
- `examples/products.india.csv`
- `README.md`

## Validation

- Use [validation-checklist.md](validation-checklist.md) before switching to any live adapter mode.
- Re-validate each store's terms, rate limits, and allowed integration method before production automation.

