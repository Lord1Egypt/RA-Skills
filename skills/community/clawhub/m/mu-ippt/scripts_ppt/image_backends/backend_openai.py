#!/usr/bin/env python3
"""
OpenAI DALL-E image generation backend.

Requires:
  OPENAI_API_KEY   Your OpenAI API key

Optional:
  OPENAI_IMAGE_MODEL   Model name (default: dall-e-3)
  OPENAI_BASE_URL      Override API base URL
"""

import json
import os
import time
from pathlib import Path

import requests

from image_backends.backend_common import (
    MAX_RETRIES,
    download_image,
    is_rate_limit_error,
    require_api_key,
    resolve_output_path,
    retry_delay,
)


# Aspect-ratio → DALL-E 3 size mapping
ASPECT_RATIO_SIZES = {
    "1:1": "1024x1024",
    "16:9": "1792x1024",
    "9:16": "1024x1792",
    "3:2": "1792x1024",
    "2:3": "1024x1792",
    "4:3": "1792x1024",
    "3:4": "1024x1792",
}

DEFAULT_SIZE = "1024x1024"


def _resolve_size(aspect_ratio: str, image_size: str) -> str:
    """Map aspect_ratio to a DALL-E 3 supported size string."""
    return ASPECT_RATIO_SIZES.get(aspect_ratio, DEFAULT_SIZE)


def _generate_image(
    prompt: str,
    negative_prompt: str | None = None,
    aspect_ratio: str = "1:1",
    image_size: str = "1K",
    output_dir: str | None = None,
    filename: str | None = None,
    model: str | None = None,
) -> str:
    """Call the OpenAI Images API and return the saved file path."""
    api_key = require_api_key(
        "OPENAI_API_KEY",
        message="OPENAI_API_KEY environment variable is required for the openai backend.",
    )
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model_name = model or os.environ.get("OPENAI_IMAGE_MODEL", "dall-e-3")
    size = _resolve_size(aspect_ratio, image_size)

    full_prompt = prompt
    if negative_prompt:
        full_prompt = f"{prompt}. Avoid: {negative_prompt}"

    print("[OpenAI Image]")
    print(f"  Prompt:   {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print(f"  Model:    {model_name}")
    print(f"  Size:     {size}")
    print()
    print("  [..] Generating...", end="", flush=True)
    start = time.time()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model_name,
        "prompt": full_prompt,
        "n": 1,
        "size": size,
        "response_format": "url",
    }

    resp = requests.post(
        f"{base_url}/images/generations",
        headers=headers,
        json=payload,
        timeout=180,
    )

    elapsed = time.time() - start
    print(f"\n  [DONE] Response received ({elapsed:.1f}s)")

    if resp.status_code != 200:
        raise RuntimeError(f"OpenAI API HTTP {resp.status_code}: {resp.text[:300]}")

    data = resp.json()
    image_url = data.get("data", [{}])[0].get("url", "")
    if not image_url:
        raise RuntimeError(f"OpenAI API returned no image URL: {json.dumps(data)[:300]}")

    # Download and save
    print("  [..] Downloading image...", end="", flush=True)
    ext = ".png"
    path = resolve_output_path(prompt, output_dir, filename, ext)
    download_image(image_url, path)
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
    """Generate an image with retries using the OpenAI backend."""
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

    raise RuntimeError(f"OpenAI: Failed after {max_retries + 1} attempts. Last error: {last_error}")
