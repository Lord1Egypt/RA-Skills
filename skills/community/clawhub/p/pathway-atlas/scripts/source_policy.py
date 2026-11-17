"""Deterministic source independence and evidence-admission policy."""

from __future__ import annotations

import hashlib
import json
import unicodedata
from collections import defaultdict
from dataclasses import replace
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

if __package__:
    from .contracts import (
        EvidenceFact,
        EvidenceStatus,
        FactClaim,
        SourceCandidate,
        SourceTier,
    )
else:  # ``sys.path`` rooted at ``scripts`` package compatibility.
    from contracts import (  # type: ignore
        EvidenceFact,
        EvidenceStatus,
        FactClaim,
        SourceCandidate,
        SourceTier,
    )


_TRACKING_PARAMETERS = frozenset(
    {
        "_ga",
        "_gl",
        "dclid",
        "fbclid",
        "gclid",
        "igshid",
        "mc_cid",
        "mc_eid",
        "msclkid",
        "si",
        "spm",
        "yclid",
    }
)


def canonicalize_url(url: str) -> str:
    """Remove URL decorations that do not identify the referenced document."""

    value = url.strip()
    try:
        parsed = urlsplit(value)
    except ValueError:
        return value

    scheme = parsed.scheme.lower()
    hostname = parsed.hostname
    if hostname is None:
        netloc = parsed.netloc.lower()
    else:
        try:
            port = parsed.port
        except ValueError:
            return value
        host = hostname.lower()
        if ":" in host:
            host = f"[{host}]"
        userinfo = ""
        if parsed.username is not None:
            userinfo = parsed.username
            if parsed.password is not None:
                userinfo += f":{parsed.password}"
            userinfo += "@"
        default_port = (scheme == "http" and port == 80) or (
            scheme == "https" and port == 443
        )
        netloc = f"{userinfo}{host}"
        if port is not None and not default_port:
            netloc += f":{port}"

    parameters = [
        (key, item)
        for key, item in parse_qsl(parsed.query, keep_blank_values=True)
        if not _is_tracking_parameter(key)
    ]
    query = urlencode(sorted(parameters), doseq=True)
    return urlunsplit((scheme, netloc, parsed.path, query, ""))


def canonicalize_provenance_url(url: str) -> str:
    """Canonicalize a traceable absolute HTTP(S) provenance URL.

    Opaque labels, relative references, non-web schemes, credentials, and
    malformed authorities return an empty string so evidence admission fails
    closed even when callers do not run the bundle validator first.
    """

    parsed_parts = _public_http_parts(url)
    if parsed_parts is None:
        return ""
    parsed, hostname, port = parsed_parts
    scheme = parsed.scheme.casefold()
    rendered_host = f"[{hostname}]" if ":" in hostname else hostname
    default_port = (scheme == "http" and port == 80) or (
        scheme == "https" and port == 443
    )
    netloc = rendered_host
    if port is not None and not default_port:
        netloc += f":{port}"
    parameters = [
        (key, item)
        for key, item in parse_qsl(parsed.query, keep_blank_values=True)
        if not _is_tracking_parameter(key)
    ]
    query = urlencode(sorted(parameters), doseq=True)
    return urlunsplit((scheme, netloc, parsed.path, query, ""))


def content_fingerprint(text: str) -> str:
    """Return a whitespace-insensitive SHA-256 fingerprint for source text."""

    normalized = " ".join(unicodedata.normalize("NFKC", text).split())
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return f"sha256:{digest}"


def canonical_site_identity(url: str) -> str:
    """Return a stable site identity for an absolute public HTTP(S) URL.

    Site identity deliberately ignores the HTTP/HTTPS distinction and their
    default ports.  A leading ``www.`` label and a DNS root trailing dot are
    aliases of the same publishing site.
    """

    parsed_parts = _public_http_parts(url)
    if parsed_parts is None:
        return ""
    parsed, hostname, port = parsed_parts
    scheme = parsed.scheme.casefold()
    if ":" not in hostname:
        if hostname.startswith("www.") and len(hostname) > len("www."):
            hostname = hostname[len("www.") :]
    default_port = (scheme == "http" and port == 80) or (
        scheme == "https" and port == 443
    )
    if port is not None and not default_port:
        return f"{hostname}:{port}"
    return hostname


def _public_http_parts(url: str) -> tuple[Any, str, int | None] | None:
    if not isinstance(url, str) or not url or url != url.strip():
        return None
    if any(character.isspace() for character in url) or "\\" in url:
        return None
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        return None
    if _authority_has_empty_port(parsed.netloc):
        return None
    if (
        parsed.scheme.casefold() not in {"http", "https"}
        or parsed.hostname is None
        or parsed.username is not None
        or parsed.password is not None
    ):
        return None
    hostname = parsed.hostname.rstrip(".").casefold()
    if not hostname:
        return None
    if ":" not in hostname:
        try:
            hostname = hostname.encode("idna").decode("ascii")
        except UnicodeError:
            return None
        labels = hostname.split(".")
        if len(hostname) > 253 or any(
            not label
            or len(label) > 63
            or label.startswith("-")
            or label.endswith("-")
            or any(
                character != "-"
                and not (character.isascii() and character.isalnum())
                for character in label
            )
            for label in labels
        ):
            return None
    return parsed, hostname, port


def _authority_has_empty_port(netloc: str) -> bool:
    """Detect a present-but-empty port in an already parsed authority."""

    authority = netloc.rsplit("@", 1)[-1]
    if authority.startswith("["):
        closing_bracket = authority.rfind("]")
        return closing_bracket >= 0 and authority[closing_bracket + 1 :] == ":"
    return authority.endswith(":")


def deduplicate_candidates(
    candidates: Iterable[SourceCandidate],
) -> tuple[list[SourceCandidate], dict[str, str]]:
    """Keep one deterministic candidate from every non-independent component."""

    unique, rejected, _ = _deduplicate_with_representatives(candidates)
    return unique, rejected


def _deduplicate_with_representatives(
    candidates: Iterable[SourceCandidate],
) -> tuple[list[SourceCandidate], dict[str, str], dict[str, str]]:
    """Deduplicate candidates and retain a source-ID-to-representative map."""

    all_candidates = sorted(candidates, key=_candidate_sort_key)
    rejected_reasons = {
        candidate.source_id: "insufficient-source-identity"
        for candidate in all_candidates
        if not _has_complete_identity(candidate)
    }
    ordered = [
        candidate
        for candidate in all_candidates
        if candidate.source_id not in rejected_reasons
    ]
    parents = list(range(len(ordered)))

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parents[right_root] = left_root

    indexes: dict[str, dict[str, int]] = {
        "publisher": {},
        "site": {},
        "citation_root": {},
        "content_hash": {},
    }
    for index, candidate in enumerate(ordered):
        for identity_kind, identity in _candidate_identities(candidate).items():
            if not identity:
                continue
            existing = indexes[identity_kind].get(identity)
            if existing is None:
                indexes[identity_kind][identity] = index
            else:
                union(existing, index)

    components: dict[int, list[int]] = defaultdict(list)
    for index in range(len(ordered)):
        components[find(index)].append(index)

    unique: list[SourceCandidate] = []
    representatives: dict[str, str] = {}
    for component in components.values():
        component.sort()
        retained = min(component, key=lambda index: _representative_sort_key(ordered[index]))
        unique.append(ordered[retained])
        reason = _component_rejection_reason([ordered[index] for index in component])
        representative_id = ordered[retained].source_id
        for index in component:
            source_id = ordered[index].source_id
            representatives[source_id] = representative_id
            if index != retained:
                rejected_reasons[source_id] = reason

    unique.sort(key=_candidate_sort_key)
    rejected = {
        candidate.source_id: rejected_reasons[candidate.source_id]
        for candidate in all_candidates
        if candidate.source_id in rejected_reasons
    }
    return unique, rejected, representatives


def evaluate_claims(
    field: str,
    claims: Iterable[FactClaim],
    sources: Iterable[SourceCandidate],
) -> EvidenceFact:
    """Apply tiered evidence policy to claims for one field without estimation."""

    unique_sources, _, representatives = _deduplicate_with_representatives(sources)
    sources_by_id = {source.source_id: source for source in unique_sources}
    field_claims = sorted(
        (
            replace(claim, source_id=representatives[claim.source_id])
            for claim in claims
            if claim.field == field and claim.source_id in representatives
        ),
        key=_claim_sort_key,
    )
    claims_by_source: dict[str, list[FactClaim]] = defaultdict(list)
    for claim in field_claims:
        claims_by_source[claim.source_id].append(claim)

    a_source_ids = {
        source.source_id for source in unique_sources if source.tier == SourceTier.A
    }
    a_roots = {
        root
        for source in unique_sources
        if source.tier == SourceTier.A
        for root in (
            canonicalize_provenance_url(source.url),
            _canonical_root(source.citation_root),
        )
        if root
    }
    direct_a_source_ids = {
        source.source_id
        for source in unique_sources
        if source.tier == SourceTier.B
        and _canonical_root(source.citation_root) in a_roots
    }

    a_claims = _claims_for_sources(claims_by_source, a_source_ids | direct_a_source_ids)
    if a_claims:
        method = "direct-a-upstream" if not set(_source_ids(a_claims)) & a_source_ids else "tier-a"
        return _evaluate_layer(
            field,
            a_claims,
            EvidenceStatus.OFFICIAL,
            1,
            method,
        )

    b_source_ids = {
        source.source_id
        for source in unique_sources
        if source.tier == SourceTier.B and source.source_id not in direct_a_source_ids
    }
    b_claims = _claims_for_sources(claims_by_source, b_source_ids)
    if b_claims:
        traceable_b_claims = [
            claim
            for claim in b_claims
            if _canonical_root(sources_by_id[claim.source_id].citation_root)
        ]
        if _has_conflict(b_claims):
            return _conflict_fact(field, b_claims)
        if len(_source_ids(traceable_b_claims)) >= 2:
            return _evaluate_layer(
                field,
                traceable_b_claims,
                EvidenceStatus.CORROBORATED,
                2,
                "two-source-consensus",
            )

    c_claims = _claims_for_sources(
        claims_by_source,
        {source.source_id for source in unique_sources if source.tier == SourceTier.C},
    )
    if _has_conflict(c_claims):
        return _conflict_fact(field, c_claims)
    if len(_source_ids(c_claims)) >= 3:
        return _evaluate_layer(
            field,
            c_claims,
            EvidenceStatus.REFERENCE,
            3,
            "three-source-consensus",
        )

    observed = b_claims or c_claims
    return _fact(
        field,
        None,
        None,
        EvidenceStatus.MISSING,
        _source_ids(observed),
        "insufficient-independent-sources",
        "No qualifying independent sources provide an exact value.",
    )


def _is_tracking_parameter(key: str) -> bool:
    normalized = key.casefold()
    return normalized.startswith("utm_") or normalized in _TRACKING_PARAMETERS


def _candidate_sort_key(candidate: SourceCandidate) -> tuple[str, ...]:
    return (
        candidate.source_id,
        canonicalize_url(candidate.url),
        _publisher_key(candidate.publisher),
        _canonical_root(candidate.citation_root),
        _content_hash_key(candidate.content_hash),
        candidate.published_at or "",
        candidate.retrieved_at,
        candidate.summary,
    )


def _representative_sort_key(candidate: SourceCandidate) -> tuple[int, tuple[str, ...]]:
    tier_priority = {
        SourceTier.A: 0,
        SourceTier.B: 1,
        SourceTier.C: 2,
    }
    return (tier_priority[candidate.tier], _candidate_sort_key(candidate))


def _candidate_identities(candidate: SourceCandidate) -> dict[str, str]:
    return {
        "publisher": _publisher_key(candidate.publisher),
        "site": canonical_site_identity(candidate.url),
        "citation_root": _canonical_root(candidate.citation_root),
        "content_hash": _content_hash_key(candidate.content_hash),
    }


def _has_complete_identity(candidate: SourceCandidate) -> bool:
    return all(_candidate_identities(candidate).values())


def _publisher_key(publisher: str) -> str:
    return " ".join(publisher.casefold().split())


def _canonical_root(citation_root: str) -> str:
    return canonicalize_provenance_url(citation_root)


def _content_hash_key(content_hash: str) -> str:
    return content_hash.strip().casefold()


def _component_rejection_reason(component: list[SourceCandidate]) -> str:
    for identity_kind in ("publisher", "citation_root"):
        identities = [_candidate_identities(source)[identity_kind] for source in component]
        if len([item for item in identities if item]) != len(set(item for item in identities if item)):
            return "same-publisher-or-citation-root"
    site_identities = [_candidate_identities(source)["site"] for source in component]
    if len(site_identities) != len(set(site_identities)):
        return "same-site"
    return "same-content-hash"


def _claim_sort_key(claim: FactClaim) -> tuple[str, str, str]:
    return (claim.source_id, _claim_signature(claim), claim.method)


def _claim_signature(claim: FactClaim) -> str:
    try:
        return json.dumps(
            [claim.value, claim.unit],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError):
        return repr((claim.value, claim.unit))


def _claims_for_sources(
    claims_by_source: dict[str, list[FactClaim]], source_ids: set[str]
) -> list[FactClaim]:
    return [
        claim
        for source_id in sorted(source_ids)
        for claim in claims_by_source.get(source_id, [])
    ]


def _source_ids(claims: Iterable[FactClaim]) -> tuple[str, ...]:
    return tuple(sorted({claim.source_id for claim in claims}))


def _has_conflict(claims: Iterable[FactClaim]) -> bool:
    return len({_claim_signature(claim) for claim in claims}) > 1


def _evaluate_layer(
    field: str,
    claims: list[FactClaim],
    status: EvidenceStatus,
    minimum_sources: int,
    method: str,
) -> EvidenceFact:
    if _has_conflict(claims):
        return _conflict_fact(field, claims)
    source_ids = _source_ids(claims)
    if len(source_ids) < minimum_sources:
        return _fact(
            field,
            None,
            None,
            EvidenceStatus.MISSING,
            source_ids,
            "insufficient-independent-sources",
            "No qualifying independent sources provide an exact value.",
        )
    selected = min(claims, key=_claim_sort_key)
    return _fact(field, selected.value, selected.unit, status, source_ids, method, "")


def _conflict_fact(field: str, claims: Iterable[FactClaim]) -> EvidenceFact:
    return _fact(
        field,
        None,
        None,
        EvidenceStatus.CONFLICT,
        _source_ids(claims),
        "conflicting-exact-values",
        "Independent sources disagree on an exact value.",
    )


def _fact(
    field: str,
    value: Any,
    unit: str | None,
    status: EvidenceStatus,
    source_ids: tuple[str, ...],
    method: str,
    notes: str,
) -> EvidenceFact:
    identity = json.dumps(
        [field, value, unit, status.value, source_ids, method, notes],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        default=repr,
    )
    fact_id = f"{field}:{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:16]}"
    return EvidenceFact(fact_id, field, value, unit, status, source_ids, method, notes)


__all__ = [
    "canonical_site_identity",
    "canonicalize_provenance_url",
    "canonicalize_url",
    "content_fingerprint",
    "deduplicate_candidates",
    "evaluate_claims",
]
