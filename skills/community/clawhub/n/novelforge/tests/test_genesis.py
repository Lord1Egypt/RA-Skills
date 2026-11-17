"""Unit tests for story genesis, scale benchmarks, and capacity assessment."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.genesis import (
    calculate_scale_spec,
    evaluate_story_capacity,
    init_project_with_genesis,
    normalize_genre,
    SCALE_TIERS,
)
from novelforge_engine.project import verify_project


class TestStoryGenesis(unittest.TestCase):
    def test_genre_normalization(self):
        # Single canonical
        self.assertEqual(normalize_genre("修仙"), "修仙")
        # Aliases
        self.assertEqual(normalize_genre("玄幻"), "修仙")
        self.assertEqual(normalize_genre("都市修真"), "都市异能")
        self.assertEqual(normalize_genre("电竞文"), "电竞")
        self.assertEqual(normalize_genre("克系悬疑"), "克苏鲁")
        # Composite genre
        self.assertEqual(normalize_genre("都市脑洞+规则怪谈"), "都市脑洞+规则怪谈")
        self.assertEqual(normalize_genre("玄幻 / 系统流"), "修仙+系统流")
        # Max 2 composite parts
        self.assertEqual(normalize_genre("修仙 + 系统流 + 穿书"), "修仙+系统流")
        # Empty fallback
        self.assertEqual(normalize_genre(""), "通用故事")

    def test_scale_spec_calculation(self):
        # Short tier
        short = calculate_scale_spec("short", target_words=20000)
        self.assertEqual(short["tier"], "short")
        self.assertEqual(short["target_words"], 20000)
        self.assertEqual(short["estimated_chapters"], 8)
        self.assertEqual(short["planned_volumes"], 1)

        # Standard tier default
        std = calculate_scale_spec("standard")
        self.assertEqual(std["tier"], "standard")
        self.assertEqual(std["target_words"], 800000)
        self.assertEqual(std["planned_volumes"], 5)
        self.assertGreater(std["estimated_chapters"], 200)

        # Epic tier
        epic = calculate_scale_spec("epic", target_words=2400000)
        self.assertEqual(epic["tier"], "epic")
        self.assertEqual(epic["target_words"], 2400000)
        self.assertEqual(epic["planned_volumes"], 10)

    def test_capacity_assessment_healthy(self):
        res = evaluate_story_capacity(
            scale_tier="standard",
            target_words=800000,
            progression_ranks=6,
            factions_count=4,
            motivations_count=3,
            genre="修仙+系统流",
        )
        self.assertEqual(res["status"], "HEALTHY")
        self.assertIn("良好匹配", res["diagnostics"][0])
        self.assertEqual(res["genre"], "修仙+系统流")

    def test_capacity_assessment_underpowered_risk(self):
        # 1M words with single motivation, 1 rank, 1 faction -> RISK_UNDERPOWERED
        res = evaluate_story_capacity(
            scale_tier="standard",
            target_words=1000000,
            progression_ranks=1,
            factions_count=1,
            motivations_count=1,
        )
        self.assertEqual(res["status"], "RISK_UNDERPOWERED")
        self.assertTrue(any("小马拉大车" in d for d in res["diagnostics"]))
        self.assertTrue(any("剧情注水" in d for d in res["diagnostics"]))

    def test_capacity_assessment_overcomplex_risk(self):
        # 30k words with 10 ranks and 8 factions -> RISK_OVERCOMPLEX
        res = evaluate_story_capacity(
            scale_tier="short",
            target_words=30000,
            progression_ranks=10,
            factions_count=8,
            motivations_count=2,
        )
        self.assertEqual(res["status"], "RISK_OVERCOMPLEX")
        self.assertTrue(any("大马拉小车" in d for d in res["diagnostics"]))
        self.assertTrue(any("信息过载" in d for d in res["diagnostics"]))

    def test_init_project_with_genesis_and_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            profile = init_project_with_genesis(
                p,
                genre="玄幻 + 系统流",
                scale_tier="standard",
                target_words=900000,
            )
            self.assertEqual(profile["genre"], "修仙+系统流")
            self.assertEqual(profile["scale"]["tier"], "standard")
            self.assertEqual(profile["scale"]["target_words"], 900000)
            self.assertEqual(profile["scale"]["planned_volumes"], 5)

            # verify_project should pass
            verify_res = verify_project(p)
            self.assertEqual(verify_res["status"], "PASS")

    def test_verify_project_scale_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            init_project_with_genesis(p)
            proj_file = p / ".novelforge" / "state" / "project.json"
            data = json.loads(proj_file.read_text(encoding="utf-8"))
            data["scale"]["tier"] = "galaxy-tier"  # invalid
            proj_file.write_text(json.dumps(data), encoding="utf-8")

            res = verify_project(p)
            self.assertEqual(res["status"], "FAIL")
            self.assertTrue(any("scale.tier must be short" in e["problem"] for e in res["errors"]))

    def test_cli_assess_capacity_and_init(self):
        cli = SKILL_ROOT / "scripts" / "novelforgectl.py"

        # 1. assess-capacity CLI
        proc = subprocess.run(
            [
                sys.executable,
                str(cli),
                "project",
                "assess-capacity",
                "--scale", "standard",
                "--words", "800000",
                "--ranks", "6",
                "--factions", "3",
                "--motivations", "3",
                "--genre", "都市脑洞+规则怪谈",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        data = json.loads(proc.stdout)
        self.assertEqual(data["status"], "HEALTHY")
        self.assertEqual(data["genre"], "都市脑洞+规则怪谈")

        # 2. init with scale CLI
        with tempfile.TemporaryDirectory() as tmp:
            proc_init = subprocess.run(
                [
                    sys.executable,
                    str(cli),
                    "project",
                    "init",
                    tmp,
                    "--genre", "修仙+系统流",
                    "--scale", "epic",
                    "--words", "2500000",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            data_init = json.loads(proc_init.stdout)
            self.assertEqual(data_init["status"], "PASS")
            self.assertEqual(data_init["project"]["scale"]["tier"], "epic")
            self.assertEqual(data_init["project"]["scale"]["target_words"], 2500000)


if __name__ == "__main__":
    unittest.main()

