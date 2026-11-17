#!/usr/bin/env python3
"""Smoke tests for compact native-host Agent task cards."""

from __future__ import annotations

import json
import copy
import hashlib
import tempfile
import unittest
import subprocess
from pathlib import Path

from prepare_agent_task_cards import ANALYSIS_AGENTS, analysis_cards
from runtime_acceptance import ACCEPTANCE_SCOPE, build_prompt, write_lead_card
from prepare_workbuddy_acceptance_scaffold import prepare_scaffold
from prepare_codex_acceptance import prepare as prepare_codex_acceptance
from bind_workbuddy_analysis_returns import bind
from prepare_workbuddy_acceptance_review import prepare as prepare_review
from finalize_workbuddy_acceptance_review import finalize as finalize_review
from analysis_depth_smoke import GOOD_DEPTH
from collaboration_smoke import handoff
from role_analysis_contract import questions, contract

def bind_questions(body, role):
    body['analysis_depth']['question_contract']=contract(role,'mechanism')
    rows=questions(role,'mechanism')
    for row in rows:
        row.update(status='answered',answer='本次为固定合成夹具，核对运行身份和来源指纹一致；不证明原生执行或经营结论。',evidence_ids=[body['evidence_ledger'][0]['id']])
    body['analysis_depth']['minimum_analysis_set']=rows


class Args:
    run_dir = ""
    plugin_dir = ""
    baseline = None
    chapter_plan = None
    inventory = None
    attempt = "a1"
    output = None
    pretty = False
    host = "workbuddy"


class AgentTaskCardSmoke(unittest.TestCase):
    def make_run(self, root: Path) -> Path:
        run = root / "run"
        run.mkdir()
        common = {"run_id": "acc-v200-card-test", "client_scope": "runtime-acceptance-no-client-data", "team_version": "2.0.3"}
        (run / "team-bootstrap.json").write_text(json.dumps({**common, "host": "workbuddy", "status": "team_created"}), encoding="utf-8")
        (run / "baseline-pack.json").write_text(json.dumps({**common, "scope": "bounded test"}), encoding="utf-8")
        (run / "chapter-plan.json").write_text(json.dumps({**common, "chapters": [{"chapter_id": "C1", "owner_agent": "data-analyst"}]}), encoding="utf-8")
        (run / "report-inventory.json").write_text(json.dumps(common), encoding="utf-8")
        return run

    def test_cards_are_role_scoped_and_prompts_are_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            run = self.make_run(root)
            args = Args()
            args.run_dir = str(run)
            args.plugin_dir = str(root)
            result = analysis_cards(args)
            self.assertEqual([item["agent_id"] for item in result["cards"]], list(ANALYSIS_AGENTS))
            self.assertLessEqual(result["launch_prompt_max_chars"], 300)
            return_files: set[str] = set()
            for item in result["cards"]:
                card = json.loads(Path(item["card_path"]).read_text(encoding="utf-8"))
                self.assertEqual(card["attempt_id"], "a1")
                self.assertTrue(card["paths"]["return_file"].endswith("a1.return.json"))
                required = card["required_result"]["return_receipt_required_fields"]
                self.assertIn("handoff_sha256", required)
                self.assertNotIn("raw_handoff_sha256", required)
                self.assertIn("exactly handoff_sha256", card["required_result"]["handoff_sha256_definition"])
                return_files.add(card["paths"]["return_file"])
            self.assertEqual(len(return_files), 4)

    def test_codex_cards_use_native_orchestration_identity_without_workbuddy_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            run = root / "run"
            run.mkdir()
            common = {"run_id": "acc-v200-codex-card", "client_scope": "runtime-acceptance-no-client-data", "team_version": "2.0.3"}
            (run / "host-orchestration-plan.json").write_text(json.dumps({**common, "host": "codex", "status": "planned_not_executed", "bootstrap_mode": "codex_native_subagents"}), encoding="utf-8")
            (run / "baseline-pack.json").write_text(json.dumps({**common, "scope": "bounded codex test"}), encoding="utf-8")
            (run / "chapter-plan.json").write_text(json.dumps({**common, "chapters": [{"chapter_id": "C1", "owner_agent": "data-analyst"}]}), encoding="utf-8")
            (run / "report-inventory.json").write_text(json.dumps(common), encoding="utf-8")
            args = Args()
            args.run_dir = str(run)
            args.plugin_dir = str(root)
            args.host = "codex"
            result = analysis_cards(args)
            self.assertEqual(result["host"], "codex")
            for item in result["cards"]:
                card = json.loads(Path(item["card_path"]).read_text(encoding="utf-8"))
                self.assertEqual(card["host"], "codex")
                self.assertIn("host_identity", card["paths"])
                self.assertNotIn("team_bootstrap", card["paths"])
                self.assertEqual(card["required_result"]["message_recipient"], "team-lead")
                self.assertNotIn("send_message_recipient", card["required_result"])

    def test_invalid_attempt_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            run = self.make_run(root)
            args = Args()
            args.run_dir = str(run)
            args.plugin_dir = str(root)
            args.attempt = "data-analyst-a1"
            with self.assertRaises(SystemExit):
                analysis_cards(args)

    def test_lead_acceptance_card_has_fixed_identity_and_short_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            work = root / "work"; runs = work / "runs"
            work.mkdir(); runs.mkdir()
            plugin = root / "plugin"; (plugin / ".codebuddy-plugin").mkdir(parents=True)
            (plugin / ".codebuddy-plugin" / "plugin.json").write_text(json.dumps({"version": "2.0.3"}), encoding="utf-8")
            card_path, run_dir = write_lead_card(work, runs, plugin, "2.0.3", "acc-v200-candidate1-", "r7")
            card = json.loads(card_path.read_text(encoding="utf-8"))
            prompt = build_prompt(card_path)
            self.assertEqual(card["run_id"], "acc-v200-candidate1-r7")
            self.assertEqual(card["client_scope"], ACCEPTANCE_SCOPE)
            self.assertEqual(Path(card["run_dir"]), run_dir)
            self.assertLessEqual(len(prompt), 300)
            self.assertIn("OMNI_ECOM_ACCEPTANCE_CARD", prompt)
            self.assertIn("--help", card["forbidden_exploration"])
            self.assertIn("prepare_workbuddy_acceptance_scaffold.py", card["scaffold_command"])

    def test_acceptance_scaffold_creates_valid_immutable_inputs_and_cards(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); work = root / "work"; runs = work / "runs"; plugin = root / "plugin"
            work.mkdir(); runs.mkdir(); (plugin / ".codebuddy-plugin").mkdir(parents=True)
            (plugin / ".codebuddy-plugin" / "plugin.json").write_text(json.dumps({"version": "2.0.3"}), encoding="utf-8")
            card_path, run_dir = write_lead_card(work, runs, plugin, "2.0.3", "acc-v200-candidate1-", "scaffold")
            result = prepare_scaffold(card_path, plugin)
            self.assertEqual(result["status"], "acceptance_scaffold_ready")
            self.assertTrue((run_dir / "run-journal.sqlite").is_file())
            self.assertTrue((run_dir / "report-clusters.json").is_file())
            self.assertTrue((run_dir / "claim-ledger.json").is_file())
            self.assertTrue((run_dir / "team-lead-handoff.json").is_file())
            baseline = json.loads((run_dir / "baseline-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(baseline["contract_name"], "omni-ecom.analysis-baseline")
            manifest = json.loads(Path(result["launch_manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["cards"]), 4)
            self.assertLessEqual(manifest["launch_prompt_max_chars"], 300)
            self.assertIn("wait_for_agent_returns.py", result["wait_command"])
            self.assertIn("data-analyst=data-analyst/a1.return.json", result["wait_command"])
            self.assertNotIn("data-analyst\\a1.return.json", result["wait_command"])
            with self.assertRaises(ValueError):
                prepare_scaffold(card_path, plugin)

    def test_codex_acceptance_scaffold_has_no_workbuddy_team_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); work = root / "work"; plugin = root / "plugin"
            (plugin / ".codebuddy-plugin").mkdir(parents=True)
            (plugin / ".codebuddy-plugin" / "plugin.json").write_text(json.dumps({"version": "2.0.3"}), encoding="utf-8")
            result = prepare_codex_acceptance(work, plugin, "r1")
            run_dir = Path(result["run_dir"])
            self.assertEqual(result["host"], "codex")
            self.assertFalse((run_dir / "team-bootstrap.json").exists())
            plan = json.loads((run_dir / "host-orchestration-plan.json").read_text(encoding="utf-8"))
            self.assertEqual(plan["bootstrap_mode"], "codex_native_subagents")
            manifest = json.loads(Path(result["launch_manifest"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["host"], "codex")
            self.assertIn("--host codex", result["analysis_binding_command_template"])
            self.assertIn("--host codex", result["review_prepare_command"])

    def test_real_task_ids_bind_completed_returns_to_sqlite_and_sealed_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); work = root / "work"; runs = work / "runs"; plugin = root / "plugin"
            work.mkdir(); runs.mkdir(); (plugin / ".codebuddy-plugin").mkdir(parents=True)
            (plugin / ".codebuddy-plugin" / "plugin.json").write_text(json.dumps({"version": "2.0.3"}), encoding="utf-8")
            card_path, run_dir = write_lead_card(work, runs, plugin, "2.0.3", "acc-v200-candidate1-", "binding")
            prepare_scaffold(card_path, plugin)
            baseline_hash = hashlib.sha256((run_dir / "baseline-pack.json").read_bytes()).hexdigest()
            mappings = []
            for index, role in enumerate(ANALYSIS_AGENTS, 1):
                raw = run_dir / "raw-handoffs" / f"handoff-{role}-a1.json"; raw.parent.mkdir(exist_ok=True)
                body = handoff(role, f"{role} 完成固定验收")
                body.update(__import__('artifact_contract').native_handoff_identity('2.0.3'), agent_version='2.0.3')
                body.update(run_id="acc-v200-candidate1-binding", client_scope=ACCEPTANCE_SCOPE, attempt_id="a1")
                body["scope"] = json.loads((run_dir / "baseline-pack.json").read_text(encoding="utf-8"))["scope"]
                body["analysis_depth"] = copy.deepcopy(GOOD_DEPTH)
                body["analysis_depth"]["created_by_team_version"] = "2.0.3"
                body["analysis_depth"]["baseline_ack"]["baseline_sha256"] = baseline_hash
                bind_questions(body,role)
                raw.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
                digest = hashlib.sha256(raw.read_bytes()).hexdigest()
                task_id = f"agent-binding-{index}"; mappings.append(f"{role}={task_id}")
                ret = run_dir / "agent-returns" / role / "a1.return.json"; ret.parent.mkdir(parents=True, exist_ok=True)
                ret.write_text(json.dumps({"run_id": "acc-v200-candidate1-binding", "agent_id": role, "agent_task_id": task_id, "attempt_id": "a1", "return_status": "completed", "returned_at": "2026-09-09T00:00:00Z", "contribution_summary": f"{role} 完成固定验收", "response": {"result": "ok"}, "handoff_sha256": digest}, ensure_ascii=False), encoding="utf-8")
            result = bind(run_dir, mappings)
            self.assertEqual(result["status"], "analysis_returns_bound")
            self.assertEqual(len(list((run_dir / "sealed").glob("*.json"))), 4)
            self.assertTrue((run_dir / "quality-inputs.json").is_file())

    def test_fixed_after_binding_commands_build_verified_chart_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); work = root / "work"; runs = work / "runs"; plugin = Path(__file__).resolve().parents[1]
            work.mkdir(); runs.mkdir()
            version = json.loads((plugin/'version-info.json').read_text(encoding='utf-8'))['team_version']
            card_path, run_dir = write_lead_card(work, runs, plugin, version, "acc-v200-candidate1-", "pipeline")
            scaffold = prepare_scaffold(card_path, plugin)
            baseline_hash = hashlib.sha256((run_dir / "baseline-pack.json").read_bytes()).hexdigest()
            mappings = []
            for index, role in enumerate(ANALYSIS_AGENTS, 1):
                raw = run_dir / "raw-handoffs" / f"handoff-{role}-a1.json"; raw.parent.mkdir(exist_ok=True)
                body = handoff(role, f"{role} 完成固定验收")
                body.update(run_id="acc-v200-candidate1-pipeline", client_scope=ACCEPTANCE_SCOPE, attempt_id="a1")
                body.update(__import__('artifact_contract').native_handoff_identity(version), agent_version=version)
                body["scope"] = json.loads((run_dir / "baseline-pack.json").read_text(encoding="utf-8"))["scope"]
                body["analysis_depth"] = copy.deepcopy(GOOD_DEPTH)
                body["analysis_depth"]["created_by_team_version"] = version
                body["analysis_depth"]["baseline_ack"]["baseline_sha256"] = baseline_hash
                bind_questions(body,role)
                raw.write_text(json.dumps(body, ensure_ascii=False), encoding="utf-8")
                task_id = f"agent-pipeline-{index}"; mappings.append(f"{role}={task_id}")
                member_card = json.loads((run_dir / "task-cards" / "analysis" / "a1" / f"{role}-a1.json").read_text(encoding="utf-8"))
                generated = subprocess.run(member_card["return_command"], shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
                self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
            bind(run_dir, mappings)
            for command in scaffold["after_binding_commands"]:
                completed = subprocess.run(command, shell=True, cwd=work, capture_output=True, text=True, encoding="utf-8", errors="replace")
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            receipt = json.loads((run_dir / "pdf-delivery.json").read_text(encoding="utf-8"))
            self.assertEqual(receipt["status"], "pdf_render_verified")
            self.assertGreaterEqual(receipt["chart_count"], 3)
            report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
            self.assertTrue(report['acceptance_only'])
            self.assertEqual(len(report['mechanism_findings']), 4)
            self.assertEqual(report['metrics'][0]['inputs']['gmv'],1000)
            self.assertIn('经营 BLOCKED',report['acceptance_notice'])
            self.assertEqual(report["stage0"]["status"], "stage0_complete")
            self.assertEqual(len(report["collaboration_quality"]["agent_depth"]), 4)
            markdown = (run_dir / "report.md").read_text(encoding="utf-8")
            self.assertIn("数据概览与覆盖", markdown)
            self.assertIn("协作质量记录", markdown)
            review = prepare_review(run_dir, plugin)
            self.assertIn("delivery-review=delivery-review/a1.return.json", review["wait_command"])
            manifest = json.loads((run_dir / "review-manifest.json").read_text(encoding="utf-8"))
            card_body = json.loads(Path(review['card_path']).read_text(encoding='utf-8'))
            self.assertEqual(card_body['raw_review_result_template']['reviewed_artifacts'], [{'file': entry['file'],'sha256': entry['sha256']} for entry in manifest['artifacts']])
            self.assertEqual(card_body['raw_review_result_template']['review_status'],'rejected')
            raw = run_dir / "review" / "R1" / "delivery-review-r1-a1.return.json"; raw.parent.mkdir(parents=True)
            raw.write_text(json.dumps({"schema_version": "2.0", "artifact_type": "review_result", "contract_name": "omni-ecom.review-result", "contract_version": "2.0", "created_by_team_version": "2.0.3", "legacy_compatibility": {"read_only_import": ["omni-ecom.review-result@1.0"], "current_completion_authority": False}, "run_id": "acc-v200-candidate1-pipeline", "client_scope": ACCEPTANCE_SCOPE, "agent_id": "delivery-review", "agent_version": "2.0.3", "review_attempt_id": "delivery-review-r1-a1", "report_revision": "R1", "return_status": "completed", "returned_at": "2099-09-09T00:00:00Z", "review_status": "passed", "reviewed_manifest_sha256": manifest["manifest_sha256"], "reviewed_artifacts": [{"file": item["file"], "sha256": item["sha256"]} for item in manifest["artifacts"]], "findings": ["冻结报告和来源一致"], "required_changes": [], "contribution_summary": "独立复核通过"}, ensure_ascii=False), encoding="utf-8")
            review_card = json.loads(Path(review["card_path"]).read_text(encoding="utf-8"))
            raw_payload = json.loads(raw.read_text(encoding='utf-8'))
            raw_payload.update(created_by_team_version=version,agent_version=version)
            raw.write_text(json.dumps(raw_payload,ensure_ascii=False),encoding='utf-8')
            generated = subprocess.run(review_card["return_command"], shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
            self.assertEqual(generated.returncode, 0, generated.stdout + generated.stderr)
            final = finalize_review(run_dir, plugin, "agent-review-pipeline")
            self.assertEqual(final["status"], "candidate_pipeline_complete" if '-candidate.' in version else "formal_delivery_complete")
            self.assertIn("delivery-review：agent-review-pipeline", final["required_final_summary"])
            self.assertEqual(len(final["agent_task_ids"]), 5)
            self.assertTrue((run_dir / ("candidate-acceptance-receipt.json" if '-candidate.' in version else "completion-receipt.json")).is_file())


if __name__ == "__main__":
    unittest.main()
