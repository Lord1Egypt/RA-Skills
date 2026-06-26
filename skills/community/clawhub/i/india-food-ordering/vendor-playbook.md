# Vendor playbook (multi-vendor)

Primary:

- Swiggy
- Zomato

Optional (if connectors exist):

- EatSure
- magicpin
- ONDC-compatible food apps
- Blinkit Bistro / Zepto Cafe style quick-food verticals

## Comparison dimensions

- final payable amount (not menu price only)
- ETA and delivery reliability
- availability of selected items
- cancellation/refund policies

## Recommended selection strategy

1. user preference
2. item availability
3. lower payable total
4. better ETA

If tie, ask user to choose.

## Fallback sequence

If primary vendor fails:

1. explain failure reason
2. offer equivalent cart on alternate vendor
3. re-show full preview
4. ask explicit confirmation again

## Logging fields (optional)

- timestamp
- vendor
- restaurant
- total
- address label
- order reference
- failure reason (if any)

