# Validation checklist

## Safety checks

- [ ] No order placement without explicit "yes" confirmation
- [ ] Confirmation prompt always includes vendor, items, total, address, ETA
- [ ] Address is always validated before checkout
- [ ] COD/non-cancellable constraints are displayed when relevant

## Functional checks

- [ ] Search works for available connectors
- [ ] Cart add/remove updates totals correctly
- [ ] Fallback to alternate vendor works with re-confirmation
- [ ] Error messages are clear and actionable

## Trust checks

- [ ] No hidden auto-retries that can cause duplicate orders
- [ ] No unsupported claims about cancellation/refunds
- [ ] User sees vendor chosen and reason

