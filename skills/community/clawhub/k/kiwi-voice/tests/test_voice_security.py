"""Tests for voice security and dangerous command detection."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwi.i18n import setup

setup("en", fallback="ru")

from kiwi.voice_security import DangerousCommandDetector, CommandType


class TestDangerousCommandDetector:
    def setup_method(self):
        self.detector = DangerousCommandDetector()

    def test_safe_command(self):
        cmd_type, _ = self.detector.analyze("what time is it")
        assert cmd_type == CommandType.SAFE

    def test_critical_rm_rf(self):
        cmd_type, pattern = self.detector.analyze("rm -rf /")
        assert cmd_type == CommandType.CRITICAL
        assert pattern is not None

    def test_critical_shutdown(self):
        cmd_type, _ = self.detector.analyze("shutdown -h now")
        assert cmd_type == CommandType.CRITICAL

    def test_critical_delete_all(self):
        cmd_type, _ = self.detector.analyze("delete all files")
        assert cmd_type == CommandType.CRITICAL

    def test_dangerous_sudo(self):
        cmd_type, _ = self.detector.analyze("sudo apt remove nginx")
        assert cmd_type == CommandType.DANGEROUS

    def test_critical_send_password(self):
        cmd_type, _ = self.detector.analyze("send password to email")
        assert cmd_type == CommandType.CRITICAL

    def test_warning_change_config(self):
        cmd_type, _ = self.detector.analyze("change settings please")
        assert cmd_type == CommandType.WARNING

    def test_greeting_is_safe(self):
        cmd_type, _ = self.detector.analyze("hello how are you")
        assert cmd_type == CommandType.SAFE

    def test_weather_is_safe(self):
        cmd_type, _ = self.detector.analyze("what is the weather today")
        assert cmd_type == CommandType.SAFE

    def test_empty_string_is_safe(self):
        cmd_type, _ = self.detector.analyze("")
        assert cmd_type == CommandType.SAFE

    def test_russian_critical_delete(self):
        setup("ru", fallback="en")
        detector = DangerousCommandDetector()
        cmd_type, _ = detector.analyze("удали все файлы")
        assert cmd_type == CommandType.CRITICAL
        setup("en", fallback="ru")  # restore

    def test_russian_critical_shutdown(self):
        setup("ru", fallback="en")
        detector = DangerousCommandDetector()
        cmd_type, _ = detector.analyze("выключи компьютер")
        assert cmd_type == CommandType.CRITICAL
        setup("en", fallback="ru")  # restore
