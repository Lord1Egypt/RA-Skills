#!/usr/bin/env python3
"""hackrf-sdr waterfall - Generate waterfall + spectrum plot.

Two modes:
  1. IQ mode (default): Capture IQ samples via hackrf_transfer, compute
     high-resolution spectrogram with FFT. ~5 kHz resolution, no artifacts.
  2. Sweep mode (--mode sweep): Use hackrf_sweep for quick low-res previews.

Usage:
  waterfall.py --start 420 --end 440                    # IQ mode (default)
  waterfall.py --start 420 --end 440 --mode sweep        # Sweep mode
  waterfall.py --input capture.raw --freq 430e6 --rate 20e6  # From file
"""

import sys
import os
import argparse
import subprocess

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# ─── IQ spectrogram ───────────────────────────────────────────────────────────

def generate_iq_waterfall(iq_file, center_freq, sample_rate, outdir,
                          title_suffix="", fft_size=4096, avg_factor=50,
                          max_time_rows=300):
    """Generate waterfall from IQ capture file."""
    raw = np.fromfile(iq_file, dtype=np.int8)
    iq = raw.reshape(-1, 2)
    I = iq[:, 0].astype(np.float32) / 127.0
    Q = iq[:, 1].astype(np.float32) / 127.0
    complex_sig = I + 1j * Q

    n_samples = len(complex_sig)
    n_ffts = n_samples // fft_size
    if n_ffts < avg_factor * 2:
        print(f"ERROR: Not enough samples (need >= {fft_size * avg_factor * 2}, got {n_samples})")
        return None

    window = np.hanning(fft_size)
    freq_axis = np.fft.fftshift(np.fft.fftfreq(fft_size, 1.0 / sample_rate)) + center_freq
    freq_mhz = freq_axis / 1e6
    freq_res_khz = (freq_mhz[1] - freq_mhz[0]) * 1000

    # Compute spectrogram with averaging
    n_rows = n_ffts // avg_factor
    row_step = max(1, n_rows // max_time_rows)
    effective_avg = avg_factor * row_step

    spectrogram = np.empty((n_rows, fft_size), dtype=np.float32)
    for row in range(n_rows):
        acc = np.zeros(fft_size, dtype=np.float64)
        for j in range(avg_factor):
            idx = row * avg_factor + j
            chunk = complex_sig[idx * fft_size : (idx + 1) * fft_size]
            spectrum = np.fft.fftshift(np.fft.fft(chunk * window))
            acc += np.abs(spectrum) ** 2
        acc /= avg_factor
        spectrogram[row] = 10.0 * np.log10(acc / fft_size + 1e-12)

    # Downsample
    wf = spectrogram[::row_step]
    time_sec = np.arange(wf.shape[0]) * effective_avg * fft_size / sample_rate

    # Mark DC spike (center freq ±50 kHz) for color scale computation
    dc_center_mhz = center_freq / 1e6
    dc_mask = np.abs(freq_mhz - dc_center_mhz) < 0.05

    # Compute noise floor from non-DC data so DC doesn't skew it
    non_dc_wf = wf.copy()
    non_dc_wf[:, dc_mask] = np.nan
    noise_floor = np.nanmedian(non_dc_wf)
    avg_spectrum = np.nanmean(wf, axis=0)  # full spectrum including DC
    avg_spectrum_nodc = np.nanmean(non_dc_wf, axis=0)  # for signal detection

    # Signal detection (exclude DC from auto-detect)
    threshold = noise_floor + 5
    signal_mask = avg_spectrum_nodc > threshold
    signal_mask &= ~dc_mask

    groups = []
    if np.any(signal_mask):
        indices = np.where(signal_mask)[0]
        current_group = [indices[0]]
        for i in indices[1:]:
            if i - current_group[-1] <= 10:
                current_group.append(i)
            else:
                groups.append(current_group)
                current_group = [i]
        groups.append(current_group)

    # Report
    peak_idx = np.nanargmax(avg_spectrum)
    print("\n" + "=" * 55)
    print("  WATERFALL SCAN REPORT (IQ mode)")
    print("=" * 55)
    print(f"  Center freq:      {center_freq/1e6:.1f} MHz")
    print(f"  Sample rate:      {sample_rate/1e6:.1f} MSPS")
    print(f"  FFT size:         {fft_size} ({freq_res_khz:.1f} kHz res)")
    print(f"  Avg factor:       {effective_avg} ({effective_avg * fft_size / sample_rate * 1000:.1f} ms/row)")
    print(f"  Duration:         {n_samples/sample_rate:.2f} s")
    print(f"  Noise floor:      {noise_floor:.1f} dB")
    print(f"  Peak frequency:   {freq_mhz[peak_idx]:.3f} MHz ({avg_spectrum[peak_idx]:.1f} dB)")
    print(f"  SNR:              {avg_spectrum[peak_idx]-noise_floor:+.1f} dB")
    print(f"  Signals found:    {len(groups)}")
    for i, g in enumerate(groups):
        g_freqs = freq_mhz[g]
        peak_j = g[np.argmax(avg_spectrum[g])]
        bw_khz = (max(g_freqs) - min(g_freqs)) * 1000
        if len(g) > 1:
            bw_khz += freq_res_khz
        print(f"    Signal {i+1}: {min(g_freqs):.3f}-{max(g_freqs):.3f} MHz "
              f"(center {(min(g_freqs)+max(g_freqs))/2:.3f}, "
              f"BW ~{bw_khz:.0f} kHz, peak {avg_spectrum[peak_j]:.1f} dB, "
              f"SNR {avg_spectrum[peak_j]-noise_floor:+.1f} dB)")
    print("=" * 55)

    outpath = os.path.join(outdir, 'waterfall.png')

    # Color scale: noise floor -> deep blue, signals -> yellow/red
    vmin = noise_floor
    vmax = noise_floor + 20
    spec_max = max(avg_spectrum.max(), noise_floor + 30)

    # FIGURE: use fig.add_axes with same left/right for perfect alignment
    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('#0a0a1a')

    # All three: spectrum, waterfall, colorbar - same left/right = perfect alignment
    L, R = 0.07, 0.97
    ax_spec = fig.add_axes([L, 0.62, R - L, 0.32])
    ax_wf   = fig.add_axes([L, 0.16, R - L, 0.43], sharex=ax_spec)
    cax     = fig.add_axes([L, 0.07, R - L, 0.04])  # horizontal colorbar

    # Spectrum
    ax_spec.fill_between(freq_mhz, avg_spectrum, noise_floor - 10, alpha=0.6, color='#00d4ff')
    ax_spec.plot(freq_mhz, avg_spectrum, color='#00ff88', linewidth=0.8)
    ax_spec.axhline(y=noise_floor, color='red', linestyle=':', alpha=0.5,
                     label=f'Noise: {noise_floor:.1f} dB')
    ax_spec.axhline(y=threshold, color='orange', linestyle=':', alpha=0.5,
                     label=f'Threshold: {threshold:.1f} dB')
    ax_spec.axvline(x=dc_center_mhz, color='magenta', linestyle=':', alpha=0.4,
                     label=f'DC @ {dc_center_mhz:.1f} MHz')
    for g in groups:
        peak_j = g[np.argmax(avg_spectrum[g])]
        ax_spec.annotate(
            f'{freq_mhz[peak_j]:.2f}\n{avg_spectrum[peak_j]:.1f}dB',
            xy=(freq_mhz[peak_j], avg_spectrum[peak_j]),
            xytext=(freq_mhz[peak_j] + 0.3, avg_spectrum[peak_j] + 3),
            fontsize=7, color='yellow', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='yellow', lw=1))
    ax_spec.set_ylabel('Power (dB)', color='white', fontsize=11)
    ax_spec.set_title(f'Spectrum + Waterfall {title_suffix}', color='white',
                       fontsize=14, fontweight='bold')
    ax_spec.legend(facecolor='#2a2a4e', edgecolor='gray', labelcolor='white',
                    fontsize=8)
    ax_spec.set_facecolor('#0a0a1a')
    ax_spec.tick_params(colors='white', labelbottom=False)
    ax_spec.grid(True, alpha=0.3, color='gray')
    ax_spec.set_ylim(noise_floor - 10, spec_max)
    ax_spec.set_xlim(freq_mhz[0], freq_mhz[-1])

    # Waterfall
    wf_plot = np.clip(wf, vmin, vmax)
    im = ax_wf.imshow(wf_plot, aspect='auto', origin='lower',
                       extent=[freq_mhz[0], freq_mhz[-1], 0, time_sec[-1]],
                       cmap='turbo', vmin=vmin, vmax=vmax,
                       interpolation='nearest')
    for g in groups:
        center = (freq_mhz[g[0]] + freq_mhz[g[-1]]) / 2
        ax_wf.axvline(x=center, color='white', linestyle='--', alpha=0.5, lw=1)
    ax_wf.axvline(x=dc_center_mhz, color='magenta', linestyle=':', alpha=0.4, lw=1)
    ax_wf.set_xlabel('Frequency (MHz)', color='white', fontsize=12)
    ax_wf.set_ylabel('Time (s)', color='white', fontsize=12)
    ax_wf.tick_params(colors='white')
    ax_wf.set_facecolor('#0a0a1a')

    # Horizontal colorbar
    cbar = fig.colorbar(im, cax=cax, orientation='horizontal')
    cbar.set_label('Power (dB)', color='white')
    cbar.ax.xaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.xaxis.get_majorticklabels(), color='white')

    for ax in [ax_spec, ax_wf]:
        for spine in ax.spines.values():
            spine.set_color('gray')
        plt.setp(ax.xaxis.get_majorticklabels(), color='white')
        plt.setp(ax.yaxis.get_majorticklabels(), color='white')

    fig.savefig(outpath, dpi=150, facecolor='#0a0a1a')
    plt.close('all')
    print(f"\nPlot saved: {outpath}")
    return outpath


# ─── Sweep mode ────────────────────────────────────────────────────────────────

def parse_sweep_data(data_text):
    """Parse hackrf_sweep CSV output with actual sub-bin count."""
    time_bins = {}
    all_freqs = set()
    times = []
    for line in data_text.strip().split('\n'):
        line = line.strip()
        if not line or not line.startswith('2'):
            continue
        parts = line.split(', ')
        if len(parts) < 7:
            continue
        try:
            timestamp = parts[0] + ' ' + parts[1]
            low_hz = int(parts[2])
            high_hz = int(parts[3])
            db_values = [float(x) for x in parts[6:]]
            if not db_values:
                continue
            actual_bin_hz = (high_hz - low_hz) / len(db_values)
            if timestamp not in time_bins:
                times.append(timestamp)
                time_bins[timestamp] = {}
            for i, db in enumerate(db_values):
                freq = low_hz + int((i + 0.5) * actual_bin_hz)
                time_bins[timestamp][freq] = db
                all_freqs.add(freq)
        except (ValueError, IndexError):
            continue
    return time_bins, all_freqs, times


def generate_sweep_waterfall(time_bins, all_freqs, times, outdir,
                              title_suffix=""):
    """Generate waterfall from sweep data (low-res, quick preview)."""
    sorted_freqs = sorted(all_freqs)
    freqs_mhz = np.array([f / 1e6 for f in sorted_freqs])

    waterfall = []
    for t in times:
        row = [time_bins[t].get(f, np.nan) for f in sorted_freqs]
        waterfall.append(row)
    waterfall = np.array(waterfall, dtype=float)

    for row_idx in range(waterfall.shape[0]):
        row = waterfall[row_idx]
        nans = np.isnan(row)
        if nans.any() and not nans.all():
            valid = ~nans
            row[nans] = np.interp(np.where(nans)[0], np.where(valid)[0], row[valid])

    noise_floor = np.median(waterfall)
    avg_spectrum = np.mean(waterfall, axis=0)
    peak_idx = np.argmax(avg_spectrum)

    threshold = noise_floor + 5
    signal_mask = avg_spectrum > threshold
    groups = []
    if np.any(signal_mask):
        indices = np.where(signal_mask)[0]
        current_group = [indices[0]]
        for i in indices[1:]:
            if i - current_group[-1] <= 2:
                current_group.append(i)
            else:
                groups.append(current_group)
                current_group = [i]
        groups.append(current_group)

    vmin = noise_floor
    vmax = noise_floor + 20

    fig = plt.figure(figsize=(16, 10))
    fig.patch.set_facecolor('#0a0a1a')

    L, R = 0.07, 0.97
    ax_spec = fig.add_axes([L, 0.62, R - L, 0.32])
    ax_wf   = fig.add_axes([L, 0.16, R - L, 0.43], sharex=ax_spec)
    cax     = fig.add_axes([L, 0.07, R - L, 0.04])

    spec_max = noise_floor + 30
    ax_spec.fill_between(freqs_mhz, np.clip(avg_spectrum, None, spec_max),
                          noise_floor - 10, alpha=0.6, color='#00d4ff')
    ax_spec.plot(freqs_mhz, np.clip(avg_spectrum, None, spec_max),
                 color='#00ff88', linewidth=1)
    ax_spec.axhline(y=noise_floor, color='red', linestyle=':', alpha=0.5,
                     label=f'Noise: {noise_floor:.1f} dB')
    ax_spec.axhline(y=threshold, color='orange', linestyle=':', alpha=0.5,
                     label=f'Threshold: {threshold:.1f} dB')
    for g in groups:
        peak_g_idx = g[np.argmax(avg_spectrum[g])]
        ax_spec.annotate(
            f'{freqs_mhz[peak_g_idx]:.1f}\n{avg_spectrum[peak_g_idx]:.1f} dB',
            xy=(freqs_mhz[peak_g_idx], avg_spectrum[peak_g_idx]),
            xytext=(freqs_mhz[peak_g_idx] + (freqs_mhz[1] - freqs_mhz[0]) * 3,
                    avg_spectrum[peak_g_idx] + 1.5),
            fontsize=7, color='yellow', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='yellow', lw=1))
    ax_spec.set_ylabel('Power (dB)', color='white', fontsize=11)
    ax_spec.set_title(f'Spectrum + Waterfall {title_suffix}', color='white',
                       fontsize=14, fontweight='bold')
    ax_spec.legend(facecolor='#2a2a4e', edgecolor='gray', labelcolor='white',
                    fontsize=8)
    ax_spec.set_facecolor('#0a0a1a')
    ax_spec.tick_params(colors='white', labelbottom=False)
    ax_spec.grid(True, alpha=0.3, color='gray')
    ax_spec.set_ylim(noise_floor - 10, spec_max)

    im = ax_wf.imshow(waterfall, aspect='auto', origin='lower',
                       extent=[freqs_mhz[0], freqs_mhz[-1], 0, len(times)],
                       cmap='turbo', vmin=vmin, vmax=vmax,
                       interpolation='nearest')
    for g in groups:
        g_freqs = freqs_mhz[g]
        center = (min(g_freqs) + max(g_freqs)) / 2
        ax_wf.axvline(x=center, color='white', linestyle='--', alpha=0.5, lw=1)
    ax_wf.set_xlabel('Frequency (MHz)', color='white', fontsize=12)
    ax_wf.set_ylabel('Time (sweep #)', color='white', fontsize=12)
    ax_wf.tick_params(colors='white')

    cbar = fig.colorbar(im, cax=cax, orientation='horizontal')
    cbar.set_label('Power (dB)', color='white')
    cbar.ax.xaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.xaxis.get_majorticklabels(), color='white')

    for ax in [ax_spec, ax_wf]:
        for spine in ax.spines.values():
            spine.set_color('gray')
        plt.setp(ax.xaxis.get_majorticklabels(), color='white')
        plt.setp(ax.yaxis.get_majorticklabels(), color='white')

    outpath = os.path.join(outdir, 'waterfall.png')
    fig.savefig(outpath, dpi=150, facecolor=fig.get_facecolor())
    plt.close('all')

    snr = avg_spectrum[peak_idx] - noise_floor
    print("\n" + "=" * 55)
    print("  WATERFALL SCAN REPORT (Sweep mode)")
    print("=" * 55)
    print(f"  Noise floor:      {noise_floor:.1f} dB")
    print(f"  Peak frequency:   {freqs_mhz[peak_idx]:.2f} MHz ({avg_spectrum[peak_idx]:.1f} dB)")
    print(f"  SNR:              {snr:+.1f} dB")
    print(f"  Signals found:    {len(groups)}")
    for i, g in enumerate(groups):
        g_freqs = freqs_mhz[g]
        peak_g_idx = g[np.argmax(avg_spectrum[g])]
        center_g = (min(g_freqs) + max(g_freqs)) / 2
        bw = max(g_freqs) - min(g_freqs)
        if len(g) > 1:
            bw += freqs_mhz[1] - freqs_mhz[0]
        print(f"    Signal {i+1}: {min(g_freqs):.2f}-{max(g_freqs):.2f} MHz "
              f"(center {center_g:.2f}, BW ~{bw*1000:.0f} kHz, "
              f"peak {avg_spectrum[peak_g_idx]:.1f} dB, "
              f"SNR {avg_spectrum[peak_g_idx]-noise_floor:+.1f} dB)")
    print("=" * 55)
    print(f"\nPlot saved: {outpath}")
    return outpath


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Generate waterfall from HackRF data')
    parser.add_argument('--start', type=float, default=420,
                        help='Start frequency MHz (default: 420)')
    parser.add_argument('--end', type=float, default=440,
                        help='End frequency MHz (default: 440)')
    parser.add_argument('--mode', choices=['iq', 'sweep'], default='iq',
                        help='Capture mode: iq (high-res, default) or sweep (quick)')
    parser.add_argument('--lna', type=int, default=16,
                        help='LNA gain dB (default: 16)')
    parser.add_argument('--vga', type=int, default=20,
                        help='VGA gain dB (default: 20)')
    parser.add_argument('--duration', type=float, default=5,
                        help='IQ capture duration in seconds (default: 5)')
    parser.add_argument('--fft', type=int, default=4096,
                        help='FFT size for IQ mode (default: 4096)')
    parser.add_argument('--avg', type=int, default=50,
                        help='FFT averaging per waterfall row (default: 50)')
    parser.add_argument('--sweeps', type=int, default=50,
                        help='Number of sweeps for sweep mode (default: 50)')
    parser.add_argument('--bin', type=float, default=1000000,
                        help='Bin width Hz for sweep mode (default: 1MHz)')
    parser.add_argument('--input', type=str, default=None,
                        help='Input file (IQ raw for iq mode, CSV for sweep mode)')
    parser.add_argument('--freq', type=float, default=None,
                        help='Center frequency Hz for IQ input file')
    parser.add_argument('--rate', type=float, default=None,
                        help='Sample rate for IQ input file (Hz)')
    parser.add_argument('--outdir', default='.',
                        help='Output directory')

    args = parser.parse_args()

    # Compute sample rate and center freq for IQ mode
    standard_rates = [2e6, 4e6, 5e6, 8e6, 10e6, 12.5e6, 16e6, 20e6]
    bandwidth = (args.end - args.start) * 1e6
    min_rate = bandwidth * 1.1
    sample_rate = min((r for r in standard_rates if r >= min_rate), default=20e6)
    center_freq = ((args.start + args.end) / 2) * 1e6

    if args.mode == 'iq':
        if args.input:
            iq_file = args.input
            freq = args.freq if args.freq else center_freq
            rate = args.rate if args.rate else sample_rate
        else:
            n_samples = int(sample_rate * args.duration)
            iq_file = '/tmp/iq_waterfall_capture.raw'
            print(f"Capturing IQ: center={center_freq/1e6:.1f} MHz, "
                  f"rate={sample_rate/1e6:.1f} MSPS, "
                  f"duration={args.duration}s")
            result = subprocess.run(
                ['hackrf_transfer', '-f', str(int(center_freq)),
                 '-s', str(int(sample_rate)),
                 '-l', str(args.lna), '-g', str(args.vga),
                 '-n', str(n_samples), '-r', iq_file],
                capture_output=True, text=True, timeout=300)
            if result.returncode != 0:
                print(f"ERROR: hackrf_transfer failed: {result.stderr}")
                sys.exit(1)
            freq = center_freq
            rate = sample_rate

        freq_res = rate / args.fft
        title = (f"| {args.start}-{args.end} MHz | IQ {rate/1e6:.1f} MSPS | "
                  f"{freq_res/1000:.1f} kHz res | LNA={args.lna} VGA={args.vga}")
        outpath = generate_iq_waterfall(iq_file, freq, rate, args.outdir,
                                         title, fft_size=args.fft,
                                         avg_factor=args.avg)
        if not args.input and iq_file.startswith('/tmp/'):
            try:
                os.remove(iq_file)
            except OSError:
                pass

    else:  # sweep mode
        if args.input:
            with open(args.input, 'r') as f:
                data_text = f.read()
        else:
            print(f"Running hackrf_sweep: {args.start}-{args.end} MHz, "
                  f"{args.sweeps} sweeps, LNA={args.lna} VGA={args.vga}...")
            result = subprocess.run(
                ['hackrf_sweep', '-f',
                 f'{int(args.start)}:{int(args.end)}',
                 '-l', str(args.lna), '-g', str(args.vga),
                 '-w', str(int(args.bin)), '-N', str(args.sweeps)],
                capture_output=True, text=True, timeout=180)
            data_text = result.stdout

        time_bins, all_freqs, times = parse_sweep_data(data_text)
        if not times:
            print("ERROR: No sweep data received")
            sys.exit(1)

        title = (f"| {args.start}-{args.end} MHz | {args.sweeps} sweeps | "
                  f"{args.bin/1000:.0f} kHz bins | LNA={args.lna} VGA={args.vga}")
        generate_sweep_waterfall(time_bins, all_freqs, times, args.outdir, title)


if __name__ == '__main__':
    main()
