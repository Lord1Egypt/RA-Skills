#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(PACKAGE_ROOT))

from modeio_redact.adapters.coverage import summarize_redaction_removal_coverage  # noqa: E402
from modeio_redact.core.errors import ApplyError, VerificationError  # noqa: E402
from modeio_redact.core.models import InputSource  # noqa: E402
from modeio_redact.core.pipeline import RedactionFilePipeline, RedactionProviderPipeline  # noqa: E402
from modeio_redact.core.policy import AssurancePolicy  # noqa: E402
from modeio_redact.planning.plan_builder import build_redaction_plan  # noqa: E402


class TestPipelineSkeleton(unittest.TestCase):
    def test_build_redaction_plan_resolves_multiple_spans(self):
        plan = build_redaction_plan(
            canonical_text="Email: alice@example.com; Backup: alice@example.com",
            mapping_entries=[
                {
                    "placeholder": "[EMAIL_1]",
                    "original": "alice@example.com",
                    "type": "email",
                }
            ],
        )

        self.assertEqual(plan.expected_count, 2)
        self.assertEqual(plan.spans[0].start, 7)

    def test_pipeline_writes_text_output_with_marker_and_sidecar(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "incident.txt"
            output_path = Path(tmpdir) / "incident.redacted.txt"
            input_path.write_text("Email: alice@example.com", encoding="utf-8")

            source = InputSource(
                content="Email: alice@example.com",
                input_type="file",
                input_path=str(input_path),
                extension=".txt",
                handler_key="text",
            )
            pipeline = RedactionFilePipeline(policy=AssurancePolicy.best_effort())

            result = pipeline.run(
                source=source,
                anonymized_content="Email: [EMAIL_1]",
                mapping_entries=[
                    {
                        "placeholder": "[EMAIL_1]",
                        "original": "alice@example.com",
                        "type": "email",
                    }
                ],
                resolved_output_path=output_path,
                map_ref={
                    "mapId": "test-map-id",
                    "mapPath": "/tmp/test-map-id.json",
                    "entryCount": 1,
                },
            )

            output_content = output_path.read_text(encoding="utf-8")
            self.assertIn("privacy-protector-map-id: test-map-id", output_content)
            self.assertIn("[EMAIL_1]", output_content)
            self.assertEqual(result.output_path, str(output_path))
            self.assertTrue(result.verification_report.skipped)
            self.assertEqual(result.apply_report.expected_count, 1)
            self.assertEqual(result.apply_report.applied_count, 1)
            self.assertIsNotNone(result.sidecar_path)
            self.assertTrue(Path(result.sidecar_path).exists())

    def test_pipeline_strict_coverage_raises_on_apply_mismatch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "incident.txt"
            output_path = Path(tmpdir) / "incident.redacted.txt"
            input_path.write_text("Email: alice@example.com", encoding="utf-8")

            source = InputSource(
                content="Email: alice@example.com",
                input_type="file",
                input_path=str(input_path),
                extension=".txt",
                handler_key="text",
            )
            pipeline = RedactionFilePipeline(
                policy=AssurancePolicy(
                    level="best_effort",
                    fail_on_coverage_mismatch=True,
                    fail_on_residual_findings=False,
                )
            )

            with self.assertRaises(ApplyError):
                pipeline.run(
                    source=source,
                    anonymized_content="Email: alice@example.com",
                    mapping_entries=[
                        {
                            "placeholder": "[EMAIL_1]",
                            "original": "alice@example.com",
                            "type": "email",
                        }
                    ],
                    resolved_output_path=output_path,
                    map_ref=None,
                )

    def test_pipeline_verified_policy_raises_when_residual_found(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = Path(tmpdir) / "incident.txt"
            output_path = Path(tmpdir) / "incident.redacted.txt"
            input_path.write_text("Email: alice@example.com", encoding="utf-8")

            source = InputSource(
                content="Email: alice@example.com",
                input_type="file",
                input_path=str(input_path),
                extension=".txt",
                handler_key="text",
            )
            pipeline = RedactionFilePipeline(policy=AssurancePolicy.verified())

            with self.assertRaises(VerificationError):
                pipeline.run(
                    source=source,
                    anonymized_content="Email: [EMAIL_1] (source alice@example.com)",
                    mapping_entries=[
                        {
                            "placeholder": "[EMAIL_1]",
                            "original": "alice@example.com",
                            "type": "email",
                        }
                    ],
                    resolved_output_path=output_path,
                    map_ref=None,
                )

    def test_provider_pipeline_uses_local_provider_for_lite(self):
        def _unused_remote(*_args, **_kwargs):
            raise AssertionError("remote provider should not be used for lite")

        provider_pipeline = RedactionProviderPipeline(api_anonymize_callable=_unused_remote)
        result = provider_pipeline.run(
            content="Email: alice@example.com",
            level="lite",
            input_type="text",
        )

        self.assertTrue(result.has_pii)
        self.assertIn("[EMAIL_1]", result.anonymized_content)

    def test_provider_pipeline_uses_remote_provider_for_non_lite(self):
        captured = {}

        def _fake_remote(content, *, level, sender_code=None, recipient_code=None, input_type="text"):
            captured["content"] = content
            captured["level"] = level
            captured["sender_code"] = sender_code
            captured["recipient_code"] = recipient_code
            captured["input_type"] = input_type
            return {
                "success": True,
                "data": {
                    "anonymizedContent": "Email: [EMAIL_1]",
                    "hasPII": True,
                    "mapping": [
                        {
                            "anonymized": "[EMAIL_1]",
                            "original": "alice@example.com",
                            "type": "email",
                        }
                    ],
                },
            }

        provider_pipeline = RedactionProviderPipeline(api_anonymize_callable=_fake_remote)
        result = provider_pipeline.run(
            content="Email: alice@example.com",
            level="dynamic",
            input_type="file",
            sender_code="CN SHA",
            recipient_code="US NYC",
        )

        self.assertEqual(captured["level"], "dynamic")
        self.assertEqual(captured["input_type"], "file")
        self.assertEqual(result.anonymized_content, "Email: [EMAIL_1]")
        self.assertTrue(result.has_pii)
        self.assertEqual(len(result.items), 1)
        self.assertEqual(result.items[0].placeholder, "[EMAIL_1]")

    def test_redaction_removal_coverage_counts_removed_originals(self):
        plan = build_redaction_plan(
            canonical_text="Email: alice@example.com\nPhone: 415-555-1234",
            mapping_entries=[
                {
                    "placeholder": "[EMAIL_1]",
                    "original": "alice@example.com",
                    "type": "email",
                },
                {
                    "placeholder": "[PHONE_1]",
                    "original": "415-555-1234",
                    "type": "phone",
                },
            ],
        )

        report = summarize_redaction_removal_coverage("Email:\nPhone:", plan)
        self.assertEqual(report.expected_count, 2)
        self.assertEqual(report.applied_count, 2)
        self.assertEqual(report.found_count, 2)
        self.assertEqual(len(report.missed_spans), 0)

        partial_report = summarize_redaction_removal_coverage("Email: alice@example.com\nPhone:", plan)
        self.assertEqual(partial_report.expected_count, 2)
        self.assertEqual(partial_report.applied_count, 1)
        self.assertEqual(len(partial_report.missed_spans), 1)


if __name__ == "__main__":
    unittest.main()
