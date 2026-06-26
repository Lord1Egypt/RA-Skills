"""
providers.py — Multi-provider image generation interface.

Each provider implements the ImageProvider protocol.
Easy to add new providers: implement generate() and register in get_provider().

Supported providers: gemini, openai, grok (xAI), minimax.
API keys are loaded from environment variables only (set directly or via
openclaw.json → env.vars).
"""

from __future__ import annotations

import base64
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ── Data types ────────────────────────────────────────────────────────────────

@dataclass
class ImageResult:
    """Result from an image generation call."""
    image_bytes: bytes
    mime_type: str = "image/png"
    revised_prompt: str | None = None  # Some providers return an improved prompt
    model: str | None = None
    provider: str | None = None


# ── Provider interface ───────────────────────────────────────────────────────

class ImageProvider(ABC):
    """Base class for all image generation providers."""

    name: str = "base"
    supports_size: bool = True      # False if provider only supports certain sizes
    supports_revision: bool = False  # True if provider can revise the prompt

    @abstractmethod
    def generate(
        self,
        prompt: str,
        size: tuple[int, int] | None = None,
        model: str | None = None,
        style: str | None = None,
        **kwargs,
    ) -> ImageResult:
        """Generate an image. Raises on failure."""
        ...


# ─────────────────────────────────────────────────────────────────────────────
# Gemini — Google Gemini Flash Image
# ─────────────────────────────────────────────────────────────────────────────

class GeminiProvider(ImageProvider):
    """
    Google Gemini image generation.

    API: https://ai.google.dev/gemini-api/docs/image-generation
    Key: GEMINI_API_KEY env var
    """

    name = "gemini"
    supports_revision = True

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")

    def generate(
        self,
        prompt: str,
        size: tuple[int, int] | None = None,
        model: str | None = None,
        style: str | None = None,
        **kwargs,
    ) -> ImageResult:
        import urllib.request
        import json

        model = model or os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
        url = f"{self.BASE_URL}/{model}:generateContent?key={self.api_key}"

        full_prompt = prompt
        if style:
            full_prompt = f"{prompt}. Style: {style}"

        gen_config: dict = {"responseModalities": ["TEXT", "IMAGE"]}

        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": gen_config,
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            raise RuntimeError(f"Gemini API error {e.code}: {body[:500]}") from e

        parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])

        image_bytes = None
        mime_type = "image/png"
        revised = None

        for part in parts:
            if part.get("inlineData"):
                data_str = part["inlineData"]["data"]
                try:
                    import base64 as b64mod
                    image_bytes = b64mod.b64decode(data_str)
                except Exception:
                    image_bytes = bytes.fromhex(data_str)
                mime_type = part["inlineData"].get("mimeType", "image/png")
            if part.get("text"):
                revised = part["text"]

        if not image_bytes:
            reason = data.get("promptFeedback", {}).get("blockReason", "no image returned")
            raise RuntimeError(f"Gemini blocked or returned no image: {reason}")

        return ImageResult(
            image_bytes=image_bytes,
            mime_type=mime_type,
            revised_prompt=revised,
            model=model,
            provider=self.name,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Grok — xAI image generation API
# ─────────────────────────────────────────────────────────────────────────────

class GrokProvider(ImageProvider):
    """
    xAI Grok image generation via the OpenAI-compatible API.

    API: https://docs.x.ai/docs/guides/image-generation
    Key: XAI_API_KEY env var
    """

    name = "grok"
    supports_revision = False

    BASE_URL = "https://api.x.ai/v1"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("XAI_API_KEY", "")

    def generate(
        self,
        prompt: str,
        size: tuple[int, int] | None = None,
        model: str | None = None,
        style: str | None = None,
        **kwargs,
    ) -> ImageResult:
        import urllib.request
        import json

        w, h = size or (1024, 1024)
        size_str = f"{w}x{h}"

        model_name = model or "grok-2-image"

        full_prompt = prompt
        if style:
            full_prompt = f"{prompt}. Style: {style}"

        url = f"{self.BASE_URL}/images/generations"
        payload = {
            "model": model_name,
            "prompt": full_prompt,
            "n": 1,
            "size": size_str,
            "response_format": "b64_json",
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Grok API error {e.code}: {e.read().decode()[:500]}") from e

        b64 = data.get("data", [{}])[0].get("b64_json", "")
        if not b64:
            raise RuntimeError("Grok returned no image data")

        return ImageResult(
            image_bytes=base64.b64decode(b64),
            mime_type="image/png",
            model=model_name,
            provider=self.name,
        )


# ─────────────────────────────────────────────────────────────────────────────
# MiniMax — MiniMax AI image generation API
# ─────────────────────────────────────────────────────────────────────────────

class MiniMaxProvider(ImageProvider):
    """
    MiniMax image generation API.

    API: https://www.minimaxi.com/document/Image-Generation
    Key: MINIMAX_API_KEY env var
    """

    name = "minimax"

    BASE_URL = "https://api.minimax.chat/v1"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")

    def generate(
        self,
        prompt: str,
        size: tuple[int, int] | None = None,
        model: str | None = None,
        style: str | None = None,
        **kwargs,
    ) -> ImageResult:
        import urllib.request
        import json

        w, h = size or (1024, 1024)
        model_name = model or "image-01"

        full_prompt = prompt
        if style:
            full_prompt = f"{prompt}. Style: {style}"

        url = f"{self.BASE_URL}/image_generation"
        payload = {
            "model": model_name,
            "prompt": full_prompt,
            "width": w,
            "height": h,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"MiniMax API error {e.code}: {e.read().decode()[:500]}") from e

        base64_data = data.get("data", {}).get("base64_image", "")
        if not base64_data:
            raise RuntimeError(f"MiniMax returned no image data: {json.dumps(data)[:300]}")

        return ImageResult(
            image_bytes=base64.b64decode(base64_data.lstrip()),
            mime_type="image/png",
            revised_prompt=data.get("revised_prompt"),
            model=model_name,
            provider=self.name,
        )


# ─────────────────────────────────────────────────────────────────────────────
# OpenAI — GPT Image / DALL-E
# ─────────────────────────────────────────────────────────────────────────────

class OpenAIProvider(ImageProvider):
    """
    OpenAI image generation (gpt-image-1, dall-e-3).

    API: https://platform.openai.com/docs/guides/images
    Key: OPENAI_API_KEY env var
    """

    name = "openai"
    supports_revision = True

    BASE_URL = "https://api.openai.com/v1"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")

    def generate(
        self,
        prompt: str,
        size: tuple[int, int] | None = None,
        model: str | None = None,
        style: str | None = None,
        **kwargs,
    ) -> ImageResult:
        import urllib.request
        import json

        w, h = size or (1024, 1024)
        size_str = f"{w}x{h}"

        model_name = model or "gpt-image-1"

        url = f"{self.BASE_URL}/images/generations"
        payload = {
            "model": model_name,
            "prompt": prompt,
            "n": 1,
            "size": size_str,
            "response_format": "b64_json",
        }

        # style param is only supported by dall-e-3
        if model_name == "dall-e-3":
            payload["style"] = style or "vivid"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"OpenAI API error {e.code}: {e.read().decode()[:500]}") from e

        b64 = data.get("data", [{}])[0].get("b64_json", "")
        if not b64:
            raise RuntimeError("OpenAI returned no image data")

        return ImageResult(
            image_bytes=base64.b64decode(b64),
            mime_type="image/png",
            revised_prompt=data.get("data", [{}])[0].get("revised_prompt"),
            model=model_name,
            provider=self.name,
        )


# ─────────────────────────────────────────────────────────────────────────────
# Provider registry
# ─────────────────────────────────────────────────────────────────────────────

_PROVIDERS: dict[str, type[ImageProvider]] = {
    "gemini": GeminiProvider,
    "grok": GrokProvider,
    "minimax": MiniMaxProvider,
    "openai": OpenAIProvider,
}


def get_provider(name: str) -> ImageProvider:
    """Return an instance of the named provider. Raises KeyError if unknown."""
    cls = _PROVIDERS[name.lower()]
    return cls()


def register_provider(cls: type[ImageProvider]) -> None:
    """Register a new provider. Call before get_provider()."""
    _PROVIDERS[cls.name] = cls


def list_providers() -> list[str]:
    """Return names of all available providers."""
    return list(_PROVIDERS.keys())
