"""
Crop operation for image-works.
Supports region crop and aspect-ratio crop.
"""
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


def crop_region(image, x: int, y: int, width: int, height: int) -> Dict:
    """
    Crop a specific rectangular region from an image.
    
    Args:
        image: PIL Image object.
        x: Left coordinate.
        y: Top coordinate.
        width: Crop width.
        height: Crop height.
        
    Returns:
        Dict with 'image' (cropped PIL Image).
    """
    img_width, img_height = image.size
    
    # Clamp to image boundaries
    x = max(0, min(x, img_width - 1))
    y = max(0, min(y, img_height - 1))
    width = min(width, img_width - x)
    height = min(height, img_height - y)
    
    cropped = image.crop((x, y, x + width, y + height))
    
    return {"image": cropped, "dimensions": (width, height), "region": (x, y, x + width, y + height)}


def crop_aspect_ratio(image, aspect_ratio: str, position: str = "center") -> Dict:
    """
    Crop an image to a specific aspect ratio.
    
    Supported ratios: '1:1', '4:3', '3:4', '16:9', '9:16', '3:2', '2:3'
    
    Args:
        image: PIL Image object.
        aspect_ratio: Target aspect ratio string (e.g., '1:1', '16:9').
        position: Crop position ('center', 'top', 'bottom', 'left', 'right').
        
    Returns:
        Dict with 'image' (cropped PIL Image).
    """
    from PIL import Image
    
    img_width, img_height = image.size
    img_ratio = img_width / img_height
    
    # Parse target ratio
    try:
        parts = aspect_ratio.split(":")
        target_ratio = float(parts[0]) / float(parts[1])
    except (ValueError, IndexError, ZeroDivisionError):
        return {"image": image, "warning": f"Invalid aspect ratio: {aspect_ratio}"}
    
    if abs(img_ratio - target_ratio) < 0.01:
        # Already at target ratio
        return {"image": image, "dimensions": image.size, "ratio": aspect_ratio}
    
    if img_ratio > target_ratio:
        # Image is wider than target - crop width
        new_width = int(img_height * target_ratio)
        new_height = img_height
    else:
        # Image is taller than target - crop height
        new_width = img_width
        new_height = int(img_width / target_ratio)
    
    # Calculate position-based offset
    position_map = {
        "center": ((img_width - new_width) // 2, (img_height - new_height) // 2),
        "top": (0, 0),
        "bottom": (img_width - new_width, img_height - new_height),
        "left": (0, (img_height - new_height) // 2),
        "right": (img_width - new_width, (img_height - new_height) // 2),
        "top-left": (0, 0),
        "top-right": (img_width - new_width, 0),
        "bottom-left": (0, img_height - new_height),
        "bottom-right": (img_width - new_width, img_height - new_height),
    }
    
    x_start, y_start = position_map.get(position, position_map["center"])
    x_start = max(0, x_start)
    y_start = max(0, y_start)
    
    cropped = image.crop((x_start, y_start, x_start + new_width, y_start + new_height))
    
    return {"image": cropped, "dimensions": (new_width, new_height), "ratio": aspect_ratio,
            "method": "aspect_crop"}


# Preset crop dimensions for common platforms (in pixels)
PRESET_CROPS = {
    "wechat-moments": {"width": None, "height": None, "description": "9-grid cut"},
    "wechat-cover": {"width": 900, "height": 383, "fit": "cover"},
    "xiaohongshu": {"aspect_ratio": "3:4"},
    "taobao-main": {"width": 800, "height": 800, "fit": "cover"},
    "douyin-cover": {"width": 1920, "height": 1080, "fit": "cover"},
    "weibo": {"aspect_ratio": "16:9"},
    "bilibili-cover": {"aspect_ratio": "16:9"},
    "avatar": {"width": 400, "height": 400, "fit": "cover"},
}
