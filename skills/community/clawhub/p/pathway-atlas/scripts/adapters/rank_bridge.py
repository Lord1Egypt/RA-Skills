"""Authenticate exact rank adapter rows against one profile and query plan."""

from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import date
import hashlib
import json
import re
from typing import Any, Iterable, Mapping
from urllib.parse import parse_qsl, unquote, urlsplit

if __package__ == "scripts.adapters":
    from . import (
        CellStatus,
        ExtractedCoverage,
        ExtractedRow,
        ExtractedTable,
        validate_public_locator,
    )
    from ..contracts import (
        EvidenceFact,
        EvidenceStatus,
        FactClaim,
        SourceCandidate,
        SourceTier,
    )
    from ..evidence import EvidenceStore
    from ..planning_profile import PlanningProfile
    from ..province_registry import canonical_discovery_subject_key
    from ..query_plan import QueryPlan, QueryTask, validate_query_plan_payload
    from ..source_policy import (
        canonical_site_identity,
        canonicalize_provenance_url,
        evaluate_claims,
    )
else:  # pragma: no cover - flat scripts-path compatibility
    from adapters import (  # type: ignore
        CellStatus,
        ExtractedCoverage,
        ExtractedRow,
        ExtractedTable,
        validate_public_locator,
    )
    from contracts import (  # type: ignore
        EvidenceFact,
        EvidenceStatus,
        FactClaim,
        SourceCandidate,
        SourceTier,
    )
    from evidence import EvidenceStore  # type: ignore
    from planning_profile import PlanningProfile  # type: ignore
    from province_registry import canonical_discovery_subject_key  # type: ignore
    from query_plan import QueryPlan, QueryTask, validate_query_plan_payload  # type: ignore
    from source_policy import (  # type: ignore
        canonical_site_identity,
        canonicalize_provenance_url,
        evaluate_claims,
    )


_ACCEPTED = frozenset(
    {EvidenceStatus.OFFICIAL, EvidenceStatus.CORROBORATED, EvidenceStatus.REFERENCE}
)
_COVERAGE = _ACCEPTED
_EXTRACTION_METHODS = frozenset(
    {"html-table", "xlsx-worksheet", "xls-worksheet", "pdf-text-table", "host-ocr-rows"}
)
_SHA256 = re.compile(r"^sha256:([0-9a-f]{64})$")
_SYNTHETIC_PUBLISHER = re.compile(r"^rank-publisher-sha256-([0-9a-f]{64})$")
_SYNTHETIC_SITE = re.compile(
    r"^rank-site\.([0-9a-f]{32})\.([0-9a-f]{32})\.invalid$"
)
_SYNTHETIC_IDENTITY_PATH = re.compile(r"^/rank-identity/([0-9a-f]{64})/?$")


class RankBridgeError(ValueError):
    """An adapter result cannot form authenticated rank evidence."""


def _canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _plan_digest(plan: QueryPlan) -> str:
    return _canonical_digest(plan.to_dict())


def _canonical_task_snapshot(task: QueryTask) -> QueryTask:
    if not isinstance(task, QueryTask):
        raise TypeError("task must be a QueryTask")
    payload = task.to_dict()
    try:
        snapshot = QueryTask(**payload)
    except (KeyError, TypeError, ValueError):
        raise RankBridgeError("query task is not canonical") from None
    if snapshot.to_dict() != payload:
        raise RankBridgeError("query task is not canonical")
    return snapshot


def _pending_official_score(profile: PlanningProfile) -> int | None:
    observations = tuple(
        item
        for item in profile.rank_observations
        if item.scope == "province_official"
    )
    if not observations:
        return None
    latest = max(observations, key=lambda item: item.exam_date)
    if latest.rank is not None:
        return None
    return latest.score


def _exact_mapping(value: Any, names: set[str], label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != names:
        raise RankBridgeError(f"{label} fields do not match the contract")
    return value


def _validate_safe_json(value: Any, label: str) -> None:
    if value is None or isinstance(value, (int, float, bool)):
        return
    if isinstance(value, str):
        try:
            validate_public_locator(value)
        except (TypeError, ValueError):
            raise RankBridgeError(f"{label} contains unsafe public text") from None
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            _validate_safe_json(key, label)
            _validate_safe_json(item, label)
        return
    if isinstance(value, (tuple, list)):
        for item in value:
            _validate_safe_json(item, label)
        return
    raise RankBridgeError(f"{label} contains unsupported data")


def _http_identities(value: Any, label: str) -> tuple[str, str]:
    if not isinstance(value, str):
        raise RankBridgeError(f"{label} must be a public HTTP URL")
    canonical = canonicalize_provenance_url(value)
    site = canonical_site_identity(value)
    if not canonical or not site:
        raise RankBridgeError(f"{label} must be a public HTTP URL")
    try:
        parsed = urlsplit(value)
        pieces = [parsed.hostname or "", unquote(parsed.fragment)]
        pieces.extend(unquote(item) for item in parsed.path.split("/") if item)
        pieces.extend(
            f"{unquote(key)}:{unquote(item)}"
            for key, item in parse_qsl(parsed.query, keep_blank_values=True)
        )
        for piece in pieces:
            if piece:
                validate_public_locator(piece)
    except (TypeError, ValueError):
        raise RankBridgeError(f"{label} contains unsafe public text") from None
    return canonical, site


def _encoded_http_identities(value: str) -> tuple[str, str] | None:
    try:
        parsed = urlsplit(value)
    except ValueError:
        return None
    host_match = _SYNTHETIC_SITE.fullmatch(parsed.hostname or "")
    path_match = _SYNTHETIC_IDENTITY_PATH.fullmatch(parsed.path)
    if host_match is None or path_match is None:
        return None
    return (
        "sha256:" + path_match.group(1),
        "sha256:" + host_match.group(1) + host_match.group(2),
    )


def _candidate_projection(candidate: SourceCandidate) -> dict[str, str]:
    publisher_match = _SYNTHETIC_PUBLISHER.fullmatch(candidate.publisher)
    for name in (
        "source_id",
        "publisher",
        "published_at",
        "retrieved_at",
        "content_hash",
        "summary",
    ):
        # Replayed publisher identities encode a digest, not public prose.
        if name == "publisher" and publisher_match is not None:
            continue
        item = getattr(candidate, name)
        if item is not None:
            _validate_safe_json(item, f"rank source {name}")
    if _SHA256.fullmatch(candidate.content_hash) is None:
        raise RankBridgeError("rank source content hash is invalid")
    encoded_url = _encoded_http_identities(candidate.url)
    if encoded_url is None:
        canonical_url, site = _http_identities(candidate.url, "rank source URL")
        url_hash = _canonical_digest(canonical_url)
        site_hash = _canonical_digest(site)
    else:
        url_hash, site_hash = encoded_url
    encoded_root = _encoded_http_identities(candidate.citation_root)
    if encoded_root is None:
        canonical_root, citation_site = _http_identities(
            candidate.citation_root, "rank source citation root"
        )
        citation_root_hash = _canonical_digest(canonical_root)
        citation_site_hash = _canonical_digest(citation_site)
    else:
        citation_root_hash, citation_site_hash = encoded_root
    publisher_hash = (
        "sha256:" + publisher_match.group(1)
        if publisher_match is not None
        else _canonical_digest(" ".join(candidate.publisher.casefold().split()))
    )
    return {
        "source_id": candidate.source_id,
        "tier": candidate.tier.value,
        "publisher_hash": publisher_hash,
        "site_hash": site_hash,
        "url_hash": url_hash,
        "citation_root_hash": citation_root_hash,
        "citation_site_hash": citation_site_hash,
        "content_hash": candidate.content_hash,
    }


def _hash_hex(value: Any, label: str) -> str:
    if not isinstance(value, str):
        raise RankBridgeError(f"{label} is invalid")
    matched = _SHA256.fullmatch(value)
    if matched is None:
        raise RankBridgeError(f"{label} is invalid")
    return matched.group(1)


def _synthetic_identity_url(site_hash: Any, identity_hash: Any) -> str:
    site = _hash_hex(site_hash, "rank source site hash")
    identity = _hash_hex(identity_hash, "rank source identity hash")
    return (
        f"https://rank-site.{site[:32]}.{site[32:]}.invalid/"
        f"rank-identity/{identity}"
    )


def _candidate_from_projection(value: Any) -> SourceCandidate:
    payload = _exact_mapping(
        value,
        {
            "source_id",
            "tier",
            "publisher_hash",
            "site_hash",
            "url_hash",
            "citation_root_hash",
            "citation_site_hash",
            "content_hash",
        },
        "rank input source",
    )
    try:
        publisher = _hash_hex(payload["publisher_hash"], "rank publisher hash")
        return SourceCandidate(
            source_id=payload["source_id"],
            url=_synthetic_identity_url(payload["site_hash"], payload["url_hash"]),
            publisher=f"rank-publisher-sha256-{publisher}",
            tier=SourceTier(payload["tier"]),
            published_at=None,
            retrieved_at="2000-01-01T00:00:00Z",
            content_hash=payload["content_hash"],
            citation_root=_synthetic_identity_url(
                payload["citation_site_hash"], payload["citation_root_hash"]
            ),
            summary="rank source projection",
        )
    except (KeyError, TypeError, ValueError):
        raise RankBridgeError("rank input source is invalid") from None


def _table_from_projection(value: Any) -> ExtractedTable:
    payload = _exact_mapping(
        value,
        {
            "task_id",
            "row",
            "coverage",
            "extraction_method",
            "locator_hash",
            "sources",
        },
        "rank input projection",
    )
    row_payload = _exact_mapping(payload["row"], {"values"}, "rank input row")
    coverage = _exact_mapping(
        payload["coverage"],
        {"lower_score", "upper_score", "lower_rank", "upper_rank"},
        "rank input coverage",
    )
    locator_hash = _hash_hex(payload["locator_hash"], "rank locator hash")
    try:
        values = row_payload["values"]
        if not isinstance(values, Mapping):
            raise TypeError
        row = ExtractedRow(
            values=values,
            cell_status={name: CellStatus.EXACT for name in values},
            location=f"rank-locator-sha256-{locator_hash}",
            confidence=1,
            warnings=(),
        )
        return ExtractedTable(
            table_id="rank-table",
            caption=None,
            sheet=None,
            rows=(row,),
            coverage=ExtractedCoverage(**dict(coverage)),
            warnings=(),
            extraction_method=payload["extraction_method"],
        )
    except (KeyError, TypeError, ValueError):
        raise RankBridgeError("rank input table is invalid") from None


def _locator_hash(value: str) -> str:
    prefix = "rank-locator-sha256-"
    if value.startswith(prefix) and _SHA256.fullmatch("sha256:" + value[len(prefix):]):
        return "sha256:" + value[len(prefix):]
    return _canonical_digest(value)


def _input_projection(
    task: QueryTask,
    table: ExtractedTable,
    row: ExtractedRow,
    candidates: tuple[SourceCandidate, ...],
) -> dict[str, Any]:
    _validate_safe_json(task.task_id, "rank query task")
    _validate_safe_json(table.to_dict(), "rank adapter table")
    return {
        "task_id": task.task_id,
        "row": {"values": row.to_dict()["values"]},
        "coverage": table.coverage.to_dict(),
        "extraction_method": table.extraction_method,
        "locator_hash": _locator_hash(row.location),
        "sources": [_candidate_projection(item) for item in candidates],
    }


def _candidate_snapshot(candidate: SourceCandidate) -> SourceCandidate:
    return SourceCandidate(
        source_id=candidate.source_id,
        url=candidate.url,
        publisher=candidate.publisher,
        tier=candidate.tier,
        published_at=candidate.published_at,
        retrieved_at=candidate.retrieved_at,
        content_hash=candidate.content_hash,
        citation_root=candidate.citation_root,
        summary=candidate.summary,
    )


def _candidates(values: Iterable[SourceCandidate]) -> tuple[SourceCandidate, ...]:
    if isinstance(values, (str, bytes, bytearray)):
        raise TypeError("candidates must contain SourceCandidate records")
    result = tuple(values)
    if not result or any(not isinstance(item, SourceCandidate) for item in result):
        raise TypeError("candidates must contain SourceCandidate records")
    source_ids = tuple(item.source_id for item in result)
    if len(source_ids) != len(set(source_ids)):
        raise RankBridgeError("candidate source IDs must be unique")
    snapshots = tuple(_candidate_snapshot(item) for item in result)
    return tuple(sorted(snapshots, key=lambda item: item.source_id))


def _rank_row_hash(row: ExtractedRow) -> str:
    return _canonical_digest({"values": row.to_dict()["values"]})


def _exact_score_value(
    *,
    profile: PlanningProfile,
    plan: QueryPlan,
    task: QueryTask,
    table: ExtractedTable,
    row: ExtractedRow,
    coverage_status: EvidenceStatus,
) -> tuple[str, str, dict[str, Any], str]:
    if task.kind != "score_table" or task.target_name is not None:
        raise RankBridgeError("query task is not a score-table task")
    if set(row.values) not in (
        {"score", "rank", "cumulative_count"},
        {"score", "cumulative_count"},
    ):
        raise RankBridgeError("score-table row fields do not match the contract")
    if any(status is not CellStatus.EXACT for status in row.cell_status.values()):
        raise RankBridgeError("rank adapter row contains non-exact cells")
    score = row.values["score"]
    cumulative = row.values["cumulative_count"]
    # Official one-point tables commonly publish only score and cumulative
    # count. The cumulative count is the last rank at that score; derive it
    # here so the original column remains singly mapped and replayable.
    rank = row.values.get("rank", cumulative)
    if any(
        not isinstance(item, int) or isinstance(item, bool)
        for item in (score, rank, cumulative)
    ):
        raise RankBridgeError("score-table values must be exact integers")
    if score < 0 or rank < 1 or cumulative < rank:
        raise RankBridgeError("score-table values are outside their supported bounds")
    declared_scales = {
        item.max_score
        for item in profile.rank_observations
        if item.max_score is not None
    }
    if len(declared_scales) != 1 or score > next(iter(declared_scales)):
        raise RankBridgeError("score-table row does not match the profile score scale")
    coverage = table.coverage
    bounds = (
        coverage.lower_score,
        coverage.upper_score,
        coverage.lower_rank,
        coverage.upper_rank,
    )
    if any(not isinstance(item, int) or isinstance(item, bool) for item in bounds):
        raise RankBridgeError("score-table coverage must have exact numeric bounds")
    if not coverage.lower_score <= score <= coverage.upper_score:
        raise RankBridgeError("score lies outside the exact table coverage")
    if not coverage.lower_rank <= rank <= coverage.upper_rank:
        raise RankBridgeError("rank lies outside the exact table coverage")

    fact_id = f"score-table-{task.year}"
    row_hash = _rank_row_hash(row)
    value = {
        "schema_version": "1.0",
        "kind": "official_score_table",
        "profile_digest": profile.digest,
        "query_plan_digest": _plan_digest(plan),
        "query_task_id": task.task_id,
        "province": task.province,
        "subject_group": task.subject_group,
        "year": task.year,
        "score": score,
        "rank": rank,
        "cumulative_count": cumulative,
        "coverage_min_score": coverage.lower_score,
        "coverage_max_score": coverage.upper_score,
        "coverage_min_rank": coverage.lower_rank,
        "coverage_max_rank": coverage.upper_rank,
        "coverage_status": coverage_status.value,
        "row_hash": row_hash,
    }
    return "rank_channel", fact_id, value, row_hash


def _exact_joint_exam_value(
    *,
    profile: PlanningProfile,
    plan: QueryPlan,
    task: QueryTask,
    table: ExtractedTable,
    row: ExtractedRow,
    coverage_status: EvidenceStatus,
) -> tuple[str, str, dict[str, Any], str]:
    expected = {
        "scope",
        "rank_scope",
        "exam_date",
        "lower_rank",
        "central_rank",
        "upper_rank",
        "cohort_size",
    }
    if task.kind != "joy_report" or set(row.values) != expected:
        raise RankBridgeError("adapter row is not a planned joint-exam result")
    if row.values["scope"] != "joint_exam":
        raise RankBridgeError("rank result scope is unsupported")
    rank_scope = row.values["rank_scope"]
    if rank_scope not in {"province_joint", "city_joint"}:
        raise RankBridgeError("joint-exam rank scope is unsupported")
    exam_date = row.values["exam_date"]
    if not isinstance(exam_date, str):
        raise RankBridgeError("joint-exam date must be an ISO calendar date")
    try:
        parsed_exam_date = date.fromisoformat(exam_date)
    except ValueError:
        raise RankBridgeError("joint-exam date must be an ISO calendar date") from None
    if parsed_exam_date.isoformat() != exam_date or parsed_exam_date.year != task.year:
        raise RankBridgeError("joint-exam date does not match the query year")
    if any(status is not CellStatus.EXACT for status in row.cell_status.values()):
        raise RankBridgeError("rank adapter row contains non-exact cells")
    lower = row.values["lower_rank"]
    central = row.values["central_rank"]
    upper = row.values["upper_rank"]
    cohort = row.values["cohort_size"]
    if any(
        not isinstance(item, int) or isinstance(item, bool) or item < 1
        for item in (lower, central, upper, cohort)
    ):
        raise RankBridgeError("joint-exam ranks and cohort must be positive integers")
    if not lower <= central <= upper <= cohort:
        raise RankBridgeError("joint-exam bounds must be ordered within the cohort")
    coverage = table.coverage
    if (
        not isinstance(coverage.lower_rank, int)
        or isinstance(coverage.lower_rank, bool)
        or not isinstance(coverage.upper_rank, int)
        or isinstance(coverage.upper_rank, bool)
        or coverage.lower_rank > lower
        or coverage.upper_rank < upper
        or coverage.lower_rank < 1
        or coverage.upper_rank > cohort
    ):
        raise RankBridgeError("joint-exam bounds lack exact cohort coverage")
    fact_id = f"joint-exam-{exam_date}-{rank_scope}"
    row_hash = _rank_row_hash(row)
    value = {
        "schema_version": "1.0",
        "channel_id": fact_id,
        "kind": "joint_exam",
        "rank_scope": rank_scope,
        "exam_date": exam_date,
        "profile_digest": profile.digest,
        "query_plan_digest": _plan_digest(plan),
        "query_task_id": task.task_id,
        "province": task.province,
        "subject_group": task.subject_group,
        "high_school": profile.high_school,
        "class_level": profile.class_level,
        "year": task.year,
        "lower_rank": lower,
        "central_rank": central,
        "upper_rank": upper,
        "lower_percentile": lower / cohort,
        "central_percentile": central / cohort,
        "upper_percentile": upper / cohort,
        "cohort_size": cohort,
        "coverage": min(1.0, (coverage.upper_rank - coverage.lower_rank + 1) / cohort),
        "comparability": 1.0,
        "backtest_error": None,
        "coverage_min_rank": coverage.lower_rank,
        "coverage_max_rank": coverage.upper_rank,
        "coverage_status": coverage_status.value,
        "row_hash": row_hash,
    }
    return "rank_channel", fact_id, value, row_hash


def _exact_school_anchor_value(
    *,
    profile: PlanningProfile,
    plan: QueryPlan,
    task: QueryTask,
    table: ExtractedTable,
    row: ExtractedRow,
    coverage_status: EvidenceStatus,
) -> tuple[str, str, dict[str, Any], str]:
    expected = {
        "scope",
        "school_name",
        "class_level",
        "school_rank",
        "province_rank",
        "school_score",
        "max_score",
        "cohort_size",
    }
    comparability_fields = {"comparability_tier", "comparability_basis"}
    if (
        task.kind != "joy_report"
        or not expected <= set(row.values)
        or set(row.values) - expected not in (set(), comparability_fields)
    ):
        raise RankBridgeError("adapter row is not a planned school anchor")
    if row.values["scope"] != "school_anchor":
        raise RankBridgeError("rank result scope is unsupported")
    if any(status is not CellStatus.EXACT for status in row.cell_status.values()):
        raise RankBridgeError("rank adapter row contains non-exact cells")
    if (
        profile.high_school is None
        or profile.class_level is None
        or task.target_name != profile.high_school
    ):
        raise RankBridgeError("school anchor task does not match the profile school")
    school_name = row.values["school_name"]
    class_level = row.values["class_level"]
    if not isinstance(school_name, str) or not school_name.strip():
        raise RankBridgeError("school anchor school name must be non-empty text")
    if not isinstance(class_level, str) or not class_level.strip():
        raise RankBridgeError("school anchor class level must be non-empty text")
    exact_class = (
        school_name == profile.high_school and class_level == profile.class_level
    )
    same_school = school_name == profile.high_school
    if exact_class:
        if comparability_fields & set(row.values):
            raise RankBridgeError(
                "exact-class anchors must not declare broadened comparability"
            )
        comparability_tier = "exact_class"
        comparability_basis = "same_school_exact_class"
    elif same_school:
        if set(row.values) - expected != comparability_fields:
            raise RankBridgeError(
                "broadened school anchors require explicit comparability evidence"
            )
        comparability_tier = "same_school"
        expected_basis = (
            "authenticated_same_school_whole_school_cohort"
            if class_level in {"全校", "校级", "全年级"}
            else "authenticated_same_school_other_class_cohort"
        )
        if (
            row.values["comparability_tier"] != comparability_tier
            or row.values["comparability_basis"] != expected_basis
        ):
            raise RankBridgeError(
                "same-school anchor comparability is not authenticated"
            )
        comparability_basis = expected_basis
    else:
        if set(row.values) - expected != comparability_fields:
            raise RankBridgeError(
                "regional school anchors require explicit comparability evidence"
            )
        comparability_tier = row.values["comparability_tier"]
        comparability_basis = row.values["comparability_basis"]
        if (
            comparability_tier != "regional_similar"
            or comparability_basis
            not in {
                "authenticated_similar_school_cohort",
                "authenticated_regional_cohort",
            }
        ):
            raise RankBridgeError(
                "regional school anchor comparability is not authenticated"
            )
    school_rank = row.values["school_rank"]
    province_rank = row.values["province_rank"]
    school_score = row.values["school_score"]
    max_score = row.values["max_score"]
    cohort = row.values["cohort_size"]
    if any(
        not isinstance(item, int) or isinstance(item, bool) or item < 1
        for item in (school_rank, province_rank, school_score, max_score, cohort)
    ):
        raise RankBridgeError("school anchor values must be positive exact integers")
    declared_scales = {
        item.max_score
        for item in profile.rank_observations
        if item.max_score is not None
    }
    if len(declared_scales) != 1 or max_score not in declared_scales or school_score > max_score:
        raise RankBridgeError("school score does not match the profile score scale")
    if school_rank > cohort:
        raise RankBridgeError("school rank lies outside the declared cohort")
    coverage = table.coverage
    if (
        not isinstance(coverage.lower_rank, int)
        or isinstance(coverage.lower_rank, bool)
        or not isinstance(coverage.upper_rank, int)
        or isinstance(coverage.upper_rank, bool)
        or coverage.lower_rank > school_rank
        or coverage.upper_rank < school_rank
        or coverage.lower_rank < 1
        or coverage.upper_rank > cohort
    ):
        raise RankBridgeError("school anchor lacks exact cohort coverage")
    row_hash = _rank_row_hash(row)
    fact_id = (
        f"school-anchor-{task.year}"
        if exact_class
        else f"school-anchor-{task.year}-{row_hash.removeprefix('sha256:')[:12]}"
    )
    whole_school = (
        same_school
        and comparability_basis
        == "authenticated_same_school_whole_school_cohort"
    )
    value = {
        "schema_version": "1.0",
        "profile_digest": profile.digest,
        "query_plan_digest": _plan_digest(plan),
        "query_task_id": task.task_id,
        "province": task.province,
        "subject_group": task.subject_group,
        "class_level": profile.class_level,
        "anchor_id": fact_id,
        "year": task.year,
        "school_name": school_name,
        "scope_type": "whole_school" if whole_school else "named_program",
        "scope_value": school_name if whole_school else class_level,
        "comparability_tier": comparability_tier,
        "comparability_basis": comparability_basis,
        "school_rank": school_rank,
        "province_rank": province_rank,
        "school_score": school_score,
        "cohort_size": cohort,
        "coverage_status": coverage_status.value,
        "coverage_min_school_rank": coverage.lower_rank,
        "coverage_max_school_rank": coverage.upper_rank,
        "row_hash": row_hash,
    }
    return "rank_anchor", fact_id, value, row_hash


def _exact_rank_value(
    *,
    profile: PlanningProfile,
    plan: QueryPlan,
    task: QueryTask,
    table: ExtractedTable,
    row: ExtractedRow,
    coverage_status: EvidenceStatus,
) -> tuple[str, str, dict[str, Any], str]:
    if task.kind == "score_table":
        return _exact_score_value(
            profile=profile,
            plan=plan,
            task=task,
            table=table,
            row=row,
            coverage_status=coverage_status,
        )
    if row.values.get("scope") == "joint_exam":
        return _exact_joint_exam_value(
            profile=profile,
            plan=plan,
            task=task,
            table=table,
            row=row,
            coverage_status=coverage_status,
        )
    if row.values.get("scope") == "school_anchor":
        return _exact_school_anchor_value(
            profile=profile,
            plan=plan,
            task=task,
            table=table,
            row=row,
            coverage_status=coverage_status,
        )
    raise RankBridgeError("adapter row is not a supported rank result")


@dataclass(frozen=True, init=False)
class RankEvidenceBridge:
    """Factory-only authenticated result and Task-4 outcome digest seam."""

    profile_digest: str
    query_plan_digest: str
    task: QueryTask
    table: ExtractedTable
    adapter_row: ExtractedRow
    candidates: tuple[SourceCandidate, ...]
    fact_namespace: str
    fact_id: str
    source_ids: tuple[str, ...]
    evidence_status: EvidenceStatus
    coverage_status: EvidenceStatus
    evidence_method: str
    extraction_method: str
    locator: str
    row_hash: str
    artifact_digest: str
    provenance_digest: str
    origin_digest: str
    bridge_digest: str
    _fact_value_json: str
    _origin_json: str

    def __init__(self) -> None:
        raise TypeError("RankEvidenceBridge is factory-only")

    @classmethod
    def _create(cls, **values: Any) -> "RankEvidenceBridge":
        if set(values) != {item.name for item in fields(cls)}:
            raise TypeError("rank bridge factory fields do not match the contract")
        instance = object.__new__(cls)
        for name, value in values.items():
            object.__setattr__(instance, name, value)
        return instance

    @property
    def fact(self) -> EvidenceFact:
        value = json.loads(self._fact_value_json)
        if not isinstance(value, dict):  # pragma: no cover - factory invariant
            raise RankBridgeError("rank fact snapshot is invalid")
        value.update(
            {
                "artifact_digest": self.artifact_digest,
                "provenance_digest": self.provenance_digest,
                "bridge_digest": self.bridge_digest,
            }
        )
        return EvidenceFact(
            fact_id=self.fact_id,
            field=f"{self.fact_namespace}:{self.fact_id}",
            value=value,
            unit=None,
            status=self.evidence_status,
            source_ids=self.source_ids,
            method=self.evidence_method,
            notes=f"query_task:{self.task.task_id}",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_digest": self.profile_digest,
            "query_plan_digest": self.query_plan_digest,
            "task": self.task.to_dict(),
            "table": self.table.to_dict(),
            "adapter_row": self.adapter_row.to_dict(),
            "sources": [item.to_dict() for item in self.candidates],
            "fact": self.fact.to_dict(),
            "coverage_status": self.coverage_status.value,
            "row_hash": self.row_hash,
            "artifact_digest": self.artifact_digest,
            "provenance_digest": self.provenance_digest,
            "origin_digest": self.origin_digest,
            "bridge_digest": self.bridge_digest,
            "extraction_method": self.extraction_method,
            "locator": self.locator,
        }

    def persist(self, store: EvidenceStore) -> None:
        """Persist the verified fact and its exact adapter provenance."""

        if not isinstance(store, EvidenceStore):
            raise TypeError("store must be an EvidenceStore")
        store.add_fact(
            self.fact,
            year=self.task.year,
            extraction_method=self.extraction_method,
            locator=self.locator,
        )


def bridge_rank_evidence(
    *,
    profile: PlanningProfile,
    plan: QueryPlan,
    task: QueryTask,
    table: ExtractedTable,
    extracted_row: ExtractedRow,
    candidates: Iterable[SourceCandidate],
    coverage_status: EvidenceStatus,
) -> RankEvidenceBridge:
    """Authenticate one exact adapter result without caller-authored trust."""

    if not isinstance(profile, PlanningProfile):
        raise TypeError("profile must be a PlanningProfile")
    if type(plan) is not QueryPlan:
        raise TypeError("plan must be a canonical QueryPlan")
    try:
        validated_plan = validate_query_plan_payload(plan.to_dict())
    except (KeyError, TypeError, ValueError):
        raise RankBridgeError("plan is not a canonical validated query plan") from None
    if validated_plan.to_dict() != plan.to_dict():
        raise RankBridgeError("plan is not a canonical validated query plan")
    if not isinstance(task, QueryTask):
        raise TypeError("task must be a QueryTask")
    if sum(item is task for item in plan.tasks) != 1:
        raise RankBridgeError("query task is detached from its canonical plan")
    canonical_task = _canonical_task_snapshot(task)
    if not isinstance(table, ExtractedTable) or not isinstance(extracted_row, ExtractedRow):
        raise TypeError("table and extracted_row must be adapter contracts")
    if sum(item is extracted_row for item in table.rows) != 1:
        raise RankBridgeError("adapter row is detached from its table")
    if any(
        status is not CellStatus.EXACT
        for row in table.rows
        for status in row.cell_status.values()
    ):
        raise RankBridgeError("rank table contains a non-exact coverage boundary")
    if table.extraction_method not in _EXTRACTION_METHODS:
        raise RankBridgeError("adapter extraction method is unsupported")
    if not isinstance(coverage_status, EvidenceStatus) or coverage_status not in _COVERAGE:
        raise RankBridgeError("coverage status is not report-consumable")
    expected_subject = canonical_discovery_subject_key(
        profile.subject_mode,
        profile.subject_group,
        profile.secondary_subjects,
        province=profile.province,
    )
    if (
        plan.province != profile.province
        or plan.subject_group != expected_subject
        or plan.exam_year != profile.exam_year
        or canonical_task.province != profile.province
        or canonical_task.subject_group != expected_subject
    ):
        raise RankBridgeError("profile, plan, and query-task contexts disagree")

    normalized_candidates = _candidates(candidates)
    fact_namespace, fact_id, value, row_hash = _exact_rank_value(
        profile=profile,
        plan=plan,
        task=canonical_task,
        table=table,
        row=extracted_row,
        coverage_status=coverage_status,
    )
    input_projection = _input_projection(
        canonical_task,
        table,
        extracted_row,
        normalized_candidates,
    )
    policy_candidates = tuple(
        _candidate_from_projection(item) for item in input_projection["sources"]
    )
    value = {
        **value,
        "input_projection": input_projection,
        "content_hash": _canonical_digest(input_projection),
    }
    target_score = (
        _pending_official_score(profile)
        if canonical_task.kind == "score_table"
        else None
    )
    target_score_matched = (
        target_score is None or value.get("score") == target_score
    )
    if target_score is not None:
        value = {
            **value,
            "target_score": target_score,
            "target_score_matched": target_score_matched,
            **(
                {}
                if target_score_matched
                else {"kind": "score_table_unmatched"}
            ),
        }
    field = f"{fact_namespace}:{fact_id}"
    evaluated = evaluate_claims(
        field,
        tuple(
            FactClaim(
                field=field,
                value=value,
                unit=None,
                source_id=item.source_id,
                method="rank-adapter-bridge-v1",
            )
            for item in policy_candidates
        ),
        policy_candidates,
    )
    if evaluated.status not in _ACCEPTED or evaluated.value != value:
        raise RankBridgeError("candidate policy does not support rank evidence")
    if value.get("kind") == "official_score_table" and evaluated.status is not EvidenceStatus.OFFICIAL:
        value = {**value, "kind": "score_table_reference"}
        evaluated = evaluate_claims(
            field,
            tuple(
                FactClaim(
                    field=field,
                    value=value,
                    unit=None,
                    source_id=item.source_id,
                    method="rank-adapter-bridge-v1",
                )
                for item in policy_candidates
            ),
            policy_candidates,
        )
        if evaluated.status not in _ACCEPTED or evaluated.value != value:
            raise RankBridgeError("candidate policy does not support rank evidence")
    if fact_namespace == "rank_anchor":
        value = {
            **value,
            "source_ids": list(evaluated.source_ids),
            "evidence_status": evaluated.status.value,
        }
        evaluated = evaluate_claims(
            field,
            tuple(
                FactClaim(
                    field=field,
                    value=value,
                    unit=None,
                    source_id=item.source_id,
                    method="rank-adapter-bridge-v1",
                )
                for item in policy_candidates
            ),
            policy_candidates,
        )
        if evaluated.status not in _ACCEPTED or evaluated.value != value:
            raise RankBridgeError("candidate policy does not support rank evidence")
    evidence_status = (
        evaluated.status
        if target_score_matched
        else EvidenceStatus.PARTIAL
    )
    locator = validate_public_locator(extracted_row.location)
    artifact_digest = _canonical_digest(
        {
            "input_projection": input_projection,
            "row_hash": row_hash,
        }
    )
    provenance_digest = _canonical_digest(
        {
            "task_id": canonical_task.task_id,
            "year": canonical_task.year,
            "source_ids": list(evaluated.source_ids),
            "evidence_status": evidence_status.value,
            "coverage_status": coverage_status.value,
            "evidence_method": evaluated.method,
            "extraction_method": table.extraction_method,
            "locator_hash": input_projection["locator_hash"],
        }
    )
    plan_identity = _plan_digest(plan)
    origin_payload = {
        "schema_version": "1.0",
        "profile_digest": profile.digest,
        "query_plan_digest": plan_identity,
        "task": canonical_task.to_dict(),
        "source_policy": {
            "id": canonical_task.source_policy_id,
            "version": canonical_task.source_policy_version,
        },
        "table": table.to_dict(),
        "adapter_row": extracted_row.to_dict(),
        "adapter_row_index": next(
            index for index, item in enumerate(table.rows) if item is extracted_row
        ),
        "sources": [item.to_dict() for item in normalized_candidates],
        "coverage_status": coverage_status.value,
    }
    origin_json = json.dumps(
        origin_payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    origin_digest = _canonical_digest(origin_payload)
    bridge_digest = _canonical_digest(
        {
            "profile_digest": profile.digest,
            "query_plan_digest": plan_identity,
            "task_id": canonical_task.task_id,
            "fact_id": fact_id,
            "row_hash": row_hash,
            "artifact_digest": artifact_digest,
            "provenance_digest": provenance_digest,
        }
    )
    return RankEvidenceBridge._create(
        profile_digest=profile.digest,
        query_plan_digest=plan_identity,
        task=task,
        table=table,
        adapter_row=extracted_row,
        candidates=normalized_candidates,
        fact_namespace=fact_namespace,
        fact_id=fact_id,
        source_ids=evaluated.source_ids,
        evidence_status=evidence_status,
        coverage_status=coverage_status,
        evidence_method=evaluated.method,
        extraction_method=table.extraction_method,
        locator=locator,
        row_hash=row_hash,
        artifact_digest=artifact_digest,
        provenance_digest=provenance_digest,
        origin_digest=origin_digest,
        bridge_digest=bridge_digest,
        _fact_value_json=json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ),
        _origin_json=origin_json,
    )


def validate_rank_evidence_bridge(
    bridge: RankEvidenceBridge,
    profile: PlanningProfile,
    plan: QueryPlan,
) -> RankEvidenceBridge:
    """Rebuild a bridge through its public inputs and reject any mutation."""

    if type(bridge) is not RankEvidenceBridge:
        raise TypeError("evidence must contain factory rank bridges")
    if not isinstance(profile, PlanningProfile):
        raise TypeError("profile must be a PlanningProfile")
    if type(plan) is not QueryPlan:
        raise TypeError("plan must be a canonical QueryPlan")
    try:
        canonical_plan = validate_query_plan_payload(plan.to_dict())
    except (KeyError, TypeError, ValueError):
        raise RankBridgeError("plan is not a canonical validated query plan") from None
    if canonical_plan.to_dict() != plan.to_dict():
        raise RankBridgeError("plan is not a canonical validated query plan")
    try:
        origin = json.loads(bridge._origin_json)
    except (AttributeError, TypeError, ValueError, json.JSONDecodeError):
        raise RankBridgeError("rank bridge factory origin is invalid") from None
    expected_origin_fields = {
        "schema_version",
        "profile_digest",
        "query_plan_digest",
        "task",
        "source_policy",
        "table",
        "adapter_row",
        "adapter_row_index",
        "sources",
        "coverage_status",
    }
    if (
        not isinstance(origin, dict)
        or set(origin) != expected_origin_fields
        or origin.get("schema_version") != "1.0"
        or json.dumps(
            origin,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        != bridge._origin_json
        or _canonical_digest(origin) != bridge.origin_digest
    ):
        raise RankBridgeError("rank bridge factory origin is invalid")
    raw_task = origin.get("task")
    if not isinstance(raw_task, dict):
        raise RankBridgeError("rank bridge task origin is invalid")
    try:
        origin_task = QueryTask(**raw_task)
    except (KeyError, TypeError, ValueError):
        raise RankBridgeError("rank bridge task origin is invalid") from None
    if origin_task.to_dict() != raw_task:
        raise RankBridgeError("rank bridge task origin is invalid")
    canonical_task = next(
        (
            item
            for item in canonical_plan.tasks
            if item.task_id == origin_task.task_id
        ),
        None,
    )
    if (
        canonical_task is None
        or canonical_task.to_dict() != origin_task.to_dict()
    ):
        raise RankBridgeError(
            "rank bridge task does not match the canonical query task"
        )
    row_index = origin.get("adapter_row_index")
    if (
        not isinstance(row_index, int)
        or isinstance(row_index, bool)
        or row_index < 0
        or row_index >= len(bridge.table.rows)
        or bridge.table.rows[row_index] is not bridge.adapter_row
    ):
        raise RankBridgeError("rank bridge adapter row origin is invalid")
    try:
        visible_origin = {
            "schema_version": "1.0",
            "profile_digest": bridge.profile_digest,
            "query_plan_digest": bridge.query_plan_digest,
            "task": bridge.task.to_dict(),
            "source_policy": {
                "id": bridge.task.source_policy_id,
                "version": bridge.task.source_policy_version,
            },
            "table": bridge.table.to_dict(),
            "adapter_row": bridge.adapter_row.to_dict(),
            "adapter_row_index": row_index,
            "sources": [item.to_dict() for item in bridge.candidates],
            "coverage_status": bridge.coverage_status.value,
        }
    except (AttributeError, TypeError, ValueError):
        raise RankBridgeError("rank bridge visible origin is invalid") from None
    if (
        json.dumps(
            visible_origin,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        != bridge._origin_json
        or bridge.profile_digest != profile.digest
        or bridge.query_plan_digest != _plan_digest(canonical_plan)
    ):
        raise RankBridgeError(
            "rank bridge no longer matches its factory-owned origin"
        )
    expected_bridge_digest = _canonical_digest(
        {
            "profile_digest": bridge.profile_digest,
            "query_plan_digest": bridge.query_plan_digest,
            "task_id": bridge.task.task_id,
            "fact_id": bridge.fact_id,
            "row_hash": bridge.row_hash,
            "artifact_digest": bridge.artifact_digest,
            "provenance_digest": bridge.provenance_digest,
        }
    )
    if bridge.bridge_digest != expected_bridge_digest:
        raise RankBridgeError("rank bridge identity digest disagrees")
    rebuilt = bridge_rank_evidence(
        profile=profile,
        plan=canonical_plan,
        task=canonical_task,
        table=bridge.table,
        extracted_row=bridge.adapter_row,
        candidates=bridge.candidates,
        coverage_status=bridge.coverage_status,
    )
    if (
        rebuilt.to_dict() != bridge.to_dict()
        or rebuilt._origin_json != bridge._origin_json
    ):
        raise RankBridgeError("rank bridge no longer matches its authenticated inputs")
    return bridge


def _replay_rank_evidence_fact(
    fact: Mapping[str, Any],
    profile: PlanningProfile,
    plan: QueryPlan,
) -> RankEvidenceBridge:
    """Rebuild a persisted fact from its canonical typed input projection."""

    if not isinstance(fact, Mapping):
        raise TypeError("fact must be a persisted evidence mapping")
    value = fact.get("value")
    if not isinstance(value, Mapping):
        raise RankBridgeError("persisted rank fact value is invalid")
    projection = _exact_mapping(
        value.get("input_projection"),
        {
            "task_id",
            "row",
            "coverage",
            "extraction_method",
            "locator_hash",
            "sources",
        },
        "rank input projection",
    )
    if value.get("content_hash") != _canonical_digest(dict(projection)):
        raise RankBridgeError("rank input projection content hash disagrees")
    task_id = projection["task_id"]
    task = next((item for item in plan.tasks if item.task_id == task_id), None)
    if task is None:
        raise RankBridgeError("rank input task is detached from the canonical plan")
    table = _table_from_projection(projection)
    sources_value = projection["sources"]
    if isinstance(sources_value, (str, bytes, bytearray)):
        raise RankBridgeError("rank input sources must be an ordered collection")
    try:
        sources = tuple(_candidate_from_projection(item) for item in sources_value)
        coverage_status = EvidenceStatus(value["coverage_status"])
    except (KeyError, TypeError, ValueError):
        raise RankBridgeError("rank input trust projection is invalid") from None
    rebuilt = bridge_rank_evidence(
        profile=profile,
        plan=plan,
        task=task,
        table=table,
        extracted_row=table.rows[0],
        candidates=sources,
        coverage_status=coverage_status,
    )
    if rebuilt.fact.to_dict() != dict(fact):
        raise RankBridgeError("persisted rank fact does not match its typed input")
    return rebuilt


__all__ = [
    "RankBridgeError",
    "RankEvidenceBridge",
    "bridge_rank_evidence",
    "validate_rank_evidence_bridge",
]
