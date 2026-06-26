#!/usr/bin/env python3
"""
Reproduce the 15-chain benchmark on an image.
Outputs extracted text for each chain, comparing accuracy.

Usage: python scripts/benchmark_chains.py --image phone_photo.jpg
"""

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from liaogong_ocr import CHAINS, CHAIN_BENCHMARKS, OCREngine


def main():
    parser = argparse.ArgumentParser(description='Benchmark preprocessing chains')
    parser.add_argument('--image', '-i', required=True, help='Test image path')
    parser.add_argument('--output', '-o', help='Output directory for results')
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        print(f"Error: {image_path} not found")
        sys.exit(1)

    print(f"{'='*70}")
    print(f"Benchmarking preprocessing chains on: {image_path.name}")
    print(f"{'='*70}\n")

    engine = OCREngine()

    results = []
    for name, chain_fn in CHAINS.items():
        print(f"[{name}] ", end='', flush=True)
        start = time.time()

        try:
            from PIL import Image
            img = Image.open(image_path)
            processed = chain_fn(img)

            # Use tesseract for benchmarking (consistent confidence comparison)
            result = engine.process_from_image(processed, engine='tesseract')
            elapsed = time.time() - start

            text_preview = result['text'][:60].replace('\n', ' ')
            benchmark = CHAIN_BENCHMARKS.get(name, {})
            known_acc = benchmark.get('digit_acc', '?')

            print(f"OK ({elapsed:.1f}s) | known_acc={known_acc} | text={text_preview}")

            results.append({
                'chain': name,
                'known_acc': known_acc,
                'time': elapsed,
                'text': result['text'],
            })

        except Exception as e:
            elapsed = time.time() - start
            print(f"FAIL ({elapsed:.1f}s) | {e}")

    # Summary
    print(f"\n{'='*70}")
    print(f"Summary (sorted by known accuracy)")
    print(f"{'='*70}")
    results.sort(key=lambda r: r['known_acc'] if isinstance(r['known_acc'], float) else 0, reverse=True)
    for r in results:
        acc_str = f"{r['known_acc']:.0%}" if isinstance(r['known_acc'], float) else str(r['known_acc'])
        text_preview = r['text'][:40].replace('\n', ' ')
        print(f"  {acc_str:>5} | {r['chain']:<25} | {text_preview}")

    # Save outputs if requested
    if args.output:
        out_dir = Path(args.output)
        out_dir.mkdir(parents=True, exist_ok=True)
        for r in results:
            fpath = out_dir / f"{r['chain']}.txt"
            fpath.write_text(r['text'], encoding='utf-8')
        print(f"\nResults saved to: {out_dir}")


if __name__ == '__main__':
    main()
