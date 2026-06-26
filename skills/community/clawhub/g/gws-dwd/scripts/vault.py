#!/usr/bin/env python3
"""Google Vault API — search email content org-wide via eDiscovery."""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from typing import Optional

from auth import get_service


def create_matter(service, name: str = "Jarvis Investigation") -> dict:
    """Create a new Vault matter for investigation."""
    body = {"name": name, "state": "OPEN"}
    matter = service.matters().create(body=body).execute()
    return matter


def close_matter(service, matter_id: str) -> None:
    """Close a matter (required before deletion)."""
    service.matters().close(matterId=matter_id, body={}).execute()


def delete_matter(service, matter_id: str) -> None:
    """Delete a matter. Must be closed first."""
    service.matters().delete(matterId=matter_id).execute()


def count_results(
    service,
    matter_id: str,
    accounts: list[str],
    terms: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> dict:
    """Count matching messages without exporting.

    Args:
        service: Vault API service.
        matter_id: Matter to run query in.
        accounts: List of email addresses to search.
        terms: Gmail search operators (from:, to:, subject:, etc).
        start_time: ISO 8601 start time (optional).
        end_time: ISO 8601 end time (optional).

    Returns:
        Dict with total_count and per-account breakdown.
    """
    query = {
        "corpus": "MAIL",
        "dataScope": "ALL_DATA",
        "searchMethod": "ACCOUNT",
        "accountInfo": {"emails": accounts},
        "terms": terms,
        "mailOptions": {"excludeDrafts": True},
    }
    if start_time:
        query["startTime"] = start_time
    if end_time:
        query["endTime"] = end_time

    request = {"query": query}
    operation = service.matters().count(matterId=matter_id, body=request).execute()

    # Poll until complete
    while True:
        op = service.operations().get(name=operation["name"]).execute()
        if op.get("done"):
            break
        time.sleep(2)

    if "error" in op:
        return {"error": op["error"]}

    response = op.get("response", {})
    total = int(response.get("totalCount", 0))
    mail_count = response.get("mailCountResult", {})
    queried = int(mail_count.get("queriedAccountsCount", 0))
    matching = int(mail_count.get("matchingAccountsCount", 0))

    # Account-level breakdown (if present — depends on query type)
    account_counts = mail_count.get("accountCountErrors", [])
    non_queryable = mail_count.get("nonQueryableAccounts", [])

    result = {
        "total_count": total,
        "queried_accounts": queried,
        "matching_accounts": matching,
        "accounts_searched": accounts,
    }
    if account_counts:
        result["account_errors"] = account_counts
    if non_queryable:
        result["non_queryable_accounts"] = non_queryable

    return result


def search_and_export(
    service,
    matter_id: str,
    accounts: list[str],
    terms: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    export_name: str = "gws-skill-export",
) -> dict:
    """Create an export of matching messages.

    Args:
        service: Vault API service.
        matter_id: Matter to run query in.
        accounts: List of email addresses to search.
        terms: Gmail search operators.
        start_time: ISO 8601 start time (optional).
        end_time: ISO 8601 end time (optional).
        export_name: Name for the export.

    Returns:
        Export metadata including download info.
    """
    query = {
        "corpus": "MAIL",
        "dataScope": "ALL_DATA",
        "searchMethod": "ACCOUNT",
        "accountInfo": {"emails": accounts},
        "terms": terms,
        "mailOptions": {"excludeDrafts": True},
    }
    if start_time:
        query["startTime"] = start_time
    if end_time:
        query["endTime"] = end_time

    export_body = {
        "name": export_name,
        "query": query,
        "exportOptions": {
            "mailOptions": {
                "exportFormat": "MBOX",
                "showConfidentialModeContent": False,
            },
        },
    }

    export = service.matters().exports().create(
        matterId=matter_id, body=export_body
    ).execute()

    export_id = export["id"]

    # Poll until export is complete
    while True:
        exp = service.matters().exports().get(
            matterId=matter_id, exportId=export_id
        ).execute()
        status = exp.get("status", "")
        if status == "COMPLETED":
            return exp
        elif status == "FAILED":
            return {"error": "Export failed", "details": exp}
        time.sleep(5)


def search_org_unit(
    service,
    matter_id: str,
    org_unit_id: str,
    terms: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
) -> dict:
    """Count matching messages across an entire org unit.

    Args:
        service: Vault API service.
        matter_id: Matter to run query in.
        org_unit_id: Google org unit ID to search.
        terms: Gmail search operators.
        start_time: ISO 8601 start time (optional).
        end_time: ISO 8601 end time (optional).

    Returns:
        Count results dict.
    """
    query = {
        "corpus": "MAIL",
        "dataScope": "ALL_DATA",
        "searchMethod": "ORG_UNIT",
        "orgUnitInfo": {"orgUnitId": org_unit_id},
        "terms": terms,
        "mailOptions": {"excludeDrafts": True},
    }
    if start_time:
        query["startTime"] = start_time
    if end_time:
        query["endTime"] = end_time

    request = {"query": query}
    operation = service.matters().count(matterId=matter_id, body=request).execute()

    while True:
        op = service.operations().get(name=operation["name"]).execute()
        if op.get("done"):
            break
        time.sleep(2)

    if "error" in op:
        return {"error": op["error"]}

    response = op.get("response", {})
    total = int(response.get("totalCount", 0))
    mail_count = response.get("mailCountResult", {})
    queried = int(mail_count.get("queriedAccountsCount", 0))
    matching = int(mail_count.get("matchingAccountsCount", 0))

    result = {
        "total_count": total,
        "queried_accounts": queried,
        "matching_accounts": matching,
        "org_unit_id": org_unit_id,
    }

    return result


def run_investigation(
    accounts: list[str],
    terms: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    org_unit_id: Optional[str] = None,
    export: bool = False,
) -> dict:
    """Full investigation flow: create matter → query → cleanup.

    Args:
        accounts: List of email addresses to search (ignored if org_unit_id set).
        terms: Gmail search operators.
        start_time: ISO 8601 start time (optional).
        end_time: ISO 8601 end time (optional).
        org_unit_id: Search entire OU instead of specific accounts.
        export: If True, export full content. If False, just count.

    Returns:
        Investigation results.
    """
    service = get_service("vault")
    matter = None

    try:
        # Create matter
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        matter = create_matter(service, f"gws-{ts}")
        matter_id = matter["matterId"]

        if org_unit_id:
            result = search_org_unit(service, matter_id, org_unit_id, terms, start_time, end_time)
        elif export:
            result = search_and_export(service, matter_id, accounts, terms, start_time, end_time)
        else:
            result = count_results(service, matter_id, accounts, terms, start_time, end_time)

        result["matter_id"] = matter_id
        result["query"] = {"accounts": accounts, "terms": terms, "start_time": start_time, "end_time": end_time}
        return result

    finally:
        # Always cleanup: close then delete
        if matter:
            try:
                close_matter(service, matter["matterId"])
                delete_matter(service, matter["matterId"])
            except Exception:
                pass  # Best effort cleanup


def main():
    parser = argparse.ArgumentParser(description="Google Vault email search")
    parser.add_argument("--accounts", nargs="+", help="Email addresses to search")
    parser.add_argument("--terms", required=True, help="Gmail search operators (from:, to:, subject:, etc)")
    parser.add_argument("--start", help="Start time (ISO 8601)")
    parser.add_argument("--end", help="End time (ISO 8601)")
    parser.add_argument("--org-unit", help="Org unit ID (search entire OU)")
    parser.add_argument("--export", action="store_true", help="Export full content (not just count)")
    args = parser.parse_args()

    if not args.accounts and not args.org_unit:
        print(json.dumps({"error": "Must specify --accounts or --org-unit"}))
        sys.exit(1)

    try:
        result = run_investigation(
            accounts=args.accounts or [],
            terms=args.terms,
            start_time=args.start,
            end_time=args.end,
            org_unit_id=args.org_unit,
            export=args.export,
        )
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
