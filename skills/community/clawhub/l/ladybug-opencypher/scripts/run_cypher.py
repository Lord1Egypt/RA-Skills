#!/usr/bin/env python3
"""run_cypher.py — Execute Cypher against a Ladybug .lbug file.

Usage:
  python run_cypher.py /path/to/db.lbug -c "MATCH (n) RETURN n LIMIT 5"
  python run_cypher.py /path/to/db.lbug --file query.cypher

Requires: real_ladybug on PYTHONPATH (Ladybug Python bindings).
"""
import argparse
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Cypher against a Ladybug database file.")
    parser.add_argument("database", help="Path to .lbug database file")
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("-c", "--command", metavar="CYPHER", help="Cypher string to execute")
    g.add_argument("-f", "--file", metavar="PATH", help="Path to a .cypher file")
    parser.add_argument(
        "--print-rows",
        action="store_true",
        help="Print each row (default: only row count for non-empty results)",
    )
    args = parser.parse_args()

    try:
        import real_ladybug as lb
    except ImportError:
        print("ERROR: real_ladybug not importable. Install Ladybug bindings and ensure PYTHONPATH.", file=sys.stderr)
        return 1

    db_path = Path(args.database)
    if not db_path.exists():
        print(f"ERROR: database not found: {db_path}", file=sys.stderr)
        return 1

    if args.file:
        cypher = Path(args.file).read_text(encoding="utf-8")
    else:
        cypher = args.command

    db = lb.Database(str(db_path))
    conn = lb.Connection(db)
    result = conn.execute(cypher)

    if isinstance(result, list):
        for i, part in enumerate(result):
            _print_result(part, label=f"statement[{i}]", print_rows=args.print_rows)
    else:
        _print_result(result, label="result", print_rows=args.print_rows)

    return 0


def _print_result(result, *, label: str, print_rows: bool) -> None:
    rows = list(result) if hasattr(result, "__iter__") and not isinstance(result, (str, bytes)) else [result]
    if not rows:
        print(f"{label}: 0 rows")
        return
    print(f"{label}: {len(rows)} row(s)")
    if print_rows:
        for row in rows:
            print(row)


if __name__ == "__main__":
    raise SystemExit(main())
