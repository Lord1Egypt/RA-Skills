#!/usr/bin/env python3
"""Build a fail-closed v2 release acceptance receipt from real external evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ARTIFACT = "omni-ecom.release-acceptance-ledger@2.0"
RECEIPT_ARTIFACT = "omni-ecom.release-acceptance-receipt@2.0"
REQUIRED_DOMAINS = {
    "workbuddy_native_multi_agent_pdf": "workbuddy",
    "codex_native_multi_agent_pdf": "codex",
}
OPTIONAL_DOMAINS = {
    "platform_api_read": None,
    "controlled_action_readback": None,
    "live_model_route_baseline": None,
}
ALL_DOMAINS = {**REQUIRED_DOMAINS, **OPTIONAL_DOMAINS}
REQUIRED_KINDS = {
    "workbuddy_native_multi_agent_pdf": "native_host_acceptance",
    "codex_native_multi_agent_pdf": "native_host_acceptance",
    "platform_api_read": "live_api_read_acceptance",
    "controlled_action_readback": "live_controlled_action_readback",
    "live_model_route_baseline": "live_model_route_acceptance",
}
FORBIDDEN_MARKERS = ("synthetic", "mock", "fixture", "simulated", "candidate_self_attestation")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("json_root_not_object")
    return value


def _text_contains_forbidden(value: Any) -> bool:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True).casefold()
    return any(marker in text for marker in FORBIDDEN_MARKERS)


def validate_receipt(receipt: dict[str, Any], target_version: str) -> list[str]:
    errors: list[str] = []
    if receipt.get("artifact_type") != RECEIPT_ARTIFACT:
        errors.append("release_acceptance_receipt_type_invalid")
    if receipt.get("status") != "release_acceptance_verified":
        errors.append("release_acceptance_not_verified")
    if str(receipt.get("target_version") or "") != target_version:
        errors.append("release_acceptance_target_version_mismatch")
    domains = receipt.get("domains")
    if not isinstance(domains, list) or set(domains) != set(REQUIRED_DOMAINS):
        errors.append("release_acceptance_domains_incomplete")
    evidence = receipt.get("evidence_fingerprints")
    if not isinstance(evidence, list) or not set(REQUIRED_DOMAINS).issubset(
            {str(item.get("domain") or "") for item in evidence if isinstance(item, dict)}):
        errors.append("release_acceptance_evidence_incomplete")
    else:
        seen: set[str] = set()
        for item in evidence:
            if not isinstance(item, dict):
                errors.append("release_acceptance_evidence_invalid")
                continue
            domain = str(item.get("domain") or "")
            if domain in seen:
                errors.append(f"release_acceptance_domain_duplicate:{domain}")
            seen.add(domain)
            digest = str(item.get("sha256") or "")
            if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                errors.append(f"release_acceptance_hash_invalid:{domain}")
            if domain not in ALL_DOMAINS:
                errors.append(f"release_acceptance_domain_unknown:{domain}")
    optional = receipt.get("optional_capabilities")
    if not isinstance(optional, dict) or set(optional) != set(OPTIONAL_DOMAINS):
        errors.append("release_acceptance_optional_capabilities_invalid")
    else:
        fingerprint_domains = {str(item.get("domain") or "") for item in evidence or [] if isinstance(item, dict)}
        for domain, status in optional.items():
            if status not in ("enabled", "not_enabled"):
                errors.append(f"release_acceptance_optional_status_invalid:{domain}")
            if status == "enabled" and domain not in fingerprint_domains:
                errors.append(f"release_acceptance_optional_evidence_missing:{domain}")
    return errors


def evaluate(ledger_path: Path, target_version: str) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    try:
        ledger = load_json(ledger_path)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        return {}, [f"acceptance_ledger_unreadable:{exc}"]
    if ledger.get("artifact_type") != ARTIFACT:
        errors.append("acceptance_ledger_type_invalid")
    if str(ledger.get("target_version") or "") != target_version:
        errors.append("acceptance_target_version_mismatch")
    if ledger.get("environment") != "real_external_acceptance":
        errors.append("acceptance_environment_not_real")
    items = ledger.get("evidence")
    if not isinstance(items, list):
        return ledger, errors + ["acceptance_evidence_not_list"]
    by_domain: dict[str, dict[str, Any]] = {}
    fingerprints: list[dict[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            errors.append("acceptance_evidence_item_invalid")
            continue
        domain = str(item.get("domain") or "")
        if domain not in ALL_DOMAINS:
            errors.append(f"acceptance_domain_unknown:{domain}")
            continue
        if domain in by_domain:
            errors.append(f"acceptance_domain_duplicate:{domain}")
            continue
        by_domain[domain] = item
        expected_host = ALL_DOMAINS[domain]
        if expected_host and item.get("host") != expected_host:
            errors.append(f"acceptance_host_mismatch:{domain}")
        if item.get("status") != "PASS" or item.get("environment") != "live":
            errors.append(f"acceptance_not_live_pass:{domain}")
        if item.get("evidence_kind") != REQUIRED_KINDS[domain]:
            errors.append(f"acceptance_evidence_kind_invalid:{domain}")
        if _text_contains_forbidden({"kind": item.get("evidence_kind"), "notes": item.get("notes")}):
            errors.append(f"acceptance_synthetic_marker:{domain}")
        source_value = str(item.get("source_file") or "").strip()
        source_path = Path(source_value)
        if not source_path.is_absolute():
            source_path = (ledger_path.parent / source_path).resolve()
        if not source_path.is_file():
            errors.append(f"acceptance_source_missing:{domain}")
            continue
        actual_hash = sha256(source_path)
        if str(item.get("sha256") or "").casefold() != actual_hash:
            errors.append(f"acceptance_source_hash_mismatch:{domain}")
            continue
        try:
            source = load_json(source_path)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"acceptance_source_unreadable:{domain}:{exc}")
            continue
        if source.get("status") != "PASS":
            errors.append(f"acceptance_source_not_pass:{domain}")
        if source.get("acceptance_domain") != domain or source.get("evidence_kind") != REQUIRED_KINDS[domain]:
            errors.append(f"acceptance_source_identity_mismatch:{domain}")
        source_version = str(source.get("version") or source.get("target_version") or "")
        if source_version != target_version and not source_version.startswith(f"{target_version}-candidate."):
            errors.append(f"acceptance_source_version_mismatch:{domain}")
        if source.get("environment") != "live" or _text_contains_forbidden({"kind": source.get("evidence_kind"), "mode": source.get("mode")}):
            errors.append(f"acceptance_source_not_live:{domain}")
        if expected_host and source.get("host") != expected_host:
            errors.append(f"acceptance_source_host_mismatch:{domain}")
        if domain.endswith("native_multi_agent_pdf"):
            for field in ("pipeline_completion_verified", "multi_agent_complete", "pdf_review_passed"):
                if source.get(field) is not True:
                    errors.append(f"acceptance_source_{field}_missing:{domain}")
        elif domain == "platform_api_read":
            for field in ("scoped_read_observation_passed", "source_fingerprint_verified", "credential_scope_verified"):
                if source.get(field) is not True:
                    errors.append(f"acceptance_source_{field}_missing:{domain}")
        elif domain == "controlled_action_readback":
            for field in ("explicit_approval_verified", "bounded_action_verified", "idempotency_verified", "readback_verified"):
                if source.get(field) is not True:
                    errors.append(f"acceptance_source_{field}_missing:{domain}")
        elif domain == "live_model_route_baseline":
            for field in ("two_live_cohorts_verified", "minimum_sample_verified", "human_route_acceptance_recorded"):
                if source.get(field) is not True:
                    errors.append(f"acceptance_source_{field}_missing:{domain}")
            if source.get("automatic_route_switch") is not False:
                errors.append(f"acceptance_source_automatic_route_switch_not_false:{domain}")
        fingerprints.append({"domain": domain, "sha256": actual_hash})
    for domain in REQUIRED_DOMAINS:
        if domain not in by_domain:
            errors.append(f"acceptance_domain_missing:{domain}")
    optional_status = {
        domain: "enabled" if domain in by_domain and not any(error.endswith(f":{domain}") for error in errors)
        else "not_enabled"
        for domain in OPTIONAL_DOMAINS
    }
    receipt = {
        "artifact_type": RECEIPT_ARTIFACT,
        "status": "release_acceptance_verified" if not errors else "release_acceptance_incomplete",
        "target_version": target_version,
        "verified_at": datetime.now(timezone.utc).isoformat(),
        "ledger_sha256": sha256(ledger_path),
        "domains": sorted(REQUIRED_DOMAINS),
        "optional_capabilities": optional_status,
        "evidence_fingerprints": sorted(fingerprints, key=lambda value: value["domain"]),
        "errors": sorted(set(errors)),
    }
    return receipt, errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify all real v2 release acceptance domains")
    parser.add_argument("ledger")
    parser.add_argument("--target-version", default="2.0.3")
    parser.add_argument("--output")
    args = parser.parse_args()
    receipt, errors = evaluate(Path(args.ledger).resolve(), args.target_version)
    payload = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
    if args.output and not errors:
        output = Path(args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(payload, encoding="utf-8")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(payload, end="")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
