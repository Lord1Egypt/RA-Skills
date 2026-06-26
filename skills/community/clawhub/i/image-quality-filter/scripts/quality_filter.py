#!/usr/bin/env python3
"""
Image Quality Filter
Detect and filter out low-quality images
"""

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from PIL import Image
import math

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


def calculate_blur_laplacian(image: Image.Image) -> float:
    """Calculate blur score using Laplacian variance"""
    if not HAS_CV2:
        return 200  # Default high score if no cv2
    
    import numpy as np
    try:
        # Convert to grayscale
        img_array = image.convert('L')
        img_np = np.array(img_array)
        
        # Calculate Laplacian
        laplacian = cv2.Laplacian(img_np, cv2.CV_64F)
        variance = laplacian.var()
        return variance
    except:
        return 200


def calculate_brightness(image: Image.Image) -> float:
    """Calculate average brightness"""
    try:
        # Convert to grayscale
        gray = image.convert('L')
        # Get histogram
        hist = gray.histogram()
        
        # Calculate weighted average
        total = sum(hist)
        if total == 0:
            return 0
        
        brightness = sum(i * hist[i] for i in range(256)) / total
        return brightness
    except:
        return 128


def get_resolution(image: Image.Image) -> Tuple[int, int]:
    """Get image resolution"""
    return image.width, image.height


def analyze_image(file_path: str, blur_threshold: float = 100,
                 min_brightness: float = 30, max_brightness: float = 220,
                 min_width: int = 640, min_height: int = 480) -> Dict:
    """Analyze a single image and return quality info"""
    result = {
        'path': file_path,
        'issues': [],
        'score': 100
    }
    
    try:
        with Image.open(file_path) as img:
            # Check resolution
            width, height = get_resolution(img)
            result['resolution'] = (width, height)
            
            if width < min_width or height < min_height:
                result['issues'].append('RES')
                result['score'] -= 40
            
            # Check brightness
            brightness = calculate_brightness(img)
            result['brightness'] = brightness
            
            if brightness < min_brightness:
                result['issues'].append('DARK')
                result['score'] -= 30
            elif brightness > max_brightness:
                result['issues'].append('BRIGHT')
                result['score'] -= 30
            
            # Check blur
            blur_score = calculate_blur_laplacian(img)
            result['blur'] = blur_score
            
            if blur_score < blur_threshold:
                result['issues'].append('BLUR')
                result['score'] -= 40
            
            # Cap score at 0
            result['score'] = max(0, result['score'])
    
    except Exception as e:
        result['issues'].append('ERROR')
        result['error'] = str(e)
        result['score'] = 0
    
    return result


def scan_directory(directory: str, extensions: List[str],
                  blur_threshold: float, min_brightness: float,
                  max_brightness: float, min_width: int, min_height: int) -> List[Dict]:
    """Scan directory for low quality images"""
    directory = Path(directory)
    
    # Find all image files
    image_files = []
    for ext in extensions:
        image_files.extend(directory.rglob(f"*.{ext}"))
        image_files.extend(directory.rglob(f"*.{ext.upper()}"))
    
    image_files = [str(f) for f in image_files if f.is_file()]
    
    if not image_files:
        print("No image files found")
        return []
    
    print(f"Scanning {len(image_files)} images...")
    
    results = []
    for i, file_path in enumerate(image_files):
        if i % 10 == 0:
            print(f"  Analyzing {i}/{len(image_files)}...")
        
        result = analyze_image(
            file_path, blur_threshold, min_brightness, max_brightness,
            min_width, min_height
        )
        results.append(result)
    
    return results


def format_size(file_path: str) -> str:
    """Get human-readable file size"""
    try:
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{1}GB"
    except:
        return "?"


def cmd_scan(args):
    """Scan for low quality images"""
    results = scan_directory(
        args.directory,
        args.extensions.split(','),
        args.blur_threshold,
        args.min_brightness,
        args.max_brightness,
        args.min_width,
        args.min_height
    )
    
    # Filter to only low quality
    low_quality = [r for r in results if r['issues']]
    
    if not low_quality:
        print("No low quality images found!")
        return
    
    print(f"\nFound {len(low_quality)} low-quality images:")
    
    for r in low_quality:
        issues = ','.join(r['issues'])
        print(f"[{issues:6s}] {r['path']} (score: {r['score']})")
    
    print(f"\nTotal: {len(low_quality)} low-quality images")
    
    # Handle action
    if args.action == "delete":
        confirm = input("\nDelete low quality images? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled")
            return
        
        deleted = 0
        for r in low_quality:
            try:
                os.remove(r['path'])
                deleted += 1
                print(f"Deleted: {r['path']}")
            except Exception as e:
                print(f"Error deleting {r['path']}: {e}")
        
        print(f"\nDeleted {deleted} files")
    
    elif args.action == "move":
        output_dir = args.output or "low_quality"
        os.makedirs(output_dir, exist_ok=True)
        
        moved = 0
        for r in low_quality:
            try:
                basename = os.path.basename(r['path'])
                dest = os.path.join(output_dir, basename)
                shutil.move(r['path'], dest)
                moved += 1
                print(f"Moved: {r['path']} -> {dest}")
            except Exception as e:
                print(f"Error moving {r['path']}: {e}")
        
        print(f"\nMoved {moved} files to {output_dir}/")


def main():
    parser = argparse.ArgumentParser(
        description="Image Quality Filter - Detect and filter low-quality images"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # scan command
    parser_scan = subparsers.add_parser("scan", help="Scan for low quality images")
    parser_scan.add_argument("directory", help="Directory to scan")
    parser_scan.add_argument("--blur-threshold", "-b", type=float, default=100,
                            help="Blur threshold (default: 100)")
    parser_scan.add_argument("--min-resolution", "-r", default="640x480",
                            help="Minimum resolution (default: 640x480)")
    parser_scan.add_argument("--min-brightness", type=float, default=30,
                            help="Minimum brightness 0-255 (default: 30)")
    parser_scan.add_argument("--max-brightness", type=float, default=220,
                            help="Maximum brightness 0-255 (default: 220)")
    parser_scan.add_argument("--action", "-a", choices=['list', 'delete', 'move'],
                            default='list', help="Action to take")
    parser_scan.add_argument("--output", "-o", default="",
                            help="Output directory for --action move")
    parser_scan.add_argument("--extensions", "-e", default="jpg,jpeg,png,bmp,gif,webp",
                            help="File extensions to scan")
    parser_scan.set_defaults(func=cmd_scan)
    
    args = parser.parse_args()
    
    # Parse resolution
    if hasattr(args, 'min_resolution'):
        res_parts = args.min_resolution.lower().split('x')
        if len(res_parts) == 2:
            args.min_width = int(res_parts[0])
            args.min_height = int(res_parts[1])
        else:
            args.min_width = 640
            args.min_height = 480
    
    if args.command is None:
        parser.print_help()
        return
    
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
