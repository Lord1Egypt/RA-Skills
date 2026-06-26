import argparse
from typing import List
from config import STORES, mock_search


def parse_stores(value: str) -> List[str]:
    raw = [s.strip() for s in value.split(",") if s.strip()]
    return [s for s in raw if s in STORES]


def main():
    parser = argparse.ArgumentParser(description="Track a product and alert on price/margin.")
    parser.add_argument("--product", required=True)
    parser.add_argument("--stores", default="amazon_in,flipkart,croma")
    parser.add_argument("--alert-below", type=float, default=None)
    parser.add_argument("--alert-margin", type=float, default=0.0, help="e.g., 0.2 for 20%%")
    parser.add_argument("--pincode", default=None)
    args = parser.parse_args()

    stores = parse_stores(args.stores)
    if not stores:
        raise SystemExit("No valid stores provided.")

    rows = mock_search(args.product, stores)
    rows.sort(key=lambda x: x.effective_price)
    best = rows[0]
    worst = rows[-1]

    print(f"Tracking: {args.product}")
    if args.pincode:
        print(f"Pincode context: {args.pincode}")

    for r in rows:
        print(
            f"- {STORES[r.store]}: effective={r.effective_price:.2f}, "
            f"list={r.list_price:.2f}, stock={'yes' if r.in_stock else 'no'}"
        )

    if args.alert_below is not None and best.effective_price <= args.alert_below:
        print(f"\nALERT: Best price {best.effective_price:.2f} is below threshold {args.alert_below:.2f}.")

    if worst.effective_price > 0:
        margin = (worst.effective_price - best.effective_price) / worst.effective_price
        if margin >= args.alert_margin > 0:
            print(f"ALERT: Arbitrage spread {margin:.2%} between {STORES[best.store]} and {STORES[worst.store]}.")


if __name__ == "__main__":
    main()

