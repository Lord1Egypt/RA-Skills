"""Regression tests for native v2 report identity and legacy separation."""
import json
import sys
import tempfile
import contextlib
import io
import unittest
from pathlib import Path
from unittest.mock import patch

from artifact_contract import (native_analysis_identity, native_audit_identity, native_baseline_identity, native_claim_identity, native_failure_diagnostic, native_handoff_identity, native_report_identity,
                               native_team_bootstrap_identity,
                               native_runtime_event_identity,
                               native_operational_identity, native_receipt_identity, validate_native_claim_identity,
                               validate_analysis_identity, validate_audit_identity, validate_baseline_identity, validate_failure_diagnostic, validate_native_report, validate_operational_identity, validate_receipt_identity,
                               validate_runtime_event_identity)
from artifact_contract import validate_team_bootstrap_identity
from claim_guard import validate_claims

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"skills"/"ecom-diagnosis-core"/"scripts"))
from validate_handoff import validate as validate_handoff


class ArtifactContractTests(unittest.TestCase):
    def report(self):
        return dict(native_report_identity("2.0.3-candidate.1"), team_version="2.0.3-candidate.1")

    def test_failure_diagnostic_is_v2_but_never_a_pass_receipt(self):
        value=dict(**native_failure_diagnostic('claim_guard'),status='claim_guard_blocked',
                   errors=['synthetic'],checked_at='2026-09-08T00:00:00+00:00')
        self.assertEqual('claim_guard',validate_failure_diagnostic(value,'claim_guard'))
        with self.assertRaisesRegex(ValueError,'receipt_identity_invalid'):
            validate_receipt_identity(value,'claim_guard')
        import jsonschema
        schema=json.loads((ROOT/'schemas'/'failure-diagnostic.schema.json').read_text(encoding='utf-8'))
        jsonschema.validate(value,schema)

    def test_native_candidate_report_has_v2_contract(self):
        result = validate_native_report(self.report())
        self.assertEqual(result["status"], "native_v2_report_contract_verified")

    def test_old_report_cannot_pose_as_native_v2(self):
        report = self.report(); report["schema_version"] = "1.0"
        with self.assertRaisesRegex(ValueError, "artifact_report_schema_not_v2"):
            validate_native_report(report)

    def test_creator_version_must_match_visible_team_version(self):
        report = self.report(); report["created_by_team_version"] = "1.6.0"
        with self.assertRaisesRegex(ValueError, "artifact_creator_version_drift"):
            validate_native_report(report)

    def test_legacy_never_inherits_approval_or_execution(self):
        for key in ("approval_inherited", "execution_permission_inherited"):
            with self.subTest(key=key):
                report = self.report(); report["legacy_compatibility"][key] = True
                with self.assertRaisesRegex(ValueError, "artifact_legacy_boundary_invalid"):
                    validate_native_report(report)

    def test_schema_declares_v2_native_report(self):
        schema = json.loads((ROOT/"schemas"/"report-package.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], "2.0")
        self.assertIn("created_by_team_version", schema["required"])
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            self.skipTest("jsonschema unavailable")
        Draft202012Validator.check_schema(schema)

    def handoff(self):
        return dict(native_handoff_identity("2.0.3-candidate.1"), run_id="run-native-handoff",
                    agent_id="data-analyst", agent_version="2.0.3-candidate.1",
                    scope={"platform":"演示平台","store":"脱敏店铺","period":"2026-W01","grain":"week"},
                    gate_status="WARN", status="draft_diagnosis", facts=[], judgments=[], hypotheses=[], actions=[],
                    risks=[], missing_data=["缺少推广后台"], evidence_ledger=[])

    def test_native_v2_handoff_is_accepted(self):
        self.assertEqual(validate_handoff(self.handoff()), [])

    def test_v1_handoff_is_history_not_current_return(self):
        body = self.handoff(); body["schema_version"] = "1.0"
        self.assertTrue(any("只读历史迁移" in item for item in validate_handoff(body)))

    def test_handoff_creator_version_cannot_drift(self):
        body = self.handoff(); body["agent_version"] = "2.0.3"
        self.assertTrue(any("created_by_team_version" in item for item in validate_handoff(body)))

    def test_handoff_schema_declares_native_v2(self):
        schema = json.loads((ROOT/"schemas"/"handoff.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], "2.0")
        self.assertEqual(schema["properties"]["contract_name"]["const"], "omni-ecom.expert-handoff")

    def claim_ledger(self):
        return dict(native_claim_identity("2.0.3-candidate.1"), run_id="run-native-claims", client_scope="synthetic",
                    period="2026-07", claims=[dict(claim_id="C-gmv", metric="gmv", value=100, unit="元",
                    period="2026-07", status="verified", source_ref=dict(source_id="synthetic",
                    source_file="source.csv", field="GMV", source_sha256="a"*64))])

    def test_native_v2_claim_ledger_is_accepted(self):
        body = self.claim_ledger()
        self.assertEqual(validate_native_claim_identity(body), "2.0.3-candidate.1")
        self.assertEqual(validate_claims(body)[0], [])

    def test_v1_claim_ledger_cannot_support_current_report(self):
        body = self.claim_ledger(); body["schema_version"] = "1.0"
        self.assertIn("claim_schema_version_invalid", validate_claims(body)[0])

    def test_claim_legacy_boundary_cannot_be_relaxed(self):
        body = self.claim_ledger(); body["legacy_compatibility"]["current_numeric_evidence"] = True
        self.assertIn("claim_legacy_boundary_invalid", validate_claims(body)[0])

    def test_claim_schema_declares_native_v2(self):
        schema = json.loads((ROOT/"schemas"/"claim-ledger.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], "2.0")
        self.assertEqual(schema["properties"]["contract_name"]["const"], "omni-ecom.claim-ledger")

    def test_pdf_receipt_identity_is_version_bound(self):
        body = native_receipt_identity("pdf_delivery", "2.0.3-candidate.1")
        self.assertEqual(validate_receipt_identity(body,"pdf_delivery","2.0.3-candidate.1"),"2.0.3-candidate.1")
        with self.assertRaisesRegex(ValueError,"receipt_team_version_mismatch"):
            validate_receipt_identity(body,"pdf_delivery","2.0.3")

    def test_completion_receipt_identity_is_distinct(self):
        body = native_receipt_identity("completion", "2.0.3")
        self.assertEqual(body["contract_name"],"omni-ecom.completion-receipt")
        with self.assertRaisesRegex(ValueError,"receipt_identity_invalid"):
            validate_receipt_identity(body,"pdf_delivery","2.0.3")

    def test_completion_event_is_distinct_from_completion_receipt(self):
        event=native_receipt_identity('completion_event','2.0.3-candidate.1')
        self.assertEqual(validate_receipt_identity(event,'completion_event','2.0.3-candidate.1'),
                         '2.0.3-candidate.1')
        with self.assertRaisesRegex(ValueError,'receipt_identity_invalid'):
            validate_receipt_identity(event,'completion','2.0.3-candidate.1')

    def test_old_receipt_cannot_gain_current_authority(self):
        body = native_receipt_identity("completion", "2.0.3")
        body["legacy_compatibility"]["current_completion_authority"] = True
        with self.assertRaisesRegex(ValueError,"receipt_legacy_boundary_invalid"):
            validate_receipt_identity(body,"completion","2.0.3")

    def test_pdf_and_completion_schemas_are_v2(self):
        for name,contract in (("pdf-delivery.schema.json","omni-ecom.pdf-delivery"),
                              ("completion-receipt.schema.json","omni-ecom.completion-receipt"),
                              ("delivery-completed-event.schema.json","omni-ecom.delivery-completed-event")):
            with self.subTest(name=name):
                schema=json.loads((ROOT/"schemas"/name).read_text(encoding="utf-8"))
                self.assertEqual(schema["properties"]["schema_version"]["const"],"2.0")
                self.assertEqual(schema["properties"]["contract_name"]["const"],contract)

    def test_review_chain_has_distinct_version_bound_identities(self):
        for kind in ("review_manifest","review_result","review_attestation","review_release"):
            with self.subTest(kind=kind):
                body=native_receipt_identity(kind,"2.0.3-candidate.1")
                self.assertEqual(validate_receipt_identity(body,kind,"2.0.3-candidate.1"),"2.0.3-candidate.1")

    def test_claim_and_public_receipts_cannot_cross_authorize(self):
        body=native_receipt_identity("claim_guard","2.0.3")
        with self.assertRaisesRegex(ValueError,"receipt_identity_invalid"):
            validate_receipt_identity(body,"public_output_guard","2.0.3")

    def test_v1_review_or_guard_receipt_is_not_current(self):
        for kind in ("review_manifest","review_result","review_attestation","review_release","claim_guard","public_output_guard"):
            with self.subTest(kind=kind):
                body=native_receipt_identity(kind,"2.0.3"); body["schema_version"]="1.0"
                with self.assertRaisesRegex(ValueError,"receipt_identity_invalid"):
                    validate_receipt_identity(body,kind,"2.0.3")

    def test_review_and_guard_schemas_are_v2(self):
        pairs=(("review-manifest.schema.json","omni-ecom.review-manifest"),
               ("review-result.schema.json","omni-ecom.review-result"),
               ("review-attestation.schema.json","omni-ecom.review-attestation"),
               ("review-release.schema.json","omni-ecom.review-release"),
               ("claim-guard-receipt.schema.json","omni-ecom.claim-guard"),
               ("public-output-receipt.schema.json","omni-ecom.public-output-guard"))
        for name,contract in pairs:
            with self.subTest(name=name):
                schema=json.loads((ROOT/"schemas"/name).read_text(encoding="utf-8"))
                self.assertEqual(schema["properties"]["schema_version"]["const"],"2.0")
                self.assertEqual(schema["properties"]["contract_name"]["const"],contract)

    def test_wrong_creator_version_blocks_every_new_receipt(self):
        for kind in ("review_manifest","review_result","review_attestation","review_release","claim_guard","public_output_guard"):
            with self.subTest(kind=kind):
                body=native_receipt_identity(kind,"2.0.3")
                with self.assertRaisesRegex(ValueError,"receipt_team_version_mismatch"):
                    validate_receipt_identity(body,kind,"2.0.4")

    def test_public_guard_output_requires_team_version(self):
        import public_output_guard
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw); source=root/"safe.txt"; source.write_text("safe",encoding="utf-8")
            registry=root/"clients.json"; registry.write_text('{"registered_client_terms":[]}',encoding="utf-8")
            args=["public_output_guard.py","--file",str(source),"--registry",str(registry),"--output",str(root/"receipt.json")]
            with patch("sys.argv",args),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(public_output_guard.main(),2)
            self.assertFalse((root/"receipt.json").exists())

    def test_public_guard_writes_native_v2_receipt(self):
        import public_output_guard
        with tempfile.TemporaryDirectory() as raw:
            root=Path(raw); source=root/"safe.txt"; source.write_text("safe",encoding="utf-8")
            registry=root/"clients.json"; registry.write_text('{"registered_client_terms":[]}',encoding="utf-8")
            output=root/"receipt.json"
            args=["public_output_guard.py","--file",str(source),"--registry",str(registry),"--team-version","2.0.3-candidate.1","--output",str(output)]
            with patch("sys.argv",args),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(public_output_guard.main(),0)
            validate_receipt_identity(json.loads(output.read_text(encoding="utf-8")),"public_output_guard","2.0.3-candidate.1")

    def test_controlled_action_and_approval_are_version_bound(self):
        action=native_operational_identity("controlled_action","2.0.3-candidate.1")
        approval=native_operational_identity("approval","2.0.3-candidate.1")
        self.assertEqual(validate_operational_identity(action,"controlled_action","2.0.3-candidate.1"),"2.0.3-candidate.1")
        self.assertEqual(validate_operational_identity(approval,"approval","2.0.3-candidate.1"),"2.0.3-candidate.1")
        with self.assertRaisesRegex(ValueError,"operational_identity_invalid"):
            validate_operational_identity(approval,"controlled_action","2.0.3-candidate.1")

    def test_old_operational_record_cannot_gain_execution_authority(self):
        action=native_operational_identity("controlled_action","2.0.3")
        action["legacy_compatibility"]["current_execution_authority"]=True
        with self.assertRaisesRegex(ValueError,"operational_legacy_boundary_invalid"):
            validate_operational_identity(action,"controlled_action","2.0.3")

    def test_controlled_action_and_approval_schemas_are_v2(self):
        for name,contract in (("controlled-action.schema.json","omni-ecom.controlled-action"),
                              ("approval-decision.schema.json","omni-ecom.approval-decision")):
            with self.subTest(name=name):
                schema=json.loads((ROOT/"schemas"/name).read_text(encoding="utf-8"))
                self.assertEqual(schema["properties"]["schema_version"]["const"],"2.0")
                self.assertEqual(schema["properties"]["contract_name"]["const"],contract)

    def test_execution_audit_schemas_are_distinct_native_v2(self):
        pairs=(("action-policy-decision.schema.json","action_policy_decision","omni-ecom.action-policy-decision"),
               ("connector-call.schema.json","connector_call_record","omni-ecom.connector-call"),
               ("action-readback.schema.json","action_readback_record","omni-ecom.action-readback"),
               ("action-outcome.schema.json","action_outcome_record","omni-ecom.action-outcome"),
               ("behavior-monitor-policy.schema.json","behavior_monitor_policy_record","omni-ecom.behavior-monitor-policy"),
               ("behavior-monitor-comparison.schema.json","behavior_monitor_comparison_record","omni-ecom.behavior-monitor-comparison"),
               ("model-route.schema.json","model_observation_record","omni-ecom.model-observation"),
               ("human-feedback.schema.json","human_feedback_record","omni-ecom.human-feedback"),
               ("quality-observation.schema.json","quality_observation_record","omni-ecom.quality-observation"))
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            Draft202012Validator=None
        for name,artifact_type,contract in pairs:
            with self.subTest(name=name):
                schema=json.loads((ROOT/"schemas"/name).read_text(encoding="utf-8"))
                self.assertEqual(schema["properties"]["schema_version"]["const"],"2.0")
                self.assertEqual(schema["properties"]["artifact_type"]["const"],artifact_type)
                self.assertEqual(schema["properties"]["contract_name"]["const"],contract)
                if Draft202012Validator:
                    Draft202012Validator.check_schema(schema)

    def test_quality_audit_identities_are_distinct_and_version_bound(self):
        for kind in ('model_observation','human_feedback','quality_observation','monitor_policy','monitor_comparison'):
            with self.subTest(kind=kind):
                body=native_audit_identity(kind,'2.0.3-candidate.1')
                self.assertEqual(validate_audit_identity(body,kind,'2.0.3-candidate.1'),'2.0.3-candidate.1')
                with self.assertRaisesRegex(ValueError,'audit_team_version_mismatch'):
                    validate_audit_identity(body,kind,'2.0.3')

    def test_quality_audit_legacy_or_cross_type_cannot_authorize_current_baseline(self):
        body=native_audit_identity('model_observation','2.0.3')
        body['legacy_compatibility']['current_quality_authority']=True
        with self.assertRaisesRegex(ValueError,'audit_legacy_boundary_invalid'):
            validate_audit_identity(body,'model_observation','2.0.3')
        body=native_audit_identity('human_feedback','2.0.3')
        with self.assertRaisesRegex(ValueError,'audit_identity_invalid'):
            validate_audit_identity(body,'quality_observation','2.0.3')

    def test_collaboration_runtime_events_bind_type_and_team_version(self):
        for event_type in ('member_started','member_returned','member_failed','member_rejected',
                           'challenge_started','challenge_returned','challenge_failed','challenge_rejected'):
            with self.subTest(event_type=event_type):
                body=native_runtime_event_identity(event_type,'2.0.3-candidate.1')
                self.assertEqual(validate_runtime_event_identity(body,event_type,'2.0.3-candidate.1'),
                                 '2.0.3-candidate.1')
        body=native_runtime_event_identity('member_started','2.0.3-candidate.1')
        with self.assertRaisesRegex(ValueError,'runtime_event_identity_invalid'):
            validate_runtime_event_identity(body,'member_returned','2.0.3-candidate.1')
        with self.assertRaisesRegex(ValueError,'runtime_event_team_version_mismatch'):
            validate_runtime_event_identity(body,'member_started','2.0.3')
        schema=json.loads((ROOT/'schemas'/'collaboration-event.schema.json').read_text(encoding='utf-8'))
        self.assertEqual(schema['properties']['contract_name']['const'],'omni-ecom.collaboration-event')
        try:
            from jsonschema import Draft202012Validator
        except ImportError:
            return
        Draft202012Validator.check_schema(schema)

    def test_analysis_baseline_is_native_v2_and_version_bound(self):
        body=dict(**native_baseline_identity('2.0.3-candidate.1'),team_version='2.0.3-candidate.1',
                  run_id='run-baseline',client_scope='synthetic')
        self.assertEqual(validate_baseline_identity(body,'2.0.3-candidate.1','run-baseline','synthetic'),
                         '2.0.3-candidate.1')
        body['legacy_compatibility']['current_analysis_authority']=True
        with self.assertRaisesRegex(ValueError,'baseline_legacy_boundary_invalid'):
            validate_baseline_identity(body,'2.0.3-candidate.1','run-baseline','synthetic')
        schema=json.loads((ROOT/'schemas'/'baseline-pack.schema.json').read_text(encoding='utf-8'))
        self.assertEqual(schema['properties']['schema_version']['const'],'2.0')

    def test_depth_and_conflict_analysis_artifacts_are_distinct_native_v2(self):
        pairs=(('depth_declaration','analysis-depth.schema.json','omni-ecom.analysis-depth'),
               ('depth_guard','analysis-depth-guard.schema.json','omni-ecom.analysis-depth-guard'),
               ('conflict_scan','conflict-scan.schema.json','omni-ecom.conflict-scan'),
               ('conflict_verdict','conflict-verdict.schema.json','omni-ecom.conflict-verdict'))
        for kind,name,contract in pairs:
            with self.subTest(kind=kind):
                body=native_analysis_identity(kind,'2.0.3-candidate.1')
                self.assertEqual(validate_analysis_identity(body,kind,'2.0.3-candidate.1'),'2.0.3-candidate.1')
                schema=json.loads((ROOT/'schemas'/name).read_text(encoding='utf-8'))
                self.assertEqual(schema['properties']['schema_version']['const'],'2.0')
                self.assertEqual(schema['properties']['contract_name']['const'],contract)
        body=native_analysis_identity('depth_guard','2.0.3-candidate.1')
        with self.assertRaisesRegex(ValueError,'analysis_identity_invalid'):
            validate_analysis_identity(body,'conflict_scan','2.0.3-candidate.1')

    def test_team_bootstrap_is_native_v2_scope_bound_and_workbuddy_specific(self):
        body=dict(**native_team_bootstrap_identity('2.0.3-candidate.1'),run_id='run-bootstrap',
                  client_scope='synthetic',team_version='2.0.3-candidate.1',host='workbuddy',
                  status='team_created',team_name='synthetic-team',host_mode='interactive',
                  created_at='2026-09-08T00:00:00+00:00')
        self.assertEqual(validate_team_bootstrap_identity(body,'2.0.3-candidate.1','run-bootstrap','synthetic'),
                         '2.0.3-candidate.1')
        with self.assertRaisesRegex(ValueError,'team_bootstrap_client_scope_mismatch'):
            validate_team_bootstrap_identity(body,'2.0.3-candidate.1','run-bootstrap','other')
        schema=json.loads((ROOT/'schemas'/'team-bootstrap.schema.json').read_text(encoding='utf-8'))
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(schema); Draft202012Validator(schema).validate(body)


if __name__ == "__main__":
    unittest.main()
