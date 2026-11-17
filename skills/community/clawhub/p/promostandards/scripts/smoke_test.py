#!/usr/bin/env python3
"""Live read-only smoke test / provisioning validator.

Given a company code (or a config file) and credentials in the environment,
calls every **read** endpoint the supplier registers and reports
pass / fail / unsupported per service. Doubles as the health check for an
already-provisioned supplier.

`sendPO` is never called, and there is no flag to make it call one — a
write does not belong in a health check. `getSupportedOrderTypes` is used
to prove the PO endpoint is reachable instead, which is read-only.

    smoke_test.py --company SanMar --product-id PC61
    smoke_test.py --config sanmar.json --product-id PC61 --json
"""

from __future__ import annotations

import argparse
import json
import sys
import time

import provision
from client import PromoStandardsClient
from config import SupplierConfig
from errors import NotSupportedError, PromoStandardsError

#: (service, label, callable) — every one read-only.
CHECKS = [
    ("INV", "getInventoryLevels",
     lambda c, p: c.get_inventory(p["product_id"])),
    ("INV", "getFilterValues",
     lambda c, p: c.get_inventory_filters(p["product_id"])),
    ("PRODUCT", "getProduct",
     lambda c, p: c.get_product(p["product_id"])),
    ("PPC", "getFobPoints",
     lambda c, p: c.get_fob_points(p["product_id"])),
    ("PPC", "getAvailableLocations",
     lambda c, p: c.get_decoration_locations(p["product_id"])),
    ("PO", "getSupportedOrderTypes",
     lambda c, p: c.adapter("PO").get_supported_order_types()),
]


def _summarize(value: object) -> str:
    """One-line description of a result, for the human-readable report."""
    if hasattr(value, "levels"):
        levels = value.levels
        located = sum(1 for lvl in levels if lvl.locations)
        return (f"{len(levels)} level(s)"
                + (f", {located} with warehouse detail" if located else ""))
    if hasattr(value, "parts"):
        return f"product '{value.name or value.product_id}', {len(value.parts)} part(s)"
    if isinstance(value, list):
        return f"{len(value)} row(s)"
    if isinstance(value, dict):
        for key in ("part_ids", "order_types", "product_ids", "products"):
            if key in value:
                return f"{len(value[key])} {key}"
        return "ok"
    return "ok"


def run(client: PromoStandardsClient, product_id: str,
        services: list[str] | None = None) -> list[dict]:
    results = []
    params = {"product_id": product_id}

    for service, operation, call in CHECKS:
        if services and service not in services:
            continue
        if not client.config.supports(service):
            results.append({
                "service": service, "operation": operation,
                "status": "unsupported",
                "detail": "supplier does not publish this service",
            })
            continue

        started = time.time()
        try:
            value = call(client, params)
        except NotSupportedError as exc:
            results.append({
                "service": service, "operation": operation,
                "status": "unsupported", "detail": str(exc),
            })
        except PromoStandardsError as exc:
            results.append({
                "service": service, "operation": operation,
                "status": "fail", "detail": str(exc),
                "error_type": exc.kind,
                "ms": int((time.time() - started) * 1000),
            })
        except Exception as exc:  # noqa: BLE001 - a health check must not die
            results.append({
                "service": service, "operation": operation,
                "status": "fail", "detail": f"unexpected: {exc}",
                "error_type": "unexpected",
                "ms": int((time.time() - started) * 1000),
            })
        else:
            results.append({
                "service": service, "operation": operation,
                "status": "pass", "detail": _summarize(value),
                "ms": int((time.time() - started) * 1000),
            })
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--company", help="registry company code")
    source.add_argument("--config", help="path to a supplier config file")
    parser.add_argument("--product-id", required=True,
                        help="a product id known to exist at this supplier")
    parser.add_argument("--service", action="append",
                        help="limit to these services (repeatable)")
    parser.add_argument("--dump", help="registry dump path (with --company)")
    parser.add_argument("--test-endpoints", action="store_true",
                        help="target registered test endpoints where present")
    parser.add_argument("--json", action="store_true", help="machine-readable")
    args = parser.parse_args(argv)

    try:
        if args.config:
            config = SupplierConfig.load(args.config)
        else:
            config = SupplierConfig.from_dict(
                provision.build_config(args.company, dump_path=args.dump)
            )
    except PromoStandardsError as exc:
        print(json.dumps({"error": exc.as_dict()}), file=sys.stderr)
        return 2

    try:
        config.require_credentials()
    except PromoStandardsError as exc:
        # Named without ever printing the value.
        print(json.dumps({"error": exc.as_dict()}), file=sys.stderr)
        return 2

    client = PromoStandardsClient(config, use_test=args.test_endpoints)
    results = run(client, args.product_id,
                  [s.upper() for s in args.service] if args.service else None)

    counts = {"pass": 0, "fail": 0, "unsupported": 0}
    for row in results:
        counts[row["status"]] = counts.get(row["status"], 0) + 1

    if args.json:
        print(json.dumps({
            "supplier": config.supplier,
            "productId": args.product_id,
            "usedTestEndpoints": args.test_endpoints,
            "counts": counts,
            "results": results,
        }, indent=2))
    else:
        print(f"\nPromoStandards smoke test — {config.supplier} "
              f"(product {args.product_id})")
        print(f"{'SERVICE':<9} {'OPERATION':<26} {'STATUS':<12} DETAIL")
        print("-" * 78)
        for row in results:
            timing = f"[{row['ms']}ms] " if row.get("ms") is not None else ""
            print(f"{row['service']:<9} {row['operation']:<26} "
                  f"{row['status']:<12} {timing}{row['detail']}")
        print(f"\n{counts['pass']} passed, {counts['fail']} failed, "
              f"{counts['unsupported']} unsupported")

    # Non-zero only on real failures: "unsupported" is information, not error.
    return 1 if counts["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
