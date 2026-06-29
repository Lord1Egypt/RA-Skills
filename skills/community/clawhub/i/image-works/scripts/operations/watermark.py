"""
Watermark operation for image-works.
Supports text watermark, image watermark, and tile watermark.
"""
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


def add_text_watermark(image, text: str, position: str = "bottom-right",
                       opacity: float = 0.5, font_size: int = 48,
                       color: str = "#ffffff") -> Dict:
    """
    Add a text watermark to an image.
    
    Args:
        image: PIL Image object.
        text: Watermark text.
        position: Position ('center', 'top-left', 'top-right', 'bottom-left', 
                  'bottom-right', 'tile').
        opacity: Text opacity 0.0-1.0.
        font_size: Font size in pixels.
        color: Text color hex string.
        
    Returns:
        Dict with 'image' (watermarked PIL Image).
    """
    from PIL import Image, ImageDraw, ImageFont
    import math
    
    # Ensure image is in RGBA for compositing
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    # Create a transparent overlay
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Try to load a font
    font = None
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for fp in font_paths:
        try:
            font = ImageFont.truetype(fp, font_size)
            break
        except (IOError, OSError):
            continue
    
    if font is None:
        font = ImageFont.load_default()
    
    # Calculate text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    img_width, img_height = image.size
    
    # Parse color
    if color.startswith("#"):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)
    else:
        r, g, b = 255, 255, 255
    
    # Calculate position
    margin = 20
    positions = {
        "center": ((img_width - text_width) // 2, (img_height - text_height) // 2),
        "top-left": (margin, margin),
        "top-right": (img_width - text_width - margin, margin),
        "bottom-left": (margin, img_height - text_height - margin),
        "bottom-right": (img_width - text_width - margin, img_height - text_height - margin),
    }
    
    if position == "tile":
        # Tile watermark across the image
        spacing_x = text_width + 100
        spacing_y = text_height + 100
        for y in range(0, img_height, spacing_y):
            for x in range(0, img_width, spacing_x):
                # Rotate text for tile watermark
                rotated_overlay = Image.new("RGBA", (text_width + 20, text_height + 20), (0, 0, 0, 0))
                r_draw = ImageDraw.Draw(rotated_overlay)
                r_draw.text((10, 10), text, font=font, fill=(r, g, b, int(255 * opacity)))
                rotated_overlay = rotated_overlay.rotate(30, expand=True, fillcolor=(0, 0, 0, 0))
                
                overlay.paste(rotated_overlay, (x - rotated_overlay.width // 4, 
                                                y - rotated_overlay.height // 4),
                             rotated_overlay)
    else:
        pos = positions.get(position, positions["bottom-right"])
        draw.text(pos, text, font=font, fill=(r, g, b, int(255 * opacity)))
    
    # Composite
    watermarked = Image.alpha_composite(image, overlay)
    
    return {"image": watermarked}


def add_image_watermark(image, watermark_path: str, position: str = "bottom-right",
                        opacity: float = 0.5, scale: float = 0.2) -> Dict:
    """
    Add an image watermark (logo) to an image.
    
    Args:
        image: PIL Image object.
        watermark_path: Path to watermark image.
        position: Position ('center', 'top-left', etc.).
        opacity: Watermark opacity 0.0-1.0.
        scale: Watermark size relative to main image (0.0-1.0).
        
    Returns:
        Dict with 'image' (watermarked PIL Image).
    """
    from PIL import Image
    
    try:
        watermark = Image.open(watermark_path)
    except (IOError, FileNotFoundError) as e:
        return {"image": image, "warning": f"Could not open watermark: {e}"}
    
    # Ensure watermark has alpha
    if watermark.mode != "RGBA":
        watermark = watermark.convert("RGBA")
    
    # Resize watermark
    img_width, img_height = image.size
    wm_width = int(img_width * scale)
    wm_height = int(watermark.height * (wm_width / watermark.width))
    watermark = watermark.resize((wm_width, wm_height), Image.LANCZOS)
    
    # Apply opacity
    if opacity < 1.0:
        r, g, b, a = watermark.split()
        a = a.point(lambda x: int(x * opacity))
        watermark = Image.merge("RGBA", (r, g, b, a))
    
    # Calculate position
    margin = 20
    positions = {
        "center": ((img_width - wm_width) // 2, (img_height - wm_height) // 2),
        "top-left": (margin, margin),
        "top-right": (img_width - wm_width - margin, margin),
        "bottom-left": (margin, img_height - wm_height - margin),
        "bottom-right": (img_width - wm_width - margin, img_height - wm_height - margin),
    }
    
    pos = positions.get(position, positions["bottom-right"])
    
    # Composite
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    
    image.paste(watermark, pos, watermark)
    
    return {"image": image}
