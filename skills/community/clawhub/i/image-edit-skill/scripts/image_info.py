#!/usr/bin/env python3
"""
Image Info - Extract and display image metadata and properties
"""

import argparse
import json
import sys
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS


def get_image_info(image_path):
    """Extract comprehensive image information"""
    img = Image.open(image_path)
    
    info = {
        'file': {
            'path': str(image_path),
            'name': image_path.name,
            'size_bytes': image_path.stat().st_size,
            'size_kb': round(image_path.stat().st_size / 1024, 2),
            'size_mb': round(image_path.stat().st_size / (1024 * 1024), 2),
        },
        'image': {
            'format': img.format,
            'mode': img.mode,
            'width': img.width,
            'height': img.height,
            'aspect_ratio': round(img.width / img.height, 2),
            'megapixels': round((img.width * img.height) / 1_000_000, 2),
        },
        'color': {
            'palette': img.palette.mode if img.palette else None,
            'bands': img.getbands(),
        }
    }
    
    # Extract EXIF data
    exif_data = {}
    try:
        exif = img.getexif()
        if exif:
            for tag_id, value in exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                # Convert bytes to string
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')
                    except:
                        value = str(value)
                exif_data[tag_name] = value
    except:
        pass
    
    if exif_data:
        info['exif'] = exif_data
    
    # Get image info dict
    if img.info:
        info['metadata'] = img.info
    
    return info


def format_info_text(info):
    """Format image info as readable text"""
    lines = []
    lines.append("=" * 60)
    lines.append(f"IMAGE INFORMATION: {info['file']['name']}")
    lines.append("=" * 60)
    lines.append("")
    
    lines.append("FILE:")
    lines.append(f"  Path: {info['file']['path']}")
    lines.append(f"  Size: {info['file']['size_kb']} KB ({info['file']['size_bytes']} bytes)")
    lines.append("")
    
    lines.append("IMAGE:")
    lines.append(f"  Format: {info['image']['format']}")
    lines.append(f"  Mode: {info['image']['mode']}")
    lines.append(f"  Dimensions: {info['image']['width']} x {info['image']['height']}")
    lines.append(f"  Aspect Ratio: {info['image']['aspect_ratio']}")
    lines.append(f"  Megapixels: {info['image']['megapixels']} MP")
    lines.append("")
    
    lines.append("COLOR:")
    lines.append(f"  Bands: {info['color']['bands']}")
    if info['color']['palette']:
        lines.append(f"  Palette: {info['color']['palette']}")
    lines.append("")
    
    if 'exif' in info and info['exif']:
        lines.append("EXIF DATA:")
        for key, value in info['exif'].items():
            # Skip very long values
            str_value = str(value)
            if len(str_value) > 100:
                str_value = str_value[:97] + "..."
            lines.append(f"  {key}: {str_value}")
        lines.append("")
    
    if 'metadata' in info and info['metadata']:
        lines.append("METADATA:")
        for key, value in info['metadata'].items():
            str_value = str(value)
            if len(str_value) > 100:
                str_value = str_value[:97] + "..."
            lines.append(f"  {key}: {str_value}")
        lines.append("")
    
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Display image information and metadata')
    parser.add_argument('image', help='Input image file')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format')
    parser.add_argument('--output', '-o', help='Save output to file')
    
    args = parser.parse_args()
    
    try:
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"Error: Image file '{args.image}' not found", file=sys.stderr)
            sys.exit(1)
        
        # Get image info
        info = get_image_info(image_path)
        
        # Format output
        if args.format == 'json':
            output = json.dumps(info, indent=2, ensure_ascii=False)
        else:
            output = format_info_text(info)
        
        # Display or save
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"✓ Image info saved to: {args.output}")
        else:
            print(output)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
