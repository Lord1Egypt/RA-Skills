# Pillow Common Operations Reference

Quick reference guide for common Pillow (PIL) image processing operations.

## 1. Opening and Saving Images

### Open Image
```python
from PIL import Image

# Open image file
img = Image.open('photo.jpg')

# Open from bytes
from io import BytesIO
img = Image.open(BytesIO(image_bytes))
```

### Save Image
```python
# Save with default settings
img.save('output.png')

# Save JPEG with quality
img.save('output.jpg', quality=95, optimize=True)

# Save PNG with compression
img.save('output.png', compress_level=9)

# Save with specific format
img.save('output', format='JPEG')
```

## 2. Image Properties

### Get Basic Info
```python
width, height = img.size
format = img.format  # 'JPEG', 'PNG', etc.
mode = img.mode      # 'RGB', 'RGBA', 'L', etc.
info = img.info      # Metadata dictionary
```

### Image Modes
- `'1'`: 1-bit pixels, black and white
- `'L'`: 8-bit pixels, grayscale
- `'RGB'`: 3x8-bit pixels, true color
- `'RGBA'`: 4x8-bit pixels, true color with transparency
- `'CMYK'`: 4x8-bit pixels, color separation

## 3. Resizing and Cropping

### Resize
```python
# Resize to exact dimensions
new_img = img.resize((800, 600), Image.Resampling.LANCZOS)

# Maintain aspect ratio
img.thumbnail((800, 600), Image.Resampling.LANCZOS)
```

### Crop
```python
# Crop rectangle (left, upper, right, lower)
box = (100, 100, 400, 400)
cropped = img.crop(box)
```

### Resampling Filters
- `NEAREST`: Fastest, lowest quality
- `BOX`: Box filter
- `BILINEAR`: Linear interpolation
- `HAMMING`: Hamming filter
- `BICUBIC`: Cubic interpolation
- `LANCZOS`: High-quality downsampling (recommended)

## 4. Rotation and Flip

### Rotate
```python
# Rotate with expansion
rotated = img.rotate(45, expand=True)

# Rotate with specific fill color
rotated = img.rotate(30, fillcolor='white')

# Rotate by 90° increments (faster)
rotated = img.rotate(90, expand=True)
```

### Flip and Mirror
```python
from PIL import Image

# Flip horizontally (mirror)
flipped_h = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

# Flip vertically
flipped_v = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

# Rotate 90° counter-clockwise
rotated = img.transpose(Image.Transpose.ROTATE_90)

# Rotate 180°
rotated = img.transpose(Image.Transpose.ROTATE_180)
```

## 5. Color Adjustments

### Enhance Colors
```python
from PIL import ImageEnhance

# Brightness (0.0 = black, 1.0 = original, 2.0 = twice as bright)
enhancer = ImageEnhance.Brightness(img)
brighter = enhancer.enhance(1.5)

# Contrast (0.0 = gray, 1.0 = original, 2.0 = high contrast)
enhancer = ImageEnhance.Contrast(img)
contrasted = enhancer.enhance(1.3)

# Color saturation (0.0 = grayscale, 1.0 = original, 2.0 = vivid)
enhancer = ImageEnhance.Color(img)
saturated = enhancer.enhance(1.2)

# Sharpness (0.0 = blurred, 1.0 = original, 2.0 = sharpened)
enhancer = ImageEnhance.Sharpness(img)
sharpened = enhancer.enhance(2.0)
```

### Convert Color Modes
```python
# RGB to grayscale
gray = img.convert('L')

# RGB to RGBA (add alpha channel)
rgba = img.convert('RGBA')

# RGBA to RGB (remove alpha)
rgb = img.convert('RGB')

# RGB to palette mode
palette = img.convert('P')
```

## 6. Filters

### Apply Filters
```python
from PIL import ImageFilter

# Blur
blurred = img.filter(ImageFilter.BLUR)
blurred = img.filter(ImageFilter.GaussianBlur(radius=5))

# Sharpen
sharpened = img.filter(ImageFilter.SHARPEN)
sharpened = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))

# Edge detection
edges = img.filter(ImageFilter.FIND_EDGES)
edges = img.filter(ImageFilter.CONTOUR)

# Smooth
smooth = img.filter(ImageFilter.SMOOTH)
smooth = img.filter(ImageFilter.SMOOTH_MORE)

# Detail enhancement
detailed = img.filter(ImageFilter.DETAIL)

# Emboss
embossed = img.filter(ImageFilter.EMBOSS)
```

### Custom Filters
```python
# Custom kernel filter
from PIL import ImageFilter

kernel = ImageFilter.Kernel((3, 3), 
    [-1, -1, -1,
     -1,  9, -1,
     -1, -1, -1])
filtered = img.filter(kernel)
```

## 7. Drawing on Images

### Draw Shapes and Text
```python
from PIL import ImageDraw, ImageFont

# Create drawing context
draw = ImageDraw.Draw(img)

# Draw rectangle
draw.rectangle([10, 10, 100, 100], outline='red', width=3)
draw.rectangle([150, 150, 250, 250], fill='blue')

# Draw circle/ellipse
draw.ellipse([50, 50, 150, 150], outline='green', width=2)

# Draw line
draw.line([0, 0, 200, 200], fill='yellow', width=5)

# Draw text
font = ImageFont.truetype('arial.ttf', 24)
draw.text((50, 50), 'Hello World', fill='white', font=font)

# Multi-line text
draw.multiline_text((50, 100), 'Line 1\nLine 2', fill='black', font=font)
```

## 8. Image Composition

### Paste Images
```python
# Paste image at position
background.paste(foreground, (100, 100))

# Paste with transparency mask
background.paste(foreground, (100, 100), foreground)

# Alpha composite (requires RGBA)
composite = Image.alpha_composite(background, foreground)
```

### Blend Images
```python
# Blend two images (0.0 = first image, 1.0 = second image)
blended = Image.blend(img1, img2, alpha=0.5)
```

### Create New Images
```python
# New blank image
new_img = Image.new('RGB', (800, 600), color='white')
new_img = Image.new('RGBA', (800, 600), color=(255, 0, 0, 128))

# From array
import numpy as np
array = np.random.randint(0, 255, (600, 800, 3), dtype=np.uint8)
img = Image.fromarray(array)
```

## 9. Image Transformations

### Perspective Transform
```python
# Define transformation coefficients
coeffs = [a, b, c, d, e, f, g, h]
transformed = img.transform(
    img.size, 
    Image.Transform.PERSPECTIVE, 
    coeffs, 
    Image.Resampling.BICUBIC
)
```

### Affine Transform
```python
# Affine transformation (6 coefficients)
coeffs = [a, b, c, d, e, f]
transformed = img.transform(
    img.size, 
    Image.Transform.AFFINE, 
    coeffs
)
```

## 10. Working with Channels

### Split and Merge Channels
```python
# Split into channels
r, g, b = img.split()
r, g, b, a = rgba_img.split()

# Merge channels
new_img = Image.merge('RGB', (r, g, b))
new_img = Image.merge('RGBA', (r, g, b, a))

# Swap channels
img = Image.merge('RGB', (b, g, r))  # BGR
```

### Alpha Channel Operations
```python
# Extract alpha
alpha = img.split()[3]

# Add alpha channel
img.putalpha(alpha)

# Modify alpha values
alpha = alpha.point(lambda p: p * 0.5)  # 50% transparency
img.putalpha(alpha)
```

## 11. Thumbnails and Previews

### Create Thumbnails
```python
# Create thumbnail (maintains aspect ratio, modifies in-place)
img.thumbnail((200, 200), Image.Resampling.LANCZOS)

# Create thumbnail as new image
from PIL import Image
thumb = img.copy()
thumb.thumbnail((200, 200), Image.Resampling.LANCZOS)
```

### Reduce File Size
```python
# Optimize JPEG
img.save('optimized.jpg', optimize=True, quality=85)

# Convert to progressive JPEG
img.save('progressive.jpg', progressive=True, quality=85)

# Reduce PNG size
img.save('optimized.png', optimize=True, compress_level=9)
```

## 12. EXIF Data

### Read EXIF
```python
from PIL.ExifTags import TAGS

exif = img.getexif()
for tag_id, value in exif.items():
    tag_name = TAGS.get(tag_id, tag_id)
    print(f"{tag_name}: {value}")
```

### Preserve EXIF
```python
# Save with EXIF data preserved
exif = img.getexif()
img.save('output.jpg', exif=exif)
```

## 13. Common Patterns

### Maintain Aspect Ratio Resize
```python
def resize_with_aspect(img, target_width=None, target_height=None):
    width, height = img.size
    if target_width and not target_height:
        target_height = int(height * target_width / width)
    elif target_height and not target_width:
        target_width = int(width * target_height / height)
    return img.resize((target_width, target_height), Image.Resampling.LANCZOS)
```

### Add Border
```python
from PIL import ImageOps

# Add border
bordered = ImageOps.expand(img, border=10, fill='white')
```

### Convert RGBA to RGB
```python
def rgba_to_rgb(img, background_color=(255, 255, 255)):
    if img.mode != 'RGBA':
        return img.convert('RGB')
    
    rgb = Image.new('RGB', img.size, background_color)
    rgb.paste(img, mask=img.split()[3])  # Use alpha as mask
    return rgb
```

## 14. Performance Tips

- Use `thumbnail()` instead of `resize()` when you don't need exact dimensions
- Use `LANCZOS` resampling for best quality downscaling
- Use `NEAREST` for fastest operations (when quality doesn't matter)
- Process images in batches with multiprocessing for large datasets
- Use `.copy()` before modifying if you need to preserve the original
- Close images when done: `img.close()`

## 15. Error Handling

```python
from PIL import Image

try:
    img = Image.open('image.jpg')
    # Process image...
except FileNotFoundError:
    print("Image file not found")
except Image.UnidentifiedImageError:
    print("Cannot identify image file")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'img' in locals():
        img.close()
```
