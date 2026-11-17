#!/usr/bin/env python3
"""Issue the only formal completion receipt after report, review and privacy gates pass."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from quality_gate import validate_quality, validate_frozen_quality
from review_guard import validate_manifest, validate_attestation, changed_entries
from host_runtime import Runtime, ID_PATTERN, validate_analysis_binding, validate_review_binding


ROOT = Path(__file__).resolve().parents[1]
TASK_ID_RE = re.compile(ID_PATTERN)
CORE_ARTIFACTS = ("report.json", "report.md", "report.pdf", "pdf-delivery.json")
ANALYSIS_ROLES = (
    "omni-ecom-team-lead",
    "data-analyst",
    "platform-ops",
    "content-live-growth",
    "ad-profit-optimizer",
)


def validate_version_mode(version_info: dict[str, Any], candidate_acceptance: bool) -> str:
    version = str(version_info.get("team_version") or "")
    if candidate_acceptance:
        require(version_info.get("release_status") == "candidate" and version_info.get("release_ready") is False,
                "candidate_acceptance_requires_candidate_metadata")
        require(bool(re.fullmatch(r"2\.0\.[0-9]+-candidate\.[1-9][0-9]*", version)),
                "candidate_acceptance_version_invalid")
    else:
        require(version_info.get("release_status") == "released" and version_info.get("release_ready") is True,
                "candidate_version_not_release_ready")
    return version


def completion_identity(candidate_acceptance: bool, version: str) -> tuple[dict[str, Any], str]:
    if candidate_acceptance:
        return ({
            "schema_version": "2.0",
            "artifact_type": "candidate_runtime_acceptance",
            "contract_name": "omni-ecom.candidate-runtime-acceptance",
            "contract_version": "2.0",
            "created_by_team_version": version,
            "legacy_compatibility": {"read_only_import": [], "current_completion_authority": False},
        }, "candidate_pipeline_complete")
    from artifact_contract import native_receipt_identity
    return native_receipt_identity("completion", version), "formal_delivery_complete"


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ValueError(f"json_root_invalid:{path.name}")
    return payload


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def artifact(path: Path) -> dict[str, Any]:
    require(path.is_file() and path.stat().st_size > 0, f"artifact_missing:{path.name}")
    return {"file": path.name, "sha256": sha256(path), "bytes": path.stat().st_size}


def validate_public_receipt(receipt: dict[str, Any], report_dir: Path) -> None:
    from artifact_contract import validate_receipt_identity
    validate_receipt_identity(receipt, "public_output_guard", read_json(report_dir / "report.json").get("team_version"))
    require(receipt.get("status") == "public_output_guard_passed", "public_output_guard_not_passed")
    entries = receipt.get("artifacts")
    require(isinstance(entries, list), "public_output_guard_receipt_invalid")
    index = {str(item.get("file")): item for item in entries if isinstance(item, dict)}
    for name in ("report.json", "report.md", "report.pdf"):
        path = report_dir / name
        item = index.get(name)
        require(isinstance(item, dict) and item.get("sha256") == sha256(path), "public_output_guard_stale")


def validate_claim_receipt(receipt: dict[str, Any], report_dir: Path) -> dict:
    """Require the numeric claim/formula gate to be bound to the frozen report."""
    from artifact_contract import validate_receipt_identity
    validate_receipt_identity(receipt, "claim_guard", read_json(report_dir / "report.json").get("team_version"))
    require(receipt.get("status") == "claim_guard_passed", "claim_guard_not_passed")
    require(int(receipt.get("claims_count", 0)) > 0, "claim_ledger_empty")
    report_path = report_dir / "report.md"
    require(receipt.get("report_file") == "report.md", "claim_report_binding_missing")
    require(receipt.get("report_sha256") == sha256(report_path), "claim_report_binding_stale")
    errors = receipt.get("errors")
    require(not errors, "claim_guard_not_passed")
    from claim_source_guard import validate_report_sources
    actual=validate_report_sources(read_json(report_dir/'report.json'),report_dir,
                                   report_path.read_text(encoding='utf-8-sig'),require_context=True)
    require(receipt.get('verification_kind')=='local_source_reproduction_not_authenticity',
            'claim_receipt_source_verification_missing')
    for key in ('run_id','client_scope','period','claims_sha256','claims_count','verified_count','derived_count','unknown_count','source_checks'):
        require(receipt.get(key)==actual[key], 'claim_receipt_recomputed_mismatch:'+key)
        if key.endswith('_count'):
            require(type(receipt.get(key)) is int, 'claim_receipt_count_invalid')
    # Legacy CLI uses a display basename; the report, not the receipt, selects
    # the canonical confined ledger. Its actual hash is checked above.
    require(receipt.get('claims_file')==Path(actual['claims_file']).name, 'claim_receipt_ledger_mismatch')
    return actual


def validate_comprehensive(
    report: dict[str, Any], manifest: dict[str, Any], attestation: dict[str, Any],
    release_receipt: dict[str, Any],
) -> tuple[str, str]:
    identity = (report.get("run_id"), report.get("client_scope"), report.get("team_version"), report.get("report_revision"))
    from artifact_contract import validate_receipt_identity
    validate_receipt_identity(manifest, "review_manifest", identity[2])
    validate_receipt_identity(attestation, "review_attestation", identity[2])
    validate_receipt_identity(release_receipt, "review_release", identity[2])
    for payload in (manifest, attestation, release_receipt):
        require(payload.get("run_id") == identity[0], "completion_identity_mismatch")
    require(manifest.get("client_scope") == identity[1], "completion_identity_mismatch")
    require(manifest.get("team_version") == identity[2], "completion_identity_mismatch")
    require(manifest.get("report_revision") == identity[3], "completion_identity_mismatch")
    require(attestation.get("agent_id") == "delivery-review", "review_attestation_invalid")
    require(attestation.get("return_status") == "completed", "review_attestation_invalid")
    require(attestation.get("review_status") == "passed", "review_not_passed_blocked")
    require(not attestation.get("required_changes"), "review_not_passed_blocked")
    require(attestation.get("report_revision") == identity[3], "review_revision_mismatch")
    review_attempt_id = str(attestation.get("review_attempt_id") or "")
    review_task_id = str(attestation.get("agent_task_id") or "")
    require(bool(review_attempt_id), "review_attempt_id_missing")
    require(bool(TASK_ID_RE.fullmatch(review_task_id)), "review_agent_task_id_invalid")
    require(release_receipt.get("status") == "review_release_verified", "review_release_not_verified")
    require(release_receipt.get('client_scope')==identity[1] and release_receipt.get('team_version')==identity[2],
            'completion_identity_mismatch')
    require(release_receipt.get("review_attempt_id") == review_attempt_id, "review_attempt_mismatch")
    require(release_receipt.get("review_agent_task_id") == review_task_id, "review_agent_task_mismatch")
    require(release_receipt.get("report_revision") == identity[3], "review_revision_mismatch")
    require(release_receipt.get("manifest_sha256") == manifest.get("manifest_sha256"), "review_manifest_mismatch")
    return review_attempt_id, review_task_id


def build_activity(report: dict[str, Any], review_task_id: str = "", review_summary: str = "") -> list[dict[str, Any]]:
    source = report.get("expert_participation")
    require(isinstance(source, list) and len(source) == 6, "expert_activity_invalid")
    activity: list[dict[str, Any]] = []
    for item in source:
        require(isinstance(item, dict), "expert_activity_invalid")
        agent_id = str(item.get("agent_id") or "")
        status = str(item.get("participation_status") or "not_invoked")
        task_ids = [str(value) for value in item.get("agent_task_ids", []) if str(value)]
        summary = str(item.get("contribution_summary") or "")
        if agent_id == "delivery-review" and review_task_id:
            status = "contributed"
            task_ids = [review_task_id]
            summary = review_summary
        if status == "pending_review":
            status = "not_invoked"
        activity.append({
            "agent_id": agent_id,
            "participation_status": status,
            "agent_task_ids": task_ids,
            "contribution_summary": summary,
        })
    require({item["agent_id"] for item in activity} == set(ANALYSIS_ROLES) | {"delivery-review"}, "expert_activity_invalid")
    return activity


def main() -> int:
    parser = argparse.ArgumentParser(description="Formal delivery completion gate")
    parser.add_argument("--report-dir", required=True)
    parser.add_argument("--public-guard-receipt", required=True)
    parser.add_argument("--manifest")
    parser.add_argument("--attestation")
    parser.add_argument("--release-receipt")
    parser.add_argument("--claim-receipt", required=True, help="数字来源、公式和归因闸门回执")
    parser.add_argument("--version-info", default=str(ROOT / "version-info.json"))
    parser.add_argument("--output", required=True)
    parser.add_argument("--candidate-acceptance", action="store_true", help="Validate the complete candidate pipeline without issuing formal delivery")
    args = parser.parse_args()
    try:
        checked_files={}
        def checked_json(path):
            before=sha256(path)
            value=read_json(path)
            require(sha256(path)==before,'completion_input_changed')
            checked_files[path]=before
            return value
        report_dir = Path(args.report_dir).expanduser().resolve()
        paths = {name: report_dir / name for name in CORE_ARTIFACTS}
        artifacts = [artifact(path) for path in paths.values()]
        report = checked_json(paths["report.json"])
        from data_quality_report_guard import validate_data_quality_report
        data_quality_scope_gate = validate_data_quality_report(report)
        pdf_receipt = checked_json(paths["pdf-delivery.json"])
        version_info = checked_json(Path(args.version_info).expanduser().resolve())
        validate_version_mode(version_info, args.candidate_acceptance)
        require(report.get("team_version") == version_info.get("team_version"), "team_version_mismatch")
        from artifact_contract import validate_receipt_identity
        validate_receipt_identity(pdf_receipt, "pdf_delivery", report.get("team_version"))
        require(report.get("collaboration_mode") in ("comprehensive", "single_point"), "collaboration_mode_invalid")
        profiles=read_json(ROOT/'config'/'task-profiles.json')['profiles']
        profile=profiles.get(report.get('task_type'))
        require(profile is not None,'completion_task_type_invalid')
        require(profile['default_collaboration_mode']!='comprehensive' or report['collaboration_mode']=='comprehensive',
                'comprehensive_task_cannot_degrade')
        quality_receipt = validate_quality(report_dir, report)
        from claim_source_guard import validate_pdf_source_binding
        pdf_claims=validate_pdf_source_binding(pdf_receipt,report_dir,report)
        require(pdf_claims==quality_receipt['claim_source_gate'], 'pdf_quality_source_mismatch')
        runtime_config=checked_json(report_dir/'quality-inputs.json')
        runtime_receipt, runtime_files=validate_analysis_binding(report_dir,report,runtime_config['handoffs'],require_idle=True)
        initial_runtime_receipt=runtime_receipt
        require(pdf_receipt.get("status") == "pdf_render_verified", "pdf_delivery_not_verified")
        require(pdf_receipt.get("team_version") == report.get("team_version"), "pdf_delivery_mismatch")
        require(pdf_receipt.get("report_revision") == report.get("report_revision"), "pdf_delivery_mismatch")
        require(pdf_receipt.get("report_sha256") == sha256(paths["report.pdf"]), "pdf_delivery_mismatch")
        require(int(pdf_receipt.get("chart_count", 0)) >= 3, "pdf_delivery_not_verified")

        public_receipt_path = Path(args.public_guard_receipt).expanduser().resolve()
        public_receipt = checked_json(public_receipt_path)
        validate_public_receipt(public_receipt, report_dir)
        artifacts.append(artifact(public_receipt_path))

        collaboration_mode = str(report.get("collaboration_mode") or "")
        review_required = collaboration_mode == "comprehensive"
        review_attempt_id = ""
        review_task_id = ""
        review_summary = ""
        release_sha = ""
        review_binding = None
        if review_required:
            require(bool(args.manifest and args.attestation and args.release_receipt), "review_evidence_missing")
            manifest_path = Path(args.manifest).expanduser().resolve()
            attestation_path = Path(args.attestation).expanduser().resolve()
            release_path = Path(args.release_receipt).expanduser().resolve()
            manifest = checked_json(manifest_path)
            attestation = checked_json(attestation_path)
            release_receipt = checked_json(release_path)
            validate_manifest(manifest)
            validate_attestation(attestation, manifest)
            changed_artifacts, changed_sources = changed_entries(manifest)
            require(not changed_artifacts and not changed_sources, "review_stale_blocked")
            validate_frozen_quality(manifest, report_dir, quality_receipt)
            require(manifest.get('runtime_gate')==runtime_receipt,'runtime_frozen_selection_mismatch')
            frozen={str(Path(item['path']).resolve()):item['sha256'] for item in manifest['sources']+manifest['artifacts']}
            for name,expected in runtime_files.items():
                require(frozen.get(str((report_dir/name).resolve()))==expected,'runtime_frozen_evidence_missing')
            review_attempt_id, review_task_id = validate_comprehensive(report, manifest, attestation, release_receipt)
            require(release_receipt.get('review_attestation_sha256')==sha256(attestation_path),
                    'review_release_attestation_mismatch')
            review_binding, review_files=validate_review_binding(report_dir,report,manifest,attestation)
            runtime_files.update(review_files)
            review_summary = str(attestation.get("contribution_summary") or "独立交付复核通过")
            artifacts.extend([artifact(manifest_path), artifact(attestation_path), artifact(release_path)])
            release_sha = sha256(release_path)

        claim_receipt_path = Path(args.claim_receipt).expanduser().resolve()
        claim_receipt = checked_json(claim_receipt_path)
        actual_claims=validate_claim_receipt(claim_receipt, report_dir)
        require(actual_claims==quality_receipt['claim_source_gate'], 'claim_quality_recheck_changed')
        artifacts.append(artifact(claim_receipt_path))

        activity = build_activity(report, review_task_id, review_summary)
        by_role={item['agent_id']:item for item in activity}
        selected={item['role']:item for item in runtime_receipt['members']}
        for role in ANALYSIS_ROLES[1:]:
            member=by_role[role]
            if role in selected:
                require(member['participation_status']=='contributed' and
                        member['agent_task_ids']==[selected[role]['agent_task_id']],
                        'runtime_activity_task_mismatch:'+role)
            else:
                require(member['participation_status']=='not_invoked' and not member['agent_task_ids'],
                        'runtime_uninvoked_activity_claim:'+role)
        if review_required:
            by_id = {item["agent_id"]: item for item in activity}
            for agent_id in ANALYSIS_ROLES:
                require(by_id[agent_id]["participation_status"] == "contributed", f"required_agent_missing:{agent_id}")
            for agent_id in ANALYSIS_ROLES[1:]:
                require(bool(by_id[agent_id]["agent_task_ids"]), f"required_agent_task_id_missing:{agent_id}")
            require(by_id["delivery-review"]["participation_status"] == "contributed", "delivery_review_missing")

        receipt_identity, completion_status = completion_identity(args.candidate_acceptance, report.get("team_version"))
        result: dict[str, Any] = {
            **receipt_identity,
            "status": completion_status,
            "run_id": report.get("run_id"),
            "client_scope": report.get("client_scope"),
            "team_version": report.get("team_version"),
            "report_revision": report.get("report_revision"),
            "task_type": report.get("task_type"),
            "collaboration_mode": collaboration_mode,
            "review_required": review_required,
            "review_attempt_id": review_attempt_id,
            "review_agent_task_id": review_task_id,
            "claim_guard_status": "claim_guard_passed",
            "quality_gate": quality_receipt,
            "data_quality_scope_gate": data_quality_scope_gate,
            "runtime_gate": dict(analysis=runtime_receipt,review=review_binding),
            "public_output_guard_status": "public_output_guard_passed",
            "expert_activity": activity,
            "artifacts": artifacts,
            "completed_at": utc_now(),
        }
        if release_sha:
            result["release_receipt_sha256"] = release_sha
            result['review_files']=dict(manifest=str(manifest_path.relative_to(report_dir)),
                                        attestation=str(attestation_path.relative_to(report_dir)))
        output = Path(args.output).expanduser().resolve()
        require(output.is_relative_to(report_dir),'completion_output_outside_run')
        require(not output.exists(), "completion_receipt_already_exists")
        latest_runtime,_=validate_analysis_binding(report_dir,report,runtime_config['handoffs'],require_idle=True)
        require(latest_runtime==initial_runtime_receipt,'runtime_selection_changed_before_completion')
        if review_required:
            latest_review,_=validate_review_binding(report_dir,report,manifest,attestation)
            require(latest_review==review_binding,'runtime_review_changed_before_completion')
        for name,expected in runtime_files.items():
            require(sha256(report_dir/name)==expected,'runtime_evidence_changed_before_completion')
        for path,expected in checked_files.items():
            require(sha256(path)==expected,'completion_input_changed')
            require(path.is_relative_to(report_dir) or path==Path(args.version_info).expanduser().resolve(),
                    'completion_evidence_outside_run')
        for item in quality_receipt['inputs']:
            require(sha256(report_dir/item['file'])==item['sha256'], 'quality_changed_before_completion')
        for item in artifacts:
            # Core report files were checked at entry and must still match on release.
            if item['file'] in CORE_ARTIFACTS:
                require(sha256(report_dir/item['file'])==item['sha256'], 'report_changed_before_completion')
        result['input_fingerprints']={str(path.relative_to(report_dir)):expected for path,expected in checked_files.items()
                                      if path.is_relative_to(report_dir)}
        for item in quality_receipt['inputs']:
            result['input_fingerprints'][item['file']]=item['sha256']
        result['input_fingerprints'].update(runtime_files)
        result['input_fingerprints'].update({item['file']:item['sha256'] for item in artifacts if item['file'] in CORE_ARTIFACTS})
        if args.candidate_acceptance:
            with output.open("x", encoding="utf-8") as stream:
                json.dump(result, stream, ensure_ascii=False, indent=2)
                stream.write("\n")
        else:
            runtime=Runtime(report_dir,report['run_id'],report['client_scope'])
            try:
                runtime.commit_completion(result,str(output.relative_to(report_dir)))
            finally: runtime.close()
        print(json.dumps({
            "status": result["status"],
            "team_version": result["team_version"],
            "report_revision": result["report_revision"],
            "task_type": result["task_type"],
            "expert_count": len(activity),
            "output": output.name,
        }, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, IndexError, TypeError, ArithmeticError, ImportError, RecursionError, sqlite3.Error) as exc:
        print(json.dumps({"status": "completion_blocked", "reason": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
