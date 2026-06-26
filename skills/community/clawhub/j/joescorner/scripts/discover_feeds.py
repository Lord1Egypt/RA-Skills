# /// script
# dependencies = ["joescorner"]
# requires-python = ">=3.11"
# ///

"""Discover public feeds on Joe's Corner."""

import argparse
import json
import sys

from joescorner import FeedSort, JoesCorner


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--sort",
        choices=["popular", "alphabetical", "newest"],
        default="popular",
        help="sort order (default: popular)",
    )
    parser.add_argument("--limit", type=int, default=20, help="number of feeds (default: 20)")
    parser.add_argument("--compact", action="store_true", help="plain text output to save context")
    args = parser.parse_args()

    sort = FeedSort(args.sort)
    client = JoesCorner()
    response = client.list_feeds(sort=sort, limit=args.limit)

    if not args.compact:
        json.dump(
            [f.model_dump(mode="json") for f in response.items],
            sys.stdout,
            indent=2,
        )
        print()
    else:
        for feed in response.items:
            desc = f" - {feed.description}" if feed.description else ""
            print(f"{feed.owner}/{feed.slug}: {feed.name}{desc}")


if __name__ == "__main__":
    main()
