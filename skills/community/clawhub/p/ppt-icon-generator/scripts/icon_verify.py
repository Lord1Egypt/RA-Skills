#!/usr/bin/env python3
"""
Icon Verify - Check icon properties
"""

import argparse
from PIL import Image

def verify_icon(file_path):
    """Verify icon file"""
    try:
        with Image.open(file_path) as img:
            print(f"📁 File: {file_path}")
            print(f"📐 Size: {img.size[0]}x{img.size[1]}")
            print(f"🖼️  Format: {img.format}")
            print(f"🎨 Mode: {img.mode}")
            
            if img.mode == 'RGBA':
                # Check if has transparency
                alpha = img.split()[-1]
                has_transparency = any(p < 255 for p in alpha.getdata())
                print(f"✨ Transparent: {'Yes' if has_transparency else 'No (solid)'}")
            else:
                print(f"✨ Transparent: No ({img.mode} mode)")
            
            print(f"💾 File size: {img.fp.seek(0, 2) / 1024:.1f} KB")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Verify icon properties')
    parser.add_argument('--file', '-f', required=True, help='Icon file to verify')
    args = parser.parse_args()
    
    verify_icon(args.file)

if __name__ == '__main__':
    main()
