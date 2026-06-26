from PIL import Image, ImageDraw, ImageFont
import platform
import os


def _get_system_font(size: int) -> ImageFont.FreeTypeFont:
    system = platform.system()
    font_paths = []
    
    if system == "Windows":
        font_paths = [
            "C:\\Windows\\Fonts\\msyh.ttc",
            "C:\\Windows\\Fonts\\simhei.ttf",
            "C:\\Windows\\Fonts\\simsun.ttc"
        ]
    elif system == "Darwin":
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/Arial.ttf"
        ]
    elif system == "Linux":
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
    
    try:
        return ImageFont.load_default()
    except:
        return ImageFont.truetype("arial.ttf", size)


def _calculate_position(
    image: Image.Image,
    text: str,
    font: ImageFont.FreeTypeFont,
    position: str | tuple[int, int],
    offset: tuple[int, int] = (0, 0)
) -> tuple[int, int]:
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    img_width, img_height = image.size
    
    if isinstance(position, str):
        position = position.lower()
        if position == "top-left":
            x, y = 0, 0
        elif position == "top-center":
            x, y = (img_width - text_width) // 2, 0
        elif position == "top-right":
            x, y = img_width - text_width, 0
        elif position == "center-left":
            x, y = 0, (img_height - text_height) // 2
        elif position == "center":
            x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
        elif position == "center-right":
            x, y = img_width - text_width, (img_height - text_height) // 2
        elif position == "bottom-left":
            x, y = 0, img_height - text_height
        elif position == "bottom-center":
            x, y = (img_width - text_width) // 2, img_height - text_height
        elif position == "bottom-right":
            x, y = img_width - text_width, img_height - text_height
        else:
            raise ValueError(f"Unknown position: {position}")
    else:
        x, y = position
    
    return (x + offset[0], y + offset[1])


def add_text(
    image: Image.Image,
    text: str,
    position: str | tuple[int, int] = "center",
    font_path: str | None = None,
    font_size: int = 40,
    color: tuple[int, int, int] | tuple[int, int, int, int] = (0, 0, 0),
    rotation: float = 0.0,
    offset: tuple[int, int] = (0, 0)
) -> Image.Image:
    result = image.copy()
    
    if font_path and os.path.exists(font_path):
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = _get_system_font(font_size)
    
    text_image = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    text_image = Image.new("RGBA", (text_width + 20, text_height + 20), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_image)
    draw.text((10, 10), text, font=font, fill=color)
    
    if rotation != 0:
        text_image = text_image.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
    
    x, y = _calculate_position(result, text, font, position, offset)
    
    result.paste(text_image, (x, y), text_image)
    
    return result
