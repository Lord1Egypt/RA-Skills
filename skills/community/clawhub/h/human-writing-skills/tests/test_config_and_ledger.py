import json
import os
import unittest
from types import SimpleNamespace
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.compiler import compile_humanize_prompt_text
from humanwriting.config import apply_project_defaults, load_project_config
from humanwriting.ledger import compile_ledger_extraction_prompt_text


class ConfigAndLedgerTests(unittest.TestCase):
    def test_project_config_applies_only_lightweight_defaults(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath(".humanwriting.json").write_text(
                json.dumps(
                    {
                        "style": "fiction",
                        "document_type": "fiction",
                        "context": "ledger.md",
                        "allow": ["END001"],
                    }
                ),
                encoding="utf-8",
            )
            root.joinpath("ledger.md").write_text("Confirmed fact.", encoding="utf-8")
            draft = root / "chapter.md"
            draft.write_text("A short chapter.", encoding="utf-8")

            arguments = SimpleNamespace(
                style="general",
                lint_style="general",
                document_type="auto",
                context=None,
                allow=[],
                lint_allow=[],
                draft=str(draft),
            )

            previous = Path.cwd()
            os.chdir(root)
            try:
                config = apply_project_defaults(arguments, ["lint", "--draft", str(draft)])
            finally:
                os.chdir(previous)

        self.assertIsNotNone(config)
        self.assertEqual(arguments.style, "fiction")
        self.assertEqual(arguments.document_type, "fiction")
        self.assertEqual(arguments.allow, ["END001"])
        self.assertTrue(arguments.context.endswith("ledger.md"))

    def test_project_config_parses_supported_values(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            root.joinpath(".humanwriting.json").write_text('{"style":"fiction"}', encoding="utf-8")
            self.assertEqual(load_project_config(root).values["style"], "fiction")

    def test_ledger_prompt_requires_evidence_and_preserves_unknowns(self):
        prompt = compile_ledger_extraction_prompt_text(
            "Lin leaves the blue folder on the desk and promises to return before dawn.",
            "# Existing Ledger\n\n- Lin has not returned.",
        )
        self.assertIn("observed", prompt)
        self.assertIn("inferred", prompt)
        self.assertIn("Existing Ledger Authority", prompt)
        self.assertIn("Carried Objects", prompt)

    def test_text_humanize_prompt_has_in_memory_fidelity_source(self):
        prompt = compile_humanize_prompt_text("The gate is locked.", style="fiction")
        self.assertIn("Original: supplied draft", prompt)
        self.assertIn("The gate is locked.", prompt)
