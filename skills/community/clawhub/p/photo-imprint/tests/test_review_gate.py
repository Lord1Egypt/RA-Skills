from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "bin"


def run(script: str, *args: object, ok: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(BIN / script), *(str(arg) for arg in args)],
        text=True,
        capture_output=True,
        check=False,
    )
    if ok and result.returncode != 0:
        raise AssertionError(f"{script} failed ({result.returncode})\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
    return result


def make_photo(path: Path, capture: str) -> None:
    exif = Image.Exif()
    exif[36867] = capture
    Image.new("RGB", (80, 60), "white").save(path, exif=exif)


class ReviewGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.work = Path(self.tempdir.name)
        self.photos = self.work / "photos"
        self.photos.mkdir()
        make_photo(self.photos / "later.jpg", "2026:08:17 10:09:00")
        make_photo(self.photos / "first.jpg", "2026:08:15 09:47:20")
        make_photo(self.photos / "middle.jpg", "2026:08:16 11:31:45")
        self.config = self.work / "resolved.json"
        run("resolve_config.py", "--preset", ROOT / "presets/travel-food-journal.json", "--output", self.config)
        self.manifest = self.work / "manifest.json"
        run("preprocess.py", "--input", self.photos, "--output", self.manifest, "--config", self.config)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_preprocess_orders_exif_and_initializes_plan_fields(self) -> None:
        manifest = json.loads(self.manifest.read_text())
        self.assertEqual([item["filename"] for item in manifest["items"]], ["first.jpg", "middle.jpg", "later.jpg"])
        self.assertTrue(manifest["requires_user_confirmation"])
        self.assertEqual(manifest["review_gate"]["batch_render_authorized"], False)
        self.assertEqual(len(manifest["unconfirmed_production_briefs"]), 3)
        for item in manifest["items"]:
            self.assertEqual(item["production_brief"]["preserve_anchors"], [])
            self.assertIsNone(item["production_brief"]["thumbnail_read"])

    def test_build_render_plan_blocks_missing_production_briefs(self) -> None:
        result = run(
            "build_render_plan.py",
            "--config", self.config,
            "--manifest", self.manifest,
            "--output", self.work / "render-plan.json",
            ok=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("production_brief.subject_priority is required", result.stderr)

    def prepare_plan(self) -> tuple[Path, Path, Path]:
        manifest = json.loads(self.manifest.read_text())
        priorities = ["open sky and height", "tree within courtyard", "glass facade"]
        for index, item in enumerate(manifest["items"]):
            item["location"] = f"LOCATION {index + 1}"
            item["subject"] = f"SUBJECT {index + 1}"
            item["caption_status"] = {"location": "confirmed", "subject": "confirmed", "date": "confirmed"}
            item["production_brief"] = {
                "subject_priority": priorities[index],
                "thumbnail_read": f"thumbnail read {index + 1}",
                "preserve_anchors": [f"anchor {index + 1}a", f"anchor {index + 1}b"],
                "abstract_or_omit": [f"omit detail {index + 1}"],
                "material_depth_cues": [f"depth cue {index + 1}"],
                "structural_lines": [{"element": f"line {index + 1}", "operation": "retain_but_simplify"}],
                "forbidden_inventions": [f"invented item {index + 1}"],
            }
        self.manifest.write_text(json.dumps(manifest))
        render_plan = self.work / "render-plan.json"
        run("build_render_plan.py", "--config", self.config, "--manifest", self.manifest, "--output", render_plan)
        plan_data = json.loads(render_plan.read_text())
        plan_data["style_references"] = [{
            "id": "test-reference",
            "technique_roles": ["broken contour", "restrained value grouping"],
        }]
        render_plan.write_text(json.dumps(plan_data))
        production_plan = self.work / "production-plan.md"
        state = self.work / "approval-state.json"
        run(
            "build_production_plan.py",
            "--render-plan", render_plan,
            "--output", production_plan,
            "--state-output", state,
        )
        return render_plan, production_plan, state

    def renderer_receipt(self, render_plan: Path, sample_plate: Path) -> Path:
        source = json.loads(render_plan.read_text())["pages"][0]["source_path"]
        receipt = self.work / "renderer-receipt.json"
        run(
            "renderer_receipt.py", "register",
            "--output", receipt,
            "--renderer-kind", "local",
            "--model", "fixture-renderer", "--model-version", "1", "--seed", "7",
            "--settings-json", '{"mode":"fixture"}',
            "--source", f"page-1={source}",
            "--rendered-output", f"page-1={sample_plate}",
        )
        return receipt

    def test_plan_contains_required_review_information(self) -> None:
        render_plan, production_plan, state = self.prepare_plan()
        text = production_plan.read_text()
        self.assertIn("DRAFT — batch rendering is blocked", text)
        self.assertIn("Subject priority", text)
        self.assertIn("Preserve anchors", text)
        self.assertIn("Thumbnail read", text)
        self.assertIn("Material/depth cues", text)
        self.assertIn("Source-grounded structural lines", text)
        self.assertIn("Abstract or omit", text)
        self.assertIn("Caption fields/status", text)
        self.assertIn("Style-reference technique roles", text)
        self.assertIn("broken contour; restrained value grouping", text)
        self.assertIn("Render page 1 only", text)
        gate = json.loads(state.read_text())
        self.assertEqual(gate["status"], "plan_ready_sample_not_registered")
        self.assertEqual(gate["permitted_render_pages"], [1])
        self.assertEqual(gate["blocked_render_pages"], [2, 3])

    def test_batch_blocks_until_explicit_approval_then_emits_only_remaining_pages(self) -> None:
        render_plan, _production_plan, state = self.prepare_plan()
        sample_scope = self.work / "sample-scope.json"
        run("render_scope.py", "--render-plan", render_plan, "--state", state, "--mode", "sample", "--output", sample_scope)
        self.assertEqual([p["page"] for p in json.loads(sample_scope.read_text())["pages"]], [1])

        blocked = run(
            "render_scope.py", "--render-plan", render_plan, "--state", state,
            "--mode", "batch", "--output", self.work / "batch.json", ok=False,
        )
        self.assertEqual(blocked.returncode, 3)
        self.assertIn("require explicit user approval", blocked.stderr)

        sample = self.work / "sample.png"
        sample_plate = self.work / "sample-plate.png"
        Image.new("RGBA", (1152, 2048), (0, 0, 0, 0)).save(sample)
        Image.new("RGBA", (1152, 2048), (0, 0, 0, 0)).save(sample_plate)
        no_receipt = run("review_gate.py", "register-sample", "--state", state, "--sample", sample,
            "--sample-plate", sample_plate, ok=False)
        self.assertNotEqual(no_receipt.returncode, 0)
        self.assertIn("renderer-record", no_receipt.stderr.lower())
        receipt = self.renderer_receipt(render_plan, sample_plate)
        extra_output = self.work / "unauthorized-page-2.png"
        Image.new("RGBA", (1152, 2048), (0, 0, 0, 0)).save(extra_output)
        overbroad = json.loads(receipt.read_text())
        overbroad["rendered_outputs"].append({
            "name": extra_output.name, "path": str(extra_output.resolve()),
            "sha256": hashlib.sha256(extra_output.read_bytes()).hexdigest(), "bytes": extra_output.stat().st_size,
        })
        receipt.write_text(json.dumps(overbroad))
        extra_blocked = run("review_gate.py", "register-sample", "--state", state, "--sample", sample,
            "--sample-plate", sample_plate, "--renderer-record", receipt, ok=False)
        self.assertNotEqual(extra_blocked.returncode, 0)
        self.assertIn("exactly the normalized sample plate", extra_blocked.stderr.lower())
        receipt = self.renderer_receipt(render_plan, sample_plate)
        run("review_gate.py", "register-sample", "--state", state, "--sample", sample, "--sample-plate", sample_plate,
            "--renderer-record", receipt)
        still_blocked = run(
            "render_scope.py", "--render-plan", render_plan, "--state", state,
            "--mode", "batch", "--output", self.work / "batch.json", ok=False,
        )
        self.assertEqual(still_blocked.returncode, 3)
        not_shown = run(
            "review_gate.py", "approve", "--state", state,
            "--approval-text", "Approved", "--explicit-user-approval", ok=False,
        )
        self.assertEqual(not_shown.returncode, 3)
        self.assertIn("plan decisions and sample were discussed", not_shown.stderr)

        run(
            "review_gate.py", "mark-shown", "--state", state,
            "--presentation-mode", "faithful-summary",
            "--discussion-note", "production plan decisions and sample discussed together in chat",
            "--plan-decisions-communicated", "--sample-discussed",
            "--decision-coverage", "ordered-page-briefs",
            "--decision-coverage", "sample-style-contract",
            "--decision-coverage", "sample-scope",
            "--decision-coverage", "finish-qa-delivery",
        )
        inferred = run(
            "review_gate.py", "approve", "--state", state,
            "--approval-text", "Looks interesting", ok=False,
        )
        self.assertEqual(inferred.returncode, 3)
        self.assertIn("never infer permission", inferred.stderr)

        run(
            "review_gate.py", "approve", "--state", state,
            "--approval-text", "Approved. Please render the remaining pages.",
            "--explicit-user-approval",
        )
        batch = self.work / "batch.json"
        run("render_scope.py", "--render-plan", render_plan, "--state", state, "--mode", "batch", "--output", batch)
        self.assertEqual([p["page"] for p in json.loads(batch.read_text())["pages"]], [2, 3])

    def test_any_plan_or_sample_revision_invalidates_prior_approval(self) -> None:
        render_plan, production_plan, state = self.prepare_plan()
        sample = self.work / "sample.png"
        sample_plate = self.work / "sample-plate.png"
        Image.new("RGBA", (1152, 2048), (0, 0, 0, 0)).save(sample)
        Image.new("RGBA", (1152, 2048), (0, 0, 0, 0)).save(sample_plate)
        receipt = self.renderer_receipt(render_plan, sample_plate)
        run("review_gate.py", "register-sample", "--state", state, "--sample", sample, "--sample-plate", sample_plate,
            "--renderer-record", receipt)
        run(
            "review_gate.py", "mark-shown", "--state", state,
            "--presentation-mode", "faithful-summary",
            "--discussion-note", "production plan decisions and sample discussed together in chat",
            "--plan-decisions-communicated", "--sample-discussed",
            "--decision-coverage", "ordered-page-briefs",
            "--decision-coverage", "sample-style-contract",
            "--decision-coverage", "sample-scope",
            "--decision-coverage", "finish-qa-delivery",
        )
        run(
            "review_gate.py", "approve", "--state", state,
            "--approval-text", "Yes, continue with pages two and three.",
            "--explicit-user-approval",
        )
        original_config = self.config.read_bytes()
        self.config.write_bytes(original_config + b"\n")
        config_blocked = run(
            "render_scope.py", "--render-plan", render_plan, "--state", state,
            "--mode", "batch", "--output", self.work / "batch-config.json", ok=False,
        )
        self.assertEqual(config_blocked.returncode, 3)
        self.assertIn("resolved config changed", config_blocked.stderr)
        self.config.write_bytes(original_config)
        production_plan.write_text(production_plan.read_text() + "\nrevision\n")
        blocked = run(
            "render_scope.py", "--render-plan", render_plan, "--state", state,
            "--mode", "batch", "--output", self.work / "batch.json", ok=False,
        )
        self.assertEqual(blocked.returncode, 3)
        self.assertIn("changed after the review state was created", blocked.stderr)


if __name__ == "__main__":
    unittest.main()
