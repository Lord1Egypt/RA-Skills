import datetime as dt
import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'hello.py'
sys.path.insert(0, str(SCRIPT.parent))

import hello  # noqa: E402


class HelloSkillTests(unittest.TestCase):
    def test_get_greeting_morning(self) -> None:
        result = hello.get_greeting('测试', dt.datetime(2026, 3, 10, 9, 0, 0))
        self.assertEqual(result['greeting'], '早上好')
        self.assertEqual(result['name'], '测试')
        self.assertIn('欢迎使用 OpenClaw Skills', result['message'])

    def test_cli_outputs_json(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), 'Codex'],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout)
        self.assertEqual(payload['name'], 'Codex')
        self.assertIn(payload['greeting'], {'早上好', '下午好', '晚上好'})


if __name__ == '__main__':
    unittest.main()
