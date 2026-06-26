#!/usr/bin/env python3
"""
Watermark Tool - Add text or image watermarks to images
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def add_text_watermark(img, text, position='bottom-right', font_size=36, 
                       opacity=128, color='white', margin=10):
    """Add text watermark to image"""
    # Create a transparent layer
    watermark_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)
    
    # Try to load a font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Calculate text size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position
    width, height = img.size
    positions = {
        'top-left': (margin, margin),
        'top-right': (width - text_width - margin, margin),
        'bottom-left': (margin, height - text_height - margin),
        'bottom-right': (width - text_width - margin, height - text_height - margin),
        'center': ((width - text_width) // 2, (height - text_height) // 2),
    }
    
    pos = positions.get(position, positions['bottom-right'])
    
    # Parse color
    if isinstance(color, str):
        color_map = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
        }
        color_rgb = color_map.get(color.lower(), (255, 255, 255))
    else:
        color_rgb = color
    
    # Draw text with opacity
    draw.text(pos, text, font=font, fill=(*color_rgb, opacity))
    
    # Composite with original image
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    watermarked = Image.alpha_composite(img, watermark_layer)
    return watermarked


def add_image_watermark(img, watermark_path, position='bottom-right', 
                        scale=0.2, opacity=128, margin=10):
    """Add image watermark"""
    # Load watermark
    watermark = Image.open(watermark_path)
    
    # Resize watermark
    watermark_width = int(img.width * scale)
    watermark_height = int(watermark.height * watermark_width / watermark.width)
    watermark = watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)
    
    # Adjust opacity
    if watermark.mode != 'RGBA':
        watermark = watermark.convert('RGBA')
    
    alpha = watermark.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity / 255))
    watermark.putalpha(alpha)
    
    # Calculate position
    width, height = img.size
    wm_width, wm_height = watermark.size
    
    positions = {
        'top-left': (margin, margin),
        'top-right': (width - wm_width - margin, margin),
        'bottom-left': (margin, height - wm_height - margin),
        'bottom-right': (width - wm_width - margin, height - wm_height - margin),
        'center': ((width - wm_width) // 2, (height - wm_height) // 2),
    }
    
    pos = positions.get(position, positions['bottom-right'])
    
    # Convert base image to RGBA
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Create composite
    watermarked = img.copy()
    watermarked.paste(watermark, pos, watermark)
    
    return watermarked


def main():
    parser = argparse.ArgumentParser(description='Add watermark to images')
    parser.add_argument('input', help='Input image file')
    parser.add_argument('output', help='Output image file')
    
    # Watermark type
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text', help='Text watermark')
    group.add_argument('--image', help='Image watermark file')
    
    # Common options
    parser.add_argument('--position', default='bottom-right',
                       choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
                       help='Watermark position')
    parser.add_argument('--opacity', type=int, default=128, help='Opacity (0-255)')
    parser.add_argument('--margin', type=int, default=10, help='Margin from edge (pixels)')
    
    # Text-specific options
    parser.add_argument('--font-size', type=int, default=36, help='Font size for text')
    parser.add_argument('--color', default='white', help='Text color (white/black/red/etc)')
    
    # Image-specific options
    parser.add_argument('--scale', type=float, default=0.2, 
                       help='Watermark scale relative to image width (0.0-1.0)')
    
    args = parser.parse_args()
    
    try:
        # Load image
        print(f"Loading image: {args.input}")
        img = Image.open(args.input)
        
        # Add watermark
        if args.text:
            print(f"Adding text watermark: '{args.text}'")
            result = add_text_watermark(
                img, args.text, args.position, args.font_size, 
                args.opacity, args.color, args.margin
            )
        else:
            print(f"Adding image watermark: {args.image}")
            result = add_image_watermark(
                img, args.image, args.position, 
                args.scale, args.opacity, args.margin
            )
        
        # Convert back to RGB if output is JPEG
        if Path(args.output).suffix.lower() in ['.jpg', '.jpeg']:
            result = result.convert('RGB')
        
        # Save
        print(f"Saving to: {args.output}")
        result.save(args.output, quality=95, optimize=True)
        print("✓ Watermark added successfully!")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
