#!/usr/bin/env python3
"""Check whether a Texas service address is ready for destination URL generation."""

from __future__ import annotations

import argparse
import json
import re
from typing import List

from normalize_address_query import normalize_raw_address_query


UNIT_MARKER_PATTERN = re.compile(
    r"(?i)(?:\b(?:unit|apt|apartment|suite|ste|lot|bldg|building|u)\b\.?|#)"
)
UNIT_WITH_VALUE_PATTERN = re.compile(
    r"(?i)(?:\b(?:unit|apt|apartment|suite|ste|lot|bldg|building|u)\b\.?|#)\s*"
    r"([a-z0-9]+(?:\s*(?:&|and|-)\s*[a-z0-9]+)*)"
)
INCOMPLETE_UNIT_PATTERN = re.compile(
    r"(?i)(?:\b(?:unit|apt|apartment|suite|ste|lot|bldg|building|u)\b\.?|#)\s*$"
)


def clean(value: str | None) -> str:
    return (value or "").strip()


def has_street_number_and_name(street: str) -> bool:
    return bool(re.search(r"\d", street) and re.search(r"[A-Za-z]", street))


def normalize_unit_value(value: str) -> str:
    normalized = clean(value).lower()
    normalized = re.sub(r"\band\b", "&", normalized)
    normalized = re.sub(r"\s+", "", normalized)
    return normalized


def extract_inline_unit_values(street: str) -> List[str]:
    return [match.group(1) for match in UNIT_WITH_VALUE_PATTERN.finditer(street)]


def has_incomplete_unit_marker(street: str) -> bool:
    return bool(INCOMPLETE_UNIT_PATTERN.search(street.strip()))


def infer_unit_status(street: str, unit: str, requires_unit: bool) -> str:
    explicit_unit = normalize_unit_value(unit)
    inline_unit_values = {
        normalize_unit_value(value)
        for value in extract_inline_unit_values(street)
        if normalize_unit_value(value)
    }
    has_inline_marker = bool(UNIT_MARKER_PATTERN.search(street))
    incomplete_inline_unit = has_incomplete_unit_marker(street)

    if explicit_unit:
        if inline_unit_values and explicit_unit not in inline_unit_values:
            return "ambiguous"
        if len(inline_unit_values) > 1:
            return "ambiguous"
        return "provided"

    if incomplete_inline_unit:
        return "missing"

    if len(inline_unit_values) > 1:
        return "ambiguous"

    if requires_unit and not explicit_unit and not inline_unit_values:
        return "missing"

    if has_inline_marker and not inline_unit_values:
        return "missing"

    if inline_unit_values:
        return "provided"

    return "missing" if requires_unit else "not_needed"


def collect_missing_fields(
    street: str,
    city: str,
    zipcode: str,
    state: str,
    unit: str,
    requires_unit: bool,
) -> List[str]:
    missing: List[str] = []
    unit_status = infer_unit_status(street=street, unit=unit, requires_unit=requires_unit)

    if not has_street_number_and_name(street):
        missing.append("street")
    if not clean(city):
        missing.append("city")
    if not re.fullmatch(r"\d{5}", clean(zipcode)):
        missing.append("zipcode")
    if clean(state) and clean(state).upper() != "TX":
        missing.append("state")
    if unit_status in {"missing", "ambiguous"}:
        missing.append("unit")

    return missing


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check whether a Texas service address is complete enough to build a destination URL.",
    )
    parser.add_argument(
        "--address-query",
        default="",
        help="Raw address query to normalize before readiness checks.",
    )
    parser.add_argument("--street", default="")
    parser.add_argument("--unit", default="")
    parser.add_argument("--city", default="")
    parser.add_argument("--state", default="TX")
    parser.add_argument("--zipcode", default="")
    parser.add_argument(
        "--requires-unit",
        action="store_true",
        help="Require a unit value when the address is a multi-family or unit-specific location.",
    )
    args = parser.parse_args()

    normalized_query = (
        normalize_raw_address_query(args.address_query)
        if clean(args.address_query)
        else None
    )
    normalized_fields = normalized_query["normalized"] if normalized_query else {}

    street = clean(args.street) or normalized_fields.get("street", "")
    unit = clean(args.unit) or normalized_fields.get("unit", "")
    city = clean(args.city) or normalized_fields.get("city", "")
    state_input = clean(args.state)
    normalized_state = clean(normalized_fields.get("state", ""))
    state = state_input if args.state != "TX" or not normalized_state else normalized_state
    if not state:
        state = "TX"
    zipcode = clean(args.zipcode) or normalized_fields.get("zipcode", "")

    normalized_unit_status = normalized_query["unit_status"] if normalized_query else "not_needed"
    requires_unit = args.requires_unit or normalized_unit_status in {"missing", "ambiguous", "provided"}

    missing_fields = collect_missing_fields(
        street=street,
        city=city,
        zipcode=zipcode,
        state=state,
        unit=unit,
        requires_unit=requires_unit,
    )
    unit_status = infer_unit_status(
        street=street,
        unit=unit,
        requires_unit=requires_unit,
    )

    result = {
        "address_query": clean(args.address_query),
        "can_build_destination_url": not missing_fields,
        "inferred_requires_unit": unit_status in {"missing", "ambiguous", "provided"},
        "normalized_address": {
            "city": city,
            "state": state.upper() or "TX",
            "street": street,
            "unit": unit,
            "zipcode": zipcode,
        },
        "normalized_query": normalized_query,
        "normalized_state": state.upper() or "TX",
        "missing_fields": missing_fields,
        "requires_unit": requires_unit,
        "unit_status": unit_status,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
