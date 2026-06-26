from pathlib import Path
import unittest


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_declares_openclaw_skill_key(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn('"skillKey": "hik-cloud-device-management"', content)

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
            / "device-management.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("docs/hik-cloud-open", content)

    def test_reference_captures_key_status_semantics(self):
        content = (
            Path(__file__).resolve().parents[1]
            / "references"
            / "device-management.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`deviceStatus`：`0` 离线、`1` 在线", content)
        self.assertIn("`defence`：只在 `get + needDefence=true` 时返回", content)
        self.assertIn("`privacyStatus`：`0` 关闭、`1` 打开", content)
        self.assertIn("`pirStatus`：`1` 启用、`0` 禁用", content)
        self.assertIn("`alarmSoundMode`：`0` 短叫、`1` 长叫、`2` 静音、`3` 自定义语音", content)
        self.assertIn("`cloudStatus`：`-2` 不支持、`-1` 未开通、`0` 未激活、`1` 激活、`2` 过期", content)

    def test_docs_capture_key_status_semantics(self):
        content = (
            Path(__file__).resolve().parents[2]
            / "docs"
            / "hik-cloud-open"
            / "device-management.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`defence` 只会出现在 `get` 接口且请求参数 `needDefence=true` 时", content)
        self.assertIn("`privacyStatus` 用来判断隐私模式是否开启", content)
        self.assertIn("`alarmSoundMode` 用来判断告警声音播放方式", content)
        self.assertIn("`diskState` 是 SD 卡状态串", content)
        self.assertIn("`nvrDiskState` 是 NVR 硬盘状态串", content)

    def test_skill_summarizes_status_semantics(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("`defence`：只在 `get + --need-defence` 时返回", content)
        self.assertIn("`privacyStatus`：`0` 关闭、`1` 打开", content)
        self.assertIn("`diskState` / `nvrDiskState`：状态串按盘位拼接", content)


if __name__ == "__main__":
    unittest.main()
