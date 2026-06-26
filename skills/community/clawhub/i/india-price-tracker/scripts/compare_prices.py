import argparse
from typing import List
from config import STORES, mock_search


def parse_stores(value: str) -> List[str]:
    raw = [s.strip() for s in value.split(",") if s.strip()]
    return [s for s in raw if s in STORES]


def to_markdown(keyword: str, rows) -> str:
    lines = []
    lines.append(f"# Price comparison: {keyword}")
    lines.append("")
    lines.append("| Store | List Price | Effective Price | In Stock | Rating |")
    lines.append("| --- | ---: | ---: | :---: | ---: |")
    for r in rows:
        lines.append(
            f"| {STORES[r.store]} | {r.list_price:.2f} | {r.effective_price:.2f} | "
            f"{'Yes' if r.in_stock else 'No'} | {r.seller_rating:.1f} |"
        )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Compare product prices across Indian stores.")
    parser.add_argument("--keyword", required=True)
    parser.add_argument("--stores", default="amazon_in,flipkart,reliance_digital,croma,vijay_sales,tata_cliq")
    parser.add_argument("--report", choices=["markdown", "text"], default="text")
    args = parser.parse_args()

    stores = parse_stores(args.stores)
    if not stores:
        raise SystemExit("No valid stores provided.")

    rows = mock_search(args.keyword, stores)
    rows.sort(key=lambda x: (x.effective_price, not x.in_stock))

    if args.report == "markdown":
        print(to_markdown(args.keyword, rows))
    else:
        print(f"Price comparison for: {args.keyword}")
        for r in rows:
            print(
                f"- {STORES[r.store]} | list={r.list_price:.2f} | effective={r.effective_price:.2f} "
                f"| stock={'yes' if r.in_stock else 'no'} | rating={r.seller_rating:.1f}"
            )


if __name__ == "__main__":
    main()

