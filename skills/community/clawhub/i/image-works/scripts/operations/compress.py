"""
Compress operation for image-works.
Supports quality compression, target-size compression, and lossless compression.
"""
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def compress_image(image, quality: Optional[int] = None,
                   target_size_kb: Optional[int] = None,
                   lossless: bool = False,
                   format: str = "JPEG") -> Dict:
    """
    Compress an image using quality or target size.
    
    Args:
        image: PIL Image object.
        quality: Quality value 1-100 (default: 85 for lossy, None for lossless).
        target_size_kb: Target file size in KB (uses binary search).
        lossless: Whether to use lossless compression (PNG/WebP lossless).
        format: Output format ('JPEG', 'PNG', 'WEBP').
        
    Returns:
        Dict with 'bytes' (compressed image data) and 'quality' used.
    """
    import io
    from PIL import Image
    
    if lossless:
        # Lossless mode
        buf = io.BytesIO()
        save_kwargs = {"format": format}
        
        if format == "PNG":
            save_kwargs["optimize"] = True
        elif format == "WEBP":
            save_kwargs["lossless"] = True
        elif format == "JPEG":
            # JPEG doesn't support true lossless, use quality 100
            save_kwargs["quality"] = 100
            save_kwargs["optimize"] = True
        
        image.save(buf, **save_kwargs)
        return {"bytes": buf.getvalue(), "quality": 100, "method": "lossless"}
    
    if target_size_kb:
        return _compress_to_target(image, target_size_kb, format)
    
    # Standard quality compression
    effective_quality = quality if quality is not None else 85
    
    buf = io.BytesIO()
    save_kwargs = {"format": format, "optimize": True}
    
    if format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = effective_quality
    
    image.save(buf, **save_kwargs)
    return {"bytes": buf.getvalue(), "quality": effective_quality, "method": "quality"}


def _compress_to_target(image, target_kb: int, format: str) -> Dict:
    """
    Binary search to find quality that achieves target file size.
    
    Args:
        image: PIL Image.
        target_kb: Target size in KB.
        format: Output format.
        
    Returns:
        Dict with 'bytes' and 'quality'.
    """
    import io
    from PIL import Image
    
    low, high = 1, 95
    best_quality = high
    best_bytes = None
    
    for _ in range(8):  # Binary search iterations
        mid = (low + high) // 2
        buf = io.BytesIO()
        
        save_kwargs = {"format": format, "optimize": True}
        if format in ("JPEG", "WEBP"):
            save_kwargs["quality"] = mid
        
        image.save(buf, **save_kwargs)
        size_kb = buf.tell() / 1024
        
        if size_kb <= target_kb:
            best_quality = mid
            best_bytes = buf.getvalue()
            low = mid + 1
        else:
            high = mid - 1
        
        if low > high:
            break
    
    if best_bytes is None:
        # Even lowest quality exceeds target
        buf = io.BytesIO()
        save_kwargs = {"format": format, "optimize": True}
        if format in ("JPEG", "WEBP"):
            save_kwargs["quality"] = 1
        image.save(buf, **save_kwargs)
        return {"bytes": buf.getvalue(), "quality": 1, "method": "target_size",
                "warning": f"Target size {target_kb}KB not achievable at quality=1"}
    
    return {"bytes": best_bytes, "quality": best_quality, "method": "target_size"}


def auto_quality(image, format: str = "JPEG", min_acceptable_ssim: float = 0.95) -> Dict:
    """
    Smart compression: find optimal quality that preserves visual quality.
    
    Uses a simplified approach: tries quality=85, checks file size ratio,
    then adjusts.
    
    Args:
        image: PIL Image.
        format: Output format.
        min_acceptable_ssim: Not used directly (requires SSIM computation).
        
    Returns:
        Dict with 'bytes' and 'quality'.
    """
    import io
    from PIL import Image
    
    # Strategy: start at 85, go down if the file is large
    sizes_at_quality = {}
    
    for q in [85, 75, 60]:
        buf = io.BytesIO()
        save_kwargs = {"format": format, "optimize": True}
        if format in ("JPEG", "WEBP"):
            save_kwargs["quality"] = q
        image.save(buf, **save_kwargs)
        sizes_at_quality[q] = buf.tell()
    
    # Find best balance
    max_size = sizes_at_quality[85]
    threshold = 500 * 1024  # 500KB threshold
    
    if max_size > threshold:
        # Large image: try lower quality
        for q in [75, 60]:
            if sizes_at_quality[q] <= threshold:
                buf = io.BytesIO()
                save_kwargs = {"format": format, "optimize": True}
                if format in ("JPEG", "WEBP"):
                    save_kwargs["quality"] = q
                image.save(buf, **save_kwargs)
                return {"bytes": buf.getvalue(), "quality": q, "method": "auto"}
    
    # Use quality 85 as default
    buf = io.BytesIO()
    save_kwargs = {"format": format, "optimize": True}
    if format in ("JPEG", "WEBP"):
        save_kwargs["quality"] = 85
    image.save(buf, **save_kwargs)
    return {"bytes": buf.getvalue(), "quality": 85, "method": "auto"}
