#!/usr/bin/env python3
"""Validate structured appeal data and generate matching Markdown and PDF files."""

from __future__ import annotations

import argparse
import html
import ipaddress
import json
import os
import re
import sys
import tempfile
import unicodedata
from datetime import date, timedelta
from math import isfinite
from pathlib import Path
from statistics import median
from typing import Any
from urllib.parse import unquote, urlsplit

from url_safety import public_https_url_error

ALLOWED_PRICE_KINDS = {"exact_closed_price", "range_lower_bound"}
ALLOWED_ARM_LENGTH = {"verified", "likely", "unknown", "not_arm_length"}
ALLOWED_COMPARISON_VALUE_TYPES = {
    "actual_value",
    "estimated_market_value",
    "fair_market_value",
    "full_cash_value",
    "just_value",
    "market_value",
    "true_value",
}
ALLOWED_NOTICE_DERIVATIONS = {
    "authority_specific",
    "cap",
    "classification",
    "equalization",
    "exemption",
    "ratio",
    "reported_only",
    "same_as_source",
}
ALLOWED_NOTICE_VALUE_TYPES = {
    "actual_value",
    "appraised_value",
    "assessed_value",
    "equalized_assessed_value",
    "estimated_market_value",
    "fair_market_value",
    "full_cash_value",
    "just_value",
    "limited_property_value",
    "market_value",
    "state_equalized_value",
    "taxable_value",
    "true_value",
}
ASSESSED_VALUE_TYPES = {
    "appraised_value",
    "assessed_value",
    "limited_property_value",
}
EQUALIZED_VALUE_TYPES = {
    "equalized_assessed_value",
    "state_equalized_value",
}
TAXABLE_VALUE_TYPES = {"taxable_value"}
DERIVATION_TYPE_EDGES: dict[str, frozenset[tuple[str, str]]] = {
    "ratio": frozenset(
        {
            *(
                (source, target)
                for source in ALLOWED_COMPARISON_VALUE_TYPES
                for target in ASSESSED_VALUE_TYPES
            ),
            ("appraised_value", "assessed_value"),
            ("limited_property_value", "assessed_value"),
        }
    ),
    "cap": frozenset(
        {
            *(
                (source, target)
                for source in ALLOWED_COMPARISON_VALUE_TYPES
                for target in ASSESSED_VALUE_TYPES
            ),
            ("appraised_value", "assessed_value"),
            ("appraised_value", "limited_property_value"),
            ("assessed_value", "limited_property_value"),
        }
    ),
    "classification": frozenset(
        (source, target)
        for source in ALLOWED_COMPARISON_VALUE_TYPES
        for target in ("appraised_value", "assessed_value")
    ),
    "equalization": frozenset(
        {
            *(
                (source, target)
                for source in ASSESSED_VALUE_TYPES
                for target in EQUALIZED_VALUE_TYPES
            ),
            ("equalized_assessed_value", "state_equalized_value"),
        }
    ),
    "exemption": frozenset(
        (source, "taxable_value")
        for source in ASSESSED_VALUE_TYPES | EQUALIZED_VALUE_TYPES
    ),
    "authority_specific": frozenset(
        {
            *((source, "taxable_value") for source in ASSESSED_VALUE_TYPES),
            *((source, "taxable_value") for source in EQUALIZED_VALUE_TYPES),
            ("taxable_value", "taxable_value"),
        }
    ),
}
NONINCREASING_DERIVATIONS = {
    "authority_specific",
    "cap",
    "classification",
    "exemption",
}
ALLOWED_REJECTED_STATUSES = {
    "valuation_eligible_omitted",
    "research_only_inadmissible",
}
ALLOWED_REJECTION_REASONS = {
    "above_current_comparison_value",
    "age_mismatch",
    "bed_bath_mismatch",
    "condition_mismatch",
    "duplicate_record",
    "hoa_context_mismatch",
    "living_area_mismatch",
    "location_mismatch",
    "non_arm_length",
    "non_market_transfer",
    "outside_legal_sale_window",
    "property_type_mismatch",
    "unverified_transaction",
}
INADMISSIBLE_REJECTION_REASONS = {
    "duplicate_record",
    "non_arm_length",
    "non_market_transfer",
    "outside_legal_sale_window",
    "unverified_transaction",
}
TRANSACTION_RECORD_REJECTION_REASONS = {
    "duplicate_record",
    "non_arm_length",
    "non_market_transfer",
    "outside_legal_sale_window",
}
ALLOWED_SOURCE_ROLES = {
    "appeal_rule",
    "assessment_notice",
    "deadline_rule",
    "marketability_evidence",
    "parcel_record",
    "sale_window_rule",
    "submission_rule",
    "transaction_record",
    "valuation_rule",
}
ALLOWED_SOURCE_KINDS = {"owner_attachment", "public_url"}
OWNER_ATTACHMENT_SOURCE_ROLES = {
    "assessment_notice",
    "marketability_evidence",
    "transaction_record",
}
ALLOWED_SOURCE_FIELDS = {
    "accessed_date",
    "id",
    "publisher",
    "roles",
    "source_kind",
    "supports",
    "title",
    "url",
}
LEGAL_SOURCE_ROLES = {
    "appeal_rule",
    "deadline_rule",
    "sale_window_rule",
    "submission_rule",
    "valuation_rule",
}
ALLOWED_DOCUMENT_MODES = {
    "informal_review_attachment",
    "formal_board_evidence",
    "protest_statement",
    "grievance_support",
    "abatement_support",
    "tribunal_exhibit",
}
ALLOWED_ROUTE_FAMILIES = {
    "assessor_then_local_board",
    "local_equalization_board",
    "abatement",
    "grievance",
    "appraisal_review_board",
    "value_adjustment_board",
    "board_of_revision",
    "county_tax_board",
    "bopta",
    "state_assessment_ladder",
}
CONTROL_CHARACTER_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
SOURCE_ID_RE = re.compile(r"[A-Za-z0-9._-]{1,40}")
MARKDOWN_SPECIAL_RE = re.compile(r"([\\`*_\[\]|<>])")
OBFUSCATED_URI_RE = re.compile(
    r"(?<![A-Za-z0-9+.-])[A-Za-z][A-Za-z0-9+.-]{0,31}\s*:\s*(?://|\\\\)",
    re.IGNORECASE,
)
URI_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9+.-])(?P<uri>[A-Za-z][A-Za-z0-9+.-]{0,31}:"
    r"[^\s\"'<>]+)",
    re.IGNORECASE,
)
ABSOLUTE_PATH_RE = re.compile(
    r"(?:"
    r"(?:\\\\|//)[^/\\\s\"'<>]+[/\\][^\s\"'<>]+|"
    r"[a-z]:[/\\][^\s\"'<>]+|"
    r"(?:~|\.\.?)[/\\][^\s\"'<>]+)",
    re.IGNORECASE,
)
NUMERIC_SLASH_NOTATION_RE = re.compile(
    r"(?<!\S)\d+(?:\.\d+)?(?:/\d+(?:\.\d+)?)+(?:[.,;:!?])?(?!\S)"
)
ASCII_DNS_LABEL_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")
SERVICE_DNS_LABEL_RE = re.compile(r"_[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?")
BRACKETED_IP_RE = re.compile(r"\[([^\]]+)\](?::\d{1,5})?")
LOCALHOST_RE = re.compile(r"(?<![\w-])localhost(?![\w-])", re.IGNORECASE)
ASCII_DOTTED_DECIMAL_RE = re.compile(r"[0-9]+\.[0-9]+")
DNS_TOKEN_DELIMITERS = frozenset("/\\@=,:;!?()[]{}\"'<>+$%|*`")
OWNER_ATTACHMENT_DISPLAY = (
    "Owner-provided attachment (not embedded; attach separately through the official filing channel)"
)
MAX_ABSOLUTE_NUMBER = 1_000_000_000_000_000
MAX_JSON_INTEGER_DIGITS = len(str(MAX_ABSOLUTE_NUMBER))
MAX_CASE_JSON_BYTES = 5 * 1024 * 1024
MAX_JSON_NESTING_DEPTH = 100
MAX_SELECTED_COMPARABLES = 20
MAX_REJECTED_COMPARABLES = 100
MAX_SOURCES = 200
MAX_NOTICE_VALUES = 50
MAX_SPECIAL_FACTORS = 20
MAX_TEXT_LIST_ITEMS = 50
MAX_SOURCE_LINKS = 50
MAX_SOURCE_SUPPORTS = 50
MAX_REJECTION_REASONS = len(ALLOWED_REJECTION_REASONS)
MAX_VALIDATION_ERRORS = 200
MAX_VALIDATION_ERROR_LENGTH = 1000
MAX_UNKNOWN_FIELDS_REPORTED = 20
MAX_LOCATOR_NORMALIZATION_PASSES = 2048
MAX_LOCATOR_NORMALIZATION_WORK = 1_000_000
MAX_DNS_CANDIDATE_CHARS = 253
MAX_IP_CANDIDATE_CHARS = 128

TOP_LEVEL_FIELDS = {
    "schema_version",
    "case",
    "selection_policy",
    "comparables",
    "rejected_comparables",
    "contrary_evidence_review",
    "sources",
}
CASE_FIELDS = {
    "review_title",
    "appeal_type",
    "appeal_ground",
    "document_mode",
    "property_address",
    "apn",
    "assessment_year",
    "valuation_date",
    "value_basis",
    "likely_comparison_value_range",
    "prepared_date",
    "subject_source_ids",
    "assessment_source_ids",
    "jurisdiction",
    "property",
    "valuation_rationale",
    "verification",
    "owner_name",
    "argument_points",
    "suggested_attachments",
    "declaration",
    "declaration_owner_approved",
    "include_signature_block",
    "special_factors",
    "initial_assessed_value",
    "requested_value",
    "likely_value_range",
}
VALUE_BASIS_FIELDS = {
    "comparison_basis_kind",
    "comparison_value_type",
    "comparison_value_label",
    "current_comparison_value",
    "requested_comparison_value",
    "primary_notice_value_id",
    "notice_values",
    "source_ids",
    "notice_value_type",
    "notice_value_label",
    "current_notice_value",
    "requested_notice_value",
    "assessment_ratio",
}
NOTICE_VALUE_FIELDS = {
    "id",
    "value_type",
    "label",
    "authority",
    "current_value",
    "requested_value",
    "derivation",
    "source_ids",
}
DERIVATION_FIELDS = {"kind", "source_value_id", "factor", "description", "source_ids"}
RANGE_FIELDS = {"low", "high"}
VERIFICATION_FIELDS = {
    "official_rules_rechecked",
    "official_rules_current_as_of",
    "subject_facts_reconciled",
    "value_basis_reconciled",
    "comparable_sales_verified",
    "contrary_evidence_reviewed",
}
JURISDICTION_FIELDS = {
    "country",
    "state",
    "state_code",
    "county_or_locality",
    "route_family",
    "route_override",
    "appeal_stage",
    "filing_authority",
    "valuation_standard",
    "filing_deadline_rule",
    "filing_deadline",
    "official_form_required",
    "official_form_name",
    "official_form_url",
    "submission_url",
    "informal_preserves_formal_deadline",
    "source_ids",
    "deadline_source_ids",
}
ROUTE_OVERRIDE_FIELDS = {"reason", "source_ids"}
PROPERTY_FIELDS = {
    "property_type",
    "residential_use_verification",
    "year_built",
    "living_area_sqft",
    "bedrooms",
    "bathrooms",
    "stories",
    "lot_size_sqft",
    "parking",
    "development_or_hoa",
}
RESIDENTIAL_USE_FIELDS = {"status", "classification", "source_ids"}
CONTRARY_REVIEW_FIELDS = {
    "completed",
    "all_plausible_candidates_recorded",
    "summary",
    "disclosure",
    "source_ids",
}
SELECTION_POLICY_FIELDS = {
    "minimum_comps",
    "maximum_comps",
    "legal_sale_window",
    "strict_bed_bath_match",
    "strict_property_type_match",
    "exclude_above_current_comparison_value",
    "allow_provisional_range_prices",
    "max_post_valuation_days",
}
LEGAL_SALE_WINDOW_FIELDS = {"start_date", "end_date", "basis", "source_ids"}
SELECTED_COMPARABLE_FIELDS = {
    "address",
    "apn",
    "transaction_id",
    "sale_date",
    "sale_price",
    "price_source_kind",
    "reported_price_range",
    "property_type",
    "bedrooms",
    "bathrooms",
    "living_area_sqft",
    "year_built",
    "distance_miles",
    "same_development",
    "arm_length_status",
    "relevance",
    "source_ids",
}
REJECTED_COMPARABLE_FIELDS = SELECTED_COMPARABLE_FIELDS | {
    "valuation_status",
    "reasons",
    "relevance_review",
    "materially_contrary",
    "duplicate_of_transaction_id",
}
SPECIAL_FACTOR_FIELDS = {"title", "facts", "market_effect", "source_ids"}


class ValidationErrors(list[str]):
    """Collect a bounded number of deterministic validation errors."""

    def __init__(self, limit: int = MAX_VALIDATION_ERRORS) -> None:
        super().__init__()
        self.limit = limit
        self.suppressed = 0

    def append(self, item: str) -> None:
        if len(item) > MAX_VALIDATION_ERROR_LENGTH:
            item = item[: MAX_VALIDATION_ERROR_LENGTH - 3] + "..."
        if len(self) < self.limit:
            super().append(item)
        else:
            self.suppressed += 1

    def extend(self, items: Any) -> None:
        for item in items:
            self.append(item)

    def reported(self) -> list[str]:
        result = list(self)
        if self.suppressed:
            result.append(
                f"Additional validation errors suppressed after the first {self.limit}: "
                f"{self.suppressed}"
            )
        return result


def money(value: float) -> str:
    return f"${value:,.0f}"


def number(value: float | None) -> str:
    if value is None:
        return "Not reported"
    if float(value).is_integer():
        return f"{int(value):,}"
    return f"{value:,.1f}"


def normalized_locator_variants(value: str) -> tuple[str, ...] | None:
    variants: list[str] = []
    candidate = value
    work = 0
    translation = str.maketrans(
        {
            "\u2044": "/",
            "\u2215": "/",
            "\uff0f": "/",
            "\u29f5": "\\",
            "\ufe68": "\\",
            "\uff3c": "\\",
            "\u3002": ".",
            "\uff0e": ".",
            "\uff61": ".",
        }
    )
    for _iteration in range(MAX_LOCATOR_NORMALIZATION_PASSES):
        work += len(candidate)
        if work > MAX_LOCATOR_NORMALIZATION_WORK:
            return None
        variants.append(candidate)
        normalized = html.unescape(candidate)
        normalized = unquote(normalized)
        normalized = unicodedata.normalize("NFKC", normalized).translate(translation)
        normalized = "".join(
            character
            for character in normalized
            if unicodedata.category(character) != "Cf"
        )
        if normalized == candidate:
            return tuple(variants)
        candidate = normalized
    return None


def contains_uri_locator(value: str) -> bool:
    if OBFUSCATED_URI_RE.search(value):
        return True
    for match in URI_TOKEN_RE.finditer(value):
        try:
            if urlsplit(match.group("uri")).scheme:
                return True
        except ValueError:
            return True
    return False


def contains_path_separator_locator(value: str) -> bool:
    allowed_slashes = {
        index
        for match in NUMERIC_SLASH_NOTATION_RE.finditer(value)
        for index in range(match.start(), match.end())
        if value[index] == "/"
    }
    return any(
        character == "\\" or index not in allowed_slashes
        for index, character in enumerate(value)
        if character in "/\\"
    )


def is_ip_literal_candidate(value: str) -> bool:
    candidate = value.rstrip(".")
    bracketed = BRACKETED_IP_RE.fullmatch(candidate)
    if bracketed:
        candidate = bracketed.group(1)

    options = [candidate]
    if candidate.count(":") == 1:
        host, port = candidate.rsplit(":", 1)
        if port.isdigit() and 1 <= len(port) <= 5:
            options.append(host)
    compressed_suffix = candidate.find("::", 1)
    if compressed_suffix > 0:
        options.append(candidate[compressed_suffix:])

    scoped_options = []
    for option in options:
        if "%" not in option:
            continue
        base = option.split("%", 1)[0].removeprefix("[").removesuffix("]")
        scoped_options.append(base)
    options.extend(scoped_options)

    for option in options:
        try:
            ipaddress.ip_address(option)
        except ValueError:
            continue
        return True
    return False


def is_dns_name_candidate(value: str) -> bool:
    hostname = value.rstrip(".")
    labels = hostname.split(".")
    if len(labels) < 2 or any(not label for label in labels):
        return False
    if ASCII_DOTTED_DECIMAL_RE.fullmatch(hostname):
        return False

    encoded_length = len(labels) - 1
    for label in labels:
        if label.startswith("_"):
            if SERVICE_DNS_LABEL_RE.fullmatch(label) is None:
                return False
            encoded_label = label.encode("ascii")
        else:
            try:
                encoded_label = label.encode("idna")
            except UnicodeError:
                return False
            if ASCII_DNS_LABEL_RE.fullmatch(encoded_label.decode("ascii")) is None:
                return False
        if len(encoded_label) > 63:
            return False
        encoded_length += len(encoded_label)
    return encoded_length <= 253


def dns_candidate_tokens(value: str):
    candidate: list[str] = []
    has_dot = False
    overlong = False

    for character in value:
        is_delimiter = (
            character.isspace()
            or character in DNS_TOKEN_DELIMITERS
            or unicodedata.category(character).startswith("C")
        )
        if not is_delimiter:
            has_dot = has_dot or character == "."
            if len(candidate) < MAX_DNS_CANDIDATE_CHARS:
                candidate.append(character)
            else:
                overlong = True
            continue
        if has_dot:
            yield "".join(candidate), overlong
        candidate = []
        has_dot = False
        overlong = False
    if has_dot:
        yield "".join(candidate), overlong


def ip_literal_candidate_tokens(value: str):
    candidate: list[str] = []
    has_colon = False
    overlong = False

    for character in value:
        is_candidate_character = character.isascii() and (
            character.isalnum() or character in "[]_.:%-"
        )
        if is_candidate_character:
            has_colon = has_colon or character == ":"
            if len(candidate) < MAX_IP_CANDIDATE_CHARS:
                candidate.append(character)
            else:
                overlong = True
            continue
        if has_colon:
            yield "".join(candidate), overlong
        candidate = []
        has_colon = False
        overlong = False
    if has_colon:
        yield "".join(candidate), overlong


def contains_host_locator(value: str) -> bool:
    if LOCALHOST_RE.search(value):
        return True
    for candidate, overlong in ip_literal_candidate_tokens(value):
        if overlong or is_ip_literal_candidate(candidate):
            return True
    for candidate, overlong in dns_candidate_tokens(value):
        if overlong:
            return True
        if is_ip_literal_candidate(candidate) or is_dns_name_candidate(candidate):
            return True
        hostname = candidate.rstrip(".")
        is_plain_decimal = ASCII_DOTTED_DECIMAL_RE.fullmatch(hostname) is not None
        if "." in hostname and not is_plain_decimal:
            return True
    return False


def private_locator_problem(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    variants = normalized_locator_variants(value)
    if variants is None:
        return True
    return any(
        contains_uri_locator(candidate)
        or contains_path_separator_locator(candidate)
        or ABSOLUTE_PATH_RE.search(candidate)
        or contains_host_locator(candidate)
        for candidate in variants
    )


def reject_unknown_fields(
    mapping: dict[Any, Any],
    allowed: set[str],
    path: str,
    errors: list[str],
) -> None:
    unexpected = [key for key in mapping if not isinstance(key, str) or key not in allowed]
    if not unexpected:
        return
    labels = sorted(
        [key if isinstance(key, str) else repr(key) for key in unexpected],
        key=ascii,
    )
    displayed = [
        label[:77] + "..." if len(label) > 80 else label
        for label in labels[:MAX_UNKNOWN_FIELDS_REPORTED]
    ]
    suffix = (
        f"; {len(labels) - MAX_UNKNOWN_FIELDS_REPORTED} additional fields omitted"
        if len(labels) > MAX_UNKNOWN_FIELDS_REPORTED
        else ""
    )
    errors.append(f"{path} contains unsupported fields: {', '.join(displayed)}{suffix}")


def bounded_items(
    value: list[Any],
    path: str,
    maximum: int,
    errors: list[str],
) -> list[Any]:
    if len(value) > maximum:
        errors.append(f"{path} may contain at most {maximum} items; found {len(value)}")
        return value[:maximum]
    return value


def reject_unicode_surrogates(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, str):
        if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
            errors.append(f"{path} contains an invalid Unicode surrogate")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            reject_unicode_surrogates(item, f"{path}[{index}]", errors)
        return
    if isinstance(value, dict):
        for index, (key, item) in enumerate(value.items()):
            if isinstance(key, str) and any(
                0xD800 <= ord(character) <= 0xDFFF for character in key
            ):
                errors.append(f"{path} object key at position {index} contains an invalid Unicode surrogate")
                child_path = f"{path}.<invalid-key-{index}>"
            else:
                child_path = f"{path}.{key}" if isinstance(key, str) else f"{path}.<key-{index}>"
            reject_unicode_surrogates(item, child_path, errors)


def validate_text(
    value: Any,
    field: str,
    errors: list[str],
    *,
    max_length: int,
    allow_newlines: bool = False,
) -> str | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a nonempty string")
        return None
    if len(value) > max_length:
        errors.append(f"{field} must be no longer than {max_length} characters")
        return value
    if CONTROL_CHARACTER_RE.search(value):
        errors.append(f"{field} contains a control character")
    if not allow_newlines and ("\n" in value or "\r" in value):
        errors.append(f"{field} must be a single line")
    reject_private_locator(value, field, errors)
    return value


def validate_url(value: Any, field: str, errors: list[str]) -> str | None:
    problem = public_https_url_error(value)
    if problem:
        errors.append(f"{field} {problem}")
        return None
    return value


def reject_private_locator(value: Any, field: str, errors: list[str]) -> None:
    if private_locator_problem(value):
        errors.append(
            f"{field} must not contain a URL or local path; describe the attachment without a locator"
        )


def validate_source_links(
    path: str,
    linked_sources: Any,
    source_ids: set[str],
    errors: list[str],
    *,
    required_roles: set[str] | None = None,
    source_roles: dict[str, set[str]] | None = None,
) -> list[str]:
    if not isinstance(linked_sources, list) or not linked_sources:
        errors.append(f"{path} must be a nonempty array")
        return []
    linked_sources = bounded_items(linked_sources, path, MAX_SOURCE_LINKS, errors)
    normalized: list[str] = []
    for source_id in linked_sources:
        if not isinstance(source_id, str):
            errors.append(f"{path} must contain only string source ids")
            continue
        value = source_id
        normalized.append(value)
        if value not in source_ids:
            errors.append(f"{path} references unknown source id {source_id}")
    if required_roles and source_roles is not None:
        linked_roles = set().union(*(source_roles.get(item, set()) for item in normalized))
        missing_roles = sorted(required_roles - linked_roles)
        if missing_roles:
            errors.append(f"{path} must reference sources with roles: {', '.join(missing_roles)}")
    return normalized


def md_escape(value: Any) -> str:
    normalized = str(value).replace("\r\n", "\n").replace("\r", "\n")
    escaped_lines = []
    for line in normalized.split("\n"):
        escaped = MARKDOWN_SPECIAL_RE.sub(r"\\\1", line)
        escaped = re.sub(
            r"^(\s*)(#{1,6})",
            lambda match: match.group(1) + "\\#" * len(match.group(2)),
            escaped,
        )
        escaped = re.sub(r"^(\s*)([>+-]|\d+\.)", r"\1\\\2", escaped)
        escaped_lines.append(escaped)
    return "  \n".join(escaped_lines)


def iso_date(value: Any, field: str, errors: list[str]) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{field} must use YYYY-MM-DD format; got {value!r}")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{field} must use YYYY-MM-DD format; got {value!r}")
        return None


def display_date(value: str) -> str:
    parsed = date.fromisoformat(value)
    return f"{parsed.strftime('%B')} {parsed.day}, {parsed.year}"


def display_deadline(jurisdiction: dict[str, Any]) -> str:
    value = jurisdiction.get("filing_deadline")
    if value:
        return display_date(str(value))
    return "Notice-specific or not fixed; see deadline rule"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:90] or "property-tax-appeal"


def require(mapping: dict[str, Any], key: str, path: str, errors: list[str]) -> Any:
    value = mapping.get(key)
    if value is None or value == "" or value == []:
        errors.append(f"Missing required field: {path}.{key}")
    return value


def same_number(left: Any, right: Any) -> bool:
    try:
        return abs(float(left) - float(right)) < 0.001
    except (OverflowError, TypeError, ValueError):
        return False


def transactions_match(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_fingerprint = transaction_fingerprint(left)
    return left_fingerprint is not None and left_fingerprint == transaction_fingerprint(right)


def is_number(value: Any) -> bool:
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        return abs(value) <= MAX_ABSOLUTE_NUMBER
    return (
        isinstance(value, float)
        and isfinite(value)
        and abs(value) <= MAX_ABSOLUTE_NUMBER
    )


def is_integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def whole_dollar_amount(value: Any) -> int | None:
    if not is_number(value):
        return None
    numeric = float(value)
    if not numeric.is_integer():
        return None
    return int(numeric)


def transaction_fingerprint(record: dict[str, Any]) -> tuple[Any, ...] | None:
    normalized_strings: list[str] = []
    for field in ("address", "apn"):
        value = record.get(field)
        if not isinstance(value, str):
            return None
        normalized_strings.append(value.strip().casefold())
    sale_date = record.get("sale_date")
    price_kind = record.get("price_source_kind")
    sale_price = whole_dollar_amount(record.get("sale_price"))
    if not isinstance(sale_date, str) or not isinstance(price_kind, str):
        return None
    if sale_price is None:
        return None
    range_values: tuple[int, int] | None = None
    if price_kind == "range_lower_bound":
        reported_range = record.get("reported_price_range")
        if not isinstance(reported_range, dict):
            return None
        low = whole_dollar_amount(reported_range.get("low"))
        high = whole_dollar_amount(reported_range.get("high"))
        if low is None or high is None:
            return None
        range_values = (low, high)
    return (
        *normalized_strings,
        sale_date,
        price_kind,
        sale_price,
        range_values,
    )


def parse_bounded_json_int(raw_value: str) -> int:
    digits = raw_value.removeprefix("-").lstrip("0") or "0"
    if len(digits) > MAX_JSON_INTEGER_DIGITS:
        raise ValueError(
            f"JSON integer exceeds the supported numeric range of "
            f"+/-{MAX_ABSOLUTE_NUMBER}"
        )
    value = int(raw_value)
    if abs(value) > MAX_ABSOLUTE_NUMBER:
        raise ValueError(
            f"JSON integer exceeds the supported numeric range of "
            f"+/-{MAX_ABSOLUTE_NUMBER}"
        )
    return value


def reject_json_constant(raw_value: str) -> None:
    raise ValueError(f"Unsupported JSON numeric constant: {raw_value}")


class CaseJsonLimitError(ValueError):
    """Case JSON exceeded a deterministic parser resource boundary."""


class DuplicateJsonKeyError(ValueError):
    """Case JSON contained an ambiguous duplicate object key."""


def reject_duplicate_json_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            display_key = key if len(key) <= 80 else key[:77] + "..."
            raise DuplicateJsonKeyError(f"Duplicate JSON object key: {display_key!r}")
        result[key] = value
    return result


def validate_json_nesting(text: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character in "[{":
            depth += 1
            if depth > MAX_JSON_NESTING_DEPTH:
                raise CaseJsonLimitError(
                    f"Case JSON exceeds the maximum nesting depth of {MAX_JSON_NESTING_DEPTH}"
                )
        elif character in "]}":
            depth = max(0, depth - 1)


def load_case_json(path: Path) -> Any:
    with path.open("rb") as stream:
        raw = stream.read(MAX_CASE_JSON_BYTES + 1)
    if len(raw) > MAX_CASE_JSON_BYTES:
        raise CaseJsonLimitError(
            f"Case JSON exceeds the {MAX_CASE_JSON_BYTES // (1024 * 1024)} MiB input limit"
        )
    text = raw.decode("utf-8")
    validate_json_nesting(text)
    return json.loads(
        text,
        parse_int=parse_bounded_json_int,
        parse_constant=reject_json_constant,
        object_pairs_hook=reject_duplicate_json_keys,
    )


def first_existing_symlink_component(path: Path) -> Path | None:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        if current.is_symlink():
            return current
        if not current.exists():
            break
    return None


def derivation_type_error(kind: Any, source_type: Any, target_type: Any) -> str | None:
    if not all(isinstance(value, str) for value in (kind, source_type, target_type)):
        return "derivation kind, source type, and target type must all be strings"
    if kind == "reported_only":
        return None
    if kind == "same_as_source":
        if source_type != target_type:
            return "same_as_source requires identical source and target value types"
        return None
    allowed_edges = DERIVATION_TYPE_EDGES.get(kind)
    if allowed_edges is not None and (source_type, target_type) not in allowed_edges:
        return (
            f"{kind} does not allow {source_type} -> {target_type}; use reported_only "
            "when no supported mechanical relationship is claimed"
        )
    return None


def validate_case(data: Any) -> tuple[list[str], list[str]]:
    errors = ValidationErrors()
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["Top-level case data must be an object"], warnings

    reject_unicode_surrogates(data, "$", errors)
    if errors:
        return errors.reported(), warnings
    reject_unknown_fields(data, TOP_LEVEL_FIELDS, "Top-level case data", errors)

    if data.get("schema_version") != "2.0":
        errors.append("Top-level schema_version must be '2.0'")

    case = data.get("case")
    policy = data.get("selection_policy")
    comps = data.get("comparables")
    rejected = data.get("rejected_comparables", [])
    sources = data.get("sources")
    contrary_review = data.get("contrary_evidence_review")

    if not isinstance(case, dict):
        errors.append("Top-level 'case' must be an object")
        return errors.reported(), warnings
    if not isinstance(policy, dict):
        errors.append("Top-level 'selection_policy' must be an object")
        return errors.reported(), warnings
    if not isinstance(comps, list):
        errors.append("Top-level 'comparables' must be an array")
        return errors.reported(), warnings
    if not isinstance(rejected, list):
        errors.append("Top-level 'rejected_comparables' must be an array")
        rejected = []
    if not isinstance(sources, list):
        errors.append("Top-level 'sources' must be an array")
        return errors.reported(), warnings
    if not isinstance(contrary_review, dict):
        errors.append("Top-level 'contrary_evidence_review' must be an object")
        return errors.reported(), warnings

    comps = bounded_items(comps, "comparables", MAX_SELECTED_COMPARABLES, errors)
    rejected = bounded_items(
        rejected, "rejected_comparables", MAX_REJECTED_COMPARABLES, errors
    )
    sources = bounded_items(sources, "sources", MAX_SOURCES, errors)
    reject_unknown_fields(case, CASE_FIELDS, "case", errors)
    reject_unknown_fields(policy, SELECTION_POLICY_FIELDS, "selection_policy", errors)
    reject_unknown_fields(
        contrary_review,
        CONTRARY_REVIEW_FIELDS,
        "contrary_evidence_review",
        errors,
    )

    for key in (
        "review_title",
        "appeal_type",
        "appeal_ground",
        "document_mode",
        "property_address",
        "apn",
        "assessment_year",
        "valuation_date",
        "value_basis",
        "likely_comparison_value_range",
        "prepared_date",
        "subject_source_ids",
        "assessment_source_ids",
        "jurisdiction",
        "property",
        "valuation_rationale",
        "verification",
    ):
        require(case, key, "case", errors)

    for legacy_field in ("initial_assessed_value", "requested_value", "likely_value_range"):
        if legacy_field in case:
            errors.append(
                f"case.{legacy_field} is a legacy v1 field; migrate to case.value_basis and "
                "case.likely_comparison_value_range"
            )

    for key, limit, allow_newlines in (
        ("review_title", 180, False),
        ("appeal_type", 120, False),
        ("property_address", 300, False),
        ("apn", 100, False),
        ("assessment_year", 60, False),
        ("valuation_rationale", 2400, True),
    ):
        validate_text(
            case.get(key),
            f"case.{key}",
            errors,
            max_length=limit,
            allow_newlines=allow_newlines,
        )
    if "owner_name" in case and case["owner_name"] is not None:
        validate_text(case["owner_name"], "case.owner_name", errors, max_length=160)

    document_mode = case.get("document_mode")
    if not isinstance(document_mode, str) or document_mode not in ALLOWED_DOCUMENT_MODES:
        errors.append(f"case.document_mode must be one of {sorted(ALLOWED_DOCUMENT_MODES)}")
    if case.get("appeal_ground") != "market_value":
        errors.append(
            "case.appeal_ground must be 'market_value'; this builder does not generate "
            "unequal-assessment, exemption, classification, or other non-market-value packets"
        )

    valuation_date = iso_date(case.get("valuation_date"), "case.valuation_date", errors)
    prepared_date = iso_date(case.get("prepared_date"), "case.prepared_date", errors)
    if valuation_date and prepared_date and valuation_date > prepared_date:
        errors.append("case.valuation_date cannot be after case.prepared_date")

    value_basis = case.get("value_basis")
    current_comparison: Any = None
    requested_comparison: Any = None
    notice_values: list[Any] = []
    if not isinstance(value_basis, dict):
        errors.append("case.value_basis must be an object")
    else:
        reject_unknown_fields(
            value_basis,
            VALUE_BASIS_FIELDS,
            "case.value_basis",
            errors,
        )
        for key in (
            "comparison_basis_kind",
            "comparison_value_type",
            "comparison_value_label",
            "current_comparison_value",
            "requested_comparison_value",
            "primary_notice_value_id",
            "notice_values",
            "source_ids",
        ):
            if key not in value_basis:
                errors.append(f"Missing required field: case.value_basis.{key}")
        for legacy_field in (
            "notice_value_type",
            "notice_value_label",
            "current_notice_value",
            "requested_notice_value",
            "assessment_ratio",
        ):
            if legacy_field in value_basis:
                errors.append(
                    f"case.value_basis.{legacy_field} is obsolete; represent each notice value "
                    "in case.value_basis.notice_values"
                )
        if value_basis.get("comparison_basis_kind") != "sale_comparable_market_value":
            errors.append(
                "case.value_basis.comparison_basis_kind must be "
                "'sale_comparable_market_value'"
            )
        comparison_type = value_basis.get("comparison_value_type")
        if (
            not isinstance(comparison_type, str)
            or comparison_type not in ALLOWED_COMPARISON_VALUE_TYPES
        ):
            errors.append(
                "case.value_basis.comparison_value_type must be one of "
                f"{sorted(ALLOWED_COMPARISON_VALUE_TYPES)}"
            )
        validate_text(
            value_basis.get("comparison_value_label"),
            "case.value_basis.comparison_value_label",
            errors,
            max_length=80,
        )
        current_comparison = value_basis.get("current_comparison_value")
        requested_comparison = value_basis.get("requested_comparison_value")
        for field, value in (
            ("current_comparison_value", current_comparison),
            ("requested_comparison_value", requested_comparison),
        ):
            if not is_number(value) or value <= 0:
                errors.append(f"case.value_basis.{field} must be a positive number")
        if is_number(current_comparison) and is_number(requested_comparison):
            if requested_comparison > current_comparison:
                errors.append(
                    "case.value_basis.requested_comparison_value cannot exceed "
                    "current_comparison_value"
                )
            elif requested_comparison == current_comparison:
                warnings.append(
                    "Requested comparison value equals the current comparison value; "
                    "no reduction is requested"
                )

        raw_notice_values = value_basis.get("notice_values")
        if not isinstance(raw_notice_values, list) or not raw_notice_values:
            errors.append("case.value_basis.notice_values must be a nonempty array")
        else:
            notice_values = bounded_items(
                raw_notice_values,
                "case.value_basis.notice_values",
                MAX_NOTICE_VALUES,
                errors,
            )
        node_ids: set[str] = set()
        node_map: dict[str, dict[str, Any]] = {}
        for index, node in enumerate(notice_values):
            path = f"case.value_basis.notice_values[{index}]"
            if not isinstance(node, dict):
                errors.append(f"{path} must be an object")
                continue
            reject_unknown_fields(node, NOTICE_VALUE_FIELDS, path, errors)
            for key in (
                "id",
                "value_type",
                "label",
                "authority",
                "current_value",
                "requested_value",
                "derivation",
                "source_ids",
            ):
                if key not in node:
                    errors.append(f"Missing required field: {path}.{key}")
            node_id = node.get("id")
            if not isinstance(node_id, str) or not SOURCE_ID_RE.fullmatch(node_id):
                errors.append(f"{path}.id must match {SOURCE_ID_RE.pattern}")
            elif node_id in node_ids:
                errors.append(f"Duplicate notice value id: {node_id}")
            else:
                node_ids.add(node_id)
                node_map[node_id] = node
            if (
                not isinstance(node.get("value_type"), str)
                or node.get("value_type") not in ALLOWED_NOTICE_VALUE_TYPES
            ):
                errors.append(
                    f"{path}.value_type must be one of {sorted(ALLOWED_NOTICE_VALUE_TYPES)}"
                )
            validate_text(node.get("label"), f"{path}.label", errors, max_length=80)
            validate_text(node.get("authority"), f"{path}.authority", errors, max_length=180)
            current_value = node.get("current_value")
            requested_value = node.get("requested_value")
            if not is_number(current_value) or current_value < 0:
                errors.append(f"{path}.current_value must be a nonnegative number")
            if requested_value is not None and (
                not is_number(requested_value) or requested_value < 0
            ):
                errors.append(f"{path}.requested_value must be a nonnegative number or null")
            elif (
                is_number(current_value)
                and is_number(requested_value)
                and requested_value > current_value
            ):
                errors.append(f"{path}.requested_value cannot exceed its current_value")
            derivation = node.get("derivation")
            if not isinstance(derivation, dict):
                errors.append(f"{path}.derivation must be an object")
                continue
            reject_unknown_fields(
                derivation,
                DERIVATION_FIELDS,
                f"{path}.derivation",
                errors,
            )
            for key in ("kind", "source_value_id", "factor", "description", "source_ids"):
                if key not in derivation:
                    errors.append(f"Missing required field: {path}.derivation.{key}")
            kind = derivation.get("kind")
            if not isinstance(kind, str) or kind not in ALLOWED_NOTICE_DERIVATIONS:
                errors.append(
                    f"{path}.derivation.kind must be one of "
                    f"{sorted(ALLOWED_NOTICE_DERIVATIONS)}"
                )
            validate_text(
                derivation.get("description"),
                f"{path}.derivation.description",
                errors,
                max_length=1000,
                allow_newlines=True,
            )
            factor = derivation.get("factor")
            if kind == "ratio":
                if not is_number(factor) or factor <= 0:
                    errors.append(f"{path}.derivation.factor must be positive for ratio")
                elif factor > 1:
                    errors.append(f"{path}.derivation.factor cannot exceed 1 for ratio")
            elif factor is not None:
                errors.append(f"{path}.derivation.factor must be null unless kind is ratio")

        primary_id = value_basis.get("primary_notice_value_id")
        if not isinstance(primary_id, str) or primary_id not in node_ids:
            errors.append(
                "case.value_basis.primary_notice_value_id must reference a notice value id"
            )

        source_nodes: dict[str, dict[str, Any]] = {
            "comparison_value": {
                "value_type": comparison_type,
                "current_value": current_comparison,
                "requested_value": requested_comparison,
            },
            **node_map,
        }
        graph: dict[str, str] = {}
        for index, node in enumerate(notice_values):
            if not isinstance(node, dict) or not isinstance(node.get("derivation"), dict):
                continue
            path = f"case.value_basis.notice_values[{index}]"
            source_value_id = node["derivation"].get("source_value_id")
            node_id = node.get("id")
            if not isinstance(source_value_id, str) or source_value_id not in source_nodes:
                errors.append(
                    f"{path}.derivation.source_value_id must reference comparison_value or a "
                    "notice value id"
                )
                continue
            if isinstance(node_id, str):
                graph[node_id] = source_value_id
            source_node = source_nodes[source_value_id]
            kind = node["derivation"].get("kind")
            factor = node["derivation"].get("factor")
            type_problem = derivation_type_error(
                kind,
                source_node.get("value_type"),
                node.get("value_type"),
            )
            if type_problem:
                errors.append(f"{path}.derivation is type-incompatible: {type_problem}")
            if (
                kind != "reported_only"
                and source_node.get("requested_value") is None
                and node.get("requested_value") is not None
            ):
                errors.append(
                    f"{path}.requested_value must be null because "
                    f"{source_value_id}.requested_value is null; use reported_only only for an "
                    "independently sourced value"
                )
            if kind == "same_as_source":
                for key in ("current_value", "requested_value"):
                    source_value = source_node.get(key)
                    node_value = node.get(key)
                    if source_value is None and node_value is None:
                        continue
                    if not same_number(source_value, node_value):
                        errors.append(
                            f"{path}.{key} must equal {source_value_id}.{key} for "
                            "same_as_source"
                        )
            elif kind == "ratio" and is_number(factor):
                for key in ("current_value", "requested_value"):
                    source_value = source_node.get(key)
                    node_value = node.get(key)
                    if source_value is None and node_value is None:
                        continue
                    if not is_number(source_value) or not is_number(node_value):
                        errors.append(
                            f"{path}.{key} must be numeric when ratio derivation is used"
                        )
                        continue
                    try:
                        expected = source_value * factor
                    except OverflowError:
                        errors.append(
                            f"{path}.{key} cannot be derived because the ratio arithmetic "
                            "exceeds the supported numeric range"
                        )
                        continue
                    if not is_number(expected):
                        errors.append(
                            f"{path}.{key} cannot be derived because the result exceeds "
                            f"{MAX_ABSOLUTE_NUMBER:,}"
                        )
                        continue
                    tolerance = max(2.0, expected * 0.00001)
                    if abs(node_value - expected) > tolerance:
                        errors.append(
                            f"{path}.{key} must equal {source_value_id}.{key} times the "
                            "sourced ratio, within normal rounding tolerance"
                        )
            elif isinstance(kind, str) and kind in NONINCREASING_DERIVATIONS:
                for key in ("current_value", "requested_value"):
                    source_value = source_node.get(key)
                    node_value = node.get(key)
                    if source_value is None and node_value is None:
                        continue
                    if not is_number(source_value) or not is_number(node_value):
                        continue
                    tolerance = max(2.0, abs(source_value) * 0.00001)
                    if node_value > source_value + tolerance:
                        errors.append(
                            f"{path}.{key} cannot exceed {source_value_id}.{key} for "
                            f"{kind}"
                        )

        for node_id in graph:
            seen: set[str] = set()
            cursor = node_id
            while cursor in graph:
                if cursor in seen:
                    errors.append("case.value_basis.notice_values derivations must not form a cycle")
                    break
                seen.add(cursor)
                cursor = graph[cursor]

    likely = case.get("likely_comparison_value_range")
    if not isinstance(likely, dict):
        errors.append("case.likely_comparison_value_range must be an object with low and high")
    else:
        reject_unknown_fields(
            likely,
            RANGE_FIELDS,
            "case.likely_comparison_value_range",
            errors,
        )
        low = likely.get("low")
        high = likely.get("high")
        if not is_number(low) or not is_number(high) or low <= 0 or high <= 0:
            errors.append(
                "case.likely_comparison_value_range.low and .high must be positive numbers"
            )
        elif low > high:
            errors.append("case.likely_comparison_value_range.low cannot exceed .high")
        elif is_number(current_comparison) and high > current_comparison:
            errors.append(
                "case.likely_comparison_value_range.high cannot exceed the current "
                "comparison value"
            )

    verification = case.get("verification")
    if not isinstance(verification, dict):
        errors.append("case.verification must be an object")
    else:
        reject_unknown_fields(
            verification,
            VERIFICATION_FIELDS,
            "case.verification",
            errors,
        )
        for key in (
            "official_rules_rechecked",
            "subject_facts_reconciled",
            "value_basis_reconciled",
            "comparable_sales_verified",
            "contrary_evidence_reviewed",
        ):
            if verification.get(key) is not True:
                errors.append(f"case.verification.{key} must be true after human review")
        current_as_of = iso_date(
            verification.get("official_rules_current_as_of"),
            "case.verification.official_rules_current_as_of",
            errors,
        )
        if prepared_date and current_as_of and current_as_of != prepared_date:
            errors.append(
                "case.verification.official_rules_current_as_of must equal case.prepared_date"
            )

    jurisdiction = case.get("jurisdiction")
    if isinstance(jurisdiction, dict):
        reject_unknown_fields(
            jurisdiction,
            JURISDICTION_FIELDS,
            "case.jurisdiction",
            errors,
        )
        for key in (
            "country",
            "state",
            "state_code",
            "county_or_locality",
            "route_family",
            "appeal_stage",
            "filing_authority",
            "valuation_standard",
            "filing_deadline_rule",
            "official_form_required",
            "submission_url",
            "source_ids",
            "deadline_source_ids",
        ):
            require(jurisdiction, key, "case.jurisdiction", errors)
        for key in (
            "filing_deadline",
            "official_form_name",
            "official_form_url",
            "informal_preserves_formal_deadline",
        ):
            if key not in jurisdiction:
                errors.append(f"Missing required field: case.jurisdiction.{key}")
        for key, limit, allow_newlines in (
            ("state", 80, False),
            ("state_code", 2, False),
            ("county_or_locality", 180, False),
            ("appeal_stage", 180, False),
            ("filing_authority", 180, False),
            ("valuation_standard", 500, True),
            ("filing_deadline_rule", 1000, True),
        ):
            validate_text(
                jurisdiction.get(key),
                f"case.jurisdiction.{key}",
                errors,
                max_length=limit,
                allow_newlines=allow_newlines,
            )
        if jurisdiction.get("country") != "US":
            errors.append("case.jurisdiction.country must be 'US'")
        state_code = str(jurisdiction.get("state_code", "")).upper()
        registry_path = Path(__file__).resolve().parents[1] / "references" / "us-jurisdictions.json"
        try:
            with registry_path.open(encoding="utf-8") as stream:
                state_profiles = json.load(stream)["jurisdictions"]
        except (OSError, KeyError, json.JSONDecodeError) as exc:
            errors.append(f"Could not load US jurisdiction registry: {exc}")
            state_profiles = {}
        if state_code not in state_profiles:
            errors.append("case.jurisdiction.state_code must be a supported US state or DC code")
        elif str(jurisdiction.get("state", "")).strip() != state_profiles[state_code]["name"]:
            errors.append(
                "case.jurisdiction.state must match the name in us-jurisdictions.json for "
                f"{state_code}"
            )
        route_family = jurisdiction.get("route_family")
        override = jurisdiction.get("route_override")
        if isinstance(override, dict):
            reject_unknown_fields(
                override,
                ROUTE_OVERRIDE_FIELDS,
                "case.jurisdiction.route_override",
                errors,
            )
            validate_text(
                override.get("reason"),
                "case.jurisdiction.route_override.reason",
                errors,
                max_length=1000,
                allow_newlines=True,
            )
        elif override is not None:
            errors.append("case.jurisdiction.route_override must be an object when provided")
        if not isinstance(route_family, str) or route_family not in ALLOWED_ROUTE_FAMILIES:
            errors.append(
                f"case.jurisdiction.route_family must be one of {sorted(ALLOWED_ROUTE_FAMILIES)}"
            )
        elif state_code in state_profiles:
            expected_route = state_profiles[state_code]["route_family"]
            if route_family != expected_route:
                if not isinstance(override, dict):
                    errors.append(
                        "case.jurisdiction.route_family differs from the state registry; "
                        "provide a sourced case.jurisdiction.route_override"
                    )
                else:
                    if not isinstance(override.get("source_ids"), list) or not override.get(
                        "source_ids"
                    ):
                        errors.append(
                            "case.jurisdiction.route_override.source_ids must be a nonempty array"
                        )
        filing_deadline = jurisdiction.get("filing_deadline")
        if filing_deadline == "":
            errors.append("case.jurisdiction.filing_deadline must be an ISO date or null")
        elif filing_deadline is not None:
            parsed_deadline = iso_date(
                filing_deadline, "case.jurisdiction.filing_deadline", errors
            )
            if prepared_date and parsed_deadline and parsed_deadline < prepared_date:
                errors.append(
                    "case.jurisdiction.filing_deadline is before case.prepared_date; "
                    "do not generate a packet for an expired fixed deadline"
                )
        form_required = jurisdiction.get("official_form_required")
        if not isinstance(form_required, bool):
            errors.append("case.jurisdiction.official_form_required must be true or false")
        form_name = jurisdiction.get("official_form_name")
        if form_required:
            require(jurisdiction, "official_form_name", "case.jurisdiction", errors)
            require(jurisdiction, "official_form_url", "case.jurisdiction", errors)
        if form_name is not None:
            validate_text(
                form_name,
                "case.jurisdiction.official_form_name",
                errors,
                max_length=220,
            )
        form_url = jurisdiction.get("official_form_url")
        if form_url is not None:
            validate_url(form_url, "case.jurisdiction.official_form_url", errors)
        validate_url(jurisdiction.get("submission_url"), "case.jurisdiction.submission_url", errors)
        deadline_effect = jurisdiction.get("informal_preserves_formal_deadline")
        if deadline_effect is not None and not isinstance(deadline_effect, bool):
            errors.append(
                "case.jurisdiction.informal_preserves_formal_deadline must be true, false, or null"
            )
        if document_mode == "informal_review_attachment" and deadline_effect is False:
            warnings.append(
                "Informal review does not preserve the formal filing deadline; calendar and "
                "preserve formal rights separately"
            )
        elif document_mode == "informal_review_attachment" and deadline_effect is None:
            warnings.append(
                "Informal review is not verified to preserve the formal filing deadline; "
                "calendar and preserve formal rights separately"
            )
    elif jurisdiction is not None:
        errors.append("case.jurisdiction must be an object")

    subject = case.get("property")
    residential_use: Any = None
    if isinstance(subject, dict):
        reject_unknown_fields(subject, PROPERTY_FIELDS, "case.property", errors)
        for key in (
            "property_type",
            "residential_use_verification",
            "year_built",
            "living_area_sqft",
            "bedrooms",
            "bathrooms",
        ):
            require(subject, key, "case.property", errors)
        validate_text(
            subject.get("property_type"),
            "case.property.property_type",
            errors,
            max_length=120,
        )
        residential_use = subject.get("residential_use_verification")
        if not isinstance(residential_use, dict):
            errors.append("case.property.residential_use_verification must be an object")
        else:
            reject_unknown_fields(
                residential_use,
                RESIDENTIAL_USE_FIELDS,
                "case.property.residential_use_verification",
                errors,
            )
            for key in ("status", "classification", "source_ids"):
                require(
                    residential_use,
                    key,
                    "case.property.residential_use_verification",
                    errors,
                )
            if residential_use.get("status") != "verified_residential":
                errors.append(
                    "case.property.residential_use_verification.status must be "
                    "'verified_residential'; non-residential cases are outside this builder's scope"
                )
            validate_text(
                residential_use.get("classification"),
                "case.property.residential_use_verification.classification",
                errors,
                max_length=180,
            )
        for key in ("parking", "development_or_hoa"):
            if key in subject and subject[key] is not None:
                validate_text(
                    subject[key],
                    f"case.property.{key}",
                    errors,
                    max_length=300,
                )
        if (
            not is_number(subject.get("living_area_sqft"))
            or subject.get("living_area_sqft", 0) <= 0
        ):
            errors.append("case.property.living_area_sqft must be positive")
        if not is_integer(subject.get("year_built")) or subject.get("year_built", 0) <= 0:
            errors.append("case.property.year_built must be a positive integer")
        if not is_number(subject.get("bedrooms")) or subject.get("bedrooms", -1) < 0:
            errors.append("case.property.bedrooms must be a nonnegative number")
        if not is_number(subject.get("bathrooms")) or subject.get("bathrooms", 0) <= 0:
            errors.append("case.property.bathrooms must be a positive number")
        for key in ("stories", "lot_size_sqft"):
            value = subject.get(key)
            if value is not None and (not is_number(value) or value <= 0):
                errors.append(f"case.property.{key} must be a positive number or null")
    elif subject is not None:
        errors.append("case.property must be an object")

    for key in ("argument_points", "suggested_attachments"):
        value = case.get(key, [])
        if not isinstance(value, list):
            errors.append(f"case.{key} must be an array of strings")
        else:
            value = bounded_items(value, f"case.{key}", MAX_TEXT_LIST_ITEMS, errors)
            if not all(isinstance(item, str) for item in value):
                errors.append(f"case.{key} must be an array of strings")
                continue
            for index, item in enumerate(value):
                validate_text(
                    item,
                    f"case.{key}[{index}]",
                    errors,
                    max_length=2000 if key == "argument_points" else 300,
                    allow_newlines=key == "argument_points",
                )
    declaration = case.get("declaration")
    if declaration is not None and not isinstance(declaration, str):
        errors.append("case.declaration must be a string when provided")
    elif declaration is not None:
        validate_text(
            declaration,
            "case.declaration",
            errors,
            max_length=2000,
            allow_newlines=True,
        )
    declaration_approved = case.get("declaration_owner_approved", False)
    include_signature = case.get("include_signature_block", False)
    if not isinstance(declaration_approved, bool):
        errors.append("case.declaration_owner_approved must be true or false")
    if not isinstance(include_signature, bool):
        errors.append("case.include_signature_block must be true or false")
    if declaration and declaration_approved is not True:
        errors.append(
            "case.declaration requires case.declaration_owner_approved=true after the owner "
            "approves the exact text"
        )
    if declaration_approved is True and not declaration:
        errors.append("case.declaration_owner_approved cannot be true without a declaration")
    if include_signature is True and declaration_approved is not True:
        errors.append(
            "case.include_signature_block requires an owner-approved declaration"
        )

    factors = case.get("special_factors", [])
    if not isinstance(factors, list):
        errors.append("case.special_factors must be an array")
        factors = []
    else:
        factors = bounded_items(
            factors,
            "case.special_factors",
            MAX_SPECIAL_FACTORS,
            errors,
        )

    source_ids: set[str] = set()
    source_roles: dict[str, set[str]] = {}
    for index, source in enumerate(sources):
        path = f"sources[{index}]"
        if not isinstance(source, dict):
            errors.append(f"{path} must be an object")
            continue
        reject_unknown_fields(source, ALLOWED_SOURCE_FIELDS, path, errors)
        for key in (
            "id",
            "source_kind",
            "title",
            "publisher",
            "accessed_date",
            "supports",
            "roles",
        ):
            require(source, key, path, errors)
        if "url" not in source:
            errors.append(f"Missing required field: {path}.url")
        source_id = source.get("id")
        if not isinstance(source_id, str) or not SOURCE_ID_RE.fullmatch(source_id.strip()):
            errors.append(
                f"{path}.id must contain 1-40 letters, digits, dots, underscores, or hyphens"
            )
        else:
            normalized_source_id = source_id.strip()
            if normalized_source_id in source_ids:
                errors.append(f"Duplicate source id: {normalized_source_id}")
            source_ids.add(normalized_source_id)
        source_kind = source.get("source_kind")
        if source_kind is not None and (
            not isinstance(source_kind, str) or source_kind not in ALLOWED_SOURCE_KINDS
        ):
            errors.append(
                f"{path}.source_kind must be one of {sorted(ALLOWED_SOURCE_KINDS)}"
            )
        title = source.get("title")
        publisher = source.get("publisher")
        validate_text(title, f"{path}.title", errors, max_length=300)
        validate_text(publisher, f"{path}.publisher", errors, max_length=200)
        if "url" in source:
            if source_kind == "public_url":
                validate_url(source.get("url"), f"{path}.url", errors)
            elif source_kind == "owner_attachment" and source.get("url") is not None:
                errors.append(f"{path}.url must be null for an owner_attachment source")
        accessed = iso_date(source.get("accessed_date"), f"{path}.accessed_date", errors)
        if prepared_date and accessed and accessed > prepared_date:
            errors.append(f"{path}.accessed_date cannot be after case.prepared_date")
        supports = source.get("supports")
        if not isinstance(supports, list) or not supports:
            errors.append(f"{path}.supports must be a nonempty array")
        else:
            supports = bounded_items(
                supports,
                f"{path}.supports",
                MAX_SOURCE_SUPPORTS,
                errors,
            )
            if not all(isinstance(item, str) for item in supports):
                errors.append(f"{path}.supports must contain only strings")
            for support_index, support in enumerate(supports):
                if not isinstance(support, str):
                    continue
                validate_text(
                    support,
                    f"{path}.supports[{support_index}]",
                    errors,
                    max_length=400,
                    allow_newlines=True,
                )
        roles = source.get("roles")
        normalized_roles: set[str] = set()
        if not isinstance(roles, list) or not roles:
            errors.append(f"{path}.roles must be a nonempty array")
        else:
            roles = bounded_items(roles, f"{path}.roles", len(ALLOWED_SOURCE_ROLES), errors)
            if not all(isinstance(role, str) for role in roles):
                errors.append(f"{path}.roles must contain only strings")
            normalized_roles = {role for role in roles if isinstance(role, str)}
            unsupported = sorted(normalized_roles - ALLOWED_SOURCE_ROLES)
            if unsupported:
                errors.append(f"{path}.roles contains unsupported roles: {', '.join(unsupported)}")
            if source_kind == "owner_attachment":
                private_unsupported = sorted(
                    normalized_roles - OWNER_ATTACHMENT_SOURCE_ROLES
                )
                if private_unsupported:
                    errors.append(
                        f"{path}.roles for owner_attachment may contain only "
                        f"{sorted(OWNER_ATTACHMENT_SOURCE_ROLES)}; unsupported: "
                        f"{', '.join(private_unsupported)}"
                    )
        if isinstance(source_id, str) and SOURCE_ID_RE.fullmatch(source_id.strip()):
            source_roles[source_id.strip()] = normalized_roles
        if (
            prepared_date
            and accessed
            and normalized_roles & LEGAL_SOURCE_ROLES
            and accessed != prepared_date
        ):
            errors.append(
                f"{path}.accessed_date must equal case.prepared_date for current rule sources"
            )

    validate_source_links(
        "case.subject_source_ids",
        case.get("subject_source_ids"),
        source_ids,
        errors,
        required_roles={"parcel_record"},
        source_roles=source_roles,
    )
    if isinstance(residential_use, dict):
        validate_source_links(
            "case.property.residential_use_verification.source_ids",
            residential_use.get("source_ids"),
            source_ids,
            errors,
            required_roles={"parcel_record"},
            source_roles=source_roles,
        )
    validate_source_links(
        "case.assessment_source_ids",
        case.get("assessment_source_ids"),
        source_ids,
        errors,
        required_roles={"assessment_notice"},
        source_roles=source_roles,
    )
    if isinstance(value_basis, dict):
        validate_source_links(
            "case.value_basis.source_ids",
            value_basis.get("source_ids"),
            source_ids,
            errors,
            required_roles={"assessment_notice", "valuation_rule"},
            source_roles=source_roles,
        )
        for index, node in enumerate(notice_values):
            if not isinstance(node, dict):
                continue
            path = f"case.value_basis.notice_values[{index}]"
            validate_source_links(
                f"{path}.source_ids",
                node.get("source_ids"),
                source_ids,
                errors,
                required_roles={"assessment_notice"},
                source_roles=source_roles,
            )
            derivation = node.get("derivation")
            if isinstance(derivation, dict):
                validate_source_links(
                    f"{path}.derivation.source_ids",
                    derivation.get("source_ids"),
                    source_ids,
                    errors,
                    required_roles={"valuation_rule"},
                    source_roles=source_roles,
                )
    if isinstance(jurisdiction, dict):
        validate_source_links(
            "case.jurisdiction.source_ids",
            jurisdiction.get("source_ids"),
            source_ids,
            errors,
            required_roles={"appeal_rule", "submission_rule", "valuation_rule"},
            source_roles=source_roles,
        )
        validate_source_links(
            "case.jurisdiction.deadline_source_ids",
            jurisdiction.get("deadline_source_ids"),
            source_ids,
            errors,
            required_roles={"deadline_rule"},
            source_roles=source_roles,
        )
        route_override = jurisdiction.get("route_override")
        if isinstance(route_override, dict):
            validate_source_links(
                "case.jurisdiction.route_override.source_ids",
                route_override.get("source_ids"),
                source_ids,
                errors,
                required_roles={"appeal_rule"},
                source_roles=source_roles,
            )

    if contrary_review.get("completed") is not True:
        errors.append("contrary_evidence_review.completed must be true after neutral review")
    if contrary_review.get("all_plausible_candidates_recorded") is not True:
        errors.append(
            "contrary_evidence_review.all_plausible_candidates_recorded must be true"
        )
    validate_text(
        contrary_review.get("summary"),
        "contrary_evidence_review.summary",
        errors,
        max_length=1800,
        allow_newlines=True,
    )
    if contrary_review.get("disclosure") is not None:
        validate_text(
            contrary_review.get("disclosure"),
            "contrary_evidence_review.disclosure",
            errors,
            max_length=1800,
            allow_newlines=True,
        )
    validate_source_links(
        "contrary_evidence_review.source_ids",
        contrary_review.get("source_ids"),
        source_ids,
        errors,
        required_roles={"parcel_record", "transaction_record"},
        source_roles=source_roles,
    )

    minimum = policy.get("minimum_comps", 3)
    maximum = policy.get("maximum_comps", 10)
    if not is_integer(minimum) or minimum < 1:
        errors.append("selection_policy.minimum_comps must be a positive integer")
        minimum = 3
    elif minimum > MAX_SELECTED_COMPARABLES:
        errors.append(
            f"selection_policy.minimum_comps cannot exceed {MAX_SELECTED_COMPARABLES}"
        )
        minimum = 3
    if not is_integer(maximum) or maximum < minimum:
        errors.append("selection_policy.maximum_comps must be an integer >= minimum_comps")
        maximum = 10
    elif maximum > MAX_SELECTED_COMPARABLES:
        errors.append(
            f"selection_policy.maximum_comps cannot exceed {MAX_SELECTED_COMPARABLES}"
        )
        maximum = MAX_SELECTED_COMPARABLES
    if len(comps) < minimum:
        errors.append(f"At least {minimum} selected comparables are required; found {len(comps)}")
    if len(comps) > maximum:
        errors.append(f"No more than {maximum} selected comparables are allowed; found {len(comps)}")

    legal_window = policy.get("legal_sale_window")
    window_start: date | None = None
    window_end: date | None = None
    max_post_days: int | None = None
    if isinstance(legal_window, dict):
        reject_unknown_fields(
            legal_window,
            LEGAL_SALE_WINDOW_FIELDS,
            "selection_policy.legal_sale_window",
            errors,
        )
        for key in ("start_date", "end_date", "basis", "source_ids"):
            require(legal_window, key, "selection_policy.legal_sale_window", errors)
        window_start = iso_date(
            legal_window.get("start_date"),
            "selection_policy.legal_sale_window.start_date",
            errors,
        )
        window_end = iso_date(
            legal_window.get("end_date"),
            "selection_policy.legal_sale_window.end_date",
            errors,
        )
        if window_start and window_end and window_start > window_end:
            errors.append(
                "selection_policy.legal_sale_window.start_date cannot exceed end_date"
            )
        if prepared_date and window_end and window_end > prepared_date:
            errors.append(
                "selection_policy.legal_sale_window.end_date cannot be after case.prepared_date"
            )
        validate_text(
            legal_window.get("basis"),
            "selection_policy.legal_sale_window.basis",
            errors,
            max_length=1200,
            allow_newlines=True,
        )
        validate_source_links(
            "selection_policy.legal_sale_window.source_ids",
            legal_window.get("source_ids"),
            source_ids,
            errors,
            required_roles={"sale_window_rule"},
            source_roles=source_roles,
        )
        if "max_post_valuation_days" in policy:
            errors.append(
                "selection_policy.max_post_valuation_days is a legacy v1 field; use only the "
                "sourced legal_sale_window"
            )
    elif legal_window is not None:
        errors.append("selection_policy.legal_sale_window must be an object")
    else:
        errors.append("selection_policy.legal_sale_window is required")

    strict_match = policy.get("strict_bed_bath_match", True)
    strict_property_type = policy.get("strict_property_type_match", True)
    exclude_high = policy.get("exclude_above_current_comparison_value", True)
    allow_ranges = policy.get("allow_provisional_range_prices", False)
    for key, value in (
        ("strict_bed_bath_match", strict_match),
        ("strict_property_type_match", strict_property_type),
        ("exclude_above_current_comparison_value", exclude_high),
        ("allow_provisional_range_prices", allow_ranges),
    ):
        if not isinstance(value, bool):
            errors.append(f"selection_policy.{key} must be true or false")
    strict_match = strict_match if isinstance(strict_match, bool) else True
    strict_property_type = (
        strict_property_type if isinstance(strict_property_type, bool) else True
    )
    exclude_high = exclude_high if isinstance(exclude_high, bool) else True
    allow_ranges = allow_ranges if isinstance(allow_ranges, bool) else False
    seen_transactions: dict[str, dict[str, Any]] = {}
    seen_transaction_fingerprints: dict[tuple[Any, ...], str] = {}

    for index, comp in enumerate(comps):
        path = f"comparables[{index}]"
        if not isinstance(comp, dict):
            errors.append(f"{path} must be an object")
            continue
        reject_unknown_fields(comp, SELECTED_COMPARABLE_FIELDS, path, errors)
        for key in (
            "address",
            "apn",
            "transaction_id",
            "sale_date",
            "sale_price",
            "price_source_kind",
            "property_type",
            "bedrooms",
            "bathrooms",
            "living_area_sqft",
            "arm_length_status",
            "relevance",
            "source_ids",
        ):
            require(comp, key, path, errors)

        for key, limit, allow_newlines in (
            ("address", 300, False),
            ("apn", 100, False),
            ("transaction_id", 160, False),
            ("property_type", 120, False),
            ("relevance", 1600, True),
        ):
            validate_text(
                comp.get(key),
                f"{path}.{key}",
                errors,
                max_length=limit,
                allow_newlines=allow_newlines,
            )

        sale_date = iso_date(comp.get("sale_date"), f"{path}.sale_date", errors)
        if valuation_date and sale_date:
            if prepared_date and sale_date > prepared_date:
                errors.append(f"{path}.sale_date cannot be after case.prepared_date")
            if window_start and sale_date < window_start:
                errors.append(
                    f"{path} sold {sale_date.isoformat()}, before the sourced legal sale "
                    f"window beginning {window_start.isoformat()}"
                )
            if window_end and sale_date > window_end:
                errors.append(
                    f"{path} sold {sale_date.isoformat()}, after the sourced legal sale "
                    f"window ending {window_end.isoformat()}"
                )
            if (
                max_post_days is not None
                and sale_date > valuation_date + timedelta(days=max_post_days)
            ):
                errors.append(
                    f"{path} sold {sale_date.isoformat()}, beyond the allowed "
                    f"{max_post_days} days after the valuation date"
                )
            if sale_date < valuation_date - timedelta(days=730):
                warnings.append(f"{path} sold more than two years before the valuation date")

        price = comp.get("sale_price")
        if not is_number(price) or price <= 0:
            errors.append(f"{path}.sale_price must be a positive number")
        elif whole_dollar_amount(price) is None:
            errors.append(f"{path}.sale_price must be stated in whole dollars")
        elif exclude_high and is_number(current_comparison) and price > current_comparison:
            errors.append(
                f"{path}.sale_price {money(price)} exceeds the current comparison value "
                f"{money(current_comparison)} while "
                "exclude_above_current_comparison_value is enabled"
            )

        area = comp.get("living_area_sqft")
        if not is_number(area) or area <= 0:
            errors.append(f"{path}.living_area_sqft must be a positive number")
        if not is_number(comp.get("bedrooms")) or comp.get("bedrooms", -1) < 0:
            errors.append(f"{path}.bedrooms must be a nonnegative number")
        if not is_number(comp.get("bathrooms")) or comp.get("bathrooms", 0) <= 0:
            errors.append(f"{path}.bathrooms must be a positive number")
        year_built = comp.get("year_built")
        if year_built is not None and (not is_integer(year_built) or year_built <= 0):
            errors.append(f"{path}.year_built must be a positive integer when provided")
        distance = comp.get("distance_miles")
        if distance is not None and (not is_number(distance) or distance < 0):
            errors.append(f"{path}.distance_miles must be a nonnegative number when provided")
        same_development = comp.get("same_development")
        if same_development is not None and not isinstance(same_development, bool):
            errors.append(f"{path}.same_development must be true or false when provided")

        price_kind = comp.get("price_source_kind")
        if not isinstance(price_kind, str) or price_kind not in ALLOWED_PRICE_KINDS:
            errors.append(f"{path}.price_source_kind must be one of {sorted(ALLOWED_PRICE_KINDS)}")
        if price_kind == "range_lower_bound":
            reported_range = comp.get("reported_price_range")
            if not isinstance(reported_range, dict):
                errors.append(f"{path}.reported_price_range is required for a range lower bound")
            else:
                reject_unknown_fields(
                    reported_range,
                    RANGE_FIELDS,
                    f"{path}.reported_price_range",
                    errors,
                )
                range_low = reported_range.get("low")
                range_high = reported_range.get("high")
                if not is_number(range_low) or not is_number(range_high):
                    errors.append(f"{path}.reported_price_range.low and .high must be numbers")
                else:
                    if (
                        whole_dollar_amount(range_low) is None
                        or whole_dollar_amount(range_high) is None
                    ):
                        errors.append(
                            f"{path}.reported_price_range.low and .high must be stated in "
                            "whole dollars"
                        )
                    if range_low >= range_high:
                        errors.append(f"{path}.reported_price_range.low must be below .high")
                    elif is_number(price) and price != range_low:
                        errors.append(f"{path}.sale_price must equal reported_price_range.low")
            if not allow_ranges:
                errors.append(
                    f"{path} uses a provisional range lower bound; verify exact closed price or "
                    "enable allow_provisional_range_prices with an accurate disclosure"
                )
        elif "reported_price_range" in comp:
            reported_range = comp.get("reported_price_range")
            if isinstance(reported_range, dict):
                reject_unknown_fields(
                    reported_range,
                    RANGE_FIELDS,
                    f"{path}.reported_price_range",
                    errors,
                )
            errors.append(
                f"{path}.reported_price_range is allowed only for a range lower bound"
            )

        arm_length = comp.get("arm_length_status")
        if not isinstance(arm_length, str) or arm_length not in ALLOWED_ARM_LENGTH:
            errors.append(f"{path}.arm_length_status must be one of {sorted(ALLOWED_ARM_LENGTH)}")
        elif arm_length == "not_arm_length":
            errors.append(f"{path} cannot be selected because it is not an arm's-length transfer")
        elif arm_length == "unknown":
            errors.append(
                f"{path}.arm_length_status must be verified or likely for selected evidence"
            )

        if strict_match and isinstance(subject, dict):
            if not same_number(comp.get("bedrooms"), subject.get("bedrooms")):
                errors.append(f"{path}.bedrooms does not match the subject under strict matching")
            if not same_number(comp.get("bathrooms"), subject.get("bathrooms")):
                errors.append(f"{path}.bathrooms does not match the subject under strict matching")

        if strict_property_type and isinstance(subject, dict):
            comp_type = str(comp.get("property_type", "")).strip().casefold()
            subject_type = str(subject.get("property_type", "")).strip().casefold()
            if comp_type and subject_type and comp_type != subject_type:
                errors.append(
                    f"{path}.property_type does not match the subject under strict matching"
                )

        validate_source_links(
            f"{path}.source_ids",
            comp.get("source_ids"),
            source_ids,
            errors,
            required_roles={"parcel_record", "transaction_record"},
            source_roles=source_roles,
        )
        transaction_id = comp.get("transaction_id")
        if isinstance(transaction_id, str) and transaction_id.strip():
            normalized_transaction_id = transaction_id.strip()
            if normalized_transaction_id in seen_transactions:
                errors.append(
                    f"Duplicate selected comparable transaction_id: "
                    f"{normalized_transaction_id}"
                )
            else:
                fingerprint = transaction_fingerprint(comp)
                if fingerprint is not None and fingerprint in seen_transaction_fingerprints:
                    errors.append(
                        f"{path} duplicates an earlier selected transaction under a "
                        "different transaction_id"
                    )
                seen_transactions[normalized_transaction_id] = comp
                if fingerprint is not None:
                    seen_transaction_fingerprints.setdefault(
                        fingerprint,
                        normalized_transaction_id,
                    )

    for index, factor in enumerate(factors):
        path = f"case.special_factors[{index}]"
        if not isinstance(factor, dict):
            errors.append(f"{path} must be an object")
            continue
        reject_unknown_fields(factor, SPECIAL_FACTOR_FIELDS, path, errors)
        for key in ("title", "facts", "market_effect", "source_ids"):
            require(factor, key, path, errors)
        validate_text(factor.get("title"), f"{path}.title", errors, max_length=180)
        validate_text(
            factor.get("facts"),
            f"{path}.facts",
            errors,
            max_length=2400,
            allow_newlines=True,
        )
        validate_text(
            factor.get("market_effect"),
            f"{path}.market_effect",
            errors,
            max_length=2400,
            allow_newlines=True,
        )
        validate_source_links(
            f"{path}.source_ids",
            factor.get("source_ids"),
            source_ids,
            errors,
            required_roles={"marketability_evidence"},
            source_roles=source_roles,
        )

    for index, comp in enumerate(rejected):
        path = f"rejected_comparables[{index}]"
        if not isinstance(comp, dict):
            errors.append(f"{path} must be an object")
            continue
        reject_unknown_fields(comp, REJECTED_COMPARABLE_FIELDS, path, errors)
        for key in (
            "address",
            "apn",
            "transaction_id",
            "sale_date",
            "sale_price",
            "price_source_kind",
            "property_type",
            "bedrooms",
            "bathrooms",
            "living_area_sqft",
            "arm_length_status",
            "relevance",
            "valuation_status",
            "reasons",
            "relevance_review",
            "materially_contrary",
            "source_ids",
        ):
            require(comp, key, path, errors)
        validate_text(comp.get("address"), f"{path}.address", errors, max_length=300)
        validate_text(comp.get("apn"), f"{path}.apn", errors, max_length=100)
        validate_text(
            comp.get("transaction_id"),
            f"{path}.transaction_id",
            errors,
            max_length=160,
        )
        validate_text(
            comp.get("property_type"),
            f"{path}.property_type",
            errors,
            max_length=120,
        )
        validate_text(
            comp.get("relevance"),
            f"{path}.relevance",
            errors,
            max_length=1600,
            allow_newlines=True,
        )
        validate_text(
            comp.get("relevance_review"),
            f"{path}.relevance_review",
            errors,
            max_length=1600,
            allow_newlines=True,
        )
        valuation_status = comp.get("valuation_status")
        if (
            not isinstance(valuation_status, str)
            or valuation_status not in ALLOWED_REJECTED_STATUSES
        ):
            errors.append(
                f"{path}.valuation_status must be one of {sorted(ALLOWED_REJECTED_STATUSES)}"
            )
        reasons = require(comp, "reasons", path, errors)
        if isinstance(reasons, list):
            reasons = bounded_items(
                reasons,
                f"{path}.reasons",
                MAX_REJECTION_REASONS,
                errors,
            )
        if reasons is not None and (
            not isinstance(reasons, list)
            or not reasons
            or not all(
                isinstance(reason, str) and reason in ALLOWED_REJECTION_REASONS
                for reason in reasons
            )
        ):
            errors.append(
                f"{path}.reasons must be a nonempty array using only "
                f"{sorted(ALLOWED_REJECTION_REASONS)}"
            )
        reason_set = (
            {reason for reason in reasons if isinstance(reason, str)}
            if isinstance(reasons, list)
            else set()
        )
        if valuation_status == "valuation_eligible_omitted" and (
            reason_set & INADMISSIBLE_REJECTION_REASONS
        ):
            errors.append(
                f"{path} cannot be valuation eligible when its reasons identify an "
                "inadmissible transaction"
            )
        if valuation_status == "research_only_inadmissible" and not (
            reason_set & INADMISSIBLE_REJECTION_REASONS
        ):
            errors.append(
                f"{path} must include an inadmissible transaction reason when its status is "
                "research_only_inadmissible"
            )
        materially_contrary = comp.get("materially_contrary")
        if not isinstance(materially_contrary, bool):
            errors.append(f"{path}.materially_contrary must be true or false")
        elif valuation_status == "research_only_inadmissible" and materially_contrary:
            errors.append(f"{path}.materially_contrary must be false for research-only evidence")

        transaction_id = comp.get("transaction_id")
        normalized_transaction_id = (
            transaction_id.strip()
            if isinstance(transaction_id, str) and transaction_id.strip()
            else ""
        )
        duplicate_of_transaction_id = comp.get("duplicate_of_transaction_id")
        controlled_duplicate = False
        if "duplicate_record" in reason_set:
            validated_duplicate_id = validate_text(
                duplicate_of_transaction_id,
                f"{path}.duplicate_of_transaction_id",
                errors,
                max_length=160,
            )
            normalized_duplicate_id = (
                validated_duplicate_id.strip()
                if validated_duplicate_id is not None
                else ""
            )
            prior_transaction = seen_transactions.get(normalized_duplicate_id)
            if normalized_duplicate_id and prior_transaction is None:
                errors.append(
                    f"{path}.duplicate_of_transaction_id must reference an earlier selected "
                    "or rejected transaction_id"
                )
            elif normalized_duplicate_id and (
                normalized_transaction_id != normalized_duplicate_id
            ):
                errors.append(
                    f"{path}.transaction_id must equal duplicate_of_transaction_id when "
                    "duplicate_record is used"
                )
            elif prior_transaction is not None and not transactions_match(
                comp, prior_transaction
            ):
                errors.append(
                    f"{path} must exactly match the earlier transaction's address, APN, sale "
                    "date, price kind, price, and reported range when duplicate_record is used"
                )
            elif normalized_duplicate_id:
                controlled_duplicate = True
        elif duplicate_of_transaction_id is not None:
            errors.append(
                f"{path}.duplicate_of_transaction_id is allowed only when reasons includes "
                "duplicate_record"
            )
        if normalized_transaction_id in seen_transactions and not controlled_duplicate:
            errors.append(
                f"Duplicate candidate comparable transaction_id: {normalized_transaction_id}"
            )
        if normalized_transaction_id and not controlled_duplicate:
            fingerprint = transaction_fingerprint(comp)
            prior_fingerprint_id = (
                seen_transaction_fingerprints.get(fingerprint)
                if fingerprint is not None
                else None
            )
            if prior_fingerprint_id is not None:
                errors.append(
                    f"{path} duplicates an earlier transaction under a different "
                    "transaction_id; use duplicate_record and reference the earlier id"
                )
            seen_transactions.setdefault(normalized_transaction_id, comp)
            if fingerprint is not None:
                seen_transaction_fingerprints.setdefault(
                    fingerprint,
                    normalized_transaction_id,
                )

        rejected_sale_date = iso_date(comp.get("sale_date"), f"{path}.sale_date", errors)
        if rejected_sale_date:
            if prepared_date and rejected_sale_date > prepared_date:
                errors.append(f"{path}.sale_date cannot be after case.prepared_date")
            if (
                valuation_status == "valuation_eligible_omitted"
                and window_start
                and rejected_sale_date < window_start
            ):
                errors.append(
                    f"{path} sold before the sourced legal sale window beginning "
                    f"{window_start.isoformat()}"
                )
            if (
                valuation_status == "valuation_eligible_omitted"
                and window_end
                and rejected_sale_date > window_end
            ):
                errors.append(
                    f"{path} sold after the sourced legal sale window ending "
                    f"{window_end.isoformat()}"
                )
        rejected_price = comp.get("sale_price")
        if not is_number(rejected_price) or rejected_price <= 0:
            errors.append(f"{path}.sale_price must be a positive number")
        elif whole_dollar_amount(rejected_price) is None:
            errors.append(f"{path}.sale_price must be stated in whole dollars")
        price_kind = comp.get("price_source_kind")
        if not isinstance(price_kind, str) or price_kind not in ALLOWED_PRICE_KINDS:
            errors.append(f"{path}.price_source_kind must be one of {sorted(ALLOWED_PRICE_KINDS)}")
        if price_kind == "range_lower_bound":
            reported_range = comp.get("reported_price_range")
            if not isinstance(reported_range, dict):
                errors.append(f"{path}.reported_price_range is required for a range lower bound")
            else:
                reject_unknown_fields(
                    reported_range,
                    RANGE_FIELDS,
                    f"{path}.reported_price_range",
                    errors,
                )
                range_low = reported_range.get("low")
                range_high = reported_range.get("high")
                if not is_number(range_low) or not is_number(range_high):
                    errors.append(f"{path}.reported_price_range.low and .high must be numbers")
                else:
                    if (
                        whole_dollar_amount(range_low) is None
                        or whole_dollar_amount(range_high) is None
                    ):
                        errors.append(
                            f"{path}.reported_price_range.low and .high must be stated in "
                            "whole dollars"
                        )
                    if range_low >= range_high:
                        errors.append(f"{path}.reported_price_range.low must be below .high")
                    elif is_number(rejected_price) and rejected_price != range_low:
                        errors.append(f"{path}.sale_price must equal reported_price_range.low")
            if not allow_ranges:
                errors.append(
                    f"{path} uses a provisional range lower bound; verify exact closed price or "
                    "enable allow_provisional_range_prices with an accurate disclosure"
                )
        elif "reported_price_range" in comp:
            reported_range = comp.get("reported_price_range")
            if isinstance(reported_range, dict):
                reject_unknown_fields(
                    reported_range,
                    RANGE_FIELDS,
                    f"{path}.reported_price_range",
                    errors,
                )
            errors.append(
                f"{path}.reported_price_range is allowed only for a range lower bound"
            )
        if not is_number(comp.get("bedrooms")) or comp.get("bedrooms", -1) < 0:
            errors.append(f"{path}.bedrooms must be a nonnegative number")
        if not is_number(comp.get("bathrooms")) or comp.get("bathrooms", 0) <= 0:
            errors.append(f"{path}.bathrooms must be a positive number")
        if (
            not is_number(comp.get("living_area_sqft"))
            or comp.get("living_area_sqft", 0) <= 0
        ):
            errors.append(f"{path}.living_area_sqft must be a positive number")
        year_built = comp.get("year_built")
        if year_built is not None and (not is_integer(year_built) or year_built <= 0):
            errors.append(f"{path}.year_built must be a positive integer when provided")
        distance = comp.get("distance_miles")
        if distance is not None and (not is_number(distance) or distance < 0):
            errors.append(f"{path}.distance_miles must be a nonnegative number when provided")
        same_development = comp.get("same_development")
        if same_development is not None and not isinstance(same_development, bool):
            errors.append(f"{path}.same_development must be true or false when provided")
        arm_length = comp.get("arm_length_status")
        if not isinstance(arm_length, str) or arm_length not in ALLOWED_ARM_LENGTH:
            errors.append(f"{path}.arm_length_status must be one of {sorted(ALLOWED_ARM_LENGTH)}")
        elif valuation_status == "valuation_eligible_omitted" and arm_length not in {
            "verified",
            "likely",
        }:
            errors.append(
                f"{path}.arm_length_status must be verified or likely for valuation-eligible "
                "omitted evidence"
            )
        linked_source_ids = validate_source_links(
            f"{path}.source_ids",
            comp.get("source_ids"),
            source_ids,
            errors,
            required_roles=(
                {"parcel_record", "transaction_record"}
                if valuation_status == "valuation_eligible_omitted"
                else {"parcel_record"}
            ),
            source_roles=source_roles,
        )
        linked_roles = set().union(
            *(source_roles.get(source_id, set()) for source_id in linked_source_ids)
        )
        if (
            reason_set & TRANSACTION_RECORD_REJECTION_REASONS
            and "transaction_record" not in linked_roles
        ):
            errors.append(
                f"{path}.source_ids must include a transaction_record source for reasons: "
                f"{', '.join(sorted(reason_set & TRANSACTION_RECORD_REJECTION_REASONS))}"
            )
        if reason_set & {"non_arm_length", "non_market_transfer"} and arm_length != (
            "not_arm_length"
        ):
            errors.append(
                f"{path}.arm_length_status must be not_arm_length when reasons includes "
                "non_arm_length or non_market_transfer"
            )
        if arm_length == "not_arm_length" and not (
            reason_set & {"non_arm_length", "non_market_transfer"}
        ):
            errors.append(
                f"{path}.reasons must identify non_arm_length or non_market_transfer when "
                "arm_length_status is not_arm_length"
            )
        outside_window = bool(
            rejected_sale_date
            and (
                (window_start is not None and rejected_sale_date < window_start)
                or (window_end is not None and rejected_sale_date > window_end)
            )
        )
        if "outside_legal_sale_window" in reason_set and not outside_window:
            errors.append(
                f"{path}.sale_date must fall outside the sourced legal sale window when "
                "reasons includes outside_legal_sale_window"
            )
        if "unverified_transaction" in reason_set:
            if arm_length != "unknown":
                errors.append(
                    f"{path}.arm_length_status must be unknown when reasons includes "
                    "unverified_transaction"
                )
            if price_kind != "range_lower_bound":
                errors.append(
                    f"{path}.price_source_kind must be range_lower_bound when reasons includes "
                    "unverified_transaction"
                )
            if "transaction_record" in linked_roles:
                errors.append(
                    f"{path}.source_ids must not claim a transaction_record when reasons "
                    "includes unverified_transaction"
                )

    eligible_rejected = [
        comp
        for comp in rejected
        if isinstance(comp, dict)
        and comp.get("valuation_status") == "valuation_eligible_omitted"
    ]
    material_contrary = [
        comp for comp in eligible_rejected if comp.get("materially_contrary") is True
    ]
    try:
        best_selected_score = max(relevance_score(comp, case) for comp in comps)
    except (AttributeError, KeyError, OverflowError, TypeError, ValueError, ZeroDivisionError):
        best_selected_score = None
    if best_selected_score is not None:
        for index, comp in enumerate(rejected):
            if not isinstance(comp, dict):
                continue
            if comp.get("valuation_status") != "valuation_eligible_omitted":
                continue
            try:
                rejected_score = relevance_score(comp, case)
            except (
                AttributeError,
                KeyError,
                OverflowError,
                TypeError,
                ValueError,
                ZeroDivisionError,
            ):
                continue
            if rejected_score >= best_selected_score:
                if comp.get("materially_contrary") is not True:
                    errors.append(
                        f"rejected_comparables[{index}].materially_contrary must be true because "
                        "its deterministic relevance score is at least the best selected score"
                    )
                if comp not in material_contrary:
                    material_contrary.append(comp)
    if material_contrary and not contrary_review.get("disclosure"):
        errors.append(
            "contrary_evidence_review.disclosure is required when a rejected candidate is "
            "materially contrary"
        )

    if comps and is_number(requested_comparison):
        comp_prices = [
            comp.get("sale_price")
            for comp in comps
            if isinstance(comp, dict) and is_number(comp.get("sale_price"))
        ]
        if comp_prices:
            floor = min(comp_prices)
            if requested_comparison < floor * 0.95 and not case.get("special_factors"):
                warnings.append(
                    "Requested value is more than 5% below the lowest selected sale without a "
                    "documented special factor"
                )

    return errors.reported(), warnings


def relevance_score(comp: dict[str, Any], case: dict[str, Any]) -> float:
    subject = case["property"]
    score = 0.0
    if str(comp.get("property_type", "")).strip().casefold() == str(
        subject.get("property_type", "")
    ).strip().casefold():
        score += 4
    else:
        score -= 5
    if comp.get("same_development"):
        score += 5
    if same_number(comp.get("bedrooms"), subject.get("bedrooms")):
        score += 3
    if same_number(comp.get("bathrooms"), subject.get("bathrooms")):
        score += 3
    area_delta = abs(comp["living_area_sqft"] - subject["living_area_sqft"]) / subject[
        "living_area_sqft"
    ]
    if area_delta <= 0.02:
        score += 5
    elif area_delta <= 0.05:
        score += 4
    elif area_delta <= 0.10:
        score += 2
    elif area_delta <= 0.15:
        score += 1
    valuation = date.fromisoformat(case["valuation_date"])
    sold = date.fromisoformat(comp["sale_date"])
    days = abs((sold - valuation).days)
    if days <= 45:
        score += 4
    elif days <= 90:
        score += 3
    elif days <= 180:
        score += 2
    elif days <= 365:
        score += 1
    if comp.get("arm_length_status") == "verified":
        score += 2
    elif comp.get("arm_length_status") == "likely":
        score += 1
    distance = comp.get("distance_miles")
    if isinstance(distance, (int, float)):
        if distance <= 0.25:
            score += 2
        elif distance <= 0.75:
            score += 1
    return score


def candidate_pool(data: dict[str, Any]) -> list[dict[str, Any]]:
    eligible_omitted = [
        comp
        for comp in data.get("rejected_comparables", [])
        if comp.get("valuation_status") == "valuation_eligible_omitted"
    ]
    return [*data["comparables"], *eligible_omitted]


def candidate_identity_sort_key(comp: dict[str, Any]) -> tuple[str, ...]:
    values = tuple(
        str(comp.get(field, "")).strip()
        for field in ("transaction_id", "sale_date", "address", "apn")
    )
    return (*tuple(value.casefold() for value in values), *values)


def candidate_price_interval(comp: dict[str, Any]) -> tuple[float, float]:
    if comp["price_source_kind"] == "range_lower_bound":
        reported = comp["reported_price_range"]
        return float(reported["low"]), float(reported["high"])
    price = float(comp["sale_price"])
    return price, price


def material_adverse_candidates(data: dict[str, Any]) -> list[dict[str, Any]]:
    rejected = [
        comp
        for comp in data.get("rejected_comparables", [])
        if comp.get("valuation_status") == "valuation_eligible_omitted"
    ]
    selected = data["comparables"]
    best_selected_score = max(relevance_score(comp, data["case"]) for comp in selected)
    return [
        comp
        for comp in rejected
        if comp.get("materially_contrary") is True
        or relevance_score(comp, data["case"]) >= best_selected_score
    ]


def selected_summary(data: dict[str, Any]) -> dict[str, Any]:
    case = data["case"]
    comps = candidate_pool(data)
    strongest_score = max(relevance_score(comp, case) for comp in comps)
    strongest_candidates = sorted(
        (
            comp
            for comp in comps
            if relevance_score(comp, case) == strongest_score
        ),
        key=candidate_identity_sort_key,
    )
    intervals = [candidate_price_interval(comp) for comp in comps]
    exact_prices = [
        comp["sale_price"]
        for comp in comps
        if comp["price_source_kind"] == "exact_closed_price"
    ]
    areas = [comp["living_area_sqft"] for comp in comps]
    larger = [comp for comp in comps if comp["living_area_sqft"] > case["property"]["living_area_sqft"]]
    current_value = case["value_basis"]["current_comparison_value"]
    return {
        "strongest": strongest_candidates[0],
        "strongest_candidates": strongest_candidates,
        "strongest_score": strongest_score,
        "candidate_count": len(comps),
        "researched_count": len(data["comparables"]) + len(data.get("rejected_comparables", [])),
        "inadmissible_count": sum(
            comp.get("valuation_status") == "research_only_inadmissible"
            for comp in data.get("rejected_comparables", [])
        ),
        "selected_count": len(data["comparables"]),
        "price_low": min(low for low, _high in intervals),
        "price_high": max(high for _low, high in intervals),
        "price_median": median(exact_prices) if len(exact_prices) >= 2 else None,
        "area_low": min(areas),
        "area_high": max(areas),
        "larger": larger,
        "exact_count": len(exact_prices),
        "below_count": sum(high < current_value for _low, high in intervals),
        "at_or_above_count": sum(low >= current_value for low, _high in intervals),
        "overlap_count": sum(low < current_value <= high for low, high in intervals),
    }


def comparison_label(case: dict[str, Any]) -> str:
    return str(case["value_basis"]["comparison_value_label"])


def primary_notice_value(case: dict[str, Any]) -> dict[str, Any]:
    basis = case["value_basis"]
    primary_id = basis["primary_notice_value_id"]
    return next(node for node in basis["notice_values"] if node["id"] == primary_id)


def price_evidence_text(comp: dict[str, Any]) -> str:
    if comp["price_source_kind"] == "exact_closed_price":
        return money(comp["sale_price"])
    reported = comp["reported_price_range"]
    return (
        f"reported range {money(reported['low'])} to {money(reported['high'])} "
        "(exact consideration unverified)"
    )


def price_per_sqft_evidence_text(comp: dict[str, Any]) -> str:
    area = comp["living_area_sqft"]
    if comp["price_source_kind"] == "exact_closed_price":
        return f"{money(comp['sale_price'] / area)}/sq ft"
    reported = comp["reported_price_range"]
    return (
        f"{money(reported['low'] / area)} to {money(reported['high'] / area)}/sq ft "
        "(reported range)"
    )


def advocacy_table_intro(case: dict[str, Any]) -> str:
    return (
        "The following transactions are the advocacy-table evidence identified for the "
        f"{display_date(case['valuation_date'])} valuation date."
    )


def rejection_reason_text(reasons: list[str]) -> str:
    return ", ".join(reason.replace("_", " ") for reason in reasons)


def strongest_sale_sentence(comp: dict[str, Any]) -> str:
    if comp["price_source_kind"] == "exact_closed_price":
        return (
            f"It closed for {money(comp['sale_price'])} on "
            f"{display_date(comp['sale_date'])}."
        )
    reported_range = comp["reported_price_range"]
    return (
        "Its transaction was reported with a price range of "
        f"{money(reported_range['low'])} to {money(reported_range['high'])} for its "
        f"{display_date(comp['sale_date'])} transaction; exact recorded consideration was "
        "not verified."
    )


def co_best_summary_sentence(comps: list[dict[str, Any]]) -> str:
    details = []
    for comp in comps:
        if comp["price_source_kind"] == "exact_closed_price":
            price_clause = f"closed for {money(comp['sale_price'])}"
        else:
            price_clause = price_evidence_text(comp)
        details.append(
            f"{comp['address']} (APN {comp['apn']}, transaction ID "
            f"{comp['transaction_id']}) {price_clause} on {display_date(comp['sale_date'])}"
        )
    return (
        f"The {len(comps)} co-best direct candidates by the deterministic physical and temporal "
        f"relevance score are " + "; ".join(details) + "."
    )


def request_summary_paragraphs(data: dict[str, Any]) -> list[str]:
    case = data["case"]
    subject = case["property"]
    basis = case["value_basis"]
    stats = selected_summary(data)
    strongest = stats["strongest"]
    strongest_candidates = stats["strongest_candidates"]
    primary_notice = primary_notice_value(case)
    inadmissible_clause = (
        "1 research-only transaction is"
        if stats["inadmissible_count"] == 1
        else f"{stats['inadmissible_count']} research-only transactions are"
    )
    notice_sentence = (
        f"The notice reports {primary_notice['label'].lower()} of "
        f"{money(primary_notice['current_value'])}. "
    )
    if (
        primary_notice["value_type"] == basis["comparison_value_type"]
        and same_number(primary_notice["current_value"], basis["current_comparison_value"])
    ):
        notice_sentence = ""
    strongest_sentence = (
        (
            "The strongest direct candidate by the deterministic physical and temporal "
            f"relevance score is {strongest['address']}. "
            f"{strongest_sale_sentence(strongest)}"
        )
        if len(strongest_candidates) == 1
        else co_best_summary_sentence(strongest_candidates)
    )
    paragraphs = [
        (
            f"This attachment requests review of APN {case['apn']} through the "
            f"{case['appeal_type']} process. {notice_sentence}For comparison with market sales, "
            f"the current {comparison_label(case).lower()} is "
            f"{money(basis['current_comparison_value'])}; the requested "
            f"{comparison_label(case).lower()} as of {display_date(case['valuation_date'])} is "
            f"{money(basis['requested_comparison_value'])}."
        ),
        (
            f"The subject is {property_phrase(subject)} built in {subject['year_built']}, "
            f"with approximately {number(subject['living_area_sqft'])} square feet, "
            f"{number(subject['bedrooms'])} bedrooms, and {number(subject['bathrooms'])} bathrooms."
        ),
        (
            f"The research ledger contains {stats['researched_count']} transactions. "
            f"The admissible neutral candidate pool contains {stats['candidate_count']}, of "
            f"which {stats['selected_count']} appear in the advocacy table; "
            f"{inadmissible_clause} excluded from all "
            "valuation arithmetic and anchoring. "
            f"Their verified price intervals span {money(stats['price_low'])} to "
            f"{money(stats['price_high'])}. {strongest_sentence}"
        ),
        case["valuation_rationale"],
    ]
    return paragraphs


def analysis_paragraphs(data: dict[str, Any]) -> list[str]:
    case = data["case"]
    subject = case["property"]
    basis = case["value_basis"]
    stats = selected_summary(data)
    strongest_candidates = stats["strongest_candidates"]
    below_count = stats["below_count"]
    at_or_above_count = stats["at_or_above_count"]
    overlap_count = stats["overlap_count"]
    comp_count = stats["candidate_count"]
    if below_count == comp_count:
        distribution_sentence = (
            f"All {comp_count} neutral-pool price intervals are entirely below the current "
            f"{comparison_label(case).lower()} of {money(basis['current_comparison_value'])}."
        )
    elif at_or_above_count == comp_count:
        distribution_sentence = (
            f"None of the {comp_count} neutral-pool price intervals is below the current "
            f"{comparison_label(case).lower()} of {money(basis['current_comparison_value'])}."
        )
    else:
        below_verb = "is" if below_count == 1 else "are"
        above_verb = "is" if at_or_above_count == 1 else "are"
        cross_verb = "crosses" if overlap_count == 1 else "cross"
        distribution_sentence = (
            f"Of {comp_count} neutral-pool price intervals, {below_count} {below_verb} entirely "
            f"below, {at_or_above_count} {above_verb} at or above, and {overlap_count} "
            f"{cross_verb} the current "
            f"{comparison_label(case).lower()} of {money(basis['current_comparison_value'])}."
        )
    if stats["price_median"] is None:
        central_sentence = (
            f"Only {stats['exact_count']} exact closed price is available, so provisional range "
            "endpoints are excluded and no central point estimate is reported."
            if stats["exact_count"] == 1
            else "No exact closed prices are available, so provisional range endpoints are excluded and no central point estimate is reported."
        )
    else:
        central_sentence = (
            f"The median of the {stats['exact_count']} exact closed prices is approximately "
            f"{money(stats['price_median'])}, before considering subject-specific differences."
        )
    direct_descriptions = []
    for comp in strongest_candidates:
        if comp["price_source_kind"] == "exact_closed_price":
            price_clause = f"closed at {money(comp['sale_price'])}"
        else:
            price_clause = f"has {price_evidence_text(comp)}"
        direct_descriptions.append(
            f"{comp['address']} (APN {comp['apn']}, transaction ID "
            f"{comp['transaction_id']}). It has {number(comp['bedrooms'])} bedrooms and "
            f"{number(comp['bathrooms'])} bathrooms, contains approximately "
            f"{number(comp['living_area_sqft'])} square feet, and {price_clause}. "
            f"{comp['relevance']}"
        )
    direct_intro = (
        "The most directly comparable sale is "
        if len(direct_descriptions) == 1
        else "The most directly comparable candidates are tied by the deterministic score: "
    )
    paragraphs = [
        direct_intro + " ".join(direct_descriptions),
        f"{distribution_sentence} {central_sentence}",
    ]
    if stats["larger"]:
        larger_intervals = [candidate_price_interval(comp) for comp in stats["larger"]]
        paragraphs.append(
            f"{len(stats['larger'])} neutral-pool candidates are larger than the subject's "
            f"{number(subject['living_area_sqft'])} square feet; their verified price intervals "
            f"span {money(min(low for low, _high in larger_intervals))} to "
            f"{money(max(high for _low, high in larger_intervals))}. These "
            "larger transactions do not support placing the smaller subject above their indicated "
            "range without a documented superior feature."
        )
    paragraphs.extend(case.get("argument_points", []))
    return paragraphs


def conclusion_paragraphs(data: dict[str, Any]) -> list[str]:
    case = data["case"]
    basis = case["value_basis"]
    likely = case["likely_comparison_value_range"]
    stats = selected_summary(data)
    if stats["below_count"] == stats["candidate_count"]:
        evidence_clause = (
            "Every neutral-pool price interval is entirely below the current value."
        )
    elif stats["at_or_above_count"] == stats["candidate_count"]:
        evidence_clause = (
            "The neutral-pool price evidence is not below the current value; any requested "
            "reduction therefore depends on the documented physical, temporal, or marketability "
            "differences described in this attachment."
        )
    else:
        evidence_clause = (
            "The neutral candidate pool contains mixed or overlapping price evidence. The "
            "requested value therefore depends on the documented relevance and marketability "
            "differences rather than an assertion that all candidates are below the current value."
        )
    requested_nodes = [
        node
        for node in basis["notice_values"]
        if node.get("requested_value") is not None
        and (
            node["value_type"] != basis["comparison_value_type"]
            or not same_number(node["requested_value"], basis["requested_comparison_value"])
        )
    ]
    notice_clause = "".join(
        f" The corresponding requested {node['label'].lower()} for {node['authority']} is "
        f"{money(node['requested_value'])}."
        for node in requested_nodes
    )
    if stats["exact_count"] < 2:
        point_clause = (
            " Because fewer than two exact closed prices are available, the requested point value "
            "is provisional and is not presented as a median or other central sale-price estimate."
        )
    else:
        point_clause = ""
    return [
        (
            f"{evidence_clause} The requested {comparison_label(case).lower()} is "
            f"{money(basis['requested_comparison_value'])} as of "
            f"{display_date(case['valuation_date'])}.{point_clause}{notice_clause} Any dependent assessed or "
            "taxable value should be recalculated by the filing authority under the applicable "
            "jurisdictional rules."
        ),
        (
            f"Based on the verified comparable evidence, a reasonable estimated "
            f"{comparison_label(case).lower()} review outcome is approximately "
            f"{money(likely['low'])} to {money(likely['high'])}. This range is an evidence-based "
            "estimate, not a guarantee of the authority's determination."
        ),
    ]


def contrary_review_paragraphs(data: dict[str, Any]) -> list[str]:
    review = data["contrary_evidence_review"]
    paragraphs = [
        f"{review['summary']} Sources: {source_refs(review['source_ids'])}."
    ]
    if review.get("disclosure"):
        paragraphs.append(review["disclosure"])
    for comp in material_adverse_candidates(data):
        paragraphs.append(
            f"Disclosed omitted candidate: {comp['address']} (APN {comp['apn']}), "
            f"transaction ID {comp['transaction_id']}, {display_date(comp['sale_date'])}, "
            f"{price_evidence_text(comp)}. "
            f"Relevance score {relevance_score(comp, data['case']):g}; presentation exclusion: "
            f"{rejection_reason_text(comp['reasons'])}. {comp['relevance_review']} Sources: "
            f"{source_refs(comp['source_ids'])}."
        )
    return paragraphs


def property_phrase(subject: dict[str, Any]) -> str:
    value = str(subject["property_type"]).strip()
    article = "an" if value[:1].lower() in "aeiou" else "a"
    return f"{article} {value}"


def source_refs(source_ids: list[str]) -> str:
    return ", ".join(f"[{source_id}]" for source_id in source_ids)


def source_card_data(source: dict[str, Any]) -> dict[str, str]:
    is_owner_attachment = source["source_kind"] == "owner_attachment"
    return {
        "heading": f"[{source['id']}] {source['title']}",
        "publisher": source["publisher"],
        "accessed": display_date(source["accessed_date"]),
        "date_label": "Reviewed" if is_owner_attachment else "Accessed",
        "locator": OWNER_ATTACHMENT_DISPLAY if is_owner_attachment else source["url"],
        "source_kind": source["source_kind"],
        "supports": "; ".join(source["supports"]),
    }


def md_cell(value: Any) -> str:
    return md_escape(value).replace("  \n", " ")


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(md_cell(value) for value in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(value) for value in row) + " |")
    return lines


def subject_rows(case: dict[str, Any]) -> list[list[Any]]:
    subject = case["property"]
    basis = case["value_basis"]
    rows: list[list[Any]] = [
        ["Address", case["property_address"]],
        ["APN", case["apn"]],
        ["Property type", subject["property_type"]],
        [
            "Residential-use classification",
            subject["residential_use_verification"]["classification"],
        ],
        [
            "Residential-use sources",
            source_refs(subject["residential_use_verification"]["source_ids"]),
        ],
        ["Year built", subject["year_built"]],
        ["Living area", f"{number(subject['living_area_sqft'])} sq ft"],
        ["Bedrooms / bathrooms", f"{number(subject['bedrooms'])} / {number(subject['bathrooms'])}"],
        ["Verification sources", source_refs(case["subject_source_ids"])],
    ]
    if case.get("owner_name"):
        rows.insert(2, ["Owner", case["owner_name"]])
    for key, label in (
        ("stories", "Stories"),
        ("lot_size_sqft", "Lot size"),
        ("parking", "Parking"),
        ("development_or_hoa", "Development / HOA"),
    ):
        value = subject.get(key)
        if value is not None and value != "":
            suffix = " sq ft" if key == "lot_size_sqft" else ""
            rows.append([label, f"{number(value) if isinstance(value, (int, float)) else value}{suffix}"])
    rows.extend(
        [
            [
                f"Current {comparison_label(case).lower()}",
                money(basis["current_comparison_value"]),
            ],
            [
                f"Requested {comparison_label(case).lower()}",
                money(basis["requested_comparison_value"]),
            ],
        ]
    )
    for node in basis["notice_values"]:
        rows.append(
            [
                f"Current {node['label'].lower()} ({node['authority']})",
                money(node["current_value"]),
            ]
        )
        if node.get("requested_value") is not None:
            rows.append(
                [
                    f"Requested {node['label'].lower()} ({node['authority']})",
                    money(node["requested_value"]),
                ]
            )
        derivation = node["derivation"]
        rows.append(
            [
                f"{node['label']} relationship",
                f"{derivation['description']} Sources: {source_refs(derivation['source_ids'])}",
            ]
        )
    return rows


def filing_rows(case: dict[str, Any]) -> list[list[Any]]:
    jurisdiction = case["jurisdiction"]
    rule_source_ids = list(
        dict.fromkeys(jurisdiction["source_ids"] + jurisdiction["deadline_source_ids"])
    )
    form_name = jurisdiction.get("official_form_name")
    form_display = form_name or (
        "Separate official form not required for this stage"
        if jurisdiction.get("official_form_required") is False
        else "Not yet verified"
    )
    rows: list[list[Any]] = [
        ["Jurisdiction", f"{jurisdiction['county_or_locality']}, {jurisdiction['state']}"],
        ["Document mode", case["document_mode"].replace("_", " ").title()],
        ["Appeal stage", jurisdiction["appeal_stage"]],
        ["Filing authority", jurisdiction["filing_authority"]],
        ["Valuation standard", jurisdiction["valuation_standard"]],
        ["Filing deadline", display_deadline(jurisdiction)],
        ["Deadline rule", jurisdiction["filing_deadline_rule"]],
        ["Official form", form_display],
        ["Submission page", jurisdiction["submission_url"]],
        [
            "Rule sources",
            source_refs(rule_source_ids),
        ],
    ]
    if jurisdiction.get("official_form_url"):
        rows.insert(8, ["Official form URL", jurisdiction["official_form_url"]])
    return rows


def filing_note_paragraphs(case: dict[str, Any]) -> list[str]:
    jurisdiction = case["jurisdiction"]
    notes = [
        (
            f"This document is a supporting evidence attachment for the "
            f"{jurisdiction['appeal_stage']} stage."
        )
    ]
    if jurisdiction["official_form_required"]:
        notes.append(
            f"It does not replace the required official form "
            f"{jurisdiction['official_form_name']}; file that form and this attachment through "
            f"the official channel by the applicable deadline."
        )
    if case["document_mode"] == "informal_review_attachment":
        preserves = jurisdiction.get("informal_preserves_formal_deadline")
        if preserves is False:
            notes.append(
                "The informal review does not preserve the separate formal appeal deadline."
            )
        elif preserves is None:
            notes.append(
                "The informal review has not been verified to preserve the separate formal "
                "appeal deadline."
            )
    notes.append(
        "Continue to follow the authority's tax-payment instructions; this attachment does not "
        "itself suspend payment obligations."
    )
    return notes


def comparable_rows(data: dict[str, Any]) -> list[list[Any]]:
    rows = []
    for comp in data["comparables"]:
        rows.append(
            [
                comp["address"],
                comp["apn"],
                comp["transaction_id"],
                display_date(comp["sale_date"]),
                price_evidence_text(comp),
                f"{number(comp['bedrooms'])} / {number(comp['bathrooms'])}",
                number(comp["living_area_sqft"]),
                price_per_sqft_evidence_text(comp),
                comp["relevance"],
                source_refs(comp["source_ids"]),
            ]
        )
    return rows


def build_markdown(data: dict[str, Any]) -> str:
    case = data["case"]
    basis = case["value_basis"]
    primary_notice = primary_notice_value(case)
    likely = case["likely_comparison_value_range"]
    lines: list[str] = [
        f"# {md_escape(case['review_title'])}",
        "",
        f"**Property:** {md_escape(case['property_address'])}  ",
        f"**APN:** {md_escape(case['apn'])}  ",
        f"**Assessment year:** {md_escape(case['assessment_year'])}  ",
        f"**Valuation date:** {display_date(case['valuation_date'])}  ",
        (
            f"**Current {md_escape(comparison_label(case).lower())}:** "
            f"{money(basis['current_comparison_value'])}  "
        ),
        (
            f"**Requested {md_escape(comparison_label(case).lower())}:** "
            f"{money(basis['requested_comparison_value'])}  "
        ),
        (
            f"**Current {md_escape(primary_notice['label'].lower())}:** "
            f"{money(primary_notice['current_value'])}  "
        ),
        (
            f"**Estimated likely {md_escape(comparison_label(case).lower())} range:** "
            f"{money(likely['low'])} to {money(likely['high'])}  "
        ),
        f"**Prepared:** {display_date(case['prepared_date'])}",
        "",
        "## Filing Information",
        "",
    ]
    lines.extend(markdown_table(["Item", "Verified detail"], filing_rows(case)))
    lines.extend(["", "### Filing Note", ""])
    for paragraph in filing_note_paragraphs(case):
        lines.extend([md_escape(paragraph), ""])
    lines.extend([
        "## Request Summary",
        "",
    ])
    for paragraph in request_summary_paragraphs(data):
        lines.extend([md_escape(paragraph), ""])

    lines.extend(["## Subject Property", ""])
    lines.extend(markdown_table(["Item", "Verified detail"], subject_rows(case)))
    lines.extend(
        [
            "",
            "## Comparable Sales",
            "",
            advocacy_table_intro(case),
            "",
        ]
    )
    lines.extend(
        markdown_table(
            [
                "Address",
                "APN",
                "Transaction ID",
                "Sale date",
                "Price evidence",
                "Beds / baths",
                "Sq ft",
                "Price / sq ft",
                "Relevance",
                "Sources",
            ],
            comparable_rows(data),
        )
    )
    lines.extend(["", "## Sales Comparison Analysis", ""])
    for paragraph in analysis_paragraphs(data):
        lines.extend([md_escape(paragraph), ""])

    lines.extend(["## Contrary Evidence Review", ""])
    for paragraph in contrary_review_paragraphs(data):
        lines.extend([md_escape(paragraph), ""])

    factors = case.get("special_factors", [])
    if factors:
        lines.extend(["## Documented Marketability Factors", ""])
        for factor in factors:
            lines.extend(
                [
                    f"### {md_escape(factor['title'])}",
                    "",
                    md_escape(factor["facts"]),
                    "",
                    md_escape(factor["market_effect"]),
                    "",
                    f"Sources: {source_refs(factor['source_ids'])}",
                    "",
                ]
            )

    lines.extend(["## Requested Value Conclusion", ""])
    for paragraph in conclusion_paragraphs(data):
        lines.extend([md_escape(paragraph), ""])

    attachments = case.get("suggested_attachments", [])
    if attachments:
        lines.extend(["## Suggested Attachments", ""])
        for index, attachment in enumerate(attachments, start=1):
            lines.append(f"{index}. {md_escape(attachment)}")
        lines.append("")

    lines.extend(["## Evidence Sources", ""])
    for source in data["sources"]:
        card = source_card_data(source)
        locator = (
            f"<{card['locator']}>"
            if card["source_kind"] == "public_url"
            else md_escape(card["locator"])
        )
        lines.append(
            f"- **{md_escape(card['heading'])}**, {md_escape(card['publisher'])}. "
            f"{locator}. {card['date_label']} {card['accessed']}. "
            f"Supports: {md_escape(card['supports'])}."
        )
    if case.get("declaration") and case.get("declaration_owner_approved") is True:
        lines.extend(["", "## Declaration", "", md_escape(case["declaration"]), ""])
        if case.get("include_signature_block") is True:
            lines.extend(
                [
                    "**Owner signature:** ________________________________________  ",
                    "**Date:** ____________________",
                    "",
                ]
            )
    else:
        lines.append("")
    return "\n".join(lines)


def render_pdf(data: dict[str, Any], output_path: Path) -> None:
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.lib.pagesizes import LETTER
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.pdfbase import pdfmetrics
        from reportlab.platypus import (
            KeepTogether,
            LongTable,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError as exc:
        requirements_lock = Path(__file__).with_name("requirements.lock")
        raise RuntimeError(
            "PDF generation requires the bundled locked dependencies. Install them with "
            f"'python3 -m pip install --require-hashes -r {requirements_lock}'."
        ) from exc

    case = data["case"]
    base_font = "Helvetica"
    bold_font = "Helvetica-Bold"
    base14_fonts = tuple(pdfmetrics.getFont(name) for name in (base_font, bold_font))

    def base14_supports(character: str) -> bool:
        if character in "\n\r\t":
            return True
        try:
            encoded = character.encode("cp1252")
        except UnicodeEncodeError:
            return False
        if len(encoded) != 1:
            return False
        code = encoded[0]
        return all(
            (glyph_name := font.encoding.vector[code]) is not None
            and glyph_name in font.face.glyphNames
            for font in base14_fonts
        )

    def text_values(value: Any) -> list[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, dict):
            return [item for child in value.values() for item in text_values(child)]
        if isinstance(value, list):
            return [item for child in value for item in text_values(child)]
        return []

    unsupported = sorted(
        {
            character
            for value in text_values(data)
            for character in value
            if not base14_supports(character)
        },
        key=ord,
    )
    if unsupported:
        shown = unsupported[:12]
        details = ", ".join(f"U+{ord(character):04X}" for character in shown)
        if len(unsupported) > len(shown):
            details += f", and {len(unsupported) - len(shown)} more"
        raise RuntimeError(
            "PDF Base 14 font coverage is unavailable for these characters: "
            f"{details}. Use the official English spelling where one exists, or generate "
            "Markdown only with --no-pdf."
        )

    def pdf_markup(value: Any) -> str:
        return html.escape(str(value)).replace("\n", "<br/>")
    styles = getSampleStyleSheet()
    navy = colors.HexColor("#17324D")
    teal = colors.HexColor("#167D86")
    ink = colors.HexColor("#17212B")
    muted = colors.HexColor("#52606D")
    line = colors.HexColor("#C9D2DA")
    wash = colors.HexColor("#EEF4F6")
    light = colors.HexColor("#F7F9FA")

    title_style = ParagraphStyle(
        "AppealTitle",
        parent=styles["Title"],
        fontName=bold_font,
        fontSize=17,
        leading=20,
        textColor=navy,
        alignment=TA_LEFT,
        spaceAfter=9,
    )
    subtitle_style = ParagraphStyle(
        "AppealSubtitle",
        parent=styles["Normal"],
        fontName=base_font,
        fontSize=9,
        leading=12,
        textColor=muted,
        spaceAfter=8,
    )
    heading_style = ParagraphStyle(
        "AppealHeading",
        parent=styles["Heading2"],
        fontName=bold_font,
        fontSize=11,
        leading=14,
        textColor=navy,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
    )
    subheading_style = ParagraphStyle(
        "AppealSubheading",
        parent=styles["Heading3"],
        fontName=bold_font,
        fontSize=9.5,
        leading=12,
        textColor=teal,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "AppealBody",
        parent=styles["BodyText"],
        fontName=base_font,
        fontSize=9,
        leading=12.2,
        textColor=ink,
        spaceAfter=6,
        allowWidows=0,
        allowOrphans=0,
        splitLongWords=True,
    )
    small_style = ParagraphStyle(
        "AppealSmall",
        parent=body_style,
        fontSize=7.2,
        leading=9.2,
        spaceAfter=2,
        splitLongWords=True,
    )
    source_style = ParagraphStyle(
        "AppealSource",
        parent=small_style,
        fontSize=6.5,
        leading=7.8,
        spaceAfter=0,
        splitLongWords=True,
    )
    table_header_style = ParagraphStyle(
        "AppealTableHeader",
        parent=small_style,
        fontName=bold_font,
        textColor=colors.white,
        alignment=TA_CENTER,
    )
    table_cell_style = ParagraphStyle(
        "AppealTableCell",
        parent=small_style,
        fontSize=7,
        leading=8.5,
        textColor=ink,
    )
    meta_label_style = ParagraphStyle(
        "AppealMetaLabel",
        parent=small_style,
        fontName=bold_font,
        fontSize=7.5,
        leading=9.5,
        textColor=muted,
    )
    meta_value_style = ParagraphStyle(
        "AppealMetaValue",
        parent=small_style,
        fontName=base_font,
        fontSize=8.2,
        leading=10,
        textColor=ink,
    )

    def paragraph(value: Any, style: ParagraphStyle = body_style) -> Paragraph:
        return Paragraph(pdf_markup(value), style)

    def heading(value: str) -> Paragraph:
        return Paragraph(pdf_markup(value), heading_style)

    def make_table(
        rows: list[list[Any]],
        widths: list[float],
        header: bool = False,
        compact: bool = False,
    ) -> Table:
        rendered: list[list[Paragraph]] = []
        for row_index, row in enumerate(rows):
            rendered.append(
                [
                    paragraph(
                        cell,
                        table_header_style if header and row_index == 0 else table_cell_style,
                    )
                    for cell in row
                ]
            )
        table_class = LongTable if header else Table
        table = table_class(rendered, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
        commands: list[tuple[Any, ...]] = [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.35, line),
            ("LEFTPADDING", (0, 0), (-1, -1), 4 if not compact else 3),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4 if not compact else 3),
            ("TOPPADDING", (0, 0), (-1, -1), 4 if not compact else 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4 if not compact else 3),
        ]
        if header:
            commands.extend(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), navy),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, light]),
                ]
            )
        else:
            commands.extend(
                [
                    ("BACKGROUND", (0, 0), (0, -1), wash),
                    ("ROWBACKGROUNDS", (1, 0), (-1, -1), [colors.white, light]),
                ]
            )
        table.setStyle(TableStyle(commands))
        return table

    output_path.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(output_path),
        pagesize=LETTER,
        rightMargin=0.52 * inch,
        leftMargin=0.52 * inch,
        topMargin=0.58 * inch,
        bottomMargin=0.58 * inch,
        title=case["review_title"],
        author="Property owner",
        subject=f"Assessment review for {case['property_address']}",
        invariant=1,
    )

    story: list[Any] = [
        paragraph(case["review_title"], title_style),
        paragraph(case["property_address"], subtitle_style),
    ]

    basis = case["value_basis"]
    primary_notice = primary_notice_value(case)
    likely = case["likely_comparison_value_range"]
    metadata = [
        [paragraph("APN", meta_label_style), paragraph(case["apn"], meta_value_style),
         paragraph("Assessment year", meta_label_style), paragraph(case["assessment_year"], meta_value_style)],
        [paragraph("Valuation date", meta_label_style), paragraph(display_date(case["valuation_date"]), meta_value_style),
         paragraph("Prepared", meta_label_style), paragraph(display_date(case["prepared_date"]), meta_value_style)],
        [paragraph(f"Current {comparison_label(case).lower()}", meta_label_style), paragraph(money(basis["current_comparison_value"]), meta_value_style),
         paragraph(f"Requested {comparison_label(case).lower()}", meta_label_style), paragraph(money(basis["requested_comparison_value"]), meta_value_style)],
        [paragraph(f"Current {primary_notice['label'].lower()}", meta_label_style), paragraph(money(primary_notice["current_value"]), meta_value_style),
         paragraph("Likely review range", meta_label_style), paragraph(f"{money(likely['low'])} to {money(likely['high'])}", meta_value_style)],
        [paragraph("Value-basis source", meta_label_style), paragraph(source_refs(basis["source_ids"]), meta_value_style),
         paragraph("Filing authority", meta_label_style), paragraph(case["jurisdiction"]["filing_authority"], meta_value_style)],
        [paragraph("Appeal stage", meta_label_style), paragraph(case["jurisdiction"]["appeal_stage"], meta_value_style),
         paragraph("Filing deadline", meta_label_style), paragraph(display_deadline(case["jurisdiction"]), meta_value_style)],
    ]
    metadata_table = Table(metadata, colWidths=[0.95 * inch, 2.25 * inch, 0.95 * inch, 2.3 * inch])
    metadata_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, line),
                ("BACKGROUND", (0, 0), (0, -1), wash),
                ("BACKGROUND", (2, 0), (2, -1), wash),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.extend([metadata_table, Spacer(1, 4), heading("Filing Information")])
    story.append(make_table(filing_rows(case), [1.62 * inch, 5.4 * inch]))
    story.append(heading("Filing Note"))
    story.extend(paragraph(item) for item in filing_note_paragraphs(case))
    story.append(heading("Request Summary"))
    story.extend(paragraph(item) for item in request_summary_paragraphs(data))

    story.append(heading("Subject Property"))
    story.append(make_table(subject_rows(case), [1.62 * inch, 5.4 * inch]))

    story.extend(
        [
            heading("Comparable Sales"),
            paragraph(advocacy_table_intro(case)),
        ]
    )
    comp_headers = [
        "Address / APN",
        "Sale date",
        "Price evidence",
        "Beds / baths",
        "Sq ft",
        "Price / sq ft",
    ]
    comp_pdf_rows: list[list[Any]] = [comp_headers]
    for comp in data["comparables"]:
        comp_pdf_rows.append(
            [
                (
                    f"{comp['address']}\nAPN {comp['apn']}\nTransaction ID "
                    f"{comp['transaction_id']}\nSources {source_refs(comp['source_ids'])}"
                ),
                display_date(comp["sale_date"]),
                price_evidence_text(comp),
                f"{number(comp['bedrooms'])} / {number(comp['bathrooms'])}",
                number(comp["living_area_sqft"]),
                price_per_sqft_evidence_text(comp),
            ]
        )
    story.append(
        make_table(
            comp_pdf_rows,
            [
                2.25 * inch,
                0.9 * inch,
                1.2 * inch,
                0.65 * inch,
                0.57 * inch,
                1.45 * inch,
            ],
            header=True,
            compact=True,
        )
    )
    story.append(Spacer(1, 4))
    for index, comp in enumerate(data["comparables"], start=1):
        story.append(paragraph(f"{index}. {comp['address']}: {comp['relevance']}", small_style))
    story.append(heading("Sales Comparison Analysis"))
    story.extend(paragraph(item) for item in analysis_paragraphs(data))

    story.append(heading("Contrary Evidence Review"))
    story.extend(paragraph(item) for item in contrary_review_paragraphs(data))

    factors = case.get("special_factors", [])
    if factors:
        for index, factor in enumerate(factors):
            factor_block = [
                paragraph(factor["title"], subheading_style),
                paragraph(factor["facts"]),
                paragraph(factor["market_effect"]),
                paragraph(f"Sources: {source_refs(factor['source_ids'])}", small_style),
            ]
            if index == 0:
                factor_block.insert(0, heading("Documented Marketability Factors"))
            story.append(KeepTogether(factor_block))

    story.append(heading("Requested Value Conclusion"))
    story.extend(paragraph(item) for item in conclusion_paragraphs(data))

    attachments = case.get("suggested_attachments", [])
    if attachments:
        story.append(heading("Suggested Attachments"))
        for index, attachment in enumerate(attachments, start=1):
            story.append(paragraph(f"{index}. {attachment}"))

    source_cards: list[Paragraph] = []
    for source in data["sources"]:
        card = source_card_data(source)
        source_text = (
            f"{card['heading']} | {card['publisher']} | "
            f"{card['date_label']} {card['accessed']}\n"
            f"{card['locator']}\nSupports: {card['supports']}"
        )
        source_cards.append(paragraph(source_text, source_style))
    source_rows: list[list[Paragraph]] = []
    for index in range(0, len(source_cards), 2):
        row = source_cards[index : index + 2]
        if len(row) == 1:
            row.append(paragraph("", source_style))
        source_rows.append(row)
    source_table = Table(source_rows, colWidths=[3.46 * inch, 3.46 * inch], hAlign="LEFT")
    source_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.35, line),
                ("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, light]),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    source_and_declaration: list[Any] = [heading("Evidence Sources"), source_table]
    if case.get("declaration") and case.get("declaration_owner_approved") is True:
        source_and_declaration.extend(
            [heading("Declaration"), paragraph(case["declaration"])]
        )
    if case.get("include_signature_block") is True:
        source_and_declaration.extend(
            [
                Spacer(1, 12),
                make_table(
                    [["Owner signature", ""], ["Date", ""]],
                    [1.2 * inch, 5.82 * inch],
                    compact=True,
                ),
            ]
        )
    if len(data["sources"]) <= 8:
        story.append(KeepTogether(source_and_declaration))
    else:
        story.extend(source_and_declaration)

    def page_decor(canvas: Any, doc: Any) -> None:
        canvas.saveState()
        width, _height = LETTER
        canvas.setStrokeColor(line)
        canvas.setLineWidth(0.4)
        canvas.line(0.52 * inch, 0.42 * inch, width - 0.52 * inch, 0.42 * inch)
        canvas.setFillColor(muted)
        canvas.setFont(base_font, 7)
        footer_address = case["property_address"]
        if len(footer_address) > 80:
            footer_address = footer_address[:77] + "..."
        footer_style = ParagraphStyle(
            "AppealFooter",
            parent=small_style,
            fontSize=7,
            leading=8,
            textColor=muted,
        )
        footer = Paragraph(pdf_markup(footer_address), footer_style)
        footer.wrapOn(canvas, 5.6 * inch, 0.2 * inch)
        footer.drawOn(canvas, 0.52 * inch, 0.20 * inch)
        canvas.drawRightString(width - 0.52 * inch, 0.25 * inch, f"Page {doc.page}")
        canvas.restoreState()

    document.build(story, onFirstPage=page_decor, onLaterPages=page_decor)


def commit_staged_outputs(
    staged_outputs: list[tuple[Path, Path]],
    staging_dir: Path,
    *,
    force: bool = False,
) -> None:
    backups: dict[Path, Path] = {}
    installed: list[Path] = []
    try:
        if force:
            for _staged, destination in staged_outputs:
                if destination.exists():
                    backup = staging_dir / f"backup-{len(backups)}-{destination.name}"
                    os.replace(destination, backup)
                    backups[destination] = backup
            for staged, destination in staged_outputs:
                os.replace(staged, destination)
                installed.append(destination)
        else:
            for staged, destination in staged_outputs:
                os.link(staged, destination)
                installed.append(destination)
    except OSError:
        for destination in reversed(installed):
            try:
                destination.unlink(missing_ok=True)
            except OSError:
                pass
        for destination, backup in backups.items():
            if backup.exists():
                os.replace(backup, destination)
        raise


def write_packet_outputs(
    data: dict[str, Any],
    output_dir: Path,
    basename: str,
    *,
    no_pdf: bool,
    force: bool = False,
) -> list[Path]:
    if output_dir.is_symlink():
        raise RuntimeError(f"Refusing symbolic-link output directory: {output_dir}")
    created_output_dir = not output_dir.exists()
    output_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    if created_output_dir:
        output_dir.chmod(0o700)
    if not output_dir.is_dir():
        raise RuntimeError(f"Output path is not a directory: {output_dir}")
    markdown_path = output_dir / f"{basename}.md"
    pdf_path = output_dir / f"{basename}.pdf"
    destinations = [markdown_path] if no_pdf else [markdown_path, pdf_path]
    for destination in (markdown_path, pdf_path):
        if destination.is_symlink():
            raise RuntimeError(f"Refusing to replace symbolic-link output path: {destination}")
        if destination.exists() and not destination.is_file():
            raise RuntimeError(
                f"Refusing to replace non-file output path: {destination}"
            )
        if no_pdf and destination == pdf_path and destination.exists():
            raise RuntimeError(
                f"Refusing Markdown-only generation while sibling PDF exists: {destination}"
            )
        if destination in destinations and destination.exists() and not force:
            raise RuntimeError(
                f"Output already exists: {destination}; pass --force only after verifying it "
                "belongs to this case"
            )
    with tempfile.TemporaryDirectory(prefix=".appeal-build-", dir=output_dir) as temp:
        staging_dir = Path(temp)
        staged_markdown = staging_dir / markdown_path.name
        staged_markdown.write_text(build_markdown(data), encoding="utf-8")
        staged_markdown.chmod(0o600)
        staged_outputs = [(staged_markdown, markdown_path)]
        if not no_pdf:
            staged_pdf = staging_dir / pdf_path.name
            render_pdf(data, staged_pdf)
            if not staged_pdf.is_file() or not staged_pdf.read_bytes().startswith(b"%PDF-"):
                raise RuntimeError("PDF generation did not produce a valid PDF file")
            staged_pdf.chmod(0o600)
            staged_outputs.append((staged_pdf, pdf_path))
        commit_staged_outputs(staged_outputs, staging_dir, force=force)
    return [destination for _staged, destination in staged_outputs]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate property-tax appeal data and generate matching Markdown and PDF files."
    )
    parser.add_argument("case_json", type=Path, help="Path to the structured case JSON")
    parser.add_argument("--output-dir", type=Path, help="Directory for final Markdown and PDF")
    parser.add_argument("--basename", help="Output basename without extension")
    parser.add_argument("--validate-only", action="store_true", help="Validate without writing files")
    parser.add_argument("--no-pdf", action="store_true", help="Generate Markdown only")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing regular output file after verifying it belongs to this case",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        data = load_case_json(args.case_json)
    except FileNotFoundError:
        print(f"ERROR: Case file not found: {args.case_json}", file=sys.stderr)
        return 2
    except CaseJsonLimitError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except DuplicateJsonKeyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"ERROR: Invalid JSON numeric value: {exc}", file=sys.stderr)
        return 2
    except UnicodeDecodeError:
        print("ERROR: Case file must be valid UTF-8 JSON", file=sys.stderr)
        return 2
    except RecursionError:
        print("ERROR: Case JSON is nested too deeply to parse safely", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: Unable to read case file: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate_case(data)
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    print(
        f"VALID: {len(data['comparables'])} selected comparables, "
        f"{len(data.get('rejected_comparables', []))} rejected candidates, "
        f"{len(data['sources'])} sources."
    )
    if args.validate_only:
        return 0

    output_dir = args.output_dir or args.case_json.parent
    basename = args.basename or slugify(
        f"{data['case']['property_address']} {data['case']['appeal_type']}"
    )
    if not re.fullmatch(r"[A-Za-z0-9._-]+", basename):
        print("ERROR: --basename may contain only letters, digits, dots, underscores, and hyphens", file=sys.stderr)
        return 2

    try:
        symlink_component = first_existing_symlink_component(output_dir)
        if symlink_component is not None:
            raise RuntimeError(
                f"Refusing output path with symbolic-link component: {symlink_component}"
            )
        written_paths = write_packet_outputs(
            data,
            output_dir,
            basename,
            no_pdf=args.no_pdf,
            force=args.force,
        )
    except Exception as exc:  # noqa: BLE001 - keep the CLI boundary traceback-free.
        print(f"ERROR: Output generation failed: {exc}", file=sys.stderr)
        return 3
    for path in written_paths:
        print(f"WROTE: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
