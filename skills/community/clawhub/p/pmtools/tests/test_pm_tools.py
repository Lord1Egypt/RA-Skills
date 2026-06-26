import json
import os
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class _Recorder:
    def __init__(self):
        self.lock = threading.Lock()
        self.items = []

    def add(self, item):
        with self.lock:
            self.items.append(item)

    def last(self):
        with self.lock:
            return self.items[-1] if self.items else None


class _Handler(BaseHTTPRequestHandler):
    recorder = _Recorder()

    def log_message(self, fmt, *args):
        return

    def _read_body(self):
        n = int(self.headers.get("Content-Length", "0") or "0")
        if n <= 0:
            return b""
        return self.rfile.read(n)

    def _reply(self, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _record(self):
        body = self._read_body()
        parsed = urlparse(self.path)
        item = {
            "method": self.command,
            "path": parsed.path,
            "query": parse_qs(parsed.query, keep_blank_values=True),
            "headers": {k.lower(): v for k, v in self.headers.items()},
            "body": body,
        }
        self.recorder.add(item)
        return item

    def do_GET(self):
        item = self._record()
        self._reply({"code": 0, "msg": "success", "data": {"echo": {"path": item["path"], "query": item["query"]}}})

    def do_POST(self):
        item = self._record()
        if item["path"] == "/open-apis/auth/v3/tenant_access_token/internal":
            body = json.loads((item["body"] or b"{}").decode("utf-8"))
            if body.get("app_id") == "cli_test" and body.get("app_secret") == "sec_test":
                self._reply({"code": 0, "msg": "ok", "tenant_access_token": "t-tenant-test", "expire": 7200})
                return
            self._reply({"code": 1, "msg": "invalid app credentials"})
            return
        self._reply({"code": 0, "msg": "success", "data": {"echo": {"path": item["path"]}}})

    def do_PATCH(self):
        item = self._record()
        self._reply({"code": 0, "msg": "success", "data": {"echo": {"path": item["path"]}}})

    def do_PUT(self):
        item = self._record()
        self._reply({"code": 0, "msg": "success", "data": {"echo": {"path": item["path"]}}})

    def do_DELETE(self):
        item = self._record()
        self._reply({"code": 0, "msg": "success"})


def _start_server():
    httpd = HTTPServer(("127.0.0.1", 0), _Handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


class PmToolsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = _start_server()
        cls.base_url = f"http://127.0.0.1:{cls.httpd.server_port}/open-apis/okr/v1"
        cls.open_api_base = f"http://127.0.0.1:{cls.httpd.server_port}/open-apis"
        cls._orig_env = dict(os.environ)
        os.environ["FEISHU_OKR_BASE_URL"] = cls.base_url
        os.environ["FEISHU_OPEN_API_BASE_URL"] = cls.open_api_base
        os.environ["FEISHU_APP_ID"] = "cli_test"
        os.environ["FEISHU_APP_SECRET"] = "sec_test"
        os.environ["PM_TOOLS_DISABLE_AUTO_UPDATE"] = "1"
        os.environ["PM_TOOLS_TOKEN_CACHE_PATH"] = os.path.join(tempfile.gettempdir(), "pmtools_test_token.json")

        import importlib.util
        import pathlib

        script = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "pm_tools.py"
        spec = importlib.util.spec_from_file_location("pm_tools_mod", str(script))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cls.pm = mod

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        os.environ.clear()
        os.environ.update(cls._orig_env)

    def test_periods_create(self):
        self.pm.periods_create("r1", "2022-01")
        last = _Handler.recorder.last()
        self.assertEqual(last["method"], "POST")
        self.assertEqual(last["path"], "/open-apis/okr/v1/periods")
        self.assertIn("authorization", last["headers"])
        self.assertEqual(last["headers"]["authorization"], "Bearer t-tenant-test")
        body = json.loads(last["body"].decode("utf-8"))
        self.assertEqual(body["period_rule_id"], "r1")
        self.assertEqual(body["start_month"], "2022-01")

    def test_user_okrs_list_query(self):
        self.pm.user_okrs_list(
            user_id="ou_x",
            offset="0",
            limit="5",
            user_id_type="open_id",
            lang="zh_cn",
            period_ids=["p1", "p2"],
        )
        last = _Handler.recorder.last()
        self.assertEqual(last["method"], "GET")
        self.assertEqual(last["path"], "/open-apis/okr/v1/users/ou_x/okrs")
        self.assertEqual(last["query"]["offset"], ["0"])
        self.assertEqual(last["query"]["limit"], ["5"])
        self.assertEqual(last["query"]["lang"], ["zh_cn"])
        self.assertEqual(sorted(last["query"]["period_ids"]), ["p1", "p2"])

    def test_progress_create_plain_text(self):
        self.pm.progress_create(
            source_title="t",
            source_url="https://example.com",
            target_id="tid",
            target_type=2,
            text="hello",
            content_json=None,
            content_file=None,
            percent=12.34,
            status=1,
            source_url_pc=None,
            source_url_mobile=None,
            user_id_type=None,
        )
        last = _Handler.recorder.last()
        self.assertEqual(last["method"], "POST")
        self.assertEqual(last["path"], "/open-apis/okr/v1/progress_records")
        body = json.loads(last["body"].decode("utf-8"))
        self.assertEqual(body["target_type"], 2)
        self.assertIn("content", body)
        self.assertIn("progress_rate", body)

    def test_image_upload_multipart(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
            f.write(b"\x89PNG\r\n\x1a\n")
            fp = f.name
        try:
            self.pm.image_upload(fp, "tid", 2)
            last = _Handler.recorder.last()
            self.assertEqual(last["method"], "POST")
            self.assertEqual(last["path"], "/open-apis/okr/v1/images/upload")
            ct = last["headers"].get("content-type", "")
            self.assertTrue(ct.startswith("multipart/form-data; boundary="))
            self.assertIn(b'name="target_id"', last["body"])
            self.assertIn(b"tid", last["body"])
            self.assertIn(b'name="data"', last["body"])
        finally:
            os.unlink(fp)

    def test_self_update_cache_skip(self):
        with tempfile.TemporaryDirectory() as td:
            cache = os.path.join(td, "c.json")
            now = int(time.time())
            with open(cache, "w", encoding="utf-8") as f:
                json.dump({"last_checked_ts": now}, f)
            os.environ["PM_TOOLS_UPDATE_CACHE_PATH"] = cache
            res = self.pm.self_update()
            self.assertTrue(res["skipped"])


if __name__ == "__main__":
    unittest.main()
