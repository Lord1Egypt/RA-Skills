"""
Instagram Daily Digest — entry point.

Usage:
    python main.py                              # run and save digest.html
    python main.py --accounts user1 user2       # override accounts from config
    python main.py --list-accounts              # print configured accounts and exit
"""

import argparse
import shutil
import sys
from pathlib import Path

import config
import scraper
import analyzer
import emailer


def run(accounts: list[str] | None = None) -> None:
    if accounts:
        config.INSTAGRAM_ACCOUNTS = accounts
    print("=" * 60)
    print("Instagram Daily Digest")
    print("=" * 60)

    # 1. Scrape ────────────────────────────────────────────────────
    print("\n[1/2] Scraping Instagram accounts…")
    results, tmp_dir = scraper.scrape()

    total_reels   = sum(len(d["reels"])   for d in results.values())
    total_stories = sum(len(d["stories"]) for d in results.values())
    print(f"\nFound: {total_reels} reels, {total_stories} stories across "
          f"{len(results)} accounts.")

    if total_reels == 0 and total_stories == 0:
        print("Nothing to report today.")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return

    # 2. Analyze ───────────────────────────────────────────────────
    print("\n[2/2] Transcribing and summarizing audio…")
    analyzer.analyze_all(results)

    # 3. Save HTML ─────────────────────────────────────────────────
    html = emailer.build_html(results)
    out = Path("digest.html")
    out.write_text(html, encoding="utf-8")
    print(f"\nSaved to {out.resolve()}")

    # 4. Cleanup ───────────────────────────────────────────────────
    shutil.rmtree(tmp_dir, ignore_errors=True)
    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instagram Daily Digest")
    parser.add_argument("--accounts", nargs="+", metavar="USERNAME",
                        help="Override the account list from config (space-separated usernames)")
    parser.add_argument("--list-accounts", action="store_true",
                        help="Print configured accounts and exit")
    args = parser.parse_args()

    if args.list_accounts:
        accounts = args.accounts or config.INSTAGRAM_ACCOUNTS
        print("Configured accounts:")
        for a in accounts:
            print(f"  @{a}")
        sys.exit(0)

    try:
        run(accounts=args.accounts)
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(0)
