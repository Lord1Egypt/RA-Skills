from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import gemini_adapter as ga


class PromptTests(unittest.TestCase):
    def test_prompt_binds_expected_meter_identity_and_extraction_only(self):
        prompt = ga.build_prompt({
            "meter_id": 1001,
            "serial": "TESTCW01",
            "meter_type": "ColdWater",
            "apartment": "Fixture A",
        })
        self.assertIn("1001", prompt)
        self.assertIn("TESTCW01", prompt)
        self.assertIn("ColdWater", prompt)
        self.assertIn("same_meter", prompt)
        self.assertIn("integer_part", prompt)
        self.assertIn("Do not submit", prompt)


class NormalizeTests(unittest.TestCase):
    def sample(self, **changes):
        value = {
            "same_meter": True,
            "meter_type": "cold_water",
            "serial_visible": True,
            "serial": "TESTCW01",
            "reading_raw": "00720.123",
            "integer_part": 720,
            "decimal_part": 123,
            "digit_confidence": [0.99, 0.98, 0.97],
            "image_quality": "good",
            "glare": False,
            "blur": False,
            "rotation": 1.5,
            "ambiguous": False,
        }
        value.update(changes)
        return value

    def test_normalize_accepts_dict_and_preserves_typed_fields(self):
        result = ga.normalize_result(self.sample())
        self.assertTrue(result["same_meter"])
        self.assertEqual(result["integer_part"], 720)
        self.assertEqual(result["decimal_part"], 123)
        self.assertEqual(result["digit_confidence"], [0.99, 0.98, 0.97])

    def test_normalize_accepts_json_code_fence(self):
        raw = "```json\n" + json.dumps(self.sample(), ensure_ascii=False) + "\n```"
        result = ga.normalize_result(raw)
        self.assertEqual(result["serial"], "TESTCW01")

    def test_normalize_rejects_missing_required_field(self):
        raw = self.sample()
        del raw["integer_part"]
        with self.assertRaises(ga.GeminiResultError):
            ga.normalize_result(raw)

    def test_normalize_rejects_invalid_confidence(self):
        with self.assertRaises(ga.GeminiResultError):
            ga.normalize_result(self.sample(digit_confidence=[0.9, 1.2]))

    def test_normalize_rejects_non_integer_integer_part(self):
        with self.assertRaises(ga.GeminiResultError):
            ga.normalize_result(self.sample(integer_part=720.5))


class ComparePassesTests(unittest.TestCase):
    def sample(self, integer_part=720, decimal_part=123, serial="TESTCW01"):
        return ga.normalize_result({
            "same_meter": True,
            "meter_type": "cold_water",
            "serial_visible": True,
            "serial": serial,
            "reading_raw": f"{integer_part}.{decimal_part}",
            "integer_part": integer_part,
            "decimal_part": decimal_part,
            "digit_confidence": [0.99, 0.98, 0.97],
            "image_quality": "good",
            "glare": False,
            "blur": False,
            "rotation": 0.0,
            "ambiguous": False,
        })

    def test_compare_passes_marks_agreement(self):
        merged = ga.compare_passes(self.sample(), self.sample())
        self.assertTrue(merged["passes_agree"])
        self.assertEqual(merged["integer_part"], 720)

    def test_compare_passes_marks_reading_disagreement(self):
        merged = ga.compare_passes(self.sample(), self.sample(integer_part=721))
        self.assertFalse(merged["passes_agree"])
        self.assertTrue(merged["ambiguous"])

    def test_compare_passes_marks_identity_disagreement(self):
        merged = ga.compare_passes(self.sample(), self.sample(serial="999999"))
        self.assertFalse(merged["passes_agree"])
        self.assertTrue(merged["ambiguous"])


class DeepReadingGuardTests(unittest.TestCase):
    def profile(self):
        return {"meter_id":1002,"serial":"TESTHW01","physical_serial":"TESTHW01",
                "meter_type":"HotWater","integer_digits":5,"decimal_digits":3}

    def vision(self, black="00008", red="611", serial="TESTHW01", ambiguous=False, meter_type="hot_water"):
        return {"same_meter":True,"meter_type":meter_type,"serial_visible":True,"serial":serial,
                "black_digits":black,"red_digits":red,"display_bbox":[0.25,0.30,0.75,0.48],
                "digit_confidence":[0.99]*8,"ambiguous":ambiguous}

    def test_profile_layout_reconstructs_8_611_not_86_11(self):
        r=ga.validate_deep_reading(self.profile(),self.vision(),self.vision(),["8611"])
        self.assertTrue(r["ok"])
        self.assertEqual(r["integer_part"],8)
        self.assertEqual(r["decimal_part"],611)
        self.assertAlmostEqual(r["reading_value"],8.611,places=3)
        self.assertEqual(r["canonical_digits"],"00008611")

    def test_pass_disagreement_is_fail_closed(self):
        r=ga.validate_deep_reading(self.profile(),self.vision(),self.vision(black="00086",red="110"),["8611"])
        self.assertFalse(r["ok"])
        self.assertEqual(r["status"],"RED")
        self.assertIn("vision_pass_disagreement",r["reasons"])

    def test_local_ocr_mismatch_is_fail_closed(self):
        r=ga.validate_deep_reading(self.profile(),self.vision(),self.vision(),["00008699"])
        self.assertFalse(r["ok"])
        self.assertIn("local_ocr_not_confirmed",r["reasons"])

    def test_three_unanimous_vision_passes_override_noisy_local_ocr(self):
        good=self.vision()
        r=ga.validate_deep_reading(self.profile(),good,good,["00008699"],third=good,previous_value=3)
        self.assertTrue(r["ok"]); self.assertEqual(r["integer_part"],8)
        self.assertIn("local_ocr_disagreed",r.get("warnings",[]))

    def test_wrong_digit_group_lengths_are_rejected(self):
        r=ga.validate_deep_reading(self.profile(),self.vision(black="0008",red="611"),self.vision(black="0008",red="611"),["8611"])
        self.assertFalse(r["ok"])
        self.assertIn("digit_layout_mismatch",r["reasons"])


    def test_two_of_three_resolves_one_bad_pass(self):
        good=self.vision(black="00735",red="609",serial="TESTCW01",meter_type="cold_water")
        bad=self.vision(black="00235",red="609",serial="TESTCW01",meter_type="cold_water")
        profile={"meter_id":1001,"serial":"TESTCW01","physical_serial":"TESTCW01","meter_type":"ColdWater","integer_digits":5,"decimal_digits":3}
        r=ga.validate_deep_reading(profile,good,bad,[],third=good,previous_value=715)
        self.assertTrue(r["ok"]); self.assertEqual(r["integer_part"],735)

    def test_wrong_two_of_three_is_blocked_by_monotonicity(self):
        wrong=self.vision(black="00235",red="609",serial="TESTCW01",meter_type="cold_water")
        right=self.vision(black="00735",red="609",serial="TESTCW01",meter_type="cold_water")
        profile={"meter_id":1001,"serial":"TESTCW01","physical_serial":"TESTCW01","meter_type":"ColdWater","integer_digits":5,"decimal_digits":3}
        r=ga.validate_deep_reading(profile,wrong,wrong,[],third=right,previous_value=715)
        self.assertFalse(r["ok"]); self.assertIn("reading_decreased",r["reasons"])

    def test_three_way_disagreement_is_fail_closed(self):
        a=self.vision(black="00735",red="609"); b=self.vision(black="00736",red="609"); c=self.vision(black="00735",red="610")
        r=ga.validate_deep_reading(self.profile(),a,b,[],third=c,previous_value=3)
        self.assertFalse(r["ok"]); self.assertIn("no_vision_consensus",r["reasons"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
