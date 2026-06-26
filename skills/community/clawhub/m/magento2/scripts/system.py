#!/usr/bin/env python3
"""System management — health checks and cache management."""

import os
import sys
import argparse
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from magento_client import get_client, list_configured_sites, MagentoAPIError, print_error_and_exit

try:
    from tabulate import tabulate
except ImportError:
    sys.exit("Missing dependency: uv pip install tabulate")


def cmd_status(args):
    client = get_client(args.site)
    try:
        # Check basic connection by fetching store info
        store_info = client.get("store/storeConfigs")
        print("API Connection: OK")
        if store_info:
            print(f"Store Count: {len(store_info)}")
            print(f"Base URL: {store_info[0].get('base_url')}")
    except MagentoAPIError as e:
        print(f"API Connection: FAILED ({e.status})")
        print_error_and_exit(e)


def cmd_modules(args):
    client = get_client(args.site)
    try:
        modules = client.get("modules")
        print(f"Total Modules: {len(modules)}")
        # If too many, just list the first 50 or those that look custom
        custom = [m for m in modules if not m.startswith("Magento_")]
        if custom:
            print("\nCustom/Third-party Modules:")
            for m in custom:
                print(f"- {m}")
        
        print("\nAll modules (first 20):")
        for m in modules[:20]:
            print(f"- {m}")
    except MagentoAPIError as e:
        print_error_and_exit(e)


def cmd_schema(args):
    client = get_client(args.site)
    try:
        # Fetch the schema. This can be VERY large, so we just want to see if it works
        # and maybe list some top-level paths.
        schema = client.get("/rest/all/schema?services=all")
        print("API Schema available.")
        paths = list(schema.get("paths", {}).keys())
        print(f"Total API Paths: {len(paths)}")
        
        # Look for custom paths (not Magento standard)
        custom_paths = [p for p in paths if not p.startswith("/V1/")]
        if custom_paths:
            print("\nCustom API Paths detected:")
            for p in custom_paths[:20]:
                 print(f"- {p}")
        
        print("\nStandard API Paths (V1, first 10):")
        v1_paths = [p for p in paths if p.startswith("/V1/")]
        for p in v1_paths[:10]:
            print(f"- {p}")
            
    except MagentoAPIError as e:
        # Schema might be protected or too large
        print(f"Could not fetch full schema: {e}")
        print("Try exploring modules instead.")


def cmd_cache_list(args):
    client = get_client(args.site)
    try:
        caches = client.get("cache")
    except MagentoAPIError as e:
        print_error_and_exit(e)

    rows = [[c.get("id"), c.get("status"), c.get("label")] for c in caches]
    print(tabulate(rows, headers=["ID", "Status", "Label"], tablefmt="github"))


def cmd_cache_flush(args):
    client = get_client(args.site)
    # If no types specified, flush all
    try:
        if not args.types:
            # Fetch all types first
            caches = client.get("cache")
            types = [c.get("id") for c in caches]
        else:
            types = [t.strip() for t in args.types.split(",")]

        # Magento expects IDs in the request
        for cache_type in types:
            client.post("cache/clear", {"ids": [cache_type]})
            print(f"Cache '{cache_type}' cleared.")
        
        print("\nAll specified caches have been cleared.")
    except MagentoAPIError as e:
        print_error_and_exit(e)


def cmd_sites(args):
    sites, has_default = list_configured_sites()
    if not has_default and not sites:
        print("No sites configured. Set MAGENTO_BASE_URL or MAGENTO_BASE_URL_<SITE>.")
        return
    rows = []
    if has_default:
        rows.append(["(default)", os.environ.get("MAGENTO_BASE_URL", "")])
    for site in sites:
        rows.append([site, os.environ.get(f"MAGENTO_BASE_URL_{site.upper()}", "")])
    print(tabulate(rows, headers=["Site", "Base URL"], tablefmt="github"))


def main():
    parser = argparse.ArgumentParser(description="Magento 2 system management")
    parser.add_argument("--site", default=None, help="Site alias (e.g. us, eu)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Check API connection status")
    sub.add_parser("modules", help="List all installed Magento modules")
    sub.add_parser("schema", help="Show REST API schema (summary)")
    sub.add_parser("cache-list", help="List cache types and statuses")
    sub.add_parser("sites", help="List all configured Magento sites")

    p_flush = sub.add_parser("cache-flush", help="Flush specific or all caches")
    p_flush.add_argument("--types", help="Comma-separated list of cache IDs to flush (default: all)")

    args = parser.parse_args()
    commands = {
        "status": cmd_status,
        "modules": cmd_modules,
        "schema": cmd_schema,
        "cache-list": cmd_cache_list,
        "cache-flush": cmd_cache_flush,
        "sites": cmd_sites,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()