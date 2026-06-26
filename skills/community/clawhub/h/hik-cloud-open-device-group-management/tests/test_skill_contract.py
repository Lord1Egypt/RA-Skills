from pathlib import Path
import unittest


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_declares_openclaw_skill_key(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn('"skillKey": "hik-cloud-device-group-management"', content)

    def test_skill_declares_openclaw_requires_env(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn('"env": ["HIK_OPEN_CLIENT_ID", "HIK_OPEN_CLIENT_SECRET"]', content)

    def test_skill_hides_explicit_token_workflow(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("不向用户暴露 token 调用流程", content)
        self.assertIn("不对外暴露 “获取 access_token” 操作", content)

    def test_skill_documents_shared_token_cache_file(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("~/.cache/hik_open/token.json", content)


if __name__ == "__main__":
    unittest.main()
