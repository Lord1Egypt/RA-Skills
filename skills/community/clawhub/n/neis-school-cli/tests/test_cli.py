import importlib.util
import io
import json
import pathlib
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch


ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "neis_cli.py"
FIXTURES = pathlib.Path(__file__).resolve().parent / "fixtures"

spec = importlib.util.spec_from_file_location("neis_cli", SCRIPT_PATH)
neis_cli = importlib.util.module_from_spec(spec)
assert spec.loader is not None
sys.modules[spec.name] = neis_cli
spec.loader.exec_module(neis_cli)


def fixture(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class StubClient:
    def __init__(self, payload):
        self.payload = payload

    def fetch(self, endpoint, params):
        return self.payload


class NeisCliTests(unittest.TestCase):
    def test_endpoint_for_school_level_returns_expected_dataset(self):
        self.assertEqual(neis_cli.endpoint_for_school_level("elementary"), "elsTimetable")
        self.assertEqual(neis_cli.endpoint_for_school_level("middle"), "misTimetable")
        self.assertEqual(neis_cli.endpoint_for_school_level("high"), "hisTimetable")

    def test_normalize_date_accepts_dashed_and_compact_formats(self):
        self.assertEqual(neis_cli.normalize_date("2026-03-16").isoformat(), "2026-03-16")
        self.assertEqual(neis_cli.normalize_date("20260316").isoformat(), "2026-03-16")

    def test_normalize_date_rejects_invalid_format(self):
        with self.assertRaises(neis_cli.CliError):
            neis_cli.normalize_date("2026/03/16")

    def test_meal_from_row_splits_html_fields(self):
        row = fixture("meal_success.json")["mealServiceDietInfo"][1]["row"][0]
        meal = neis_cli.meal_from_row(row)
        self.assertEqual(meal["date"], "2026-03-16")
        self.assertEqual(meal["meal_name"], "중식")
        self.assertEqual(meal["dishes"][0], "혼합잡곡밥 (5)")
        self.assertEqual(meal["origin_info"][1], "닭고기 : 국내산")

    def test_extract_rows_returns_empty_list_on_no_data(self):
        self.assertEqual(neis_cli.extract_rows(fixture("no_data.json"), "mealServiceDietInfo"), [])

    def test_resolve_school_raises_when_multiple_candidates_exist(self):
        client = StubClient(fixture("school_search_ambiguous.json"))
        with self.assertRaises(neis_cli.CliError) as ctx:
            neis_cli.resolve_school(client, "가락")
        self.assertIn("학교명이 여러 개 검색되었습니다", str(ctx.exception))

    def test_get_timetable_sorts_periods(self):
        client = StubClient(fixture("timetable_success.json"))
        school = neis_cli.school_from_row(fixture("school_search_single.json")["schoolInfo"][1]["row"][0])
        rows = neis_cli.get_timetable(client, school, neis_cli.normalize_date("2026-03-16"), "1", "1")
        self.assertEqual([row["period"] for row in rows], ["1", "2", "3"])

    def test_main_prints_help(self):
        result = subprocess.run(
            ["python3", str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("학교 검색, 급식, 시간표를 NEIS OpenAPI로 조회합니다.", result.stdout)

    def test_school_search_json_output(self):
        payload = fixture("school_search_single.json")
        with patch.object(neis_cli, "NeisClient", return_value=StubClient(payload)):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                exit_code = neis_cli.main(["school", "search", "세종과학예술영재학교", "--json"])
        self.assertEqual(exit_code, 0)
        data = json.loads(buffer.getvalue())
        self.assertTrue(data["ok"])
        self.assertEqual(data["command"], "school.search")
        self.assertEqual(data["endpoint"], "schoolInfo")
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["data"]["schools"][0]["school_level"], "high")
        self.assertEqual(data["data"]["schools"][0]["school_code"], "9300181")


if __name__ == "__main__":
    unittest.main()
