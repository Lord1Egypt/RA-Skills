#!/usr/bin/env python3
"""
mock_data.py - Generate realistic fake/mock data for testing and development.

Usage:
    python3 mock_data.py <type> [--count N] [--format json|csv|sql|lines] [options]
"""

import argparse
import csv
import io
import json
import random
import string
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# ─── Data pools ──────────────────────────────────────────────────────────────

FIRST_NAMES = [
    "James", "Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia",
    "Benjamin", "Isabella", "Lucas", "Mia", "Henry", "Charlotte", "Alexander",
    "Amelia", "Mason", "Harper", "Ethan", "Evelyn", "Daniel", "Abigail",
    "Matthew", "Emily", "Aiden", "Elizabeth", "Logan", "Mila", "Jackson",
    "Ella", "Sebastian", "Chloe", "Jack", "Victoria", "Owen", "Riley",
    "Elijah", "Aria", "Gabriel", "Lily", "Carter", "Grace", "Jayden", "Zoey",
    "Julian", "Nora", "Wyatt", "Penelope", "Samuel", "Layla", "David",
    "Scarlett", "Joseph", "Eleanor", "John", "Hannah", "Caleb", "Lillian",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Reed", "Chen", "Kim", "Park", "Patel", "Singh",
]

DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "fastmail.com", "protonmail.com",
    "icloud.com", "fakecorp.io", "testmail.dev", "example.net", "devteam.co",
    "techworks.io", "mailbox.org", "inbox.test", "startup.tech",
]

STREET_TYPES = ["Ave", "St", "Blvd", "Dr", "Ln", "Rd", "Way", "Ct", "Pl"]
STREET_NAMES = [
    "Oak", "Maple", "Cedar", "Pine", "Elm", "Washington", "Park", "Lake",
    "Hill", "Main", "Sunset", "Highland", "Meadow", "River", "Forest",
    "Valley", "Spring", "Willow", "Birch", "Canyon", "Harbor", "Horizon",
]
CITIES = [
    "Austin", "Denver", "Seattle", "Portland", "Nashville", "Chicago",
    "Phoenix", "Dallas", "San Jose", "Boston", "Atlanta", "Miami",
    "Minneapolis", "Detroit", "San Diego", "Baltimore", "Columbus", "Memphis",
    "Louisville", "Tucson", "Fresno", "Sacramento", "Raleigh", "Salt Lake City",
]
STATES = ["TX", "CO", "WA", "OR", "TN", "IL", "AZ", "CA", "MA", "GA",
          "FL", "MN", "MI", "NC", "UT", "NY", "OH", "VA", "PA", "NV"]

COMPANY_PREFIXES = [
    "Nexigen", "Apex", "Vertex", "Horizon", "Synapse", "Quantum", "Orbit",
    "Fusion", "Meridian", "Zenith", "Catalyst", "Nova", "Vector", "Lumina",
    "Cortex", "Forge", "Prism", "Helix", "Titan", "Echo", "Peak", "Summit",
]
COMPANY_SUFFIXES = [
    "Solutions", "Technologies", "Systems", "Group", "Partners", "Labs",
    "Ventures", "Consulting", "Innovations", "Digital", "Networks", "Global",
    "Works", "Dynamics", "Studio", "Media", "Cloud", "Data", "AI",
]
COMPANY_TYPES = ["LLC", "Inc", "Corp", "Co", "Ltd", ""]

LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam "
    "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo "
    "consequat duis aute irure dolor in reprehenderit in voluptate velit esse "
    "cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat "
    "non proident sunt in culpa qui officia deserunt mollit anim id est laborum"
).split()

URL_PATHS = ["/", "/api/v1", "/api/v2", "/dashboard", "/users", "/settings",
             "/products", "/orders", "/about", "/contact", "/docs", "/health"]

# ─── Generators ──────────────────────────────────────────────────────────────

def gen_name(rng):
    return f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"


def gen_email(rng, name=None):
    if name is None:
        name = gen_name(rng)
    first, last = name.lower().split()[:2]
    sep = rng.choice([".", "_", ""])
    num = rng.choice(["", str(rng.randint(1, 99))])
    domain = rng.choice(DOMAINS)
    return f"{first}{sep}{last}{num}@{domain}"


def gen_phone(rng):
    area = rng.randint(200, 999)
    prefix = rng.randint(200, 999)
    line = rng.randint(1000, 9999)
    return f"({area}) {prefix}-{line}"


def gen_address(rng):
    num = rng.randint(100, 9999)
    street = f"{rng.choice(STREET_NAMES)} {rng.choice(STREET_TYPES)}"
    city = rng.choice(CITIES)
    state = rng.choice(STATES)
    zip_code = rng.randint(10000, 99999)
    return f"{num} {street}, {city} {state} {zip_code}"


def gen_company(rng):
    prefix = rng.choice(COMPANY_PREFIXES)
    suffix = rng.choice(COMPANY_SUFFIXES)
    ctype = rng.choice(COMPANY_TYPES)
    name = f"{prefix} {suffix}"
    if ctype:
        name += f" {ctype}"
    return name


def gen_uuid(_rng):
    return str(uuid.uuid4())


def gen_date(rng):
    start = datetime(2000, 1, 1)
    end = datetime(2026, 12, 31)
    delta = end - start
    rand_days = rng.randint(0, delta.days)
    return (start + timedelta(days=rand_days)).strftime("%Y-%m-%d")


def gen_datetime(rng):
    start = datetime(2000, 1, 1)
    end = datetime(2026, 12, 31)
    delta = end - start
    rand_secs = rng.randint(0, int(delta.total_seconds()))
    return (start + timedelta(seconds=rand_secs)).strftime("%Y-%m-%dT%H:%M:%S")


def gen_lorem(rng, words=20):
    w = [rng.choice(LOREM_WORDS) for _ in range(words)]
    text = " ".join(w)
    return text[0].upper() + text[1:] + "."


def gen_number(rng):
    return rng.randint(1, 10000)


def gen_float(rng):
    return round(rng.uniform(0.0, 1000.0), 4)


def gen_bool(rng):
    return rng.choice([True, False])


def gen_color(rng):
    return "#{:06x}".format(rng.randint(0, 0xFFFFFF))


def gen_url(rng):
    domain_name = rng.choice(COMPANY_PREFIXES).lower()
    tld = rng.choice(["io", "com", "co", "tech", "ai", "dev"])
    path = rng.choice(URL_PATHS)
    return f"https://{domain_name}.{tld}{path}"


def gen_ip(rng):
    return ".".join(str(rng.randint(1, 254)) for _ in range(4))


def gen_user(rng):
    name = gen_name(rng)
    email = gen_email(rng, name=name)
    return {
        "id": gen_uuid(rng),
        "name": name,
        "email": email,
        "phone": gen_phone(rng),
        "company": gen_company(rng),
        "address": gen_address(rng),
        "created_at": gen_date(rng),
        "active": gen_bool(rng),
    }


FIELD_GENERATORS = {
    "name": gen_name,
    "email": gen_email,
    "phone": gen_phone,
    "address": gen_address,
    "company": gen_company,
    "uuid": gen_uuid,
    "date": gen_date,
    "datetime": gen_datetime,
    "lorem": gen_lorem,
    "number": gen_number,
    "float": gen_float,
    "bool": gen_bool,
    "color": gen_color,
    "url": gen_url,
    "ip": gen_ip,
}

TYPE_GENERATORS = {
    **FIELD_GENERATORS,
    "user": gen_user,
}


def gen_record(rng, fields):
    """Generate a record with specified fields."""
    record = {}
    for field in fields:
        field = field.strip()
        if field in FIELD_GENERATORS:
            record[field] = FIELD_GENERATORS[field](rng)
        else:
            record[field] = f"<unknown:{field}>"
    return record


# ─── Output formatters ───────────────────────────────────────────────────────

def format_json(records):
    if len(records) == 1:
        return json.dumps(records[0], indent=2, default=str) + "\n"
    return json.dumps(records, indent=2, default=str) + "\n"


def format_csv(records):
    if not records:
        return ""
    out = io.StringIO()
    if isinstance(records[0], dict):
        fields = list(records[0].keys())
        writer = csv.DictWriter(out, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    else:
        writer = csv.writer(out)
        for r in records:
            writer.writerow([r])
    return out.getvalue()


def format_sql(records, table):
    if not records:
        return ""
    lines = []
    if isinstance(records[0], dict):
        fields = list(records[0].keys())
        cols = ", ".join(fields)
        for rec in records:
            def sql_val(v):
                if v is None:
                    return "NULL"
                if isinstance(v, bool):
                    return "TRUE" if v else "FALSE"
                if isinstance(v, (int, float)):
                    return str(v)
                return "'" + str(v).replace("'", "''") + "'"
            vals = ", ".join(sql_val(rec[f]) for f in fields)
            lines.append(f"INSERT INTO {table} ({cols}) VALUES ({vals});")
    else:
        for r in records:
            val = "'" + str(r).replace("'", "''") + "'"
            lines.append(f"INSERT INTO {table} (value) VALUES ({val});")
    return "\n".join(lines) + "\n"


def format_lines(records):
    lines = []
    for r in records:
        if isinstance(r, dict):
            lines.append(json.dumps(r, default=str))
        else:
            lines.append(str(r))
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(
        description="Generate realistic fake/mock data for testing and development.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Data types: user, name, email, phone, address, company, uuid, date,
            datetime, lorem, number, float, bool, color, url, ip, record

Examples:
  python3 mock_data.py user --count 10
  python3 mock_data.py email --count 5
  python3 mock_data.py record --fields "name,email,phone,company" --count 5
  python3 mock_data.py user --count 20 --format csv
  python3 mock_data.py user --count 10 --format sql --table users
  python3 mock_data.py lorem --words 50
        """
    )
    parser.add_argument(
        "type",
        choices=list(TYPE_GENERATORS.keys()) + ["record"],
        help="Type of data to generate"
    )
    parser.add_argument("--count", "-n", type=int, default=1,
                        help="Number of records (default: 1)")
    parser.add_argument("--format", "-f",
                        choices=["json", "csv", "sql", "lines"],
                        default="json",
                        help="Output format (default: json)")
    parser.add_argument("--table", default="records",
                        help="Table name for SQL output (default: records)")
    parser.add_argument("--fields",
                        help="Comma-separated fields for 'record' type")
    parser.add_argument("--seed", type=int,
                        help="Random seed for reproducible output")
    parser.add_argument("--words", type=int, default=20,
                        help="Word count for lorem type (default: 20)")
    parser.add_argument("--output", "-o",
                        help="Write output to file instead of stdout")

    args = parser.parse_args()

    rng = random.Random(args.seed)

    # Generate records
    records = []
    for _ in range(args.count):
        dtype = args.type
        if dtype == "record":
            if not args.fields:
                print("[ERROR] --fields is required for 'record' type", file=sys.stderr)
                sys.exit(2)
            fields = args.fields.split(",")
            records.append(gen_record(rng, fields))
        elif dtype == "lorem":
            records.append(gen_lorem(rng, words=args.words))
        elif dtype in TYPE_GENERATORS:
            records.append(TYPE_GENERATORS[dtype](rng))

    # Format output
    if args.format == "json":
        output = format_json(records)
    elif args.format == "csv":
        output = format_csv(records)
    elif args.format == "sql":
        output = format_sql(records, args.table)
    elif args.format == "lines":
        output = format_lines(records)

    # Write output
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"[OK] Written {args.count} record(s) to {args.output}")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
