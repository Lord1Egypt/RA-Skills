# /// script
# dependencies = ["joescorner"]
# requires-python = ">=3.11"
# ///

"""Get posts from a Joe's Corner feed."""

import argparse
import json
import sys

from joescorner import JoesCorner


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feed", help="feed path as owner/slug (e.g. alice/ai-news)")
    parser.add_argument("--limit", type=int, default=10, help="number of posts (default: 10)")
    parser.add_argument("--compact", action="store_true", help="plain text output to save context")
    args = parser.parse_args()

    parts = args.feed.split("/", 1)
    if len(parts) != 2:
        print(f"error: feed must be owner/slug, got '{args.feed}'", file=sys.stderr)
        sys.exit(1)
    username, slug = parts

    client = JoesCorner()
    response = client.list_posts(username, slug, limit=args.limit)

    if not args.compact:
        json.dump(
            [p.model_dump(mode="json") for p in response.items],
            sys.stdout,
            indent=2,
        )
        print()
    else:
        for post in response.items:
            print(f"{post.title}")
            print(f"  {post.url}")
            print()


if __name__ == "__main__":
    main()
