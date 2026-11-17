#!/usr/bin/env python3
"""Validate compact public gameplay research without importing it at runtime."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

_IDENTIFIER = re.compile(r"^[a-z][a-z0-9_.-]*$")
_SOURCE_TYPES = {"official", "wiki", "guide", "community"}
_CONFIDENCE = {"low", "medium", "high"}
_VOLATILITY = {"low", "medium", "high"}
_CATEGORIES = {"mechanic", "strategy", "reward-hypothesis", "safety"}
_STATUSES = {"unverified", "runtime-verified", "rejected"}


def _mapping(value: object, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or any(not isinstance(key, str) for key in value):
        raise ValueError(f"{path} must be an object with string keys")
    return value


def _sequence(value: object, path: str) -> Sequence[Any]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        raise ValueError(f"{path} must be an array")
    return value


def _exact(value: Mapping[str, Any], allowed: set[str], path: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ValueError(f"{path} contains unexpected fields: {unknown}")


def _identifier(value: object, path: str) -> str:
    if not isinstance(value, str) or _IDENTIFIER.fullmatch(value) is None:
        raise ValueError(f"{path} must be a public identifier")
    return value


def _text(value: object, path: str, *, maximum: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f"{path} must contain 1 to {maximum} characters")
    return value


def _timestamp(value: object, path: str) -> None:
    text = _text(value, path, maximum=40)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{path} must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ValueError(f"{path} must include a timezone")


def _public_url(value: object, path: str) -> str:
    text = _text(value, path, maximum=2048)
    parsed = urlsplit(text)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError(f"{path} must be an HTTP(S) URL")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError(f"{path} must not contain credentials")
    hostname = parsed.hostname.lower()
    if hostname == "localhost" or hostname.endswith(".local"):
        raise ValueError(f"{path} must not reference a local host")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return text
    if not address.is_global:
        raise ValueError(f"{path} must not reference a private or local address")
    return text


def validate_manifest(value: object) -> None:
    root = _mapping(value, "manifest")
    _exact(
        root,
        {"schema_version", "environment_id", "generated_at", "sources", "claims"},
        "manifest",
    )
    if root.get("schema_version") != "glr.knowledge-research.v1":
        raise ValueError("manifest.schema_version must be glr.knowledge-research.v1")
    _identifier(root.get("environment_id"), "manifest.environment_id")
    _timestamp(root.get("generated_at"), "manifest.generated_at")

    source_ids: set[str] = set()
    for index, item in enumerate(_sequence(root.get("sources"), "manifest.sources")):
        path = f"manifest.sources[{index}]"
        source = _mapping(item, path)
        _exact(
            source,
            {
                "id",
                "url",
                "publisher",
                "source_type",
                "accessed_at",
                "content_updated_at",
                "summary",
                "confidence",
                "volatility",
            },
            path,
        )
        source_id = _identifier(source.get("id"), f"{path}.id")
        if source_id in source_ids:
            raise ValueError(f"duplicate source id: {source_id}")
        source_ids.add(source_id)
        _public_url(source.get("url"), f"{path}.url")
        _text(source.get("publisher"), f"{path}.publisher", maximum=120)
        if source.get("source_type") not in _SOURCE_TYPES:
            raise ValueError(f"{path}.source_type is unsupported")
        _timestamp(source.get("accessed_at"), f"{path}.accessed_at")
        if source.get("content_updated_at") is not None:
            _timestamp(source.get("content_updated_at"), f"{path}.content_updated_at")
        _text(source.get("summary"), f"{path}.summary", maximum=500)
        if source.get("confidence") not in _CONFIDENCE:
            raise ValueError(f"{path}.confidence is unsupported")
        if source.get("volatility") not in _VOLATILITY:
            raise ValueError(f"{path}.volatility is unsupported")

    claim_ids: set[str] = set()
    for index, item in enumerate(_sequence(root.get("claims"), "manifest.claims")):
        path = f"manifest.claims[{index}]"
        claim = _mapping(item, path)
        _exact(
            claim,
            {
                "id",
                "category",
                "status",
                "statement",
                "source_ids",
                "confidence",
                "version_assumption",
                "contradictions",
            },
            path,
        )
        claim_id = _identifier(claim.get("id"), f"{path}.id")
        if claim_id in claim_ids:
            raise ValueError(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        if claim.get("category") not in _CATEGORIES:
            raise ValueError(f"{path}.category is unsupported")
        if claim.get("status") not in _STATUSES:
            raise ValueError(f"{path}.status is unsupported")
        _text(claim.get("statement"), f"{path}.statement", maximum=500)
        references = _sequence(claim.get("source_ids"), f"{path}.source_ids")
        if not references:
            raise ValueError(f"{path}.source_ids cannot be empty")
        for reference in references:
            source_id = _identifier(reference, f"{path}.source_ids[]")
            if source_id not in source_ids:
                raise ValueError(f"{path} references unknown source {source_id}")
        if claim.get("confidence") not in _CONFIDENCE:
            raise ValueError(f"{path}.confidence is unsupported")
        for optional in ("version_assumption", "contradictions"):
            if claim.get(optional) is not None:
                _text(claim.get(optional), f"{path}.{optional}", maximum=500)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        with args.manifest.open(encoding="utf-8") as stream:
            value = json.load(stream)
        validate_manifest(value)
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(f"Valid research manifest: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
