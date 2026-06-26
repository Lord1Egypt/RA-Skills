#!/usr/bin/env python3
"""
Extract product information from PDF catalog using sequential matching.
Usage: python extract_products.py <input.pdf> [--output products.xlsx] [--images-dir product_images]

This script uses sequential matching based on PDF visual order:
1. Products are defined in the order they appear in the PDF (top to bottom)
2. Images are extracted and split (combined images are detected by aspect ratio)
3. Products are matched to images sequentially
4. Results are exported to Excel

Note: You need to edit the PRODUCTS_IN_ORDER list to match your PDF content.
"""

import argparse
import os
import sys
import fitz
from PIL import Image
import io
import pandas as pd


def ask_currency():
    """Ask user for currency."""
    print("\n" + "="*60)
    print("Currency Detection")
    print("="*60)
    print("PDF files typically don't include currency symbols.")
    print("Please specify the currency for the prices in this PDF.\n")
    print("Common currencies:")
    print("  CNY - Chinese Yuan (人民币)")
    print("  USD - US Dollar (美元)")
    print("  EUR - Euro (欧元)")
    print("  BRL - Brazilian Real (巴西雷亚尔)")
    print("  JPY - Japanese Yen (日元)")
    print("  GBP - British Pound (英镑)")
    print("  or enter any other currency code\n")
    
    while True:
        currency = input("Enter currency code (e.g., CNY, USD, BRL): ").strip().upper()
        if currency:
            confirm = input(f"Confirm currency is {currency}? (y/n): ").strip().lower()
            if confirm == 'y':
                return currency
        print("Please enter a valid currency code.\n")


def extract_and_split_images(pdf_path, output_dir="product_images"):
    """
    Extract images from PDF, split combined images, save ALL parts.
    Returns list of image parts in PDF order.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    doc = fitz.open(pdf_path)
    page = doc[0]
    
    image_list = page.get_images(full=True)
    
    # Extract all images (excluding full-page screenshots)
    raw_images = []
    for img_idx, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        
        # Skip full-page screenshots (width > 500)
        if base_image.get("width", 0) > 500:
            print(f"  Skipping full-page image: {base_image['width']}x{base_image['height']}")
            continue
        
        pil_img = Image.open(io.BytesIO(base_image["image"]))
        raw_images.append({
            'index': len(raw_images),
            'image': pil_img,
            'width': pil_img.size[0],
            'height': pil_img.size[1]
        })
    
    doc.close()
    
    # Split images based on aspect ratio and save ALL parts
    all_image_parts = []
    part_counter = 0
    
    for raw_img in raw_images:
        aspect_ratio = raw_img['height'] / raw_img['width'] if raw_img['width'] > 0 else 0
        
        # Determine split count based on aspect ratio
        if aspect_ratio > 2.5:
            split_count = 3  # Likely 3 products
        elif aspect_ratio > 1.8:
            split_count = 2  # Likely 2 products
        else:
            split_count = 1  # Single product
        
        if split_count > 1:
            item_height = raw_img['height'] // split_count
            for i in range(split_count):
                top = i * item_height
                bottom = (i + 1) * item_height if i < split_count - 1 else raw_img['height']
                cropped = raw_img['image'].crop((0, top, raw_img['width'], bottom))
                
                output_path = f"{output_dir}/img_{part_counter:02d}.png"
                cropped.save(output_path)
                
                all_image_parts.append({
                    'path': output_path,
                    'index': part_counter
                })
                part_counter += 1
        else:
            output_path = f"{output_dir}/img_{part_counter:02d}.png"
            raw_img['image'].save(output_path)
            
            all_image_parts.append({
                'path': output_path,
                'index': part_counter
            })
            part_counter += 1
    
    return all_image_parts


def match_products_sequentially(products_in_order, image_parts, currency):
    """
    Match products with images sequentially based on PDF order.
    """
    matched_products = []
    image_idx = 0
    
    for model, qty, price, num_images in products_in_order:
        product_images = []
        
        # Consume the specified number of images for this product
        for i in range(num_images):
            if image_idx < len(image_parts):
                product_images.append(image_parts[image_idx])
                image_idx += 1
        
        if product_images:
            primary_image = product_images[0]['path']
            all_paths = ', '.join([img['path'] for img in product_images])
        else:
            primary_image = ''
            all_paths = ''
        
        matched_products.append({
            'model': model,
            'quantity': qty,
            'currency': currency,
            'price': price,
            'image_path': primary_image,
            'all_images': all_paths
        })
    
    return matched_products


def extract_with_visual_mapping(pdf_path, output_dir, products, image_mapping):
    """
    Extract images with manual visual mapping.
    Use this when PyMuPDF returns images in xref order (not visual order).
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Output directory for images
        products: List of product dicts with model, quantity, price
        image_mapping: Dict mapping image_index -> (model_list, split_count)
                      Example: {1: (["800C"], 1), 6: (["S6", "X6", "X7"], 3)}
    
    Returns:
        List of product dicts with image_path added
    """
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    page = doc[0]
    image_list = page.get_images(full=True)
    
    # Create product lookup by model
    product_lookup = {p['model']: p for p in products}
    
    for img_idx, img in enumerate(image_list):
        if img_idx not in image_mapping:
            continue
            
        xref = img[0]
        base_image = doc.extract_image(xref)
        
        # Skip full-page screenshots
        if base_image.get("width", 0) > 500:
            continue
        
        model_list, split_count = image_mapping[img_idx]
        pil_img = Image.open(io.BytesIO(base_image["image"]))
        width, height = pil_img.size
        
        print(f"  Processing image {img_idx}: {width}x{height}, models={model_list}, splits={split_count}")
        
        if split_count == 1:
            # Single product
            model = model_list[0]
            output_path = f"{output_dir}/{model}.png"
            pil_img.save(output_path)
            if model in product_lookup:
                product_lookup[model]['image_path'] = output_path
                print(f"    -> Saved: {model}.png")
        else:
            # Split combined image
            item_height = height // split_count
            for i in range(min(split_count, len(model_list))):
                model = model_list[i]
                top = i * item_height
                bottom = (i + 1) * item_height if i < split_count - 1 else height
                cropped = pil_img.crop((0, top, width, bottom))
                output_path = f"{output_dir}/{model}.png"
                cropped.save(output_path)
                if model in product_lookup:
                    product_lookup[model]['image_path'] = output_path
                    print(f"    -> Saved part {i+1}: {model}.png")
    
    doc.close()
    
    # Return updated products list
    return [product_lookup[m] for m in [p['model'] for p in products]]


def export_to_excel(products, output_path="products.xlsx"):
    """Export matched products to Excel."""
    if not products:
        print("No products to export")
        return None
    
    df_data = []
    for p in products:
        df_data.append({
            '商品型号': p['model'],
            '起批量': p['quantity'],
            '币种': p['currency'],
            '价格': p['price'],
            '商品图片路径': p['image_path'],
            '所有图片': p.get('all_images', '')
        })
    
    df = pd.DataFrame(df_data)
    df.to_excel(output_path, index=False, engine='openpyxl')
    return df


def extract_catalog(pdf_path, output_excel="products.xlsx", output_images="product_images"):
    """Complete workflow to extract product catalog from PDF."""
    
    # Step 1: Ask for currency
    currency = ask_currency()
    
    # Step 2: Define products in PDF order
    # EDIT THIS LIST to match your PDF content
    # Format: (model, quantity, price, num_images)
    # num_images: 1 for single image, 2+ for combined images
    products_in_order = [
        # Example products - replace with your actual products
        ("PRODUCT_1", 1, 100, 1),
        ("PRODUCT_2", 1, 200, 1),
        ("PRODUCT_3", 2, 300, 3),  # Product with 3 images
        ("PRODUCT_4", 1, 150, 1),
        ("PRODUCT_5", 1, 250, 2),  # Product with 2 images
    ]
    
    print(f"\nDefined {len(products_in_order)} products")
    print("\nNote: Please edit the PRODUCTS_IN_ORDER list in the script")
    print("to match your actual PDF content for accurate extraction.")
    
    # Step 3: Extract and split images
    print("\n" + "="*60)
    print("Extracting and splitting images...")
    print("="*60)
    image_parts = extract_and_split_images(pdf_path, output_images)
    print(f"\nCreated {len(image_parts)} image parts")
    
    # Step 4: Match products with images
    print("\n" + "="*60)
    print("Matching products with images...")
    print("="*60)
    matched = match_products_sequentially(products_in_order, image_parts, currency)
    
    # Show results
    print()
    with_images = 0
    without_images = 0
    for p in matched:
        if p['image_path']:
            status = "✓"
            with_images += 1
        else:
            status = "✗"
            without_images += 1
        print(f"  {status} {p['model']:<20} | Qty: {p['quantity']:3d} | Price: {p['price']:6d} {p['currency']}")
    
    # Step 5: Export to Excel
    print("\n" + "="*60)
    print("Exporting to Excel...")
    print("="*60)
    export_to_excel(matched, output_excel)
    
    print(f"\n✅ Extraction complete!")
    print(f"   - Total products: {len(matched)}")
    print(f"   - With images: {with_images}")
    print(f"   - Without images: {without_images}")
    print(f"   - Image parts: {len(image_parts)}")
    print(f"   - Excel file: {output_excel}")
    print(f"   - Images folder: {output_images}")
    
    return matched


def main():
    parser = argparse.ArgumentParser(
        description="Extract products from PDF catalog using sequential matching",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
IMPORTANT:
  Before using this script, you MUST edit the PRODUCTS_IN_ORDER list
  in the script to match your actual PDF content.

Examples:
  python extract_products.py catalog.pdf
  python extract_products.py catalog.pdf --output products.xlsx --images-dir images
        """
    )
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("--output", "-o", default="products.xlsx",
                        help="Output Excel file (default: products.xlsx)")
    parser.add_argument("--images-dir", "-i", default="product_images",
                        help="Output directory for images (default: product_images)")
    
    args = parser.parse_args()
    
    try:
        extract_catalog(args.input, args.output, args.images_dir)
    
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
