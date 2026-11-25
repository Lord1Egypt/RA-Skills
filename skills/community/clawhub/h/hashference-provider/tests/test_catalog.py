import importlib.util
import json
import contextlib
import io
from unittest.mock import patch
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("catalog", ROOT / "scripts/catalog.py")
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((ROOT / "references/catalog-snapshot.json").read_text())
        cls.rows = c.rows_from(cls.payload)

    def test_shapes(self):
        self.assertEqual(c.rows_from(self.rows), self.rows)
        self.assertEqual(c.rows_from({"models": self.rows}), self.rows)

    def test_invalid_catalog(self):
        for value in [None, {}, [], {"data": "bad"}, [{"id": ""}], [self.rows[0], self.rows[0]]]:
            with self.subTest(value=type(value).__name__), self.assertRaises(ValueError):
                c.rows_from(value)

    def test_snapshot_inventory(self):
        self.assertEqual(len(self.rows), 123)
        self.assertEqual(len(c.select(self.rows)), 62)
        self.assertEqual(sum(bool(r.get("same_model_as")) for r in self.rows), 61)

    def test_aliases(self):
        self.assertEqual(len(c.select(self.rows, aliases=True)), 123)
        self.assertTrue(all(not r.get("same_model_as") for r in c.select(self.rows)))

    def test_endpoint_not_protocol(self):
        row = next(r for r in self.rows if r.get("protocol") == "responses")
        self.assertEqual(c.select([row], transport="chat"), [row])
        chat = next(r for r in self.rows if r["id"] == "hashference-glm-5-3")
        with self.assertRaises(ValueError):
            c.select([chat], transport="responses")

    def test_tool_filter(self):
        self.assertTrue(all(r["supports_tools"] is True for r in c.select(self.rows, agents_only=True)))
        row = dict(self.rows[0], supports_tools=False)
        self.assertEqual(len(c.select([row])), 1)
        with self.assertRaises(ValueError):
            c.select([row], agents_only=True)

    def test_missing_id_is_error(self):
        with self.assertRaises(ValueError):
            c.select(self.rows, ids=["invented-model"])

    def test_ids_verbatim(self):
        rows = c.select(self.rows, ids=["glm-5-3-flash-uncensored"])
        self.assertEqual(c.model_config(rows[0], "chat")["id"], "glm-5-3-flash-uncensored")

    def test_usd_conversion(self):
        row = next(r for r in self.rows if r["id"] == "hashference-glm-5-3")
        cfg = c.model_config(row, "chat")
        self.assertEqual(cfg["cost"]["input"], 0.441)
        self.assertEqual(cfg["cost"]["output"], 1.386)
        self.assertNotIn("cacheWrite", cfg["cost"])

    def test_input_and_output_budget(self):
        for r in c.select(self.rows):
            cfg = c.model_config(r, "chat")
            self.assertLessEqual(cfg["maxTokens"], r["max_output_tokens"])
            self.assertLessEqual(cfg["contextWindow"], r["context_length"])
            if "max_input_tokens" in r:
                self.assertLessEqual(cfg["contextWindow"] - cfg["maxTokens"], r["max_input_tokens"])

    def test_missing_limits_not_guessed(self):
        for field in ["context_length", "default_max_output_tokens", "max_output_tokens"]:
            row = dict(self.rows[0]); row.pop(field)
            with self.assertRaises(ValueError):
                c.model_config(row, "chat")

    def test_transport_export(self):
        for transport in c.ENDPOINTS:
            rows = c.select(self.rows, transport=transport, aliases=True)
            cfgs = json.loads(c.render(rows, "openclaw", transport))
            self.assertEqual({x["api"] for x in cfgs}, {c.APIS[transport]})
            self.assertEqual(len(cfgs), len(rows))

    def test_raw_metadata_retained(self):
        row = next(r for r in self.rows if r.get("promotion"))
        self.assertEqual(json.loads(c.render([row], "json", "chat"))[0], row)

    def test_markdown_escape(self):
        row = dict(self.rows[0], name="unsafe|table")
        self.assertIn("unsafe" + chr(92) + "|table", c.render([row], "markdown", "chat"))

    def run_cli(self, args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            c.main(args)
        return stdout.getvalue(), stderr.getvalue()

    def test_cli_offline_stdout(self):
        out, err = self.run_cli(["--input", str(ROOT / "references/catalog-snapshot.json"), "--format", "openclaw", "--agents-only"])
        self.assertGreater(len(json.loads(out)), 0)
        self.assertIn("live catalog entries selected", err)

    def assert_output_rejected(self, target):
        with patch.object(c.urllib.request, "urlopen") as network:
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as stopped:
                    c.main(["--output", str(target)])
            self.assertEqual(stopped.exception.code, 2)
            network.assert_not_called()

    def test_missing_config_output_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "openclaw.json"
            self.assert_output_rejected(target)
            self.assertFalse(target.exists())

    def test_existing_config_output_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "openclaw.json"
            target.write_text('{"preserve":true}')
            self.assert_output_rejected(target)
            self.assertEqual(target.read_text(), '{"preserve":true}')

    def test_directory_symlink_output_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "config"
            config.mkdir()
            link = root / "artifact-link"
            link.symlink_to(config, target_is_directory=True)
            self.assert_output_rejected(link / "openclaw.json")
            self.assertFalse((config / "openclaw.json").exists())

    def test_output_abbreviation_also_rejected(self):
        self.assert_output_rejected("ignored.json")
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as stopped:
                c.main(["--out", "ignored.json"])
        self.assertEqual(stopped.exception.code, 2)

    def test_no_write_mode_in_helper(self):
        import ast
        tree = ast.parse((ROOT / "scripts/catalog.py").read_text())
        forbidden = {"write_text", "write_bytes", "touch", "mkdir", "unlink", "rename", "replace", "symlink_to"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                # str.replace is used only for Markdown escaping, not Path mutation.
                if node.func.attr == "replace":
                    continue
                self.assertNotIn(node.func.attr, forbidden)
                self.assertNotEqual(node.func.attr, "open")



if __name__ == "__main__":
    unittest.main()
