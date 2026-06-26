#!/usr/bin/env python3
"""hackrf-sdr demod - Demodulate IQ capture (FM, AM, SSB).

Usage: demod.py <iq_file> --mode <fm|am|usb|lsb> [options]
  Options:
    --freq <Hz>       Center frequency (default: from filename or 3220 MHz)
    --rate <Hz>       Sample rate (default: 10 MSPS)
    --offset <Hz>     Signal offset from center (default: 0)
    --bw <Hz>         Demodulation bandwidth (default: auto)
    --out <file>      Output WAV file (default: /tmp/demod_out.wav)
    --duration <sec>  Output duration in seconds (default: all)
"""

import sys
import os
import argparse
import re
import numpy as np
from scipy import signal as sci_signal

try:
    import soundfile as sf
    HAS_SOUNDFILE = True
except ImportError:
    HAS_SOUNDFILE = False


def load_iq(filename, max_samples=None):
    """Load IQ data from HackRF raw file (int8 interleaved I,Q)."""
    raw = np.fromfile(filename, dtype=np.int8)
    iq = raw[0::2].astype(np.float32) + 1j * raw[1::2].astype(np.float32)
    iq /= 128.0
    if max_samples and len(iq) > max_samples:
        iq = iq[:max_samples]
    return iq


def demod_fm(iq, fs, freq_offset=0, deemph=50e-6):
    """FM demodulation."""
    t = np.arange(len(iq))
    shifted = iq * np.exp(-1j * 2 * np.pi * freq_offset / fs * t)

    # FM demod: phase difference
    phase = np.unwrap(np.angle(shifted))
    demod = np.diff(phase) * fs / (2 * np.pi)
    demod = np.concatenate([[0], demod])

    # De-emphasis filter
    if deemph > 0:
        alpha = 1.0 - np.exp(-1.0 / (fs * deemph))
        b = [alpha]
        a = [1, -(1 - alpha)]
        demod = sci_signal.lfilter(b, a, demod)

    return demod


def demod_am(iq, fs, freq_offset=0):
    """AM demodulation (envelope detector)."""
    t = np.arange(len(iq))
    shifted = iq * np.exp(-1j * 2 * np.pi * freq_offset / fs * t)

    # AM demod: envelope
    demod = np.abs(shifted)
    # Remove DC
    demod = demod - np.mean(demod)
    return demod


def demod_ssb(iq, fs, freq_offset=0, side='usb'):
    """SSB demodulation (USB or LSB)."""
    t = np.arange(len(iq))
    shifted = iq * np.exp(-1j * 2 * np.pi * freq_offset / fs * t)

    if side == 'lsb':
        freq_offset_neg = -freq_offset
        shifted = iq * np.exp(-1j * 2 * np.pi * freq_offset_neg / fs * t)

    demod = np.real(shifted)
    return demod


def main():
    parser = argparse.ArgumentParser(description='Demodulate HackRF IQ capture')
    parser.add_argument('iq_file', help='IQ capture file (.raw)')
    parser.add_argument('--mode', required=True, choices=['fm', 'am', 'usb', 'lsb'],
                        help='Demodulation mode')
    parser.add_argument('--freq', type=float, default=None, help='Center frequency Hz')
    parser.add_argument('--rate', type=float, default=10000000, help='Sample rate Hz')
    parser.add_argument('--offset', type=float, default=0, help='Signal offset from center Hz')
    parser.add_argument('--bw', type=float, default=None, help='Demod bandwidth Hz (auto)')
    parser.add_argument('--out', default='/tmp/demod_out.wav', help='Output WAV file')
    parser.add_argument('--duration', type=float, default=None, help='Output duration seconds')
    args = parser.parse_args()

    if args.freq is None:
        match = re.search(r'(\d{4,})', os.path.basename(args.iq_file))
        if match:
            args.freq = float(match.group(1)) * 1e6
        else:
            args.freq = 3220e6

    # Default bandwidths by mode
    bw_defaults = {'fm': 200000, 'am': 10000, 'usb': 3000, 'lsb': 3000}
    bw = args.bw or bw_defaults.get(args.mode, 100000)

    print(f"Loading IQ: {args.iq_file}")
    max_samples = int(args.duration * args.rate) if args.duration else None
    iq = load_iq(args.iq_file, max_samples=max_samples)
    print(f"Loaded {len(iq)} samples ({len(iq)/args.rate:.2f}s)")

    # Demodulate
    if args.mode == 'fm':
        print(f"FM demodulating (offset={args.offset} Hz, bw={bw} Hz)...")
        demod = demod_fm(iq, args.rate, freq_offset=args.offset)
    elif args.mode == 'am':
        print(f"AM demodulating (offset={args.offset} Hz, bw={bw} Hz)...")
        demod = demod_am(iq, args.rate, freq_offset=args.offset)
    elif args.mode in ('usb', 'lsb'):
        print(f"{args.mode.upper()} demodulating (offset={args.offset} Hz)...")
        demod = demod_ssb(iq, args.rate, freq_offset=args.offset, side=args.mode)

    # Low-pass filter to audio bandwidth
    audio_bw = min(bw, args.rate / 2)
    lpf = sci_signal.firwin(200, audio_bw, fs=args.rate)
    demod = sci_signal.lfilter(lpf, [1.0], demod)

    # Resample to audio rate
    audio_rate = 48000
    if args.rate != audio_rate:
        from scipy.signal import resample
        num_out = int(len(demod) * audio_rate / args.rate)
        demod = resample(demod, num_out)

    # Normalize
    demod = demod / (np.max(np.abs(demod)) + 1e-10) * 0.9

    # Save
    print(f"Saving to {args.out}...")
    if HAS_SOUNDFILE:
        sf.write(args.out, demod, audio_rate)
    else:
        import wave
        with wave.open(args.out, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(audio_rate)
            pcm = (demod * 32767).astype(np.int16)
            wf.writeframes(pcm.tobytes())

    duration = len(demod) / audio_rate
    print(f"Done: {args.out} ({duration:.2f}s at {audio_rate} Hz)")


if __name__ == '__main__':
    main()