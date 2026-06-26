"""CLI entrypoint for paper matching and recommendation MVP."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from paper_matching.config import load_settings  # noqa: E402
from paper_matching.pipeline import run_pipeline  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the paper matching recommendation MVP")
    parser.add_argument("--db-dsn", help="PostgreSQL DSN, e.g. postgresql://user:pass@host:5432/db")
    parser.add_argument("--output-dir", help="Directory to write run reports")
    parser.add_argument("--profile-source", choices=["db"], default="db", help="Load member profiles from database")
    parser.add_argument("--days", type=int, default=7, help="Lookback window in days")
    parser.add_argument("--top-k", type=int, default=5, help="Recommendations per member")
    parser.add_argument("--max-results-per-member", type=int, default=20, help="ArXiv fetch limit per member")
    parser.add_argument("--dry-run", action="store_true", help="Generate report without sending notifications")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    settings = load_settings(db_dsn=args.db_dsn, output_dir=args.output_dir)
    report = run_pipeline(
        settings=settings,
        days=args.days,
        top_k=args.top_k,
        max_results_per_member=args.max_results_per_member,
        profile_source=args.profile_source,
        dry_run=args.dry_run,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
