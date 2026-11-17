from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, PngImagePlugin

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
        raise AssertionError(
            f"{script} failed ({result.returncode})\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def load_qa_module():
    sys.path.insert(0, str(BIN))
    spec = importlib.util.spec_from_file_location("qa_images_under_test", BIN / "qa_images.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProductionBlockerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.work = Path(self.tempdir.name)
        self.config = self.work / "resolved.json"
        run(
            "resolve_config.py",
            "--preset", ROOT / "presets" / "travel-food-journal.json",
            "--output", self.config,
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def write_plan(self, source: Path, caption_status: str = "confirmed") -> Path:
        contract = {
            "mark_edge_quality": ["broken dry marks"],
            "negative_space_rules": ["paper remains open"],
            "fill_tonal_rules": ["restrained dark accents"],
            "background_cleanliness": ["no haze"],
            "frame_border_policy": "forbid",
            "abstraction_level": "moderate",
            "generated_page_is_style_reference": False,
        }
        plan = self.work / "plan.json"
        plan.write_text(json.dumps({
            "schema_version": "2.0.0",
            "resolved_config_lock": {"path": str(self.config.resolve()), "sha256": sha(self.config)},
            "style_reference_locks": [],
            "sample_style_contract": contract,
            "composition": {"canvas": {"width": 1152, "height": 2048}},
            "modules": {"caption": {"enabled": True, "lines": ["location", "date"]}},
            "pages": [{
                "page": 1,
                "source_path": str(source.resolve()),
                "source_sha256": sha(source),
                "capture_time": "2026-08-27T12:00:00",
                "caption_data": {"location": "TEST", "date": "2026-08-27"},
                "caption_status": {"location": caption_status, "date": caption_status},
                "production_brief": {
                    "subject_priority": "subject",
                    "thumbnail_read": "subject",
                    "preserve_anchors": ["anchor"],
                    "abstract_or_omit": ["noise"],
                    "material_depth_cues": ["depth"],
                    "structural_lines": [{"element": "line", "operation": "retain"}],
                    "forbidden_inventions": ["invented object"],
                },
            }],
        }))
        return plan

    def write_full_state(self, plan: Path) -> Path:
        plan_data = json.loads(plan.read_text())
        production = self.work / "production.md"
        production.write_text("approved production plan")
        sample = self.work / "sample.png"
        sample_plate = self.work / "sample-plate.png"
        Image.new("RGB", (1152, 2048), "white").save(sample)
        Image.new("RGBA", (1152, 2048), (0, 0, 0, 0)).save(sample_plate)
        validation_report = self.work / "sample-plate-validation.json"
        run("clean_plate.py", "validate", "--input", sample_plate, "--config", self.config,
            "--report", validation_report)
        plate_validation = json.loads(validation_report.read_text())["analysis"]
        renderer_receipt = self.work / "sample-renderer-receipt.json"
        run(
            "renderer_receipt.py", "register",
            "--output", renderer_receipt,
            "--renderer-kind", "local",
            "--model", "fixture-renderer", "--model-version", "1", "--seed", "7",
            "--settings-json", '{"mode":"fixture"}',
            "--source", f"page-1={plan_data['pages'][0]['source_path']}",
            "--rendered-output", f"page-1={sample_plate}",
        )
        state = self.work / "state.json"
        state.write_text(json.dumps({
            "schema_version": "2.0.0",
            "status": "batch_approved",
            "created_at_utc": "2026-08-27T19:00:00+00:00",
            "render_plan_path": str(plan.resolve()),
            "render_plan_sha256": sha(plan),
            "production_plan_path": str(production.resolve()),
            "production_plan_sha256": sha(production),
            "sample_style_contract_sha256": canonical_hash(plan_data["sample_style_contract"]),
            "sample_page": 1,
            "sample_path": str(sample.resolve()),
            "sample_sha256": sha(sample),
            "sample_plate_path": str(sample_plate.resolve()),
            "sample_plate_sha256": sha(sample_plate),
            "sample_plate_validation": plate_validation,
            "renderer_record": {"path": str(renderer_receipt.resolve()), "sha256": sha(renderer_receipt)},
            "sample_registered_at_utc": "2026-08-27T19:01:00+00:00",
            "presented_at_utc": "2026-08-27T19:02:00+00:00",
            "presentation_record": {
                "mode": "artifact",
                "note": "reviewed",
                "decision_coverage": [
                    "finish-qa-delivery", "ordered-page-briefs", "sample-scope", "sample-style-contract"
                ],
                "plan_decisions_communicated": True,
                "sample_discussed": True,
            },
            "approved_at_utc": "2026-08-27T19:03:00+00:00",
            "explicit_approval": {"actor": "user", "text": "Approved"},
            "permitted_render_pages": [],
            "blocked_render_pages": [],
            "revision_ledger": [],
        }))
        return state

    def prepare_review(self, final: Path, plan: Path, *, plates: Path | None = None,
                       config: Path | None = None) -> tuple[Path, Path]:
        if plates is None:
            plates = self.work / f"plates-{final.name}"
            plates.mkdir()
            for image_path in final.iterdir():
                with Image.open(image_path) as image:
                    Image.new("RGBA", image.size, (0, 0, 0, 0)).save(plates / f"{image_path.stem}.png")
        stage = self.work / f"stage-{final.name}.json"
        run("package_verified.py", "stage", "--input", final, "--output", stage)
        qa = self.work / f"qa-{final.name}"
        args: list[object] = ["--input", final, "--output", qa, "--config", config or self.config, "--render-plan", plan]
        if plates is not None:
            args += ["--plates", plates]
        run("qa_images.py", *args)
        checklist = qa / "review-checklist.json"
        data = json.loads(checklist.read_text())
        for page in data["page_level_compliance"]["pages"]:
            for entry in page["checks"].values():
                entry.update(status="pass", evidence="manual full-size and phone review")
        for entry in data["set_level_cohesion"]["checks"].values():
            entry.update(status="pass", evidence="manual set review")
        data["page_level_compliance"]["status"] = "pass"
        data["set_level_cohesion"]["status"] = "pass"
        checklist.write_text(json.dumps(data))
        return stage, checklist

    def write_composition_manifest(self, final: Path, state: Path) -> Path:
        state_data = json.loads(state.read_text())
        plan_path = Path(state_data["render_plan_path"])
        plan_data = json.loads(plan_path.read_text())
        plates = self.work / f"composition-plates-{final.name}"
        plates.mkdir(exist_ok=True)
        receipt = self.work / f"composition-receipt-{final.name}.json"
        receipt_args: list[object] = [
            "register", "--output", receipt, "--renderer-kind", "local",
            "--model", "fixture-renderer", "--model-version", "1", "--seed", "7",
            "--settings-json", '{"mode":"fixture"}',
        ]
        plate_entries = []
        output_entries = []
        for page, image_path in enumerate(sorted(final.iterdir()), start=1):
            plate = plates / f"{page:02d}.png"
            with Image.open(image_path) as image:
                Image.new("RGBA", image.size, (0, 0, 0, 0)).save(plate)
            source = plan_data["pages"][page - 1]["source_path"]
            receipt_args += ["--source", f"page-{page}={source}", "--rendered-output", f"page-{page}={plate}"]
            plate_entries.append({"page": page, "path": str(plate.resolve()), "sha256": sha(plate)})
            output_entries.append({"page": page, "path": str(image_path.resolve()), "sha256": sha(image_path)})
        run("renderer_receipt.py", *receipt_args)
        manifest = self.work / f"composition-{final.name}.json"
        manifest.write_text(json.dumps({
            "schema_version": "1.1.0", "deterministic": True,
            "config_sha256": plan_data["resolved_config_lock"]["sha256"],
            "render_plan_sha256": sha(plan_path),
            "renderer_receipt": {"path": str(receipt.resolve()), "sha256": sha(receipt)},
            "font": {"path": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                     "sha256": sha(Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))},
            "plates": plate_entries,
            "metadata_policy": {"exif_gps_xmp": "forbidden", "verified": True},
            "outputs": output_entries,
        }))
        return manifest

    def package(self, final: Path, stage: Path, checklist: Path, state: Path, *, ok: bool,
                sync_sample: bool = True) -> subprocess.CompletedProcess[str]:
        if sync_sample:
            state_data = json.loads(state.read_text())
            sample_page = next(path for path in sorted(final.iterdir()) if path.stem == "01")
            state_data["sample_path"] = str(sample_page.resolve())
            state_data["sample_sha256"] = sha(sample_page)
            state.write_text(json.dumps(state_data))
        composition = self.write_composition_manifest(final, state)
        return run(
            "package_verified.py", "package",
            "--input", final,
            "--staging-manifest", stage,
            "--review-checklist", checklist,
            "--state", state,
            "--composition-manifest", composition,
            "--output", self.work / "release.zip",
            "--manifest-output", self.work / "release.json",
            ok=ok,
        )

    def test_rgb_distance_uses_non_overflowing_arithmetic(self) -> None:
        qa = load_qa_module()
        result = qa.metrics(Image.new("RGB", (20, 20), (0, 0, 0)), (255, 255, 255))
        self.assertEqual(result["empty_area_noise_ratio"], 1.0)

    def test_manual_pass_cannot_override_dimensions_plate_or_severe_diagnostics(self) -> None:
        source = self.work / "source.jpg"
        Image.new("RGB", (32, 32), "white").save(source)
        plan = self.write_plan(source)
        final = self.work / "bad-final"
        final.mkdir()
        Image.new("RGB", (64, 96), "black").save(final / "01.webp")
        plates = self.work / "plates"
        plates.mkdir()
        _stage, checklist = self.prepare_review(final, plan, plates=plates)
        result = run("review_checklist.py", "validate", "--checklist", checklist, ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("objective", result.stderr.lower())

    def test_reviewed_page_hashes_must_match_exact_staging_manifest(self) -> None:
        source = self.work / "source.jpg"
        Image.new("RGB", (32, 32), "white").save(source)
        plan = self.write_plan(source)
        reviewed = self.work / "reviewed"
        reviewed.mkdir()
        Image.new("RGB", (1152, 2048), (241, 235, 221)).save(reviewed / "01.webp")
        _reviewed_stage, checklist = self.prepare_review(reviewed, plan)
        substituted = self.work / "substituted"
        substituted.mkdir()
        Image.new("RGB", (1152, 2048), (240, 235, 221)).save(substituted / "01.webp")
        substituted_stage = self.work / "substituted-stage.json"
        run("package_verified.py", "stage", "--input", substituted, "--output", substituted_stage)
        result = self.package(substituted, substituted_stage, checklist, self.write_full_state(plan), ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("review", result.stderr.lower())

    def test_review_evidence_hash_change_blocks_packaging(self) -> None:
        source = self.work / "source.jpg"
        Image.new("RGB", (32, 32), "white").save(source)
        plan = self.write_plan(source)
        final = self.work / "final"
        final.mkdir()
        Image.new("RGB", (1152, 2048), (241, 235, 221)).save(final / "01.webp")
        stage, checklist = self.prepare_review(final, plan)
        data = json.loads(checklist.read_text())
        phone = Path(data["page_level_compliance"]["pages"][0]["phone_scale_evidence"])
        Image.new("RGB", (10, 10), "red").save(phone)
        result = self.package(final, stage, checklist, self.write_full_state(plan), ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence", result.stderr.lower())

    def test_batch_requires_confirmed_captions_and_current_source_hashes(self) -> None:
        source = self.work / "source.jpg"
        Image.new("RGB", (32, 32), "white").save(source)
        plan = self.write_plan(source, caption_status="proposed")
        state = self.write_full_state(plan)
        proposed = run(
            "render_scope.py", "--render-plan", plan, "--state", state,
            "--mode", "batch", "--output", self.work / "batch.json", ok=False,
        )
        self.assertNotEqual(proposed.returncode, 0)
        self.assertIn("caption", proposed.stderr.lower())

        plan_data = json.loads(plan.read_text())
        plan_data["pages"][0]["caption_status"] = {"location": "confirmed", "date": "confirmed"}
        plan.write_text(json.dumps(plan_data))
        state = self.write_full_state(plan)
        scope_data = json.loads(state.read_text())
        scope_data["permitted_render_pages"] = [99]
        state.write_text(json.dumps(scope_data))
        wrong_scope = run(
            "render_scope.py", "--render-plan", plan, "--state", state,
            "--mode", "batch", "--output", self.work / "batch-wrong-scope.json", ok=False,
        )
        self.assertNotEqual(wrong_scope.returncode, 0)
        self.assertIn("authorization scope", wrong_scope.stderr.lower())

        state = self.write_full_state(plan)
        Image.new("RGB", (32, 32), "black").save(source)
        stale = run(
            "render_scope.py", "--render-plan", plan, "--state", state,
            "--mode", "batch", "--output", self.work / "batch-stale.json", ok=False,
        )
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("source", stale.stderr.lower())

    def test_packaging_rejects_qa_run_with_a_different_config(self) -> None:
        source = self.work / "source.jpg"
        Image.new("RGB", (32, 32), "white").save(source)
        plan = self.write_plan(source)
        final = self.work / "wrong-qa-config-final"
        final.mkdir()
        Image.new("RGB", (1152, 2048), (241, 235, 221)).save(final / "01.webp")
        alternate = self.work / "alternate-config.json"
        alternate_data = json.loads(self.config.read_text())
        alternate_data["profiles"]["unification"]["paper"]["color"] = "#f0eadc"
        alternate.write_text(json.dumps(alternate_data))
        stage, checklist = self.prepare_review(final, plan, config=alternate)
        result = self.package(final, stage, checklist, self.write_full_state(plan), ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("qa report", result.stderr.lower())
        self.assertIn("config", result.stderr.lower())

    def test_packaging_requires_staged_page_one_to_equal_approved_sample_bytes(self) -> None:
        source = self.work / "source.jpg"
        Image.new("RGB", (32, 32), "white").save(source)
        plan = self.write_plan(source)
        final = self.work / "changed-sample-final"
        final.mkdir()
        Image.new("RGB", (1152, 2048), (241, 235, 221)).save(final / "01.webp")
        stage, checklist = self.prepare_review(final, plan)
        state = self.write_full_state(plan)
        result = self.package(final, stage, checklist, state, ok=False, sync_sample=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("approved sample", result.stderr.lower())

    def test_packaging_rejects_approval_scope_that_does_not_cover_plan(self) -> None:
        source = self.work / "source.jpg"
        Image.new("RGB", (32, 32), "white").save(source)
        plan = self.write_plan(source)
        final = self.work / "wrong-approval-scope-final"
        final.mkdir()
        Image.new("RGB", (1152, 2048), (241, 235, 221)).save(final / "01.webp")
        stage, checklist = self.prepare_review(final, plan)
        state = self.write_full_state(plan)
        data = json.loads(state.read_text())
        data["permitted_render_pages"] = [99]
        state.write_text(json.dumps(data))
        result = self.package(final, stage, checklist, state, ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("authorization scope", result.stderr.lower())

    def test_packaging_requires_complete_approval_state_schema(self) -> None:
        source = self.work / "source.jpg"
        Image.new("RGB", (32, 32), "white").save(source)
        plan = self.write_plan(source)
        final = self.work / "final"
        final.mkdir()
        Image.new("RGB", (1152, 2048), (241, 235, 221)).save(final / "01.webp")
        stage, checklist = self.prepare_review(final, plan)
        state = self.write_full_state(plan)
        state_data = json.loads(state.read_text())
        del state_data["presentation_record"]
        state.write_text(json.dumps(state_data))
        result = self.package(final, stage, checklist, state, ok=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("state", result.stderr.lower())

    def test_package_revalidates_renderer_receipt_captions_and_current_sources(self) -> None:
        source = self.work / "source.jpg"
        Image.new("RGB", (32, 32), "white").save(source)
        plan = self.write_plan(source)
        final = self.work / "final-input-locks"
        final.mkdir()
        Image.new("RGB", (1152, 2048), (241, 235, 221)).save(final / "01.webp")
        stage, checklist = self.prepare_review(final, plan)

        state = self.write_full_state(plan)
        data = json.loads(state.read_text())
        data["renderer_record"] = None
        state.write_text(json.dumps(data))
        missing_receipt = self.package(final, stage, checklist, state, ok=False)
        self.assertNotEqual(missing_receipt.returncode, 0)
        self.assertIn("renderer", missing_receipt.stderr.lower())

        state = self.write_full_state(plan)
        Image.new("RGB", (32, 32), "black").save(source)
        stale_source = self.package(final, stage, checklist, state, ok=False)
        self.assertNotEqual(stale_source.returncode, 0)
        self.assertIn("source", stale_source.stderr.lower())

        Image.new("RGB", (32, 32), "white").save(source)
        proposed_plan = self.write_plan(source, caption_status="proposed")
        proposed_state = self.write_full_state(proposed_plan)
        unconfirmed = self.package(final, stage, checklist, proposed_state, ok=False)
        self.assertNotEqual(unconfirmed.returncode, 0)
        self.assertIn("caption", unconfirmed.stderr.lower())

    def test_stage_rejects_exif_gps_or_xmp_metadata(self) -> None:
        exif_dir = self.work / "exif-final"
        exif_dir.mkdir()
        exif = Image.Exif()
        exif[36867] = "2026:08:27 12:00:00"
        Image.new("RGB", (20, 20), "white").save(exif_dir / "01.jpg", exif=exif)
        result = run(
            "package_verified.py", "stage", "--input", exif_dir,
            "--output", self.work / "exif-stage.json", ok=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata", result.stderr.lower())

        xmp_dir = self.work / "xmp-final"
        xmp_dir.mkdir()
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_itxt("XML:com.adobe.xmp", "<x:xmpmeta>test</x:xmpmeta>")
        Image.new("RGB", (20, 20), "white").save(xmp_dir / "01.png", pnginfo=pnginfo)
        result = run(
            "package_verified.py", "stage", "--input", xmp_dir,
            "--output", self.work / "xmp-stage.json", ok=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata", result.stderr.lower())

        gps_dir = self.work / "gps-final"
        gps_dir.mkdir()
        gps_info = PngImagePlugin.PngInfo()
        gps_info.add_text("GPSLatitude", "37.0000")
        Image.new("RGB", (20, 20), "white").save(gps_dir / "01.png", pnginfo=gps_info)
        result = run(
            "package_verified.py", "stage", "--input", gps_dir,
            "--output", self.work / "gps-stage.json", ok=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("metadata", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
