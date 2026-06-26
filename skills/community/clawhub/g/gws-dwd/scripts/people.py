#!/usr/bin/env python3
"""Google People API — contacts and org directory via domain-wide delegation."""

import argparse
import json
import sys
from typing import Optional

from auth import get_service


def list_contacts(
    user: str,
    max_results: int = 50,
) -> dict:
    """List a user's contacts.

    Args:
        user: Email address (impersonated via DWD).
        max_results: Max contacts to return.

    Returns:
        Dict with contact list.
    """
    service = get_service("people", impersonate=user)
    results = service.people().connections().list(
        resourceName="people/me",
        pageSize=max_results,
        personFields="names,emailAddresses,phoneNumbers,organizations",
    ).execute()

    connections = results.get("connections", [])
    return {
        "user": user,
        "total": len(connections),
        "contacts": [_parse_person(p) for p in connections],
    }


def search_contacts(
    user: str,
    query: str,
    max_results: int = 10,
) -> dict:
    """Search a user's contacts.

    Args:
        user: Email address.
        query: Search query (name, email, phone).
        max_results: Max results.

    Returns:
        Dict with matching contacts.
    """
    service = get_service("people", impersonate=user)
    results = service.people().searchContacts(
        query=query,
        pageSize=max_results,
        readMask="names,emailAddresses,phoneNumbers,organizations",
    ).execute()

    people = results.get("results", [])
    return {
        "user": user,
        "query": query,
        "total": len(people),
        "contacts": [_parse_person(p.get("person", {})) for p in people],
    }


def search_directory(
    user: str,
    query: str,
    max_results: int = 10,
) -> dict:
    """Search the organization's directory.

    Args:
        user: Email address.
        query: Search query.
        max_results: Max results.

    Returns:
        Dict with matching directory entries.
    """
    service = get_service("people", impersonate=user)
    results = service.people().searchDirectoryPeople(
        query=query,
        readMask="names,emailAddresses,phoneNumbers,organizations",
        sources=["DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE"],
        pageSize=max_results,
    ).execute()

    people = results.get("people", [])
    return {
        "user": user,
        "query": query,
        "total": len(people),
        "directory_entries": [_parse_person(p) for p in people],
    }


def _parse_person(person: dict) -> dict:
    """Parse a People API person into a clean dict."""
    names = person.get("names", [])
    emails = person.get("emailAddresses", [])
    phones = person.get("phoneNumbers", [])
    orgs = person.get("organizations", [])

    return {
        "name": names[0].get("displayName", "") if names else "",
        "emails": [e.get("value", "") for e in emails],
        "phones": [p.get("value", "") for p in phones],
        "organization": orgs[0].get("name", "") if orgs else "",
        "title": orgs[0].get("title", "") if orgs else "",
    }


def main():
    parser = argparse.ArgumentParser(description="Google People API — contacts and directory")
    sub = parser.add_subparsers(dest="command", required=True)

    # contacts
    p_contacts = sub.add_parser("contacts", help="List contacts")
    p_contacts.add_argument("--user", required=True)
    p_contacts.add_argument("--max", type=int, default=50)

    # search
    p_search = sub.add_parser("search", help="Search contacts")
    p_search.add_argument("--user", required=True)
    p_search.add_argument("--query", required=True)
    p_search.add_argument("--max", type=int, default=10)

    # directory
    p_dir = sub.add_parser("directory", help="Search org directory")
    p_dir.add_argument("--user", required=True)
    p_dir.add_argument("--query", required=True)
    p_dir.add_argument("--max", type=int, default=10)

    args = parser.parse_args()

    try:
        if args.command == "contacts":
            result = list_contacts(args.user, args.max)
        elif args.command == "search":
            result = search_contacts(args.user, args.query, args.max)
        elif args.command == "directory":
            result = search_directory(args.user, args.query, args.max)
        else:
            result = {"error": f"Unknown command: {args.command}"}

        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
