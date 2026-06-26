from __future__ import annotations
"""
image_gen.py — Image generation wrapper for hum content creation.

Wraps scripts/lib/image-gen/generate.py so it can be called
as a Python module without subprocess.

Provider is resolved from: explicit arg > HUM_IMAGE_MODEL env > openclaw.json > "gemini".
Visual style from VOICE.md is auto-injected when no style arg is given.

Usage:
    from create.image_gen import generate_image
    path = generate_image("split screen finance illustration", platform="twitter")
"""

import base64
import json
import os
import sys
from pathlib import Path

# Path to the image-gen lib (bundled inside hum)
_IMAGE_GEN_DIR = Path(__file__).resolve().parent.parent / "lib" / "image-gen"

if str(_IMAGE_GEN_DIR) not in sys.path:
    sys.path.insert(0, str(_IMAGE_GEN_DIR))

from generate import generate_image as _generate_image  # noqa: E402


def _resolve_provider(provider: str | None) -> str:
    """Resolve provider from arg, config, or default."""
    if provider:
        return provider
    # Lazy import to avoid circular deps at module load
    from scripts.config import load_config
    return load_config().get("image_model", "gemini")


def _resolve_style(style: str | None) -> str | None:
    """Load visual style from VOICE.md if no explicit style given."""
    if style is not None:
        return style
    from scripts.config import load_config, load_visual_style
    cfg = load_config()
    return load_visual_style(cfg["data_dir"])


# ── Public API ───────────────────────────────────────────────────────────────


PLATFORM_SIZES = {
    "x":            (1200, 675),
    "twitter":      (1200, 675),
    "linkedin":     (1200, 627),
    "instagram":    (1080, 1080),
    "facebook":     (1200, 630),
    "1:1":          (1024, 1024),
    "16:9":         (1920, 1080),
    "9:16":         (1080, 1920),
}


def generate_image(
    prompt: str,
    *,
    provider: str | None = None,
    platform: str | None = None,
    size: tuple[int, int] | None = None,
    model: str | None = None,
    style: str | None = None,
    no_enhance: bool = False,
    output_path: str | None = None,
) -> str:
    """
    Generate an image and return the path to the saved file.

    Args:
        prompt: Image description
        provider: "gemini", "openai", "grok", "minimax" (default from config)
        platform: Target platform (auto-selects size) — use "twitter" for X posts
        size: W×H tuple, overrides platform
        model: Provider-specific model override
        style: Style directive (defaults to VOICE.md Visual Style)
        no_enhance: Skip LLM prompt enhancement
        output_path: Save to this path instead of temp file

    Returns:
        Path to the generated image file.

    Raises:
        RuntimeError: If generation fails
    """
    resolved_provider = _resolve_provider(provider)
    resolved_style = _resolve_style(style)

    # Map "x" to "twitter" for generate.py platform presets
    platform_arg = platform
    if platform_arg == "x":
        platform_arg = "twitter"

    # Resolve size string
    if size is None and platform:
        size = PLATFORM_SIZES.get(platform)
    size_str = f"{size[0]}x{size[1]}" if size else None

    if output_path is None:
        output_path = f"/tmp/hum-image-{os.getpid()}.png"

    saved = _generate_image(
        prompt=prompt,
        platform=platform_arg,
        output_path=output_path,
        provider=resolved_provider,
        size=size_str,
        model=model,
        style=resolved_style,
        no_enhance=no_enhance,
    )

    if not Path(output_path).exists():
        raise RuntimeError(f"Image was not saved to {output_path}")

    return saved or output_path


def generate_image_json(
    prompt: str,
    *,
    provider: str | None = None,
    platform: str | None = None,
    size: tuple[int, int] | None = None,
    model: str | None = None,
    style: str | None = None,
    no_enhance: bool = False,
) -> dict:
    """
    Generate an image and return full metadata as a JSON dict.

    Returns:
        {
            "success": True,
            "provider": str,
            "model": str,
            "size": (w, h),
            "prompt": original prompt,
            "enhanced_prompt": str | None,
            "revised_prompt": str | None,
            "image_b64": base64-encoded PNG,
            "image_path": temp file path,
        }
    """
    import io

    resolved_provider = _resolve_provider(provider)
    resolved_style = _resolve_style(style)

    if size is None and platform:
        size = PLATFORM_SIZES.get(platform)
    size_str = f"{size[0]}x{size[1]}" if size else None

    # Capture the JSON printed to stdout by emit_json=True
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        _generate_image(
            prompt=prompt,
            platform=platform,
            output_path=None,
            provider=resolved_provider,
            size=size_str,
            model=model,
            style=resolved_style,
            no_enhance=no_enhance,
            emit_json=True,
        )
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

    data = json.loads(output)

    # Write temp file from b64 payload
    if data.get("success") and data.get("image_b64"):
        img_bytes = base64.b64decode(data["image_b64"])
        img_path = f"/tmp/hum-image-{os.getpid()}.png"
        Path(img_path).write_bytes(img_bytes)
        data["image_path"] = img_path

    return data
