# -*- coding: utf-8 -*-
"""pp_api SDK 契约：返回 dict、异常不静默、关键键齐全。"""
import unittest

try:
    from tests._common import AI_TEXT
except ImportError:  # 直跑模式（-s tests）
    from _common import AI_TEXT
import pp_api


class TestSdkContracts(unittest.TestCase):
    def test_detect_text_returns_dict(self):
        r = pp_api.detect_text(AI_TEXT)
        self.assertIsInstance(r, dict)
        self.assertIn("overall_ai_score", r)

    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            pp_api.detect_text("")
        with self.assertRaises(ValueError):
            pp_api.detect_text(None)

    def test_gate_text_keys(self):
        r = pp_api.gate_text(AI_TEXT)
        self.assertIsInstance(r, dict)
        for k in ("composite_ai_risk", "verdict"):
            self.assertIn(k, r)

    def test_workflow_required_keys(self):
        r = pp_api.workflow(AI_TEXT)
        for k in ("detect", "paragraphs", "gate", "terms", "smell", "style",
                  "quality", "aigc_label", "integrity_notice", "fix_suggest"):
            self.assertIn(k, r, f"workflow 缺键: {k}")

    def test_workflow_fix_block(self):
        r = pp_api.workflow(AI_TEXT)
        fx = r["fix_suggest"]
        self.assertIsNotNone(fx.get("stats"))
        self.assertIn("type_counts", fx["stats"])

    def test_engine_version_string(self):
        self.assertTrue(str(pp_api.engine_version()))


if __name__ == "__main__":
    unittest.main()
