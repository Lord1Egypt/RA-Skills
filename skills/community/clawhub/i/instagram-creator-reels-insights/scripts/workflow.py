#!/usr/bin/env python3
"""Deterministic offline selection and transcript reconciliation; no network or persistence."""
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

class ContractError(ValueError):
    pass

TRACKING = {"igsh", "igshid", "fbclid", "gclid"}

def validate_settings(settings):
    if not isinstance(settings, dict):
        raise ContractError("settings must be an object")
    cap = settings.get("per_creator_limit")
    if type(cap) is not int or cap <= 0:
        raise ContractError("per_creator_limit must be a positive integer")
    accounts = settings.get("accounts")
    if not isinstance(accounts, list) or not accounts:
        raise ContractError("accounts must be a non-empty list")
    normalized = []
    for raw in accounts:
        if not isinstance(raw, str):
            raise ContractError("account entries must be strings")
        value = raw.strip()
        if value.startswith("@"):
            value = value[1:]
        if "://" in value:
            try:
                u = urlsplit(value)
                if (u.scheme != "https" or u.hostname not in ("instagram.com", "www.instagram.com")
                        or u.query or u.fragment or not re.fullmatch(r"/[A-Za-z0-9._]{1,30}/?", u.path)):
                    raise ValueError
                value = u.path.strip("/")
            except ValueError:
                raise ContractError("unsupported or ambiguous Instagram profile URL")
        if not re.fullmatch(r"[A-Za-z0-9._]{1,30}", value) or value in {".", ".."}:
            raise ContractError("invalid Instagram username")
        normalized.append(value.lower())
    if len(set(normalized)) != len(normalized):
        raise ContractError("duplicate accounts after normalization")
    return {"per_creator_limit": cap, "accounts": normalized,
            "save_consent": settings.get("save_consent") is True}

def parse_time(value, numeric_unit=None):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if numeric_unit != "unix_seconds":
            return None
        try:
            return datetime.fromtimestamp(value, tz=timezone.utc)
        except (OverflowError, OSError, ValueError):
            return None
    if not isinstance(value, str):
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc) if dt.tzinfo else None
    except ValueError:
        return None

def window(now, mode):
    end = parse_time(now)
    if end is None or mode not in ("daily", "weekly"):
        raise ContractError("now must be timezone-aware ISO-8601 and mode daily or weekly")
    start = end - (timedelta(hours=24) if mode == "daily" else timedelta(days=7))
    return {"start_utc": start.isoformat().replace("+00:00", "Z"),
            "end_utc_exclusive": end.isoformat().replace("+00:00", "Z")}

def canonical_post_url(value):
    if not isinstance(value, str):
        return None
    try:
        u = urlsplit(value.strip())
        if u.scheme.lower() not in ("https", "http") or u.hostname not in ("instagram.com", "www.instagram.com", "m.instagram.com"):
            return None
        if u.username or u.password or u.port not in (None, 80, 443):
            return None
        match = re.fullmatch(r"/(p|reel|reels|tv)/([A-Za-z0-9_-]+)/?", u.path)
        if not match:
            return None
        query = []
        for key, val in parse_qsl(u.query, keep_blank_values=True):
            low = key.lower()
            if low in TRACKING or low.startswith("utm_"):
                continue
            query.append((key, val))
        query.sort()
        kind = "reel" if match.group(1) in ("reel", "reels") else match.group(1)
        return urlunsplit(("https", "www.instagram.com", f"/{kind}/{match.group(2)}/",
                           urlencode(query), ""))
    except ValueError:
        return None

def require_post_contract(contract):
    keys = ("creator", "url", "timestamp", "type", "id")
    if not isinstance(contract, dict) or any(not isinstance(contract.get(k), str) or not contract[k] for k in keys):
        raise ContractError("interface_error: exact Profile Posts output field contract is missing")
    if contract.get("video_values") != ["Video"]:
        raise ContractError('interface_error: only the exact type value "Video" is eligible for transcription')
    if contract.get("non_video_values") != []:
        raise ContractError("interface_error: additional non-video type mappings are not supported")
    if any(not isinstance(value, str) or not value for value in contract["video_values"] + contract["non_video_values"]):
        raise ContractError("interface_error: media type values must be verified non-empty strings")
    if contract.get("id_kind") not in {"code", "pk"}:
        raise ContractError("interface_error: verified stable ID kind must be code or pk")

def _selection_metadata_error(accounts, code, missing, detail):
    counts = {}
    for account in accounts if isinstance(accounts, list) else []:
        if isinstance(account, str) and account:
            counts[account.lower()] = {"returned_raw_rows": None,
                "discovered_returned_in_window": 0, "type_video_candidates": 0,
                "selected": 0, "omitted_by_cap_observed": 0,
                "coverage_status": "unknown", "additional_candidates_unknown": True,
                "possible_results_limit_reached": None, "results_limit_scope_unknown": True,
                "run_coverage": [], "out_of_window": 0,
                "unknown_media_type": 0, "timestamp_unverified": 0,
                "multi_username_run_observed": False,
                "results_limit_per_creator_unattributed": False,
                "row_issue_count": 0}
    return {"status": "partial_interface_error", "coverage_status": "unknown", "selected": [],
            "counts": counts, "unresolved": [], "run_coverage": [],
            "interface_errors": [{"code": code, "missing": missing, "detail": detail}],
            "row_interface_error_count": 0, "identity_conflict_count": 0,
            "run_failures": [], "unattributed_issue_count": 0,
            "possible_results_limit_reached": None}

def _verified_retrieval_completeness(bundle):
    value = bundle.get("retrieval_complete")
    evidence = bundle.get("retrieval_complete_evidence")
    preserved_evidence = dict(evidence) if isinstance(evidence, dict) else None

    def insufficient_or_malformed(conflict=False, keep_evidence=False):
        retained = preserved_evidence if value is False or keep_evidence else None
        return (False if value is False else None, retained, conflict)

    if not isinstance(evidence, dict):
        return insufficient_or_malformed()
    if (not isinstance(evidence.get("source"), str) or not evidence["source"].strip()
            or not isinstance(evidence.get("detail"), str) or not evidence["detail"].strip()):
        return insufficient_or_malformed()

    count_fields = ("dataset_total", "result_count", "returned_items", "model_visible_rows")
    if any(field in evidence and evidence[field] is not None
           and (type(evidence[field]) is not int or evidence[field] < 0)
           for field in count_fields):
        return insufficient_or_malformed()
    bool_fields = ("truncated", "truncation_marker_detected", "json_complete",
                   "has_more", "all_pages_read")
    if any(field in evidence and evidence[field] is not None
           and type(evidence[field]) is not bool for field in bool_fields):
        return insufficient_or_malformed()
    markers = evidence.get("truncation_markers", [])
    if (not isinstance(markers, list)
            or any(not isinstance(marker, str) or not marker.strip() for marker in markers)):
        return insufficient_or_malformed()
    next_offset_kind = evidence.get("next_offset_kind")
    if next_offset_kind is not None and not isinstance(next_offset_kind, str):
        return insufficient_or_malformed()
    normalized_next_offset_kind = (next_offset_kind.strip().casefold()
                                   if isinstance(next_offset_kind, str) else None)
    if next_offset_kind is not None and normalized_next_offset_kind not in {"exact", "speculative"}:
        return (False if value is False else None, preserved_evidence, True)
    next_offset = evidence.get("next_offset")
    if next_offset is not None and (type(next_offset) is not int or next_offset < 0):
        return insufficient_or_malformed()
    terminal_cursor_conflict = (
        evidence.get("has_more") is False
        and (next_offset is not None or normalized_next_offset_kind == "speculative"))

    # Keep the caller's evidence intact for audit; the helper cannot authenticate it.
    visible_rows = len(bundle["posts"]) if isinstance(bundle.get("posts"), list) else None
    model_visible_rows = evidence.get("model_visible_rows", visible_rows)
    if visible_rows is None or model_visible_rows is None:
        return insufficient_or_malformed()
    if model_visible_rows > visible_rows:
        return False, preserved_evidence, value is True
    if model_visible_rows < visible_rows:
        return insufficient_or_malformed(conflict=value is True, keep_evidence=True)

    explicit_incomplete = (
        evidence.get("truncated") is True
        or evidence.get("truncation_marker_detected") is True
        or bool(markers)
        or evidence.get("json_complete") is False
        or evidence.get("has_more") is True
        or evidence.get("all_pages_read") is False
    )
    if explicit_incomplete:
        return False, preserved_evidence, value is True or terminal_cursor_conflict

    if terminal_cursor_conflict:
        return (False if value is False else None), preserved_evidence, True

    for field in ("dataset_total", "result_count", "returned_items"):
        count = evidence.get(field)
        if count is not None and count > model_visible_rows:
            return False, preserved_evidence, value is True
        if count is not None and count < model_visible_rows:
            return insufficient_or_malformed(conflict=value is True, keep_evidence=True)

    if value is False:
        complete_claim = evidence.get("json_complete") is True and (
            (evidence.get("dataset_total") is not None
             and evidence["dataset_total"] == model_visible_rows)
            or (evidence.get("all_pages_read") is True
                and evidence.get("has_more") is False))
        return False, preserved_evidence, complete_claim
    if value is not True or evidence.get("json_complete") is not True:
        return None, preserved_evidence, False

    dataset_total_matches = (evidence.get("dataset_total") is not None
                             and evidence["dataset_total"] == model_visible_rows)
    terminal_page_verified = (evidence.get("all_pages_read") is True
                              and evidence.get("has_more") is False)
    # next_offset_kind describes the cursor emitted by the page represented here.
    # A speculative cursor on that same page conflicts with either terminal proof.
    speculative_terminal_conflict = (
        normalized_next_offset_kind == "speculative" and (dataset_total_matches or terminal_page_verified))
    if speculative_terminal_conflict:
        return None, preserved_evidence, True
    if dataset_total_matches or terminal_page_verified:
        return True, preserved_evidence, False
    return None, preserved_evidence, False

def select_posts(runs, accounts, cap, start, end, contract, display_timezone="UTC"):
    """Select posts from per-run bundles; limit checks always use pre-filter run rows."""
    require_post_contract(contract)
    if not isinstance(accounts, list) or any(not isinstance(a, str) or not a for a in accounts):
        raise ContractError("accounts must be an array of non-empty usernames")
    if not isinstance(runs, list) or not runs:
        return _selection_metadata_error(accounts, "missing_run_boundary", ["runs"],
                                         "Per-run posts, usernames, and resultsLimit metadata are required")
    if type(cap) is not int or cap <= 0:
        raise ContractError("per_creator_limit must be a positive integer")
    wanted = {a.lower() for a in accounts}
    lo, hi = parse_time(start), parse_time(end)
    if lo is None or hi is None or hi <= lo:
        raise ContractError("invalid half-open report window")
    if not isinstance(display_timezone, str) or not display_timezone.strip():
        raise ContractError("display_timezone must be a non-empty IANA timezone name")
    display_timezone = display_timezone.strip()
    try:
        display_tz = ZoneInfo(display_timezone)
    except (ZoneInfoNotFoundError, ValueError):
        raise ContractError("display_timezone must be a valid IANA timezone name")
    by_creator = {a: [] for a in wanted}
    unresolved, seen, seen_ids = [], {}, {}
    row_error_count = 0
    identity_conflict_count = 0
    unattributed_issue_count = 0
    classifications = {a: {"out_of_window": 0, "unknown_media_type": 0,
                           "discovered_returned_in_window": 0,
                           "timestamp_unverified": 0, "returned_raw_rows": 0,
                           "additional_candidates_unknown": False, "run_coverage": [],
                           "multi_username_run_observed": False,
                           "results_limit_per_creator_unattributed": False,
                           "row_issue_count": 0}
                       for a in wanted}
    normalized_runs, missing_run_fields, used_run_ids, run_failures = [], [], set(), []
    row_identity_fallback_run_ids = set()

    def preserve_unattributable_bundle_rows(bundle, run_index, missing_fields):
        nonlocal row_error_count, unattributed_issue_count
        posts = bundle.get("posts") if isinstance(bundle, dict) else None
        if not isinstance(posts, list):
            return
        run_id = bundle.get("run_id")
        for row_index, row in enumerate(posts):
            unresolved.append({"row": row, "run_id": run_id, "run_index": run_index,
                               "row_index": row_index, "status": "interface_error",
                               "reason": "discovery bundle metadata is incomplete; row cannot be safely assigned",
                               "missing_run_fields": missing_fields})
            row_error_count += 1
            unattributed_issue_count += 1

    def record_row_attributed_fallback_run(run_record, creator):
        if run_record["run_id"] not in row_identity_fallback_run_ids:
            return
        attributed = run_record["row_attributed_usernames"]
        if creator not in attributed:
            attributed.append(creator)
            classifications[creator]["run_coverage"].append({
                "run_id": run_record["run_id"],
                "status": "run_username_mapping_missing",
                "run_status": run_record["run_status"],
                "results_limit": run_record["results_limit"],
                "raw_returned_rows": run_record["raw_returned_rows"],
                "possible_results_limit_reached": run_record["possible_results_limit_reached"],
                "retrieval_complete": run_record["retrieval_complete"],
                "retrieval_completeness_evidence": run_record["retrieval_completeness_evidence"],
                "retrieval_completeness_conflict": run_record["retrieval_completeness_conflict"],
                "attributed_via": "row_creator_field"})
            classifications[creator]["returned_raw_rows"] = None
        classifications[creator]["additional_candidates_unknown"] = True
        classifications[creator]["results_limit_scope_unknown"] = True
        classifications[creator]["possible_results_limit_reached"] = None

    for index, bundle in enumerate(runs):
        if not isinstance(bundle, dict):
            missing_run_fields.append({"run_index": index, "missing": ["run_id", "usernames", "results_limit", "posts", "retrieval_complete"]})
            continue
        required_run_fields = ("run_id", "usernames", "results_limit", "posts")
        missing = [field for field in required_run_fields if field not in bundle]
        if missing:
            missing_run_fields.append({"run_index": index, "missing": missing})
            run_id = bundle.get("run_id")
            usernames_missing_only = missing == ["usernames"]
            valid_remaining_metadata = (
                isinstance(run_id, str) and bool(run_id) and run_id not in used_run_ids
                and type(bundle.get("results_limit")) is int and bundle["results_limit"] > 0
                and isinstance(bundle.get("posts"), list)
                and (bundle.get("retrieval_complete") is None or type(bundle.get("retrieval_complete")) is bool)
            )
            if usernames_missing_only and valid_remaining_metadata:
                raw_posts = bundle["posts"]
                normalized_status = (bundle.get("run_status").upper().replace("_", "-")
                                     if isinstance(bundle.get("run_status"), str) else None)
                (retrieval_complete, completeness_evidence,
                 completeness_conflict) = _verified_retrieval_completeness(bundle)
                run_record = {"run_id": run_id, "usernames": [],
                              "results_limit": bundle["results_limit"],
                              "raw_returned_rows": len(raw_posts),
                              "possible_results_limit_reached": len(raw_posts) >= bundle["results_limit"],
                              "coverage_status": "run_username_mapping_missing",
                              "retrieval_complete": retrieval_complete,
                              "retrieval_completeness_evidence": completeness_evidence,
                              "retrieval_completeness_conflict": completeness_conflict,
                              "limit_scope_unknown": True,
                              "run_status": normalized_status,
                              "status_message": bundle.get("status_message"),
                              "error": bundle.get("run_error"), "run_index": index,
                              "row_attributed_usernames": []}
                normalized_runs.append((run_record, set(), raw_posts))
                row_identity_fallback_run_ids.add(run_id)
                used_run_ids.add(run_id)
                if normalized_status in {"FAILED", "ABORTED", "TIMED-OUT"}:
                    run_failures.append({"run_id": run_id, "usernames": [],
                                         "row_attributed_usernames": run_record["row_attributed_usernames"],
                                         "run_status": normalized_status,
                                         "error": bundle.get("run_error"),
                                         "status_message": bundle.get("status_message"),
                                         "coverage_status": "run_username_mapping_missing"})
            else:
                preserve_unattributable_bundle_rows(bundle, index, missing)
            continue
        run_id, usernames = bundle["run_id"], bundle["usernames"]
        limit, raw_posts = bundle["results_limit"], bundle["posts"]
        (retrieval_complete, completeness_evidence,
         completeness_conflict) = _verified_retrieval_completeness(bundle)
        if (not isinstance(run_id, str) or not run_id or run_id in used_run_ids
                or not isinstance(usernames, list) or not usernames
                or any(not isinstance(name, str) or not name for name in usernames)
                or type(limit) is not int or limit <= 0 or not isinstance(raw_posts, list)
                or (bundle.get("retrieval_complete") is not None and type(bundle.get("retrieval_complete")) is not bool)):
            missing_run_fields.append({"run_index": index, "missing": ["valid unique run_id, usernames, positive results_limit, posts array, or retrieval_complete"]})
            preserve_unattributable_bundle_rows(bundle, index,
                                                ["valid unique run_id, usernames, positive results_limit, posts array, or retrieval_complete"])
            continue
        mapped = {name.lower() for name in usernames}
        if not mapped.issubset(wanted):
            missing_run_fields.append({"run_index": index, "missing": ["requested-account mapping"],
                                        "unexpected_usernames": sorted(mapped - wanted)})
            preserve_unattributable_bundle_rows(bundle, index, ["requested-account mapping"])
            continue
        used_run_ids.add(run_id)
        raw_status = bundle.get("run_status")
        normalized_status = raw_status.upper().replace("_", "-") if isinstance(raw_status, str) else None
        known_statuses = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT", "READY", "RUNNING", "ABORTING", "TIMING-OUT"}
        status_known = normalized_status in known_statuses
        actor_succeeded = normalized_status == "SUCCEEDED"
        run_succeeded = actor_succeeded and retrieval_complete is True
        run_failed = normalized_status in {"FAILED", "ABORTED", "TIMED-OUT"}
        run_status_unknown = not status_known
        scope_verified = (bundle.get("results_limit_scope") == "run_total"
                          and bundle.get("results_limit_scope_verified") is True)
        multi_scope_unknown = len(mapped) > 1 and not scope_verified
        reached = len(raw_posts) >= limit
        if run_failed:
            coverage = "run_failed"
        elif run_status_unknown:
            coverage = "run_status_unknown"
        elif not actor_succeeded:
            coverage = "run_incomplete"
        elif retrieval_complete is None:
            coverage = "retrieval_completeness_unknown"
        elif retrieval_complete is False:
            coverage = "retrieval_incomplete"
        elif multi_scope_unknown:
            coverage = "possible_results_limit_reached_scope_unknown" if reached else "unknown_multi_username_limit_scope"
        elif reached:
            coverage = "possible_results_limit_reached"
        else:
            coverage = "returned_below_run_limit"
        run_record = {"run_id": run_id, "usernames": sorted(mapped), "results_limit": limit,
                      "raw_returned_rows": len(raw_posts), "possible_results_limit_reached": reached,
                      "coverage_status": coverage, "retrieval_complete": retrieval_complete,
                      "retrieval_completeness_evidence": completeness_evidence,
                      "retrieval_completeness_conflict": completeness_conflict,
                      "limit_scope_unknown": multi_scope_unknown, "run_status": normalized_status,
                      "status_message": bundle.get("status_message"),
                      "error": bundle.get("run_error"), "run_index": index}
        normalized_runs.append((run_record, mapped, raw_posts))
        if run_failed:
            run_failures.append({"run_id": run_id, "usernames": sorted(mapped),
                                 "row_attributed_usernames": [],
                                 "run_status": normalized_status or "MISSING_OR_UNKNOWN",
                                 "error": bundle.get("run_error"),
                                 "status_message": bundle.get("status_message"),
                                 "coverage_status": coverage})
        for creator in mapped:
            classifications[creator]["run_coverage"].append({
                "run_id": run_id, "status": coverage, "run_status": normalized_status,
                "results_limit": limit, "raw_returned_rows": len(raw_posts),
                "possible_results_limit_reached": reached,
                "retrieval_complete": retrieval_complete,
                "retrieval_completeness_evidence": completeness_evidence,
                "retrieval_completeness_conflict": completeness_conflict})
            if len(mapped) == 1 and classifications[creator]["returned_raw_rows"] is not None:
                classifications[creator]["returned_raw_rows"] += len(raw_posts)
            else:
                # The run rows cannot be apportioned to individual creators from
                # a multi-username run without per-creator grouping evidence.
                classifications[creator]["returned_raw_rows"] = None
            if len(mapped) > 1:
                classifications[creator]["multi_username_run_observed"] = True
                classifications[creator]["results_limit_per_creator_unattributed"] = True
                classifications[creator]["possible_results_limit_reached"] = None
            if multi_scope_unknown:
                classifications[creator]["results_limit_scope_unknown"] = True
                classifications[creator]["possible_results_limit_reached"] = None
                classifications[creator]["additional_candidates_unknown"] = True
            else:
                classifications[creator].setdefault("results_limit_scope_unknown", False)
                classifications[creator].setdefault("possible_results_limit_reached", False)
                if len(mapped) == 1 and not classifications[creator]["multi_username_run_observed"]:
                    classifications[creator]["possible_results_limit_reached"] = (
                        classifications[creator]["possible_results_limit_reached"] or reached)
            classifications[creator]["additional_candidates_unknown"] = (
                    classifications[creator]["additional_candidates_unknown"] or reached or not run_succeeded)
    missing_creators = sorted(wanted - {creator for _, mapped, _ in normalized_runs for creator in mapped})
    if missing_creators:
        missing_run_fields.append({"missing": ["run-to-creator mapping"], "usernames": missing_creators})
        for creator in missing_creators:
            classifications[creator]["additional_candidates_unknown"] = True
            classifications[creator]["results_limit_scope_unknown"] = True
            classifications[creator]["possible_results_limit_reached"] = None
    if missing_run_fields:
        result = _selection_metadata_error(accounts, "invalid_or_missing_run_metadata", missing_run_fields,
                                           "Cannot determine run-local resultsLimit coverage or creator mapping")
        result["run_coverage"] = [record for record, _, _ in normalized_runs]
        result["unresolved"] = unresolved
        result["row_interface_error_count"] = row_error_count
        result["unattributed_issue_count"] = unattributed_issue_count
        if not normalized_runs:
            return result
        # Continue processing identifiable bundles, while preserving the
        # missing-run metadata error and forcing unknown aggregate coverage.

    video_values = set(contract["video_values"])
    required = [contract[k] for k in ("creator", "timestamp", "id")]
    media_type_field = contract["type"]
    raw_index = 0
    for run_record, run_usernames, raw_posts in normalized_runs:
        row_identity_fallback = run_record["run_id"] in row_identity_fallback_run_ids
        for row_index, row in enumerate(raw_posts):
            row_source = {"run_id": run_record["run_id"], "run_index": run_record["run_index"],
                          "row_index": row_index}
            if not isinstance(row, dict) or any(key not in row for key in required):
                if row_identity_fallback:
                    unresolved.append({"row": row, **row_source,
                                       "status": "interface_error",
                                       "reason": "row lacks a required contracted field; creator cannot be verified"})
                    row_error_count += 1
                    unattributed_issue_count += 1
                    raw_index += 1
                    continue
                raise ContractError(f"interface_error: Profile Posts row {raw_index} lacks a required contracted field")
            creator = row[contract["creator"]]
            url = row.get(contract["url"])
            raw_stamp = row[contract["timestamp"]]
            stamp = parse_time(raw_stamp, numeric_unit=contract.get("timestamp_unit"))
            media_type_present = media_type_field in row
            kind = row.get(media_type_field)
            stable_id = row[contract["id"]]
            if not isinstance(creator, str):
                if row_identity_fallback:
                    unresolved.append({"row": row, **row_source,
                                       "status": "interface_error",
                                       "reason": "creator has an invalid contracted type"})
                    row_error_count += 1
                    unattributed_issue_count += 1
                    raw_index += 1
                    continue
                raise ContractError(f"interface_error: Profile Posts row {raw_index} has an invalid creator field type")
            creator = creator.lower()
            canon = canonical_post_url(url)
            ident = str(stable_id) if stable_id not in (None, "") else None
            creator_matches_request = creator in wanted
            creator_matches_run = creator in run_usernames
            if not creator_matches_run and not (row_identity_fallback and creator_matches_request):
                unresolved.append({"row": row, **row_source, "status": "interface_error",
                                   "reason": "creator cannot be verified against the missing run mapping"})
                row_error_count += 1
                if creator in classifications:
                    classifications[creator]["row_issue_count"] += 1
                else:
                    unattributed_issue_count += 1
                raw_index += 1
                continue
            is_video_type = media_type_present and isinstance(kind, str) and kind == "Video"
            if stamp is None:
                classifications[creator]["timestamp_unverified"] += 1
                issue = {"row": row, **row_source, "status": "timestamp_unverified",
                         "field": contract["timestamp"], "field_present": True,
                         "value": raw_stamp,
                         "reason": "timestamp type, unit, or timezone is not verified or parseable"}
                if not is_video_type:
                    issue.update({"field": media_type_field, "field_present": media_type_present,
                                  "value": kind})
                unresolved.append(issue)
                raw_index += 1
                continue
            if not lo <= stamp < hi:
                classifications[creator]["out_of_window"] += 1
                issue = {"row": row, **row_source, "status": "out_of_window"}
                if not is_video_type:
                    issue.update({"field": media_type_field, "field_present": media_type_present,
                                  "value": kind})
                unresolved.append(issue)
                raw_index += 1
                continue
            if canon is not None:
                classifications[creator]["discovered_returned_in_window"] += 1
            if not is_video_type:
                classifications[creator]["unknown_media_type"] += 1
                unresolved.append({"row": row, **row_source, "status": "unknown_media_type",
                                   "field": media_type_field, "field_present": media_type_present,
                                   "value": kind})
                raw_index += 1
                continue
            if canon is None:
                unresolved.append({"row": row, **row_source, "status": "interface_error",
                                   "reason": "confirmed Video row has no usable Instagram post URL"})
                row_error_count += 1
                classifications[creator]["row_issue_count"] += 1
                raw_index += 1
                continue
            key = ("url", canon)
            if key in seen:
                prior = seen[key]
                if (prior["creator"] != creator or prior["stable_id"] and ident and prior["stable_id"] != ident
                        or prior["timestamp"] != stamp):
                    reason = ("same canonical URL has conflicting creator, stable ID, or timestamp evidence")
                    unresolved.append({"row": row, **row_source, "status": "identity_conflict",
                                       "reason": reason, "conflicts_with": prior["index"]})
                    identity_conflict_count += 1
                    classifications[creator]["row_issue_count"] += 1
                    prior_creator = prior["creator"]
                    if prior_creator in classifications:
                        classifications[prior_creator]["row_issue_count"] += 1
                else:
                    if (row_identity_fallback and creator_matches_request and stamp is not None
                            and lo <= stamp < hi and isinstance(kind, str) and kind in video_values):
                        record_row_attributed_fallback_run(run_record, creator)
                    unresolved.append({"row": row, **row_source, "status": "duplicate_candidate", "duplicate_of": prior["index"]})
                raw_index += 1
                continue
            if ident and ident in seen_ids and seen_ids[ident]["url"] != canon:
                unresolved.append({"row": row, **row_source, "status": "identity_conflict",
                                   "reason": "same stable ID maps to a different canonical URL",
                                   "conflicts_with": seen_ids[ident]["index"]})
                identity_conflict_count += 1
                classifications[creator]["row_issue_count"] += 1
                prior_row = seen_ids[ident]
                prior_creator = prior_row.get("creator")
                if prior_creator in classifications:
                    classifications[prior_creator]["row_issue_count"] += 1
                raw_index += 1
                continue
            if (row_identity_fallback and creator_matches_request and stamp is not None
                    and lo <= stamp < hi and isinstance(kind, str) and kind in video_values):
                record_row_attributed_fallback_run(run_record, creator)
            seen[key] = {"creator": creator, "stable_id": ident, "timestamp": stamp, "index": raw_index}
            if ident:
                seen_ids[ident] = {"url": canon, "index": raw_index, "creator": creator}
            if kind in video_values:
                by_creator[creator].append({"row": row, "creator": creator, "url": canon, "stable_id": ident,
                                           "stable_id_kind": contract["id_kind"], "timestamp": stamp,
                                           "published_at_utc": stamp.isoformat().replace("+00:00", "Z"),
                                           "published_at_local": stamp.astimezone(display_tz).isoformat(),
                                           "display_timezone": display_timezone,
                                           "source_run_id": run_record["run_id"],
                                           "source_run_index": run_record["run_index"]})
            raw_index += 1
    at_limit_possible = any(record["possible_results_limit_reached"] for record, _, _ in normalized_runs)
    unknown_scope = any(record["limit_scope_unknown"] for record, _, _ in normalized_runs)
    selected, counts = [], {}
    for creator, rows in by_creator.items():
        rows.sort(key=lambda x: x["timestamp"], reverse=True)
        chosen = rows[:cap]
        for item in chosen:
            item.pop("timestamp", None)
        selected.extend(chosen)
        creator_run_records = classifications[creator]["run_coverage"]
        creator_unknown = (classifications[creator].get("results_limit_scope_unknown", False)
                           or any(item["status"] in {"run_status_unknown", "retrieval_completeness_unknown"}
                                  for item in creator_run_records))
        creator_partial = (classifications[creator]["row_issue_count"] > 0
                           or classifications[creator]["additional_candidates_unknown"]
                           or len(rows) > len(chosen)
                           or classifications[creator]["unknown_media_type"] > 0
                           or classifications[creator]["timestamp_unverified"] > 0
                           or bool(classifications[creator].get("possible_results_limit_reached")))
        creator_partial = creator_partial or any(item["status"] not in {
            "returned_below_run_limit", "possible_results_limit_reached",
            "unknown_multi_username_limit_scope", "possible_results_limit_reached_scope_unknown"
        } for item in creator_run_records)
        counts[creator] = {"discovered_returned_in_window": classifications[creator]["discovered_returned_in_window"],
                           "type_video_candidates": len(rows),
                           "returned_raw_rows": classifications[creator]["returned_raw_rows"], "selected": len(chosen),
                           "omitted_by_cap_observed": max(0, len(rows)-len(chosen)),
                           "coverage_status": "unknown" if creator_unknown else ("partial" if creator_partial or len(rows) > len(chosen) else "complete"),
                           "additional_candidates_unknown": classifications[creator]["additional_candidates_unknown"],
                           "possible_results_limit_reached": classifications[creator].get("possible_results_limit_reached"),
                           "results_limit_scope_unknown": classifications[creator].get("results_limit_scope_unknown", False),
                           "run_coverage": classifications[creator]["run_coverage"],
                           **classifications[creator]}
    unknown_types = any(counts[a]["unknown_media_type"] for a in counts)
    omitted = any(counts[a]["omitted_by_cap_observed"] for a in counts)
    unverified_times = any(counts[a]["timestamp_unverified"] for a in counts)
    run_incomplete = any(not (record["run_status"] == "SUCCEEDED" and record["retrieval_complete"])
                         for record, _, _ in normalized_runs)
    row_issues = identity_conflict_count > 0 or row_error_count > 0
    incomplete = (unknown_scope or at_limit_possible or omitted or unverified_times or unknown_types
                  or run_incomplete
                  or any(counts[a]["row_issue_count"] for a in counts)
                  or unattributed_issue_count > 0 or bool(missing_run_fields))
    if row_error_count or missing_run_fields:
        status = "partial_interface_error"
    elif incomplete:
        status = "partial"
    elif selected:
        status = "complete"
    else:
        status = "no_candidates"
    coverage_unknown = (unknown_scope or unattributed_issue_count > 0 or bool(missing_run_fields)
                        or any(record["coverage_status"] in {"run_status_unknown", "retrieval_completeness_unknown"}
                               for record, _, _ in normalized_runs))
    interface_errors = ([{"code": "invalid_or_missing_run_metadata", "missing": missing_run_fields}]
                        if missing_run_fields else [])
    return {"status": status, "selected": selected, "counts": counts, "unresolved": unresolved,
            "coverage_status": "unknown" if coverage_unknown else ("partial" if incomplete else "complete"),
            "run_coverage": [record for record, _, _ in normalized_runs],
            "run_failures": run_failures, "row_interface_error_count": row_error_count,
            "identity_conflict_count": identity_conflict_count,
            "unattributed_issue_count": unattributed_issue_count,
            "interface_errors": interface_errors,
            "possible_results_limit_reached": at_limit_possible}

def reconcile_transcripts(submitted, rows, run_status, dataset_complete, post_contract, transcript_contract, run_error=None):
    require_post_contract(post_contract)
    names = ("url", "code", "pk", "creator", "text", "segments", "error", "segment_text")
    if not isinstance(transcript_contract, dict) or any(not isinstance(transcript_contract.get(k), str) or not transcript_contract[k] for k in names):
        raise ContractError("interface_error: exact Transcript output field contract is missing")
    if not isinstance(submitted, list) or not isinstance(rows, list):
        raise ContractError("interface_error: submitted candidates and transcript rows must be arrays")
    if not submitted:
        raise ContractError("interface_error: reconcile requires at least one submitted Video candidate")
    if dataset_complete is not None and type(dataset_complete) is not bool:
        raise ContractError("dataset_complete must be true, false, or unknown/null")
    if isinstance(run_status, str):
        run_status = run_status.upper().replace("_", "-")
    if run_status not in {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT", "READY", "RUNNING", "ABORTING", "TIMING-OUT", "UNKNOWN"}:
        raise ContractError("unrecognized run status")
    if isinstance(run_error, str):
        run_error = run_error.strip() or None
    else:
        run_error = None
    post_id_kind = transcript_contract.get("post_id_kind")
    if post_id_kind not in {"code", "pk"}:
        raise ContractError("interface_error: verified post stable-ID kind is missing")
    if post_id_kind != post_contract["id_kind"]:
        raise ContractError("interface_error: Profile Posts and Transcript stable ID kinds differ; no verified mapping exists")
    by_url, by_id = {}, {}
    for post in submitted:
        by_url.setdefault(post["url"], []).append(post)
        if post.get("stable_id"):
            by_id.setdefault((post_id_kind, str(post["stable_id"])), []).append(post)
    results = {}
    failed_statuses = {"FAILED", "ABORTED", "TIMED-OUT"}
    for p in submitted:
        prior = results.get(p["url"])
        if prior:
            prior["status"] = "duplicate_candidate"
            prior["dataset_complete"] = dataset_complete
            prior["reason"] = "Duplicate candidate in submitted list"
            prior.setdefault("duplicates", []).append(p)
        else:
            result = {"post": p, "dataset_complete": dataset_complete, "run_status": run_status}
            if run_status in failed_statuses:
                result.update({"status": "run_failed", "reason": run_error or f"Transcript Actor run ended with {run_status}",
                               "error": run_error})
            elif run_status in {"READY", "RUNNING", "ABORTING", "TIMING-OUT", "UNKNOWN"}:
                result.update({"status": "pending", "reason": "Transcript Actor run has not reached a confirmed terminal state"})
            elif run_status == "SUCCEEDED" and dataset_complete is not True:
                reason = ("Transcript Dataset is explicitly incomplete" if dataset_complete is False
                          else "Transcript Dataset completeness is unknown")
                result.update({"status": "pending", "reason": reason})
            else:
                result["status"] = "not_returned"
            results[p["url"]] = result
    row_counts, conflicted_posts = {}, set()
    url_field, code_field, pk_field, creator_field = (transcript_contract[k] for k in ("url", "code", "pk", "creator"))
    id_field = pk_field if post_id_kind == "pk" else code_field
    def mark_conflict(posts, row, row_index, reason):
        for candidate in posts:
            if candidate["url"] in results:
                results[candidate["url"]] = {"post": candidate, "row": row,
                    "dataset_complete": dataset_complete,
                    "run_status": run_status,
                    "status": "identity_conflict", "reason": reason, "row_index": row_index}
                conflicted_posts.add(candidate["url"])

    for row_index, row in enumerate(rows):
        if not isinstance(row, dict):
            results[f"unassigned:{row_index}"] = {"row": row, "dataset_complete": dataset_complete, "status": "schema_invalid"}
            continue
        if url_field not in row:
            results[f"unassigned:{row_index}"] = {"row": row, "dataset_complete": dataset_complete, "status": "schema_invalid", "reason": "URL field is missing"}
            continue
        raw_url = row.get(url_field)
        canon = canonical_post_url(raw_url) if raw_url is not None else None
        ident = row.get(id_field)
        id_candidates = by_id.get((post_id_kind, str(ident)), []) if ident not in (None, "") else []
        if raw_url is not None and canon is None:
            if id_candidates:
                mark_conflict(id_candidates, row, row_index, "transcript URL is invalid but the stable ID points to a submitted post")
            else:
                results[f"unassigned:{row_index}"] = {"row": row, "dataset_complete": dataset_complete, "status": "schema_invalid", "reason": "invalid transcript URL"}
            continue
        if raw_url is None and not id_candidates:
            results[f"unassigned:{row_index}"] = {"row": row, "dataset_complete": dataset_complete, "status": "schema_invalid"}
            continue
        url_candidates = by_url.get(canon, []) if canon else []
        if url_candidates and ident not in (None, "") and any(
                p.get("stable_id") and str(p["stable_id"]) != str(ident) for p in url_candidates):
            mark_conflict(url_candidates + id_candidates, row, row_index, "transcript URL and stable ID identify different posts")
            continue
        if url_candidates and id_candidates:
            url_keys = {p["url"] for p in url_candidates}
            id_keys = {p["url"] for p in id_candidates}
            if url_keys != id_keys:
                mark_conflict(url_candidates + id_candidates, row, row_index, "transcript URL and stable ID identify different submitted posts")
                continue
        if raw_url is not None and not url_candidates and id_candidates:
            mark_conflict(id_candidates, row, row_index, "transcript URL points to a different post than the stable ID")
            continue
        candidates = url_candidates or id_candidates
        if not candidates:
            results[f"unassigned:{row_index}"] = {"row": row, "dataset_complete": dataset_complete, "status": "unmatched"}
            continue
        if len(candidates) != 1:
            mark_conflict(candidates, row, row_index, "transcript identity matches more than one submitted post")
            continue
        post = candidates[0]
        if post["url"] in conflicted_posts:
            results[post["url"]].setdefault("conflicting_rows", []).append(row)
            continue
        returned_creator = row.get(creator_field)
        if returned_creator not in (None, ""):
            if not isinstance(returned_creator, str):
                mark_conflict([post], row, row_index, "transcript creator field has an invalid type")
                continue
            if returned_creator.strip().lstrip("@").casefold() != str(post.get("creator", "")).strip().lstrip("@").casefold():
                mark_conflict([post], row, row_index, "transcript creator differs from the submitted post owner")
                continue
        text_key, seg_key, error_key = (transcript_contract[k] for k in ("text", "segments", "error"))
        row_counts[post["url"]] = row_counts.get(post["url"], 0) + 1
        if row_counts[post["url"]] > 1:
            previous = results[post["url"]]
            prior_rows = previous.get("rows", [previous["row"]])
            results[post["url"]] = {"post": post, "rows": prior_rows + [row],
                                     "dataset_complete": dataset_complete,
                                     "run_status": run_status,
                                     "status": "duplicate_transcript_rows"}
            continue
        if error_key in row and not isinstance(row[error_key], (str, type(None))):
            status, transcript = "schema_invalid", None
        elif error_key in row and row[error_key] not in (None, ""):
            status, transcript = "failed", None
        elif text_key not in row:
            segments = row.get(seg_key)
            segment_text_key = transcript_contract["segment_text"]
            if seg_key in row and not isinstance(segments, list):
                status, transcript = "schema_invalid", None
            elif isinstance(segments, list) and segments and all(isinstance(s, dict) and isinstance(s.get(segment_text_key), str) for s in segments):
                status, transcript = "segments_only", None
            elif isinstance(segments, list) and any(not isinstance(s, dict) or segment_text_key not in s or not isinstance(s.get(segment_text_key), str) for s in segments):
                status, transcript = "schema_invalid", None
            else:
                status, transcript = "schema_missing_text", None
        elif not isinstance(row[text_key], str):
            status, transcript = "schema_invalid", None
        elif not row[text_key].strip():
            status, transcript = "empty", ""
        else:
            status, transcript = "success", row[text_key]
        results[post["url"]] = {"post": post, "row": row, "transcript": transcript,
                                 "dataset_complete": dataset_complete, "run_status": run_status,
                                 "status": status}
    return list(results.values())

def split_batches(urls, batch_size):
    if not isinstance(urls, list) or any(not isinstance(url, str) or not url for url in urls):
        raise ContractError("urls must be a list of non-empty strings")
    if type(batch_size) is not int or batch_size <= 0:
        raise ContractError("batch_size must come from a verified live limit")
    return [urls[i:i+batch_size] for i in range(0, len(urls), batch_size)]

def main():
    try:
        req = json.load(sys.stdin)
        op = req.get("operation")
        if op == "settings": result = validate_settings(req.get("settings"))
        elif op == "window": result = window(req.get("now"), req.get("mode"))
        elif op == "select": result = select_posts(req.get("runs"), req.get("accounts"), req.get("per_creator_limit"), req.get("start"), req.get("end_exclusive"), req.get("post_contract"), req.get("display_timezone", "UTC"))
        elif op == "split": result = {"batches": split_batches(req.get("urls"), req.get("batch_size"))}
        elif op == "reconcile":
            result = {"results": reconcile_transcripts(req.get("submitted"), req.get("rows"), req.get("run_status"), req.get("dataset_complete"), req.get("post_contract"), req.get("transcript_contract"), req.get("run_error"))}
        else: raise ContractError("unknown operation")
        print(json.dumps(result, ensure_ascii=False, default=lambda x: x.isoformat()))
    except (ContractError, TypeError, AttributeError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
