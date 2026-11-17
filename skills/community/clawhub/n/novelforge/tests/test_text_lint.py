import importlib.util
import tempfile
import unittest
from pathlib import Path


LINTER_PATH = Path(__file__).resolve().parents[1] / "scripts" / "novelforge_lint.py"
SPEC = importlib.util.spec_from_file_location("novel_lint", LINTER_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TextLintTests(unittest.TestCase):
    def test_style_signals_are_advisory_without_project_blocking_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_text("他想起了十分钟以前的约定。\n", encoding="utf-8")
            result = MODULE.run_lint(str(path))

            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["errors"], [])
            self.assertTrue(result["warnings"])

    def test_project_policy_can_promote_one_style_rule_to_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_text("他想起了十分钟以前的约定。\n", encoding="utf-8")
            result = MODULE.run_lint(str(path), config={"blocking_rules": ["mental"]})

            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any(item["rule"] == "mental" for item in result["errors"]))

    def test_cli_loads_policy_from_project_root_for_nested_chapters(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".novelforge" / "state").mkdir(parents=True)
            (root / ".novelforge" / "state" / "project.json").write_text(
                '{"schema": 1, "engine": "custom", "blocking_rules": ["mental"]}',
                encoding="utf-8",
            )
            chapter = root / "chapters" / "v01-c01.txt"
            chapter.parent.mkdir()
            chapter.write_text("他想起了旧约定。\n", encoding="utf-8")
            result = MODULE.run_lint(
                str(chapter),
                config=MODULE.load_project_config_for_path(chapter),
            )

            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any(item["rule"] == "mental" for item in result["errors"]))

    def test_project_style_detector_is_used_by_text_linter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_text("项目暗语", encoding="utf-8")
            result = MODULE.run_lint(
                str(path),
                config={
                    "style_detectors": [{"id": "project-code", "pattern": "项目暗语"}],
                    "policies": {"blocking_rules": ["project-code"]},
                },
            )

            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any(item["rule"] == "project-code" for item in result["errors"]))

    def test_style_detector_blocking_mode_applies_to_text_linter(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_text("他想起了旧约定。\n", encoding="utf-8")
            result = MODULE.run_lint(str(path), config={"policies": {"style_detector_mode": "blocking"}})

            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(result["errors"])

    def test_ai_trope_detected_as_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_text("马蹄踏碎了官道上的月光，夜风猎猎作响。\n忽然传出一声轻笑。\n", encoding="utf-8")
            result = MODULE.run_lint(str(path))

            self.assertEqual(result["status"], "PASS")
            tropes = [w for w in result["warnings"] if w["rule"] == "ai-trope"]
            self.assertTrue(len(tropes) >= 2)

    def test_repetitive_action_in_single_paragraph_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_text("张三点了点头。李四也点了点头。王五跟着点了点头。\n", encoding="utf-8")
            result = MODULE.run_lint(str(path))

            self.assertEqual(result["status"], "PASS")
            rep = [w for w in result["warnings"] if w["rule"] == "repetitive-action"]
            self.assertTrue(len(rep) >= 1)
            self.assertIn("点", rep[0]["problem"])

    def test_stock_rhetorical_question_ending_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_text("他回到了屋里歇下。\n\n“杨家？”\n", encoding="utf-8")
            result = MODULE.run_lint(str(path))

            self.assertEqual(result["status"], "PASS")
            endings = [w for w in result["warnings"] if w["rule"] == "ai-trope" and "ending" in w["problem"]]
            self.assertTrue(len(endings) == 1)

    def test_flat_cadence_detected_for_monotonous_sentences(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            # 25 sentences with almost identical length (20 characters each)
            sentences = ["这是一句长度非常均匀的句子呢。" * 1 for _ in range(25)]
            path.write_text("".join(sentences), encoding="utf-8")
            result = MODULE.run_lint(str(path))

            cadence = [w for w in result["warnings"] if w["rule"] == "flat-cadence"]
            self.assertTrue(len(cadence) == 1)

    def test_pompous_naming_detected_for_grandiosity(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_text("盛世集团收购了帝豪酒店，天机阁派出使者接洽。\n", encoding="utf-8")
            result = MODULE.run_lint(str(path))

            self.assertEqual(result["status"], "PASS")
            pomp = [w for w in result["warnings"] if w["rule"] == "pompous-naming"]
            self.assertTrue(len(pomp) >= 1)
            self.assertIn("pompous", pomp[0]["problem"])

    def test_multi_genre_ai_trope_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_text("众人倒吸一口凉气，他嘴角勾起一抹玩味的弧度，深邃眼眸闪过寒芒。全场陷入死一般的寂静。\n", encoding="utf-8")
            result = MODULE.run_lint(str(path))

            self.assertEqual(result["status"], "PASS")
            tropes = [w for w in result["warnings"] if w["rule"] == "ai-trope"]
            self.assertTrue(len(tropes) >= 1)


if __name__ == "__main__":
    unittest.main()

