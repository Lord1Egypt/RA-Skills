from __future__ import annotations

import io
import json
import msgpack
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from live_api_test import LiveSuite  # noqa: E402


class LiveHarnessOfflineTests(unittest.TestCase):
    def test_v5_payload_contains_structured_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            suite = LiveSuite("test-token", Path(temp_dir), 1)
            payload = suite.build_image_payload(
                model="nai-diffusion-5-full",
                prompt="transparent moon",
                negative_prompt="blurry",
                straight_alpha=True,
            )
            params = payload["parameters"]
            self.assertEqual(payload["action"], "generate")
            self.assertEqual(params["params_version"], 4)
            self.assertTrue(params["straight_alpha"])
            self.assertEqual(params["qualityPresetId"], "standard")

    def test_v45_payload_contains_character_and_reference_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            suite = LiveSuite("test-token", Path(temp_dir), 1)
            payload = suite.build_image_payload(
                model="nai-diffusion-4-5-full",
                prompt="two people",
                characters=[
                    {
                        "prompt": "girl, silver hair",
                        "uc": "bad hands",
                        "center": {"x": 0.3, "y": 0.5},
                    }
                ],
                references=["encoded-vibe"],
                reference_information=[0.7],
                reference_strengths=[0.6],
            )
            params = payload["parameters"]
            self.assertEqual(params["characterPrompts"][0]["prompt"], "girl, silver hair")
            self.assertEqual(params["v4_prompt"]["caption"]["char_captions"][0]["centers"][0]["x"], 0.3)
            self.assertEqual(params["reference_image_multiple"], ["encoded-vibe"])
            self.assertEqual(params["reference_strength_multiple"], [0.6])

    def test_v45_inpaint_payload_contains_required_fields(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            suite = LiveSuite("test-token", Path(temp_dir), 1)
            payload = suite.build_image_payload(
                model="nai-diffusion-4-5-full-inpainting",
                action="infill",
                prompt="a flower",
                image=b"image",
                mask=b"mask",
                strength=0.25,
                noise=0.0,
                inpaint_img2img_strength=1,
            )
            params = payload["parameters"]
            self.assertIn("v4_prompt", params)
            self.assertEqual(params["inpaintImg2ImgStrength"], 1)
            self.assertIn("extra_noise_seed", params)

    def test_messagepack_final_image_decoding(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            suite = LiveSuite("test-token", Path(temp_dir), 1)
            image = b"fake-png-bytes"
            frame = msgpack.packb(
                {"event_type": "final", "samp_ix": 0, "image": image},
                use_bin_type=True,
            )
            stream = len(frame).to_bytes(4, "big") + frame
            self.assertEqual(suite.parse_msgpack_images(stream), [image])

    def test_zip_image_decoding(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            suite = LiveSuite("test-token", Path(temp_dir), 1)
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as archive:
                archive.writestr("sample.png", b"png")
                archive.writestr("metadata.json", json.dumps({"seed": 42}))
            self.assertEqual(suite.parse_zip_images(buffer.getvalue()), [b"png"])

    def test_mask_is_a_png(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            suite = LiveSuite("test-token", Path(temp_dir), 1)
            mask = suite.create_mask(64, 64)
            self.assertTrue(mask.startswith(b"\x89PNG"))

    def test_safe_text_redacts_token(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            suite = LiveSuite("pst-test", Path(temp_dir), 1)
            safe = suite.safe_text("Authorization: Bearer pst-test")
            self.assertNotIn("pst-test", safe)
            self.assertIn("[REDACTED]", safe)


if __name__ == "__main__":
    unittest.main()
