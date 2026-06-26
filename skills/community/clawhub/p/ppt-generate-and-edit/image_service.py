"""Image generation service abstraction used by PPT modules."""

from __future__ import annotations

import base64
from pathlib import Path

from .utils import ensure_directory, get_logger, timestamp_str

logger = get_logger(__name__)

# 1x1 transparent PNG, used as deterministic mock output.
_MOCK_PNG_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8"
    "/x8AAusB9oN8nKQAAAAASUVORK5CYII="
)


def generate_image(
    prompt: str,
    output_dir: str | Path = "ppt_skill/generated_images",
    backend: str = "mock",
) -> str:
    """Generate an image and return the local image file path.

    The default implementation is a mock backend to keep this skill runnable
    without external dependencies. Future backends can be added for DALL·E
    and local Stable Diffusion services.
    """
    safe_dir = ensure_directory(output_dir)
    output_path = safe_dir / f"img_{timestamp_str()}.png"

    logger.info("generate_image called with backend=%s prompt=%s", backend, prompt)
    if backend == "mock":
        output_path.write_bytes(base64.b64decode(_MOCK_PNG_BASE64))
        logger.info("mock image generated at %s", output_path)
        return str(output_path)

    if backend == "dalle":
        raise NotImplementedError("TODO: integrate with DALL·E API backend.")
    if backend == "stable_diffusion":
        raise NotImplementedError(
            "TODO: integrate with local Stable Diffusion service."
        )
    raise ValueError(f"Unsupported backend: {backend}")
