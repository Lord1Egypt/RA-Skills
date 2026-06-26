#!/usr/bin/env python3
"""
Image Deduplicator
Find and remove duplicate or similar images
"""

import argparse
import hashlib
import os
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple
from PIL import Image

try:
    import imagehash
    HAS_IMAGEHASH = True
except ImportError:
    HAS_IMAGEHASH = False


def get_file_hash(file_path: str) -> str:
    """Get MD5 hash of a file"""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def get_perceptual_hash(file_path: str) -> str:
    """Get perceptual hash of an image"""
    if not HAS_IMAGEHASH:
        return get_file_hash(file_path)
    
    try:
        with Image.open(file_path) as img:
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            return str(imagehash.phash(img))
    except Exception as e:
        print(f"Warning: Cannot hash {file_path}: {e}")
        return get_file_hash(file_path)


def get_image_hash(file_path: str, use_phash: bool = True) -> str:
    """Get hash of an image file"""
    if use_phash and HAS_IMAGEHASH:
        return get_perceptual_hash(file_path)
    else:
        return get_file_hash(file_path)


def scan_directory(directory: str, extensions: List[str], 
                   use_phash: bool = True) -> Dict[str, List[str]]:
    """Scan directory and find duplicates"""
    directory = Path(directory)
    
    # Find all image files
    image_files = []
    for ext in extensions:
        image_files.extend(directory.rglob(f"*.{ext}"))
        image_files.extend(directory.rglob(f"*.{ext.upper()}"))
    
    image_files = [str(f) for f in image_files if f.is_file()]
    
    if not image_files:
        print("No image files found")
        return {}
    
    print(f"Scanning {len(image_files)} images...")
    
    # Group by hash
    hash_groups = defaultdict(list)
    
    for i, file_path in enumerate(image_files):
        if i % 10 == 0:
            print(f"  Processing {i}/{len(image_files)}...")
        
        try:
            file_hash = get_image_hash(file_path, use_phash)
            hash_groups[file_hash].append(file_path)
        except Exception as e:
            print(f"Warning: Cannot process {file_path}: {e}")
    
    # Filter to only groups with duplicates
    duplicates = {h: files for h, files in hash_groups.items() if len(files) > 1}
    
    return duplicates


def format_size(file_path: str) -> str:
    """Get human-readable file size"""
    try:
        size = os.path.getsize(file_path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"
    except:
        return "?"


def cmd_scan(args):
    """Scan for duplicates"""
    duplicates = scan_directory(
        args.directory,
        args.extensions.split(','),
        use_phash=(args.threshold < 100)
    )
    
    if not duplicates:
        print("No duplicates found!")
        return
    
    print(f"\nFound {len(duplicate_groups := list(duplicates.keys()))} duplicate groups:")
    
    total_dup_files = 0
    for i, (hash_val, files) in enumerate(duplicates.items(), 1):
        print(f"\nGroup {i} ({len(files)} files):")
        for j, file_path in enumerate(files):
            size = format_size(file_path)
            prefix = "  ✓ " if j == 0 else "  ✗ "
            print(f"{prefix}{file_path} ({size})")
        
        total_dup_files += len(files) - 1
    
    print(f"\nTotal: {len(duplicates)} groups, {total_dup_files} duplicate files")
    
    # Handle action
    if args.action == "delete":
        confirm = input("\nDelete duplicates? (y/n): ")
        if confirm.lower() != 'y':
            print("Cancelled")
            return
        
        deleted = 0
        for files in duplicates.values():
            # Keep first, delete rest
            for file_path in files[1:]:
                try:
                    os.remove(file_path)
                    deleted += 1
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        
        print(f"\nDeleted {deleted} files")
    
    elif args.action == "move":
        output_dir = args.output or "duplicates"
        os.makedirs(output_dir, exist_ok=True)
        
        moved = 0
        for i, files in enumerate(duplicates.values(), 1):
            # Keep first, move rest
            for file_path in files[1:]:
                try:
                    basename = os.path.basename(file_path)
                    dest = os.path.join(output_dir, f"dup_{i}_{basename}")
                    shutil.move(file_path, dest)
                    moved += 1
                    print(f"Moved: {file_path} -> {dest}")
                except Exception as e:
                    print(f"Error moving {file_path}: {e}")
        
        print(f"\nMoved {moved} files to {output_dir}/")


def main():
    parser = argparse.ArgumentParser(
        description="Image Deduplicator - Find and remove duplicate images"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # scan command
    parser_scan = subparsers.add_parser("scan", help="Scan for duplicates")
    parser_scan.add_argument("directory", help="Directory to scan")
    parser_scan.add_argument("--threshold", "-t", type=int, default=100,
                            help="Similarity threshold 0-100 (default: 100 = exact)")
    parser_scan.add_argument("--action", "-a", choices=['list', 'delete', 'move'],
                            default='list', help="Action to take")
    parser_scan.add_argument("--output", "-o", default="",
                            help="Output directory for --action move")
    parser_scan.add_argument("--extensions", "-e", default="jpg,jpeg,png,bmp,gif,webp",
                            help="File extensions to scan (comma-separated)")
    parser_scan.set_defaults(func=cmd_scan)
    
    args = parser.parse_args()
    
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
