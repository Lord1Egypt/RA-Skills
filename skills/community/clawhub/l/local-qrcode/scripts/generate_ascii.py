#!/usr/bin/env python3
import argparse
import qrcode

def generate_qr_ascii(content):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=1,
        border=2,
    )
    qr.add_data(content)
    qr.make(fit=True)
    
    # Print ASCII QR code
    qr.print_ascii()
    print(f"\n✅ QR content: {content}")

def main():
    parser = argparse.ArgumentParser(description="Generate QR code as ASCII art for terminal")
    parser.add_argument("content", help="Text/URL content to encode in QR code")
    args = parser.parse_args()
    
    generate_qr_ascii(args.content)

if __name__ == "__main__":
    main()
