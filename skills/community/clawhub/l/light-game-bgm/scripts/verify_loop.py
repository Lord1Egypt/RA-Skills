#!/usr/bin/env python3
"""
Objectively verify a seamless loop before shipping it.

Checks the loop seam is continuous (no click) and the master isn't
clipping.  Run on the *_x2.wav (two concatenated loops) so the seam at
`beats` is a real internal boundary.

  python verify_loop.py --input loop_x2.wav --bpm 110 --beats 128

A seam is inaudible if the jump is small relative to the local RMS
(ratio < ~0.06) OR the absolute jump is tiny (< 0.01 ≈ -40 dBFS) — the
latter matters when the seam falls on a quiet/sparse moment where the
ratio looks large but you genuinely can't hear it.  clipped==0 means no
overs.
"""
import argparse
import numpy as np
from scipy.io import wavfile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--bpm', type=float, default=110)
    ap.add_argument('--beats', type=float, required=True)
    a = ap.parse_args()

    sr, x = wavfile.read(a.input)
    x = x.astype(np.float64) / 32768.0
    if x.ndim == 1:
        x = x[:, None]
    n = int(round(a.beats * 60 / a.bpm * sr))

    jump = float(np.abs(x[n] - x[n - 1]).max())
    w = int(0.02 * sr)
    rms = float(np.sqrt((x[n - w:n + w] ** 2).mean()))
    ratio = jump / (rms + 1e-9)
    peak = float(np.abs(x).max())
    clipped = int((np.abs(x) >= 0.999).sum())

    db = 20 * np.log10(ratio + 1e-9)
    inaudible = ratio < 0.06 or jump < 0.01
    print(f'seam index      : {n}')
    print(f'seam jump       : {jump:.4f}  ({20*np.log10(jump+1e-9):.1f} dBFS)')
    print(f'local rms       : {rms:.4f}')
    print(f'jump/rms        : {ratio:.4f}  ({db:.1f} dB)  '
          + ('OK (inaudible)' if inaudible else 'AUDIBLE — investigate'))
    print(f'peak            : {peak:.3f}  ' + ('OK' if peak < 1.0 else 'CLIPPING'))
    print(f'clipped samples : {clipped}')


if __name__ == '__main__':
    main()
