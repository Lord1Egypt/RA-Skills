#!/usr/bin/env python3
"""
Split segments.json into batches for parallel translation.
Each batch is saved as batch_N.json (JSON array of strings).

Usage:
  python3 split_segments.py <segments.json> <output_dir> [--batch-size 260]
"""

import json
import os
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print(f"Usage: python3 {sys.argv[0]} <segments.json> <output_dir> [--batch-size N]")
        sys.exit(1)

    segments_file = sys.argv[1]
    output_dir = sys.argv[2]
    batch_size = 260

    if "--batch-size" in sys.argv:
        idx = sys.argv.index("--batch-size")
        if idx + 1 < len(sys.argv):
            batch_size = int(sys.argv[idx + 1])

    # Load segments
    with open(segments_file) as f:
        data = json.load(f)

    # Extract unique text segments (exclude JSON batch format and system prompts)
    text_segments = []
    seen = set()
    for key in data.keys():
        key = key.strip()
        # Skip JSON batch format
        if key.startswith('[') and '"input"' in key:
            continue
        # Skip system prompts
        if key.startswith('You are a professional'):
            continue
        if key not in seen:
            seen.add(key)
            text_segments.append(key)

    total = len(text_segments)
    num_batches = (total + batch_size - 1) // batch_size

    print(f"Total unique text segments: {total}")
    print(f"Batch size: {batch_size}")
    print(f"Number of batches: {num_batches}")
    print(f"Output directory: {output_dir}")
    print()

    os.makedirs(output_dir, exist_ok=True)

    for i in range(num_batches):
        start = i * batch_size
        end = min((i + 1) * batch_size, total)
        batch = text_segments[start:end]

        batch_file = os.path.join(output_dir, f"batch_{i + 1}.json")
        with open(batch_file, 'w') as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)

        print(f"  Batch {i + 1}: segments {start + 1}-{end} ({end - start} segments) -> {batch_file}")

    print(f"\nDone! {num_batches} batch files created.")
    print(f"Translate each batch and save as translations_batch_N.json")
    print(f"Then merge all batches into translations.json")


if __name__ == "__main__":
    main()
