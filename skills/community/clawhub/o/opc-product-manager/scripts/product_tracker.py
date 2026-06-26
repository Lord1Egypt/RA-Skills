#!/usr/bin/env python3
"""
Product spec tracker for opc-product-manager.

Manages the product index, tracks spec status, and provides complexity summaries.

Usage:
    python3 product_tracker.py [products_dir]
    python3 product_tracker.py --index [products_dir]
    python3 product_tracker.py --status [products_dir]
    python3 product_tracker.py --list [products_dir]
    python3 product_tracker.py --complexity [products_dir]
    python3 product_tracker.py --json [products_dir]

Options:
    --index         Rebuild INDEX.json from product directories
    --status        Show status summary of all products
    --list          List all products (one per line)
    --complexity    Show complexity summary across all products
    --json          Output as JSON instead of human-readable
    products_dir    Path to products directory (default: ./products)

Exit codes:
    0   Success
    1   Error

Dependencies: Python 3.8+ stdlib only
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


def find_products(products_dir: Path) -> list:
    """Find all product directories containing metadata.json."""
    products = []
    if not products_dir.is_dir():
        return products

    for d in sorted(products_dir.iterdir()):
        if not d.is_dir():
            continue
        if d.name.startswith('.') or d.name == 'INDEX.json':
            continue

        meta_path = d / 'metadata.json'
        if meta_path.is_file():
            try:
                with open(meta_path, 'r') as f:
                    meta = json.load(f)
                meta['_dir'] = str(d)
                products.append(meta)
            except (json.JSONDecodeError, OSError) as e:
                print(f"Warning: Could not read {meta_path}: {e}",
                      file=sys.stderr)

    return products


def build_index(products_dir: Path) -> dict:
    """Build INDEX.json from all product metadata."""
    products = find_products(products_dir)

    # Deduplicate: keep latest version per product_id
    latest = {}
    for p in products:
        pid = p.get('product_id', '')
        version = p.get('version', 1)
        if pid not in latest or version > latest[pid].get('version', 1):
            latest[pid] = p

    index = {
        "generated_at": date.today().isoformat(),
        "total_products": len(latest),
        "products": []
    }

    status_counts = {}
    type_counts = {}
    for pid in sorted(latest.keys()):
        p = latest[pid]
        status = p.get('status', 'unknown')
        ptype = p.get('product_type', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
        type_counts[ptype] = type_counts.get(ptype, 0) + 1

        scope = p.get('scope', {})
        entry = {
            "product_id": pid,
            "product_name": p.get('product_name', ''),
            "product_type": ptype,
            "status": status,
            "version": p.get('version', 1),
            "created_at": p.get('created_at', ''),
            "updated_at": p.get('updated_at', ''),
            "complexity_score": scope.get('complexity_score'),
            "complexity_grade": scope.get('complexity_grade'),
            "handoff_generated": p.get('handoff_generated', False),
            "directory": p.get('_dir', '')
        }

        index["products"].append(entry)

    index["status_summary"] = status_counts
    index["type_summary"] = type_counts

    # Write INDEX.json
    index_path = products_dir / 'INDEX.json'
    # Remove _dir before writing
    for proj in index["products"]:
        proj.pop('_dir', None)

    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)

    return index


def get_status_summary(products_dir: Path) -> dict:
    """Get a status summary of all products."""
    products = find_products(products_dir)

    # Deduplicate by product_id
    latest = {}
    for p in products:
        pid = p.get('product_id', '')
        version = p.get('version', 1)
        if pid not in latest or version > latest[pid].get('version', 1):
            latest[pid] = p

    summary = {
        "total": len(latest),
        "by_status": {},
        "by_type": {},
        "products": []
    }

    for pid in sorted(latest.keys()):
        p = latest[pid]
        status = p.get('status', 'unknown')
        ptype = p.get('product_type', 'unknown')
        summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        summary["by_type"][ptype] = summary["by_type"].get(ptype, 0) + 1

        scope = p.get('scope', {})
        summary["products"].append({
            "product_id": pid,
            "product_name": p.get('product_name', ''),
            "product_type": ptype,
            "status": status,
            "version": p.get('version', 1),
            "complexity_score": scope.get('complexity_score'),
            "complexity_grade": scope.get('complexity_grade'),
            "updated_at": p.get('updated_at', p.get('created_at', ''))
        })

    return summary


def get_complexity_summary(products_dir: Path) -> dict:
    """Get complexity summary across all products."""
    products = find_products(products_dir)

    latest = {}
    for p in products:
        pid = p.get('product_id', '')
        version = p.get('version', 1)
        if pid not in latest or version > latest[pid].get('version', 1):
            latest[pid] = p

    result = {
        "total": len(latest),
        "by_grade": {},
        "products": []
    }

    for pid in sorted(latest.keys()):
        p = latest[pid]
        scope = p.get('scope', {})
        grade = scope.get('complexity_grade', 'unscored')
        result["by_grade"][grade] = result["by_grade"].get(grade, 0) + 1

        result["products"].append({
            "product_id": pid,
            "product_name": p.get('product_name', ''),
            "product_type": p.get('product_type', ''),
            "complexity_score": scope.get('complexity_score'),
            "complexity_grade": grade,
            "factors": scope.get('complexity_factors', {})
        })

    return result


def format_status_human(summary: dict) -> str:
    """Format status summary for human reading."""
    lines = []
    lines.append(f"Product Specs: {summary['total']} total")
    lines.append("")

    if summary["by_status"]:
        lines.append("By Status:")
        status_order = ["idea", "spec", "building", "launched", "paused", "archived"]
        for status in status_order:
            count = summary["by_status"].get(status, 0)
            if count > 0:
                lines.append(f"  {status}: {count}")

    if summary["by_type"]:
        lines.append("")
        lines.append("By Type:")
        for ptype, count in sorted(summary["by_type"].items()):
            lines.append(f"  {ptype}: {count}")

    lines.append("")
    lines.append("Products:")
    for p in summary["products"]:
        score = p.get('complexity_score')
        grade = p.get('complexity_grade', '')
        score_str = f" [{score}/10 {grade}]" if score else ""
        version_str = f" v{p['version']}" if p.get('version', 1) > 1 else ""
        updated = f" (updated {p['updated_at']})" if p.get('updated_at') else ""
        lines.append(
            f"  [{p['status']:10s}] {p['product_name']}"
            f" ({p.get('product_type', '')}){score_str}{version_str}{updated}"
        )

    return "\n".join(lines)


def format_complexity_human(result: dict) -> str:
    """Format complexity summary for human reading."""
    lines = []
    lines.append("COMPLEXITY REPORT")
    lines.append("")
    lines.append(
        f"  {'Product':<30s} {'Type':<18s} {'Score':>5s}  {'Grade'}"
    )
    lines.append("  " + "-" * 70)

    for p in result["products"]:
        name = p.get('product_name', p['product_id'])[:30]
        ptype = p.get('product_type', '')[:18]
        score = p.get('complexity_score')
        grade = p.get('complexity_grade', 'unscored')
        score_str = f"{score}/10" if score else "  —"
        lines.append(f"  {name:<30s} {ptype:<18s} {score_str:>5s}  {grade}")

    if result["by_grade"]:
        lines.append("")
        lines.append("By Grade:")
        for grade, count in sorted(result["by_grade"].items()):
            lines.append(f"  {grade}: {count}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Product spec tracker."
    )
    parser.add_argument(
        'products_dir',
        nargs='?',
        default='./products',
        help='Path to products directory (default: ./products)'
    )
    parser.add_argument(
        '--index',
        action='store_true',
        help='Rebuild INDEX.json from product directories'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show status summary of all products'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all products (one per line)'
    )
    parser.add_argument(
        '--complexity',
        action='store_true',
        help='Show complexity summary across all products'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()
    products_dir = Path(args.products_dir)

    if not products_dir.is_dir():
        if args.json:
            print(json.dumps({"error": f"Directory not found: {products_dir}"}))
        else:
            print(f"Directory not found: {products_dir}", file=sys.stderr)
            print("No product specs found. Create your first spec to get started.")
        sys.exit(0)

    try:
        if args.index:
            index = build_index(products_dir)
            if args.json:
                print(json.dumps(index, indent=2))
            else:
                print(f"Index rebuilt: {index['total_products']} products indexed.")

        elif args.complexity:
            result = get_complexity_summary(products_dir)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(format_complexity_human(result))

        elif args.list:
            products = find_products(products_dir)
            seen = {}
            for p in products:
                pid = p.get('product_id', '')
                version = p.get('version', 1)
                if pid not in seen or version > seen[pid].get('version', 1):
                    seen[pid] = p

            if args.json:
                result = [
                    {
                        "product_id": pid,
                        "product_name": p.get('product_name', ''),
                        "product_type": p.get('product_type', '')
                    }
                    for pid, p in sorted(seen.items())
                ]
                print(json.dumps(result, indent=2))
            else:
                for pid in sorted(seen.keys()):
                    p = seen[pid]
                    print(
                        f"{pid}  {p.get('product_name', '')}"
                        f"  ({p.get('product_type', '')})"
                    )

        else:
            # Default: status summary
            summary = get_status_summary(products_dir)
            if args.json:
                print(json.dumps(summary, indent=2))
            else:
                print(format_status_human(summary))

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
