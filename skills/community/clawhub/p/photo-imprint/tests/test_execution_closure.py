from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, PngImagePlugin

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "bin"
FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")


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


class ExecutionClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.work = Path(self.tempdir.name)
        self.config = self.work / "resolved.json"
        self.plan = self.work / "render-plan.json"
        self.plates = self.work / "plates"
        self.plates.mkdir()
        config = {
            "schema_version": "1.1.0",
            "resolved": True,
            "preset": "test",
            "profiles": {
                "composition": {
                    "canvas": {"width": 180, "height": 320, "aspect_ratio": "9:16"},
                    "whitespace": {"top_clear_space_ratio": 0.5, "edge_margin_ratio": 0.07},
                    "subject": {
                        "center_y_ratio": 0.65,
                        "height_ratio_min": 0.28,
                        "height_ratio_max": 0.32,
                        "horizontal_flow": ["center"],
                    },
                    "caption_zone": {
                        "position": "below-subject",
                        "minimum_subject_clearance_ratio": 0.04,
                        "maximum_lines": 3,
                        "alignment": "center",
                    },
                    "cross_slide": {"assembly": "single-long-canvas-then-crop", "boundary_overlap_px": 0},
                },
                "unification": {"paper": {"color": "#F1EBDD", "finish": "matte", "texture_scale": "shared-master"}},
            },
            "modules": {
                "caption": {
                    "enabled": True,
                    "lines": ["location", "date"],
                    "font_family": "DejaVu Sans",
                    "font_size_at_1080px": 30,
                    "color": "#3B3832",
                },
                "route": {
                    "enabled": True,
                    "color": "#A56F5A",
                    "opacity": 0.62,
                    "width_at_1080px": 3,
                    "hand_drawn": True,
                    "anti_alias": True,
                    "avoid_subjects": True,
                    "markers": {"enabled": True, "start": True, "end": True},
                },
                "watermark": {"enabled": True, "text": "@test", "position": "top-right"},
                "disclosure": {"enabled": False},
                "numbering": {"enabled": False},
            },
        }
        self.config.write_text(json.dumps(config), encoding="utf-8")
        self.plan.write_text(
            json.dumps(
                {
                    "schema_version": "2.0.0",
                    "preset": "test",
                    "resolved_config_lock": {"path": str(self.config.resolve()), "sha256": sha(self.config)},
                    "style_reference_locks": [],
                    "pages": [
                        {
                            "page": 1,
                            "source_path": str(self.config.resolve()),
                            "source_sha256": sha(self.config),
                            "placement": "center",
                            "caption_data": {"location": "PLACE", "date": "2026-08-27"},
                            "plate_contract": {"transparent_background": True},
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        plate = Image.new("RGBA", (90, 90), (0, 0, 0, 0))
        for y in range(15, 75):
            for x in range(15, 75):
                plate.putpixel((x, y), (210, 40, 30, 128))
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("XML:com.adobe.xmp", "gps latitude=private")
        metadata.add_text("exif", "private")
        plate.save(self.plates / "01.png", pnginfo=metadata)
        self.receipt = self.work / "local-renderer-receipt.json"
        run(
            "renderer_receipt.py", "register",
            "--output", self.receipt,
            "--renderer-kind", "local",
            "--model", "test-renderer", "--model-version", "1", "--seed", "7",
            "--settings-json", '{"mode":"fixture"}',
            "--source", f"page-1={self.config}",
            "--rendered-output", f"page-1={self.plates / '01.png'}",
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_compose_is_deterministic_alpha_correct_and_metadata_free(self) -> None:
        if not FONT.is_file():
            self.skipTest("test font unavailable")
        first, second = self.work / "first", self.work / "second"
        run(
            "compose.py",
            "--config", self.config,
            "--render-plan", self.plan,
            "--plates", self.plates,
            "--output", first,
            "--font", FONT,
            "--renderer-receipt", self.receipt,
        )
        run(
            "compose.py",
            "--config", self.config,
            "--render-plan", self.plan,
            "--plates", self.plates,
            "--output", second,
            "--font", FONT,
            "--renderer-receipt", self.receipt,
        )
        one, two = first / "01.png", second / "01.png"
        self.assertEqual(sha(one), sha(two))
        manifest = json.loads((first / "composition-manifest.json").read_text())
        self.assertEqual(manifest["schema_version"], "1.1.0")
        self.assertEqual(manifest["renderer_receipt"]["sha256"], sha(self.receipt))
        self.assertEqual(manifest["plates"][0]["sha256"], sha(self.plates / "01.png"))
        self.assertEqual(manifest["font"]["sha256"], sha(FONT))
        self.assertEqual(manifest["outputs"][0]["sha256"], sha(one))
        with Image.open(one) as image:
            self.assertEqual(image.size, (180, 320))
            self.assertEqual(image.mode, "RGBA")
            self.assertEqual(image.getpixel((0, 0)), (241, 235, 221, 255))
            self.assertEqual(image.getexif(), {})
            self.assertFalse(any("exif" in key.lower() or "xmp" in key.lower() or "gps" in key.lower() for key in image.info))
            # Semi-transparent source pixels must be alpha-composited, not pasted as opaque red.
            subject_pixels = [p for p in image.getdata() if p[0] > 210 and p[1] < 180 and p[2] < 170]
            self.assertTrue(subject_pixels)
            self.assertTrue(any(100 < p[1] < 180 for p in subject_pixels))
            # Route/markers and deterministic typography/watermark create non-paper pixels outside the subject.
            self.assertNotEqual(image.getpixel((12, 110)), (241, 235, 221, 255))

    def test_compose_fails_closed_on_missing_receipt_font_and_unsupported_enabled_module(self) -> None:
        no_receipt = run(
            "compose.py", "--config", self.config, "--render-plan", self.plan,
            "--plates", self.plates, "--output", self.work / "no-receipt", "--font", FONT,
            ok=False,
        )
        self.assertEqual(no_receipt.returncode, 2)
        self.assertIn("receipt", no_receipt.stderr.lower())
        missing = run(
            "compose.py", "--config", self.config, "--render-plan", self.plan,
            "--plates", self.plates, "--output", self.work / "missing", "--font", self.work / "none.ttf",
            "--renderer-receipt", self.receipt,
            ok=False,
        )
        self.assertEqual(missing.returncode, 2)
        self.assertIn("font", missing.stderr.lower())
        config = json.loads(self.config.read_text())
        config["modules"]["numbering"]["enabled"] = True
        bad_config = self.work / "bad-config.json"
        bad_config.write_text(json.dumps(config))
        unsupported = run(
            "compose.py", "--config", bad_config, "--render-plan", self.plan,
            "--plates", self.plates, "--output", self.work / "bad", "--font", FONT,
            "--renderer-receipt", self.receipt,
            ok=False,
        )
        self.assertEqual(unsupported.returncode, 2)
        self.assertIn("unsupported", unsupported.stderr.lower())

    def test_renderer_receipt_requires_complete_hash_locked_evidence(self) -> None:
        receipt = self.work / "receipt.json"
        run("renderer_receipt.py", "not-configured", "--output", receipt)
        data = json.loads(receipt.read_text())
        self.assertEqual(data["status"], "renderer_not_configured")
        self.assertEqual(data["rendered_outputs"], [])
        blocked = run(
            "renderer_receipt.py", "validate", "--receipt", receipt, "--require-rendered-output", ok=False
        )
        self.assertEqual(blocked.returncode, 3)
        self.assertIn("not configured", blocked.stderr.lower())
        forged = data | {"rendered_outputs": [{"name": "fake", "path": "/tmp/fake", "sha256": "0" * 64, "bytes": 1}]}
        receipt.write_text(json.dumps(forged))
        rejected_claim = run("renderer_receipt.py", "validate", "--receipt", receipt, ok=False)
        self.assertEqual(rejected_claim.returncode, 3)
        self.assertIn("cannot claim rendered output", rejected_claim.stderr.lower())

        source = self.work / "source.jpg"
        reference = self.work / "private-reference.webp"
        output = self.work / "rendered.png"
        source.write_bytes(b"source")
        reference.write_bytes(b"private-reference")
        output.write_bytes(b"rendered")
        no_consent = run(
            "renderer_receipt.py", "register",
            "--output", receipt,
            "--renderer-kind", "external",
            "--external-service", "example-renderer",
            "--model", "model-a", "--model-version", "1.2", "--seed", "42",
            "--settings-json", '{"steps":20,"size":[180,320]}',
            "--source", f"page-1={source}",
            "--reference", f"style-private={reference}",
            "--rendered-output", f"page-1={output}",
            ok=False,
        )
        self.assertEqual(no_consent.returncode, 3)
        self.assertIn("authorization", no_consent.stderr.lower())

        run(
            "renderer_receipt.py", "register",
            "--output", receipt,
            "--renderer-kind", "external",
            "--external-service", "example-renderer",
            "--external-reference-decision", "authorized",
            "--model", "model-a", "--model-version", "1.2", "--seed", "42",
            "--settings-json", '{"steps":20,"size":[180,320]}',
            "--source", f"page-1={source}",
            "--reference", f"style-private={reference}",
            "--rendered-output", f"page-1={output}",
        )
        registered = json.loads(receipt.read_text())
        auth = registered["external_reference_processing"]
        self.assertTrue(auth["explicit"])
        self.assertEqual(auth["service"], "example-renderer")
        self.assertEqual(auth["decision"], "authorized")
        run("renderer_receipt.py", "validate", "--receipt", receipt, "--require-rendered-output")
        revoked = json.loads(receipt.read_text())
        revoked["external_reference_processing"]["decision"] = "denied"
        receipt.write_text(json.dumps(revoked))
        denied = run("renderer_receipt.py", "validate", "--receipt", receipt, "--require-rendered-output", ok=False)
        self.assertEqual(denied.returncode, 3)
        self.assertIn("explicitly authorized", denied.stderr.lower())
        registered["external_reference_processing"]["decision"] = "authorized"
        receipt.write_text(json.dumps(registered))
        output.write_bytes(b"tampered")
        tampered = run(
            "renderer_receipt.py", "validate", "--receipt", receipt, "--require-rendered-output", ok=False
        )
        self.assertEqual(tampered.returncode, 3)
        self.assertIn("hash", tampered.stderr.lower())

    def test_route_segment_is_stable_between_sample_and_full_set(self) -> None:
        if not FONT.is_file():
            self.skipTest("test font unavailable")
        second = Image.new("RGBA", (90, 90), (0, 0, 0, 0))
        for y in range(20, 70):
            for x in range(20, 70):
                second.putpixel((x, y), (40, 80, 180, 180))
        second.save(self.plates / "02.png")
        sample_receipt = self.work / "sample-renderer-receipt.json"
        sample_receipt.write_bytes(self.receipt.read_bytes())
        run(
            "renderer_receipt.py", "register",
            "--output", self.receipt,
            "--renderer-kind", "local",
            "--model", "test-renderer", "--model-version", "1", "--seed", "7",
            "--settings-json", '{"mode":"fixture"}',
            "--source", f"page-1={self.config}",
            "--rendered-output", f"page-1={self.plates / '01.png'}",
            "--rendered-output", f"page-2={self.plates / '02.png'}",
        )
        page_one = {
            "page": 1,
            "source_path": str(self.config.resolve()),
            "source_sha256": sha(self.config),
            "placement": "center",
            "caption_data": {"location": "PLACE", "date": "2026-08-27"},
            "plate_contract": {"transparent_background": True},
        }
        page_two = {
            "page": 2,
            "source_path": str(self.config.resolve()),
            "source_sha256": sha(self.config),
            "placement": "right",
            "caption_data": {"location": "SECOND", "date": "2026-08-28"},
            "plate_contract": {"transparent_background": True},
        }
        sample_plan = self.work / "sample-plan.json"
        sample_plan.write_text(json.dumps({
            "schema_version": "2.0.0",
            "review_gate": {"permitted_before_approval": [1], "blocked_before_approval": [2]},
            "pages": [page_one],
        }))
        full_plan = self.work / "full-plan.json"
        full_plan.write_text(json.dumps({
            "schema_version": "2.0.0",
            "review_gate": {"permitted_before_approval": [1], "blocked_before_approval": [2]},
            "pages": [page_one, page_two],
        }))
        sample_out, full_out = self.work / "sample-route", self.work / "full-route"
        run("compose.py", "--config", self.config, "--render-plan", sample_plan,
            "--plates", self.plates, "--output", sample_out, "--font", FONT,
            "--renderer-receipt", sample_receipt)
        run("compose.py", "--config", self.config, "--render-plan", full_plan,
            "--plates", self.plates, "--output", full_out, "--font", FONT,
            "--renderer-receipt", self.receipt)
        self.assertEqual(sha(sample_out / "01.png"), sha(full_out / "01.png"))

    def test_environment_check_and_read_only_workflow_next(self) -> None:
        if not FONT.is_file():
            self.skipTest("test font unavailable")
        ok = run("check_environment.py", "--config", self.config, "--font", FONT, "--json")
        self.assertTrue(json.loads(ok.stdout)["ok"])
        bad = run(
            "check_environment.py", "--config", self.config, "--font", self.work / "missing.ttf", "--json", ok=False
        )
        self.assertEqual(bad.returncode, 2)
        self.assertFalse(json.loads(bad.stdout)["ok"])

        project = self.work / "project"
        project.mkdir()
        (project / "resolved-config.json").write_text(self.config.read_text())
        (project / "manifest.json").write_text('{"items":[{"page":1}]}')
        (project / "render-plan.json").write_text(self.plan.read_text())
        (project / "production-plan.md").write_text("plan")
        state = {
            "status": "plan_ready_sample_not_registered",
            "sample_page": 1,
            "blocked_render_pages": [2],
        }
        (project / "approval-state.json").write_text(json.dumps(state))
        before = {p.name: (p.stat().st_mtime_ns, sha(p)) for p in project.iterdir()}
        result = run("workflow.py", "next", "--project", project)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["next"], "configure_renderer")
        self.assertFalse(payload["gate_bypassed"])
        after = {p.name: (p.stat().st_mtime_ns, sha(p)) for p in project.iterdir()}
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
