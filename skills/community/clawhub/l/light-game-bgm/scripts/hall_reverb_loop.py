#!/usr/bin/env python3
"""
Concert-hall convolution reverb + (optional) seamless-loop tail wrap.

Why convolution: a synthesised hall impulse response (early reflections +
diffuse, HF-damped, L/R-decorrelated tail) convolved with the dry render
gives a real "performed in a hall" space — far more convincing than an
`aecho`/delay.  Render the dry stems with reverb OFF (fluidsynth -R 0 -C 0)
so this stage has full control.

Why the tail wrap: a game-BGM loop must repeat with no click and no fade.
The trick is to fold everything past the loop point (note releases + the
reverb tail) back onto the START, simulating "the previous iteration's
sound spilling into this one".  The seam then has no discontinuity.

Usage:
  python hall_reverb_loop.py --input dry.wav --output loop.wav \
      --bpm 110 --beats 128 --wet 0.34 --decay 2.1 --x2

  --beats     total beats in the loop body (bars * beats_per_bar).
              Omit (or 0) to skip looping and just add reverb.
  --decay     hall RT60-ish seconds (room ~1.2, hall ~2.1, cathedral ~3.5).
  --x2        also write <output>_x2.wav (two loops) to audition the seam.
"""
import argparse
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve

SR = 44100


def hall_ir(decay=2.1, length=None, predelay=0.022, damping=0.30, seed=3):
    rng = np.random.default_rng(seed)
    length = length or (decay + 0.5)
    n = int(length * SR)
    t = np.arange(n) / SR

    def one():
        env = np.exp(-t * (6.9 / decay))            # ~ -60 dB at `decay`s
        tail = rng.standard_normal(n) * env
        b = np.empty_like(tail)
        a = 0.0
        for i in range(n):                          # one-pole LP = HF absorption
            a += damping * (tail[i] - a)
            b[i] = a
        return b

    L, R = one(), one()
    for ch in (L, R):                               # discrete early reflections
        for ms, g in [(11, .5), (19, .42), (27, .33), (37, .27), (45, .22), (58, .16)]:
            idx = int(ms / 1000 * SR)
            if idx < n:
                ch[idx] += g * (1 if rng.random() > .5 else -1)
    pre = int(predelay * SR)
    L = np.concatenate([np.zeros(pre), L])
    R = np.concatenate([np.zeros(pre), R])
    m = max(np.abs(L).max(), np.abs(R).max())
    return L / m, R / m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--bpm', type=float, default=110)
    ap.add_argument('--beats', type=float, default=0, help='loop length in beats; 0 = no loop')
    ap.add_argument('--wet', type=float, default=0.34)
    ap.add_argument('--dry', type=float, default=0.82)
    ap.add_argument('--decay', type=float, default=2.1)
    ap.add_argument('--x2', action='store_true')
    a = ap.parse_args()

    sr, dry = wavfile.read(a.input)
    dry = dry.astype(np.float64) / 32768.0
    if dry.ndim == 1:
        dry = np.stack([dry, dry], 1)

    IRl, IRr = hall_ir(decay=a.decay)
    loop_n = int(round(a.beats * 60 / a.bpm * SR)) if a.beats else 0
    if loop_n:
        need = loop_n + len(IRl) + SR
        if len(dry) < need:
            dry = np.vstack([dry, np.zeros((need - len(dry), 2))])

    wetL = fftconvolve(dry[:, 0], IRl)[:len(dry)]
    wetR = fftconvolve(dry[:, 1], IRr)[:len(dry)]
    wet = np.stack([wetL, wetR], 1)
    wet *= 0.9 / (np.abs(wet).max() + 1e-9)
    mix = dry * a.dry + wet * a.wet

    if loop_n:
        out = mix[:loop_n].copy()
        tail = mix[loop_n:]
        tl = min(len(tail), loop_n)
        out[:tl] += tail[:tl]                        # <-- seamless wrap
    else:
        out = mix

    out = np.tanh(out * 1.05)
    out *= 0.97 / (np.abs(out).max() + 1e-9)
    wavfile.write(a.output, SR, (out * 32767).astype(np.int16))
    print(f'wrote {a.output}  ({len(out)/SR:.2f}s)'
          + (f'  loop body={loop_n/SR:.2f}s' if loop_n else '  (no loop)'))

    if a.x2 and loop_n:
        two = np.vstack([out, out])
        x2 = a.output.rsplit('.', 1)[0] + '_x2.wav'
        wavfile.write(x2, SR, (two * 32767).astype(np.int16))
        print(f'wrote {x2}  ({len(two)/SR:.2f}s, audition the seam at {loop_n/SR:.2f}s)')


if __name__ == '__main__':
    main()
