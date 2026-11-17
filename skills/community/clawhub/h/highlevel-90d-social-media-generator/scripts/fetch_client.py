#!/usr/bin/env python3
"""Get client details for the social pipeline.

TWO MODES:
  HL mode (needs HIGHLEVEL_ACCESS_TOKEN):
    python3 fetch_client.py --email client@x.com [--location-id LOC] [--json-out f.json]

  No-HL mode (no token needed, details given directly):
    python3 fetch_client.py --client-json file.json            # re-use/normalize an existing client file
    python3 fetch_client.py --details "Name|website.com|City|ST|Business Category|Company description"

Both modes write the SAME normalized client JSON, so the rest of the pipeline
(generate_posts, generate_images) never cares where the data came from.
"""
import argparse
import json
import sys

from common import load_env, hl, resolve_location, find_custom_field_map

CLIENT_KEYS = ["id", "firstName", "lastName", "email", "phone", "companyName",
               "website", "city", "state", "tags", "customFields"]


def normalize(c: dict) -> dict:
    out = {k: c.get(k) for k in CLIENT_KEYS}
    out["companyName"] = c.get("companyName") or c.get("businessName") or ""
    out["customFields"] = c.get("customFields") or {}
    return out


def from_hl(args, env):
    token = env.get("HIGHLEVEL_ACCESS_TOKEN", "")
    if not token:
        print("ERROR: HIGHLEVEL_ACCESS_TOKEN not set (HL mode). Use --client-json or --details to skip HL.", file=sys.stderr)
        sys.exit(2)
    loc = resolve_location(token, env)
    query = args.email or args.company
    if not query:
        print("ERROR: provide --email or --company for HL mode", file=sys.stderr)
        sys.exit(2)
    r = hl("POST", "/contacts/search", token, {"locationId": loc, "query": query, "page": 0, "pageLimit": 1})
    contacts = r.get("contacts", []) if isinstance(r, dict) else []
    if not contacts:
        print(f"NOT_FOUND\t{query}", file=sys.stderr)
        sys.exit(3)
    c = contacts[0]
    fmap = find_custom_field_map(token, loc)
    fields = {}
    for cf in c.get("customFields", []):
        if not isinstance(cf, dict):
            continue
        fid = cf.get("fieldId") or cf.get("id")
        name = fmap.get(fid, fid)
        val = cf.get("value")
        if name and val not in (None, ""):
            fields[name] = val
    c["customFields"] = fields
    addr = c.get("address") or {}
    if isinstance(addr, dict):
        c["city"] = addr.get("city") or c.get("city") or ""
        c["state"] = addr.get("state") or c.get("state") or ""
    return normalize(c)


def from_details(details: str) -> dict:
    """Parse a | separated details string:
    Company|website|City|ST|Business Category|Company description"""
    parts = [p.strip() for p in details.split("|")]
    if len(parts) < 5:
        print("ERROR: --details needs: Company|website|City|ST|Business Category|Company description", file=sys.stderr)
        sys.exit(2)
    company, website, city, state, category = parts[:5]
    desc = parts[5] if len(parts) > 5 else ""
    return normalize({
        "companyName": company,
        "website": website,
        "city": city,
        "state": state,
        "customFields": {
            "Business Category": category,
            "Company Description": desc,
        },
    })


def from_interactive() -> dict:
    """Ask for each client detail one question at a time (no HL connection)."""
    print("No HighLevel connection. Let's get the client details, one at a time.")
    company = input("1. Client company name: ").strip()
    website = input("2. Client website (e.g. example.com): ").strip()
    city = input("3. City: ").strip()
    state = input("4. State (e.g. FL): ").strip()
    category = input("5. Business Category (e.g. dentist): ").strip()
    desc = input("6. Company description (optional, Enter to skip): ").strip()
    if not company or not website or not city or not state or not category:
        print("ERROR: company, website, city, state, and category are required.", file=sys.stderr)
        sys.exit(2)
    return normalize({
        "companyName": company,
        "website": website,
        "city": city,
        "state": state,
        "customFields": {
            "Business Category": category,
            "Company Description": desc,
        },
    })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--email", default="")
    ap.add_argument("--company", default="")
    ap.add_argument("--location-id", default="")
    ap.add_argument("--client-json", default="", help="load/normalize existing client JSON (no HL needed)")
    ap.add_argument("--details", default="", help="Company|website|City|ST|Business Category|Description (no HL needed)")
    ap.add_argument("--interactive", action="store_true", help="ask for each detail one question at a time (no HL needed)")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    env = load_env()
    if args.location_id:
        env["HIGHLEVEL_LOCATION_ID"] = args.location_id

    if args.client_json:
        client = normalize(json.load(open(args.client_json)))
    elif args.details:
        client = from_details(args.details)
    elif args.interactive or not (args.email or args.company):
        client = from_interactive()
    else:
        client = from_hl(args, env)

    print(json.dumps(client, indent=2))
    if args.json_out:
        with open(args.json_out, "w") as f:
            json.dump(client, f, indent=2)
        print(f"# written to {args.json_out}", file=sys.stderr)


if __name__ == "__main__":
    main()
