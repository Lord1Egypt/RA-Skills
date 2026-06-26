from pathlib import Path
import unittest


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_declares_openclaw_skill_key(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn('"skillKey": "hik-cloud-device-channel-management"', content)

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
            / "device-channel-management.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("docs/hik-cloud-open", content)

    def test_skill_documents_key_channel_enum_meanings(self):
        skill_content = SKILL_PATH.read_text(encoding="utf-8")
        reference_content = (
            Path(__file__).resolve().parents[1]
            / "references"
            / "device-channel-management.md"
        ).read_text(encoding="utf-8")
        docs_content = (
            Path(__file__).resolve().parents[2]
            / "docs"
            / "hik-cloud-open"
            / "device-channel-management.md"
        ).read_text(encoding="utf-8")

        self.assertIn("channelType = 通道类型", docs_content)
        self.assertIn("10300", docs_content)
        self.assertIn("10302", docs_content)
        self.assertIn("channelStatus = 通道状态", docs_content)
        self.assertIn("`0`：离线", docs_content)
        self.assertIn("`1`：在线", docs_content)
        self.assertIn("`-1`：未上报", docs_content)
        self.assertIn("syncLocal = 是否同步到设备本地", docs_content)
        self.assertIn("`channelName` 普通情况下最多 50 个字符", docs_content)
        self.assertIn("`syncLocal=1` 时最多 32 个字符", docs_content)

        self.assertIn("channelType = 通道类型", reference_content)
        self.assertIn("10300", reference_content)
        self.assertIn("10302", reference_content)
        self.assertIn("channelStatus = 通道状态", reference_content)
        self.assertIn("`0` 离线", reference_content)
        self.assertIn("`1` 在线", reference_content)
        self.assertIn("`-1` 未上报/未关联设备", reference_content)
        self.assertIn("syncLocal = 是否同步到设备本地", reference_content)
        self.assertIn("`channelName` 普通情况下最多 50 个字符", reference_content)
        self.assertIn("`syncLocal=1` 时最多 32 个字符", reference_content)

        self.assertIn("channelType = 通道类型", skill_content)
        self.assertIn("10300", skill_content)
        self.assertIn("10302", skill_content)
        self.assertIn("channelStatus = 通道状态", skill_content)
        self.assertIn("`0` 离线", skill_content)
        self.assertIn("`1` 在线", skill_content)
        self.assertIn("`-1` 未上报/未关联设备", skill_content)
        self.assertIn("syncLocal = 是否同步到设备本地", skill_content)
        self.assertIn("`channelName` 普通情况下最多 50 个字符", skill_content)
        self.assertIn("`syncLocal=1` 时最多 32 个字符", skill_content)


if __name__ == "__main__":
    unittest.main()
