from PIL import Image
import os


def load_image(file_path: str) -> Image.Image:
    image = Image.open(file_path)
    if image.mode in ('RGBA', 'LA', 'P'):
        image = image.convert('RGBA')
    return image


def save_image(image: Image.Image, output_path: str, quality: int = 95) -> None:
    ext = os.path.splitext(output_path)[1].lower()
    if ext in ('.jpg', '.jpeg'):
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background
        image.save(output_path, 'JPEG', quality=quality, optimize=True)
    elif ext == '.png':
        image.save(output_path, 'PNG', optimize=True)
    elif ext == '.webp':
        image.save(output_path, 'WEBP', quality=quality, method=6)
    else:
        image.save(output_path)


def resize_image(image: Image.Image, size: tuple[int, int] = None, scale: float = None) -> Image.Image:
    if scale is not None:
        if scale <= 0:
            raise ValueError("Scale must be a positive number")
        new_width = int(image.width * scale)
        new_height = int(image.height * scale)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    elif size is not None:
        return image.resize(size, Image.Resampling.LANCZOS)
    else:
        raise ValueError("Either size or scale must be provided")


def crop_image(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    return image.crop(box)


def convert_format(image: Image.Image, format: str) -> Image.Image:
    format = format.upper()
    if format in ('JPEG', 'JPG'):
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            return background
        elif image.mode != 'RGB':
            return image.convert('RGB')
    elif format == 'PNG':
        if image.mode != 'RGBA' and image.mode != 'RGB':
            return image.convert('RGBA')
    return image
