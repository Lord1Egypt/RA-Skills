import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "classify_intraday_phase.py"
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("classify_intraday_phase", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def base_row():
    return {
        "symbol": "CYCU",
        "timestamp": "2026-07-30 10:18 ET",
        "candidate_status": "EXECUTE",
        "position_state": "FLAT",
        "prev_close": 0.2702,
        "open_price": 0.3233,
        "last_price": 0.4771,
        "high_price": 0.54,
        "vwap": 0.4165,
        "bid": 0.475,
        "ask": 0.477,
        "ma5": 0.46,
        "ma10": 0.43,
        "ma20": 0.40,
        "current_bar_volume": 12_000_000,
        "bar_volume_ma5": 8_000_000,
        "macd_hist": 0.02,
        "halted": False,
        "premarket_supply_risk": False,
        "dilution_overhang": False,
        "turnover_expanding": True,
        "retest_confirmed": True,
        "official_primary_source": True,
        "catalyst_age_minutes": 75,
    }


class IntradayPhaseTests(unittest.TestCase):
    def test_trend_expansion_allows_confirmed_retest(self):
        result = MODULE.classify(base_row())
        self.assertEqual(result["phase"], "TREND_EXPANSION")
        self.assertEqual(result["entry_action"], "ENTER_ON_RETEST")
        self.assertEqual(result["catalyst_stage"], "FERMENTING")

    def test_parabolic_extension_blocks_chase(self):
        row = base_row()
        row.update(
            last_price=0.81,
            high_price=0.82,
            vwap=0.5173,
            ma5=0.70,
            ma10=0.62,
            ma20=0.55,
        )
        result = MODULE.classify(row)
        self.assertEqual(result["phase"], "PARABOLIC_EXTENSION")
        self.assertEqual(result["entry_action"], "NO_NEW_ENTRY")

    def test_cycu_close_is_blow_off_distribution(self):
        row = base_row()
        row.update(
            position_state="LONG",
            last_price=1.61,
            high_price=1.84,
            vwap=0.865,
            ma5=1.672,
            ma10=1.604,
            ma20=1.567,
            current_bar_volume=76_478_010,
            bar_volume_ma5=17_978_690,
            macd_hist=-0.008,
        )
        result = MODULE.classify(row)
        self.assertEqual(result["phase"], "BLOW_OFF_DISTRIBUTION")
        self.assertEqual(result["entry_action"], "NO_NEW_ENTRY")
        self.assertEqual(result["position_action"], "EXIT_RUNNER")
        self.assertAlmostEqual(result["metrics"]["volume_impulse"], 4.2538, places=3)

    def test_halt_and_dilution_are_hard_blocks(self):
        halted = base_row()
        halted.update(halted=True, position_state="LONG")
        halted_result = MODULE.classify(halted)
        self.assertEqual(halted_result["phase"], "HALTED")
        self.assertEqual(halted_result["entry_action"], "NO_NEW_ENTRY")
        self.assertEqual(halted_result["position_action"], "RECHECK_AFTER_RESUME")

        diluted = base_row()
        diluted["dilution_overhang"] = "registered resale"
        diluted_result = MODULE.classify(diluted)
        self.assertEqual(diluted_result["entry_action"], "NO_NEW_ENTRY")
        self.assertIn("DILUTION_OVERHANG", diluted_result["risk_flags"])

        supplied = base_row()
        supplied["premarket_supply_risk"] = "registered direct offering"
        supplied_result = MODULE.classify(supplied)
        self.assertEqual(supplied_result["entry_action"], "NO_NEW_ENTRY")
        self.assertIn("SUPPLY_RISK_CONFIRMED", supplied_result["risk_flags"])

    def test_upstream_status_and_missing_data_block(self):
        watch = base_row()
        watch["candidate_status"] = "WATCH"
        self.assertEqual(MODULE.classify(watch)["entry_action"], "NO_NEW_ENTRY")

        missing = base_row()
        missing["vwap"] = ""
        missing_result = MODULE.classify(missing)
        self.assertEqual(missing_result["phase"], "WAIT_DATA")
        self.assertIn("vwap", missing_result["missing"])

    def test_position_size_formula(self):
        row = base_row()
        row.update(account_equity=100_000, entry_price=0.50, stop_price=0.45)
        sizing = MODULE.classify(row)["position_size"]
        self.assertEqual(sizing["risk_budget"], 250.00)
        self.assertEqual(sizing["risk_per_share"], 0.05)
        self.assertEqual(sizing["shares"], 5_000)
        self.assertEqual(sizing["notional"], 2_500.00)

    def test_output_enums(self):
        result = MODULE.classify(base_row())
        self.assertIn(result["phase"], MODULE.PHASES)
        self.assertIn(result["entry_action"], MODULE.ENTRY_ACTIONS)
        self.assertIn(result["position_action"], MODULE.POSITION_ACTIONS)

    def test_json_and_csv_cli_smoke(self):
        for suffix in (".json", ".csv"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as temp_dir:
                path = Path(temp_dir) / f"snapshots{suffix}"
                row = base_row()
                if suffix == ".json":
                    path.write_text(json.dumps([row]), encoding="utf-8")
                else:
                    with path.open("w", encoding="utf-8", newline="") as handle:
                        writer = csv.DictWriter(handle, fieldnames=row.keys())
                        writer.writeheader()
                        writer.writerow(row)
                completed = subprocess.run(
                    [sys.executable, str(SCRIPT), str(path), "--format", "json"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                data = json.loads(completed.stdout)
                self.assertEqual(data[0]["phase"], "TREND_EXPANSION")


if __name__ == "__main__":
    unittest.main()
