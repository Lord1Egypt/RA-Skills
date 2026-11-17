import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from release_acceptance_guard import ALL_DOMAINS, OPTIONAL_DOMAINS, REQUIRED_DOMAINS, REQUIRED_KINDS, evaluate, validate_receipt


class ReleaseAcceptanceGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_json(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")
        return path

    def source(self, domain, host=None):
        value = {
            "status": "PASS", "version": "2.0.3", "environment": "live",
            "acceptance_domain": domain, "evidence_kind": REQUIRED_KINDS[domain],
        }
        if host:
            value["host"] = host
        if domain.endswith("native_multi_agent_pdf"):
            value.update(pipeline_completion_verified=True, multi_agent_complete=True, pdf_review_passed=True)
        elif domain == "platform_api_read":
            value.update(scoped_read_observation_passed=True, source_fingerprint_verified=True, credential_scope_verified=True)
        elif domain == "controlled_action_readback":
            value.update(explicit_approval_verified=True, bounded_action_verified=True, idempotency_verified=True, readback_verified=True)
        else:
            value.update(two_live_cohorts_verified=True, minimum_sample_verified=True, human_route_acceptance_recorded=True, automatic_route_switch=False)
        return value

    def ledger(self, omit=None, mutate=None, include_optional=False):
        evidence = []
        domains = ALL_DOMAINS if include_optional else REQUIRED_DOMAINS
        for domain, host in domains.items():
            if domain == omit:
                continue
            source = self.write_json(f"{domain}.json", self.source(domain, host))
            item = {"domain": domain, "status": "PASS", "environment": "live", "evidence_kind": REQUIRED_KINDS[domain],
                    "source_file": source.name, "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
            if host:
                item["host"] = host
            evidence.append(item)
        value = {"artifact_type": "omni-ecom.release-acceptance-ledger@2.0", "target_version": "2.0.3",
                 "environment": "real_external_acceptance", "evidence": evidence}
        if mutate:
            mutate(value)
        return self.write_json("ledger.json", value)

    def test_complete_contract_builds_verified_receipt(self):
        receipt, errors = evaluate(self.ledger(), "2.0.3")
        self.assertEqual([], errors)
        self.assertEqual("release_acceptance_verified", receipt["status"])
        self.assertEqual({domain: "not_enabled" for domain in OPTIONAL_DOMAINS}, receipt["optional_capabilities"])
        self.assertEqual([], validate_receipt(receipt, "2.0.3"))

    def test_optional_capabilities_enable_only_with_live_evidence(self):
        receipt, errors = evaluate(self.ledger(include_optional=True), "2.0.3")
        self.assertEqual([], errors)
        self.assertEqual({domain: "enabled" for domain in OPTIONAL_DOMAINS}, receipt["optional_capabilities"])

    def test_missing_domain_fails_closed(self):
        receipt, errors = evaluate(self.ledger(omit="codex_native_multi_agent_pdf"), "2.0.3")
        self.assertIn("acceptance_domain_missing:codex_native_multi_agent_pdf", errors)
        self.assertEqual("release_acceptance_incomplete", receipt["status"])

    def test_mock_marker_is_rejected(self):
        def mutate(value):
            value["evidence"][0]["notes"] = "mock run"
        _, errors = evaluate(self.ledger(mutate=mutate), "2.0.3")
        self.assertTrue(any("synthetic_marker" in error for error in errors))

    def test_hash_change_is_rejected(self):
        ledger = self.ledger(include_optional=True)
        value = json.loads(ledger.read_text(encoding="utf-8"))
        source = self.root / value["evidence"][0]["source_file"]
        source.write_text(source.read_text(encoding="utf-8") + " ", encoding="utf-8")
        _, errors = evaluate(ledger, "2.0.3")
        self.assertTrue(any("source_hash_mismatch" in error for error in errors))

    def test_wrong_host_is_rejected(self):
        def mutate(value):
            value["evidence"][0]["host"] = "codex"
        _, errors = evaluate(self.ledger(mutate=mutate), "2.0.3")
        self.assertTrue(any("host_mismatch" in error for error in errors))

    def test_runtime_without_pdf_review_is_rejected(self):
        ledger = self.ledger()
        value = json.loads(ledger.read_text(encoding="utf-8"))
        item = next(item for item in value["evidence"] if item["domain"] == "workbuddy_native_multi_agent_pdf")
        source = self.root / item["source_file"]
        payload = json.loads(source.read_text(encoding="utf-8")); payload["pdf_review_passed"] = False
        source.write_text(json.dumps(payload), encoding="utf-8")
        item["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        ledger.write_text(json.dumps(value), encoding="utf-8")
        _, errors = evaluate(ledger, "2.0.3")
        self.assertIn("acceptance_source_pdf_review_passed_missing:workbuddy_native_multi_agent_pdf", errors)

    def test_action_without_readback_is_rejected(self):
        ledger = self.ledger(include_optional=True)
        value = json.loads(ledger.read_text(encoding="utf-8"))
        item = next(item for item in value["evidence"] if item["domain"] == "controlled_action_readback")
        source = self.root / item["source_file"]
        payload = json.loads(source.read_text(encoding="utf-8")); payload["readback_verified"] = False
        source.write_text(json.dumps(payload), encoding="utf-8")
        item["sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
        ledger.write_text(json.dumps(value), encoding="utf-8")
        _, errors = evaluate(ledger, "2.0.3")
        self.assertIn("acceptance_source_readback_verified_missing:controlled_action_readback", errors)

    def test_released_receipt_target_must_match(self):
        receipt, errors = evaluate(self.ledger(), "2.0.3")
        self.assertEqual([], errors)
        self.assertIn("release_acceptance_target_version_mismatch", validate_receipt(receipt, "2.0.4"))


if __name__ == "__main__":
    unittest.main()
