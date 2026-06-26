#!/usr/bin/env python3
"""
OpenClaw-friendly wrapper: shells out to ga_query.py with normalized flags.
"""

import subprocess
import sys
import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GA_QUERY_SCRIPT = os.path.join(SCRIPT_DIR, "ga_query.py")


def run_ga_query(action: str, **kwargs) -> str:
    """
    Run GA CLI and return stdout text.

    Args:
        action: realtime | historical | metadata
        **kwargs: forwarded as --kebab-case flags
    """
    cmd = [sys.executable, GA_QUERY_SCRIPT, "--action", action]

    credentials = kwargs.get("credentials")
    if credentials:
        cmd.extend(["--credentials", credentials])
    else:
        default_creds = os.path.join(SCRIPT_DIR, "ga-credentials.json")
        if os.path.exists(default_creds):
            cmd.extend(["--credentials", default_creds])

    property_id = kwargs.get("property_id")
    if property_id:
        cmd.extend(["--property-id", str(property_id)])

    for key, value in kwargs.items():
        if key in ["credentials", "property_id"]:
            continue
        if value is not None:
            key_formatted = f"--{key.replace('_', '-')}"
            if isinstance(value, bool):
                if value:
                    cmd.append(key_formatted)
            elif isinstance(value, list):
                cmd.extend([key_formatted, ",".join(map(str, value))])
            else:
                cmd.extend([key_formatted, str(value)])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=SCRIPT_DIR,
            timeout=60,
        )

        if result.returncode != 0:
            return f"❌ Query failed: {result.stderr}"

        return result.stdout

    except subprocess.TimeoutExpired:
        return "❌ Timeout (> 60s)"
    except Exception as e:
        return f"❌ Error: {e}"


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw helper for ga_query.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python openclaw_ga.py realtime --property-id 123456789

  python openclaw_ga.py historical \\
    --property-id 123456789 \\
    --start-date 7daysAgo \\
    --end-date yesterday \\
    --metrics activeUsers,sessions \\
    --dimensions country
        """,
    )

    subparsers = parser.add_subparsers(dest="action", help="Action")

    realtime_parser = subparsers.add_parser("realtime", help="Realtime report")
    realtime_parser.add_argument("--property-id", required=True, help="GA4 property ID")
    realtime_parser.add_argument("--metrics", default="activeUsers", help="Metrics list")
    realtime_parser.add_argument("--dimensions", help="Dimensions list")
    realtime_parser.add_argument("--minute-range", default="0-30", help="Minutes ago window")
    realtime_parser.add_argument("--credentials", help="Service account JSON path")

    historical_parser = subparsers.add_parser("historical", help="Historical report")
    historical_parser.add_argument("--property-id", required=True, help="GA4 property ID")
    historical_parser.add_argument("--start-date", required=True, help="Start date")
    historical_parser.add_argument("--end-date", required=True, help="End date")
    historical_parser.add_argument("--metrics", default="activeUsers", help="Metrics list")
    historical_parser.add_argument("--dimensions", help="Dimensions list")
    historical_parser.add_argument("--limit", type=int, default=10000, help="Row limit")
    historical_parser.add_argument("--credentials", help="Service account JSON path")

    metadata_parser = subparsers.add_parser("metadata", help="Metadata listing")
    metadata_parser.add_argument("--property-id", required=True, help="GA4 property ID")
    metadata_parser.add_argument("--credentials", help="Service account JSON path")

    args = parser.parse_args()

    if not args.action:
        parser.print_help()
        sys.exit(1)

    kwargs = vars(args)
    action = kwargs.pop("action")

    result = run_ga_query(action, **kwargs)
    print(result)


if __name__ == "__main__":
    main()
