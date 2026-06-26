# India Price Tracker

Starter scripts for India-focused price comparison and monitoring.

## Included stores (normalized keys)

- `amazon_in`
- `flipkart`
- `reliance_digital`
- `croma`
- `vijay_sales`
- `tata_cliq`
- `jiomart`
- `myntra`
- `ajio`
- `nykaa`
- `snapdeal`

## Run

```bash
python3 scripts/compare_prices.py --keyword "iPhone 15" --stores amazon_in,flipkart,croma --report markdown
python3 scripts/track_product.py --product "Sony WH-1000XM5" --stores amazon_in,flipkart --alert-below 24999
python3 scripts/bulk_monitor.py --csv examples/products.india.csv --margin-threshold 0.15
python3 scripts/price_history.py --product "Samsung Galaxy S24" --days 60 --trend-analysis
```

## Notes

- Default implementation uses mock adapters for safe local testing.
- To support live integrations, implement adapter methods in `scripts/config.py` and ensure policy compliance.
- Run [setup.md](setup.md) first and use [validation-checklist.md](validation-checklist.md) before enabling live automation.

