#!/usr/bin/env python3
"""Google Sheets API — read spreadsheet data via domain-wide delegation."""

import argparse
import json
import sys
from typing import Optional

from auth import get_service


def get_values(
    user: str,
    spreadsheet_id: str,
    range: str,
) -> dict:
    """Get values from a spreadsheet range.

    Args:
        user: Email address (impersonated via DWD).
        spreadsheet_id: Spreadsheet ID.
        range: A1 notation range (e.g. 'Sheet1!A1:D10').

    Returns:
        Dict with values.
    """
    service = get_service("sheets", impersonate=user)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range,
    ).execute()

    values = result.get("values", [])
    return {
        "spreadsheet_id": spreadsheet_id,
        "range": result.get("range", range),
        "rows": len(values),
        "values": values,
    }


def get_metadata(
    user: str,
    spreadsheet_id: str,
) -> dict:
    """Get spreadsheet metadata (title, sheets/tabs, etc).

    Args:
        user: Email address.
        spreadsheet_id: Spreadsheet ID.

    Returns:
        Dict with spreadsheet metadata.
    """
    service = get_service("sheets", impersonate=user)
    result = service.spreadsheets().get(
        spreadsheetId=spreadsheet_id,
        fields="spreadsheetId,properties.title,sheets.properties",
    ).execute()

    sheets = result.get("sheets", [])
    return {
        "spreadsheet_id": result.get("spreadsheetId", ""),
        "title": result.get("properties", {}).get("title", ""),
        "sheets": [
            {
                "id": s.get("properties", {}).get("sheetId", ""),
                "title": s.get("properties", {}).get("title", ""),
                "index": s.get("properties", {}).get("index", 0),
                "row_count": s.get("properties", {}).get("gridProperties", {}).get("rowCount", 0),
                "column_count": s.get("properties", {}).get("gridProperties", {}).get("columnCount", 0),
            }
            for s in sheets
        ],
    }


def batch_get(
    user: str,
    spreadsheet_id: str,
    ranges: list[str],
) -> dict:
    """Get values from multiple ranges at once.

    Args:
        user: Email address.
        spreadsheet_id: Spreadsheet ID.
        ranges: List of A1 notation ranges.

    Returns:
        Dict with values for each range.
    """
    service = get_service("sheets", impersonate=user)
    result = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id,
        ranges=ranges,
    ).execute()

    value_ranges = result.get("valueRanges", [])
    return {
        "spreadsheet_id": spreadsheet_id,
        "ranges": [
            {
                "range": vr.get("range", ""),
                "rows": len(vr.get("values", [])),
                "values": vr.get("values", []),
            }
            for vr in value_ranges
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Google Sheets read")
    sub = parser.add_subparsers(dest="command", required=True)

    # get
    p_get = sub.add_parser("get", help="Get values from a range")
    p_get.add_argument("--user", required=True)
    p_get.add_argument("--id", required=True, help="Spreadsheet ID")
    p_get.add_argument("--range", required=True, help="A1 notation range")

    # metadata
    p_meta = sub.add_parser("metadata", help="Get spreadsheet metadata")
    p_meta.add_argument("--user", required=True)
    p_meta.add_argument("--id", required=True, help="Spreadsheet ID")

    # batch
    p_batch = sub.add_parser("batch", help="Get values from multiple ranges")
    p_batch.add_argument("--user", required=True)
    p_batch.add_argument("--id", required=True, help="Spreadsheet ID")
    p_batch.add_argument("--ranges", nargs="+", required=True, help="A1 notation ranges")

    args = parser.parse_args()

    try:
        if args.command == "get":
            result = get_values(args.user, args.id, args.range)
        elif args.command == "metadata":
            result = get_metadata(args.user, args.id)
        elif args.command == "batch":
            result = batch_get(args.user, args.id, args.ranges)
        else:
            result = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
