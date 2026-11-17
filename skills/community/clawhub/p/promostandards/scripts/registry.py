"""Capability introspection from the endpoint registry.

Answers "what can this supplier actually do?" from registry data, before
any call goes out. That ordering is the point: an agent should learn that a
supplier has no Inventory service from a capability list at provisioning
time, not from a SOAP fault in the middle of a stock check.

Reads the captured dump (`assets/promostandards_endpoints.json`) by
default so provisioning works offline and repeatably; `--live` refreshes a
single company straight from the registry.
"""

from __future__ import annotations

import json
import os

import adapters
from config import SERVICE_CODES, normalize_service
from errors import ConfigError, NotSupportedError
from schemas import Capability

DEFAULT_DUMP = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "promostandards_endpoints.json",
)


def load_dump(path: str | None = None) -> dict:
    path = path or DEFAULT_DUMP
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError as exc:
        raise ConfigError(
            f"endpoint registry dump not found at {path}. "
            "Run: ps_registry.py dump -o <path>"
        ) from exc


def find_company(dump: dict, company_code: str) -> tuple[str, dict]:
    """Resolve a company code case-insensitively.

    Registry codes are wildly inconsistent ('SanMar', '135promos',
    '110964'), so an exact-match-only lookup fails constantly in practice.
    Falls back to a unique name match before giving up.
    """
    companies = dump.get("companies") or {}
    if company_code in companies:
        return company_code, companies[company_code]

    wanted = company_code.strip().lower()
    for code, entry in companies.items():
        if code.strip().lower() == wanted:
            return code, entry

    matches = [
        (code, entry) for code, entry in companies.items()
        if (entry.get("name") or "").strip().lower() == wanted
    ]
    if len(matches) == 1:
        return matches[0]

    raise ConfigError(
        f"company '{company_code}' not found in the registry dump"
        + (f" ({len(matches)} name matches — use the exact code)"
           if matches else "")
    )


def capabilities_for(company_code: str, dump: dict | None = None,
                     path: str | None = None) -> list[Capability]:
    """Every service the registry lists for a company, flagged by support.

    `supported` distinguishes "the supplier publishes this" from "we can
    drive it": a supplier on a version this package has no adapter for is
    reported, with supported=False, rather than omitted. A silent omission
    would read as "the supplier doesn't offer it", which is a different
    and actionable fact.
    """
    dump = dump or load_dump(path)
    _, entry = find_company(dump, company_code)

    capabilities = []
    for endpoint in entry.get("endpoints") or []:
        service = endpoint.get("service")
        version = endpoint.get("version")
        if not service:
            # Company Data and Remittance Advice carry an empty code.
            continue
        code = normalize_service(service)
        try:
            adapter_cls = adapters.get_adapter_class(code, str(version))
            operations = list(adapter_cls.OPERATIONS)
            supported = True
        except NotSupportedError:
            operations = []
            supported = False
        capabilities.append(Capability(
            service=code,
            service_name=endpoint.get("service_name") or SERVICE_CODES.get(code),
            version=str(version) if version else None,
            url=endpoint.get("url"),
            test_url=endpoint.get("test_url"),
            status=endpoint.get("status"),
            supported=supported,
            operations=operations,
        ))

    capabilities.sort(key=lambda c: (c.service or "", c.version or ""))
    return capabilities


def best_endpoints(capabilities: list[Capability]) -> dict[str, Capability]:
    """Pick one endpoint per service — the newest version we can drive.

    A supplier publishing Inventory at both 1.2.1 and 2.0.0 gets 2.0.0,
    which is also the only version that reports per-warehouse stock.
    Unsupported versions are considered only when nothing supported exists,
    so the resulting config still records the service (with a version we
    cannot drive) rather than pretending it is absent.
    """
    chosen: dict[str, Capability] = {}
    for capability in capabilities:
        service = capability.service
        if not service:
            continue
        current = chosen.get(service)
        if current is None:
            chosen[service] = capability
            continue
        # Prefer supported over unsupported, then the higher version.
        if capability.supported != current.supported:
            if capability.supported:
                chosen[service] = capability
            continue
        if _version_key(capability.version) > _version_key(current.version):
            chosen[service] = capability
    return chosen


def _version_key(version: str | None) -> tuple:
    if not version:
        return ()
    parts = []
    for chunk in str(version).split("."):
        try:
            parts.append(int(chunk))
        except ValueError:
            parts.append(0)
    return tuple(parts)


def summarize(capabilities: list[Capability]) -> dict:
    """Compact capability report for a drive-thru listing."""
    supported = [c for c in capabilities if c.supported]
    return {
        "capabilities": sorted({c.service for c in supported if c.service}),
        "unsupported": sorted({
            f"{c.service}@{c.version}" for c in capabilities
            if not c.supported and c.service
        }),
        "operations": sorted({
            op for c in supported for op in c.operations
        }),
    }
