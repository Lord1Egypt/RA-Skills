#!/usr/bin/env python3

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import anonymize  # noqa: E402
import detect_local  # noqa: E402


class TestLocalLiteBehavior(unittest.TestCase):
    def test_lite_mode_uses_local_detector_without_network(self):
        text = "Email: alice@example.com, Phone: 415-555-1234"

        with patch("anonymize.requests.post") as mock_post:
            result = anonymize.anonymize(text, level="lite")

        mock_post.assert_not_called()
        self.assertTrue(result.get("success"))

        data = result.get("data", {})
        self.assertEqual(data.get("mode"), "local-regex")
        self.assertTrue(data.get("hasPII"))

        anonymized = data.get("anonymizedContent", "")
        self.assertIn("[EMAIL_1]", anonymized)
        self.assertIn("[PHONE_1]", anonymized)

    def test_us_phone_formats_are_detected(self):
        samples = [
            "415-555-1234",
            "(415) 555-1234",
            "415.555.1234",
            "415 555 1234",
            "+1 415 555 1234",
            "4155551234",
            "+1 (415) 555-1234 ext 22",
        ]

        for sample in samples:
            with self.subTest(sample=sample):
                result = detect_local.detect_sensitive_local(f"Contact: {sample}")
                phone_items = [item for item in result["items"] if item["type"] == "phone"]
                self.assertGreaterEqual(len(phone_items), 1)
                self.assertIn("[PHONE_1]", result["sanitizedText"])
                for item in result["items"]:
                    self.assertIn("detectionScore", item)
                    self.assertIn("scoreThreshold", item)
                    self.assertIn("scoreReasons", item)
                    self.assertGreaterEqual(item["detectionScore"], 0.0)
                    self.assertLessEqual(item["detectionScore"], 1.0)
                    self.assertIn("confidence", item)
                    self.assertEqual(item["confidence"], item["detectionScore"])
                    self.assertIn("detectionSource", item)
                self.assertEqual(result["scoringMethod"], "heuristic-v1")
                self.assertEqual(result["detectorVersion"], "local-rules-v1")

    def test_credit_card_luhn_validator_rejects_invalid_number(self):
        result = detect_local.detect_sensitive_local("Card: 4111-1111-1111-1112")
        credit_items = [item for item in result["items"] if item["type"] == "creditCard"]
        self.assertEqual(credit_items, [])

    def test_credit_card_luhn_validator_accepts_valid_number(self):
        result = detect_local.detect_sensitive_local("Card: 4111-1111-1111-1111")
        credit_items = [item for item in result["items"] if item["type"] == "creditCard"]
        self.assertGreaterEqual(len(credit_items), 1)
        self.assertIn("[CREDIT_CARD_1]", result["sanitizedText"])
        validator = credit_items[0]["validator"]
        self.assertTrue(validator["applied"])
        self.assertTrue(validator["passed"])

    def test_profile_thresholds_change_name_detection_sensitivity(self):
        text = "Name: Alice Wang"
        strict_result = detect_local.detect_sensitive_local(text, profile="strict")
        precision_result = detect_local.detect_sensitive_local(text, profile="precision")

        strict_name_items = [item for item in strict_result["items"] if item["type"] == "name"]
        precision_name_items = [item for item in precision_result["items"] if item["type"] == "name"]

        self.assertGreaterEqual(len(strict_name_items), 1)
        self.assertEqual(precision_name_items, [])

    def test_allowlist_suppresses_matching_entity(self):
        allowlist = [{"type": "email", "kind": "exact", "value": "alice@example.com"}]
        result = detect_local.detect_sensitive_local(
            "Email: alice@example.com",
            allowlist_rules=allowlist,
        )
        email_items = [item for item in result["items"] if item["type"] == "email"]
        self.assertEqual(email_items, [])

    def test_blocklist_forces_masking_even_without_regex_pattern_hit(self):
        blocklist = [{"type": "name", "kind": "exact", "value": "Phoenix"}]
        result = detect_local.detect_sensitive_local(
            "Project codename Phoenix will launch this week.",
            blocklist_rules=blocklist,
        )
        name_items = [item for item in result["items"] if item["type"] == "name"]
        self.assertGreaterEqual(len(name_items), 1)
        self.assertTrue(name_items[0]["forcedBlocklist"])
        self.assertIn("[NAME_1]", result["sanitizedText"])

    def test_threshold_override_can_disable_specific_type(self):
        result = detect_local.detect_sensitive_local(
            "Email: alice@example.com",
            threshold_overrides={"email": 0.99},
        )
        email_items = [item for item in result["items"] if item["type"] == "email"]
        self.assertEqual(email_items, [])

    def test_non_phone_lookalike_is_not_detected_as_phone(self):
        text = "Order number 415-555-12345 should remain unchanged."
        result = detect_local.detect_sensitive_local(text)

        phone_items = [item for item in result["items"] if item["type"] == "phone"]
        self.assertEqual(phone_items, [])

    def test_ssn_format_is_not_misclassified_as_phone(self):
        text = "SSN: 123-45-6789"
        result = detect_local.detect_sensitive_local(text)

        phone_items = [item for item in result["items"] if item["type"] == "phone"]
        ssn_items = [item for item in result["items"] if item["type"] == "ssn"]

        self.assertEqual(phone_items, [])
        self.assertGreaterEqual(len(ssn_items), 1)


if __name__ == "__main__":
    unittest.main()
