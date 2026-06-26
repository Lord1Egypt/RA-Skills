#!/usr/bin/env python3
"""
Image Editor - Basic image manipulation using Pillow
Supports: resize, crop, rotate, flip, adjust brightness/contrast/color
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter


def resize_image(img, width=None, height=None, keep_aspect=True):
    """Resize image to specified dimensions"""
    if not width and not height:
        return img
    
    original_width, original_height = img.size
    
    if keep_aspect:
        if width and not height:
            height = int(original_height * width / original_width)
        elif height and not width:
            width = int(original_width * height / original_height)
        elif width and height:
            # Keep aspect ratio, fit within bounds
            ratio = min(width / original_width, height / original_height)
            width = int(original_width * ratio)
            height = int(original_height * ratio)
    else:
        width = width or original_width
        height = height or original_height
    
    return img.resize((width, height), Image.Resampling.LANCZOS)


def crop_image(img, x, y, width, height):
    """Crop image to specified rectangle"""
    return img.crop((x, y, x + width, y + height))


def rotate_image(img, angle, expand=True):
    """Rotate image by specified angle"""
    return img.rotate(angle, expand=expand, fillcolor='white')


def flip_image(img, direction):
    """Flip image horizontally or vertically"""
    if direction == 'horizontal':
        return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    elif direction == 'vertical':
        return img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return img


def adjust_brightness(img, factor):
    """Adjust brightness (factor: 0.0 = black, 1.0 = original, 2.0 = twice as bright)"""
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def adjust_contrast(img, factor):
    """Adjust contrast (factor: 0.0 = gray, 1.0 = original, 2.0 = twice contrast)"""
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)


def adjust_color(img, factor):
    """Adjust color saturation (factor: 0.0 = grayscale, 1.0 = original, 2.0 = twice saturated)"""
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(factor)


def adjust_sharpness(img, factor):
    """Adjust sharpness (factor: 0.0 = blurred, 1.0 = original, 2.0 = sharper)"""
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(factor)


def apply_filter(img, filter_name):
    """Apply image filter"""
    filters = {
        'blur': ImageFilter.BLUR,
        'contour': ImageFilter.CONTOUR,
        'detail': ImageFilter.DETAIL,
        'edge_enhance': ImageFilter.EDGE_ENHANCE,
        'emboss': ImageFilter.EMBOSS,
        'sharpen': ImageFilter.SHARPEN,
        'smooth': ImageFilter.SMOOTH,
    }
    
    if filter_name in filters:
        return img.filter(filters[filter_name])
    return img


def convert_format(img, output_format):
    """Convert image to different format"""
    # Handle RGBA to RGB conversion for JPEG
    if output_format.upper() == 'JPEG' and img.mode == 'RGBA':
        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
        rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
        return rgb_img
    return img


def main():
    parser = argparse.ArgumentParser(description='Edit images with various operations')
    parser.add_argument('input', help='Input image file')
    parser.add_argument('output', help='Output image file')
    
    # Resize options
    parser.add_argument('--width', type=int, help='New width')
    parser.add_argument('--height', type=int, help='New height')
    parser.add_argument('--no-aspect', action='store_true', help='Ignore aspect ratio when resizing')
    
    # Crop options
    parser.add_argument('--crop', nargs=4, type=int, metavar=('X', 'Y', 'WIDTH', 'HEIGHT'),
                       help='Crop image (x, y, width, height)')
    
    # Rotation and flip
    parser.add_argument('--rotate', type=float, help='Rotate image by degrees')
    parser.add_argument('--flip', choices=['horizontal', 'vertical'], help='Flip image')
    
    # Adjustments
    parser.add_argument('--brightness', type=float, help='Adjust brightness (0.0-2.0)')
    parser.add_argument('--contrast', type=float, help='Adjust contrast (0.0-2.0)')
    parser.add_argument('--color', type=float, help='Adjust color saturation (0.0-2.0)')
    parser.add_argument('--sharpness', type=float, help='Adjust sharpness (0.0-2.0)')
    
    # Filters
    parser.add_argument('--filter', choices=['blur', 'contour', 'detail', 'edge_enhance', 
                                             'emboss', 'sharpen', 'smooth'],
                       help='Apply filter')
    
    # Format conversion
    parser.add_argument('--format', help='Output format (JPEG, PNG, GIF, BMP, etc.)')
    parser.add_argument('--quality', type=int, default=95, help='JPEG quality (1-100)')
    
    args = parser.parse_args()
    
    try:
        # Load image
        print(f"Loading image: {args.input}")
        img = Image.open(args.input)
        print(f"Original size: {img.size}, mode: {img.mode}")
        
        # Apply operations in order
        if args.crop:
            print(f"Cropping to: {args.crop}")
            img = crop_image(img, *args.crop)
        
        if args.width or args.height:
            keep_aspect = not args.no_aspect
            print(f"Resizing to: {args.width}x{args.height} (keep aspect: {keep_aspect})")
            img = resize_image(img, args.width, args.height, keep_aspect)
        
        if args.rotate:
            print(f"Rotating by: {args.rotate}°")
            img = rotate_image(img, args.rotate)
        
        if args.flip:
            print(f"Flipping: {args.flip}")
            img = flip_image(img, args.flip)
        
        if args.brightness:
            print(f"Adjusting brightness: {args.brightness}")
            img = adjust_brightness(img, args.brightness)
        
        if args.contrast:
            print(f"Adjusting contrast: {args.contrast}")
            img = adjust_contrast(img, args.contrast)
        
        if args.color:
            print(f"Adjusting color: {args.color}")
            img = adjust_color(img, args.color)
        
        if args.sharpness:
            print(f"Adjusting sharpness: {args.sharpness}")
            img = adjust_sharpness(img, args.sharpness)
        
        if args.filter:
            print(f"Applying filter: {args.filter}")
            img = apply_filter(img, args.filter)
        
        # Determine output format
        output_format = args.format or Path(args.output).suffix[1:].upper()
        if output_format:
            img = convert_format(img, output_format)
        
        # Save image
        save_kwargs = {}
        if output_format == 'JPEG':
            save_kwargs['quality'] = args.quality
            save_kwargs['optimize'] = True
        
        print(f"Saving to: {args.output}")
        img.save(args.output, **save_kwargs)
        print(f"✓ Image saved successfully! Final size: {img.size}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
