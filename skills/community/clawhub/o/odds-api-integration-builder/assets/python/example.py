"""Discover catalogs/events and fetch complete public odds snapshots."""
import argparse
import json
import sys
from odds_client import ClientError, OddsClient, utc_seconds


def parser():
    cli = argparse.ArgumentParser(description="odds-api.net Python starter. Runtime ODDS_API_KEY required for network calls.")
    commands = cli.add_subparsers(dest="command", required=True)
    catalog = commands.add_parser("catalog")
    catalog.add_argument("--kind", choices=["sports", "leagues", "bookmakers"], default="sports")
    catalog.add_argument("--sport")
    catalog.add_argument("--country-code")
    events = commands.add_parser("events")
    events.add_argument("--sport", required=True)
    events.add_argument("--league")
    events.add_argument("--from", dest="from_ts", required=True)
    events.add_argument("--to", dest="to_ts", required=True)
    events.add_argument("--team")
    odds = commands.add_parser("snapshot")
    odds.add_argument("--event-id", required=True)
    odds.add_argument("--bookmakers")
    odds.add_argument("--types")
    odds.add_argument("--periods")
    return cli


def main():
    args = parser().parse_args()
    if args.command == "catalog":
        if args.sport and args.kind != "leagues":
            raise ClientError("--sport applies to the leagues catalog.")
        if args.country_code and args.kind != "bookmakers":
            raise ClientError("--country-code applies to the bookmakers catalog.")
        result = OddsClient().get("/" + args.kind, sport=args.sport, country_code=args.country_code)
    elif args.command == "events":
        start, end = utc_seconds(args.from_ts), utc_seconds(args.to_ts)
        if not 0 < end - start <= 7 * 86400:
            raise ClientError("Use an increasing UTC event window of seven days or less.")
        pages = OddsClient().pages("/events", sport=args.sport, league=args.league, start_from=int(start), start_to=int(end), limit=200)
        unique = {}
        for page in pages:
            for event in page["items"]:
                if not isinstance(event, dict) or not event.get("event_id"):
                    raise ClientError("Event response is missing its canonical ID.")
                if args.team and not any(args.team.lower() in str(event.get(key) or "").lower() for key in ("home_team", "away_team")):
                    continue
                unique[event["event_id"]] = event
        result = {"items": list(unique.values()), "complete": True, "pages": len(pages)}
    else:
        result = OddsClient().snapshot(args.event_id, bookmakers=args.bookmakers, types=args.types, periods=args.periods)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except ClientError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
    except Exception:
        print("The starter could not complete the request. Check input and public documentation.", file=sys.stderr)
        sys.exit(1)
