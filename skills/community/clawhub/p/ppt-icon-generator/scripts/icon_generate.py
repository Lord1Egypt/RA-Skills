#!/usr/bin/env python3
"""
Icon Generator - Generate custom icons using Pillow
"""

import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import math

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_gradient(size, color1, color2, direction='diagonal'):
    """Create gradient background"""
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    width, height = size
    
    for y in range(height):
        for x in range(width):
            if direction == 'horizontal':
                ratio = x / width
            elif direction == 'vertical':
                ratio = y / height
            else:  # diagonal
                ratio = (x + y) / (width + height)
            
            r = int(rgb1[0] * (1 - ratio) + rgb2[0] * ratio)
            g = int(rgb1[1] * (1 - ratio) + rgb2[1] * ratio)
            b = int(rgb1[2] * (1 - ratio) + rgb2[2] * ratio)
            
            draw.point((x, y), fill=(r, g, b, 255))
    
    return img

def draw_circle(draw, center, radius, color, width=0):
    """Draw a circle"""
    x, y = center
    bbox = [x - radius, y - radius, x + radius, y + radius]
    draw.ellipse(bbox, fill=color if width == 0 else None, outline=color, width=width)

def draw_rounded_rect(draw, bbox, radius, color, width=0):
    """Draw rounded rectangle"""
    x1, y1, x2, y2 = bbox
    
    # Draw main rectangle
    if width == 0:
        draw.rounded_rectangle(bbox, radius=radius, fill=color)
    else:
        draw.rounded_rectangle(bbox, radius=radius, outline=color, width=width)

def draw_diamond(draw, center, size, color, width=0):
    """Draw diamond shape"""
    x, y = center
    points = [
        (x, y - size),      # top
        (x + size, y),      # right
        (x, y + size),      # bottom
        (x - size, y)       # left
    ]
    
    if width == 0:
        draw.polygon(points, fill=color)
    else:
        draw.polygon(points, outline=color)
        # Draw inner fill if needed
        inner_size = size - width
        if inner_size > 0:
            inner_points = [
                (x, y - inner_size),
                (x + inner_size, y),
                (x, y + inner_size),
                (x - inner_size, y)
            ]
            draw.polygon(inner_points, fill=(255, 255, 255, 0))

def draw_star(draw, center, outer_radius, inner_radius, points_count, color):
    """Draw star shape"""
    x, y = center
    points = []
    
    for i in range(points_count * 2):
        angle = math.pi / 2 + i * math.pi / points_count
        radius = outer_radius if i % 2 == 0 else inner_radius
        px = x + radius * math.cos(angle)
        py = y - radius * math.sin(angle)
        points.append((px, py))
    
    draw.polygon(points, fill=color)

def draw_arrow(draw, start, end, color, width=8):
    """Draw arrow line"""
    # Draw line
    draw.line([start, end], fill=color, width=width)
    
    # Draw arrowhead
    x1, y1 = start
    x2, y2 = end
    
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_length = 20
    arrow_angle = math.pi / 6
    
    x3 = x2 - arrow_length * math.cos(angle - arrow_angle)
    y3 = y2 - arrow_length * math.sin(angle - arrow_angle)
    x4 = x2 - arrow_length * math.cos(angle + arrow_angle)
    y4 = y2 - arrow_length * math.sin(angle + arrow_angle)
    
    draw.polygon([(x2, y2), (x3, y3), (x4, y4)], fill=color)

def generate_shape_icon(shape, size, color, output_path, style='flat'):
    """Generate icon with basic shape"""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    rgb_color = hex_to_rgb(color)
    
    padding = size // 8
    inner_size = size - 2 * padding
    center = (size // 2, size // 2)
    
    if shape == 'circle':
        radius = inner_size // 2
        if style == 'line':
            draw_circle(draw, center, radius, rgb_color, width=size//20)
        else:
            draw_circle(draw, center, radius, rgb_color)
    
    elif shape == 'square':
        bbox = [padding, padding, size - padding, size - padding]
        if style == 'line':
            draw.rectangle(bbox, outline=rgb_color, width=size//20)
        else:
            draw.rectangle(bbox, fill=rgb_color)
    
    elif shape == 'rounded-rect':
        bbox = [padding, padding, size - padding, size - padding]
        radius = size // 10
        if style == 'line':
            draw_rounded_rect(draw, bbox, radius, rgb_color, width=size//20)
        else:
            draw_rounded_rect(draw, bbox, radius, rgb_color)
    
    elif shape == 'diamond':
        diamond_size = inner_size // 2
        if style == 'line':
            draw_diamond(draw, center, diamond_size, rgb_color, width=size//20)
        else:
            draw_diamond(draw, center, diamond_size, rgb_color)
    
    elif shape == 'star':
        outer_r = inner_size // 2
        inner_r = outer_r // 2
        draw_star(draw, center, outer_r, inner_r, 5, rgb_color)
    
    elif shape == 'triangle':
        points = [
            (center[0], padding),
            (size - padding, size - padding),
            (padding, size - padding)
        ]
        if style == 'line':
            draw.polygon(points, outline=rgb_color)
        else:
            draw.polygon(points, fill=rgb_color)
    
    elif shape == 'arrow-right':
        y = size // 2
        start = (padding, y)
        end = (size - padding, y)
        draw_arrow(draw, start, end, rgb_color, width=size//15)
    
    elif shape == 'check':
        # Draw checkmark
        line_width = size // 15
        # First stroke
        draw.line([(size//4, size//2), (size//2, 3*size//4)], 
                 fill=rgb_color, width=line_width)
        # Second stroke
        draw.line([(size//2, 3*size//4), (3*size//4, size//4)], 
                 fill=rgb_color, width=line_width)
    
    elif shape == 'x':
        # Draw X
        line_width = size // 15
        padding = size // 4
        draw.line([(padding, padding), (size-padding, size-padding)], 
                 fill=rgb_color, width=line_width)
        draw.line([(padding, size-padding), (size-padding, padding)], 
                 fill=rgb_color, width=line_width)
    
    img.save(output_path, 'PNG')
    print(f"✅ Generated: {output_path}")
    return True

def generate_text_icon(text, size, color, output_path, bg_color=None):
    """Generate icon with text"""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    rgb_color = hex_to_rgb(color)
    
    # Try to use a nice font
    font_size = size // 2
    font = None
    
    # Try different fonts
    font_paths = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/truetype/freefont/FreeSansBold.ttf',
        '/System/Library/Fonts/Helvetica.ttc',  # macOS
        'C:/Windows/Fonts/arial.ttf',  # Windows
    ]
    
    for font_path in font_paths:
        try:
            font = ImageFont.truetype(font_path, font_size)
            break
        except:
            continue
    
    if font is None:
        font = ImageFont.load_default()
    
    # Calculate text position
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Draw background if specified
    if bg_color:
        rgb_bg = hex_to_rgb(bg_color)
        padding = size // 8
        draw.rounded_rectangle(
            [padding, padding, size - padding, size - padding],
            radius=size // 10,
            fill=rgb_bg
        )
    
    # Draw text
    draw.text((x, y), text, font=font, fill=rgb_color)
    
    img.save(output_path, 'PNG')
    print(f"✅ Generated: {output_path}")
    return True

def generate_gradient_icon(shape, size, color1, color2, output_path):
    """Generate icon with gradient background"""
    # Create gradient background
    img = create_gradient((size, size), color1, color2, 'diagonal')
    
    # Create mask for shape
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    
    padding = size // 8
    center = (size // 2, size // 2)
    inner_size = size - 2 * padding
    
    if shape == 'circle':
        radius = inner_size // 2
        mask_draw.ellipse(
            [center[0]-radius, center[1]-radius, 
             center[0]+radius, center[1]+radius],
            fill=255
        )
    else:
        # Default to rounded rect
        mask_draw.rounded_rectangle(
            [padding, padding, size - padding, size - padding],
            radius=size // 10,
            fill=255
        )
    
    # Apply mask
    result = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    result.paste(img, (0, 0), mask)
    
    result.save(output_path, 'PNG')
    print(f"✅ Generated: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Generate custom icons')
    parser.add_argument('--shape', '-s', 
                       choices=['circle', 'square', 'rounded-rect', 'diamond', 
                               'star', 'triangle', 'arrow-right', 'check', 'x'],
                       help='Basic shape to generate')
    parser.add_argument('--text', '-t', help='Text to render as icon')
    parser.add_argument('--prompt', '-p', help='Description (for AI generation)')
    parser.add_argument('--style', choices=['flat', 'line', 'gradient', 'filled'],
                       default='flat', help='Icon style')
    parser.add_argument('--color', '-c', default='#4ECDC4', help='Primary color (hex)')
    parser.add_argument('--color2', help='Secondary color for gradient (hex)')
    parser.add_argument('--bg-color', help='Background color (hex)')
    parser.add_argument('--size', type=int, default=512, help='Output size in pixels')
    parser.add_argument('--output', '-o', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    print(f"🎨 Generating icon: {args.output}")
    
    if args.text:
        # Generate text icon
        generate_text_icon(args.text, args.size, args.color, args.output, args.bg_color)
    
    elif args.shape:
        # Generate shape icon
        if args.style == 'gradient' and args.color2:
            generate_gradient_icon(args.shape, args.size, args.color, args.color2, args.output)
        else:
            generate_shape_icon(args.shape, args.size, args.color, args.output, args.style)
    
    elif args.prompt:
        print(f"💡 Prompt: {args.prompt}")
        print("⚠️  AI generation requires external API. Using shape fallback...")
        # Fallback to a generic shape
        generate_shape_icon('circle', args.size, args.color, args.output, args.style)
    
    else:
        print("❌ Please specify --shape, --text, or --prompt")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
