#!/usr/bin/env python3
"""PromoStandards WebServiceRepository discovery.

Walks the public, unauthenticated endpoint registry and emits the full
company x service x version x URL matrix that provisioning consumes.

The registry is a .NET/WCF JSON service and its exact response shape is
NOT contractually documented, so every read here goes through tolerant
lookup helpers: keys are matched case-insensitively across PascalCase /
camelCase spellings, lists are unwrapped from whichever envelope the
service happens to use, and unknown keys are preserved verbatim in the
dump rather than dropped.

Run `--probe` FIRST against a new deployment: it prints the raw JSON for
a small sample so the field-name assumptions below can be corrected
before anything depends on them.

Usage:
    ps_registry.py probe                  # dump raw shapes, assume nothing
    ps_registry.py dump  [-o FILE]        # full registry -> JSON
    ps_registry.py summary [-i FILE]      # adoption counts from a dump

No credentials: this API is public. Nothing here reads secrets.
"""

from __future__ import annotations

import argparse
from concurrent import futures
import collections
import json
import sys
import time
import urllib.error
import urllib.request

BASE = (
    "https://services.promostandards.org/WebServiceRepository"
    "/WebServiceRepository.svc/json"
)

TIMEOUT = 30
RETRIES = 4
BACKOFF = 2.0
THROTTLE = 0.2  # polite delay between company calls


class RegistryError(RuntimeError):
    """Registry could not be read (network, HTTP, or malformed JSON)."""


# --------------------------------------------------------------------------
# transport
# --------------------------------------------------------------------------

def fetch_json(url: str) -> object:
    """GET `url` and parse JSON, retrying transient failures.

    Raises RegistryError with the blocked host called out, since an egress
    policy denial (403 on CONNECT) is the most common failure here and is
    not something a retry can fix.
    """
    last: Exception | None = None
    for attempt in range(RETRIES):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "promostandards-skill/registry-discovery",
                },
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw)
        except urllib.error.HTTPError as exc:
            # 4xx other than 429 will not resolve by retrying.
            if exc.code != 429 and 400 <= exc.code < 500:
                raise RegistryError(f"HTTP {exc.code} from {url}") from exc
            last = exc
        except json.JSONDecodeError as exc:
            raise RegistryError(f"non-JSON response from {url}") from exc
        except Exception as exc:  # noqa: BLE001 - urlopen raises broadly
            last = exc
        if attempt < RETRIES - 1:
            time.sleep(BACKOFF * (2**attempt))
    raise RegistryError(f"failed to fetch {url}: {last}")


# --------------------------------------------------------------------------
# tolerant shape handling
# --------------------------------------------------------------------------

def get(obj: object, *names: str, default: object = None) -> object:
    """Case-insensitive, spelling-tolerant key lookup on a dict.

    `get(d, "serviceCode", "code")` returns the first of those keys present
    under any capitalisation. Returns `default` when nothing matches, so
    callers never assume a field exists (optional means absent).
    """
    if not isinstance(obj, dict):
        return default
    lowered = {k.lower(): v for k, v in obj.items()}
    for name in names:
        if name.lower() in lowered:
            value = lowered[name.lower()]
            if value is not None:
                return value
    return default


def unwrap(payload: object, *hints: str) -> list:
    """Coerce a registry response into a list of records.

    Handles the shapes WCF services actually emit: a bare array, a `{"d":
    [...]}` ASP.NET wrapper, or a single-key object whose value is the
    array (e.g. `{"Services": [...]}`). Falls back to wrapping a lone
    object so callers always get a list.
    """
    if payload is None:
        return []
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for hint in (*hints, "d", "results", "items"):
            value = get(payload, hint)
            if isinstance(value, list):
                return value
        # single-key envelope: take the only list value present
        lists = [v for v in payload.values() if isinstance(v, list)]
        if len(lists) == 1:
            return lists[0]
        return [payload]
    return []


def service_code(record: object) -> str | None:
    """Best-effort service code ('INV', 'PROD', ...) from an endpoint record.

    The code may sit at the top level or nested under a Service/ServiceType
    object, per the documented `Service.ServiceType.Code` path.
    """
    direct = get(record, "serviceCode", "code", "serviceTypeCode", "type")
    if isinstance(direct, str) and direct.strip():
        return direct.strip().upper()
    for parent in ("service", "serviceType"):
        nested = get(record, parent)
        if isinstance(nested, dict):
            found = service_code(nested)
            if found:
                return found
    return None


def deep_get(record: object, *names: str) -> object:
    """Look a key up at the top level, then inside nested Service objects.

    The live registry nests Version/Status/WSDL under a `Service` object on
    endpoint records, while the `/services` listing puts them at the top
    level. Checking both keeps one parser correct for both shapes.
    """
    found = get(record, *names)
    if found is not None:
        return found
    for parent in ("service", "serviceType"):
        nested = get(record, parent)
        if isinstance(nested, dict):
            found = deep_get(nested, *names)
            if found is not None:
                return found
    return None


def endpoint_fields(record: dict) -> dict:
    """Normalise one endpoint record, preserving anything unrecognised."""
    known = {
        "service": service_code(record),
        "service_name": deep_get(record, "name", "serviceName"),
        "version": deep_get(record, "version", "serviceVersion", "wsVersion"),
        "url": deep_get(record, "url", "endpointUrl", "productionUrl", "uri"),
        "test_url": deep_get(record, "testUrl", "testURL", "testEndpointUrl"),
        "wsdl": deep_get(record, "wsdl", "wsdlUrl", "wsdlURL"),
        "status": deep_get(record, "status", "endpointStatus"),
    }
    consumed = {
        "servicecode", "code", "servicetypecode", "type", "service",
        "servicetype", "version", "serviceversion", "wsversion", "url",
        "endpointurl", "productionurl", "uri", "testurl", "testendpointurl",
        "wsdl", "wsdlurl", "status", "endpointstatus", "name", "servicename",
    }
    extra = {k: v for k, v in record.items() if k.lower() not in consumed}
    if extra:
        known["_extra"] = extra
    return known


def company_code(record: object) -> str | None:
    code = get(record, "companyCode", "code", "id", "companyId")
    if code is None:
        return None
    return str(code).strip() or None


# --------------------------------------------------------------------------
# commands
# --------------------------------------------------------------------------

def cmd_probe(_args: argparse.Namespace) -> int:
    """Dump raw shapes so field-name assumptions can be verified."""
    samples: list[tuple[str, str]] = [
        ("services", f"{BASE}/services"),
        ("companies", f"{BASE}/companies"),
    ]
    for label, url in samples:
        print(f"\n{'=' * 70}\n{label}: {url}\n{'=' * 70}")
        try:
            payload = fetch_json(url)
        except RegistryError as exc:
            print(f"FAILED: {exc}", file=sys.stderr)
            return 1
        text = json.dumps(payload, indent=2)
        print(text[:4000] + ("\n... [truncated]" if len(text) > 4000 else ""))
        records = unwrap(payload, label)
        print(f"\n-> {len(records)} record(s); "
              f"top-level type={type(payload).__name__}")
        if records and isinstance(records[0], dict):
            print(f"-> keys on first record: {sorted(records[0])}")

    # one company's endpoints, to pin the per-endpoint shape
    companies = unwrap(fetch_json(f"{BASE}/companies"), "companies")
    code = next(
        (company_code(c) for c in companies if company_code(c)), None
    )
    if code:
        url = f"{BASE}/companies/{code}/endpoints"
        print(f"\n{'=' * 70}\nendpoints for {code}: {url}\n{'=' * 70}")
        payload = fetch_json(url)
        text = json.dumps(payload, indent=2)
        print(text[:4000] + ("\n... [truncated]" if len(text) > 4000 else ""))
        records = unwrap(payload, "endpoints")
        if records and isinstance(records[0], dict):
            print(f"\n-> keys on first endpoint: {sorted(records[0])}")
            print(f"-> parsed: {json.dumps(endpoint_fields(records[0]))}")
    return 0


def cmd_dump(args: argparse.Namespace) -> int:
    """Walk every company and write the full endpoint matrix."""
    services = unwrap(fetch_json(f"{BASE}/services"), "services")
    companies = unwrap(fetch_json(f"{BASE}/companies"), "companies")
    print(f"registry: {len(services)} service(s), {len(companies)} company/ies",
          file=sys.stderr)

    out: dict[str, object] = {
        "source": BASE,
        "services": services,
        "companies": {},
        "errors": {},
    }
    seen_codes: set[str] = set()

    def one(company: dict) -> tuple[str | None, dict | None, str | None]:
        code = company_code(company)
        if not code:
            return None, None, None
        try:
            payload = fetch_json(f"{BASE}/companies/{code}/endpoints")
        except RegistryError as exc:
            # Degrade loudly: a dead company is recorded, not skipped.
            return code, None, str(exc)
        endpoints = [
            endpoint_fields(r)
            for r in unwrap(payload, "endpoints")
            if isinstance(r, dict)
        ]
        return code, {
            "name": get(company, "companyName", "name"),
            "type": get(company, "type", "companyType"),
            "endpoints": endpoints,
        }, None

    done = 0
    with futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        for code, entry, error in pool.map(one, companies):
            done += 1
            if code is None:
                continue
            if error:
                out["errors"][code] = error
            else:
                seen_codes.update(
                    e["service"] for e in entry["endpoints"] if e["service"]
                )
                out["companies"][code] = entry
            if done % 100 == 0 or done == len(companies):
                print(f"  {done}/{len(companies)} companies "
                      f"({len(out['errors'])} error(s))", file=sys.stderr)

    out["observed_service_codes"] = sorted(seen_codes)
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(out, handle, indent=2, sort_keys=False)
    print(f"\nwrote {args.output}", file=sys.stderr)
    return _summarize(out)


def cmd_summary(args: argparse.Namespace) -> int:
    with open(args.input, encoding="utf-8") as handle:
        return _summarize(json.load(handle))


def _summarize(dump: dict) -> int:
    """Print per-service adoption counts and version distribution."""
    companies = dump.get("companies", {})
    per_service: dict[str, set[str]] = collections.defaultdict(set)
    per_version: dict[str, collections.Counter] = collections.defaultdict(
        collections.Counter
    )

    for code, entry in companies.items():
        for endpoint in entry.get("endpoints", []):
            svc = endpoint.get("service")
            if not svc:
                continue
            per_service[svc].add(code)
            version = endpoint.get("version") or "(unspecified)"
            per_version[svc][str(version)] += 1

    total = len(companies)
    print(f"\nCompanies in registry: {total}")
    if dump.get("errors"):
        print(f"Companies that failed to read: {len(dump['errors'])}")
    print(f"Observed service codes: "
          f"{', '.join(dump.get('observed_service_codes') or sorted(per_service))}")
    print("\nAdoption by service (companies supporting / % of registry):")
    header = f"  {'SVC':<10} {'COMPANIES':>9} {'PCT':>6}   VERSIONS"
    print(header)
    print(f"  {'-' * (len(header) - 2)}")
    for svc, supporters in sorted(
        per_service.items(), key=lambda kv: len(kv[1]), reverse=True
    ):
        pct = (100.0 * len(supporters) / total) if total else 0.0
        versions = ", ".join(
            f"{ver}:{count}"
            for ver, count in per_version[svc].most_common()
        )
        print(f"  {svc:<10} {len(supporters):>9} {pct:>5.1f}%   {versions}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("probe", help="dump raw shapes, verify field names")

    dump = sub.add_parser("dump", help="full registry walk -> JSON")
    dump.add_argument("-o", "--output", default="promostandards_endpoints.json")
    dump.add_argument("-w", "--workers", type=int, default=12,
                      help="concurrent company fetches (default 12)")

    summary = sub.add_parser("summary", help="adoption counts from a dump")
    summary.add_argument("-i", "--input", default="promostandards_endpoints.json")

    args = parser.parse_args(argv)
    handlers = {"probe": cmd_probe, "dump": cmd_dump, "summary": cmd_summary}
    try:
        return handlers[args.command](args)
    except RegistryError as exc:
        print(f"registry error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
