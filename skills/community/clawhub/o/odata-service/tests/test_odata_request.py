import argparse
import contextlib
import importlib.util
import io
import json
import pathlib
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


SCRIPT = pathlib.Path(__file__).parents[1] / "scripts" / "odata_request.py"
SPEC = importlib.util.spec_from_file_location("odata_request", SCRIPT)
odata = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(odata)


class ServiceHandler(BaseHTTPRequestHandler):
    patch_count = 0
    patch_if_match = None
    patch_body = None

    def do_GET(self):
        if "$skiptoken=next" in self.path:
            payload = {"value": [{"Id": 3}], "@odata.deltaLink": "/odata/Things?$deltatoken=private"}
        else:
            payload = {"value": [{"Id": 1}, {"Id": 2}], "@odata.nextLink": "/odata/Things?$skiptoken=next"}
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_PATCH(self):
        type(self).patch_count += 1
        type(self).patch_if_match = self.headers.get("If-Match")
        length = int(self.headers.get("Content-Length", "0"))
        type(self).patch_body = self.rfile.read(length)
        self.send_response(204)
        self.send_header("ETag", 'W/"2"')
        self.end_headers()

    def log_message(self, format, *args):
        return


def transport_args(service_root):
    return dict(
        service_root=service_root,
        path="Things",
        query=[],
        odata_version="4.0",
        accept="application/json;odata.metadata=minimal",
        bearer_env=None,
        basic_user_env=None,
        basic_password_env=None,
        header_env=[],
        if_match=None,
        if_none_match=None,
        prefer=[],
        timeout=2.0,
        max_response_bytes=100_000,
    )


class ODataRequestTests(unittest.TestCase):
    def test_query_encoding_and_duplicate_detection(self):
        url = odata.add_query("https://example.test/odata/People", ["$filter=Name eq 'O''Neil'", "$top=5"])
        self.assertIn("$filter=Name+eq+'O''Neil'", url)
        with self.assertRaisesRegex(ValueError, "more than once"):
            odata.add_query("https://example.test/odata/People", ["$top=1", "$TOP=2"])

    def test_mutations_require_write_and_concurrency_intent(self):
        args = argparse.Namespace(allow_write=False, if_match=None, allow_unconditional=False)
        with self.assertRaisesRegex(ValueError, "state-changing"):
            odata.validate_mutation(args, "PATCH")
        args.allow_write = True
        with self.assertRaisesRegex(ValueError, "requires --if-match"):
            odata.validate_mutation(args, "DELETE")
        args.if_match = 'W/"1"'
        odata.validate_mutation(args, "DELETE")

    def test_url_redacts_opaque_tokens(self):
        value = odata.redact_url("https://example.test/odata/Things?$skiptoken=abc&tenant=west&sig=xyz")
        self.assertNotIn("abc", value)
        self.assertNotIn("xyz", value)
        self.assertIn("tenant=west", value)

    def test_pages_preserve_only_complete_final_delta_link(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), ServiceHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        values = transport_args(f"http://127.0.0.1:{server.server_port}/odata")
        values.update(max_pages=5, max_items=10)
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                odata.execute_pages(argparse.Namespace(**values))
        finally:
            server.shutdown()
            server.server_close()
        result = json.loads(output.getvalue())
        self.assertEqual([row["Id"] for row in result["value"]], [1, 2, 3])
        self.assertEqual(result["_retrieval"], {"pages": 2, "items": 3, "truncated": False})
        self.assertTrue(result["@odata.deltaLink"].endswith("$deltatoken=private"))

    def test_guarded_patch_sends_etag_and_body_once(self):
        ServiceHandler.patch_count = 0
        ServiceHandler.patch_if_match = None
        ServiceHandler.patch_body = None
        server = ThreadingHTTPServer(("127.0.0.1", 0), ServiceHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        values = transport_args(f"http://127.0.0.1:{server.server_port}/odata")
        with tempfile.TemporaryDirectory() as temp_dir:
            body_path = pathlib.Path(temp_dir) / "patch.json"
            body_path.write_text('{"Name":"Updated"}', encoding="utf-8")
            values.update(
                path="Things(1)",
                method="PATCH",
                body_file=str(body_path),
                empty_body=False,
                content_type="application/json",
                output_body=None,
                allow_write=True,
                allow_unconditional=False,
                allow_public_cross_origin_redirect=False,
                if_match='W/"1"',
            )
            output = io.StringIO()
            try:
                with contextlib.redirect_stdout(output):
                    odata.execute_request(argparse.Namespace(**values))
            finally:
                server.shutdown()
                server.server_close()
        result = json.loads(output.getvalue())
        self.assertEqual(result["status"], 204)
        self.assertEqual(ServiceHandler.patch_count, 1)
        self.assertEqual(ServiceHandler.patch_if_match, 'W/"1"')
        self.assertEqual(json.loads(ServiceHandler.patch_body), {"Name": "Updated"})

    def test_error_summary_omits_innererror(self):
        body = json.dumps({"error": {"code": "Conflict", "message": "Changed", "innererror": "stack"}}).encode()
        result = odata.error_summary(body, "application/json")
        self.assertEqual(result, {"code": "Conflict", "message": "Changed"})


if __name__ == "__main__":
    unittest.main()
