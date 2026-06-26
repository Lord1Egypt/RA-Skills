from PIL import Image, ImageFilter, ImageOps


def grayscale(image: Image.Image) -> Image.Image:
    return ImageOps.grayscale(image)


def sepia(image: Image.Image) -> Image.Image:
    sepia_img = image.convert('RGB')
    width, height = sepia_img.size
    pixels = sepia_img.load()
    
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            tr = min(255, tr)
            tg = min(255, tg)
            tb = min(255, tb)
            pixels[x, y] = (tr, tg, tb)
    
    return sepia_img


def blur(image: Image.Image, radius: int = 5) -> Image.Image:
    return image.filter(ImageFilter.GaussianBlur(radius=radius))


def contour(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.CONTOUR)


def invert(image: Image.Image) -> Image.Image:
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        rgb = Image.merge('RGB', (r, g, b))
        rgb_inverted = ImageOps.invert(rgb)
        r2, g2, b2 = rgb_inverted.split()
        return Image.merge('RGBA', (r2, g2, b2, a))
    else:
        return ImageOps.invert(image)


def pixelate(image: Image.Image, pixel_size: int = 10) -> Image.Image:
    if pixel_size < 1:
        pixel_size = 1
    width, height = image.size
    small = image.resize((width // pixel_size, height // pixel_size), Image.Resampling.NEAREST)
    return small.resize((width, height), Image.Resampling.NEAREST)
