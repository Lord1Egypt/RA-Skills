---
name: hackrf-sdr
description: Use HackRF One SDR for frequency scanning, IQ capture, signal analysis, waterfall generation, and demodulation. Use when the user wants to scan radio frequencies, analyze signals, capture IQ data, identify modulation types, generate waterfall/spectrum plots, or demodulate FM/AM/SSB signals with HackRF. Also use for radio monitoring, signal intelligence, or any SDR-related task.
---

# HackRF SDR Skill

Operate the HackRF One software-defined radio for scanning, capture, analysis, and demodulation.

## Prerequisites

- HackRF One connected via USB
- `hackrf_sweep` and `hackrf_transfer` CLI tools installed
- Python 3 with numpy, scipy, matplotlib

Verify: `hackrf_info` should show device info.

## Gain Settings

Default LNA=20 VGA=20 provides a good balance — noise floor is visible but not saturating, and real signals stand out clearly in the waterfall (blue background, yellow/red for signals).

- **LNA=20 VGA=20** — recommended default, clean waterfall
- **LNA=40 VGA=40** — maximum sensitivity, but waterfall turns uniformly warm/yellow (saturated noise); use only for very weak signals
- **LNA=0 VGA=0** — minimum, only for very strong nearby transmitters

When in doubt, start with LNA=20 VGA=20. Adjust if the waterfall is too hot (all yellow) or too cold (all dark blue).

## Workflow

### 1. Waterfall Visualization (IQ Mode — Recommended)

The waterfall script has two modes. **IQ mode** is the default and produces high-resolution, artifact-free waterfalls.

```bash
python3 scripts/waterfall.py --start 420 --end 440
```

This automatically:
1. Captures IQ samples via `hackrf_transfer` (5 seconds, appropriate sample rate)
2. Computes a spectrogram with ~5 kHz FFT resolution
3. Generates a clean waterfall + spectrum PNG
4. Deletes the temporary IQ capture file

**Options:**
- `--duration 5` — capture duration in seconds (default: 5)
- `--fft 4096` — FFT size, controls frequency resolution (default: 4096 ≈ 4.9 kHz at 20 MSPS)
- `--lna 20 --vga 20` — gain settings
- `--start / --end` — frequency range in MHz

**From existing IQ file:**
```bash
python3 scripts/waterfall.py --input capture.raw --freq 430e6 --rate 20e6
```

**Why IQ mode over sweep mode:**
- Fine frequency resolution (~5 kHz vs ~200 kHz)
- No horizontal stripe artifacts from sweep-to-sweep gain variation
- Real time axis in seconds
- DC spike at center frequency is visible (expected)

### 2. Waterfall Visualization (Sweep Mode — Quick Preview)

For a quick low-resolution preview using `hackrf_sweep`:

```bash
python3 scripts/waterfall.py --mode sweep --start 420 --end 440
```

- Resolution limited to ~200 kHz (hackrf_sweep truncates sub-bins)
- May show horizontal stripe artifacts
- Y-axis is sweep number, not real time
- Useful for quick wideband surveys before targeting with IQ mode

### 3. Frequency Sweep (Direct)

Use `hackrf_sweep` directly for quick signal discovery:

```bash
hackrf_sweep -f <start_mhz>:<end_mhz> -l 20 -g 20 -w 1000000 -N 50
```

- `-w 1000000`: 1 MHz bins for wide scans (200 kHz effective resolution)
- `-N 50`: 50 sweeps for averaging

**Note:** `hackrf_sweep` truncates sub-bins when bin width is too narrow (e.g., `-w 50000` reports 404 bins but delivers only ~101 per row). Use `-w 1000000` for reliable sweeps, or use IQ mode for detail.

### 4. IQ Capture (Manual)

Record raw IQ samples for detailed analysis:

```bash
hackrf_transfer -f <freq_hz> -s <sps> -l 20 -g 20 -n <samples> -r /tmp/iq_capture.raw
```

- Sample rate (`-s`): 20M for 20 MHz bandwidth, 10M for 10 MHz, 2M for narrow
- Duration: `-n` = sample_rate × seconds (e.g., 20M × 5s = 100000000)
- Always capture with enough BW to include the signal + margin
- Use lower gain (LNA=20 VGA=20) to avoid ADC clipping

**Always delete IQ captures after analysis** — they are large (~200 MB for 5s at 20 MSPS).

### 5. Signal Analysis

Analyze captured IQ data for modulation type, bandwidth, SNR:

```bash
python3 scripts/analyze.py /tmp/iq_capture.raw --freq <center_hz> --rate <sps> --outdir <dir>
```

The script:
- Computes PSD and spectrogram
- Detects peak frequency and SNR
- Measures 3dB and 10dB bandwidth
- Classifies modulation (CW, AM, FM, PSK, QAM, etc.)
- Detects pulsed vs continuous signals
- Finds secondary peaks
- Generates a 6-panel analysis PNG

### 6. Demodulation

Demodulate audio from IQ captures:

```bash
python3 scripts/demod.py /tmp/iq_capture.raw --mode <fm|am|usb|lsb> --offset <hz> --out <file.wav>
```

- `--offset`: signal frequency offset from center (from analyze.py output)
- Output: WAV at 48 kHz

### 7. Cleanup

After analysis, **delete IQ capture files**:

```bash
rm -f /tmp/iq_capture.raw
```

## Tips

- Start with a wide scan (100 MHz), then narrow down to signals of interest
- **IQ mode waterfall**: ~5 kHz resolution, no artifacts, real time axis — preferred for detailed analysis
- **Sweep mode waterfall**: ~200 kHz resolution, may have horizontal artifacts — quick preview only
- **Waterfall color scale**: noise floor → deep blue, signals → yellow/red. Adjust gain if too hot/cold.
- HackRF int8 format: 2 bytes per sample (I + Q), so 20 MSPS ≈ 40 MB/s
- For signals near DC, offset tune by 1-2 MHz to avoid DC spike
- The peak frequency from `analyze.py` is the offset from center — add to center freq for absolute freq
- Reference: `references/frequency_bands.md` for band allocations and modulation classification