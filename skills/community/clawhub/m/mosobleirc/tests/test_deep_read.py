from __future__ import annotations
import importlib.util, sys, unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
spec=importlib.util.spec_from_file_location("deep_read_test",ROOT/"scripts"/"deep_read.py")
dr=importlib.util.module_from_spec(spec); spec.loader.exec_module(dr)

class CandidateReviewTests(unittest.TestCase):
    def profile(self, previous=715, integer_digits=5, decimal_digits=3):
        return {"meter_id":1001,"apartment":"Fixture A","address":"Тестовая улица",
                "physical_serial":"TESTCW01","integer_digits":integer_digits,
                "decimal_digits":decimal_digits,"last_provider_value":previous}
    def run_case(self, black, red, *, ambiguous=False, profile=None):
        outer=self
        class Store:
            def __init__(self,*a,**k): pass
            def get_reference(self,meter_id): return profile or outer.profile()
        with patch.object(dr,"StateStore",Store):
            return dr.check_candidate(1001,black,red,ambiguous,Path("/tmp/data"))
    def test_clear_candidate_is_green(self):
        r=self.run_case("00735","609")
        self.assertTrue(r["ok"]); self.assertEqual(r["status"],"GREEN")
        self.assertEqual(r["reading_value"],735.609)
    def test_decimal_boundary_is_profile_driven(self):
        r=self.run_case("00008","611",profile=self.profile(previous=3))
        self.assertEqual(r["reading_value"],8.611); self.assertEqual(r["integer_part"],8)
    def test_decrease_is_review(self):
        r=self.run_case("00235","609")
        self.assertEqual(r["status"],"REVIEW"); self.assertIn("reading_decreased",r["reasons"])
    def test_large_jump_is_review(self):
        r=self.run_case("00086","110",profile=self.profile(previous=3))
        self.assertEqual(r["status"],"REVIEW"); self.assertIn("unusually_large_jump",r["reasons"])
    def test_ambiguous_is_review(self):
        r=self.run_case("00735","609",ambiguous=True)
        self.assertEqual(r["status"],"REVIEW"); self.assertIn("vision_ambiguous",r["reasons"])
    def test_bad_layout_is_review(self):
        r=self.run_case("0735","609")
        self.assertEqual(r["status"],"REVIEW"); self.assertIn("digit_layout_mismatch",r["reasons"])
    def test_missing_profile_layout_is_review(self):
        r=self.run_case("00735","609",profile=self.profile(integer_digits=None))
        self.assertEqual(r["status"],"REVIEW")

class NoNestedAgentTests(unittest.TestCase):
    def test_helper_has_no_nested_openclaw_agent_or_model_subprocess(self):
        text=(ROOT/"scripts"/"deep_read.py").read_text(encoding="utf-8").lower()
        self.assertNotIn("openclaw agent",text)
        self.assertNotIn("subprocess.run",text)
        self.assertNotIn("_run_pass",text)

if __name__=="__main__": unittest.main(verbosity=2)
