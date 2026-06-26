# Validation checklist

Use this before publishing live adapter support or production automation.

## Data quality

- [ ] SKU/variant matching is accurate across stores
- [ ] Outlier prices are flagged for manual review
- [ ] Stock status and delivery context are reflected in outputs

## Price logic

- [ ] Effective price formula includes discount, coupon, cashback, and shipping
- [ ] Fee assumptions for arbitrage are documented
- [ ] Currency/rounding behavior is deterministic

## Policy and compliance

- [ ] Each store's ToS allows your intended access method
- [ ] Rate limit and retry logic are safe
- [ ] No sensitive credentials in source code or chat

## Operational safety

- [ ] Alert thresholds are conservative enough to avoid noise
- [ ] Reports include confidence notes for uncertain product matches
- [ ] High-value decisions require manual verification

