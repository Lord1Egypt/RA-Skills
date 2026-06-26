# Image Processing Best Practices

Best practices and patterns for efficient image processing with Pillow.

## 1. Image Quality Considerations

### Choosing the Right Format

**JPEG**
- ✅ Best for: Photographs, complex images with many colors
- ✅ Pros: Small file size, good quality
- ❌ Cons: Lossy compression, no transparency
- 💡 Tip: Use quality 85-95 for good balance

**PNG**
- ✅ Best for: Graphics, logos, images with transparency
- ✅ Pros: Lossless compression, supports alpha channel
- ❌ Cons: Larger file sizes
- 💡 Tip: Use compress_level 6-9 for good compression

**WebP**
- ✅ Best for: Web images (modern browsers)
- ✅ Pros: Better compression than JPEG/PNG, supports transparency
- ❌ Cons: Not universally supported
- 💡 Tip: Use as primary with PNG/JPEG fallback

**GIF**
- ✅ Best for: Simple animations, very simple graphics
- ❌ Cons: Limited to 256 colors, poor for photos
- 💡 Tip: Consider WebP or APNG for modern alternatives

## 2. Resizing Best Practices

### When to Use Thumbnail vs Resize

```python
# Use thumbnail() when:
# - You want to maintain aspect ratio
# - Exact dimensions aren't critical
# - Processing many images (faster)
img.thumbnail((800, 600), Image.Resampling.LANCZOS)

# Use resize() when:
# - You need exact dimensions
# - You're deliberately changing aspect ratio
img = img.resize((800, 600), Image.Resampling.LANCZOS)
```

### Resampling Filter Selection

**Quality Priority:**
```python
# Best quality (slowest)
img.resize(size, Image.Resampling.LANCZOS)
```

**Speed Priority:**
```python
# Fastest (lowest quality)
img.resize(size, Image.Resampling.NEAREST)
```

**Balanced:**
```python
# Good balance
img.resize(size, Image.Resampling.BILINEAR)
```

### Progressive Resizing
For extreme downsizing (>50%), resize in steps:

```python
def progressive_resize(img, target_size):
    """Resize large images progressively for better quality"""
    while img.size[0] > target_size[0] * 2 or img.size[1] > target_size[1] * 2:
        img = img.resize(
            (img.size[0] // 2, img.size[1] // 2),
            Image.Resampling.LANCZOS
        )
    return img.resize(target_size, Image.Resampling.LANCZOS)
```

## 3. Color Mode Conversion

### Safe RGBA to RGB Conversion

```python
def safe_rgba_to_rgb(img, bg_color=(255, 255, 255)):
    """Convert RGBA to RGB safely"""
    if img.mode != 'RGBA':
        return img.convert('RGB')
    
    # Create white background
    background = Image.new('RGB', img.size, bg_color)
    # Paste using alpha channel as mask
    background.paste(img, mask=img.split()[3])
    return background
```

### When to Convert

- Convert to `'L'` (grayscale) for black & white processing
- Convert to `'RGB'` before saving as JPEG
- Keep `'RGBA'` for images needing transparency
- Convert to `'P'` (palette) for GIF animations

## 4. Memory Management

### Processing Large Images

```python
# Load image lazily
from PIL import Image

# Open without loading full image
img = Image.open('large_image.jpg')
print(f"Size: {img.size}, Mode: {img.mode}")  # Metadata only

# Load when needed
img.load()

# Close when done
img.close()
```

### Batch Processing Pattern

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

def process_image(image_path):
    try:
        with Image.open(image_path) as img:
            # Process...
            img.save(output_path)
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Process in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(process_image, image_paths)
```

## 5. Watermarking Strategies

### Text Watermark Best Practices

```python
def add_smart_watermark(img, text, position='bottom-right'):
    """Add watermark with automatic sizing"""
    # Calculate appropriate font size (3% of image width)
    font_size = int(img.width * 0.03)
    
    # Adjust opacity based on image brightness
    grayscale = img.convert('L')
    avg_brightness = sum(grayscale.getdata()) / len(grayscale.getdata())
    
    # Use white text on dark images, black on light images
    if avg_brightness < 128:
        color = (255, 255, 255, 200)  # White
    else:
        color = (0, 0, 0, 200)  # Black
    
    # Add watermark...
    return watermarked_img
```

### Image Watermark Placement

- **Bottom-right**: Most common, doesn't interfere with subject
- **Center**: High protection, but intrusive
- **Tiled**: Maximum protection, pattern across image
- **Corner**: Subtle, easy to crop

## 6. Filter Application

### Combining Filters

```python
from PIL import ImageFilter

# Apply multiple filters sequentially
img = img.filter(ImageFilter.SMOOTH)
img = img.filter(ImageFilter.SHARPEN)
img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150))
```

### Custom Filter Pipeline

```python
def enhance_photo(img):
    """Standard photo enhancement pipeline"""
    from PIL import ImageEnhance
    
    # 1. Slight sharpness boost
    sharpener = ImageEnhance.Sharpness(img)
    img = sharpener.enhance(1.2)
    
    # 2. Increase contrast slightly
    contrast = ImageEnhance.Contrast(img)
    img = contrast.enhance(1.1)
    
    # 3. Boost color saturation
    color = ImageEnhance.Color(img)
    img = color.enhance(1.2)
    
    return img
```

## 7. Thumbnail Generation

### Standard Thumbnail Workflow

```python
def create_thumbnail(input_path, output_path, size=(200, 200)):
    """Create optimized thumbnail"""
    with Image.open(input_path) as img:
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Create thumbnail
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save optimized
        img.save(
            output_path,
            'JPEG',
            quality=85,
            optimize=True,
            progressive=True
        )
```

### Multiple Thumbnail Sizes

```python
THUMBNAIL_SIZES = {
    'small': (150, 150),
    'medium': (300, 300),
    'large': (600, 600),
}

def generate_thumbnails(image_path, output_dir):
    """Generate multiple thumbnail sizes"""
    with Image.open(image_path) as img:
        for name, size in THUMBNAIL_SIZES.items():
            thumb = img.copy()
            thumb.thumbnail(size, Image.Resampling.LANCZOS)
            thumb.save(f"{output_dir}/{name}_{image_path.name}")
```

## 8. Image Validation

### Validate Before Processing

```python
def validate_image(image_path, max_size_mb=10, allowed_formats=None):
    """Validate image before processing"""
    if allowed_formats is None:
        allowed_formats = {'JPEG', 'PNG', 'GIF', 'WEBP'}
    
    # Check file size
    file_size_mb = image_path.stat().st_size / (1024 * 1024)
    if file_size_mb > max_size_mb:
        raise ValueError(f"Image too large: {file_size_mb:.2f} MB")
    
    # Check format
    try:
        with Image.open(image_path) as img:
            if img.format not in allowed_formats:
                raise ValueError(f"Invalid format: {img.format}")
            return True
    except Exception as e:
        raise ValueError(f"Invalid image: {e}")
```

## 9. Optimization Techniques

### JPEG Optimization

```python
def optimize_jpeg(img, quality=85):
    """Optimize JPEG for web"""
    # Ensure RGB mode
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Save with optimization
    img.save(
        output_path,
        'JPEG',
        quality=quality,
        optimize=True,
        progressive=True,  # Progressive loading
        subsampling='4:2:0'  # Chroma subsampling
    )
```

### PNG Optimization

```python
def optimize_png(img):
    """Optimize PNG file size"""
    # Remove alpha if not needed
    if img.mode == 'RGBA':
        # Check if alpha is actually used
        alpha = img.split()[3]
        if alpha.getextrema() == (255, 255):
            img = img.convert('RGB')
    
    # Save with compression
    img.save(
        output_path,
        'PNG',
        optimize=True,
        compress_level=9
    )
```

## 10. Error Handling Patterns

### Robust Image Loading

```python
def safe_image_open(path, fallback_image=None):
    """Safely open image with fallback"""
    try:
        img = Image.open(path)
        img.verify()  # Verify it's actually an image
        img = Image.open(path)  # Reopen after verify
        return img
    except Exception as e:
        print(f"Failed to open {path}: {e}")
        if fallback_image:
            return Image.open(fallback_image)
        return None
```

### Graceful Degradation

```python
def process_with_fallback(img, operations):
    """Try operations with fallback"""
    for operation in operations:
        try:
            img = operation(img)
        except Exception as e:
            print(f"Operation failed: {e}, skipping...")
            continue
    return img
```

## 11. Performance Tips

### Do's ✅
- Use `thumbnail()` for maintaining aspect ratio
- Process images in batches with multiprocessing
- Close images after processing: `img.close()`
- Use `with` statement: `with Image.open() as img:`
- Cache frequently used operations
- Use appropriate resampling filters

### Don'ts ❌
- Don't load full image if you only need metadata
- Don't keep images open longer than necessary
- Don't resize up (upscaling reduces quality)
- Don't apply too many filters (quality degrades)
- Don't forget to handle RGBA→RGB conversion for JPEG

## 12. Common Workflows

### Photo Processing Pipeline

```python
def process_photo(input_path, output_path):
    """Standard photo processing workflow"""
    with Image.open(input_path) as img:
        # 1. Auto-orient based on EXIF
        img = ImageOps.exif_transpose(img)
        
        # 2. Resize if too large
        if img.width > 2000 or img.height > 2000:
            img.thumbnail((2000, 2000), Image.Resampling.LANCZOS)
        
        # 3. Enhance
        img = enhance_photo(img)
        
        # 4. Convert for web
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # 5. Save optimized
        img.save(output_path, 'JPEG', quality=90, optimize=True)
```

### Logo/Graphic Processing

```python
def process_logo(input_path, output_path):
    """Process logo/graphic with transparency"""
    with Image.open(input_path) as img:
        # Ensure RGBA
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Resize maintaining transparency
        img.thumbnail((500, 500), Image.Resampling.LANCZOS)
        
        # Save as PNG
        img.save(output_path, 'PNG', optimize=True)
```

## 13. Testing and Validation

```python
def test_image_processing():
    """Test image processing pipeline"""
    test_cases = [
        ('photo.jpg', 'JPEG'),
        ('logo.png', 'RGBA'),
        ('animation.gif', 'P'),
    ]
    
    for path, expected_mode in test_cases:
        img = Image.open(path)
        assert img.mode == expected_mode
        # Process and validate...
```

## 14. Documentation

Always document:
- Input requirements (format, size, mode)
- Output specifications
- Destructive vs non-destructive operations
- Memory considerations
- Performance characteristics

```python
def resize_image(img, target_size, maintain_aspect=True):
    """
    Resize image to target dimensions.
    
    Args:
        img: PIL Image object
        target_size: tuple (width, height)
        maintain_aspect: bool, maintain aspect ratio
        
    Returns:
        PIL Image object (new image, original unchanged)
        
    Memory: Creates new image, original preserved
    Performance: O(n*m) where n*m is target size
    """
    # Implementation...
```
