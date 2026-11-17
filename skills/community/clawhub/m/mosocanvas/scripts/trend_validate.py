#!/usr/bin/env python3
"""Validate freshness, independence, and evidence diversity of a trend snapshot."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


def parse_time(value: Any, label: str, blockers: list[str]) -> datetime | None:
    if not isinstance(value, str):
        blockers.append(f"{label} must be an ISO 8601 timestamp")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        blockers.append(f"{label} is not a valid ISO 8601 timestamp")
        return None
    if parsed.tzinfo is None:
        blockers.append(f"{label} must include a timezone")
        return None
    return parsed.astimezone(timezone.utc)


def canonical_domain(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return (urlparse(value).hostname or "").lower().removeprefix("www.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a trend snapshot; this script does not browse or collect."
    )
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--at", help="ISO 8601 time used for reproducible freshness tests")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    blockers: list[str] = []
    warnings: list[str] = []
    try:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        snapshot = {}
        blockers.append(f"snapshot cannot be loaded: {exc}")
    if not isinstance(snapshot, dict):
        snapshot = {}
        blockers.append("snapshot must be a JSON object")

    if snapshot.get("schema") != "moso.trend-snapshot/0.2":
        blockers.append("snapshot must use moso.trend-snapshot/0.2")

    captured = parse_time(snapshot.get("captured_at"), "captured_at", blockers)
    expires = parse_time(snapshot.get("expires_at"), "expires_at", blockers)
    now = parse_time(args.at, "--at", blockers) if args.at else datetime.now(timezone.utc)
    if captured and expires and expires <= captured:
        blockers.append("expires_at must be later than captured_at")
    if expires and now and now > expires:
        blockers.append("snapshot is stale")
    if captured and now and captured > now:
        blockers.append("captured_at cannot be in the future")

    collection = snapshot.get("collection") or {}
    baseline = snapshot.get("baseline") or {}
    review = snapshot.get("review") or {}
    if collection.get("status") != "complete":
        blockers.append("trend snapshot collection must be complete")
    requested_classes = collection.get("source_classes_requested") or []
    if len(set(requested_classes)) < 3:
        blockers.append("collection must request at least three source classes")
    if baseline.get("window_days") != 7:
        blockers.append("trend baseline window must be seven days")
    prior_refs = baseline.get("prior_snapshot_refs") or []

    if review.get("disposition") != "accepted":
        blockers.append("independent trend review must accept the snapshot")
    if review.get("collector_independent") is not True:
        blockers.append("trend reviewer must be independent from collection")
    if review.get("source_identity_checked") is not True:
        blockers.append("trend reviewer must check source identity")
    if review.get("literal_copy_risk_checked") is not True:
        blockers.append("trend reviewer must check literal-copy risk")
    if collection.get("collector_id") == review.get("reviewer_id"):
        blockers.append("collector and reviewer identities must differ")
    if collection.get("collector_context_id") == review.get("reviewer_context_id"):
        blockers.append("collector and reviewer contexts must differ")

    sources = snapshot.get("sources")
    if not isinstance(sources, list) or len(sources) < 3:
        blockers.append("snapshot requires at least three sources")
        sources = []
    source_index: dict[str, dict[str, Any]] = {}
    urls: set[str] = set()
    source_classes: set[str] = set()
    for index, source in enumerate(sources, start=1):
        prefix = f"source {index}"
        if not isinstance(source, dict):
            blockers.append(f"{prefix} must be an object")
            continue
        source_id = str(source.get("id", ""))
        if not source_id or source_id in source_index:
            blockers.append(f"{prefix} has a duplicate or empty id")
        else:
            source_index[source_id] = source
        url = str(source.get("url", ""))
        if not canonical_domain(url):
            blockers.append(f"{prefix} has an invalid URL")
        if not url or url in urls:
            blockers.append(f"{prefix} has a duplicate or empty URL")
        urls.add(url)
        source_classes.add(str(source.get("source_class", "")))
        observed = parse_time(source.get("observed_at"), f"{prefix} observed_at", blockers)
        source_captured = parse_time(
            source.get("captured_at"), f"{prefix} captured_at", blockers
        )
        if observed and source_captured and observed > source_captured:
            blockers.append(f"{prefix} observed_at cannot follow captured_at")
        if source_captured and captured and source_captured > captured:
            blockers.append(f"{prefix} captured_at cannot follow snapshot captured_at")
    if len(source_classes) < 3:
        blockers.append("snapshot must contain at least three source classes")
    if not set(requested_classes).issubset(source_classes):
        blockers.append("requested source classes are not all represented")

    signals = snapshot.get("signals")
    if not isinstance(signals, list) or not signals:
        blockers.append("snapshot requires at least one signal")
        signals = []
    signal_ids: set[str] = set()
    for index, signal in enumerate(signals, start=1):
        prefix = f"signal {index}"
        if not isinstance(signal, dict):
            blockers.append(f"{prefix} must be an object")
            continue
        signal_id = str(signal.get("id", ""))
        if not signal_id or signal_id in signal_ids:
            blockers.append(f"{prefix} has a duplicate or empty id")
        signal_ids.add(signal_id)
        source_ids = signal.get("source_ids")
        if not isinstance(source_ids, list) or len(set(source_ids)) < 2:
            blockers.append(f"{prefix} requires at least two unique source ids")
            source_ids = []
        linked: list[dict[str, Any]] = []
        for source_id in source_ids:
            if source_id not in source_index:
                blockers.append(f"{prefix} references unknown source id: {source_id}")
            else:
                linked.append(source_index[source_id])
        domains = {canonical_domain(source.get("url")) for source in linked}
        creators = {
            str(source.get("creator_or_project", "")).strip().casefold()
            for source in linked
        }
        classes = {source.get("source_class") for source in linked}
        if len(domains - {""}) < 2:
            blockers.append(f"{prefix} lacks cross-domain corroboration")
        if len(creators - {""}) < 2:
            blockers.append(f"{prefix} lacks independent creator/project corroboration")
        if len(classes - {None, ""}) < 2:
            warnings.append(f"{prefix} relies on one source class")
        velocity = signal.get("velocity")
        if velocity != "unknown" and len(prior_refs) < 2:
            blockers.append(
                f"{prefix} claims velocity without at least two prior snapshots"
            )
        if not str(signal.get("velocity_evidence", "")).strip():
            blockers.append(f"{prefix} requires velocity_evidence")
        if not signal.get("avoid_literal_copy"):
            blockers.append(f"{prefix} requires an explicit do-not-copy boundary")
        if signal.get("rights_status") in {"unknown", "restricted"}:
            warnings.append(f"{prefix} is unsuitable for literal visual conditioning")

    reviewed = parse_time(review.get("reviewed_at"), "review.reviewed_at", blockers)
    if captured and reviewed and reviewed < captured:
        blockers.append("reviewed_at cannot precede snapshot captured_at")

    report = {
        "schema": "moso.trend-validation/0.2",
        "scope": "freshness-independence-and-evidence-integrity-only",
        "snapshot": str(args.snapshot.resolve()),
        "status": "block" if blockers else "pass",
        "source_count": len(source_index),
        "source_class_count": len(source_classes - {""}),
        "signal_count": len(signal_ids - {""}),
        "blockers": blockers,
        "warnings": warnings,
        "not_evaluated": [
            "whether a signal is aesthetically valuable",
            "whether a mechanism fits a specific project",
            "whether source engagement metrics are authentic"
        ]
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 1 if blockers else 0


if __name__ == "__main__":
    raise SystemExit(main())
