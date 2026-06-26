import argparse
import csv
from pathlib import Path
from typing import List
from config import STORES, mock_search


def parse_stores(value: str) -> List[str]:
    raw = [s.strip() for s in value.split(",") if s.strip()]
    return [s for s in raw if s in STORES]


def main():
    parser = argparse.ArgumentParser(description="Bulk monitor products from CSV.")
    parser.add_argument("--csv", required=True, dest="csv_path")
    parser.add_argument("--margin-threshold", type=float, default=0.15)
    parser.add_argument("--output", default="reports/alerts.txt")
    args = parser.parse_args()

    in_path = Path(args.csv_path)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    alerts: List[str] = []
    with in_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            product = (row.get("product") or "").strip()
            stores = parse_stores((row.get("stores") or "").strip())
            if not product or not stores:
                continue
            rows = mock_search(product, stores)
            rows.sort(key=lambda x: x.effective_price)
            best = rows[0]
            worst = rows[-1]
            if worst.effective_price <= 0:
                continue
            spread = (worst.effective_price - best.effective_price) / worst.effective_price
            if spread >= args.margin_threshold:
                alerts.append(
                    f"{product}: {spread:.2%} spread | buy {STORES[best.store]} @ {best.effective_price:.2f} "
                    f"| compare {STORES[worst.store]} @ {worst.effective_price:.2f}"
                )

    out_path.write_text("\n".join(alerts) if alerts else "No alerts.", encoding="utf-8")
    print(f"Wrote {len(alerts)} alerts to {out_path}")


if __name__ == "__main__":
    main()

