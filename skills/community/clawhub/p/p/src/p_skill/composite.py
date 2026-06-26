from PIL import Image
from typing import List, Tuple


def stitch_horizontal(images: List[Image.Image], align: str = 'center') -> Image.Image:
    if not images:
        raise ValueError("No images provided")

    max_height = max(img.height for img in images)

    total_width = sum(img.width for img in images)

    mode = images[0].mode
    result = Image.new(mode, (total_width, max_height))

    current_x = 0
    for img in images:
        if img.mode != mode:
            img = img.convert(mode)

        if align == 'top':
            y_offset = 0
        elif align == 'bottom':
            y_offset = max_height - img.height
        else:
            y_offset = (max_height - img.height) // 2

        result.paste(img, (current_x, y_offset))
        current_x += img.width

    return result


def stitch_vertical(images: List[Image.Image], align: str = 'center') -> Image.Image:
    if not images:
        raise ValueError("No images provided")

    max_width = max(img.width for img in images)

    total_height = sum(img.height for img in images)

    mode = images[0].mode
    result = Image.new(mode, (max_width, total_height))

    current_y = 0
    for img in images:
        if img.mode != mode:
            img = img.convert(mode)

        if align == 'left':
            x_offset = 0
        elif align == 'right':
            x_offset = max_width - img.width
        else:
            x_offset = (max_width - img.width) // 2

        result.paste(img, (x_offset, current_y))
        current_y += img.height

    return result


def stitch_grid(images: List[Image.Image], cols: int, rows: int = None, align: str = 'center') -> Image.Image:
    if not images:
        raise ValueError("No images provided")

    if cols <= 0:
        raise ValueError("Number of columns must be positive")

    if rows is None:
        rows = (len(images) + cols - 1) // cols

    if cols * rows < len(images):
        raise ValueError("Grid size is too small for the number of images")

    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)

    mode = images[0].mode
    total_width = cols * max_width
    total_height = rows * max_height
    result = Image.new(mode, (total_width, total_height))

    for idx, img in enumerate(images):
        row = idx // cols
        col = idx % cols

        if img.mode != mode:
            img = img.convert(mode)

        x_offset = col * max_width
        y_offset = row * max_height

        if align == 'top':
            img_y = y_offset
        elif align == 'bottom':
            img_y = y_offset + max_height - img.height
        else:
            img_y = y_offset + (max_height - img.height) // 2

        if align == 'left':
            img_x = x_offset
        elif align == 'right':
            img_x = x_offset + max_width - img.width
        else:
            img_x = x_offset + (max_width - img.width) // 2

        result.paste(img, (img_x, img_y))

    return result
