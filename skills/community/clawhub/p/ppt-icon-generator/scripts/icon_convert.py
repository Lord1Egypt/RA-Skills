#!/usr/bin/env python3
"""
SVG to PNG Converter
"""

import argparse
import os
import sys

def convert_svg_to_png(svg_path, png_path, size=512):
    """Convert SVG file to PNG"""
    try:
        # Try cairosvg first
        import cairosvg
        cairosvg.svg2png(url=svg_path, write_to=png_path, 
                        output_width=size, output_height=size)
        print(f"✅ Converted: {png_path}")
        return True
    except ImportError:
        pass
    
    # Try svglib + reportlab
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        
        drawing = svg2rlg(svg_path)
        if drawing:
            renderPM.drawToFile(drawing, png_path, fmt="PNG")
            print(f"✅ Converted: {png_path}")
            return True
    except ImportError:
        pass
    
    # Try inkscape
    import subprocess
    try:
        cmd = [
            'inkscape',
            svg_path,
            '--export-filename', png_path,
            '--export-width', str(size),
            '--export-height', str(size)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Converted: {png_path}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    print("❌ No SVG converter available. Install one of:")
    print("   pip install cairosvg")
    print("   pip install svglib reportlab")
    print("   apt install inkscape")
    return False

def main():
    parser = argparse.ArgumentParser(description='Convert SVG to PNG')
    parser.add_argument('--input', '-i', required=True, help='Input SVG file')
    parser.add_argument('--output', '-o', help='Output PNG file')
    parser.add_argument('--size', '-s', type=int, default=512, help='Output size')
    
    args = parser.parse_args()
    
    if not args.output:
        args.output = args.input.replace('.svg', '.png')
    
    if convert_svg_to_png(args.input, args.output, args.size):
        return 0
    return 1

if __name__ == '__main__':
    sys.exit(main())
