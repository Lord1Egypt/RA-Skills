from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
CLI = ROOT / "scripts" / "mosobleirc.py"


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SKILL.read_text(encoding="utf-8").lower()
        cls.cli = CLI.read_text(encoding="utf-8").lower()

    def test_skill_forbids_direct_provider_and_write_bypasses(self):
        self.assertIn("не вызывай мособлеирц напрямую", self.text)
        self.assertIn("send readings", self.text)
        self.assertIn("не создавай и не выбирай `operation_id`", self.text)
        self.assertIn("не вызывай `send prepare`", self.text)
        self.assertIn("одного подтверждения", self.text)

    def test_skill_forbids_health_polling_and_login_loops(self):
        self.assertIn("не используй live-команды для health-check", self.text)
        self.assertIn("не запускай sms", self.text)
        self.assertIn("401/403", self.text)

    def test_skill_forbids_secret_and_gateway_detours(self):
        self.assertIn("не запрашивай yandex_api_key", self.text)
        self.assertIn("не открывай gateway config", self.text)
        self.assertIn("не делай direct http", self.text)
        self.assertIn("timeout/5xx", self.text)

    def test_skill_requires_supervised_months(self):
        self.assertIn("первые 2–3 месяца", self.text)
        self.assertIn("требует подтверждения пользователя", self.text)

    def test_skill_keeps_mutable_data_outside_skill_tree(self):
        self.assertIn("~/.local/share/mosobleirc", self.text)
        self.assertIn("reference-images", self.text)

    def test_skill_requires_human_confirmed_reading_before_send(self):
        self.assertIn("deep_read.py", self.text)
        self.assertIn("review", self.text)
        self.assertIn("подтверждение значения при review", self.text)
        self.assertIn("до verified", self.text)
        self.assertIn("не сохраняй", self.text)
        self.assertIn("<full-reading>", self.text)
        self.assertIn("send readings", self.text)

    def test_manual_override_keeps_physical_photo_reading_separate(self):
        self.assertIn("ручном override", self.text)
        self.assertIn("photo reading", self.text)
        self.assertIn("не заменяй", self.text)
        self.assertIn("на фото", self.text)
        self.assertIn("передано в еирц", self.text)

    def test_cli_has_no_direct_submit_command(self):
        self.assertNotIn('add_parser("submit")', self.cli)
        self.assertIn('"submit-check"', self.cli)

    def test_skill_forbids_nested_agent_ocr(self):
        self.assertIn("не запускай вложенные openclaw agent", self.text)
        self.assertIn("--black-digits", self.text)
        self.assertIn("--red-digits", self.text)
        self.assertIn("текущем turn", self.text)

    def test_skill_uses_human_review_instead_of_technical_ocr_failure(self):
        self.assertIn("review", self.text)
        self.assertIn("попроси владельца подтвердить", self.text)
        self.assertIn("не проси пользователя перекалибровывать", self.text)
        self.assertNotIn("минимум два независимых vision-прохода обязательны", self.text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
