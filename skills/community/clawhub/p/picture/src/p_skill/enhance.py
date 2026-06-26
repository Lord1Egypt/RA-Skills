from PIL import Image, ImageEnhance


def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)


def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def adjust_sharpness(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)


def smart_enhance(
    image: Image.Image,
    brightness_factor: float = 1.1,
    contrast_factor: float = 1.1,
    sharpness_factor: float = 1.2
) -> Image.Image:
    result = image
    result = adjust_brightness(result, brightness_factor)
    result = adjust_contrast(result, contrast_factor)
    result = adjust_sharpness(result, sharpness_factor)
    return result
