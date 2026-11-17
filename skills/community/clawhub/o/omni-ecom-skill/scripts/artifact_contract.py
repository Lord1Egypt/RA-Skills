"""Identity rules for native v2 report artifacts and legacy read-only inputs."""
from __future__ import annotations

import re

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:\.[0-9A-Za-z-]+)*)?$")
REPORT_CONTRACT = "omni-ecom.report-package"
REPORT_SCHEMA = "2.0"
HANDOFF_CONTRACT = "omni-ecom.expert-handoff"
HANDOFF_SCHEMA = "2.0"
CLAIM_CONTRACT = "omni-ecom.claim-ledger"
CLAIM_SCHEMA = "2.0"
RECEIPT_CONTRACTS = {
    "pdf_delivery": ("pdf_delivery_receipt", "omni-ecom.pdf-delivery"),
    "completion": ("completion_receipt", "omni-ecom.completion-receipt"),
    "completion_event": ("delivery_completed_event", "omni-ecom.delivery-completed-event"),
    "review_manifest": ("review_manifest", "omni-ecom.review-manifest"),
    "review_result": ("review_result", "omni-ecom.review-result"),
    "review_attestation": ("review_attestation", "omni-ecom.review-attestation"),
    "review_release": ("review_release_receipt", "omni-ecom.review-release"),
    "claim_guard": ("claim_guard_receipt", "omni-ecom.claim-guard"),
    "public_output_guard": ("public_output_guard_receipt", "omni-ecom.public-output-guard"),
    "intake_blocked": ("intake_blocked_receipt", "omni-ecom.intake-blocked"),
    "intake_blocked_event": ("intake_blocked_event", "omni-ecom.intake-blocked-event"),
}
OPERATIONAL_CONTRACTS = {
    "platform_read": ("platform_read_observation", "omni-ecom.platform-read-observation"),
    "controlled_action": ("controlled_action_request", "omni-ecom.controlled-action"),
    "approval": ("approval_decision", "omni-ecom.approval-decision"),
    "policy_decision": ("action_policy_decision", "omni-ecom.action-policy-decision"),
    "connector_call": ("connector_call_record", "omni-ecom.connector-call"),
    "readback": ("action_readback_record", "omni-ecom.action-readback"),
    "outcome": ("action_outcome_record", "omni-ecom.action-outcome"),
}
AUDIT_CONTRACTS = {
    "model_observation": ("model_observation_record", "omni-ecom.model-observation"),
    "human_feedback": ("human_feedback_record", "omni-ecom.human-feedback"),
    "quality_observation": ("quality_observation_record", "omni-ecom.quality-observation"),
    "monitor_policy": ("behavior_monitor_policy_record", "omni-ecom.behavior-monitor-policy"),
    "monitor_comparison": ("behavior_monitor_comparison_record", "omni-ecom.behavior-monitor-comparison"),
    "model_route_assessment": ("model_route_assessment", "omni-ecom.model-route-assessment"),
}
RUNTIME_EVENT_CONTRACT = "omni-ecom.collaboration-event"
RUNTIME_EVENT_TYPES = {
    "member_started", "member_returned", "member_failed", "member_rejected",
    "challenge_started", "challenge_returned", "challenge_failed", "challenge_rejected",
}
BASELINE_CONTRACT = "omni-ecom.analysis-baseline"
TEAM_BOOTSTRAP_CONTRACT = "omni-ecom.team-bootstrap"
RUN_RECORD_CONTRACT = "omni-ecom.run-record"
RUN_SCOPE_CONTRACT = "omni-ecom.run-scope"
FAILURE_DIAGNOSTIC_CONTRACT = "omni-ecom.failure-diagnostic"
ACTION_HISTORY_CONTRACT = "omni-ecom.action-history-view"
STAGE_CONTRACTS = {
    "report_inventory": ("report_inventory", "omni-ecom.report-inventory"),
    "report_clusters": ("report_clusters", "omni-ecom.report-clusters"),
    "chapter_plan": ("chapter_plan", "omni-ecom.chapter-plan"),
    "coverage_guard": ("coverage_guard_receipt", "omni-ecom.coverage-guard"),
}
FACT_CONTRACTS = {
    "normalized_report": ("normalized_report_bundle", "omni-ecom.normalized-report"),
    "metric_gate": ("metric_gate_result", "omni-ecom.metric-gate"),
}
ANALYSIS_CONTRACTS = {
    "depth_declaration": ("analysis_depth_declaration", "omni-ecom.analysis-depth"),
    "depth_guard": ("analysis_depth_guard_receipt", "omni-ecom.analysis-depth-guard"),
    "conflict_scan": ("conflict_scan_result", "omni-ecom.conflict-scan"),
    "conflict_verdict": ("conflict_verdict_ledger", "omni-ecom.conflict-verdict"),
    "causal_review": ("causal_evidence_review", "omni-ecom.causal-evidence-review"),
    "orchestration_plan": ("host_orchestration_plan", "omni-ecom.host-orchestration-plan"),
}


def require(value, reason):
    if not value:
        raise ValueError(reason)


def native_failure_diagnostic(component):
    require(isinstance(component, str) and re.fullmatch(r"[a-z][a-z0-9_-]{1,79}", component),
            "failure_diagnostic_component_invalid")
    return {
        "schema_version": "2.0", "artifact_type": "failure_diagnostic",
        "contract_name": FAILURE_DIAGNOSTIC_CONTRACT, "contract_version": "2.0",
        "component": component,
        "legacy_compatibility": {
            "read_only_import": [f"{FAILURE_DIAGNOSTIC_CONTRACT}@1.0"],
            "current_authority": False,
        },
    }


def validate_failure_diagnostic(payload, component=None):
    require(isinstance(payload, dict) and payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == "failure_diagnostic" and
            payload.get("contract_name") == FAILURE_DIAGNOSTIC_CONTRACT and
            payload.get("contract_version") == "2.0", "failure_diagnostic_identity_invalid")
    if component is not None:
        require(payload.get("component") == component, "failure_diagnostic_component_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{FAILURE_DIAGNOSTIC_CONTRACT}@1.0"],
        "current_authority": False,
    }, "failure_diagnostic_legacy_boundary_invalid")
    return payload.get("component")


def native_action_history_identity():
    return {
        "schema_version": "2.0", "artifact_type": "read_only_action_history_view",
        "contract_name": ACTION_HISTORY_CONTRACT, "contract_version": "2.0",
        "legacy_compatibility": {
            "read_only_import": ["omni-ecom.action-tracker@1.0"],
            "current_execution_authority": False,
            "current_approval_authority": False,
        },
    }


def validate_action_history_identity(payload):
    require(isinstance(payload, dict) and payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == "read_only_action_history_view" and
            payload.get("contract_name") == ACTION_HISTORY_CONTRACT and
            payload.get("contract_version") == "2.0", "action_history_identity_invalid")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": ["omni-ecom.action-tracker@1.0"],
        "current_execution_authority": False,
        "current_approval_authority": False,
    }, "action_history_legacy_boundary_invalid")
    return payload


def native_stage_identity(kind, team_version):
    require(kind in STAGE_CONTRACTS, "stage_contract_unknown")
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "stage_version_invalid")
    artifact_type,contract=STAGE_CONTRACTS[kind]
    return {
        "schema_version": "2.0", "artifact_type": artifact_type,
        "contract_name": contract, "contract_version": "2.0",
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{contract}@1.0"],
            "current_analysis_authority": False,
        },
    }


def validate_stage_identity(payload, kind, expected_team_version=None, run_id=None, client_scope=None):
    require(kind in STAGE_CONTRACTS, "stage_contract_unknown")
    artifact_type,contract=STAGE_CONTRACTS[kind]
    require(isinstance(payload, dict) and payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == artifact_type and payload.get("contract_name") == contract and
            payload.get("contract_version") == "2.0", "stage_identity_invalid")
    version=payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version) and payload.get("team_version") == version,
            "stage_version_invalid")
    if expected_team_version is not None: require(version == expected_team_version, "stage_version_mismatch")
    if run_id is not None: require(payload.get("run_id") == run_id, "stage_run_mismatch")
    if client_scope is not None: require(payload.get("client_scope") == client_scope, "stage_client_scope_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{contract}@1.0"], "current_analysis_authority": False,
    }, "stage_legacy_boundary_invalid")
    return version


def native_fact_identity(kind, team_version):
    require(kind in FACT_CONTRACTS, "fact_contract_unknown")
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "fact_version_invalid")
    artifact_type,contract=FACT_CONTRACTS[kind]
    return {
        "schema_version": "2.0", "artifact_type": artifact_type,
        "contract_name": contract, "contract_version": "2.0",
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{contract}@1.0"],
            "current_numeric_authority": False,
        },
    }


def validate_fact_identity(payload, kind, expected_team_version=None, run_id=None, client_scope=None):
    require(kind in FACT_CONTRACTS, "fact_contract_unknown")
    artifact_type,contract=FACT_CONTRACTS[kind]
    require(isinstance(payload, dict) and payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == artifact_type and payload.get("contract_name") == contract and
            payload.get("contract_version") == "2.0", "fact_identity_invalid")
    version=payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version) and payload.get("team_version") == version,
            "fact_version_invalid")
    if expected_team_version is not None: require(version == expected_team_version, "fact_version_mismatch")
    if run_id is not None: require(payload.get("run_id") == run_id, "fact_run_mismatch")
    if client_scope is not None: require(payload.get("client_scope") == client_scope, "fact_client_scope_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{contract}@1.0"], "current_numeric_authority": False,
    }, "fact_legacy_boundary_invalid")
    return version


def native_report_identity(team_version, handoff_schema="2.0", claim_schema="2.0"):
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "artifact_team_version_invalid")
    require(handoff_schema == "2.0", "artifact_handoff_contract_unsupported")
    require(claim_schema == "2.0", "artifact_claim_contract_unsupported")
    return {
        "schema_version": REPORT_SCHEMA,
        "artifact_type": "report_package",
        "contract_name": REPORT_CONTRACT,
        "contract_version": REPORT_SCHEMA,
        "created_by_team_version": team_version,
        "input_contracts": {"handoff": handoff_schema, "claim_ledger": claim_schema},
        "legacy_compatibility": {
            "read_only_import": ["omni-ecom.report-package@1.0"],
            "execution_permission_inherited": False,
            "approval_inherited": False,
        },
    }


def validate_native_report(report):
    require(isinstance(report, dict), "artifact_report_invalid")
    require(report.get("schema_version") == REPORT_SCHEMA, "artifact_report_schema_not_v2")
    require(report.get("artifact_type") == "report_package", "artifact_type_invalid")
    require(report.get("contract_name") == REPORT_CONTRACT, "artifact_contract_name_invalid")
    require(report.get("contract_version") == REPORT_SCHEMA, "artifact_contract_version_invalid")
    team_version = report.get("team_version")
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "artifact_team_version_invalid")
    require(report.get("created_by_team_version") == team_version, "artifact_creator_version_drift")
    require(report.get("input_contracts") == {"handoff": "2.0", "claim_ledger": "2.0"},
            "artifact_input_contracts_invalid")
    legacy = report.get("legacy_compatibility")
    require(isinstance(legacy, dict) and
            legacy.get("read_only_import") == ["omni-ecom.report-package@1.0"] and
            legacy.get("execution_permission_inherited") is False and
            legacy.get("approval_inherited") is False,
            "artifact_legacy_boundary_invalid")
    return {
        "status": "native_v2_report_contract_verified",
        "contract": f"{REPORT_CONTRACT}@{REPORT_SCHEMA}",
        "team_version": team_version,
        "legacy_inputs_are_read_only": True,
    }


def native_handoff_identity(agent_version):
    require(isinstance(agent_version, str) and SEMVER.fullmatch(agent_version), "handoff_agent_version_invalid")
    return {
        "schema_version": HANDOFF_SCHEMA,
        "artifact_type": "expert_handoff",
        "contract_name": HANDOFF_CONTRACT,
        "contract_version": HANDOFF_SCHEMA,
        "created_by_team_version": agent_version,
        "legacy_compatibility": {
            "read_only_import": ["omni-ecom.expert-handoff@1.0"],
            "current_agent_return": False,
            "execution_permission_inherited": False,
        },
    }


def native_claim_identity(team_version):
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "claim_team_version_invalid")
    return {
        "schema_version": CLAIM_SCHEMA,
        "artifact_type": "numeric_claim_ledger",
        "contract_name": CLAIM_CONTRACT,
        "contract_version": CLAIM_SCHEMA,
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": ["omni-ecom.claim-ledger@1.0"],
            "current_numeric_evidence": False,
            "execution_permission_inherited": False,
        },
    }


def validate_native_claim_identity(payload):
    require(isinstance(payload, dict), "claim_ledger_invalid")
    require(payload.get("schema_version") == CLAIM_SCHEMA, "claim_schema_version_invalid")
    require(payload.get("artifact_type") == "numeric_claim_ledger", "claim_artifact_type_invalid")
    require(payload.get("contract_name") == CLAIM_CONTRACT, "claim_contract_name_invalid")
    require(payload.get("contract_version") == CLAIM_SCHEMA, "claim_contract_version_invalid")
    version = payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version), "claim_team_version_invalid")
    legacy = payload.get("legacy_compatibility")
    require(isinstance(legacy, dict) and
            legacy.get("read_only_import") == ["omni-ecom.claim-ledger@1.0"] and
            legacy.get("current_numeric_evidence") is False and
            legacy.get("execution_permission_inherited") is False,
            "claim_legacy_boundary_invalid")
    return version


def native_receipt_identity(kind, team_version):
    require(kind in RECEIPT_CONTRACTS, "receipt_kind_invalid")
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "receipt_team_version_invalid")
    artifact_type, contract_name = RECEIPT_CONTRACTS[kind]
    return {
        "schema_version": "2.0",
        "artifact_type": artifact_type,
        "contract_name": contract_name,
        "contract_version": "2.0",
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{contract_name}@1.0"],
            "current_completion_authority": False,
        },
    }


def validate_receipt_identity(payload, kind, expected_team_version=None):
    require(kind in RECEIPT_CONTRACTS and isinstance(payload, dict), "receipt_identity_invalid")
    artifact_type, contract_name = RECEIPT_CONTRACTS[kind]
    require(payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == artifact_type and
            payload.get("contract_name") == contract_name and
            payload.get("contract_version") == "2.0", "receipt_identity_invalid")
    version = payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version), "receipt_team_version_invalid")
    if expected_team_version is not None:
        require(version == expected_team_version, "receipt_team_version_mismatch")
    legacy = payload.get("legacy_compatibility")
    require(legacy == {"read_only_import": [f"{contract_name}@1.0"],
                       "current_completion_authority": False}, "receipt_legacy_boundary_invalid")
    return version


def native_operational_identity(kind, team_version):
    require(kind in OPERATIONAL_CONTRACTS, "operational_kind_invalid")
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "operational_team_version_invalid")
    artifact_type, contract_name = OPERATIONAL_CONTRACTS[kind]
    return {
        "schema_version": "2.0",
        "artifact_type": artifact_type,
        "contract_name": contract_name,
        "contract_version": "2.0",
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{contract_name}@1.0"],
            "current_execution_authority": False,
        },
    }


def validate_operational_identity(payload, kind, expected_team_version=None):
    require(kind in OPERATIONAL_CONTRACTS and isinstance(payload, dict), "operational_identity_invalid")
    artifact_type, contract_name = OPERATIONAL_CONTRACTS[kind]
    require(payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == artifact_type and
            payload.get("contract_name") == contract_name and
            payload.get("contract_version") == "2.0", "operational_identity_invalid")
    version = payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version), "operational_team_version_invalid")
    if expected_team_version is not None:
        require(version == expected_team_version, "operational_team_version_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{contract_name}@1.0"],
        "current_execution_authority": False,
    }, "operational_legacy_boundary_invalid")
    return version


def native_audit_identity(kind, team_version):
    require(kind in AUDIT_CONTRACTS, "audit_kind_invalid")
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "audit_team_version_invalid")
    artifact_type, contract_name = AUDIT_CONTRACTS[kind]
    return {
        "schema_version": "2.0",
        "artifact_type": artifact_type,
        "contract_name": contract_name,
        "contract_version": "2.0",
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{contract_name}@1.0"],
            "current_quality_authority": False,
        },
    }


def validate_audit_identity(payload, kind, expected_team_version=None):
    require(kind in AUDIT_CONTRACTS and isinstance(payload, dict), "audit_identity_invalid")
    artifact_type, contract_name = AUDIT_CONTRACTS[kind]
    require(payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == artifact_type and
            payload.get("contract_name") == contract_name and
            payload.get("contract_version") == "2.0", "audit_identity_invalid")
    version = payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version), "audit_team_version_invalid")
    if expected_team_version is not None:
        require(version == expected_team_version, "audit_team_version_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{contract_name}@1.0"],
        "current_quality_authority": False,
    }, "audit_legacy_boundary_invalid")
    return version


def native_runtime_event_identity(event_type, team_version):
    require(event_type in RUNTIME_EVENT_TYPES, "runtime_event_type_invalid")
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "runtime_event_team_version_invalid")
    return {
        "schema_version": "2.0",
        "artifact_type": "collaboration_runtime_event",
        "contract_name": RUNTIME_EVENT_CONTRACT,
        "contract_version": "2.0",
        "event_type": event_type,
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{RUNTIME_EVENT_CONTRACT}@1.0"],
            "current_collaboration_evidence": False,
        },
    }


def validate_runtime_event_identity(payload, event_type, expected_team_version=None):
    require(event_type in RUNTIME_EVENT_TYPES and isinstance(payload, dict), "runtime_event_identity_invalid")
    require(payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == "collaboration_runtime_event" and
            payload.get("contract_name") == RUNTIME_EVENT_CONTRACT and
            payload.get("contract_version") == "2.0" and
            payload.get("event_type") == event_type, "runtime_event_identity_invalid")
    version = payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version), "runtime_event_team_version_invalid")
    if expected_team_version is not None:
        require(version == expected_team_version, "runtime_event_team_version_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{RUNTIME_EVENT_CONTRACT}@1.0"],
        "current_collaboration_evidence": False,
    }, "runtime_event_legacy_boundary_invalid")
    return version


def native_baseline_identity(team_version):
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "baseline_team_version_invalid")
    return {
        "schema_version": "2.0",
        "artifact_type": "analysis_baseline_pack",
        "contract_name": BASELINE_CONTRACT,
        "contract_version": "2.0",
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{BASELINE_CONTRACT}@1.0"],
            "current_analysis_authority": False,
        },
    }


def validate_baseline_identity(payload, expected_team_version=None, run_id=None, client_scope=None):
    require(isinstance(payload, dict) and payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == "analysis_baseline_pack" and
            payload.get("contract_name") == BASELINE_CONTRACT and
            payload.get("contract_version") == "2.0", "baseline_identity_invalid")
    version = payload.get("team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version) and
            payload.get("created_by_team_version") == version, "baseline_team_version_invalid")
    if expected_team_version is not None:
        require(version == expected_team_version, "baseline_team_version_mismatch")
    if run_id is not None:
        require(payload.get("run_id") == run_id, "baseline_run_mismatch")
    if client_scope is not None:
        require(payload.get("client_scope") == client_scope, "baseline_client_scope_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{BASELINE_CONTRACT}@1.0"],
        "current_analysis_authority": False,
    }, "baseline_legacy_boundary_invalid")
    return version


def native_analysis_identity(kind, team_version):
    require(kind in ANALYSIS_CONTRACTS, "analysis_kind_invalid")
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "analysis_team_version_invalid")
    artifact_type, contract_name = ANALYSIS_CONTRACTS[kind]
    return {
        "schema_version": "2.0",
        "artifact_type": artifact_type,
        "contract_name": contract_name,
        "contract_version": "2.0",
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{contract_name}@1.0"],
            "current_analysis_authority": False,
        },
    }


def validate_analysis_identity(payload, kind, expected_team_version=None):
    require(kind in ANALYSIS_CONTRACTS and isinstance(payload, dict), "analysis_identity_invalid")
    artifact_type, contract_name = ANALYSIS_CONTRACTS[kind]
    require(payload.get("schema_version") == "2.0" and payload.get("artifact_type") == artifact_type and
            payload.get("contract_name") == contract_name and payload.get("contract_version") == "2.0",
            "analysis_identity_invalid")
    version = payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version), "analysis_team_version_invalid")
    if expected_team_version is not None:
        require(version == expected_team_version, "analysis_team_version_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{contract_name}@1.0"],
        "current_analysis_authority": False,
    }, "analysis_legacy_boundary_invalid")
    return version


def native_team_bootstrap_identity(team_version):
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "team_bootstrap_version_invalid")
    return {
        "schema_version": "2.0",
        "artifact_type": "team_bootstrap_receipt",
        "contract_name": TEAM_BOOTSTRAP_CONTRACT,
        "contract_version": "2.0",
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{TEAM_BOOTSTRAP_CONTRACT}@1.0"],
            "current_collaboration_authority": False,
        },
    }


def validate_team_bootstrap_identity(payload, expected_team_version=None, run_id=None, client_scope=None):
    require(isinstance(payload, dict) and payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == "team_bootstrap_receipt" and
            payload.get("contract_name") == TEAM_BOOTSTRAP_CONTRACT and
            payload.get("contract_version") == "2.0", "team_bootstrap_identity_invalid")
    version = payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version) and
            payload.get("team_version") == version, "team_bootstrap_version_invalid")
    if expected_team_version is not None:
        require(version == expected_team_version, "team_bootstrap_version_mismatch")
    if run_id is not None:
        require(payload.get("run_id") == run_id, "team_bootstrap_run_mismatch")
    if client_scope is not None:
        require(payload.get("client_scope") == client_scope, "team_bootstrap_client_scope_mismatch")
    require(isinstance(payload.get("client_scope"), str) and bool(payload["client_scope"].strip()),
            "team_bootstrap_client_scope_invalid")
    require(payload.get("host") == "workbuddy", "team_bootstrap_host_invalid")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{TEAM_BOOTSTRAP_CONTRACT}@1.0"],
        "current_collaboration_authority": False,
    }, "team_bootstrap_legacy_boundary_invalid")
    return version


def native_run_record_identity(team_version):
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "run_record_version_invalid")
    return {
        "schema_version": "2.0", "artifact_type": "run_status_snapshot",
        "contract_name": RUN_RECORD_CONTRACT, "contract_version": "2.0",
        "created_by_team_version": team_version, "authority": "derived_from_run_journal_sqlite",
        "legacy_compatibility": {
            "read_only_import": [f"{RUN_RECORD_CONTRACT}@1.0"],
            "current_runtime_authority": False,
        },
    }


def validate_run_record_identity(payload, expected_team_version=None, run_id=None, client_scope=None):
    require(isinstance(payload, dict) and payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == "run_status_snapshot" and
            payload.get("contract_name") == RUN_RECORD_CONTRACT and
            payload.get("contract_version") == "2.0" and
            payload.get("authority") == "derived_from_run_journal_sqlite", "run_record_identity_invalid")
    version = payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version) and
            payload.get("team_version") == version, "run_record_version_invalid")
    if expected_team_version is not None:
        require(version == expected_team_version, "run_record_version_mismatch")
    if run_id is not None:
        require(payload.get("run_id") == run_id, "run_record_run_mismatch")
    if client_scope is not None:
        require(payload.get("client_scope") == client_scope, "run_record_client_scope_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{RUN_RECORD_CONTRACT}@1.0"],
        "current_runtime_authority": False,
    }, "run_record_legacy_boundary_invalid")
    return version


def native_run_scope_identity(team_version):
    require(isinstance(team_version, str) and SEMVER.fullmatch(team_version), "run_scope_version_invalid")
    return {
        "schema_version": "2.0", "artifact_type": "run_scope_receipt",
        "contract_name": RUN_SCOPE_CONTRACT, "contract_version": "2.0",
        "created_by_team_version": team_version,
        "legacy_compatibility": {
            "read_only_import": [f"{RUN_SCOPE_CONTRACT}@1.0"],
            "current_read_authority": False,
        },
    }


def validate_run_scope_identity(payload, expected_team_version=None, run_id=None, client_scope=None):
    require(isinstance(payload, dict) and payload.get("schema_version") == "2.0" and
            payload.get("artifact_type") == "run_scope_receipt" and
            payload.get("contract_name") == RUN_SCOPE_CONTRACT and
            payload.get("contract_version") == "2.0", "run_scope_identity_invalid")
    version = payload.get("created_by_team_version")
    require(isinstance(version, str) and SEMVER.fullmatch(version) and
            payload.get("team_version") == version, "run_scope_version_invalid")
    if expected_team_version is not None:
        require(version == expected_team_version, "run_scope_version_mismatch")
    if run_id is not None:
        require(payload.get("run_id") == run_id, "run_scope_run_mismatch")
    if client_scope is not None:
        require(payload.get("client_scope") == client_scope, "run_scope_client_scope_mismatch")
    require(payload.get("legacy_compatibility") == {
        "read_only_import": [f"{RUN_SCOPE_CONTRACT}@1.0"],
        "current_read_authority": False,
    }, "run_scope_legacy_boundary_invalid")
    return version
