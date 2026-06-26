__version__ = "1.0.0"

from .core import (
    load_image,
    save_image,
    resize_image,
    crop_image,
    convert_format
)
from .enhance import (
    adjust_brightness,
    adjust_contrast,
    adjust_sharpness,
    smart_enhance
)
from .filters import (
    grayscale,
    sepia,
    blur,
    contour,
    invert,
    pixelate
)
from .composite import (
    stitch_horizontal,
    stitch_vertical,
    stitch_grid
)
from .background import (
    remove_background_simple,
    remove_background_color
)
from .text import (
    add_text
)

