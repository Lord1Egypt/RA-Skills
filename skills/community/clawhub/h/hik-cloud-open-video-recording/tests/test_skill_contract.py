from pathlib import Path
import unittest


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_declares_openclaw_skill_key(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn('"skillKey": "hik-cloud-video-recording"', content)

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
            / "video-recording.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("docs/hik-cloud-open", content)

    def test_skill_documents_key_enum_fields(self):
        skill_content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("## 关键枚举", skill_content)
        self.assertIn("`recType`：`local` 本地录像，`cloud` 云存储录像，`live` 实时录像/实时抽帧", skill_content)
        self.assertIn("`streamType`：`1` 高清主码流，`2` 标清子码流，默认 `1`", skill_content)
        self.assertIn("`devProto`：不传为萤石协议，传 `gb28181` 表示国标设备", skill_content)
        self.assertIn("`voiceSwitch`：`0` 关，`1` 开，`2` 自动，默认 `2`，仅 `record-instant` 使用", skill_content)
        self.assertIn("`frameModel`：`0` 普通，`1` 错峰，`2` 抽 I 帧", skill_content)
        self.assertIn("`fileType` / `fileChildType`：`0` 图片 / `00` jpg，`1` 视频 / `10` mp4，`2` 音频 / `20` mp3", skill_content)
        self.assertIn("`timeLines[].type`：`1` 视频文件，`3` 图片文件；`clip` 里不要和 `fileType` 混用", skill_content)


if __name__ == "__main__":
    unittest.main()
