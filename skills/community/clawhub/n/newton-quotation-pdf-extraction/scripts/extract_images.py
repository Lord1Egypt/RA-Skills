#!/usr/bin/env python3
"""
Extract images from PDF file with optional splitting for combined images.
Usage: python extract_images.py <input.pdf> [--split] [--output-dir DIR]
"""

import argparse
import os
import sys
import fitz  # PyMuPDF
from PIL import Image
import io


def extract_all_images(pdf_path, output_dir="extracted_images"):
    """Extract all images from PDF."""
    os.makedirs(output_dir, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        
        print(f"Page {page_num + 1}: Found {len(image_list)} image(s)")
        
        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            width = base_image.get("width", 0)
            height = base_image.get("height", 0)
            
            output_path = f"{output_dir}/page{page_num+1}_img{img_index}.{image_ext}"
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            
            print(f"  Saved: page{page_num+1}_img{img_index}.{image_ext} ({width}x{height})")
    
    doc.close()
    print(f"\nImages saved to: {output_dir}")


def split_combined_image(image_path, split_count, output_prefix):
    """Split a combined image into individual product images."""
    img = Image.open(image_path)
    width, height = img.size
    
    item_height = height // split_count
    output_paths = []
    
    for i in range(split_count):
        top = i * item_height
        bottom = (i + 1) * item_height if i < split_count - 1 else height
        cropped = img.crop((0, top, width, bottom))
        
        output_path = f"{output_prefix}_{i+1}.png"
        cropped.save(output_path)
        output_paths.append(output_path)
        print(f"  Split: {output_path} ({cropped.size})")
    
    return output_paths


def analyze_images(pdf_path):
    """Analyze images in PDF and suggest split configurations."""
    doc = fitz.open(pdf_path)
    page = doc[0]
    image_list = page.get_images(full=True)
    
    print(f"PDF: {pdf_path}")
    print(f"Total images: {len(image_list)}\n")
    print("Image Analysis:")
    print("-" * 60)
    
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        width = base_image.get("width", 0)
        height = base_image.get("height", 0)
        
        # Detect potential combined images
        aspect_ratio = height / width if width > 0 else 0
        is_combined = aspect_ratio > 2.5  # Tall images likely contain multiple products
        
        print(f"Image {img_index}:")
        print(f"  Size: {width}x{height}")
        print(f"  Aspect Ratio: {aspect_ratio:.2f}")
        print(f"  Likely Combined: {'Yes' if is_combined else 'No'}")
        if is_combined:
            suggested_splits = round(aspect_ratio)
            print(f"  Suggested Splits: ~{suggested_splits}")
        print()
    
    doc.close()


def main():
    parser = argparse.ArgumentParser(description="Extract images from PDF")
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("--output-dir", "-o", default="extracted_images",
                        help="Output directory (default: extracted_images)")
    parser.add_argument("--analyze", "-a", action="store_true",
                        help="Analyze images and suggest split configurations")
    parser.add_argument("--split", "-s", type=int, metavar="N",
                        help="Split each image into N parts vertically")
    
    args = parser.parse_args()
    
    try:
        if args.analyze:
            analyze_images(args.input)
        elif args.split:
            # Extract and split
            os.makedirs(args.output_dir, exist_ok=True)
            doc = fitz.open(args.input)
            page = doc[0]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                
                # Skip full-page screenshots
                if base_image.get("width", 0) > 500:
                    continue
                
                pil_img = Image.open(io.BytesIO(base_image["image"]))
                width, height = pil_img.size
                
                item_height = height // args.split
                for i in range(args.split):
                    top = i * item_height
                    bottom = (i + 1) * item_height if i < args.split - 1 else height
                    cropped = pil_img.crop((0, top, width, bottom))
                    
                    output_path = f"{args.output_dir}/img{img_index}_part{i+1}.png"
                    cropped.save(output_path)
                    print(f"Saved: {output_path}")
            
            doc.close()
        else:
            # Simple extraction
            extract_all_images(args.input, args.output_dir)
    
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
