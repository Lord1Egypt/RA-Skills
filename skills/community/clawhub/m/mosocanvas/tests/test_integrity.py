from __future__ import annotations

from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_script(name: str, *args: Path | str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *(str(arg) for arg in args)],
        text=True,
        capture_output=True,
        check=False,
    )


class EvidenceRegistryTests(unittest.TestCase):
    def test_registry_detects_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / "artifact.txt"
            artifact.write_text("approved", encoding="utf-8")
            registry = root / "registry.json"
            write_json(registry, {
                "schema": "moso.evidence-registry/0.1",
                "id": "registry",
                "created_at": "2026-07-28T00:00:00Z",
                "entries": [{
                    "id": "artifact",
                    "kind": "artifact",
                    "content_ref": "artifact.txt",
                    "sha256": sha256(artifact),
                    "size_bytes": artifact.stat().st_size,
                    "media_type": "text/plain",
                    "created_at": "2026-07-28T00:00:00Z"
                }]
            })
            self.assertEqual(run_script("evidence_validate.py", registry).returncode, 0)
            artifact.write_text("tampered", encoding="utf-8")
            result = run_script("evidence_validate.py", registry)
            self.assertEqual(result.returncode, 1)
            self.assertIn("mismatch", result.stdout)

    def test_fake_accept_without_registry_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory) / "run-state.json"
            write_json(state, {
                "schema": "moso.run-state/0.4",
                "task_id": "fake-accept",
                "mode": "direction",
                "phase": "accept",
                "spec_ref": "fake-spec",
                "shot_plan_ref": "fake-shot",
                "approved_checkpoint": {"source_ref": "fake", "role": "none"},
                "allowed_changes": [],
                "protected_elements": [],
                "attempt_budget": {
                    "generative": 0, "repair": 0,
                    "generative_used": 0, "repair_used": 0
                },
                "output_requirements": {"carrier": "social", "frame_count": 1},
                "verification": [{
                    "check": "claimed", "method": "assertion", "status": "pass"
                }],
                "direction_approval_status": "not-required",
                "quality_status": {
                    "use_scale": "pass",
                    "detail_scale": "not-required",
                    "protected_drift": "none",
                    "trajectory": "stable",
                    "independent_review": "pass",
                    "user_acceptance": "accepted"
                },
                "release_review_ref": "fake-review"
            })
            result = run_script("preflight_validate.py", state)
            self.assertEqual(result.returncode, 1)
            self.assertIn("user_decision_ref", result.stdout)
            self.assertIn("local evidence registry", result.stdout)


class ReviewIntegrityTests(unittest.TestCase):
    def finding(self, category: str) -> dict[str, object]:
        return {
            "severity": 0,
            "claim": f"{category} passed the recorded inspection",
            "evidence_region": "full frame",
            "consequence": "no release blocker observed",
            "confidence": "high",
        }

    def build_authorized_review(self, root: Path) -> tuple[Path, Path]:
        artifact = root / "artifact.svg"
        artifact.write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
            '<rect width="10" height="10" fill="#111"/></svg>',
            encoding="utf-8",
        )
        spec = root / "spec.json"
        write_json(spec, {"schema": "moso.visual-spec/0.2", "id": "spec"})
        session = root / "session.json"
        write_json(session, {
            "schema": "moso.review-session/0.1",
            "id": "session",
            "artifact_ref": "artifact",
            "reviewer_id": "reviewer-1",
            "reviewer_kind": "fresh-context-agent",
            "generation_context_id": "generation-context",
            "review_context_id": "review-context",
            "prompt_hidden": True,
            "source_hidden": True,
            "started_at": "2026-07-28T00:00:00Z",
            "committed_at": "2026-07-28T00:10:00Z",
        })
        review = root / "review.json"
        categories = (
            "carrier", "composition", "narrative", "color_light",
            "material_physics", "ai_residue", "spec_fit",
        )
        write_json(review, {
            "schema": "moso.artifact-review/0.1",
            "id": "review",
            "artifact_ref": "artifact",
            "artifact_sha256": sha256(artifact),
            "spec_ref": "spec",
            "reviewer": {
                "kind": "fresh-context-agent",
                "independent_from_generation": True,
                "actual_artifact_inspected": True,
                "reviewed_at": "2026-07-28T00:10:01Z",
                "identity_ref": "reviewer-1",
                "session_ref": "session",
            },
            "blind_pass": {
                "prompt_hidden": True,
                "first_read": "A dark square.",
                "eye_path": ["center", "edge"],
                "inferred_narrative": "Deliberately minimal.",
                "observed_anomalies": [],
            },
            "spec_pass": {
                category: [self.finding(category)] for category in categories
            },
            "decision": {
                "recommendation": "accept",
                "release_authorized": True,
                "priority_improvement": "Preserve the verified restraint.",
                "remaining_risks": [],
            },
        })
        registry = root / "registry.json"
        entries = []
        for entry_id, kind, path, media_type in (
            ("artifact", "artifact", artifact, "image/svg+xml"),
            ("spec", "visual-spec", spec, "application/json"),
            ("session", "review-session", session, "application/json"),
            ("review", "artifact-review", review, "application/json"),
        ):
            entries.append({
                "id": entry_id,
                "kind": kind,
                "content_ref": path.name,
                "sha256": sha256(path),
                "size_bytes": path.stat().st_size,
                "media_type": media_type,
                "created_at": "2026-07-28T00:10:01Z",
            })
        write_json(registry, {
            "schema": "moso.evidence-registry/0.1",
            "id": "registry",
            "created_at": "2026-07-28T00:10:01Z",
            "entries": entries,
        })
        return review, registry

    def test_authorized_review_requires_registry_and_session_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            review, _ = self.build_authorized_review(Path(directory))
            result = run_script("review_validate.py", review)
            self.assertEqual(result.returncode, 1)
            self.assertIn("requires an evidence registry", result.stdout)

    def test_evidence_bound_authorized_review_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            review, registry = self.build_authorized_review(Path(directory))
            result = run_script(
                "review_validate.py", review, "--registry", registry
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_same_context_review_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review, registry = self.build_authorized_review(root)
            session = root / "session.json"
            session_value = json.loads(session.read_text(encoding="utf-8"))
            session_value["review_context_id"] = session_value["generation_context_id"]
            write_json(session, session_value)
            registry_value = json.loads(registry.read_text(encoding="utf-8"))
            session_entry = next(
                entry for entry in registry_value["entries"]
                if entry["id"] == "session"
            )
            session_entry["sha256"] = sha256(session)
            session_entry["size_bytes"] = session.stat().st_size
            write_json(registry, registry_value)
            result = run_script(
                "review_validate.py", review, "--registry", registry
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("review context must differ", result.stdout)

    def test_complete_evidence_bound_accept_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review, registry = self.build_authorized_review(root)
            prompt = root / "prompt.txt"
            prompt.write_text("A deliberately minimal dark square.", encoding="utf-8")
            proof = root / "proof.svg"
            proof.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
                '<rect width="10" height="10" fill="#000"/></svg>',
                encoding="utf-8",
            )
            shot = root / "shot.json"
            write_json(shot, {
                "schema": "moso.shot-plan/0.2",
                "id": "shot",
                "selection": {
                    "status": "selected",
                    "proof_type": "mass-map",
                    "proof_ref": "proof",
                },
            })
            decision = root / "decision.json"
            write_json(decision, {
                "schema": "moso.user-decision/0.1",
                "id": "decision",
                "task_id": "task",
                "artifact_ref": "artifact",
                "decision": "accepted",
                "decided_at": "2026-07-28T00:11:00Z",
                "actor": "user",
            })
            self_review = root / "self-review.json"
            self_review_value = json.loads(review.read_text(encoding="utf-8"))
            self_review_value["id"] = "self-review"
            self_review_value.pop("artifact_sha256", None)
            self_review_value["reviewer"] = {
                "kind": "same-context-assistive",
                "independent_from_generation": False,
                "actual_artifact_inspected": True,
                "reviewed_at": "2026-07-28T00:05:00Z",
            }
            self_review_value["decision"] = {
                "recommendation": "user-judgment",
                "release_authorized": False,
                "priority_improvement": "Send to an independent reviewer.",
                "remaining_risks": [],
            }
            write_json(self_review, self_review_value)
            registry_value = json.loads(registry.read_text(encoding="utf-8"))
            for entry_id, kind, path, media_type in (
                ("prompt", "prompt", prompt, "text/plain"),
                ("proof", "composition-proof", proof, "image/svg+xml"),
                ("shot", "shot-plan", shot, "application/json"),
                ("decision", "user-decision", decision, "application/json"),
                ("self-review", "artifact-review", self_review, "application/json"),
            ):
                registry_value["entries"].append({
                    "id": entry_id,
                    "kind": kind,
                    "content_ref": path.name,
                    "sha256": sha256(path),
                    "size_bytes": path.stat().st_size,
                    "media_type": media_type,
                    "created_at": "2026-07-28T00:11:00Z",
                })
            write_json(registry, registry_value)

            state = root / "run-state.json"
            write_json(state, {
                "schema": "moso.run-state/0.4",
                "task_id": "task",
                "mode": "direction",
                "phase": "accept",
                "spec_ref": "spec",
                "shot_plan_ref": "shot",
                "approved_checkpoint": {"role": "none"},
                "allowed_changes": [],
                "protected_elements": [],
                "attempt_budget": {
                    "generative": 1,
                    "generative_used": 1,
                    "repair": 0,
                    "repair_used": 0,
                },
                "output_requirements": {
                    "carrier": "social image",
                    "frame_count": 1,
                },
                "verification": [{
                    "check": "artifact-bound review",
                    "method": "registered evidence",
                    "status": "pass",
                }],
                "direction_approval_status": "approved",
                "generation_attempts": [{
                    "id": "attempt-1",
                    "status": "reviewed",
                    "pre_generation_brief": {
                        "objective": "Produce the selected shot.",
                        "viewer_position": "front",
                        "first_read": "dark square",
                        "composition_geometry": "centered mass",
                        "narrative_beat": "minimal interruption",
                        "color_light_logic": "single low-key value",
                        "required_content": ["dark square"],
                        "protected_content": [],
                        "main_risk": "empty rather than deliberate",
                        "communicated_to_user": True,
                    },
                    "execution": {
                        "backend": "test",
                        "interface": "fixture",
                        "model": "fixture-model",
                        "model_version": "1",
                        "prompt_ref": "prompt",
                        "prompt_sha256": sha256(prompt),
                        "parameters": {},
                        "generated_at": "2026-07-28T00:00:00Z",
                        "output_ref": "artifact",
                    },
                    "self_review_ref": "self-review",
                    "independent_review_ref": "review",
                }],
                "quality_status": {
                    "use_scale": "pass",
                    "detail_scale": "pass",
                    "protected_drift": "none",
                    "trajectory": "improved",
                    "independent_review": "pass",
                    "user_acceptance": "accepted",
                },
                "release_review_ref": "review",
                "user_decision_ref": "decision",
            })
            result = run_script(
                "preflight_validate.py", state, "--registry", registry
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class TrendIntegrityTests(unittest.TestCase):
    def build_snapshot(self, root: Path) -> Path:
        snapshot = root / "trend.json"
        sources = []
        source_data = (
            ("source-1", "https://curated.example/a", "Curated A", "curated-showcase"),
            ("source-2", "https://portfolio.example/b", "Studio B", "practitioner-portfolio"),
            ("source-3", "https://editorial.example/c", "Report C", "editorial-trend-report"),
        )
        for source_id, url, creator, source_class in source_data:
            sources.append({
                "id": source_id,
                "url": url,
                "platform": url.split("//", 1)[1].split("/", 1)[0],
                "source_class": source_class,
                "observed_at": "2026-07-27T00:00:00Z",
                "captured_at": "2026-07-28T00:00:00Z",
                "creator_or_project": creator,
                "evidence_type": "curated",
            })
        write_json(snapshot, {
            "schema": "moso.trend-snapshot/0.2",
            "id": "trend",
            "captured_at": "2026-07-28T00:00:00Z",
            "expires_at": "2026-07-29T00:00:00Z",
            "scope": "visual design",
            "collection": {
                "collector_id": "collector",
                "collector_context_id": "collection-context",
                "query_terms": ["editorial image systems"],
                "source_classes_requested": [
                    "curated-showcase",
                    "practitioner-portfolio",
                    "editorial-trend-report",
                ],
                "status": "complete",
            },
            "baseline": {
                "window_days": 7,
                "prior_snapshot_refs": ["trend-minus-1", "trend-minus-2"],
            },
            "sources": sources,
            "signals": [{
                "id": "signal",
                "mechanism": "asymmetric negative space with small factual interruptions",
                "source_ids": ["source-1", "source-2", "source-3"],
                "velocity": "rising",
                "velocity_evidence": "Recurrence increased across two prior snapshots.",
                "curation": "strong",
                "recurrence": "cross-source",
                "novelty": "medium",
                "relevance": "high",
                "saturation_risk": "medium",
                "rights_status": "mechanism-only",
                "confidence": "medium",
                "avoid_literal_copy": ["specific layout", "creator palette"],
            }],
            "review": {
                "reviewer_id": "reviewer",
                "reviewer_context_id": "review-context",
                "collector_independent": True,
                "source_identity_checked": True,
                "literal_copy_risk_checked": True,
                "reviewed_at": "2026-07-28T00:10:00Z",
                "disposition": "accepted",
            },
        })
        return snapshot

    def test_diverse_independently_reviewed_snapshot_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            snapshot = self.build_snapshot(Path(directory))
            result = run_script(
                "trend_validate.py", snapshot, "--at", "2026-07-28T12:00:00Z"
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_same_domain_and_unproved_velocity_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            snapshot = self.build_snapshot(Path(directory))
            value = json.loads(snapshot.read_text(encoding="utf-8"))
            value["baseline"]["prior_snapshot_refs"] = []
            value["signals"][0]["source_ids"] = ["source-1", "source-2"]
            value["sources"][1]["url"] = "https://curated.example/repost"
            value["sources"][1]["creator_or_project"] = "Curated A"
            write_json(snapshot, value)
            result = run_script(
                "trend_validate.py", snapshot, "--at", "2026-07-28T12:00:00Z"
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("lacks cross-domain corroboration", result.stdout)
            self.assertIn("lacks independent creator", result.stdout)
            self.assertIn("claims velocity without", result.stdout)


class BenchmarkIntegrityTests(unittest.TestCase):
    def build_suite(self, root: Path) -> Path:
        tasks = []
        for index in range(5):
            tasks.append({
                "task_id": f"task-{index}",
                "task_class": f"class-{index}",
                "brief_ref": f"brief-{index}",
                "carrier": "3:4 social image",
                "matched_conditions": {
                    "same_brief": True,
                    "same_carrier": True,
                    "same_output_count": True,
                    "same_selection_budget": True
                },
                "mosocanvas_artifacts": [{
                    "artifact_id": f"moso-{index}",
                    "source_ref": f"moso-{index}.png"
                }],
                "target_artifacts": [{
                    "artifact_id": f"target-{index}",
                    "source_ref": f"target-{index}.png"
                }]
            })
        path = root / "suite.json"
        write_json(path, {
            "schema": "moso.benchmark-suite/0.1",
            "id": "suite",
            "lane": "matched-challenge",
            "target": {
                "system": "midjourney",
                "version_or_surface": "V8.1",
                "source_policy": "matched challenge"
            },
            "captured_at": "2026-07-28T00:00:00Z",
            "expires_at": "2027-07-28T00:00:00Z",
            "leakage_control": {
                "target_hidden_during_direction": True,
                "target_hidden_during_generation": True,
                "holdout_tasks": []
            },
            "tasks": tasks
        })
        return path

    def build_evaluation(self, root: Path, suite: Path) -> Path:
        base = datetime(2026, 7, 28, tzinfo=timezone.utc)
        comparisons = []
        dimensions = (
            "composition", "authored_specificity", "narrative", "color_light",
            "material_coherence", "ai_residue", "carrier_fit"
        )
        for index in range(30):
            pair = index % 10
            task = pair % 5
            moso_wins = pair < 9
            moso_left = index % 2 == 0
            winner_side = (
                "left" if moso_left == moso_wins else "right"
            )
            comparisons.append({
                "comparison_id": f"comparison-{index}",
                "pair_id": f"pair-{pair}",
                "task_id": f"task-{task}",
                "rater_id": f"rater-{(pair + index // 10) % 5}",
                "rater_independent": True,
                "left_artifact_id": f"{'moso' if moso_left else 'target'}-{task}",
                "right_artifact_id": f"{'target' if moso_left else 'moso'}-{task}",
                "assignment": {
                    "left_system": "mosocanvas" if moso_left else "target",
                    "right_system": "target" if moso_left else "mosocanvas",
                    "revealed_at": (base + timedelta(minutes=index, seconds=30)).isoformat()
                },
                "rating": {
                    "winner_side": winner_side,
                    "committed_at": (base + timedelta(minutes=index)).isoformat()
                },
                "dimensions": {name: winner_side for name in dimensions},
                "severity3_defects": {"left": 0, "right": 0}
            })
        path = root / "evaluation.json"
        write_json(path, {
            "schema": "moso.pairwise-evaluation/0.2",
            "id": "evaluation",
            "suite_id": "suite",
            "suite_sha256": sha256(suite),
            "protocol": {
                "source_hidden_during_rating": True,
                "prompt_hidden": True,
                "randomized_sides": True,
                "ratings_committed_before_reveal": True
            },
            "thresholds": {
                "minimum_tasks": 5,
                "minimum_comparisons": 30,
                "minimum_unique_pairs": 10,
                "minimum_raters": 5,
                "confidence_z": 1.96,
                "noninferiority_margin": 0.05,
                "exceeds_observed_preference": 0.60,
                "minimum_task_preference": 0.40
            },
            "comparisons": comparisons
        })
        return path

    def test_valid_clustered_benchmark_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            suite = self.build_suite(root)
            evaluation = self.build_evaluation(root, suite)
            result = run_script(
                "benchmark_score.py", suite, evaluation,
                "--at", "2026-07-29T00:00:00Z"
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["claim"], "exceeds-target")
            self.assertEqual(report["unique_pairs"], 10)
            self.assertEqual(report["tasks"], 5)

    def test_unknown_tasks_and_duplicate_comparisons_are_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            suite = self.build_suite(root)
            evaluation = self.build_evaluation(root, suite)
            value = json.loads(evaluation.read_text(encoding="utf-8"))
            value["suite_id"] = "wrong-suite"
            value["comparisons"][1]["comparison_id"] = value["comparisons"][0]["comparison_id"]
            value["comparisons"][2]["task_id"] = "unknown-task"
            write_json(evaluation, value)
            result = run_script(
                "benchmark_score.py", suite, evaluation,
                "--at", "2026-07-29T00:00:00Z"
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("suite_id does not match", result.stdout)
            self.assertIn("duplicate or empty comparison_id", result.stdout)
            self.assertIn("unknown task_id", result.stdout)


if __name__ == "__main__":
    unittest.main()
