from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = SKILL_ROOT / "scripts"
SCRIPT_PATH = SCRIPT_DIR / "score_candidates.py"
sys.path.insert(0, str(SCRIPT_DIR))

from score_candidates import VALID_STATUSES, classify, load_rows, markdown  # noqa: E402


def base_candidate() -> dict[str, object]:
    return {
        "symbol": "TEST",
        "timestamp": "2026-07-22T09:35:00-04:00",
        "market_status": "Open",
        "security_type": "Common Stock",
        "listed_days": 100,
        "prev_close": 1.00,
        "pre_price": 2.20,
        "pre_high": 2.30,
        "pre_volume": 1_000_000,
        "bid": 2.19,
        "ask": 2.20,
        "float_shares": 1_000_000,
        "median_dollar_volume_20": 500_000,
        "avg_volume_20": 100_000,
        "split_today": False,
        "post_split": False,
        "halted": False,
        "premarket_supply_risk": False,
        "supply_risk_source": "SEC EDGAR checked",
        "supply_risk_checked_at": "2026-07-22T08:30:00-04:00",
        "dilution_overhang": False,
    }


def conventional_candidate() -> dict[str, object]:
    row = base_candidate()
    row.update(
        {
            "open_price": 2.10,
            "last_price": 2.40,
            "regular_volume": 2_000_000,
            "vwap": 2.20,
            "first_5m_structure": "confirmed",
        }
    )
    return row


def cphi_candidate() -> dict[str, object]:
    row = base_candidate()
    row.update(
        {
            "pre_price": 1.10,
            "pre_high": 1.15,
            "open_price": 1.05,
            "last_price": 2.00,
            "regular_volume": 1_500_000,
            "vwap": 1.50,
            "first_5m_structure": "confirmed",
            "prior_abnormal_volume_warmup": True,
            "turnover_expanding": True,
        }
    )
    return row


def after_hours_candidate() -> dict[str, object]:
    row = base_candidate()
    row.update(
        {
            "symbol": "AFTER",
            "timestamp": "2026-08-13T18:00:00-04:00",
            "market_status": "After-Hours",
            "regular_close": 1.00,
            "after_price": 1.50,
            "after_high": 1.55,
            "after_volume": 500_000,
            "after_bid": 1.49,
            "after_ask": 1.50,
            "after_hours_catalyst_quality": "EARNINGS_SUPPORTED",
            "after_hours_supply_thesis": "UNKNOWN",
        }
    )
    return row


class ClassificationTests(unittest.TestCase):
    def test_conventional_gap_executes(self) -> None:
        result = classify(conventional_candidate())
        self.assertEqual(result["status"], "EXECUTE")
        self.assertEqual(result["path_type"], "CONVENTIONAL_GAP")

    def test_cphi_subtype_requires_all_confirmations(self) -> None:
        result = classify(cphi_candidate())
        self.assertEqual(result["status"], "EXECUTE")
        self.assertEqual(result["path_type"], "CPHI_SUBTYPE")

    def test_cphi_missing_warmup_waits_for_data(self) -> None:
        row = cphi_candidate()
        row.pop("prior_abnormal_volume_warmup")
        result = classify(row)
        self.assertEqual(result["status"], "WAIT_DATA")
        self.assertIn("prior_abnormal_volume_warmup", result["unknown"])

    def test_cphi_failed_turnover_expansion_is_watch(self) -> None:
        row = cphi_candidate()
        row["turnover_expanding"] = False
        result = classify(row)
        self.assertEqual(result["status"], "WATCH")
        self.assertIn("turnover_expanding", result["failed"])

    def test_premarket_fade_over_twenty_percent_is_watch(self) -> None:
        row = base_candidate()
        row.update(
            {
                "market_status": "Pre-Market",
                "pre_price": 2.00,
                "pre_high": 3.00,
                "pre_volume": 1_000_000,
            }
        )
        result = classify(row)
        self.assertEqual(result["status"], "WATCH")
        self.assertAlmostEqual(result["pre_high_fade_pct"], -33.333333, places=5)

    def test_clean_strong_premarket_candidate_waits_for_open(self) -> None:
        row = base_candidate()
        row.update({"market_status": "Pre-Market", "pre_price": 2.20, "pre_high": 2.30})
        result = classify(row)
        self.assertEqual(result["status"], "WAIT_OPEN")

    def test_split_and_etf_are_excluded(self) -> None:
        split_row = conventional_candidate()
        split_row["split_today"] = True
        etf_row = conventional_candidate()
        etf_row["security_type"] = "Leveraged ETF"
        self.assertEqual(classify(split_row)["status"], "EXCLUDE")
        self.assertEqual(classify(etf_row)["status"], "EXCLUDE")

    def test_halt_blocks_execution(self) -> None:
        row = conventional_candidate()
        row["halted"] = True
        result = classify(row)
        self.assertEqual(result["status"], "WATCH")
        self.assertIn("HALTED", result["risk_flags"])

    def test_confirmed_premarket_supply_risk_excludes(self) -> None:
        row = conventional_candidate()
        row.update(
            {
                "premarket_supply_risk": True,
                "supply_risk_type": "ACTIVE_ATM",
                "supply_risk_source": "SEC 424B5",
            }
        )
        result = classify(row)
        self.assertEqual(result["status"], "EXCLUDE")
        self.assertIn("SUPPLY_RISK_CONFIRMED", result["risk_flags"])
        self.assertIn("PREMARKET_SUPPLY_RISK", result["risk_flags"])

    def test_legacy_dilution_risk_also_excludes(self) -> None:
        row = conventional_candidate()
        row.pop("premarket_supply_risk")
        row["dilution_overhang"] = "active ATM and warrants"
        result = classify(row)
        self.assertEqual(result["status"], "EXCLUDE")
        self.assertIn("DILUTION_OVERHANG", result["risk_flags"])
        self.assertIn("SUPPLY_RISK_LEGACY_FALLBACK", result["risk_flags"])

    def test_unknown_premarket_supply_review_waits_for_data(self) -> None:
        row = conventional_candidate()
        row["premarket_supply_risk"] = "UNKNOWN"
        row["dilution_overhang"] = False
        result = classify(row)
        self.assertEqual(result["status"], "WAIT_DATA")
        self.assertIn("SUPPLY_RISK_UNKNOWN", result["risk_flags"])

    def test_legacy_clean_dilution_field_remains_compatible(self) -> None:
        row = conventional_candidate()
        row.pop("premarket_supply_risk")
        result = classify(row)
        self.assertEqual(result["status"], "EXECUTE")
        self.assertIn("SUPPLY_RISK_LEGACY_FALLBACK", result["risk_flags"])

    def test_missing_fields_remain_unknown(self) -> None:
        result = classify({"symbol": "MISS"})
        self.assertEqual(result["status"], "WAIT_DATA")
        self.assertIsNone(result["pre_gap_pct"])
        self.assertIn("security_type", result["unknown"])
        self.assertIn("MISSING_DATA", result["risk_flags"])

    def test_statuses_stay_in_public_enum(self) -> None:
        rows = [
            conventional_candidate(),
            cphi_candidate(),
            after_hours_candidate(),
            base_candidate(),
            {"symbol": "MISS"},
        ]
        self.assertTrue(all(classify(row)["status"] in VALID_STATUSES for row in rows))

    def test_after_hours_earnings_route_is_watch_only(self) -> None:
        result = classify(after_hours_candidate())
        self.assertEqual(result["status"], "WATCH")
        self.assertEqual(result["path_type"], "AFTER_HOURS_EARNINGS")
        self.assertIn("AFTER_HOURS_SIGNAL", result["risk_flags"])
        self.assertAlmostEqual(result["after_gap_pct"], 50.00, places=2)
        self.assertNotEqual(result["status"], "EXECUTE")

    def test_after_hours_verified_low_supply_route_is_watch_only(self) -> None:
        row = after_hours_candidate()
        row["after_hours_catalyst_quality"] = "UNKNOWN"
        row["after_hours_supply_thesis"] = "VERIFIED_LOW_SUPPLY"
        result = classify(row)
        self.assertEqual(result["status"], "WATCH")
        self.assertEqual(result["path_type"], "AFTER_HOURS_LOW_SUPPLY")

    def test_after_hours_confirmed_supply_risk_excludes(self) -> None:
        row = after_hours_candidate()
        row.update(
            {
                "premarket_supply_risk": True,
                "supply_risk_type": "ACTIVE_ATM",
                "supply_risk_source": "SEC 424B5",
            }
        )
        result = classify(row)
        self.assertEqual(result["status"], "EXCLUDE")
        self.assertIn("SUPPLY_RISK_CONFIRMED", result["risk_flags"])

    def test_after_hours_missing_turnover_waits_for_data(self) -> None:
        row = after_hours_candidate()
        row.pop("after_volume")
        result = classify(row)
        self.assertEqual(result["status"], "WAIT_DATA")
        self.assertTrue(any(item.startswith("after_turnover") for item in result["unknown"]))

    def test_after_hours_unverified_route_stays_watch(self) -> None:
        row = after_hours_candidate()
        row["after_hours_catalyst_quality"] = "UNKNOWN"
        row["after_hours_supply_thesis"] = "UNKNOWN"
        result = classify(row)
        self.assertEqual(result["status"], "WATCH")
        self.assertEqual(result["path_type"], "NONE")
        self.assertIn("AFTER_HOURS_UNVERIFIED_ROUTE", result["risk_flags"])

    def test_markdown_exposes_path_and_risks(self) -> None:
        output = markdown(
            [classify(conventional_candidate()), classify(after_hours_candidate())]
        )
        self.assertIn("| Path |", output)
        self.assertIn("| Risks |", output)
        self.assertIn("CONVENTIONAL_GAP", output)
        self.assertIn("After-gap", output)
        self.assertIn("AFTER_HOURS_EARNINGS", output)


class InputAndCliTests(unittest.TestCase):
    def test_loads_csv_and_json(self) -> None:
        row = base_candidate()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            json_path = root / "candidates.json"
            csv_path = root / "candidates.csv"
            json_path.write_text(json.dumps({"candidates": [row]}), encoding="utf-8")
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=row.keys())
                writer.writeheader()
                writer.writerow(row)
            self.assertEqual(load_rows(json_path)[0]["symbol"], "TEST")
            self.assertEqual(load_rows(csv_path)[0]["symbol"], "TEST")

    def test_cli_json_smoke(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "candidates.json"
            input_path.write_text(json.dumps([conventional_candidate()]), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(input_path), "--format", "json"],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertEqual(payload[0]["status"], "EXECUTE")


class DocumentationTests(unittest.TestCase):
    def test_readmes_have_matching_public_cases_and_contact(self) -> None:
        for filename in ("README.md", "README_EN.md"):
            text = (SKILL_ROOT / filename).read_text(encoding="utf-8")
            for ticker in ("ELPW", "TDIC", "SKK", "CPOP", "RGNT", "CPHI"):
                self.assertIn(ticker, text)
            for ticker in ("FGI", "GXAI"):
                self.assertIn(ticker, text)
            self.assertIn("AFTER_HOURS_EARNINGS", text)
            self.assertIn("AFTER_HOURS_LOW_SUPPLY", text)
            self.assertIn("hrclaw@126.com", text)
        self.assertIn("README_EN.md", (SKILL_ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("README.md", (SKILL_ROOT / "README_EN.md").read_text(encoding="utf-8"))

    def test_fgi_marketing_copy_has_no_performance_guarantee(self) -> None:
        chinese = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
        english = (SKILL_ROOT / "README_EN.md").read_text(encoding="utf-8")
        self.assertIn("用户反馈", chinese)
        self.assertIn("未经独立审计", chinese)
        self.assertIn("不代表未来表现", chinese)
        self.assertIn("user-reported", english)
        self.assertIn("not independently audited", english)
        self.assertIn("not indicative of future performance", english)

    def test_openai_metadata_constraints(self) -> None:
        text = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        match = re.search(r'^\s*short_description:\s*"([^"]+)"\s*$', text, re.MULTILINE)
        self.assertIsNotNone(match)
        description = match.group(1)
        self.assertGreaterEqual(len(description), 25)
        self.assertLessEqual(len(description), 64)
        self.assertIn("$money-claw-us-stocks", text)

    def test_readmes_include_install_and_custom_purchase_calls_to_action(self) -> None:
        chinese = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
        english = (SKILL_ROOT / "README_EN.md").read_text(encoding="utf-8")
        self.assertIn("立即安装", chinese)
        self.assertIn("购买定制版量化 SKILL", chinese)
        self.assertIn("Install Now", english)
        self.assertIn("Purchase a Custom Quant SKILL", english)
        self.assertIn("hrclaw@126.com", chinese)
        self.assertIn("hrclaw@126.com", english)
        self.assertIn("hrclaw@126.com", "\n".join(chinese.splitlines()[:15]))
        self.assertIn("hrclaw@126.com", "\n".join(english.splitlines()[:15]))

    def test_readmes_include_jurisdiction_and_regulated_activity_boundaries(self) -> None:
        chinese = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
        english = (SKILL_ROOT / "README_EN.md").read_text(encoding="utf-8")
        self.assertIn("中国大陆、香港和澳门特别提示", chinese)
        self.assertIn("不提供个性化荐股", chinese)
        self.assertIn("本免责声明不能使原本受监管或违法的活动变为合法", chinese)
        self.assertIn("Mainland China, Hong Kong, and Macao", english)
        self.assertIn("Type 4 regulated activity", english)
        self.assertIn("does not make an otherwise regulated or unlawful activity lawful", english)


if __name__ == "__main__":
    unittest.main()
