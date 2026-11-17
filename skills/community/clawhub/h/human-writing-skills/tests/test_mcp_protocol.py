import io
import json
import threading
import unittest
from contextlib import redirect_stdout
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import humanwriting

from humanwriting.mcp_server import MAX_HTTP_BODY_BYTES, _http_handler, call_tool, handle_message, run_stdio


class McpProtocolTests(unittest.TestCase):
    def test_malformed_nested_writing_result_does_not_break_stdio(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outline.md").write_text("Mara keeps the key.", encoding="utf-8")
            call_tool("plan_long_form_writing", {"outline_path": "outline.md", "output_dir": "writing",
                      "style": "fiction", "target_length": 200, "chunk_size": 200}, root)
            claim = json.loads(call_tool("claim_writing_task", {
                "package_dir": "writing", "task_id": "outline-check", "agent_id": "worker",
            }, root)["content"][0]["text"])
            messages = [
                {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
                    "name": "submit_writing_result", "arguments": {"package_dir": "writing", "task_id": "outline-check",
                        "agent_id": "worker", "result": {"claim_token": claim["claim_token"], "decision": [], "coverage": [], "issues": []}}}},
                {"jsonrpc": "2.0", "id": 2, "method": "ping"},
            ]
            output = io.StringIO()
            with patch("sys.stdin", io.StringIO("\n".join(map(json.dumps, messages)))), redirect_stdout(output):
                run_stdio(root)
            responses = list(map(json.loads, output.getvalue().splitlines()))
            self.assertTrue(responses[0]["result"]["isError"])
            self.assertEqual(responses[1]["result"], {})

    def test_writing_result_and_claim_prompts_round_trip_over_stdio(self):
        queue = Mock()
        role_result = {"text": 'A "quoted" paragraph.\nNext line: \\ path.', "notes": ["Keep the narrator's voice."]}
        queue.submit_writing_result.return_value = {"accepted": True}
        queue.claim_writing_task.return_value = {
            "prompt": 'Write dialogue: "Wait."\nThen continue.',
            "claim_token": "opaque-stdio-claim",
            "result_schema": {"claim_token": "opaque-stdio-claim", "text": "complete prose"},
        }
        role_result["claim_token"] = queue.claim_writing_task.return_value["claim_token"]
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
                "name": "claim_writing_task", "arguments": {"package_dir": "writing", "task_id": "writer-001", "agent_id": "worker"}}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
                "name": "submit_writing_result", "arguments": {
                    "package_dir": "writing", "task_id": "writer-001", "agent_id": "worker", "result": role_result}}},
        ]
        output = io.StringIO()
        with TemporaryDirectory() as directory, patch.object(humanwriting, "writing_queue", queue, create=True):
            with patch("sys.stdin", io.StringIO("\n".join(map(json.dumps, messages)))), redirect_stdout(output):
                run_stdio(Path(directory))
            queue.submit_writing_result.assert_called_once_with(
                package_dir=Path(directory) / "writing", task_id="writer-001", agent_id="worker", result=role_result,
            )
        responses = list(map(json.loads, output.getvalue().splitlines()))
        claimed = json.loads(responses[0]["result"]["content"][0]["text"])
        self.assertEqual(claimed, queue.claim_writing_task.return_value)
        self.assertTrue(json.loads(responses[1]["result"]["content"][0]["text"])["accepted"])

    def test_invalid_writing_calls_preserve_stdio_json_framing(self):
        requests = [
            {"jsonrpc": "2.0", "id": 1, "method": "tools/list"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {
                "name": "plan_long_form_writing", "arguments": {
                    "outline_path": "../outside.md", "output_dir": "writing", "style": "fiction", "target_length": 1000}}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                "name": "submit_writing_result", "arguments": {
                    "package_dir": "writing", "task_id": "outline-check", "agent_id": "worker", "result": "not an object"}}},
            {"jsonrpc": "2.0", "id": 4, "method": "ping"},
        ]
        output = io.StringIO()
        with TemporaryDirectory() as directory:
            with patch("sys.stdin", io.StringIO("\n".join(map(json.dumps, requests)))), redirect_stdout(output):
                run_stdio(Path(directory))
        responses = list(map(json.loads, output.getvalue().splitlines()))
        self.assertEqual([response["id"] for response in responses], [1, 2, 3, 4])
        self.assertIn("plan_long_form_writing", {tool["name"] for tool in responses[0]["result"]["tools"]})
        self.assertTrue(responses[1]["result"]["isError"])
        self.assertTrue(responses[2]["result"]["isError"])
        self.assertEqual(responses[3]["result"], {})

    def test_malformed_prompt_does_not_kill_stdio_server(self):
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "prompts/get", "params": {"name": "humanize-quick", "arguments": None}},
            {"jsonrpc": "2.0", "id": 2, "method": "ping"},
        ]
        output = io.StringIO()
        with patch("sys.stdin", io.StringIO("\n".join(map(json.dumps, messages)))), redirect_stdout(output):
            run_stdio(Path.cwd())
        responses = list(map(json.loads, output.getvalue().splitlines()))
        self.assertEqual(responses[0]["error"]["code"], -32602)
        self.assertEqual(responses[1]["result"], {})

    def test_batches_notifications_and_invalid_envelopes(self):
        root = Path.cwd()
        notification = {"jsonrpc": "2.0", "method": "notifications/cancelled"}
        ping = {"jsonrpc": "2.0", "id": 3, "method": "ping"}
        self.assertIsNone(handle_message(notification, root))
        self.assertIsNone(handle_message([notification], root))
        self.assertEqual(handle_message([notification, ping], root), [handle_message(ping, root)])
        for invalid in ([], 3, {"method": "ping"}, {"jsonrpc": "2.0", "id": {}, "method": "ping"}):
            self.assertEqual(handle_message(invalid, root)["error"]["code"], -32600)

    def test_http_origin_auth_lengths_and_methods(self):
        with TemporaryDirectory() as directory:
            server = ThreadingHTTPServer(("127.0.0.1", 0), _http_handler(Path(directory), "secret"))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            def request(method="POST", extra=None, body=b'{}'):
                headers = {"Content-Type": "application/json", "Authorization": "Bearer secret"}
                headers.update(extra or {})
                conn = HTTPConnection(*server.server_address, timeout=5)
                try:
                    conn.request(method, "/mcp", body=body, headers=headers)
                    response = conn.getresponse()
                    response.read()
                    return response.status
                finally:
                    conn.close()
            try:
                self.assertEqual(request(extra={"Origin": "https://untrusted.example"}), 403)
                self.assertEqual(request(extra={"Authorization": "Bearer wrong"}), 401)
                self.assertEqual(request(extra={"Content-Length": "-1"}), 400)
                self.assertEqual(request(extra={"Content-Length": "abc"}), 400)
                self.assertEqual(request(extra={"Content-Length": str(MAX_HTTP_BODY_BYTES + 1)}), 413)
                self.assertEqual(request(extra={"Content-Type": "text/plain"}), 415)
                self.assertEqual(request(method="GET"), 405)
                self.assertEqual(request(body=b'{"jsonrpc":"2.0","method":"notifications/cancelled"}'), 202)
                self.assertEqual(request(body=b'{"jsonrpc":"2.0","id":1,"method":"ping"}'), 200)
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)
