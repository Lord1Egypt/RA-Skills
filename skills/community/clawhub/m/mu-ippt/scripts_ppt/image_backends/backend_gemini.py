#!/usr/bin/env python3
"""
Google Gemini (Imagen) image generation backend.

Requires:
  GEMINI_API_KEY   Your Google AI API key

Optional:
  GEMINI_IMAGE_MODEL   Model name (default: imagen-3.0-generate-002)
  GEMINI_BASE_URL      Override API base URL
"""

import base64
import json
import os
import time
from pathlib import Path

import requests

from image_backends.backend_common import (
    MAX_RETRIES,
    is_rate_limit_error,
    resolve_output_path,
    report_resolution,
    retry_delay,
    save_image_bytes,
    require_api_key,
)


# Aspect-ratio → Imagen aspect ratio string
ASPECT_RATIO_MAP = {
    "1:1": "1:1",
    "16:9": "16:9",
    "9:16": "9:16",
    "4:3": "4:3",
    "3:4": "3:4",
    "3:2": "3:2",
    "2:3": "2:3",
}

DEFAULT_ASPECT = "1:1"


def _generate_image(
    prompt: str,
    negative_prompt: str | None = None,
    aspect_ratio: str = "1:1",
    image_size: str = "1K",
    output_dir: str | None = None,
    filename: str | None = None,
    model: str | None = None,
) -> str:
    """Call the Gemini/Imagen API and return the saved file path."""
    api_key = require_api_key(
        "GEMINI_API_KEY",
        message="GEMINI_API_KEY environment variable is required for the gemini backend.",
    )
    base_url = os.environ.get(
        "GEMINI_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta"
    ).rstrip("/")
    model_name = model or os.environ.get("GEMINI_IMAGE_MODEL", "imagen-3.0-generate-002")
    imagen_aspect = ASPECT_RATIO_MAP.get(aspect_ratio, DEFAULT_ASPECT)

    full_prompt = prompt
    if negative_prompt:
        full_prompt = f"{prompt}. Avoid: {negative_prompt}"

    print("[Gemini Image]")
    print(f"  Prompt:       {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print(f"  Model:        {model_name}")
    print(f"  Aspect Ratio: {imagen_aspect}")
    print()
    print("  [..] Generating...", end="", flush=True)
    start = time.time()

    url = f"{base_url}/models/{model_name}:predict?key={api_key}"
    payload = {
        "instances": [{"prompt": full_prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": imagen_aspect,
        },
    }

    resp = requests.post(url, json=payload, timeout=180)

    elapsed = time.time() - start
    print(f"\n  [DONE] Response received ({elapsed:.1f}s)")

    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API HTTP {resp.status_code}: {resp.text[:300]}")

    data = resp.json()
    predictions = data.get("predictions", [])
    if not predictions:
        raise RuntimeError(f"Gemini API returned no predictions: {json.dumps(data)[:300]}")

    # Decode base64 image
    b64_data = predictions[0].get("bytesBase64Encoded", "")
    mime_type = predictions[0].get("mimeType", "image/png")
    if not b64_data:
        raise RuntimeError(f"Gemini API returned empty image data: {json.dumps(data)[:300]}")

    image_bytes = base64.b64decode(b64_data)
    ext = ".png" if "png" in mime_type else ".jpg"
    path = resolve_output_path(prompt, output_dir, filename, ext)
    save_image_bytes(image_bytes, path, content_type=mime_type)
    return path


def generate(
    prompt: str,
    negative_prompt: str | None = None,
    aspect_ratio: str = "1:1",
    image_size: str = "1K",
    output_dir: str | None = None,
    filename: str | None = None,
    model: str | None = None,
    max_retries: int = MAX_RETRIES,
) -> str:
    """Generate an image with retries using the Gemini backend."""
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return _generate_image(
                prompt=prompt,
                negative_prompt=negative_prompt,
                aspect_ratio=aspect_ratio,
                image_size=image_size,
                output_dir=output_dir,
                filename=filename,
                model=model,
            )
        except Exception as exc:
            last_error = exc
            if attempt >= max_retries:
                break
            limited = is_rate_limit_error(exc)
            delay = retry_delay(attempt, rate_limited=limited)
            label = "Rate limit hit" if limited else f"Error: {exc}"
            print(f"\n  [WARN] {label}. Retrying in {delay}s...")
            time.sleep(delay)

    raise RuntimeError(f"Gemini: Failed after {max_retries + 1} attempts. Last error: {last_error}")
