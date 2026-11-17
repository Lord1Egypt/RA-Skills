import hashlib
import json
import threading
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from urllib.request import Request, urlopen

from http.server import ThreadingHTTPServer

from humanwriting.mcp_server import MAX_TEXT_CHARACTERS, TOOLS, _http_handler, call_tool, get_prompt, handle_message


def complete_report(task_id: str) -> str:
    return (
        "# Review Findings\n\n"
        "No contradiction was found in the assigned material.\n\n"
        "# Coverage Receipt\n\n"
        f"- Task ID: `{task_id}`\n"
        "- Scope: assigned body\n"
        "- Coverage: complete\n"
        "- Units checked: every assigned paragraph\n"
        "- Confirmed findings: 0\n"
        "- Unchecked or blocked material: none\n"
    )


class McpServerTests(unittest.TestCase):
    def test_writing_results_share_core_budget_above_single_text_limit(self):
        with TemporaryDirectory() as directory:
            from humanwriting.writing_queue import MAX_RESULT
            payload = {"text": "x" * (MAX_TEXT_CHARACTERS + 100)}
            with patch("humanwriting.writing_queue.submit_writing_result", return_value={"accepted": True}) as submit:
                result = call_tool("submit_writing_result", {"package_dir": ".", "task_id": "write-0001",
                    "agent_id": "writer", "result": payload}, Path(directory))
                self.assertTrue(json.loads(result["content"][0]["text"])["accepted"])
                submit.assert_called_once()
            with self.assertRaisesRegex(ValueError, str(MAX_RESULT)):
                call_tool("submit_writing_result", {"package_dir": ".", "task_id": "write-0001",
                    "agent_id": "writer", "result": {"text": "x" * MAX_RESULT}}, Path(directory))

    def test_mcp_rejects_stale_claim_token_after_same_agent_reclaims(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outline.md").write_text("Mara keeps the key.", encoding="utf-8")
            call_tool("plan_long_form_writing", {"outline_path": "outline.md", "output_dir": "writing",
                      "style": "fiction", "target_length": 200, "chunk_size": 200}, root)
            args = {"package_dir": "writing", "task_id": "outline-check", "agent_id": "worker"}
            first = json.loads(call_tool("claim_writing_task", args, root)["content"][0]["text"])
            with patch("humanwriting.writing_queue.LEASE_SECONDS", 0):
                current = json.loads(call_tool("claim_writing_task", args, root)["content"][0]["text"])
            self.assertIsInstance(current["claim_token"], str)
            self.assertTrue(current["claim_token"])
            self.assertNotEqual(first["claim_token"], current["claim_token"])
            self.assertEqual(current["result_schema"]["claim_token"], current["claim_token"])
            result = {"decision": "pass", "coverage": [{"id": "O0001", "quote": "Mara keeps",
                      "note": "The key's owner is explicit."}], "issues": [], "claim_token": first["claim_token"]}
            request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {
                "name": "submit_writing_result", "arguments": {**args, "result": result}}}
            rejected = handle_message(request, root)["result"]
            self.assertTrue(rejected["isError"])
            self.assertIn("token", rejected["content"][0]["text"].lower())
            result["claim_token"] = current["claim_token"]
            accepted = handle_message(request, root)["result"]
            self.assertNotIn("isError", accepted)

    def test_writing_workflow_claims_structured_roles_and_assembles_verified_prose(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "outline.md").write_text("Mara waits at the station with a key.", encoding="utf-8")
            for name, text in (("context", "Mara owns the key."), ("source", "The station closes at dusk."),
                               ("reference", "Use a plain, close third-person voice.")):
                (root / f"{name}.md").write_text(text, encoding="utf-8")
            text = ('Mara held the key against her palm. "Wait," she said. The platform clock stopped. '
                    'She looked along the empty tracks and listened for a train. No one answered from the ticket office. '
                    'She moved toward the door, keeping the key hidden in her fist. The sign said the station closed at dusk.')
            target = len("".join(text.split()))
            def invoke(name, **arguments):
                return json.loads(call_tool(name, arguments, root)["content"][0]["text"])
            planned = invoke("plan_long_form_writing", outline_path="outline.md", output_dir="writing", style="fiction",
                             target_length=target, chunk_size=500, context_paths=["context.md"],
                             source_paths=["source.md"], reference_paths=["reference.md"])
            self.assertEqual(planned["chunk_count"], 1)
            listed = invoke("list_writing_tasks", package_dir="writing")
            self.assertEqual([task["task_id"] for task in listed["tasks"] if task["ready"]], ["outline-check"])
            self.assertFalse(invoke("verify_writing_project", package_dir="writing")["ready_for_assembly"])
            with self.assertRaisesRegex(ValueError, "before assembly"):
                invoke("assemble_writing_project", package_dir="writing", output_path="final.md")
            with self.assertRaisesRegex(ValueError, "not ready"):
                invoke("claim_writing_task", package_dir="writing", task_id="continuity", agent_id="final-editor")
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            results = [
                ("outline-check", "planner", {"decision": "pass", "coverage": [
                    {"id": "O0001", "quote": "Mara waits", "note": "Starting action and location are explicit."}], "issues": []}),
                ("chunk-plan", "planner", {"style_contract": "Plain, close third-person fiction.", "chunks": [{
                    "id": "chunk-0001", "title": "The station", "brief": "Mara waits, then approaches the door.",
                    "outline_ids": ["O0001"], "entry_state": "Mara has the key.", "exit_state": "Mara keeps the key.",
                    "source_ids": ["S0001"], "reference_ids": ["R0001"], "depends_on": [], "independent": False}]}),
                ("write-0001", "writer", {"text": text, "covered_outline_ids": ["O0001"],
                    "state": {"Mara.key": "held"}, "state_changes": [], "pending_threads": [], "handoff": "Mara approaches the station door."}),
                ("review-0001", "editor", {"decision": "pass", "text_sha256": digest,
                    "coverage": [{"id": "P0001", "quote": "Mara held the key", "note": "The key remains in her possession."}],
                    "checks": {key: {"status": "pass", "note": "The scene matches the bounded assignment."}
                               for key in ("outline", "continuity", "voice", "naturalness")}, "issues": []}),
                ("continuity", "final-editor", {"decision": "pass", "chunks": [{"id": "chunk-0001", "text_sha256": digest,
                    "note": "The location, key and voice remain consistent."}], "boundaries": [], "revision_chunks": [], "issues": []}),
            ]
            for task_id, agent_id, result in results:
                claim = invoke("claim_writing_task", package_dir="writing", task_id=task_id, agent_id=agent_id)
                self.assertTrue(claim["content"])
                self.assertIsInstance(claim["result_schema"], dict)
                result["claim_token"] = claim["claim_token"]
                invoke("submit_writing_result", package_dir="writing", task_id=task_id, agent_id=agent_id, result=result)
            self.assertTrue(invoke("verify_writing_project", package_dir="writing")["ready_for_assembly"])
            assembled = invoke("assemble_writing_project", package_dir="writing", output_path="final.md")
            self.assertEqual(Path(assembled["output_path"]).read_text(encoding="utf-8"), text + "\n")

    def test_context_pagination_reads_full_json_and_validates_offsets(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            value = {"text": ('A "quoted" line.\n' + "\u96e8") * 4000, "tail": "Final state must not disappear."}
            text = json.dumps(value, ensure_ascii=False)
            (root / "result.json").write_text(text, encoding="utf-8")
            offset = 0
            pages = []
            while offset is not None:
                page = json.loads(call_tool("read_project_context", {
                    "path": "result.json", "offset": offset, "max_characters": 20000,
                }, root)["content"][0]["text"])
                pages.append(page["content"])
                self.assertEqual(page["truncated"], page["next_offset"] is not None)
                if page["next_offset"] is not None:
                    self.assertEqual(page["next_offset"], offset + 20000)
                offset = page["next_offset"]
            self.assertGreater(len(pages), 1)
            self.assertEqual(json.loads("".join(pages)), value)
            for offset in (len(text), len(text) + 100):
                page = json.loads(call_tool("read_project_context", {"path": "result.json", "offset": offset}, root)["content"][0]["text"])
                self.assertEqual(page["content"], "")
                self.assertFalse(page["truncated"])
                self.assertIsNone(page["next_offset"])
            for offset in (-1, True, 1.5, "0", None):
                with self.subTest(offset=offset), self.assertRaisesRegex(ValueError, "offset"):
                    call_tool("read_project_context", {"path": "result.json", "offset": offset}, root)

    def test_writing_tool_schemas_are_typed_and_closed(self):
        tools = {tool["name"]: tool["inputSchema"] for tool in TOOLS}
        names = {"plan_long_form_writing", "list_writing_tasks", "claim_writing_task",
                 "submit_writing_result", "verify_writing_project", "assemble_writing_project"}
        self.assertTrue(names <= tools.keys())
        for name in names:
            schema = tools[name]
            self.assertEqual(schema["type"], "object")
            self.assertFalse(schema["additionalProperties"])
            self.assertTrue(set(schema["required"]) <= schema["properties"].keys())
            self.assertTrue(all("type" in prop for prop in schema["properties"].values()))
        self.assertEqual(tools["submit_writing_result"]["properties"]["result"]["type"], "object")
        self.assertEqual(tools["plan_long_form_writing"]["properties"]["execution_mode"]["enum"],
                         ["sequential", "contract"])

    def test_writing_paths_and_arguments_are_validated_before_dispatch(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            base = {"outline_path": "outline.md", "output_dir": "writing", "style": "fiction", "target_length": 1000}
            for field in ("outline_path", "output_dir", "context_paths", "source_paths", "reference_paths"):
                with self.subTest(field=field):
                    value = ["../outside.md"] if field.endswith("_paths") else "../outside"
                    with self.assertRaisesRegex(ValueError, "within the configured"):
                        call_tool("plan_long_form_writing", {**base, field: value}, root)
            for field, value in (("target_length", True), ("target_length", 0), ("target_length", 5000001),
                                 ("chunk_size", "5000"), ("chunk_size", 199), ("chunk_size", 12001),
                                 ("max_parallel", 0), ("max_parallel", 33), ("execution_mode", "parallel"),
                                 ("length_unit", "bytes"), ("style", "unknown"), ("context_paths", [None]),
                                 ("reference_paths", [""]), ("source_paths", "source.md"), ("extra", 1)):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    call_tool("plan_long_form_writing", {**base, field: value}, root)
            for name in ("list_writing_tasks", "claim_writing_task", "submit_writing_result",
                         "verify_writing_project", "assemble_writing_project"):
                args = {"package_dir": "../escape"}
                if name in {"claim_writing_task", "submit_writing_result"}:
                    args.update(task_id="outline-check", agent_id="worker")
                if name == "submit_writing_result":
                    args["result"] = {}
                if name == "assemble_writing_project":
                    args["output_path"] = "final.md"
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, "within the configured"):
                    call_tool(name, args, root)
            with self.assertRaisesRegex(ValueError, "within the configured"):
                call_tool("assemble_writing_project", {"package_dir": "writing", "output_path": "../final.md"}, root)

    def test_writing_result_objects_are_bounded_and_strict_json(self):
        from humanwriting.writing_queue import MAX_RESULT
        with TemporaryDirectory() as directory:
            args = {"package_dir": "writing", "task_id": "outline-check", "agent_id": "worker"}
            for result in ([], "text", None, {"text": "x" * MAX_RESULT}, {"number": float("nan")}):
                with self.subTest(result_type=type(result).__name__), self.assertRaises(ValueError):
                    call_tool("submit_writing_result", {**args, "result": result}, Path(directory))

    def test_generation_sources_and_voice_references_are_root_bounded(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "source.md").write_text("Observed battery runtime: six hours.", encoding="utf-8")
            (root / "voice.md").write_text("Short, plain sentences. A limited conclusion.", encoding="utf-8")
            prompt = call_tool("compile_generation_prompt", {
                "style": "self-media", "task": "Write a review from the supplied observation.",
                "source_paths": ["source.md"], "reference_paths": ["voice.md"],
            }, root)["content"][0]["text"]
            self.assertIn("Observed battery runtime", prompt)
            self.assertIn("Supplied Factual Sources", prompt)
            self.assertIn("reference-style-alignment", prompt)
            with self.assertRaisesRegex(ValueError, "within the configured"):
                call_tool("compile_generation_prompt", {
                    "style": "fiction", "task": "Write a scene.", "reference_paths": ["../voice.md"],
                }, root)

    def test_initialize_lists_tools_and_blocks_path_escape(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            initialized = handle_message(
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}, root
            )
            listed = handle_message({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, root)
            escaped = handle_message(
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {
                        "name": "read_project_context",
                        "arguments": {"path": "../outside.md"},
                    },
                },
                root,
            )

        self.assertEqual(initialized["result"]["serverInfo"]["name"], "advanced-human-writing")
        self.assertEqual(len(listed["result"]["tools"]), len(TOOLS))
        self.assertTrue(escaped["result"]["isError"])
        self.assertIn("within the configured project root", escaped["result"]["content"][0]["text"])

    def test_single_text_tools_and_native_prompts_are_available(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            lint = call_tool("lint_text", {"text": "未来可期。"}, root)
            stats = call_tool("get_style_statistics", {"text": "Short. A longer sentence follows."}, root)
            protection = call_tool(
                "verify_protected_content",
                {"source_text": "API returned 200.", "candidate_text": "API returned 201."},
                root,
            )
            fidelity = call_tool(
                "verify_fidelity",
                {"source_text": "The rate may be 20% [1].", "candidate_text": "The rate is 20% [1]."},
                root,
            )
            ledger = call_tool("compile_ledger_extraction", {"draft": "Mara leaves the key."}, root)
        self.assertIn("CLOSE001", lint["content"][0]["text"])
        self.assertIn("sentence_length_cv", stats["content"][0]["text"])
        self.assertIn("missing_or_changed", protection["content"][0]["text"])
        self.assertEqual(json.loads(fidelity["content"][0]["text"])["status"], "needs-review")
        self.assertIn("Continuity Ledger Extraction", ledger["content"][0]["text"])

        prompts = handle_message({"jsonrpc": "2.0", "id": 5, "method": "prompts/list"}, root)
        self.assertIn("humanize-quick", {item["name"] for item in prompts["result"]["prompts"]})
        prompt = get_prompt("extract-ledger", {"draft": "Mara leaves the key."})
        self.assertIn("Continuity Ledger Extraction", prompt["messages"][0]["content"]["text"])

    def test_agents_claim_submit_verify_then_unlock_reconciliation(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "novel.md"
            ledger = root / "ledger.md"
            draft.write_text(
                ("“你要走吗？”她问。\n\n他没有回答。\n\n" + "雨落在窗外。" * 300)
                + ("\n\n" + "他沿着河岸继续走。" + "天色渐暗。" * 300),
                encoding="utf-8",
            )
            ledger.write_text("两人仍因信件争执。", encoding="utf-8")
            plan_result = call_tool(
                "plan_long_form_audit",
                {
                    "draft_path": "novel.md",
                    "output_dir": "audit",
                    "style": "fiction",
                    "context_path": "ledger.md",
                    "agent_mode": "deep",
                    "chunk_size": 2000,
                },
                root,
            )
            package = Path(json.loads(plan_result["content"][0]["text"])["package_dir"])
            listed = json.loads(
                call_tool("list_audit_tasks", {"package_dir": "audit"}, root)["content"][0]["text"]
            )
            baseline = next(task for task in listed["tasks"] if task["task_id"] == "baseline")
            self.assertTrue(baseline["ready"])
            with self.assertRaisesRegex(ValueError, "not ready"):
                call_tool(
                    "claim_audit_task",
                    {"package_dir": "audit", "task_id": "reconcile", "agent_id": "final-editor"},
                    root,
                )

            plan = json.loads((package / "agent-plan.json").read_text(encoding="utf-8"))
            for task in plan["tasks"]:
                if not task["required_before_reconciliation"]:
                    continue
                agent_id = f"worker-{task['task_id']}"
                call_tool(
                    "claim_audit_task",
                    {"package_dir": "audit", "task_id": task["task_id"], "agent_id": agent_id},
                    root,
                )
                call_tool(
                    "submit_audit_report",
                    {
                        "package_dir": "audit",
                        "task_id": task["task_id"],
                        "agent_id": agent_id,
                        "report_markdown": complete_report(task["task_id"]),
                    },
                    root,
                )

            verification = json.loads(
                call_tool("verify_audit_coverage", {"package_dir": "audit"}, root)["content"][0]["text"]
            )
            reconciliation = json.loads(
                call_tool("get_reconciliation_task", {"package_dir": "audit"}, root)["content"][0]["text"]
            )
            state = json.loads((package / "agent-state.json").read_text(encoding="utf-8"))

        self.assertTrue(verification["ready_for_reconciliation"])
        self.assertEqual(reconciliation["task_id"], "reconcile")
        self.assertIn("Reconciliation", reconciliation["content"])
        self.assertEqual(len(state["tasks"]), verification["planned"])

    def test_mcp_can_plan_opt_in_whole_book_review(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "novel.md"
            draft.write_text(
                "\n\n".join(f"Chapter {index}\n\n" + "A choice changes the next scene. " * 100 for index in range(1, 4)),
                encoding="utf-8",
            )
            call_tool("plan_long_form_audit", {
                "draft_path": "novel.md", "output_dir": "audit", "style": "fiction",
                "chunk_size": 2000, "book_level": True,
            }, root)
            plan = json.loads((root / "audit" / "agent-plan.json").read_text(encoding="utf-8"))
            self.assertIn("whole-book-architecture-audit", {task["kind"] for task in plan["tasks"]})
            self.assertTrue((root / "audit" / "00-chapter-map.json").is_file())
            with self.assertRaisesRegex(ValueError, "not ready"):
                call_tool("claim_audit_task", {"package_dir": "audit", "task_id": "book-architecture"}, root)
            for task in plan["tasks"]:
                if task["task_id"] in {"book-architecture", "reconcile"}:
                    continue
                call_tool("claim_audit_task", {"package_dir": "audit", "task_id": task["task_id"]}, root)
                call_tool("submit_audit_report", {
                    "package_dir": "audit", "task_id": task["task_id"],
                    "report_markdown": complete_report(task["task_id"]),
                }, root)
            with self.assertRaisesRegex(ValueError, "not ready"):
                call_tool("claim_audit_task", {"package_dir": "audit", "task_id": "reconcile"}, root)
            call_tool("claim_audit_task", {"package_dir": "audit", "task_id": "book-architecture"}, root)
            call_tool("submit_audit_report", {
                "package_dir": "audit", "task_id": "book-architecture",
                "report_markdown": complete_report("book-architecture"),
            }, root)
            coverage = json.loads(call_tool("verify_audit_coverage", {"package_dir": "audit"}, root)["content"][0]["text"])
            self.assertTrue(coverage["ready_for_reconciliation"])

    def test_submit_rejects_a_blocked_receipt(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("正文。" * 1200, encoding="utf-8")
            call_tool(
                "plan_long_form_audit",
                {"draft_path": "draft.md", "output_dir": "audit", "style": "fiction", "chunk_size": 2000},
                root,
            )
            with self.assertRaisesRegex(ValueError, "coverage is blocked"):
                call_tool(
                    "submit_audit_report",
                    {
                        "package_dir": "audit",
                        "task_id": "baseline",
                        "report_markdown": complete_report("baseline").replace(
                            "Coverage: complete", "Coverage: blocked"
                        ),
                    },
                    root,
                )

    def test_tampered_task_report_path_cannot_leave_audit_package(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            draft = root / "draft.md"
            draft.write_text("正文。" * 1200, encoding="utf-8")
            call_tool(
                "plan_long_form_audit",
                {"draft_path": "draft.md", "output_dir": "audit", "style": "fiction", "chunk_size": 2000},
                root,
            )
            plan_path = root / "audit" / "agent-plan.json"
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["tasks"][0]["report"] = "../outside.md"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "within the audit package"):
                call_tool("list_audit_tasks", {"package_dir": "audit"}, root)

    def test_http_transport_requires_bearer_token_and_serves_mcp(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            server = ThreadingHTTPServer(("127.0.0.1", 0), _http_handler(root, "test-token"))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            port = server.server_address[1]
            payload = json.dumps(
                {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
            ).encode("utf-8")
            request = Request(
                f"http://127.0.0.1:{port}/mcp",
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer test-token",
                },
                method="POST",
            )
            try:
                with urlopen(request, timeout=5) as response:
                    received = json.loads(response.read())
            finally:
                server.shutdown()
                server.server_close()
                thread.join(timeout=5)

        self.assertEqual(received["result"]["serverInfo"]["name"], "advanced-human-writing")


if __name__ == "__main__":
    unittest.main()
