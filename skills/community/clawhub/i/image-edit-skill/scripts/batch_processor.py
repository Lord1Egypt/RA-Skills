#!/usr/bin/env python3
"""
Batch Image Processor - Process multiple images at once
"""

import argparse
import sys
from pathlib import Path
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_single_image(input_path, output_dir, operations):
    """Process a single image with specified operations"""
    try:
        img = Image.open(input_path)
        
        # Apply operations
        if 'resize' in operations:
            width, height = operations['resize']
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        if 'thumbnail' in operations:
            size = operations['thumbnail']
            img.thumbnail(size, Image.Resampling.LANCZOS)
        
        if 'grayscale' in operations:
            img = img.convert('L')
        
        if 'brightness' in operations:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(operations['brightness'])
        
        if 'format' in operations:
            output_format = operations['format']
            if output_format.upper() == 'JPEG' and img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
                img = rgb_img
        
        # Determine output path
        output_path = Path(output_dir) / input_path.name
        if 'format' in operations:
            output_path = output_path.with_suffix(f".{operations['format'].lower()}")
        
        # Save
        save_kwargs = {}
        if output_path.suffix.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = operations.get('quality', 95)
            save_kwargs['optimize'] = True
        
        img.save(output_path, **save_kwargs)
        return f"✓ {input_path.name} → {output_path.name}"
        
    except Exception as e:
        return f"✗ {input_path.name}: {e}"


def main():
    parser = argparse.ArgumentParser(description='Batch process images')
    parser.add_argument('input_dir', help='Input directory containing images')
    parser.add_argument('output_dir', help='Output directory for processed images')
    parser.add_argument('--pattern', default='*.*', help='File pattern (e.g., *.jpg)')
    
    # Operations
    parser.add_argument('--resize', nargs=2, type=int, metavar=('WIDTH', 'HEIGHT'),
                       help='Resize all images to width x height')
    parser.add_argument('--thumbnail', nargs=2, type=int, metavar=('MAX_W', 'MAX_H'),
                       help='Create thumbnails (maintains aspect ratio)')
    parser.add_argument('--grayscale', action='store_true', help='Convert to grayscale')
    parser.add_argument('--brightness', type=float, help='Adjust brightness (0.0-2.0)')
    parser.add_argument('--format', help='Convert to format (JPEG, PNG, etc.)')
    parser.add_argument('--quality', type=int, default=95, help='JPEG quality (1-100)')
    
    # Processing options
    parser.add_argument('--workers', type=int, default=4, help='Number of parallel workers')
    
    args = parser.parse_args()
    
    # Validate directories
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    if not input_dir.exists():
        print(f"Error: Input directory '{input_dir}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all images
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    image_files = [f for f in input_dir.glob(args.pattern) 
                   if f.suffix.lower() in image_extensions]
    
    if not image_files:
        print(f"No images found in '{input_dir}' matching pattern '{args.pattern}'")
        sys.exit(1)
    
    print(f"Found {len(image_files)} images to process")
    
    # Prepare operations
    operations = {}
    if args.resize:
        operations['resize'] = tuple(args.resize)
    if args.thumbnail:
        operations['thumbnail'] = tuple(args.thumbnail)
    if args.grayscale:
        operations['grayscale'] = True
    if args.brightness:
        operations['brightness'] = args.brightness
    if args.format:
        operations['format'] = args.format
        operations['quality'] = args.quality
    
    print(f"Operations: {operations}")
    print(f"Processing with {args.workers} workers...\n")
    
    # Process images in parallel
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_single_image, img, output_dir, operations): img 
                  for img in image_files}
        
        for future in as_completed(futures):
            result = future.result()
            print(result)
    
    print(f"\n✓ Batch processing complete! Output: {output_dir}")


if __name__ == '__main__':
    main()
