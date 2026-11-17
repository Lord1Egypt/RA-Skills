#!/usr/bin/env python3
"""Run a sequential, redacted NovelAI API capability smoke suite.

The token is read only from NOVELAI_TOKEN. It is never printed, persisted, or
included in the result report. This script is intentionally API-level: the
OpenClaw and MCP CLIs are tested separately on the target host.
"""

from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass, field
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import re
import struct
import sys
import time
from typing import Any, Iterable
import uuid
import zipfile

try:
    from curl_cffi import requests
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("curl-cffi is required for the live API suite") from exc

try:
    import msgpack
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("msgpack is required for V4/V5 response decoding") from exc

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("Pillow is required to create the inpaint mask") from exc


IMAGE_HOST = "https://image.novelai.net"
LEGACY_HOST = "https://api.novelai.net"
TEXT_HOST = "https://text.novelai.net"

V4_MODELS = {
    "nai-diffusion-4-full",
    "nai-diffusion-4-full-inpainting",
    "nai-diffusion-4-curated-preview",
    "nai-diffusion-4-curated-inpainting",
    "nai-diffusion-4-5-full",
    "nai-diffusion-4-5-full-inpainting",
    "nai-diffusion-4-5-curated",
    "nai-diffusion-4-5-curated-inpainting",
    "nai-diffusion-5-full",
    "nai-diffusion-5-curated",
    "nai-diffusion-5-full-inpainting",
}
V5_MODELS = {"nai-diffusion-5-full", "nai-diffusion-5-curated"}


@dataclass
class TestResult:
    name: str
    status: str
    http_status: int | None = None
    details: dict[str, Any] = field(default_factory=dict)
    output_files: list[str] = field(default_factory=list)


class LiveSuite:
    def __init__(self, token: str, output_dir: Path, timeout: float) -> None:
        self.token = token
        self.output_dir = output_dir
        self.timeout = timeout
        self.results: list[TestResult] = []
        self.session = requests.Session(impersonate="chrome")
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/150.0.0.0 Safari/537.36"
                ),
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.9",
                "Origin": "https://novelai.net",
                "Referer": "https://novelai.net/",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
            }
        )
        self.source_image: bytes | None = None
        self.source_width = 512
        self.source_height = 768
        self.v4_image: bytes | None = None
        self.v5_image: bytes | None = None
        self.vibe_token: str | None = None
        self.auth_failed = False

    def add(
        self,
        name: str,
        status: str,
        *,
        response: Any | None = None,
        details: dict[str, Any] | None = None,
        output_files: Iterable[Path] = (),
    ) -> None:
        http_status = getattr(response, "status_code", None)
        if http_status == 401:
            self.auth_failed = True
        self.results.append(
            TestResult(
                name=name,
                status=status,
                http_status=http_status,
                details=details or {},
                output_files=[str(path) for path in output_files],
            )
        )

    def safe_text(self, value: str, limit: int = 800) -> str:
        value = value[:limit].replace(self.token, "[REDACTED]")
        value = re.sub(
            r"(?i)(authorization\s*[:=]\s*(?:bearer\s+)?)\S+",
            r"\1[REDACTED]",
            value,
        )
        value = re.sub(r"(?i)\bpst-[A-Za-z0-9_-]+\b", "[REDACTED]", value)
        return value

    def response_details(self, response: Any) -> dict[str, Any]:
        content = bytes(getattr(response, "content", b""))
        details: dict[str, Any] = {"response_bytes": len(content)}
        if content:
            text = self.safe_text(content.decode("utf-8", errors="replace"))
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                details["body_preview"] = text
            else:
                if isinstance(payload, dict):
                    details["body_keys"] = sorted(str(key) for key in payload)
                    for key in ("message", "error", "detail", "statusCode", "code"):
                        if key in payload and isinstance(payload[key], (str, int, float)):
                            details[key] = self.safe_text(str(payload[key]))
                else:
                    details["body_type"] = type(payload).__name__
        return details

    def parse_text_stream(self, response: Any) -> tuple[str, int]:
        chunks: list[str] = []
        event_count = 0
        for raw in response.iter_lines():
            if isinstance(raw, bytes):
                raw = raw.decode("utf-8", errors="replace")
            if not raw or raw.startswith(":") or not raw.startswith("data:"):
                continue
            data = raw[5:].strip()
            if data == "[DONE]":
                continue
            try:
                payload = json.loads(data)
            except json.JSONDecodeError:
                continue
            event_count += 1
            if not isinstance(payload, dict):
                continue
            choices = payload.get("choices")
            if not isinstance(choices, list) or not choices or not isinstance(choices[0], dict):
                continue
            choice = choices[0]
            delta = choice.get("delta")
            if isinstance(delta, dict) and isinstance(delta.get("content"), str):
                chunks.append(delta["content"])
            elif isinstance(choice.get("text"), str):
                chunks.append(choice["text"])
        return "".join(chunks), event_count

    def request(
        self,
        method: str,
        url: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        accept: str | None = None,
        stream_response: bool = False,
    ) -> Any:
        headers = {"Authorization": f"Bearer {self.token}"}
        if accept:
            headers["Accept"] = accept
        response = self.session.request(
            method,
            url,
            json=json_body,
            params=params,
            headers=headers,
            timeout=self.timeout,
            stream=stream_response,
        )
        return response

    def no_auth_suite_guard(self) -> bool:
        if self.auth_failed:
            return False
        return True

    def account_tests(self) -> None:
        for name, path in (
            ("get_subscription", "/user/subscription"),
            ("get_user_data", "/user/data"),
        ):
            response = self.request("GET", f"{IMAGE_HOST}{path}")
            if response.ok:
                try:
                    payload = response.json()
                except ValueError:
                    self.add(name, "fail", response=response, details={"invalid_json": True})
                    continue
                details = {
                    "body_keys": sorted(payload) if isinstance(payload, dict) else [],
                    "json_type": type(payload).__name__,
                }
                if name == "get_subscription" and isinstance(payload, dict):
                    for key in ("tier", "active", "perStepUsage"):
                        if key in payload and isinstance(payload[key], (bool, int, str)):
                            details[key] = payload[key]
                self.add(name, "pass", response=response, details=details)
            else:
                self.add(name, "fail", response=response, details=self.response_details(response))

    def model_tests(self) -> list[str] | None:
        candidates = (
            "/oa/models",
            "/oa/v1/models",
            "/models",
            "/v1/models",
        )
        for path in candidates:
            response = self.request("GET", f"{TEXT_HOST}{path}")
            if not response.ok:
                continue
            try:
                payload = response.json()
            except ValueError:
                self.add("text_model_list", "fail", response=response, details={"invalid_json": True})
                return None
            ids: list[str] = []
            if isinstance(payload, dict) and isinstance(payload.get("data"), list):
                for item in payload["data"]:
                    if isinstance(item, dict) and isinstance(item.get("id"), str):
                        ids.append(item["id"])
            details = {"path": path, "model_ids": ids[:20], "model_count": len(ids)}
            self.add("text_model_list", "pass", response=response, details=details)
            return ids
        self.add(
            "text_model_list",
            "fail",
            details={"tried_paths": list(candidates)},
        )
        return None

    def text_completion_test(self, model: str) -> None:
        if not self.no_auth_suite_guard():
            self.add("text_completion_xialong", "skip", details={"reason": "authentication unavailable"})
            return
        candidates = (
            "/oa/v1/completions",
            "/oa/completions",
            "/v1/completions",
        )
        body = {
            "model": model,
            "prompt": "Reply with exactly NAI_TEXT_OK.",
            "max_tokens": 16,
            "temperature": 0.1,
            "stream": False,
        }
        for path in candidates:
            response = self.request("POST", f"{TEXT_HOST}{path}", json_body=body)
            if not response.ok:
                continue
            try:
                payload = response.json()
            except ValueError:
                self.add("text_completion_xialong", "fail", response=response, details={"invalid_json": True})
                return
            content = ""
            if isinstance(payload, dict):
                choices = payload.get("choices")
                if isinstance(choices, list) and choices and isinstance(choices[0], dict):
                    content = str(choices[0].get("text", ""))
            self.add(
                "text_completion_xialong",
                "pass" if content else "fail",
                response=response,
                details={"path": path, "model": model, "content_preview": self.safe_text(content, 200)},
            )
            return
        self.add(
            "text_completion_xialong",
            "fail",
            details={"model": model, "tried_paths": list(candidates)},
        )

    def text_chat_test(self, model: str, *, stream: bool) -> None:
        result_name = "text_chat_glm_stream" if stream else "text_chat_glm_nonstream"
        if not self.no_auth_suite_guard():
            self.add(result_name, "skip", details={"reason": "authentication unavailable"})
            return
        candidates = (
            "/oa/v1/chat/completions",
            "/oa/chat/completions",
            "/v1/chat/completions",
        )
        body = {
            "model": model,
            "messages": [{"role": "user", "content": "Reply with exactly NAI_TEXT_OK."}],
            "max_tokens": 16,
            "temperature": 0.1,
            "stream": stream,
            "enable_thinking": False,
        }
        for path in candidates:
            response = self.request(
                "POST",
                f"{TEXT_HOST}{path}",
                json_body=body,
                stream_response=stream,
            )
            if not response.ok:
                continue
            event_count = None
            if stream:
                try:
                    content, event_count = self.parse_text_stream(response)
                except (OSError, ValueError) as exc:
                    self.add(result_name, "fail", response=response, details={"stream_error": str(exc)})
                    return
            else:
                try:
                    payload = response.json()
                except ValueError:
                    self.add(result_name, "fail", response=response, details={"invalid_json": True})
                    return
                content = ""
                if isinstance(payload, dict):
                    choices = payload.get("choices")
                    if isinstance(choices, list) and choices and isinstance(choices[0], dict):
                        choice = choices[0]
                        content = str(choice.get("text", ""))
                        if not content and isinstance(choice.get("message"), dict):
                            content = str(choice["message"].get("content", ""))
            details = {
                "path": path,
                "model": model,
                "content_preview": self.safe_text(content, 200),
            }
            if event_count is not None:
                details["event_count"] = event_count
            self.add(
                result_name,
                "pass" if content else "fail",
                response=response,
                details=details,
            )
            return
        self.add(
            result_name,
            "fail",
            details={"model": model, "tried_paths": list(candidates)},
        )

    def text_tests(self, model_ids: list[str]) -> None:
        if not model_ids or not self.no_auth_suite_guard():
            self.add("text_generation_suite", "skip", details={"reason": "model discovery/auth unavailable"})
            return
        if "xialong-v1" in model_ids:
            self.text_completion_test("xialong-v1")
        if "glm-4-6" in model_ids:
            self.text_chat_test("glm-4-6", stream=True)
            self.text_chat_test("glm-4-6", stream=False)

    @staticmethod
    def image_model_is_v4(model: str) -> bool:
        return model in V4_MODELS

    @staticmethod
    def base64_bytes(data: bytes) -> str:
        return base64.b64encode(data).decode("ascii")

    def create_mask(self, width: int, height: int) -> bytes:
        image = Image.new("L", (width, height), 0)
        left = max(0, width // 3)
        top = max(0, height // 3)
        right = min(width, width * 2 // 3)
        bottom = min(height, height * 2 // 3)
        for x in range(left, right):
            for y in range(top, bottom):
                image.putpixel((x, y), 255)
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        return buffer.getvalue()

    def build_image_payload(
        self,
        *,
        model: str,
        prompt: str,
        negative_prompt: str = "",
        width: int = 512,
        height: int = 768,
        steps: int = 8,
        seed: int = 123456789,
        action: str = "generate",
        image: bytes | None = None,
        mask: bytes | None = None,
        strength: float | None = None,
        noise: float | None = None,
        characters: list[dict[str, Any]] | None = None,
        references: list[str] | None = None,
        reference_information: list[float] | None = None,
        reference_strengths: list[float] | None = None,
        straight_alpha: bool = False,
        inpaint_img2img_strength: int | None = None,
        extra_noise_seed: int | None = None,
    ) -> dict[str, Any]:
        characters = characters or []
        char_captions = [
            {
                "char_caption": item["prompt"],
                "centers": [item.get("center", {"x": 0.5, "y": 0.5})],
            }
            for item in characters
            if item.get("enabled", True)
        ]
        negative_char_captions = [
            {
                "char_caption": item.get("uc", ""),
                "centers": [item.get("center", {"x": 0.5, "y": 0.5})],
            }
            for item in characters
            if item.get("enabled", True) and item.get("uc")
        ]
        parameters: dict[str, Any] = {
            "width": width,
            "height": height,
            "n_samples": 1,
            "steps": steps,
            "scale": 5.0,
            "sampler": "k_euler_ancestral",
            "seed": seed,
            "negative_prompt": negative_prompt,
            "qualityToggle": True,
            "params_version": 4 if model in V5_MODELS else 3,
            "dynamic_thresholding": False,
            "cfg_rescale": 0.0,
            "noise_schedule": "karras",
            "add_original_image": True,
            "controlnet_strength": 1.0,
            "characterPrompts": characters,
            "autoSmea": False,
            "deliberate_euler_ancestral_bug": False,
            "legacy": False,
            "legacy_v3_extend": False,
            "prefer_brownian": True,
            "use_coords": bool(characters),
            "legacy_uc": False,
            "stream": "msgpack",
        }
        if model in V5_MODELS:
            parameters["ucPresetId"] = "heavy"
            parameters["qualityPresetId"] = "standard"
            parameters["straight_alpha"] = straight_alpha
        else:
            parameters["ucPreset"] = 0
            parameters["sm"] = False
            parameters["sm_dyn"] = False
            parameters["autoSmea"] = False
            parameters["normalize_reference_strength_multiple"] = True
        if image is not None:
            parameters["image"] = self.base64_bytes(image)
        if mask is not None:
            parameters["mask"] = self.base64_bytes(mask)
        if strength is not None:
            parameters["strength"] = strength
        if noise is not None:
            parameters["noise"] = noise
        if action in {"img2img", "infill"}:
            parameters["extra_noise_seed"] = extra_noise_seed or 987654321
        if references:
            parameters["reference_image_multiple"] = references
            parameters["reference_information_extracted_multiple"] = (
                reference_information or [1.0] * len(references)
            )
            parameters["reference_strength_multiple"] = (
                reference_strengths or [0.6] * len(references)
            )
        if model in V4_MODELS:
            if inpaint_img2img_strength is not None:
                parameters["inpaintImg2ImgStrength"] = inpaint_img2img_strength
            parameters["v4_prompt"] = {
                "caption": {
                    "base_caption": prompt,
                    "char_captions": char_captions,
                },
                "use_coords": bool(characters),
                "use_order": True,
            }
            parameters["v4_negative_prompt"] = {
                "caption": {
                    "base_caption": negative_prompt,
                    "char_captions": negative_char_captions,
                },
                "legacy_uc": False,
            }
        return {
            "action": action,
            "input": prompt,
            "model": model,
            "parameters": parameters,
        }

    @staticmethod
    def parse_zip_images(content: bytes) -> list[bytes]:
        if not content.startswith(b"PK"):
            return []
        images: list[bytes] = []
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            for name in archive.namelist():
                if name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    images.append(archive.read(name))
        return images

    @staticmethod
    def parse_msgpack_images(content: bytes) -> list[bytes]:
        images: list[bytes] = []
        offset = 0
        while offset + 4 <= len(content):
            frame_size = struct.unpack(">I", content[offset : offset + 4])[0]
            offset += 4
            if frame_size > 128 * 1024 * 1024 or offset + frame_size > len(content):
                raise ValueError("invalid or truncated MessagePack frame")
            value = msgpack.unpackb(content[offset : offset + frame_size], raw=False)
            offset += frame_size
            if not isinstance(value, dict):
                continue
            if value.get("event_type") == "final" and isinstance(value.get("image"), bytes):
                images.append(value["image"])
        if offset != len(content):
            raise ValueError("trailing bytes in MessagePack stream")
        return images

    def decode_images(self, content: bytes) -> list[bytes]:
        if content.startswith(b"PK"):
            return self.parse_zip_images(content)
        return self.parse_msgpack_images(content)

    def save_images(self, name: str, images: list[bytes]) -> list[Path]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        paths: list[Path] = []
        for index, data in enumerate(images):
            path = self.output_dir / f"{name}-{index + 1}.png"
            path.write_bytes(data)
            paths.append(path)
        return paths

    def generate_image(
        self,
        name: str,
        *,
        model: str,
        prompt: str,
        negative_prompt: str = "",
        action: str = "generate",
        image: bytes | None = None,
        mask: bytes | None = None,
        strength: float | None = None,
        noise: float | None = None,
        characters: list[dict[str, Any]] | None = None,
        references: list[str] | None = None,
        reference_information: list[float] | None = None,
        reference_strengths: list[float] | None = None,
        straight_alpha: bool = False,
        inpaint_img2img_strength: int | None = None,
    ) -> list[bytes]:
        payload = self.build_image_payload(
            model=model,
            prompt=prompt,
            negative_prompt=negative_prompt,
            action=action,
            image=image,
            mask=mask,
            strength=strength,
            noise=noise,
            characters=characters,
            references=references,
            reference_information=reference_information,
            reference_strengths=reference_strengths,
            straight_alpha=straight_alpha,
            inpaint_img2img_strength=inpaint_img2img_strength,
        )
        response = self.request(
            "POST",
            f"{IMAGE_HOST}/ai/generate-image-stream",
            json_body=payload,
            accept="application/x-msgpack",
        )
        if not response.ok:
            self.add(name, "fail", response=response, details=self.response_details(response))
            return []
        try:
            images = self.decode_images(bytes(response.content))
        except (ValueError, msgpack.ExtraData) as exc:
            self.add(name, "fail", response=response, details={"decode_error": str(exc)})
            return []
        paths = self.save_images(name, images)
        self.add(
            name,
            "pass" if images else "fail",
            response=response,
            details={"model": model, "image_count": len(images), "response_format": "msgpack_or_zip"},
            output_files=paths,
        )
        return images

    def encode_vibe(self) -> None:
        if not self.source_image or not self.no_auth_suite_guard():
            self.add("encode_vibe", "skip", details={"reason": "source image/auth unavailable"})
            return
        response = self.request(
            "POST",
            f"{IMAGE_HOST}/ai/encode-vibe",
            json_body={
                "image": self.base64_bytes(self.source_image),
                "information_extracted": 1.0,
                "model": "nai-diffusion-4-5-full",
            },
        )
        if response.ok:
            self.vibe_token = self.base64_bytes(bytes(response.content))
            self.add("encode_vibe", "pass", response=response, details={"token_received": True})
        else:
            self.add("encode_vibe", "fail", response=response, details=self.response_details(response))

    def upscale(self) -> None:
        if not self.source_image or not self.no_auth_suite_guard():
            self.add("upscale_image", "skip", details={"reason": "source image/auth unavailable"})
            return
        body = {
            "image": self.base64_bytes(self.source_image),
            "width": self.source_width,
            "height": self.source_height,
            "scale": 2,
        }
        tried: list[str] = []
        last_response: Any | None = None
        for host in (IMAGE_HOST, LEGACY_HOST):
            url = f"{host}/ai/upscale"
            tried.append(url)
            response = self.request("POST", url, json_body=body)
            last_response = response
            if not response.ok:
                continue
            content = bytes(response.content)
            try:
                images = [content] if content.startswith(b"\x89PNG") else self.parse_zip_images(content)
            except (OSError, zipfile.BadZipFile) as exc:
                self.add(
                    "upscale_image",
                    "fail",
                    response=response,
                    details={"decode_error": str(exc), "tried_paths": tried},
                )
                return
            paths = self.save_images("upscale", images)
            self.add(
                "upscale_image",
                "pass" if images else "fail",
                response=response,
                details={"image_count": len(images), "factor": 2, "path": url},
                output_files=paths,
            )
            return
        details = {"tried_paths": tried}
        if last_response is not None:
            details.update(self.response_details(last_response))
        self.add("upscale_image", "fail", response=last_response, details=details)

    def director(self, tool: str) -> None:
        if not self.source_image or not self.no_auth_suite_guard():
            self.add(f"director_{tool}", "skip", details={"reason": "source image/auth unavailable"})
            return
        prompt = ""
        if tool == "colorize":
            prompt = "blue hair, warm evening light"
        if tool == "emotion":
            prompt = "happy;;"
        image = Image.open(io.BytesIO(self.source_image))
        width, height = image.size
        response = self.request(
            "POST",
            f"{IMAGE_HOST}/ai/augment-image",
            json_body={
                "req_type": tool,
                "width": width,
                "height": height,
                "image": self.base64_bytes(self.source_image),
                "prompt": prompt,
                "defry": 0,
            },
        )
        if not response.ok:
            self.add(f"director_{tool}", "fail", response=response, details=self.response_details(response))
            return
        images = self.parse_zip_images(bytes(response.content))
        paths = self.save_images(f"director-{tool}", images)
        self.add(
            f"director_{tool}",
            "pass" if images else "fail",
            response=response,
            details={"tool": tool, "image_count": len(images)},
            output_files=paths,
        )

    def annotate(self) -> None:
        if not self.source_image or not self.no_auth_suite_guard():
            self.add("annotate_image", "skip", details={"reason": "source image/auth unavailable"})
            return
        response = self.request(
            "POST",
            f"{LEGACY_HOST}/ai/annotate-image",
            json_body={
                "model": "fake_scribble",
                "parameters": {"image": self.base64_bytes(self.source_image)},
            },
        )
        if not response.ok:
            self.add("annotate_image", "fail", response=response, details=self.response_details(response))
            return
        images = self.parse_zip_images(bytes(response.content))
        paths = self.save_images("annotate-fake-scribble", images)
        self.add(
            "annotate_image",
            "pass" if images else "fail",
            response=response,
            details={"model": "fake_scribble", "image_count": len(images)},
            output_files=paths,
        )

    def suggest_tags(self) -> None:
        if not self.no_auth_suite_guard():
            self.add("suggest_tags", "skip", details={"reason": "auth unavailable"})
            return
        response = self.request(
            "GET",
            f"{IMAGE_HOST}/ai/generate-image/suggest-tags",
            params={
                "model": "nai-diffusion-5-full",
                "prompt": "1girl, blue hai",
                "lang": "en",
            },
        )
        if not response.ok:
            self.add("suggest_tags", "fail", response=response, details=self.response_details(response))
            return
        try:
            payload = response.json()
        except ValueError:
            self.add("suggest_tags", "fail", response=response, details={"invalid_json": True})
            return
        tags = payload.get("tags") if isinstance(payload, dict) else None
        self.add(
            "suggest_tags",
            "pass" if isinstance(tags, list) else "fail",
            response=response,
            details={"tag_count": len(tags) if isinstance(tags, list) else 0},
        )

    def local_estimate(self) -> None:
        # This is intentionally a conservative, local-only marker. The MCP
        # server's own estimate tool should be used for the authoritative UI.
        estimated = max(1, round((512 * 768) / (832 * 1216) * 8 / 28 * 5))
        self.add(
            "local_cost_estimate",
            "pass",
            details={"width": 512, "height": 768, "steps": 8, "estimated_anlas_lower_bound": estimated},
        )

    def run(self) -> dict[str, Any]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.local_estimate()
        self.account_tests()
        if not self.no_auth_suite_guard():
            self.add("live_generation_suite", "skip", details={"reason": "authentication failed"})
            return self.report()

        model_ids = self.model_tests()
        self.text_tests(model_ids or [])
        self.suggest_tags()

        v5_images = self.generate_image(
            "v5-text-to-image",
            model="nai-diffusion-5-full",
            prompt="a small moonlit harbor, transparent background, detailed anime illustration",
            negative_prompt="blurry, low quality, text, watermark",
            straight_alpha=True,
        )
        if v5_images:
            self.v5_image = v5_images[0]
            self.source_image = self.v5_image
            image = Image.open(io.BytesIO(self.source_image))
            self.source_width, self.source_height = image.size

        v4_images = self.generate_image(
            "v45-multi-character",
            model="nai-diffusion-4-5-full",
            prompt="two people standing in a moonlit harbor",
            negative_prompt="blurry, bad anatomy, watermark",
            characters=[
                {
                    "prompt": "girl, silver hair, blue coat",
                    "uc": "bad hands",
                    "center": {"x": 0.3, "y": 0.5},
                    "enabled": True,
                },
                {
                    "prompt": "boy, black hair, red scarf",
                    "uc": "bad anatomy",
                    "center": {"x": 0.7, "y": 0.5},
                    "enabled": True,
                },
            ],
        )
        if v4_images:
            self.v4_image = v4_images[0]
            self.source_image = self.v4_image
            image = Image.open(io.BytesIO(self.source_image))
            self.source_width, self.source_height = image.size

        if self.source_image:
            mask = self.create_mask(self.source_width, self.source_height)
            i2i_images = self.generate_image(
                "image-to-image",
                model="nai-diffusion-4-5-full",
                action="img2img",
                prompt="same scene, gentle watercolor lighting",
                negative_prompt="blurry, watermark",
                image=self.source_image,
                strength=0.25,
                noise=0.0,
            )
            if i2i_images:
                self.source_image = i2i_images[0]
            self.generate_image(
                "inpaint",
                model="nai-diffusion-4-5-full-inpainting",
                action="infill",
                prompt="a small blue flower in the selected area",
                negative_prompt="blurry, watermark",
                image=self.source_image,
                mask=mask,
                strength=0.25,
                noise=0.0,
                inpaint_img2img_strength=1,
            )
            self.encode_vibe()
            if self.vibe_token:
                self.generate_image(
                    "vibe-transfer",
                    model="nai-diffusion-4-5-full",
                    prompt="a quiet mountain shrine at dawn",
                    negative_prompt="blurry, watermark",
                    references=[self.vibe_token],
                    reference_information=[0.7],
                    reference_strengths=[0.6],
                )
            self.upscale()
            self.annotate()
            for tool in ("lineart", "sketch", "bg-removal", "declutter", "colorize", "emotion"):
                self.director(tool)
        else:
            self.add("image_dependent_suite", "skip", details={"reason": "no source image generated"})
        return self.report()

    def report(self) -> dict[str, Any]:
        counts: dict[str, int] = {}
        for result in self.results:
            counts[result.status] = counts.get(result.status, 0) + 1
        return {
            "schema_version": 1,
            "created_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "token_configured": True,
            "tests": [
                {
                    "name": result.name,
                    "status": result.status,
                    "http_status": result.http_status,
                    "details": result.details,
                    "output_files": result.output_files,
                }
                for result in self.results
            ],
            "summary": counts,
            "security": {
                "token_persisted": False,
                "token_printed": False,
                "report_redacted": True,
            },
        }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="live-test-output")
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args(argv)
    token = os.environ.get("NOVELAI_TOKEN", "").strip()
    if not token:
        print("NOVELAI_TOKEN is not configured", file=sys.stderr)
        return 2
    output_dir = Path(args.output_dir).expanduser().resolve()
    suite = LiveSuite(token=token, output_dir=output_dir, timeout=args.timeout)
    try:
        report = suite.run()
    except Exception as exc:  # pragma: no cover - protects live diagnostics
        suite.add(
            "live_generation_suite",
            "fail",
            details={"exception_type": type(exc).__name__},
        )
        report = suite.report()
    report_path = output_dir / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"report": str(report_path), "summary": report["summary"]}, ensure_ascii=False))
    return 0 if report["summary"].get("fail", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
