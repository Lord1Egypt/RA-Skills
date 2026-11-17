"""Normalize a local, bounded screenshot into a static work preview."""

from io import BytesIO
from pathlib import Path


def cover(path):
    try:
        from PIL import Image, ImageOps, UnidentifiedImageError
    except ImportError:
        raise RuntimeError(
            "Cover conversion needs optional Pillow: python3 -m pip install Pillow"
        ) from None
    path = Path(path).expanduser()
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 5 * 1024 * 1024:
        raise RuntimeError("Preview must be a regular PNG, JPEG or WebP file up to 5 MiB")
    try:
        with path.open("rb") as stream:
            raw = stream.read(5 * 1024 * 1024 + 1)
        if len(raw) > 5 * 1024 * 1024:
            raise ValueError("Preview grew while reading")
        with Image.open(BytesIO(raw), formats=["PNG", "JPEG", "WEBP"]) as source:
            if source.width * source.height > 16_000_000 or getattr(source, "n_frames", 1) != 1:
                raise ValueError("Use a static image up to 16 million pixels")
            image = ImageOps.exif_transpose(source).convert("RGB")
            image.thumbnail((1600, 1200))
            output = BytesIO()
            image.save(output, format="WEBP", quality=80, method=6)
        data = output.getvalue()
        if len(data) > 512 * 1024:
            raise ValueError("Preview exceeds 512 KiB; use a smaller screenshot")
        return data
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError) as exc:
        raise RuntimeError(
            "Use a valid static PNG, JPEG or WebP preview within the size limits"
        ) from exc
