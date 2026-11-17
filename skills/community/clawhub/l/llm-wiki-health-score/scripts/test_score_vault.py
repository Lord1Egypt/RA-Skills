import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import score_vault


class ScoreVaultTests(unittest.TestCase):
    def make_file(self, root: Path, relative: str, text: str = "content") -> Path:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def make_valid_vault(self, root: Path) -> None:
        self.make_file(
            root,
            "AGENTS.md",
            "raw/ wiki/ RULES.md Core Notes CORE_RELATIONSHIPS_V1",
        )
        self.make_file(
            root,
            "RULES.md",
            "raw/ wiki/ index.md log.md 核心文件索引.md CORE_RELATIONSHIPS_V1",
        )
        self.make_file(root, "index.md", "[[wiki/Topic]]")
        self.make_file(root, "log.md", "2026-08-10 audit")
        self.make_file(root, "核心文件索引.md", "[[wiki/Topic]]")
        self.make_file(root, "raw/source.pdf", "pdf bytes")
        self.make_file(
            root,
            "raw/source.pdf.core.md",
            "<!-- CORE_FILE_NOTE_V1 -->\n<!-- CORE_AUTO_SUMMARY_V1:START -->",
        )
        self.make_file(
            root,
            "wiki/Topic.md",
            "---\ndoc_role: result\ndoc_status: active\n---\n[[raw/source.pdf.core]]\n",
        )

    def test_non_llm_wiki_layout_is_scored_as_low_architecture_fit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_file(root, "notes.md", "plain notes")

            result = score_vault.score_vault(root)

        self.assertEqual(result["status"], "needs_semantic_sampling")
        self.assertIsNone(result["score"])
        self.assertFalse(result["architecture_assessment"]["karpathy_core_present"])
        self.assertIn("llm_wiki_architecture_fit", result["dimensions"])
        self.assertLess(result["dimensions"]["llm_wiki_architecture_fit"]["structural_score"], 40)

    def test_index_and_machine_index_are_optional_navigation_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_file(
                root,
                "AGENTS.md",
                "raw/ wiki/ RULES.md Core Notes CORE_RELATIONSHIPS_V1",
            )
            self.make_file(
                root,
                "RULES.md",
                "raw/ wiki/ log.md CORE_RELATIONSHIPS_V1 取信 验证 validate",
            )
            self.make_file(root, "log.md", "2026-08-10 audit")
            self.make_file(root, "raw/source.md", "source content")
            self.make_file(
                root,
                "wiki/Topic.md",
                "---\ndoc_role: result\ndoc_status: active\n---\n[[raw/source]]\n",
            )

            result = score_vault.score_vault(root)

        check_map = {item["id"]: item for item in result["architecture_assessment"]["checks"]}
        self.assertEqual(result["status"], "needs_semantic_sampling")
        self.assertFalse(check_map["human_entry_index_present"]["passed"])
        self.assertFalse(check_map["machine_index_present"]["passed"])
        self.assertFalse(check_map["human_entry_index_present"]["blocking"])
        self.assertFalse(check_map["machine_index_present"]["blocking"])

    def test_score_vault_scores_valid_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)

            result = score_vault.score_vault(root)

        self.assertEqual(result["status"], "needs_semantic_sampling")
        self.assertIsNone(result["score"])
        self.assertTrue(result["architecture_assessment"]["karpathy_core_present"])
        self.assertIn("schema_governance_quality", result["dimensions"])
        self.assertIn("knowledge_sedimentation_effectiveness", result["dimensions"])

    def test_cli_json_output_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)

            text = score_vault.render_report(score_vault.score_vault(root), "json")
            parsed = json.loads(text)

        self.assertEqual(parsed["status"], "needs_semantic_sampling")

    def test_default_artifact_paths_are_under_scored_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            resolved_root = root.resolve()

            paths = score_vault.default_artifact_paths(root, "markdown", tool_name="workbuddy")
            custom_paths = score_vault.default_artifact_paths(root, "json", tool_name="codex")

        self.assertEqual(
            paths["artifact_dir"],
            resolved_root / ".workbuddy" / "llm-wiki-health",
        )
        self.assertEqual(
            paths["report"],
            resolved_root / ".workbuddy" / "llm-wiki-health" / "llm-wiki-health-report.md",
        )
        self.assertEqual(
            paths["semantic_template"],
            resolved_root / ".workbuddy" / "llm-wiki-health" / "semantic_scores.json",
        )
        self.assertEqual(
            custom_paths["report"],
            resolved_root / ".codex" / "llm-wiki-health" / "llm-wiki-health-report.json",
        )

    def test_write_report_artifact_defaults_to_scored_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            resolved_root = root.resolve()
            self.make_valid_vault(root)
            result = score_vault.score_vault(root)

            report_path = score_vault.write_report_artifact(
                result,
                "markdown",
                None,
                tool_name="workbuddy",
            )

            self.assertTrue(report_path.exists())
            self.assertEqual(
                report_path,
                resolved_root / ".workbuddy" / "llm-wiki-health" / "llm-wiki-health-report.md",
            )
            self.assertIn("LLM Wiki 知识库评分", report_path.read_text(encoding="utf-8"))

    def test_exit_code_distinguishes_failed_and_required_final_states(self):
        self.assertEqual(score_vault.exit_code_for_result({"status": "scored"}), 0)
        self.assertEqual(score_vault.exit_code_for_result({"status": "needs_semantic_sampling"}), 0)
        self.assertEqual(
            score_vault.exit_code_for_result({"status": "needs_semantic_sampling"}, require_final=True),
            4,
        )
        self.assertEqual(score_vault.exit_code_for_result({"status": "unscorable"}), 2)
        self.assertEqual(score_vault.exit_code_for_result({"status": "semantic_input_invalid"}), 3)

    def test_tool_artifact_directory_is_excluded_from_scoring(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            self.make_file(
                root,
                ".codex/llm-wiki-health/wiki/Pollution.md",
                "---\ndoc_role: result\n---\n[[raw/generated]]\n",
            )

            stats = score_vault.collect_stats(root, tool_name="codex")

        self.assertEqual(stats["wiki_markdown_count"], 1)
        self.assertNotIn(".codex/llm-wiki-health/wiki/Pollution.md", stats["latest_wiki_pages"])

    def test_maintenance_freshness_uses_dates_not_hardcoded_year(self):
        now = datetime(2027, 1, 20)

        fresh_score = score_vault.date_freshness_score("2027-01-10 audit", now=now)
        stale_score = score_vault.date_freshness_score("2026-01-10 audit", now=now)

        self.assertGreater(fresh_score, stale_score)
        self.assertEqual(score_vault.date_freshness_score("no date", now=now), 0.0)

    def test_cli_report_json_contains_artifact_paths_written_to_stdout(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            resolved_root = root.resolve()
            self.make_valid_vault(root)

            completed = subprocess.run(
                [
                    sys.executable,
                    str(Path(score_vault.__file__).resolve()),
                    "--root",
                    str(root),
                    "--format",
                    "json",
                    "--tool-name",
                    "codex",
                ],
                check=False,
                capture_output=True,
                encoding="utf-8",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )

            report_path = resolved_root / ".codex" / "llm-wiki-health" / "llm-wiki-health-report.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            stdout_result = json.loads(completed.stdout)

        self.assertEqual(completed.returncode, 0)
        self.assertEqual(report["artifacts"], stdout_result["artifacts"])
        self.assertEqual(report["artifacts"]["report"], str(report_path))
        self.assertIn("semantic_template", report["artifacts"])

    def test_generated_core_blocks_do_not_count_as_source_traceability(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            self.make_file(
                root,
                "wiki/Topic.md",
                (
                    "---\ndoc_role: result\ndoc_status: active\n---\n"
                    "正文没有来源链接。\n"
                    "<!-- CORE_RELATIONSHIPS_V1:START -->\n"
                    "- [[raw/source.pdf.core]]\n"
                    "<!-- CORE_RELATIONSHIPS_V1:END -->\n"
                ),
            )

            stats = score_vault.collect_stats(root)

        self.assertEqual(stats["wiki_pages_with_raw_links"], 0)
        self.assertEqual(stats["latest_source_backed_count"], 0)
        self.assertEqual(stats["multi_source_wiki_pages"], 0)

    def test_source_traceability_uses_recoverability_signals_beyond_sidecars(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            (root / "raw" / "source.pdf.core.md").unlink()
            self.make_file(root, "raw/extra.docx", "docx bytes")
            self.make_file(
                root,
                "raw/source-manifest.json",
                json.dumps(
                    {
                        "sources": [
                            {"path": "raw/source.pdf", "id": "source-pdf"},
                            {"path": "raw/extra.docx", "id": "extra-docx"},
                        ]
                    }
                ),
            )
            self.make_file(
                root,
                "wiki/Topic.md",
                (
                    "---\n"
                    "doc_role: result\n"
                    "doc_status: active\n"
                    "source_scope: \"raw/source.pdf; raw/extra.docx\"\n"
                    "---\n"
                    "正文引用 [[raw/source.pdf]] 和 [[raw/extra.docx]]。\n"
                ),
            )
            self.make_file(
                root,
                "核心文件索引.md",
                "[[raw/source.pdf]]\n[[raw/extra.docx]]\n",
            )
            self.make_file(root, ".external-index/state.sqlite3", "sqlite placeholder")

            stats = score_vault.collect_stats(root)
            traceability = score_vault.score_source_traceability(stats)

        self.assertEqual(stats["core_markdown_count"], 0)
        self.assertEqual(traceability["metrics"]["sidecar_score"], 0)
        self.assertGreaterEqual(traceability["metrics"]["source_recoverability_score"], 70)
        self.assertGreater(traceability["structural_score"], 50)

    def make_semantic_scores(self, score=75):
        return {
            "schema_version": "semantic-scores-v0.2",
            "dimensions": {
                "llm_wiki_architecture_fit": {
                    "score": score,
                    "criteria": {
                        "raw_wiki_schema_layering": 4,
                        "ingest_query_lint_operations": 4,
                        "agent_operationalization": 4,
                        "modularity_and_adaptability": 4,
                    },
                    "evidence": [
                        {"file": "AGENTS.md", "note": "Schema defines raw/wiki layers and operation rules."}
                    ],
                },
                "source_traceability": {
                    "score": score,
                    "criteria": {
                        "provenance_coverage": 4,
                        "claim_source_alignment": 4,
                        "citation_granularity": 3,
                        "source_recoverability": 4,
                    },
                    "evidence": [
                        {"file": "wiki/Topic.md", "note": "Wiki page links back to raw source note."}
                    ],
                },
                "schema_governance_quality": {
                    "score": score,
                    "criteria": {
                        "completeness": 4,
                        "consistency": 4,
                        "unambiguity": 4,
                        "verifiability": 4,
                        "traceability": 4,
                        "maintainability": 4,
                    },
                    "evidence": [
                        {"file": "AGENTS.md", "note": "Schema defines layer and startup rules."}
                    ],
                },
                "knowledge_sedimentation_effectiveness": {
                    "score": score,
                    "criteria": {
                        "groundedness": 3,
                        "completeness": 3,
                        "relevance_actionability": 4,
                        "coherence_readability": 4,
                        "source_integration": 3,
                        "freshness_conflict_handling": 3,
                    },
                    "samples": [
                        {
                            "file": "wiki/Topic.md",
                            "score": score,
                            "evidence": [
                                {"file": "raw/source.pdf.core.md", "note": "Wiki page links to source note."}
                            ],
                        }
                    ],
                    "evidence": [
                        {"file": "wiki/Topic.md", "note": "Latest wiki page is source-backed."}
                    ],
                },
                "retrieval_answerability": {
                    "score": score,
                    "criteria": {
                        "navigation_findability": 4,
                        "question_context_precision": 4,
                        "answer_faithfulness": 4,
                        "answer_relevance": 4,
                    },
                    "evidence": [
                        {"file": "index.md", "note": "Entry file links to the topic page."}
                    ],
                },
                "maintenance_evolution": {
                    "score": score,
                    "criteria": {
                        "logging_freshness": 4,
                        "staleness_detection": 3,
                        "conflict_handling": 3,
                        "repair_workflow": 4,
                    },
                    "evidence": [
                        {"file": "log.md", "note": "Log records the latest audit date."}
                    ],
                },
            },
        }

    def test_semantic_template_contains_all_integrated_dimensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            result = score_vault.score_vault(root)

            template = score_vault.build_semantic_score_template(result)

        self.assertEqual(template["schema_version"], "semantic-scores-v0.2")
        self.assertEqual(set(template["dimensions"]), set(score_vault.DIMENSION_WEIGHTS))
        self.assertEqual(template["dimensions"]["schema_governance_quality"]["score"], None)
        self.assertTrue(template["dimensions"]["knowledge_sedimentation_effectiveness"]["samples"])

    def test_semantic_template_references_fixed_probe_question_set(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            result = score_vault.score_vault(root)

            template = score_vault.build_semantic_score_template(result)

        skill_root = Path(score_vault.__file__).parents[1]
        self.assertTrue((skill_root / "references" / "probe_questions.md").is_file())
        self.assertEqual(
            template["score_context"]["probe_question_reference"],
            "references/probe_questions.md",
        )
        self.assertTrue(any("探针问题" in item for item in template["score_context"]["instructions"]))

    def test_semantic_scores_merge_into_final_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            structural = score_vault.score_vault(root)

            final = score_vault.apply_semantic_scores(structural, self.make_semantic_scores())

        self.assertEqual(final["score_type"], "final_integrated_semantic_sampling")
        self.assertEqual(final["semantic_input_validation"]["passed"], True)
        for name, dimension in final["dimensions"].items():
            expected = round(
                structural["dimensions"][name]["structural_score"]
                * score_vault.SEMANTIC_BLEND_WEIGHTS[name]["structural"]
                + 75 * score_vault.SEMANTIC_BLEND_WEIGHTS[name]["semantic"],
                2,
            )
            self.assertEqual(dimension["score"], expected)
        self.assertIsInstance(final["score"], (int, float))

    def test_invalid_semantic_scores_do_not_finalize(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            structural = score_vault.score_vault(root)
            invalid = self.make_semantic_scores()
            invalid["dimensions"]["schema_governance_quality"]["evidence"] = []

            with self.assertRaises(score_vault.SemanticScoreError):
                score_vault.apply_semantic_scores(structural, invalid)

    def test_semantic_dimension_score_must_match_criteria_average(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            structural = score_vault.score_vault(root)
            invalid = self.make_semantic_scores(score=95)
            invalid["dimensions"]["source_traceability"]["criteria"] = {
                "provenance_coverage": 1,
                "claim_source_alignment": 1,
                "citation_granularity": 1,
                "source_recoverability": 1,
            }

            with self.assertRaises(score_vault.SemanticScoreError) as context:
                score_vault.apply_semantic_scores(structural, invalid)

        self.assertIn("criteria average", str(context.exception))

    def test_structural_semantic_divergence_adds_review_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            structural = score_vault.score_vault(root)
            semantic = self.make_semantic_scores(score=75)
            semantic["dimensions"]["llm_wiki_architecture_fit"]["score"] = 0
            semantic["dimensions"]["llm_wiki_architecture_fit"]["criteria"] = {
                "raw_wiki_schema_layering": 0,
                "ingest_query_lint_operations": 0,
                "agent_operationalization": 0,
                "modularity_and_adaptability": 0,
            }

            final = score_vault.apply_semantic_scores(structural, semantic)

        warnings = final["dimensions"]["llm_wiki_architecture_fit"].get("review_warnings", [])
        self.assertTrue(warnings)
        self.assertIn("llm_wiki_architecture_fit", final["semantic_input_validation"]["review_warnings"])

    def test_wikilink_resolution_detects_ambiguous_stem_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            self.make_file(root, "wiki/A/Decision.md", "---\ndoc_role: result\n---\nA")
            self.make_file(root, "wiki/B/Decision.md", "---\ndoc_role: result\n---\nB")
            self.make_file(root, "wiki/Topic.md", "---\ndoc_role: result\n---\n[[Decision]]\n")

            stats = score_vault.collect_stats(root)

        self.assertEqual(stats["ambiguous_wiki_links"], 1)
        self.assertEqual(stats["dangling_wiki_links"], 0)

    def test_wikilink_resolution_prefers_exact_relative_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_vault(root)
            self.make_file(root, "wiki/A/Decision.md", "---\ndoc_role: result\n---\nA")
            self.make_file(root, "wiki/B/Decision.md", "---\ndoc_role: result\n---\nB")
            self.make_file(root, "wiki/Topic.md", "---\ndoc_role: result\n---\n[[wiki/A/Decision]]\n")

            stats = score_vault.collect_stats(root)

        self.assertEqual(stats["ambiguous_wiki_links"], 0)
        self.assertEqual(stats["dangling_wiki_links"], 0)


if __name__ == "__main__":
    unittest.main()
