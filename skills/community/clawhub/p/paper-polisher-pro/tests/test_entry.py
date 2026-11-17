# -*- coding: utf-8 -*-
"""pp.py 统一入口契约：路由表指向真实文件、内建子命令行为、未知命令退出码。"""
import subprocess
import sys
import unittest

try:
    from tests._common import PKG_ROOT, SCRIPTS
except ImportError:  # 直跑模式（-s tests）
    from _common import PKG_ROOT, SCRIPTS

PP = str(SCRIPTS / "pp.py")


class TestRouting(unittest.TestCase):
    def test_all_commands_point_to_existing_scripts(self):
        code = ("import sys; sys.path.insert(0, %r);"
                "from pp import COMMANDS; import os;"
                "missing = [s for s, *_ in COMMANDS.values()"
                " if not os.path.exists(os.path.join(%r, s))];"
                "print('MISSING:', missing)") % (str(SCRIPTS), str(SCRIPTS))
        out = subprocess.run([sys.executable, "-c", code],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertIn("MISSING: []", out.stdout, out.stdout + out.stderr)

    def test_fix_and_verify_registered(self):
        out = subprocess.run([sys.executable, PP], capture_output=True,
                             text=True, encoding="utf-8")
        self.assertEqual(out.returncode, 0)
        for word in ("fix", "verify", "quickstart", "test"):
            self.assertIn(word, out.stdout)

    def test_unknown_command_exit2(self):
        out = subprocess.run([sys.executable, PP, "no-such-cmd"],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(out.returncode, 2)

    def test_quickstart_runs(self):
        out = subprocess.run([sys.executable, PP, "quickstart"],
                             capture_output=True, text=True, encoding="utf-8",
                             timeout=180)
        self.assertEqual(out.returncode, 0, out.stderr[-400:])
        for marker in ("第 1 步", "第 2 步", "第 3 步"):
            self.assertIn(marker, out.stdout)


if __name__ == "__main__":
    unittest.main()
