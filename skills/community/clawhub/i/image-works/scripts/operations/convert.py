"""
Format conversion for image-works.
Supports JPEG ↔ PNG ↔ WebP ↔ TIFF bidirectional conversion.
"""
import io
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


# Format mapping for PIL
FORMAT_MAP = {
    "jpeg": "JPEG",
    "jpg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "tiff": "TIFF",
    "tif": "TIFF",
    "bmp": "BMP",
    "gif": "GIF",
}

# Formats that support transparency
TRANSPARENT_FORMATS = {"PNG", "WEBP", "GIF"}


def convert_image(image, target_format: str,
                  quality: Optional[int] = None,
                  original_format: str = "JPEG") -> Dict:
    """
    Convert an image to a different format.
    
    Args:
        image: PIL Image object.
        target_format: Target format ('jpeg', 'png', 'webp', 'tiff').
        quality: Output quality (JPEG/WebP only).
        original_format: Original format for baseline.
        
    Returns:
        Dict with 'bytes' (converted data) and 'format'.
    """
    from PIL import Image
    
    fmt = FORMAT_MAP.get(target_format.lower(), "JPEG").upper()
    
    # Handle transparency
    if fmt not in TRANSPARENT_FORMATS and image.mode in ("RGBA", "LA", "P"):
        # Need to add white background for opaque formats
        background = Image.new("RGB", image.size, (255, 255, 255))
        if image.mode == "P":
            image = image.convert("RGBA")
        background.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
        image = background
    
    # Convert to RGB for JPEG
    if fmt == "JPEG" and image.mode != "RGB":
        image = image.convert("RGB")
    
    # Convert mode if needed for other formats
    if fmt in TRANSPARENT_FORMATS and image.mode not in ("RGBA", "LA", "P"):
        if fmt == "PNG":
            image = image.convert("RGBA")
    
    buf = io.BytesIO()
    save_kwargs = {"format": fmt}
    
    if fmt in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality if quality is not None else 90
        save_kwargs["optimize"] = True
    
    if fmt == "PNG":
        save_kwargs["optimize"] = True
    
    image.save(buf, **save_kwargs)
    
    return {
        "bytes": buf.getvalue(),
        "format": fmt.lower(),
        "mode": image.mode,
        "dimensions": image.size,
    }


def get_target_extension(target_format: str) -> str:
    """Get the file extension for a target format."""
    fmt_map = {
        "jpeg": ".jpg",
        "jpg": ".jpg",
        "png": ".png",
        "webp": ".webp",
        "tiff": ".tiff",
        "bmp": ".bmp",
        "gif": ".gif",
    }
    return fmt_map.get(target_format.lower(), ".bin")
