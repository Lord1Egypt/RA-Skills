#!/usr/bin/env python3
"""
Batch OCR processing for folders of images.

Usage:
    python scripts/batch_ocr.py --input ./images/ --output ./results/
    python scripts/batch_ocr.py --input ./images/ --engine easyocr --preprocess phone
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from liaogong_ocr import OCREngine


def main():
    parser = argparse.ArgumentParser(description='Batch OCR processing')
    parser.add_argument('--input', '-i', required=True, help='Input folder with images')
    parser.add_argument('--output', '-o', required=True, help='Output folder for results')
    parser.add_argument('--engine', '-e', choices=['auto', 'easyocr', 'tesseract'], default='auto')
    parser.add_argument('--preprocess', '-p', choices=['phone'], default=None)
    parser.add_argument('--ext', default='.jpg,.png,.jpeg,.bmp,.tiff,.webp',
                        help='Image extensions (comma-separated, default: jpg,png,jpeg,bmp,tiff,webp)')
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    extensions = [e.strip() for e in args.ext.split(',')]

    if not input_dir.exists():
        print(f"Error: input folder not found: {input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Collect images
    images = []
    for ext in extensions:
        images.extend(input_dir.glob(f'*{ext}'))
        images.extend(input_dir.glob(f'*{ext.upper()}'))
    images = sorted(set(images))

    if not images:
        print(f"No images found in {input_dir} with extensions {extensions}")
        sys.exit(1)

    print(f"Found {len(images)} images")
    print(f"Engine: {args.engine}")
    if args.preprocess:
        print(f"Preprocessing: {args.preprocess}")
    print()

    engine = OCREngine()
    success = 0
    failed = 0

    for i, img_path in enumerate(images, 1):
        print(f"[{i}/{len(images)}] {img_path.name} ... ", end='', flush=True)

        try:
            result = engine.process(str(img_path), engine=args.engine, preprocess=args.preprocess)

            out_path = output_dir / f"{img_path.stem}.txt"
            out_path.write_text(result['text'], encoding='utf-8')

            text_preview = result['text'][:50].replace('\n', ' ')
            conf_str = f" conf={result['confidence']}" if result['confidence'] else ""
            print(f"OK{conf_str} | {text_preview}")
            success += 1

        except Exception as e:
            print(f"FAIL | {e}")
            failed += 1

    print(f"\nDone: {success} success, {failed} failed")
    print(f"Results in: {output_dir}")


if __name__ == '__main__':
    main()
