from pathlib import Path
import unittest


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_declares_openclaw_skill_key(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn('"skillKey": "hik-cloud-device-control"', content)

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

    def test_skill_documents_device_time_sync_capability(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("设备校时", content)
        self.assertIn("time-get", content)
        self.assertIn("ntp-config-set", content)
        self.assertIn("NTP `addressingFormatType`", content)
        self.assertIn("`hostname` 模式主要使用 `hostName`", content)
        self.assertIn("`ipaddress` 模式主要使用 `ipAddress`", content)

    def test_skill_documents_ptz_mode_speed_relationship(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("云台 `mode` / `speed`", content)
        self.assertIn("`mode=0` 时 `speed` 只能取 `0-慢`、`1-适中`、`2-快`", content)
        self.assertIn("`mode=1` 时 `speed` 只能取 `0~7`", content)

    def test_skill_documents_storage_card_init_capability(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("设备存储卡初始化", content)
        self.assertIn("storage-init", content)
        self.assertIn("storage-init-progress", content)

    def test_skill_references_device_time_sync_reference_is_self_contained(self):
        ref_path = Path(__file__).resolve().parents[1] / "references" / "time-sync.md"
        content = ref_path.read_text(encoding="utf-8")
        self.assertIn("获取设备校时配置", content)
        self.assertIn("https://pic.hik-cloud.com/opencustom/apidoc/online/open/7093bbc2db7a427ca5b60001caff338d.html", content)
        self.assertNotIn("docs/hik-cloud-open", content)
        self.assertIn("addressingFormatType", content)
        self.assertIn("`hostname` 时主要使用 `hostName`", content)
        self.assertIn("`ipaddress` 时主要使用 `ipAddress`", content)
        self.assertIn("ipv6Address", content)

    def test_skill_references_ptz_mode_and_speed_relationship(self):
        ref_path = Path(__file__).resolve().parents[1] / "references" / "ptz-control.md"
        content = ref_path.read_text(encoding="utf-8")
        self.assertIn("`mode=0` 时，`speed` 只能取 `0-慢`、`1-适中`、`2-快`", content)
        self.assertIn("`mode=1` 时，`speed` 只能取 `0~7`", content)
        self.assertIn("mode", content)
        self.assertIn("speed", content)

    def test_skill_references_storage_card_init_reference_is_self_contained(self):
        ref_path = Path(__file__).resolve().parents[1] / "references" / "storage-card-init.md"
        content = ref_path.read_text(encoding="utf-8")
        self.assertIn("存储卡初始化", content)
        self.assertIn("存储卡初始化进度查询", content)
        self.assertIn("https://pic.hik-cloud.com/opencustom/apidoc/online/open/a9efdfc48a2f4ab5bd7c44ba325b6642.html", content)
        self.assertNotIn("docs/hik-cloud-open", content)


if __name__ == "__main__":
    unittest.main()
