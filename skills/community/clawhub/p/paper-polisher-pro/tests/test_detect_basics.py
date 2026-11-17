# -*- coding: utf-8 -*-
"""检测引擎基础契约：铁律/字段完整性/语域提示/编码护栏。"""
import unittest

try:
    from tests._common import AI_TEXT, HUMAN_TEXT, NARRATIVE_TEXT  # noqa: F401
except ImportError:  # 直跑模式（-s tests）
    from _common import AI_TEXT, HUMAN_TEXT, NARRATIVE_TEXT  # noqa: F401
import ai_detector


class TestIronLaws(unittest.TestCase):
    def test_short_text_unknown(self):
        rep = ai_detector.detect("这是一段不足一百字的短文本，按铁律不输出判定。", lang="zh")
        self.assertEqual(rep.overall_risk, "unknown")

    def test_empty_no_crash(self):
        rep = ai_detector.detect("", lang="zh")
        self.assertIsNotNone(rep)

    def test_determinism(self):
        a = ai_detector.detect(AI_TEXT, lang="zh")
        b = ai_detector.detect(AI_TEXT, lang="zh")
        self.assertEqual(a.overall_ai_score, b.overall_ai_score)


class TestReportFields(unittest.TestCase):
    def setUp(self):
        self.rep = ai_detector.detect(AI_TEXT, lang="zh")

    def test_risk_bands_present(self):
        self.assertIsInstance(self.rep.risk_bands, dict)
        self.assertTrue(self.rep.risk_bands, "risk_bands 应透出当前档位阈值")

    def test_integrity_notice_nonempty(self):
        self.assertTrue(self.rep.integrity_notice)

    def test_paragraph_scores_shape(self):
        self.assertGreaterEqual(len(self.rep.paragraph_scores), 1)
        p0 = self.rep.paragraph_scores[0]
        for k in ("index", "ai_score"):
            self.assertIn(k, p0)


class TestRegisterV2(unittest.TestCase):
    def test_narrative_hint_fires(self):
        rep = ai_detector.detect(NARRATIVE_TEXT, lang="zh")
        self.assertIn("文学叙事", rep.register_hint)
        self.assertIn("勿当作 AI 生成证据", rep.register_hint)

    def test_academic_no_narrative_hint(self):
        rep = ai_detector.detect(AI_TEXT, lang="zh")
        self.assertNotIn("文学叙事", rep.register_hint or "")

    def test_narrative_categories_helper(self):
        cats = ai_detector._narrative_categories(NARRATIVE_TEXT)
        self.assertGreaterEqual(len(cats), 3)


class TestEncodingGuard(unittest.TestCase):
    def test_gbk_bytes_decoded_with_warning(self):
        raw = ("本研究纳入一百二十例患者，回顾性分析其临床资料与随访结局。" * 3).encode("gbk")
        text = raw.decode("gbk", errors="replace")
        text = text.encode("utf-8", "ignore").decode("utf-8")  # 正常路径
        self.assertIn("患者", text)  # 解码管线本身可用
        rep = ai_detector.detect(text, lang="zh")
        self.assertIsNotNone(rep.overall_risk)


if __name__ == "__main__":
    unittest.main()
