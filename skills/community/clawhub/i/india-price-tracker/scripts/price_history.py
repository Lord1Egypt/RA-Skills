import argparse
import random
from typing import List
from config import STORES


def parse_stores(value: str) -> List[str]:
    raw = [s.strip() for s in value.split(",") if s.strip()]
    return [s for s in raw if s in STORES]


def mock_history(product: str, days: int, store: str) -> List[float]:
    seed = hash((product, store, days)) % 100000
    random.seed(seed)
    base = random.randint(7000, 85000)
    points = []
    for _ in range(days):
        drift = random.randint(-600, 600)
        base = max(100.0, base + drift)
        points.append(float(base))
    return points


def summarize(values: List[float]) -> str:
    low = min(values)
    high = max(values)
    avg = sum(values) / len(values)
    return f"low={low:.2f} high={high:.2f} avg={avg:.2f}"


def main():
    parser = argparse.ArgumentParser(description="Analyze price history trends.")
    parser.add_argument("--product", required=True)
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--stores", default="amazon_in,flipkart")
    parser.add_argument("--trend-analysis", action="store_true")
    args = parser.parse_args()

    stores = parse_stores(args.stores)
    if not stores:
        raise SystemExit("No valid stores provided.")

    print(f"Price history: {args.product} ({args.days} days)")
    for s in stores:
        vals = mock_history(args.product, args.days, s)
        print(f"- {STORES[s]}: {summarize(vals)}")
        if args.trend_analysis:
            trend = "up" if vals[-1] > vals[0] else "down" if vals[-1] < vals[0] else "flat"
            print(f"  trend={trend} start={vals[0]:.2f} end={vals[-1]:.2f}")


if __name__ == "__main__":
    main()

