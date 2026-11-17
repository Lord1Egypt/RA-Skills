import json
import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from humanwriting.cli import main
from humanwriting.compiler import compile_prompt, compile_audit_prompt
from humanwriting.evaluation import EDITORIAL_DIMENSIONS, evaluate_editorial_cases
from humanwriting.mcp_server import call_tool
from humanwriting.pipeline import build_audit_pipeline
from humanwriting.review import compile_critique_prompt, prepare_blind_comparison
from humanwriting.statistics import analyze_style_statistics


class GenerationQualityTests(unittest.TestCase):
    def test_default_generation_covers_all_genres_without_full_audits(self):
        for style in ("fiction", "webnovel", "self-media", "academic-paper", "formal-document", "news-report", "argumentative"):
            prompt = compile_prompt(style, "Write the requested passage.")
            self.assertEqual(prompt.count("# Technique Module: generation-quality"), 1)
            self.assertIn("Genre-Specific Generation Brief", prompt)
            self.assertNotIn("Technique Module: earned-ending-audit", prompt)
            self.assertNotIn("Technique Module: formulaic-structure-audit", prompt)
            if style not in {"fiction", "webnovel"}:
                self.assertIn("Do not invent personal experience", prompt)
                self.assertNotIn("Advance the scene through", prompt)

    def test_original_activates_preservation_but_new_draft_does_not(self):
        rewrite = compile_prompt("self-media", "Polish this.", original_text="Maybe. I am still unsure.")
        self.assertIn("Technique Module: voice-ambiguity-preservation", rewrite)
        self.assertNotIn("Technique Module: voice-ambiguity-preservation", compile_prompt("self-media", "Write an article."))

    def test_factual_self_media_sources_reach_generation_audit_and_pipeline(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "source.md"
            draft = Path(directory) / "draft.md"
            source.write_text("The device lasted six hours in the supplied test.", encoding="utf-8")
            draft.write_text("The battery lasted six hours.", encoding="utf-8")
            sources = [str(source)]
            prompt = compile_prompt("self-media", "Write a product review.", source_paths=sources)
            self.assertIn("Supplied Factual Sources", prompt)
            audit = compile_audit_prompt(str(draft), document_type="self-media", profiles=["sources"], source_paths=sources)
            self.assertIn("Audit Module: source-grounding", audit)
            stages, _ = build_audit_pipeline(str(draft), document_type="self-media", source_paths=sources, auto=True)
            self.assertIn("sources", [stage.profile for stage in stages])
            self.assertNotIn("Supplied Factual Sources", compile_prompt("fiction", "Write a scene.", source_paths=sources))

    def test_mcp_generation_and_diagnosis(self):
        with TemporaryDirectory() as directory:
            result = call_tool("compile_generation_prompt", {"style": "fiction", "task": "写一个重逢场景。"}, Path(directory))
            self.assertIn("generation-quality", result["content"][0]["text"])
            result = call_tool("compile_critique_prompt", {"style": "self-media", "draft": "A plain paragraph."}, Path(directory))
            self.assertIn("Diagnosis Only", result["content"][0]["text"])

    def test_blinding_both_orders_and_diagnosis_contract(self):
        for reverse in (0, 1):
            with patch("humanwriting.review.secrets.randbelow", return_value=reverse):
                prompt, key = prepare_blind_comparison("OLD TEXT", "NEW TEXT", "self-media")
            self.assertNotIn("version_key", prompt)
            self.assertNotIn("# Original", prompt)
            self.assertIn("tie, or insufficient-evidence", prompt)
            self.assertEqual(key["A"], "candidate" if reverse else "original")
            first = prompt.split("# Version A (data)")[1].split("# Version B (data)")[0]
            self.assertIn("NEW TEXT" if reverse else "OLD TEXT", first)
        self.assertIn("Give no replacement sentences", compile_critique_prompt("text", "fiction"))

    def test_cli_blind_keeps_key_separate_and_rejects_overwrite(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            a, b = root / "old.md", root / "new.md"
            a.write_text("original", encoding="utf-8")
            b.write_text("candidate", encoding="utf-8")
            output = root / "review"
            args = ["compare-blind", "--original", str(a), "--candidate", str(b), "--style", "fiction", "--output-dir", str(output)]
            with redirect_stdout(StringIO()):
                self.assertEqual(main(args), 0)
            self.assertEqual(set(json.loads((output / "version-key.json").read_text())), {"A", "B"})
            self.assertNotIn("version-key", (output / "comparison.md").read_text())
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                main(args)

    def test_language_segmentation_and_uncovered_profile(self):
        self.assertEqual(analyze_style_statistics("The rate is 3.14 percent. Dr. Smith reported it.").sentence_count, 2)
        de = analyze_style_statistics("Das ist ein Punkt. Darüber hinaus ist die Qualität wichtig.")
        self.assertEqual(de.language, "de")
        self.assertGreater(de.transition_density_per_1000, 0)
        self.assertEqual(analyze_style_statistics("Dr. Müller prüft den Wert 3.14. Das Ergebnis ist klar.", language="de").sentence_count, 2)
        self.assertEqual(analyze_style_statistics("A short sample.", language="pt-BR").language, "pt")
        self.assertIsNone(analyze_style_statistics("Это небольшой пример.", language="ru").transition_density_per_1000)

    def test_editorial_ratings_unblind_and_preserve_disagreement(self):
        base = {dim: 2 for dim in EDITORIAL_DIMENSIONS}
        better = {dim: 3 for dim in EDITORIAL_DIMENSIONS}
        case = {"id": "zh-voice", "language": "zh", "genre": "essay", "review_status": "native-reviewed", "source_provenance": "licensed author sample", "version_key": {"A": "candidate", "B": "original"}, "ballots": [
            {"reviewer": "one", "annotation_date": "2026-10-13", "scores": {"A": better, "B": base}, "verdict": "A"},
            {"reviewer": "two", "annotation_date": "2026-10-13", "scores": {"A": base, "B": better}, "verdict": "B"},
        ]}
        with TemporaryDirectory() as directory:
            path = Path(directory) / "cases.json"
            path.write_text(json.dumps([case]), encoding="utf-8")
            row = evaluate_editorial_cases(str(path))["cases"][0]
            self.assertTrue(row["disagreement"])
            self.assertEqual(row["mean_candidate_minus_original"]["voice"], 0)
            case["ballots"] = []
            path.write_text(json.dumps([case]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "two independent"):
                evaluate_editorial_cases(str(path))
            case["review_status"] = "seed"
            path.write_text(json.dumps([case]), encoding="utf-8")
            self.assertTrue(evaluate_editorial_cases(str(path))["cases"][0]["pending"])


if __name__ == "__main__":
    unittest.main()
