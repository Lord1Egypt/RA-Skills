import os
import sys
import argparse
from PIL import Image

def is_ig_bg(r, g, b):
    # Instagram dark mode is exactly RGB (12, 15, 20)
    return (abs(r - 12) + abs(g - 15) + abs(b - 20) < 15) or (r < 10 and g < 10 and b < 10)

def intelligent_ig_crop(input_path, output_path):
    try:
        img = Image.open(input_path).convert("RGB")
        w, h = img.size
        pixels = img.load()
        
        is_bg_row = []
        for y in range(h):
            matches = sum(1 for x in range(0, w, 10) if is_ig_bg(*pixels[x, y]))
            is_bg_row.append(matches / (w // 10) > 0.85)
            
        blocks = []
        in_block = False
        start = 0
        for y in range(h):
            if not is_bg_row[y]:
                if not in_block:
                    in_block = True
                    start = y
            else:
                if in_block:
                    in_block = False
                    blocks.append((start, y))
        if in_block:
            blocks.append((start, h))
            
        if not blocks:
            # Not an IG screenshot, save original
            img.save(output_path)
            return True
            
        blocks.sort(key=lambda b: b[1] - b[0], reverse=True)
        top, bottom = blocks[0]
        
        # Validation: prevent tiny erroneous crops
        if bottom - top < h * 0.1:
            img.save(output_path)
            return True
            
        cropped = img.crop((0, top, w, bottom))
        cropped.save(output_path)
        print(f"Successfully cropped photograph (rows {top} to {bottom})")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleanly crop IG screenshots without altering image content")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    
    args = parser.parse_args()
    intelligent_ig_crop(args.input, args.output)
