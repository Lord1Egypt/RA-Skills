import unittest

from completion_gate import completion_identity, validate_version_mode


class CompletionModeTests(unittest.TestCase):
    def test_candidate_mode_requires_candidate_metadata(self):
        with self.assertRaisesRegex(ValueError, "candidate_acceptance_requires_candidate_metadata"):
            validate_version_mode({"team_version": "2.0.3-candidate.1", "release_status": "released", "release_ready": True}, True)

    def test_candidate_mode_requires_candidate_version(self):
        with self.assertRaisesRegex(ValueError, "candidate_acceptance_version_invalid"):
            validate_version_mode({"team_version": "2.0.3", "release_status": "candidate", "release_ready": False}, True)

    def test_candidate_identity_has_no_completion_authority(self):
        identity, status = completion_identity(True, "2.0.3-candidate.1")
        self.assertEqual("candidate_pipeline_complete", status)
        self.assertEqual("candidate_runtime_acceptance", identity["artifact_type"])
        self.assertFalse(identity["legacy_compatibility"]["current_completion_authority"])

    def test_formal_mode_still_requires_release(self):
        with self.assertRaisesRegex(ValueError, "candidate_version_not_release_ready"):
            validate_version_mode({"team_version": "2.0.3-candidate.1", "release_status": "candidate", "release_ready": False}, False)

    def test_released_mode_keeps_formal_identity(self):
        self.assertEqual("2.0.3", validate_version_mode({"team_version": "2.0.3", "release_status": "released", "release_ready": True}, False))
        identity, status = completion_identity(False, "2.0.3")
        self.assertEqual("formal_delivery_complete", status)
        self.assertEqual("completion_receipt", identity["artifact_type"])


if __name__ == "__main__":
    unittest.main()
