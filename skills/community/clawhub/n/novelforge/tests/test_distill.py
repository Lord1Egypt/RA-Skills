from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
import sys

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from scripts.novelforgectl import main
from novelforge_engine.distill import distill_engine, prepare_distill, build_distill_from_spec
from novelforge_engine.engine import load_engine


class DistillTests(unittest.TestCase):
    def test_distill_from_text_samples(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sources_dir = tmp_path / "sources"
            sources_dir.mkdir()

            (sources_dir / "chapter_01.txt").write_text(
                "黑夜中，巨大的环形粒子对撞机在戈壁深处低鸣。丁仪掐灭了烟头，目光凝视着虚无。",
                encoding="utf-8",
            )
            (sources_dir / "craft_essay.md").write_text(
                "# 论宏细节与硬核逻辑\n硬科幻的核心不在于堆砌公式，而在于将技术推演转化为人类文明在绝境中的道德抉择。",
                encoding="utf-8",
            )

            out_dir = tmp_path / "engines"
            res = distill_engine(
                source_path_input=sources_dir,
                engine_id="hard-scifi",
                label="Hard Sci-Fi Perspective",
                output_dir=out_dir,
            )

            self.assertEqual(res["status"], "PASS")
            self.assertEqual(res["engine"], "hard-scifi")

            engine_root = out_dir / "hard-scifi"
            self.assertTrue((engine_root / "engine.json").is_file())
            self.assertTrue((engine_root / "applicability.md").is_file())
            self.assertTrue((engine_root / "limits.md").is_file())
            self.assertTrue((engine_root / "cards" / "models.json").is_file())
            self.assertTrue((engine_root / "cards" / "techniques.json").is_file())
            self.assertTrue((engine_root / "manifest.json").is_file())

            # Verify that load_engine validates the output cleanly
            loaded = load_engine(engine_root)
            self.assertEqual(loaded["id"], "hard-scifi")
            self.assertGreaterEqual(len(loaded["cards"]), 4)

    def test_distill_from_custom_spec(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            spec_file = tmp_path / "spec.json"
            spec = {
                "id": "noir-detective",
                "label": "Noir Detective Engine",
                "version": 1,
                "models": [
                    {
                        "id": "ND-M1",
                        "name": "cynical truth",
                        "when": {"phase": ["outline", "scene"]},
                        "requires": ["character"],
                        "hardness": "required",
                        "prompt": "每个角色都在隐瞒部分真相，侦探必须通过利益链条反向还原事实。",
                    }
                ],
                "techniques": [
                    {
                        "id": "ND-T1",
                        "name": "shadow interrogation",
                        "when": {"phase": ["scene", "draft"], "scene_types": ["dialogue", "conflict"]},
                        "requires": ["character"],
                        "hardness": "recommended",
                        "prompt": "在对话中借光影与烟雾的停顿隐匿表情，以避而不答制造嫌疑感。",
                    }
                ],
            }
            spec_file.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")

            out_dir = tmp_path / "engines"
            res = distill_engine(
                source_path_input=spec_file,
                engine_id="noir-detective",
                output_dir=out_dir,
            )
            self.assertEqual(res["status"], "PASS")

            engine_root = out_dir / "noir-detective"
            loaded = load_engine(engine_root)
            self.assertEqual(loaded["id"], "noir-detective")
            self.assertEqual(len(loaded["cards"]), 2)
            self.assertEqual(loaded["cards"][0]["id"], "ND-M1")
            self.assertEqual(loaded["cards"][1]["id"], "ND-T1")

    def test_cli_distill_and_project_installation(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sources_dir = tmp_path / "sources"
            sources_dir.mkdir()
            (sources_dir / "article.txt").write_text("武侠的精髓在因果与情义。", encoding="utf-8")

            engines_out = tmp_path / "distilled_engines"
            project_dir = tmp_path / "my_project"

            # 1. Distill engine via CLI
            code = main([
                "engine", "distill", str(sources_dir),
                "--id", "wuxia-craft",
                "--label", "Wuxia Craft Engine",
                "--output", str(engines_out),
            ])
            self.assertEqual(code, 0)
            distilled_path = engines_out / "wuxia-craft"
            self.assertTrue(distilled_path.is_dir())

            # 2. Init project
            self.assertEqual(main(["project", "init", str(project_dir)]), 0)

            # 3. Install distilled engine into project
            self.assertEqual(main(["engine", "install", str(project_dir), str(distilled_path)]), 0)
            self.assertTrue((project_dir / ".novelforge" / "engines" / "wuxia-craft" / "engine.json").is_file())

            # 4. Activate distilled engine
            self.assertEqual(main(["engine", "use", str(project_dir), "wuxia-craft"]), 0)
            proj_state = json.loads((project_dir / ".novelforge" / "state" / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(proj_state["engine"], "wuxia-craft")

    def test_two_phase_prepare_and_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sources_dir = tmp_path / "sources"
            sources_dir.mkdir()
            (sources_dir / "sample.txt").write_text("夜雨连绵，剑气如霜。", encoding="utf-8")

            # 1. Prepare phase
            staging_out = tmp_path / "staging"
            prep = prepare_distill(sources_dir, engine_id="sword-rain", label="Sword Rain Engine", output_dir=staging_out)
            self.assertEqual(prep["status"], "PREPARED")
            self.assertEqual(prep["engine_id"], "sword-rain")
            self.assertIn("io_contract", prep)
            self.assertEqual(prep["io_contract"]["output"]["format"], "json")
            self.assertTrue(Path(prep["staging_spec"]).is_file())

            # 2. Modify staging spec (as model would do based on text)
            spec_path = Path(prep["staging_spec"])
            spec_data = json.loads(spec_path.read_text(encoding="utf-8"))
            spec_data["applicability"] = "# 烟雨剑意 适用条件\n\n以凄冷氛围见长的剑戟叙事。"
            spec_path.write_text(json.dumps(spec_data, ensure_ascii=False), encoding="utf-8")

            # 3. Build phase
            out_engines = tmp_path / "engines"
            build_res = build_distill_from_spec(spec_path, output_dir=out_engines)
            self.assertEqual(build_res["status"], "PASS")
            self.assertEqual(build_res["engine"], "sword-rain")

            loaded = load_engine(out_engines / "sword-rain")
            self.assertEqual(loaded["id"], "sword-rain")
            applicability_text = (out_engines / "sword-rain" / "applicability.md").read_text(encoding="utf-8")
            self.assertIn("以凄冷氛围见长", applicability_text)

    def test_cli_distill_prepare_and_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            sources_dir = tmp_path / "sources"
            sources_dir.mkdir()
            (sources_dir / "ch1.txt").write_text("江湖夜雨十年灯。", encoding="utf-8")

            engines_out = tmp_path / "distilled"

            # 1. novelforgectl engine distill prepare
            code = main([
                "engine", "distill", "prepare", str(sources_dir),
                "--id", "rain-lantern",
                "--label", "Rain Lantern",
                "--output", str(engines_out),
            ])
            self.assertEqual(code, 0)
            staging_spec = engines_out / ".staging" / "rain-lantern" / "distill-spec.json"
            self.assertTrue(staging_spec.is_file())

            # 2. novelforgectl engine distill build
            code = main([
                "engine", "distill", "build", str(staging_spec),
                "--output", str(engines_out),
            ])
            self.assertEqual(code, 0)
            self.assertTrue((engines_out / "rain-lantern" / "engine.json").is_file())


if __name__ == "__main__":
    unittest.main()


