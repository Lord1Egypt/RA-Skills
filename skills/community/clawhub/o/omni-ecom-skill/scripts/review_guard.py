#!/usr/bin/env python3
"""Bind delivery-review approval to immutable report, adjudication and source files."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from quality_gate import validate_quality, validate_frozen_quality
from host_runtime import ID_PATTERN, validate_analysis_binding
from artifact_contract import native_receipt_identity, validate_receipt_identity


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:\.[0-9A-Za-z-]+)*)?$")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,80}$")
REVISION_RE = re.compile(r"^R[1-9][0-9]*$")
TASK_ID_RE = re.compile(ID_PATTERN)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path.name}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload_sha256(payload: dict[str, Any], excluded: set[str] | None = None) -> str:
    clean = {key: value for key, value in payload.items() if key not in (excluded or set())}
    encoded = json.dumps(clean, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_entry(raw: str) -> dict[str, Any]:
    path = Path(raw).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"review input missing: {path.name}")
    return {
        "file": path.name,
        "path": str(path),
        "sha256": file_sha256(path),
        "bytes": path.stat().st_size,
    }


def validate_pdf_bundle(
    artifacts: list[dict[str, Any]],
    run_id: str,
    client_scope: str,
    team_version: str,
    report_revision: str,
) -> None:
    """Require the default visual PDF and its deterministic render receipt."""
    by_name = {str(item.get("file")): item for item in artifacts}
    required = {"report.json", "report.md", "report.pdf", "pdf-delivery.json"}
    if not required.issubset(by_name):
        raise ValueError("pdf_delivery_required")
    report_package = read_json(Path(str(by_name["report.json"]["path"])))
    if (
        report_package.get("run_id") != run_id
        or str(report_package.get("client_scope", "")).strip() != client_scope.strip()
        or report_package.get("team_version") != team_version
        or report_package.get("report_revision") != report_revision
    ):
        raise ValueError("pdf_delivery_mismatch")
    receipt = read_json(Path(str(by_name["pdf-delivery.json"]["path"])))
    from artifact_contract import validate_receipt_identity
    validate_receipt_identity(receipt, "pdf_delivery", team_version)
    pdf_path = Path(str(by_name["report.pdf"]["path"]))
    from pdf_layout_policy import page_limit
    maximum_pages=page_limit(report_package)
    if (
        receipt.get("status") != "pdf_render_verified"
        or receipt.get("team_version") != team_version
        or receipt.get("report_revision") != report_revision
        or receipt.get("report_file") != "report.pdf"
        or receipt.get("report_sha256") != file_sha256(pdf_path)
        or int(receipt.get("chart_count", 0)) < 3
        or not 1 <= int(receipt.get("page_count", 0)) <= maximum_pages
        or receipt.get('page_limit',maximum_pages)!=maximum_pages
        or receipt.get("blank_pages") not in ([], None)
    ):
        raise ValueError("pdf_delivery_not_verified")


def validate_manifest(manifest: dict[str, Any]) -> None:
    try:
        validate_receipt_identity(manifest, "review_manifest", manifest.get("team_version"))
    except ValueError as exc:
        raise ValueError("review_manifest_invalid") from exc
    if manifest.get("status") != "awaiting_delivery_review":
        raise ValueError("review_manifest_invalid")
    if not RUN_ID_RE.fullmatch(str(manifest.get("run_id", ""))):
        raise ValueError("review_manifest_invalid")
    if not SEMVER_RE.fullmatch(str(manifest.get("team_version", ""))):
        raise ValueError("review_manifest_invalid")
    if not REVISION_RE.fullmatch(str(manifest.get("report_revision", ""))):
        raise ValueError("review_manifest_invalid")
    if not str(manifest.get("client_scope", "")).strip():
        raise ValueError("review_manifest_invalid")
    artifacts = manifest.get("artifacts")
    sources = manifest.get("sources")
    if not isinstance(artifacts, list) or not artifacts or not isinstance(sources, list):
        raise ValueError("review_manifest_invalid")
    expected = payload_sha256(manifest, {"manifest_sha256"})
    if manifest.get("manifest_sha256") != expected:
        raise ValueError("review_manifest_tampered")
    if not {"report.json", "report.md", "report.pdf", "pdf-delivery.json"}.issubset(
        {str(item.get("file")) for item in artifacts}
    ):
        raise ValueError("pdf_delivery_required")


def changed_entries(manifest: dict[str, Any]) -> tuple[list[str], list[str]]:
    changed_artifacts: list[str] = []
    changed_sources: list[str] = []
    for key, target in (("artifacts", changed_artifacts), ("sources", changed_sources)):
        for item in manifest.get(key, []):
            path = Path(str(item.get("path", ""))).resolve()
            if not path.is_file() or file_sha256(path) != item.get("sha256") or path.stat().st_size != item.get("bytes"):
                target.append(str(item.get("file") or "unknown"))
    return changed_artifacts, changed_sources


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    # A freeze must be authored exactly once, by the lead. Silently overwriting an
    # existing manifest would let a later actor (e.g. the reviewer) re-author the very
    # object that binds its own approval, destroying separation of duties.
    if Path(args.output).resolve().exists():
        raise ValueError("review_manifest_already_exists")
    if not RUN_ID_RE.fullmatch(args.run_id):
        raise ValueError("run_id_invalid")
    if not SEMVER_RE.fullmatch(args.team_version):
        raise ValueError("team_version_invalid")
    if not REVISION_RE.fullmatch(args.report_revision):
        raise ValueError("report_revision_invalid")
    artifact_entries = [file_entry(item) for item in args.artifact]
    source_entries = [file_entry(item) for item in args.source]
    mutable_sources = [item["file"] for item in source_entries if str(item["file"]).casefold().endswith(".return.json")]
    if mutable_sources:
        raise ValueError("mutable_return_source_blocked")
    all_paths = [item["path"] for item in [*artifact_entries, *source_entries]]
    if len(all_paths) != len(set(all_paths)):
        raise ValueError("review_input_duplicate")
    validate_pdf_bundle(
        artifact_entries,
        args.run_id,
        args.client_scope,
        args.team_version,
        args.report_revision,
    )
    manifest: dict[str, Any] = {
        **native_receipt_identity("review_manifest", args.team_version),
        "status": "awaiting_delivery_review",
        "run_id": args.run_id,
        "client_scope": args.client_scope.strip(),
        "team_version": args.team_version,
        "report_revision": args.report_revision,
        "created_at": utc_now(),
        "artifacts": artifact_entries,
        "sources": source_entries,
    }
    report_entry=next(item for item in artifact_entries if item['file']=='report.json')
    report_dir=Path(report_entry['path']).parent
    quality=validate_quality(report_dir,read_json(Path(report_entry['path'])))
    report=read_json(Path(report_entry['path']))
    from claim_source_guard import validate_pdf_source_binding
    validate_pdf_source_binding(read_json(report_dir/'pdf-delivery.json'),report_dir,report)
    runtime, runtime_files=validate_analysis_binding(
        report_dir,report,read_json(report_dir/'quality-inputs.json')['handoffs'])
    existing={str(Path(item['path']).resolve()) for item in artifact_entries+source_entries}
    for item in quality['inputs']:
        path=(report_dir/item['file']).resolve()
        if str(path) not in existing:
            source_entries.append(file_entry(str(path)))
            existing.add(str(path))
    manifest['quality_gate']=quality
    manifest['runtime_gate']=runtime
    for name in runtime_files:
        path=(report_dir/name).resolve()
        if str(path) not in existing:
            source_entries.append(file_entry(str(path)))
            existing.add(str(path))
        if file_sha256(path)!=runtime_files[name]:
            raise ValueError('runtime_inputs_changed')
    validate_frozen_quality(manifest,report_dir,quality)
    # Declare how manifest_sha256 is derived so any reviewer can reproduce it.
    # A document cannot contain its own byte hash, so the digest is taken over the
    # canonical JSON payload with the "manifest_sha256" key excluded. Reviewers must
    # verify by recomputing this canonical form, NOT by hashing the file bytes.
    manifest["manifest_sha256_method"] = (
        "sha256(json.dumps(manifest_without_manifest_sha256, "
        "ensure_ascii=False, sort_keys=True, separators=(',',':')).encode('utf-8'))"
    )
    manifest["manifest_sha256"] = payload_sha256(manifest)
    write_json(Path(args.output).resolve(), manifest)
    return {
        "status": "review_manifest_prepared",
        "run_id": args.run_id,
        "report_revision": args.report_revision,
        "manifest_sha256": manifest["manifest_sha256"],
        "artifact_count": len(artifact_entries),
        "source_count": len(source_entries),
        "output": Path(args.output).name,
    }


def attest(args: argparse.Namespace) -> dict[str, Any]:
    # Free-form attestation is a forgery vector: it lets any caller assert
    # --review-status passed with an arbitrary --agent-task-id and no link to a real
    # reviewer return file. Approval must always be derived from the reviewing agent's
    # own return receipt, so this path is disabled in favour of attest-result.
    raise ValueError("freeform_attest_disabled_use_attest_result")


def _attest_unused(args: argparse.Namespace) -> dict[str, Any]:
    manifest = read_json(Path(args.manifest).resolve())
    validate_manifest(manifest)
    changed_artifacts, changed_sources = changed_entries(manifest)
    if changed_artifacts or changed_sources:
        raise ValueError("review_stale_blocked")
    validate_pdf_bundle(
        manifest["artifacts"], manifest["run_id"], manifest["client_scope"],
        manifest["team_version"], manifest["report_revision"],
    )
    if not TASK_ID_RE.fullmatch(args.agent_task_id):
        raise ValueError("agent_task_id_invalid")
    if args.review_status == "passed" and args.required_change:
        raise ValueError("passed_review_cannot_have_required_changes")
    attestation = {
        **native_receipt_identity("review_attestation", manifest["team_version"]),
        "run_id": manifest["run_id"],
        "agent_id": "delivery-review",
        "agent_task_id": args.agent_task_id,
        "return_status": "completed",
        "returned_at": utc_now(),
        "review_status": args.review_status,
        "reviewed_manifest_sha256": manifest["manifest_sha256"],
        "reviewed_artifacts": [
            {"file": item["file"], "sha256": item["sha256"]}
            for item in manifest["artifacts"]
        ],
        "findings": args.finding,
        "required_changes": args.required_change,
        "contribution_summary": args.summary,
        "response": {
            "review_status": args.review_status,
            "summary": args.summary,
            "findings": args.finding,
            "required_changes": args.required_change,
        },
    }
    write_json(Path(args.output).resolve(), attestation)
    return {
        "status": "delivery_review_attested",
        "review_status": args.review_status,
        "agent_task_id": args.agent_task_id,
        "reviewed_manifest_sha256": manifest["manifest_sha256"],
        "output": Path(args.output).name,
    }


def attest_result(args: argparse.Namespace) -> dict[str, Any]:
    manifest = read_json(Path(args.manifest).resolve())
    review_result = read_json(Path(args.review_result).resolve())
    validate_manifest(manifest)
    changed_artifacts, changed_sources = changed_entries(manifest)
    if changed_artifacts or changed_sources:
        raise ValueError("review_stale_blocked")
    validate_pdf_bundle(
        manifest["artifacts"], manifest["run_id"], manifest["client_scope"],
        manifest["team_version"], manifest["report_revision"],
    )
    if not TASK_ID_RE.fullmatch(args.agent_task_id):
        raise ValueError("agent_task_id_invalid")
    validate_review_result(review_result, manifest)
    if review_result.get("run_id") != manifest.get("run_id") or review_result.get("return_status") != "completed":
        raise ValueError("review_result_invalid")
    if review_result.get("report_revision") != manifest.get("report_revision"):
        raise ValueError("review_revision_mismatch")
    if review_result.get("review_attempt_id") != args.review_attempt_id:
        raise ValueError("review_attempt_mismatch")
    review_status = review_result.get("review_status")
    if review_status not in {"passed", "conditional_pass", "rejected"}:
        raise ValueError("review_result_invalid")
    findings = review_result.get("findings")
    required_changes = review_result.get("required_changes")
    summary = review_result.get("contribution_summary")
    if not isinstance(findings, list) or not isinstance(required_changes, list) or not isinstance(summary, str) or not summary.strip():
        raise ValueError("review_result_invalid")
    if review_status == "passed" and required_changes:
        raise ValueError("passed_review_cannot_have_required_changes")
    expected_artifacts = [
        {"file": item["file"], "sha256": item["sha256"]}
        for item in manifest["artifacts"]
    ]
    if review_result.get("reviewed_manifest_sha256") != manifest.get("manifest_sha256"):
        raise ValueError("review_stale_blocked")
    if review_result.get("reviewed_artifacts") != expected_artifacts:
        raise ValueError("review_stale_blocked")
    attestation = {
        **native_receipt_identity("review_attestation", manifest["team_version"]),
        "run_id": manifest["run_id"],
        "agent_id": "delivery-review",
        "agent_task_id": args.agent_task_id,
        "review_attempt_id": args.review_attempt_id,
        "report_revision": manifest["report_revision"],
        "return_status": "completed",
        "returned_at": review_result.get("returned_at"),
        "review_status": review_status,
        "reviewed_manifest_sha256": manifest["manifest_sha256"],
        "reviewed_artifacts": expected_artifacts,
        "findings": findings,
        "required_changes": required_changes,
        "contribution_summary": summary.strip(),
        "review_result_sha256": file_sha256(Path(args.review_result).resolve()),
        "response": {
            "review_status": review_status,
            "summary": summary.strip(),
            "findings": findings,
            "required_changes": required_changes,
        },
    }
    validate_attestation(attestation, manifest)
    write_json(Path(args.output).resolve(), attestation)
    return {
        "status": "delivery_review_result_attested",
        "review_status": review_status,
        "agent_task_id": args.agent_task_id,
        "review_attempt_id": args.review_attempt_id,
        "reviewed_manifest_sha256": manifest["manifest_sha256"],
        "output": Path(args.output).name,
    }


def validate_attestation(attestation: dict[str, Any], manifest: dict[str, Any]) -> None:
    try:
        validate_receipt_identity(attestation, "review_attestation", manifest.get("team_version"))
    except ValueError as exc:
        raise ValueError("review_attestation_invalid") from exc
    if attestation.get("agent_id") != "delivery-review":
        raise ValueError("review_attestation_invalid")
    if attestation.get("run_id") != manifest.get("run_id"):
        raise ValueError("review_attestation_mismatch")
    if not TASK_ID_RE.fullmatch(str(attestation.get("agent_task_id", ""))):
        raise ValueError("review_attestation_invalid")
    if attestation.get("return_status") != "completed":
        raise ValueError("review_attestation_invalid")
    if not str(attestation.get("review_attempt_id") or "").strip():
        raise ValueError("review_attestation_invalid")
    if attestation.get("report_revision") != manifest.get("report_revision"):
        raise ValueError("review_revision_mismatch")
    try:
        reviewed_at = datetime.fromisoformat(str(attestation.get("returned_at", "")).replace("Z", "+00:00"))
        manifest_at = datetime.fromisoformat(str(manifest.get("created_at", "")).replace("Z", "+00:00"))
        if reviewed_at.tzinfo is None or manifest_at.tzinfo is None or reviewed_at < manifest_at:
            raise ValueError("review_attestation_invalid")
    except (TypeError, ValueError) as exc:
        raise ValueError("review_attestation_invalid") from exc
    if attestation.get("reviewed_manifest_sha256") != manifest.get("manifest_sha256"):
        raise ValueError("review_stale_blocked")
    expected_artifacts = [
        {"file": item["file"], "sha256": item["sha256"]}
        for item in manifest["artifacts"]
    ]
    if attestation.get("reviewed_artifacts") != expected_artifacts:
        raise ValueError("review_stale_blocked")


def validate_review_result(review_result: dict[str, Any], manifest: dict[str, Any]) -> None:
    try:
        validate_receipt_identity(review_result, "review_result", manifest.get("team_version"))
    except ValueError as exc:
        raise ValueError("review_result_invalid") from exc
    if review_result.get("agent_id") != "delivery-review":
        raise ValueError("review_result_invalid")
    if review_result.get("run_id") != manifest.get("run_id"):
        raise ValueError("review_result_invalid")
    if review_result.get("report_revision") != manifest.get("report_revision"):
        raise ValueError("review_revision_mismatch")
    if review_result.get("reviewed_manifest_sha256") != manifest.get("manifest_sha256"):
        raise ValueError("review_stale_blocked")


def verify(args: argparse.Namespace) -> dict[str, Any]:
    manifest_path = Path(args.manifest).resolve()
    attestation_path = Path(args.attestation).resolve()
    manifest = read_json(manifest_path)
    attestation = read_json(attestation_path)
    validate_manifest(manifest)
    validate_attestation(attestation, manifest)
    changed_artifacts, changed_sources = changed_entries(manifest)
    if changed_artifacts or changed_sources:
        raise ValueError("review_stale_blocked")
    validate_pdf_bundle(
        manifest["artifacts"], manifest["run_id"], manifest["client_scope"],
        manifest["team_version"], manifest["report_revision"],
    )
    if attestation.get("review_status") != "passed":
        raise ValueError("review_not_passed_blocked")
    if attestation.get("required_changes"):
        raise ValueError("review_not_passed_blocked")
    receipt = {
        **native_receipt_identity("review_release", manifest["team_version"]),
        "status": "review_release_verified",
        "run_id": manifest["run_id"],
        "client_scope": manifest["client_scope"],
        "team_version": manifest["team_version"],
        "report_revision": manifest["report_revision"],
        "manifest_sha256": manifest["manifest_sha256"],
        "review_agent_id": "delivery-review",
        "review_agent_task_id": attestation["agent_task_id"],
        "review_attempt_id": attestation["review_attempt_id"],
        "reviewed_at": attestation["returned_at"],
        "review_attestation_file": attestation_path.name,
        "review_attestation_sha256": file_sha256(attestation_path),
        "artifacts": [
            {"file": item["file"], "sha256": item["sha256"]}
            for item in manifest["artifacts"]
        ],
        "source_count": len(manifest["sources"]),
        "verified_at": utc_now(),
    }
    if args.receipt:
        write_json(Path(args.receipt).resolve(), receipt)
    return receipt


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="Immutable delivery-review release guard")
    sub = root.add_subparsers(dest="command", required=True)

    p_prepare = sub.add_parser("prepare")
    p_prepare.add_argument("--run-id", required=True)
    p_prepare.add_argument("--client-scope", required=True)
    p_prepare.add_argument("--team-version", required=True)
    p_prepare.add_argument("--report-revision", required=True)
    p_prepare.add_argument("--artifact", action="append", required=True)
    p_prepare.add_argument("--source", action="append", required=True)
    p_prepare.add_argument("--output", required=True)

    p_attest = sub.add_parser("attest")
    p_attest.add_argument("--manifest", required=True)
    p_attest.add_argument("--agent-task-id", required=True)
    p_attest.add_argument("--review-status", choices=["passed", "conditional_pass", "rejected"], required=True)
    p_attest.add_argument("--finding", action="append", default=[])
    p_attest.add_argument("--required-change", action="append", default=[])
    p_attest.add_argument("--summary", required=True)
    p_attest.add_argument("--output", required=True)

    p_attest_result = sub.add_parser("attest-result")
    p_attest_result.add_argument("--manifest", required=True)
    p_attest_result.add_argument("--review-result", required=True)
    p_attest_result.add_argument("--agent-task-id", required=True)
    p_attest_result.add_argument("--review-attempt-id", required=True)
    p_attest_result.add_argument("--output", required=True)

    p_verify = sub.add_parser("verify")
    p_verify.add_argument("--manifest", required=True)
    p_verify.add_argument("--attestation", required=True)
    p_verify.add_argument("--receipt")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        result = (
            prepare(args) if args.command == "prepare" else
            attest(args) if args.command == "attest" else
            attest_result(args) if args.command == "attest-result" else
            verify(args)
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, IndexError, TypeError, ArithmeticError, ImportError, RecursionError) as exc:
        reason = str(exc)
        status = reason if reason in {
            "review_stale_blocked", "review_not_passed_blocked", "review_manifest_tampered",
            "review_manifest_invalid", "review_attestation_invalid", "review_attestation_mismatch",
            "review_result_invalid", "review_attempt_mismatch", "review_revision_mismatch",
            "pdf_delivery_required", "pdf_delivery_not_verified", "pdf_delivery_mismatch",
        } else "review_guard_failed"
        print(json.dumps({"status": status, "reason": reason}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
