from pathlib import Path
import unittest


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_declares_openclaw_skill_key(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn('"skillKey": "hik-cloud-device-alarm-capability-management"', content)

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

    def test_skill_references_are_self_contained(self):
        content = (
            Path(__file__).resolve().parents[1]
            / "references"
            / "device-alarm-capability-management.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("docs/hik-cloud-open", content)
        self.assertIn("顶层 `code`、`message`、`data`", content)
        self.assertIn("`message` 为可选提示字段", content)

    def test_skill_documents_return_focus(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("`list` 重点看顶层 `code` / `message`", content)
        self.assertIn("`update-status` 重点看 `channelId + abilityCode + status`", content)
        self.assertIn("`intelligence-switch` 重点看 `deviceSerial + enable + type`", content)

    def test_skill_documents_field_semantics(self):
        docs_content = (
            Path(__file__).resolve().parents[2]
            / "docs"
            / "hik-cloud-open"
            / "device-alarm-capability-management.md"
        ).read_text(encoding="utf-8")
        ref_content = (
            Path(__file__).resolve().parents[1]
            / "references"
            / "device-alarm-capability-management.md"
        ).read_text(encoding="utf-8")
        skill_content = SKILL_PATH.read_text(encoding="utf-8")

        self.assertIn("`abilityCode` = 常规报警能力编码", docs_content)
        self.assertIn("`status` = 常规报警能力状态", docs_content)
        self.assertIn("`type` = 智能检测开关类型", docs_content)
        self.assertIn("10600", docs_content)
        self.assertIn("10627", docs_content)
        self.assertIn("`302` | 人形过滤", docs_content)
        self.assertIn("`304` | 人脸抠图", docs_content)

        self.assertIn("常规报警能力编码", ref_content)
        self.assertIn("常规报警能力状态", ref_content)
        self.assertIn("智能检测开关类型", ref_content)

        self.assertIn("`channelId + abilityCode + status`", skill_content)
        self.assertIn("`deviceSerial + enable + type`", skill_content)


if __name__ == "__main__":
    unittest.main()
