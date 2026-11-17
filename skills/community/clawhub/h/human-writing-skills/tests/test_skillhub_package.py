import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_skillhub_package.py"
SPEC = importlib.util.spec_from_file_location("build_skillhub_package", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SkillHubPackageTests(unittest.TestCase):
    def test_builds_executable_package_with_skillhub_metadata(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "skill"
            MODULE.build_package(ROOT, output, "9.8.7")

            skill = output.joinpath("SKILL.md").read_text(encoding="utf-8")
            self.assertIn("slug: human-writing-skills", skill)
            self.assertIn("version: 9.8.7", skill)
            self.assertIn("displayName: 增强版去 AI 写作 Skill｜高级 AI 写作工具", skill)
            self.assertIn("去AI味", skill)
            self.assertIn("AI文本润色", skill)
            self.assertIn("ai-humanizer", skill)
            self.assertIn("AI式结尾审查", skill)
            self.assertIn("生硬结尾审查", skill)
            self.assertIn("# 增强版去 AI 写作 Skill", skill)
            self.assertIn("## 适用场景", skill)
            self.assertIn("去AI味、去AI写作、消除AI腔", skill)
            self.assertNotIn("# Advanced Human Writing & AI Humanizer", skill)
            self.assertTrue(output.joinpath("humanwriting", "cli.py").is_file())
            self.assertTrue(output.joinpath("humanwriting", "linter.py").is_file())
            self.assertTrue(output.joinpath("skills", "fiction.md").is_file())
            self.assertTrue(output.joinpath("skills", "earned-ending-audit.md").is_file())
            self.assertTrue(output.joinpath("skills", "repetition-exposition-audit.md").is_file())
            self.assertTrue(output.joinpath("humanwriting", "longform.py").is_file())
            self.assertTrue(output.joinpath("tests", "test_linter.py").is_file())
            self.assertFalse(output.joinpath(".github").exists())
            self.assertFalse(output.joinpath(".gitignore").exists())
            self.assertFalse(output.joinpath(".gitattributes").exists())
            self.assertEqual(output.joinpath("LICENSE.md").read_bytes(), ROOT.joinpath("LICENSE").read_bytes())
            self.assertFalse(output.joinpath("LICENSE").exists())
            self.assertIn("](LICENSE.md)", output.joinpath("README.md").read_text(encoding="utf-8"))
            self.assertTrue(all(path.suffix for path in output.rglob("*") if path.is_file()))
            self.assertFalse(output.joinpath("package.json").exists())
            self.assertFalse(output.joinpath("MANIFEST.in").exists())
            self.assertFalse(output.joinpath("assets", "icon.webp").exists())
            self.assertFalse(output.joinpath("assets").exists())
            self.assertIn('src="https://raw.githubusercontent.com/whh110112/human-writing-skills/main/assets/logo.png"',
                          output.joinpath("README.md").read_text(encoding="utf-8"))
            self.assertFalse(output.joinpath("pnpm-lock.yaml").exists())
            self.assertFalse(output.joinpath("marketplaces").exists())
            self.assertFalse(output.joinpath("plugins").exists())
            self.assertFalse(output.joinpath(".cursor").exists())

    def test_refuses_to_mix_with_nonempty_output(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / "skill"
            output.mkdir()
            output.joinpath("existing.txt").write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "not empty"):
                MODULE.build_package(ROOT, output)


if __name__ == "__main__":
    unittest.main()
