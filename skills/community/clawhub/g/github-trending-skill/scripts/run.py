import argparse

from scripts.daily import run as run_daily
from scripts.monthly import run as run_monthly


def main() -> None:
    parser = argparse.ArgumentParser(description="GitHub Trending Skill Runner")
    parser.add_argument("--mode", choices=["daily", "monthly"], default="daily")
    parser.add_argument("--language", default="All")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    if args.mode == "daily":
        output = run_daily(language=args.language, limit=args.limit)
    else:
        output = run_monthly(language=args.language, limit=args.limit)

    print(output)


if __name__ == "__main__":
    main()

