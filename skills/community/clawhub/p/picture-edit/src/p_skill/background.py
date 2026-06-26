from PIL import Image, ImageFilter


def _smooth_edges(mask: Image.Image, blur_radius: int = 2) -> Image.Image:
    mask = mask.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return mask


def remove_background_simple(
    image: Image.Image,
    threshold: int = 240,
    smooth_radius: int = 2
) -> Image.Image:
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    mask = Image.new('L', (width, height), 255)
    
    pixels = image.load()
    mask_pixels = mask.load()
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if r >= threshold and g >= threshold and b >= threshold:
                mask_pixels[x, y] = 0
    
    if smooth_radius > 0:
        mask = _smooth_edges(mask, smooth_radius)
    
    result = image.copy()
    result.putalpha(mask)
    
    return result


def remove_background_color(
    image: Image.Image,
    target_color: tuple[int, int, int],
    tolerance: int = 30,
    smooth_radius: int = 2
) -> Image.Image:
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    width, height = image.size
    mask = Image.new('L', (width, height), 255)
    
    pixels = image.load()
    mask_pixels = mask.load()
    
    target_r, target_g, target_b = target_color
    
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            color_dist = ((r - target_r) ** 2 + (g - target_g) ** 2 + (b - target_b) ** 2) ** 0.5
            if color_dist <= tolerance:
                mask_pixels[x, y] = 0
    
    if smooth_radius > 0:
        mask = _smooth_edges(mask, smooth_radius)
    
    result = image.copy()
    result.putalpha(mask)
    
    return result
