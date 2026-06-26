#!/usr/bin/env python3
"""hackrf-sdr analyze - Full IQ signal analysis with plots.

Usage: analyze.py <iq_file> [options]
  Options:
    --freq <Hz>       Center frequency (default: auto from filename or 3220000000)
    --rate <Hz>       Sample rate (default: 10000000)
    --bw <Hz>         Analysis bandwidth filter (default: 2000000)
    --nsamples <N>    Number of samples to analyze (default: 1000000)
    --outdir <dir>    Output directory (default: current dir)
    --noplot          Skip plot generation, text only
"""

import sys
import os
import argparse
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import signal as sci_signal
from collections import defaultdict


def load_iq(filename, max_samples=None):
    """Load IQ data from HackRF raw file (int8 interleaved I,Q)."""
    raw = np.fromfile(filename, dtype=np.int8)
    iq = raw[0::2].astype(np.float32) + 1j * raw[1::2].astype(np.float32)
    iq /= 128.0  # Normalize to [-1, 1]
    if max_samples and len(iq) > max_samples:
        iq = iq[:max_samples]
    return iq


def compute_psd(iq, fs, nperseg=65536, noverlap=None):
    """Compute PSD with Welch's method."""
    if noverlap is None:
        noverlap = nperseg // 2
    f, psd = sci_signal.welch(iq, fs=fs, nperseg=nperseg, noverlap=noverlap,
                               window='hann', return_onesided=False)
    f_shifted = np.fft.fftshift(f)
    psd_shifted = np.fft.fftshift(psd)
    psd_db = 10 * np.log10(psd_shifted + 1e-20)
    return f_shifted, psd_db


def find_peak(f_offset, psd_db, noise_mask, signal_bw=2e6):
    """Find peak signal frequency and measure SNR."""
    noise_floor = np.median(psd_db[noise_mask])
    signal_region = np.abs(f_offset) < signal_bw
    if not np.any(signal_region):
        signal_region = np.abs(f_offset) < 5e6
    peak_idx = np.argmax(psd_db[signal_region])
    peak_freq = f_offset[signal_region][peak_idx]
    peak_power = psd_db[signal_region][peak_idx]
    snr = peak_power - noise_floor
    return peak_freq, peak_power, noise_floor, snr


def measure_bandwidth(f_offset, psd_db, peak_freq, peak_power, threshold_db=3):
    """Measure signal bandwidth at given dB below peak."""
    threshold = peak_power - threshold_db
    above = psd_db > threshold
    if np.any(above):
        bw = np.sum(above) * abs(f_offset[1] - f_offset[0])
        return bw
    return 0


def classify_modulation(amplitude, phase_diff):
    """Classify modulation type from amplitude and phase statistics."""
    amp_mean = np.mean(amplitude)
    amp_std = np.std(amplitude)
    cv = amp_std / amp_mean if amp_mean > 0 else 0
    phase_std = np.std(phase_diff)
    phase_mean = np.mean(phase_diff)

    if cv < 0.05 and phase_std < 0.05:
        return "CW (Continuous Wave)", cv, phase_std
    elif cv < 0.05 and phase_std < 0.5:
        return "PSK (constant envelope, discrete phase)", cv, phase_std
    elif cv < 0.05 and phase_std >= 0.5:
        return "FM/FSK (constant envelope, continuous phase)", cv, phase_std
    elif cv < 0.15 and phase_std < 0.5:
        return "QAM (low amplitude variation, stable phase)", cv, phase_std
    elif cv < 0.15 and phase_std >= 0.5:
        return "QAM/PSK (moderate amplitude variation)", cv, phase_std
    elif cv >= 0.15 and phase_std < 0.1:
        return "AM (high amplitude variation, stable phase)", cv, phase_std
    else:
        return "Mixed/Unknown (high amplitude & phase variation)", cv, phase_std


def detect_pulsed(iq, chunk_size=100000):
    """Detect if signal is pulsed by measuring power variation over time."""
    n_chunks = len(iq) // chunk_size
    if n_chunks < 2:
        return False, 0.0
    powers = []
    for i in range(n_chunks):
        chunk = iq[i * chunk_size:(i + 1) * chunk_size]
        powers.append(np.mean(np.abs(chunk) ** 2))
    powers_db = 10 * np.log10(np.array(powers) + 1e-20)
    variation = np.max(powers_db) - np.min(powers_db)
    return variation > 6, variation


def analyze_signal(iq, fs, center_freq):
    """Full signal analysis."""
    chunk = iq[:min(len(iq), 1000000)]
    f_offset, psd_db = compute_psd(chunk, fs)

    # Noise mask: frequencies far from center
    noise_mask = np.abs(f_offset) > 4e6

    # Find peaks
    peak_offset, peak_power, noise_floor, snr = find_peak(
        f_offset, psd_db, noise_mask, signal_bw=5e6)
    peak_freq_hz = center_freq + peak_offset

    # Bandwidth
    bw_3db = measure_bandwidth(f_offset, psd_db, peak_offset, peak_power, 3)
    bw_10db = measure_bandwidth(f_offset, psd_db, peak_offset, peak_power, 10)

    # Shift to signal center
    shifted = chunk * np.exp(-1j * 2 * np.pi * peak_offset / fs * np.arange(len(chunk)))
    lpf = sci_signal.firwin(200, 2e6, fs=fs)
    shifted_filt = np.convolve(shifted, lpf, mode='same')

    analytic = shifted_filt[20000:120000]
    amplitude = np.abs(analytic)
    phase_unwrap = np.unwrap(np.angle(analytic))
    phase_diff = np.diff(phase_unwrap)

    mod_type, cv, phase_std = classify_modulation(amplitude, phase_diff)
    is_pulsed, power_var = detect_pulsed(iq)

    # Find additional peaks (2nd, 3rd signals)
    psd_masked = psd_db.copy()
    peak_mask = np.abs(f_offset - peak_offset) < 2e6
    psd_masked[peak_mask] = -200
    second_peak_offset = f_offset[np.argmax(psd_masked)]
    second_peak_power = np.max(psd_masked)
    second_snr = second_peak_power - noise_floor
    second_freq_hz = center_freq + second_peak_offset

    return {
        'center_freq': center_freq,
        'peak_freq': peak_freq_hz,
        'peak_offset': peak_offset,
        'peak_power': peak_power,
        'noise_floor': noise_floor,
        'snr': snr,
        'bw_3db': bw_3db,
        'bw_10db': bw_10db,
        'modulation': mod_type,
        'amplitude_cv': cv,
        'phase_std_deg': np.degrees(phase_std),
        'is_pulsed': is_pulsed,
        'power_variation_db': power_var,
        'second_peak_freq': second_freq_hz,
        'second_peak_snr': second_snr,
        'f_offset': f_offset,
        'psd_db': psd_db,
        'chunk': chunk,
        'shifted_filt': shifted_filt,
        'amplitude': amplitude,
        'phase_diff': phase_diff,
        'phase_unwrap': phase_unwrap,
        'fs': fs,
    }


def generate_plots(result, outdir):
    """Generate analysis plots."""
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, 'signal_analysis.png')

    center_mhz = result['center_freq'] / 1e6
    peak_mhz = result['peak_freq'] / 1e6
    freq_mhz = center_mhz + result['f_offset'] / 1e6

    fig, axes = plt.subplots(3, 2, figsize=(16, 14))
    fig.patch.set_facecolor('#1a1a2e')

    # 1. PSD
    ax = axes[0, 0]
    ax.plot(freq_mhz, result['psd_db'], color='#00ff88', linewidth=0.5, alpha=0.8)
    ax.axhline(y=result['noise_floor'], color='red', linestyle='--', alpha=0.5,
               label=f'Noise: {result["noise_floor"]:.1f} dB/Hz')
    ax.axvline(x=peak_mhz, color='cyan', linestyle='--', alpha=0.5,
               label=f'Peak: {peak_mhz:.2f} MHz')
    ax.set_xlabel('Frequency (MHz)', color='white')
    ax.set_ylabel('PSD (dB/Hz)', color='white')
    ax.set_title('Power Spectral Density', color='white', fontweight='bold')
    ax.legend(facecolor='#2a2a4e', edgecolor='gray', labelcolor='white', fontsize=8)
    ax.set_facecolor('#0a0a1a')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2, color='gray')

    # 2. Spectrogram
    ax = axes[0, 1]
    nfft = 4096
    f_spec, t_spec, Sxx = sci_signal.spectrogram(
        result['chunk'], fs=result['fs'], nperseg=nfft, noverlap=nfft // 2,
        window='hann', return_onesided=False, mode='complex')
    Sxx_db = 10 * np.log10(np.abs(Sxx) ** 2 + 1e-20)
    f_spec_mhz = center_mhz + np.fft.fftshift(f_spec) / 1e6
    Sxx_db_shifted = np.fft.fftshift(Sxx_db, axes=0)

    im = ax.pcolormesh(t_spec * 1000, f_spec_mhz, Sxx_db_shifted,
                       shading='gouraud', cmap='turbo',
                       vmin=np.percentile(Sxx_db_shifted, 5),
                       vmax=np.percentile(Sxx_db_shifted, 98))
    ax.set_xlabel('Time (ms)', color='white')
    ax.set_ylabel('Frequency (MHz)', color='white')
    ax.set_title('Spectrogram', color='white', fontweight='bold')
    ax.tick_params(colors='white')
    fig.colorbar(im, ax=ax, label='dB')

    # 3. IQ constellation
    ax = axes[1, 0]
    analytic = result['shifted_filt'][20000:120000]
    step = max(1, len(analytic) // 5000)
    ax.scatter(analytic[::step].real, analytic[::step].imag, s=1, alpha=0.3, c='#00d4ff')
    ax.set_xlabel('I', color='white')
    ax.set_ylabel('Q', color='white')
    ax.set_title(f'IQ Constellation @ {peak_mhz:.2f} MHz', color='white', fontweight='bold')
    ax.set_aspect('equal')
    ax.set_facecolor('#0a0a1a')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2, color='gray')

    # 4. Amplitude histogram
    ax = axes[1, 1]
    valid_amp = result['amplitude'][result['amplitude'] > 0]
    if len(valid_amp) > 0:
        ax.hist(valid_amp, bins=200, color='#00ff88', alpha=0.7, edgecolor='#006644')
        ax.axvline(np.mean(valid_amp), color='red', linestyle='--',
                    label=f'Mean: {np.mean(valid_amp):.4f}')
    ax.set_xlabel('Amplitude', color='white')
    ax.set_ylabel('Count', color='white')
    ax.set_title(f'Amplitude (CV={result["amplitude_cv"]:.4f})', color='white', fontweight='bold')
    ax.legend(facecolor='#2a2a4e', edgecolor='gray', labelcolor='white', fontsize=8)
    ax.set_facecolor('#0a0a1a')
    ax.tick_params(colors='white')

    # 5. Phase histogram
    ax = axes[2, 0]
    phase_diff_deg = np.degrees(result['phase_diff'])
    valid_phase = phase_diff_deg[np.isfinite(phase_diff_deg)]
    if len(valid_phase) > 0:
        ax.hist(valid_phase, bins=200, color='#ff6600', alpha=0.7, edgecolor='#993300')
        ax.axvline(np.mean(valid_phase), color='cyan', linestyle='--',
                    label=f'Mean: {np.mean(valid_phase):.2f} deg')
    ax.set_xlabel('Phase difference (degrees)', color='white')
    ax.set_ylabel('Count', color='white')
    ax.set_title(f'Phase Delta (std={result["phase_std_deg"]:.1f} deg)', color='white', fontweight='bold')
    ax.legend(facecolor='#2a2a4e', edgecolor='gray', labelcolor='white', fontsize=8)
    ax.set_facecolor('#0a0a1a')
    ax.tick_params(colors='white')

    # 6. Instantaneous frequency
    ax = axes[2, 1]
    inst_freq = np.diff(result['phase_unwrap']) * result['fs'] / (2 * np.pi)
    inst_freq_khz = inst_freq / 1e3
    t_axis = np.arange(min(len(inst_freq_khz), 10000)) / result['fs'] * 1000
    ax.plot(t_axis, inst_freq_khz[:len(t_axis)], color='#ff4444', linewidth=0.3, alpha=0.7)
    ax.set_xlabel('Time (ms)', color='white')
    ax.set_ylabel('Freq offset (kHz)', color='white')
    ax.set_title('Instantaneous Frequency', color='white', fontweight='bold')
    ax.set_facecolor('#0a0a1a')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2, color='gray')

    for row in axes:
        for ax in row:
            for spine in ax.spines.values():
                spine.set_color('gray')
            plt.setp(ax.xaxis.get_majorticklabels(), color='white')
            plt.setp(ax.yaxis.get_majorticklabels(), color='white')

    signal_type = "PULSED" if result['is_pulsed'] else "CONTINUOUS"
    plt.suptitle(
        f'Signal Analysis | {peak_mhz:.2f} MHz | BW={result["bw_3db"]/1e3:.0f} kHz | '
        f'SNR={result["snr"]:.1f} dB | {result["modulation"]} | {signal_type}',
        color='white', fontsize=13, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(outpath, dpi=150, facecolor=fig.get_facecolor())
    plt.close('all')
    return outpath


def main():
    parser = argparse.ArgumentParser(description='Analyze HackRF IQ capture')
    parser.add_argument('iq_file', help='IQ capture file (.raw)')
    parser.add_argument('--freq', type=float, default=None,
                        help='Center frequency in Hz (auto-detect from filename or default 3220 MHz)')
    parser.add_argument('--rate', type=float, default=10000000,
                        help='Sample rate in Hz (default: 10 MSPS)')
    parser.add_argument('--bw', type=float, default=2000000,
                        help='Analysis bandwidth filter in Hz (default: 2 MHz)')
    parser.add_argument('--nsamples', type=int, default=1000000,
                        help='Number of samples to analyze (default: 1M)')
    parser.add_argument('--outdir', default='.', help='Output directory')
    parser.add_argument('--noplot', action='store_true', help='Skip plot generation')
    args = parser.parse_args()

    # Auto-detect frequency from filename
    if args.freq is None:
        basename = os.path.basename(args.iq_file)
        match = re.search(r'(\d{4,})', basename)
        if match:
            args.freq = float(match.group(1)) * 1e6
        else:
            args.freq = 3220e6

    print(f"Loading IQ data: {args.iq_file}")
    iq = load_iq(args.iq_file, max_samples=args.nsamples)
    print(f"Loaded {len(iq)} samples ({len(iq)/args.rate:.2f}s at {args.rate/1e6:.1f} MSPS)")

    result = analyze_signal(iq, args.rate, args.freq)

    # Print report
    peak_mhz = result['peak_freq'] / 1e6
    center_mhz = result['center_freq'] / 1e6
    second_mhz = result['second_peak_freq'] / 1e6

    print("\n" + "=" * 60)
    print("SIGNAL ANALYSIS REPORT")
    print("=" * 60)
    print(f"  Center frequency:   {center_mhz:.3f} MHz")
    print(f"  Peak frequency:     {peak_mhz:.3f} MHz")
    print(f"  Peak offset:        {result['peak_offset']/1e6:+.3f} MHz from center")
    print(f"  Peak power:         {result['peak_power']:.1f} dB/Hz")
    print(f"  Noise floor:        {result['noise_floor']:.1f} dB/Hz")
    print(f"  SNR:                {result['snr']:.1f} dB")
    print(f"  3dB bandwidth:     {result['bw_3db']/1e3:.0f} kHz")
    print(f"  10dB bandwidth:    {result['bw_10db']/1e3:.0f} kHz")
    print(f"  Modulation:         {result['modulation']}")
    print(f"  Amplitude CV:       {result['amplitude_cv']:.4f}")
    print(f"  Phase std:          {result['phase_std_deg']:.1f} deg")
    print(f"  Signal type:        {'PULSED' if result['is_pulsed'] else 'CONTINUOUS'}")
    print(f"  Power variation:    {result['power_variation_db']:.1f} dB")
    print(f"  2nd peak:           {second_mhz:.3f} MHz (SNR {result['second_peak_snr']:.1f} dB)")
    print("=" * 60)

    if not args.noplot:
        outpath = generate_plots(result, args.outdir)
        print(f"\nPlot saved: {outpath}")

    return result


if __name__ == '__main__':
    main()