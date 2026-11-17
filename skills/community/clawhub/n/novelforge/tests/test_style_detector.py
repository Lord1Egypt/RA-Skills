import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.style_detector import detect_style, policy_for_profile


class StyleDetectorTests(unittest.TestCase):
    def test_detector_is_advisory_by_default(self):
        result = detect_style("猫腻式的示例文本", {"blocking": False})
        self.assertEqual(result["status"], "WARNING")
        self.assertFalse(result["blocking"])

    def test_detector_can_be_promoted_by_project_policy(self):
        result = detect_style("自定义风格", {
            "blocking": True,
            "patterns": [{"id": "custom", "pattern": "自定义风格"}],
        })
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(result["blocking"])

    def test_explicit_empty_pattern_list_disables_optional_detector(self):
        result = detect_style("猫腻式的示例文本", {"patterns": []})

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["matches"], [])

    def test_project_mode_can_promote_all_configured_detectors(self):
        policy = policy_for_profile({
            "style_detectors": [{"id": "custom", "pattern": "信号"}],
            "policies": {"style_detector_mode": "blocking"},
        })
        result = detect_style("信号", policy)
        self.assertEqual(result["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
