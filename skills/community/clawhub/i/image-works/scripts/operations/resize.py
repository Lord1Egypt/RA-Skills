"""
Resize operation for image-works.
Supports fixed dimensions, scale ratio, max-edge, uniform batch resize.
"""
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


def resize_image(image, width: Optional[int] = None,
                 height: Optional[int] = None,
                 scale: Optional[float] = None,
                 max_edge: Optional[int] = None,
                 fit: str = "inside",
                 position: str = "center") -> Dict:
    """
    Resize an image according to specified parameters.
    
    Args:
        image: PIL Image object.
        width: Target width in pixels.
        height: Target height in pixels.
        scale: Scale factor (e.g., 0.5 = half size).
        max_edge: Max dimension constraint (maintains aspect ratio).
        fit: How to fit ('cover', 'contain', 'fill', 'inside', 'outside').
        position: Crop position for 'cover' fit ('center', 'top', etc.).
        
    Returns:
        Dict with 'image' (resized PIL Image) and 'dimensions' tuple.
    """
    from PIL import Image
    
    original_size = image.size
    img_width, img_height = original_size
    
    # Handle scale factor
    if scale is not None:
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        resized = image.resize((new_width, new_height), Image.LANCZOS)
        return {"image": resized, "dimensions": (new_width, new_height)}
    
    # Handle max edge constraint
    if max_edge is not None:
        ratio = min(max_edge / img_width, max_edge / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        resized = image.resize((new_width, new_height), Image.LANCZOS)
        return {"image": resized, "dimensions": (new_width, new_height)}
    
    # Handle width/height with fit modes
    if width is not None and height is not None:
        if fit == "fill":
            resized = image.resize((width, height), Image.LANCZOS)
            return {"image": resized, "dimensions": (width, height)}
        
        elif fit in ("cover", "contain"):
            # Calculate resize ratio to fill/contain target
            target_ratio = width / height
            img_ratio = img_width / img_height
            
            if fit == "cover":
                if img_ratio > target_ratio:
                    new_height = height
                    new_width = int(height * img_ratio)
                else:
                    new_width = width
                    new_height = int(width / img_ratio)
            else:  # contain
                if img_ratio > target_ratio:
                    new_width = width
                    new_height = int(width / img_ratio)
                else:
                    new_height = height
                    new_width = int(height * img_ratio)
            
            # Resize first
            temp = image.resize((new_width, new_height), Image.LANCZOS)
            
            if fit == "cover":
                # Center crop to target
                left = (new_width - width) // 2
                top = (new_height - height) // 2
                resized = temp.crop((left, top, left + width, top + height))
            else:
                # Create canvas for contain mode
                resized = Image.new("RGB", (width, height), (255, 255, 255))
                paste_x = (width - new_width) // 2
                paste_y = (height - new_height) // 2
                resized.paste(temp, (paste_x, paste_y))
            
            return {"image": resized, "dimensions": (width, height)}
        
        elif fit == "inside":
            # Shrink to fit inside, maintaining aspect ratio
            ratio = min(width / img_width, height / img_height, 1.0)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            resized = image.resize((new_width, new_height), Image.LANCZOS)
            return {"image": resized, "dimensions": (new_width, new_height)}
        
        elif fit == "outside":
            # Expand to cover, maintaining aspect ratio
            ratio = max(width / img_width, height / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            resized = image.resize((new_width, new_height), Image.LANCZOS)
            return {"image": resized, "dimensions": (new_width, new_height)}
    
    # Handle width-only (maintain aspect ratio)
    if width is not None and height is None:
        ratio = width / img_width
        new_height = int(img_height * ratio)
        resized = image.resize((width, new_height), Image.LANCZOS)
        return {"image": resized, "dimensions": (width, new_height)}
    
    # Handle height-only (maintain aspect ratio)
    if height is not None and width is None:
        ratio = height / img_height
        new_width = int(img_width * ratio)
        resized = image.resize((new_width, height), Image.LANCZOS)
        return {"image": resized, "dimensions": (new_width, height)}
    
    # No valid parameters
    return {"image": image, "dimensions": original_size, "warning": "No resize parameters provided"}


def calc_dimensions(img_width: int, img_height: int, dpi: Tuple[int, int] = (72, 72)) -> Dict:
    """Calculate various dimension representations."""
    return {
        "pixels": f"{img_width}×{img_height}",
        "aspect_ratio": f"{img_width // _gcd(img_width, img_height)}:{img_height // _gcd(img_width, img_height)}",
        "megapixels": round((img_width * img_height) / 1_000_000, 2),
    }


def _gcd(a: int, b: int) -> int:
    """Greatest common divisor."""
    while b:
        a, b = b, a % b
    return a
