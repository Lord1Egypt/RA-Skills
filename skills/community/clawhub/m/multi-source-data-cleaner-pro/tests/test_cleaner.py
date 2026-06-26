"""End-to-end cleaning test."""
import json, sys, unittest, tempfile
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from profile import _read_rows, profile
from normalize_types import to_iso_date, to_phone, to_number, to_bool, mask_pii
from dedup import dedup
from run_pipeline import run

SAMPLE = ROOT / "examples" / "dirty_sample.csv"

class TestCleaner(unittest.TestCase):
    def test_dates(self):
        self.assertEqual(to_iso_date("2024/03/15"), "2024-03-15")
        self.assertEqual(to_iso_date("2024年5月1日"), "2024-05-01")
        self.assertEqual(to_iso_date("15/06/2024"), "2024-06-15")
    def test_phone(self):
        self.assertTrue(to_phone("13812345678").startswith("+86"))
    def test_bool(self):
        self.assertTrue(to_bool("是"))
        self.assertFalse(to_bool("否"))
    def test_dedup(self):
        rows = _read_rows(SAMPLE)
        d = dedup(rows, ["name", "phone"], threshold=0.85)
        self.assertEqual(d["duplicate_pairs_removed"], 1)
    def test_pii_mask(self):
        self.assertEqual(mask_pii("张三", "name"), "张*")
    def test_pipeline(self):
        with tempfile.TemporaryDirectory() as td:
            out = run(SAMPLE, Path(td), "mask", ["name","phone"])
            self.assertEqual(out["rows_out"], 4)

if __name__ == "__main__":
    unittest.main()
