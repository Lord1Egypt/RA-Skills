# -*- coding: utf-8 -*-
"""Offline unit tests for scripts/ensure_env.py.

Fully offline: pip / subprocess / import probing are mocked, so no package is
ever installed and no network is touched.
"""

import io
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"),
)

import ensure_env  # noqa: E402


class TestHelpers(unittest.TestCase):
    def test_check_import_true(self):
        self.assertTrue(ensure_env.check_import("json"))

    def test_check_import_false(self):
        self.assertFalse(ensure_env.check_import("no_such_module_zzz_38"))

    def test_ok_prints(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ensure_env.ok("hello")
        self.assertIn("[ok] hello", buf.getvalue())

    def test_fail_prints_stderr_and_returns_false(self):
        buf = io.StringIO()
        with redirect_stderr(buf):
            result = ensure_env.fail("boom")
        self.assertFalse(result)
        self.assertIn("[error] boom", buf.getvalue())


class TestRunCmd(unittest.TestCase):
    def test_success_returns_zero(self):
        proc = subprocess.CompletedProcess(
            args=["x"], returncode=0, stdout="", stderr="")
        with mock.patch("subprocess.run", return_value=proc):
            self.assertEqual(ensure_env.run_cmd(["x"]), 0)

    def test_nonzero_returns_code_and_writes_stderr_tail(self):
        proc = subprocess.CompletedProcess(
            args=["x"], returncode=2, stdout="", stderr="tail-error")
        buf = io.StringIO()
        with mock.patch("subprocess.run", return_value=proc), redirect_stderr(buf):
            self.assertEqual(ensure_env.run_cmd(["x"]), 2)
        self.assertIn("tail-error", buf.getvalue())

    def test_timeout_returns_one(self):
        buf = io.StringIO()
        with mock.patch(
                "subprocess.run",
                side_effect=subprocess.TimeoutExpired(cmd=["x"], timeout=1)), \
                redirect_stderr(buf):
            self.assertEqual(ensure_env.run_cmd(["x"], timeout=1), 1)
        self.assertIn("超时", buf.getvalue())


class TestPipInstall(unittest.TestCase):
    def test_first_mirror_success(self):
        calls = []

        def fake_run(cmd, timeout=300):
            calls.append(cmd)
            return 0

        with mock.patch.object(ensure_env, "run_cmd", fake_run):
            self.assertTrue(ensure_env.pip_install(["pkg"]))
        self.assertEqual(len(calls), 1)
        self.assertIn("-i", calls[0])
        self.assertIn("pypi.tuna.tsinghua.edu.cn", calls[0])
        self.assertIn("pkg", calls[0])

    def test_falls_back_to_official_index(self):
        calls = []

        def fake_run(cmd, timeout=300):
            calls.append(cmd)
            return 1 if "-i" in cmd else 0

        with mock.patch.object(ensure_env, "run_cmd", fake_run):
            self.assertTrue(ensure_env.pip_install(["pkg"]))
        self.assertEqual(len(calls), 3)
        self.assertNotIn("-i", calls[-1])

    def test_all_sources_fail(self):
        with mock.patch.object(ensure_env, "run_cmd", return_value=1):
            self.assertFalse(ensure_env.pip_install(["pkg"]))

    def test_upgrade_flag_forwarded(self):
        captured = {}

        def fake_run(cmd, timeout=300):
            captured["cmd"] = cmd
            return 0

        with mock.patch.object(ensure_env, "run_cmd", fake_run):
            self.assertTrue(ensure_env.pip_install(["pkg"], upgrade=True))
        self.assertIn("--upgrade", captured["cmd"])


class TestEnsureEnv(unittest.TestCase):
    def test_all_present_skips_install(self):
        buf = io.StringIO()
        with mock.patch.object(ensure_env, "check_import", return_value=True), \
                mock.patch.object(ensure_env, "pip_install") as pip, \
                redirect_stdout(buf):
            self.assertTrue(ensure_env.ensure_env())
        pip.assert_not_called()
        self.assertIn("ready", buf.getvalue())

    def test_installs_missing_then_ready(self):
        installed = {"value": False}

        def fake_check(_name):
            return installed["value"]

        def fake_pip(_packages, upgrade=False):
            installed["value"] = True
            return True

        buf = io.StringIO()
        with mock.patch.object(ensure_env, "check_import", fake_check), \
                mock.patch.object(ensure_env, "pip_install", fake_pip), \
                redirect_stdout(buf):
            self.assertTrue(ensure_env.ensure_env())
        self.assertIn("installing missing packages", buf.getvalue())

    def test_install_failure_returns_false(self):
        buf, err = io.StringIO(), io.StringIO()
        with mock.patch.object(ensure_env, "check_import", return_value=False), \
                mock.patch.object(ensure_env, "pip_install", return_value=False), \
                redirect_stdout(buf), redirect_stderr(err):
            self.assertFalse(ensure_env.ensure_env())
        self.assertIn("依赖安装失败", err.getvalue())

    def test_post_install_still_unimportable(self):
        buf, err = io.StringIO(), io.StringIO()
        with mock.patch.object(ensure_env, "check_import", return_value=False), \
                mock.patch.object(ensure_env, "pip_install", return_value=True), \
                redirect_stdout(buf), redirect_stderr(err):
            self.assertFalse(ensure_env.ensure_env())
        self.assertIn("仍无法导入", err.getvalue())

    def test_upgrade_forces_install(self):
        buf = io.StringIO()
        with mock.patch.object(ensure_env, "check_import", return_value=True), \
                mock.patch.object(ensure_env, "pip_install", return_value=True) as pip, \
                redirect_stdout(buf):
            self.assertTrue(ensure_env.ensure_env(upgrade=True))
        pip.assert_called_once()
        self.assertIn("installing missing packages", buf.getvalue())


class TestMain(unittest.TestCase):
    def test_success_returns_zero(self):
        buf = io.StringIO()
        with mock.patch.object(ensure_env, "ensure_env", return_value=True) as inner, \
                redirect_stdout(buf):
            rc = ensure_env.main([])
        self.assertEqual(rc, 0)
        inner.assert_called_once_with(upgrade=False)

    def test_failure_returns_one(self):
        buf = io.StringIO()
        with mock.patch.object(ensure_env, "ensure_env", return_value=False), \
                redirect_stdout(buf):
            self.assertEqual(ensure_env.main([]), 1)

    def test_upgrade_flag_forwarded(self):
        buf = io.StringIO()
        with mock.patch.object(ensure_env, "ensure_env", return_value=True) as inner, \
                redirect_stdout(buf):
            rc = ensure_env.main(["--upgrade"])
        self.assertEqual(rc, 0)
        inner.assert_called_once_with(upgrade=True)


if __name__ == "__main__":
    unittest.main()