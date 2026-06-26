#!/usr/bin/env python3
import argparse
import qrcode
from qrcode.image.pil import PilImage

def generate_qr_png(content, output_path, box_size=10, border=4):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(content)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    print(f"✅ QR code saved to: {output_path}")
    print(f"   Content: {content}")
    print(f"   Size: {img.size[0]}x{img.size[1]} pixels")

def main():
    parser = argparse.ArgumentParser(description="Generate QR code as PNG image")
    parser.add_argument("content", help="Text/URL content to encode in QR code")
    parser.add_argument("output", help="Output PNG file path")
    parser.add_argument("--box-size", type=int, default=10, help="Box size in pixels (default: 10)")
    parser.add_argument("--border", type=int, default=4, help="Border size (default: 4)")
    args = parser.parse_args()
    
    generate_qr_png(args.content, args.output, args.box_size, args.border)

if __name__ == "__main__":
    main()
