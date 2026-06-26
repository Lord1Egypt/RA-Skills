#!/usr/bin/env python3
"""
Parse hackrf_sweep CSV output and report peaks.
Usage: python3 parse_sweep.py sweep.csv [--threshold 10]
"""
import sys
import numpy as np
from collections import defaultdict

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csv', help='hackrf_sweep CSV file')
    parser.add_argument('--threshold', type=float, default=10.0,
                        help='SNR threshold in dB above noise floor (default 10)')
    args = parser.parse_args()

    freqs = defaultdict(list)
    with open(args.csv) as f:
        for line in f:
            parts = line.strip().split(', ')
            if len(parts) < 7:
                continue
            try:
                f_start = float(parts[2])
                step    = float(parts[4])
                vals    = [float(x) for x in parts[6:]]
                for i, v in enumerate(vals):
                    freq = f_start + step * i
                    freqs[round(freq / 25000) * 25000].append(v)
            except:
                pass

    avg = {f: np.mean(v) for f, v in freqs.items()}
    noise = np.percentile(list(avg.values()), 15)
    print(f"Noise floor: {noise:.1f} dBm")
    print(f"\nPeaks >{args.threshold:.0f} dB above noise:")
    notable = sorted([(f, v) for f, v in avg.items()
                      if v > noise + args.threshold], key=lambda x: x[0])
    if not notable:
        print("  (none)")
    for f, v in notable:
        print(f"  {f/1e6:.4f} MHz  {v:+.1f} dBm  SNR={v-noise:.1f} dB")

if __name__ == '__main__':
    main()
