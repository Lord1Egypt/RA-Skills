"""Minimal sanity test — exercise the bundled extractor end-to-end."""
import json, sys, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from segment_sections import segment_sections
from rule_extract import rule_extract
from assemble_fhir import assemble_fhir
from validate_fhir import validate_fhir


SAMPLE = (ROOT / "examples" / "admission_input.txt").read_text(encoding="utf-8")


class TestPipeline(unittest.TestCase):
    def test_sections(self):
        s = segment_sections(SAMPLE)
        self.assertIn("diagnosis", s)
        self.assertIn("discharge_instructions", s)

    def test_entities(self):
        s = segment_sections(SAMPLE)
        e = rule_extract(SAMPLE, s, "admission")
        self.assertEqual(len(e["diagnosis"]), 3)
        self.assertGreaterEqual(len(e["vitals"]), 4)
        self.assertGreaterEqual(len(e["medication"]), 2)

    def test_fhir(self):
        s = segment_sections(SAMPLE)
        e = rule_extract(SAMPLE, s, "admission")
        b = assemble_fhir(e, "admission")
        v = validate_fhir(b)
        self.assertTrue(v["ok"], msg=str(v["issues"]))
        self.assertGreater(v["entry_count"], 5)


if __name__ == "__main__":
    unittest.main()
