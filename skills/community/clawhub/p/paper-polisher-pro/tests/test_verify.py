# -*- coding: utf-8 -*-
"""pp_verify 结构化零网络自证契约：正例放行 + 三类违规必须命中。"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from tests._common import SCRIPTS
except ImportError:  # 直跑模式（-s tests）
    from _common import SCRIPTS


def _loads(s):
    import json
    return json.loads(s)


class TestVerifyOnRealPackage(unittest.TestCase):
    def test_package_scripts_clean(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "pp_verify.py"), "--json"],
                             capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(out.returncode, 0, out.stdout)
        d = _loads(out.stdout)
        self.assertTrue(d["zero_network"])
        self.assertGreaterEqual(d["files_scanned"], 20)


class TestVerifyOnSynthetic(unittest.TestCase):
    def _run(self, code):
        tmp = Path(tempfile.mkdtemp(prefix="ppv_"))
        (tmp / "x.py").write_text(code, encoding="utf-8")
        try:
            out = subprocess.run([sys.executable, str(SCRIPTS / "pp_verify.py"),
                                  "--dir", str(tmp), "--json"],
                                 capture_output=True, text=True, encoding="utf-8")
            return out.returncode, _loads(out.stdout)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_urllib_import_caught(self):
        rc, d = self._run("import urllib.request\nurllib.request.urlopen('http://x')\n")
        self.assertEqual(rc, 1)
        self.assertFalse(d["zero_network"])
        self.assertTrue(any(h["kind"] in ("import", "call") for h in d["network_hits"]))

    def test_subprocess_curl_caught(self):
        rc, d = self._run("import subprocess\nsubprocess.run(['curl', '-s', 'http://x'])\n")
        self.assertEqual(rc, 1)
        self.assertTrue(any(h["kind"] == "subprocess-net" for h in d["network_hits"]))

    def test_requests_import_caught(self):
        rc, d = self._run("import requests\nrequests.get('http://x')\n")
        self.assertEqual(rc, 1)

    def test_url_constant_not_flagged(self):
        rc, d = self._run('GITHUB_URL = "https://github.com/example/x"\n'
                          "import urllib.parse\n"
                          "print(GITHUB_URL, urllib.parse.quote('论文'))\n")
        self.assertEqual(rc, 0, str(d["network_hits"]))
        self.assertTrue(d["zero_network"])

    def test_compile_error_reported(self):
        rc, d = self._run("def broken(:\n    pass\n")
        self.assertEqual(rc, 1)
        self.assertTrue(d["compile_errors"])


if __name__ == "__main__":
    unittest.main()
