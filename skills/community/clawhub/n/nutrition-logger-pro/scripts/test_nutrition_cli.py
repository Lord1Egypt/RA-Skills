import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("nutrition_cli.py")


class NutritionCliTests(unittest.TestCase):
    def run_cli(self, command, payload=None, log_dir=None, expect_success=True):
        args = [sys.executable, str(SCRIPT)]
        if log_dir is not None:
            args.extend(["--log-dir", str(log_dir)])
        args.append(command)
        proc = subprocess.run(
            args,
            input=json.dumps(payload or {}, ensure_ascii=False),
            text=True,
            capture_output=True,
            encoding="utf-8",
        )
        if expect_success:
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        else:
            self.assertNotEqual(proc.returncode, 0, proc.stderr + proc.stdout)
        try:
            return json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            self.fail(f"CLI did not return JSON: {exc}\nstdout={proc.stdout}\nstderr={proc.stderr}")

    def test_calculates_per_100g_label_values(self):
        result = self.run_cli(
            "calculate-label",
            {
                "food": "土豆泥",
                "eaten_amount_g": 150,
                "label_per": "100g",
                "nutrition_per_unit": {
                    "kcal": 110,
                    "protein_g": 2,
                    "carbs_g": 15,
                    "fat_g": 4,
                },
            },
        )

        self.assertEqual(result["food"], "土豆泥")
        self.assertEqual(result["source"], "label_calculated")
        self.assertEqual(result["confidence"], "high")
        self.assertEqual(result["nutrition"]["kcal"], 165)
        self.assertEqual(result["nutrition"]["protein_g"], 3)
        self.assertEqual(result["nutrition"]["carbs_g"], 22.5)
        self.assertEqual(result["nutrition"]["fat_g"], 6)
        self.assertIn("每100g", result["note"])

    def test_calculates_per_serving_label_values(self):
        result = self.run_cli(
            "calculate-label",
            {
                "food": "酸奶",
                "servings_eaten": 2,
                "label_per": "serving",
                "nutrition_per_unit": {
                    "kcal": 95,
                    "protein_g": 4,
                    "carbs_g": 12,
                    "fat_g": 3,
                },
            },
        )

        self.assertEqual(result["nutrition"]["kcal"], 190)
        self.assertEqual(result["nutrition"]["protein_g"], 8)
        self.assertEqual(result["source"], "label_calculated")
        self.assertIn("每份", result["note"])

    def test_rejects_negative_nutrition_values_with_chinese_error(self):
        result = self.run_cli(
            "calculate-label",
            {
                "food": "异常食物",
                "eaten_amount_g": 100,
                "label_per": "100g",
                "nutrition_per_unit": {"kcal": -1},
            },
            expect_success=False,
        )

        self.assertFalse(result["ok"])
        self.assertIn("不能为负数", result["error"])

    def test_append_entry_writes_jsonl_and_csv_for_mixed_meal(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp)
            payload = sample_mixed_breakfast()
            result = self.run_cli("append-entry", payload, log_dir=log_dir)

            self.assertTrue(result["ok"])
            entry = result["entry"]
            self.assertTrue(entry["entry_id"].startswith("nl_2026-05-20_"))
            self.assertEqual(entry["totals"]["kcal"], 470)
            self.assertEqual(entry["totals"]["protein_g"], 26)
            self.assertEqual(entry["items"][2]["source"], "user_provided")

            jsonl_path = log_dir / "food_log.jsonl"
            csv_path = log_dir / "food_log.csv"
            self.assertTrue(jsonl_path.exists())
            self.assertTrue(csv_path.exists())
            self.assertEqual(len(jsonl_path.read_text(encoding="utf-8").splitlines()), 1)
            csv_text = csv_path.read_text(encoding="utf-8-sig")
            self.assertIn("entry_id", csv_text)
            self.assertIn("面包", csv_text)
            self.assertIn("user_provided", csv_text)

    def test_day_summary_includes_source_breakdown_and_missing_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp)
            self.run_cli("append-entry", sample_mixed_breakfast(), log_dir=log_dir)
            self.run_cli("append-entry", sample_estimated_lunch(), log_dir=log_dir)

            result = self.run_cli(
                "summary-day",
                {"date": "2026-05-20", "timezone": "Europe/Brussels"},
                log_dir=log_dir,
            )

            self.assertTrue(result["ok"])
            self.assertEqual(result["date"], "2026-05-20")
            self.assertEqual(result["entry_count"], 2)
            self.assertEqual(result["totals"]["kcal"], 995)
            self.assertEqual(result["totals"]["protein_g"], 77)
            self.assertEqual(result["source_breakdown"]["user_provided"]["kcal"], 180)
            self.assertEqual(result["source_breakdown"]["estimated"]["kcal"], 815)
            self.assertGreater(result["missing_values_count"], 0)

    def test_week_summary_returns_daily_totals_averages_and_missing_days(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp)
            self.run_cli("append-entry", sample_mixed_breakfast(), log_dir=log_dir)
            dinner = sample_label_dinner()
            dinner["date"] = "2026-05-21"
            dinner["time"] = "19:15"
            self.run_cli("append-entry", dinner, log_dir=log_dir)

            result = self.run_cli(
                "summary-week",
                {"week_start": "2026-05-18", "timezone": "Europe/Brussels"},
                log_dir=log_dir,
            )

            self.assertTrue(result["ok"])
            self.assertEqual(result["week_start"], "2026-05-18")
            self.assertEqual(result["daily_totals"]["2026-05-20"]["kcal"], 470)
            self.assertEqual(result["daily_totals"]["2026-05-21"]["kcal"], 165)
            self.assertEqual(result["average_kcal"], 90.7)
            self.assertIn("2026-05-18", result["missing_days"])
            self.assertEqual(result["source_breakdown"]["label_calculated"]["kcal"], 165)

    def test_undo_last_soft_deletes_latest_entry_and_rebuilds_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp)
            self.run_cli("append-entry", sample_mixed_breakfast(), log_dir=log_dir)
            self.run_cli("append-entry", sample_estimated_lunch(), log_dir=log_dir)

            result = self.run_cli("undo-last", {}, log_dir=log_dir)
            self.assertTrue(result["ok"])
            self.assertEqual(result["undone_entry"]["meal"], "lunch")
            self.assertIn("已撤销", result["message"])

            summary = self.run_cli(
                "summary-day",
                {"date": "2026-05-20", "timezone": "Europe/Brussels"},
                log_dir=log_dir,
            )
            self.assertEqual(summary["entry_count"], 1)
            self.assertEqual(summary["totals"]["kcal"], 470)
            jsonl_lines = (log_dir / "food_log.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(jsonl_lines), 3)
            self.assertEqual(json.loads(jsonl_lines[-1])["event_type"], "deletion")

    def test_update_recent_matching_item_recalculates_totals(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp)
            self.run_cli("append-entry", sample_mixed_breakfast(), log_dir=log_dir)

            result = self.run_cli(
                "update-entry",
                {
                    "match": {"food": "面包"},
                    "patch": {
                        "food": "面包",
                        "nutrition": {"kcal": 220, "protein_g": 7},
                        "source": "user_provided",
                        "confidence": "high",
                        "note": "根据用户更正：不是180 kcal，是220 kcal，蛋白质7g。",
                    },
                },
                log_dir=log_dir,
            )

            self.assertTrue(result["ok"])
            self.assertEqual(result["entry"]["totals"]["kcal"], 510)
            self.assertEqual(result["entry"]["totals"]["protein_g"], 27)
            bread = result["entry"]["items"][2]
            self.assertEqual(bread["nutrition"]["kcal"], 220)
            self.assertEqual(bread["nutrition"]["protein_g"], 7)
            self.assertEqual(bread["source"], "user_provided")
            self.assertIn("已修正", result["message"])

    def test_update_entry_returns_candidates_when_match_is_ambiguous(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp)
            first = sample_mixed_breakfast()
            second = sample_mixed_breakfast()
            second["time"] = "10:30"
            second["meal"] = "snack"
            self.run_cli("append-entry", first, log_dir=log_dir)
            self.run_cli("append-entry", second, log_dir=log_dir)

            result = self.run_cli(
                "update-entry",
                {
                    "match": {"food": "面包"},
                    "patch": {"nutrition": {"kcal": 220}, "source": "user_provided"},
                },
                log_dir=log_dir,
                expect_success=False,
            )

            self.assertFalse(result["ok"])
            self.assertIn("无法唯一确定", result["error"])
            self.assertEqual(len(result["candidates"]), 2)

    def test_unknown_amount_fallback_keeps_nulls_and_low_confidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp)
            result = self.run_cli("append-entry", sample_unknown_amount_snack(), log_dir=log_dir)

            item = result["entry"]["items"][0]
            self.assertIsNone(item["amount_g"])
            self.assertEqual(item["confidence"], "low")
            self.assertIsNone(item["nutrition"]["kcal"])
            self.assertIn("份量不明确", item["note"])


def sample_mixed_breakfast():
    return {
        "date": "2026-05-20",
        "time": "08:05",
        "timezone": "Europe/Brussels",
        "meal": "breakfast",
        "raw_message": "记录：早餐两个鸡蛋，一杯250ml牛奶，一片面包，面包包装写180 kcal，蛋白质6g",
        "items": [
            {
                "food": "鸡蛋",
                "amount_raw": "两个",
                "amount_g": 100,
                "nutrition": {"kcal": 140, "protein_g": 12, "carbs_g": 1, "fat_g": 10},
                "source": "estimated",
                "confidence": "medium",
                "note": "估算：一个鸡蛋约50g。",
            },
            {
                "food": "牛奶",
                "amount_raw": "一杯250ml",
                "amount_g": 250,
                "nutrition": {"kcal": 150, "protein_g": 8, "carbs_g": 12, "fat_g": 8},
                "source": "estimated",
                "confidence": "medium",
                "note": "估算：按250ml普通牛奶。",
            },
            {
                "food": "面包",
                "amount_raw": "一片",
                "amount_g": None,
                "nutrition": {"kcal": 180, "protein_g": 6, "carbs_g": None, "fat_g": None},
                "source": "user_provided",
                "confidence": "high",
                "note": "使用用户提供的包装数据。",
            },
        ],
    }


def sample_estimated_lunch():
    return {
        "date": "2026-05-20",
        "time": "12:30",
        "timezone": "Europe/Brussels",
        "meal": "lunch",
        "raw_message": "午餐：鸡胸肉150g，米饭一碗，西兰花一份",
        "items": [
            {
                "food": "鸡胸肉",
                "amount_raw": "150g",
                "amount_g": 150,
                "nutrition": {"kcal": 248, "protein_g": 46, "carbs_g": 0, "fat_g": 5},
                "source": "estimated",
                "confidence": "medium",
                "note": "估算：熟鸡胸肉150g。",
            },
            {
                "food": "米饭",
                "amount_raw": "一碗",
                "amount_g": 180,
                "nutrition": {"kcal": 234, "protein_g": 4, "carbs_g": 52, "fat_g": 1},
                "source": "estimated",
                "confidence": "low",
                "note": "估算：一碗熟米饭约180g。",
            },
            {
                "food": "西兰花",
                "amount_raw": "一份",
                "amount_g": 120,
                "nutrition": {
                    "kcal": 43,
                    "protein_g": 1,
                    "carbs_g": 8,
                    "fat_g": 0,
                    "fiber_g": None,
                    "sugar_g": None,
                    "sodium_mg": None,
                },
                "source": "estimated",
                "confidence": "low",
                "note": "估算：一份西兰花约120g。",
            },
        ],
    }


def sample_label_dinner():
    return {
        "date": "2026-05-20",
        "time": "19:15",
        "timezone": "Europe/Brussels",
        "meal": "dinner",
        "raw_message": "晚餐：土豆泥150g，营养表每100g是110 kcal，蛋白质2g，碳水15g，脂肪4g",
        "items": [
            {
                "food": "土豆泥",
                "amount_raw": "150g",
                "amount_g": 150,
                "nutrition": {"kcal": 165, "protein_g": 3, "carbs_g": 22.5, "fat_g": 6},
                "source": "label_calculated",
                "confidence": "high",
                "note": "根据用户提供的每100g标签计算。",
            }
        ],
    }


def sample_unknown_amount_snack():
    return {
        "date": "2026-05-20",
        "time": "16:00",
        "timezone": "Europe/Brussels",
        "meal": "snack",
        "raw_message": "我吃了一点薯片",
        "items": [
            {
                "food": "薯片",
                "amount_raw": "一点",
                "amount_g": None,
                "nutrition": {"kcal": None, "protein_g": None, "carbs_g": None, "fat_g": None},
                "source": "estimated",
                "confidence": "low",
                "note": "份量不明确，暂不估算精确营养值。",
            }
        ],
    }


if __name__ == "__main__":
    unittest.main()
