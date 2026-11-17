import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from humanwriting.compiler import compile_audit_prompt, compile_prompt
from humanwriting.pipeline import build_audit_pipeline
from humanwriting.protection import (
    build_protection_manifest,
    compare_protected_content,
    extract_protected_items,
    detect_serious_document,
)


class ProtectionTests(unittest.TestCase):
    def test_extracts_numbers_citations_urls_code_and_terms(self):
        text = "API Accuracy was 92.4% [12]. See https://example.com and run `train.py`."
        items = extract_protected_items(text, terms=["Accuracy"])
        kinds = {item.kind for item in items}
        self.assertTrue(
            {"number", "citation", "url", "inline-code", "named-term", "explicit-term"}
            <= kinds
        )
        values = {(item.kind, item.value) for item in items}
        self.assertNotIn(("number", "12"), values)

    def test_verification_fails_when_fact_or_citation_changes(self):
        source = "Accuracy was 92.4% [12]."
        candidate = "Accuracy was 94.2% [13]."
        report = compare_protected_content(source, candidate)
        self.assertFalse(report.ok)
        missing_values = {item.value for item in report.missing_or_changed}
        self.assertIn("92.4%", missing_values)
        self.assertIn("[12]", missing_values)
        self.assertIn("94.2%", {item.value for item in report.added})

    def test_verification_passes_when_surrounding_prose_changes(self):
        source = "The result was 92.4% [12], which is important."
        candidate = "The measured accuracy remained 92.4% [12]."
        report = compare_protected_content(source, candidate)
        self.assertTrue(report.ok)

    def test_verification_fails_when_candidate_invents_protected_value(self):
        report = compare_protected_content("No measured value.", "The value was 17.2%.")
        self.assertFalse(report.ok)
        self.assertIn("17.2%", {item.value for item in report.added})

    def test_manifest_lists_explicit_term_even_before_generation(self):
        manifest = build_protection_manifest("", terms=["Salt Office"])
        self.assertIn("Salt Office", manifest)

    def test_build_and_audit_activate_protection_only_when_requested(self):
        plain = compile_prompt("fiction", "Write the next scene.")
        protected = compile_prompt(
            "fiction",
            "Write the next scene.",
            protect_terms=["Salt Office"],
        )
        self.assertNotIn("Technique Module: protected-content", plain)
        self.assertIn("Technique Module: protected-content", protected)
        self.assertIn("Salt Office", protected)

        with TemporaryDirectory() as directory:
            draft = Path(directory) / "draft.md"
            draft.write_text("Accuracy was 92.4% [12].", encoding="utf-8")
            audit = compile_audit_prompt(
                str(draft),
                profiles=["proofread"],
                protect_content=True,
            )
        self.assertIn("Audit Module: protected-content", audit)
        self.assertIn("Protected Content Manifest", audit)
        self.assertIn("92.4%", audit)
        self.assertIn("[12]", audit)

    def test_serious_styles_auto_activate_but_narrative_styles_do_not(self):
        academic = compile_prompt("academic-paper", "Write the results section with 92.4% accuracy.")
        formal = compile_prompt("formal-document", "Write an official notice with a deadline.")
        news = compile_prompt("news-report", "Write a report using the supplied figures.")
        fiction = compile_prompt("fiction", "He moved three centimeters and counted seven seconds.")
        legal_fiction = compile_prompt("fiction", "写一篇以合同纠纷为背景的法律题材小说。")

        self.assertIn("Technique Module: protected-content", academic)
        self.assertIn("Technique Module: protected-content", formal)
        self.assertIn("Technique Module: protected-content", news)
        self.assertNotIn("Technique Module: protected-content", fiction)
        self.assertNotIn("Technique Module: protected-content", legal_fiction)

    def test_auto_detection_requires_combined_serious_document_evidence(self):
        self.assertFalse(detect_serious_document("她走了3厘米。结束。", "auto")[0])
        self.assertTrue(
            detect_serious_document("研究结果见文献[12]，样本量为300。", "auto")[0]
        )
        self.assertTrue(
            detect_serious_document("第1条 本合同由甲方与乙方签订，违约责任如下。", "auto")[0]
        )
        self.assertTrue(
            detect_serious_document("API endpoint 的 request 参数见 `schema.json`。", "auto")[0]
        )

    def test_multilingual_serious_detection_requires_multiple_cues(self):
        samples = {
            "fr": ("Cette étude présente les résultats [1].", "Elle lut les résultats [1] et ferma le livre."),
            "es": ("Esta investigación presenta los resultados [1].", "Leyó los resultados [1] y cerró el libro."),
            "pt": ("Esta pesquisa apresenta os resultados [1].", "Ela leu os resultados [1] e fechou o livro."),
            "ja": ("本研究の結果を報告する。[1]", "彼女は結果[1]を読んで、本を閉じた。"),
            "ar": ("تقدم هذه الدراسة نتائج البحث [1].", "قرأت نتائج [1] ثم أغلقت الكتاب."),
        }
        for language, (serious, narrative) in samples.items():
            with self.subTest(language=language):
                self.assertTrue(detect_serious_document(serious, "auto")[0])
                self.assertFalse(detect_serious_document(narrative, "auto")[0])
                self.assertFalse(detect_serious_document(serious, "fiction")[0])
        self.assertFalse(detect_serious_document("她反复读着结果，结果，结果[1]。", "auto")[0])

    def test_audit_auto_protection_respects_document_type_override(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            legal = root / "legal.md"
            casual = root / "casual.md"
            legal.write_text("第1条 本合同由甲方与乙方签订，违约责任如下。", encoding="utf-8")
            casual.write_text("她向前走了3厘米，又退回来。", encoding="utf-8")
            legal_prompt = compile_audit_prompt(str(legal), profiles=["proofread"])
            casual_prompt = compile_audit_prompt(str(casual), profiles=["proofread"])
            suppressed = compile_audit_prompt(
                str(legal), profiles=["proofread"], document_type="fiction"
            )

        self.assertIn("Audit Module: protected-content", legal_prompt)
        self.assertNotIn("Audit Module: protected-content", casual_prompt)
        self.assertNotIn("Audit Module: protected-content", suppressed)

    def test_pipeline_auto_protection_is_loaded_once_to_save_tokens(self):
        with TemporaryDirectory() as directory:
            draft = Path(directory) / "legal.md"
            draft.write_text("第1条 本合同由甲方与乙方签订，违约责任如下。", encoding="utf-8")
            stages, _ = build_audit_pipeline(
                str(draft), stages=["logic", "proofread"]
            )
            explicit_stages, _ = build_audit_pipeline(
                str(draft), stages=["logic", "proofread"], protect_content=True
            )
            single_stage, _ = build_audit_pipeline(str(draft), stages=["logic"])

        prompts = {stage.profile: stage.prompt for stage in stages}
        explicit_prompts = {stage.profile: stage.prompt for stage in explicit_stages}
        self.assertNotIn("Audit Module: protected-content", prompts["logic"])
        self.assertIn("Audit Module: protected-content", prompts["proofread"])
        self.assertIn("Audit Module: protected-content", explicit_prompts["logic"])
        self.assertIn("Audit Module: protected-content", explicit_prompts["proofread"])
        self.assertIn("Audit Module: protected-content", single_stage[0].prompt)


if __name__ == "__main__":
    unittest.main()
