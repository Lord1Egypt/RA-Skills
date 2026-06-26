# HackRF + LilyGo Combined Workflow

Use HackRF One for fast wideband survey, then focus LilyGo CAD scanner on confirmed active bands.

## Step 1: Wideband HackRF Sweep

```bash
# Sweep 430–445 MHz, 25 kHz resolution, ~8 seconds
hackrf_sweep -f 430:445 -w 25000 -l 32 -g 40 > /tmp/sweep.csv &
sleep 8 && kill %1

# Parse peaks
python3 scripts/parse_sweep.py /tmp/sweep.csv --threshold 10
```

Example output:
```
Noise floor: -52.6 dBm
Peaks >10 dB above noise:
  432.0000 MHz  -32.9 dBm  SNR=19.7 dB   ← 70cm calling freq
  437.6750 MHz  -39.8 dBm  SNR=12.8 dB   ← satellite downlink
  440.0000 MHz  -19.3 dBm  SNR=33.3 dB   ← band edge beacon
```

## Step 2: NFM Demodulation (optional)

```bash
# Capture 8s at a specific frequency
hackrf_transfer -r /tmp/iq.raw -f 432000000 -s 2000000 -l 32 -g 40 -n 16000000
```

Then demodulate with `scipy` to identify signal type (voice, digital, beacon).

## Step 3: Focus LilyGo on Confirmed Band

After identifying LoRa-likely frequencies, update sketch:

```cpp
// Example: focus on 433-435 MHz after HackRF confirmed activity
#define FREQ_START  433000000UL
#define FREQ_END    435000000UL
#define FREQ_STEP     25000UL    // finer step for targeted scan
```

## Known Frequency Allocations (EU / Region 1)

| Frequency | Use |
|---|---|
| 430–440 MHz | 70cm amateur band |
| 432.000 MHz | SSB/CW calling frequency (EME, meteor scatter) |
| 433.050–434.790 MHz | ISM band (LoRa, remote controls, sensors) |
| 433.175 MHz | LoRaWAN EU channel 0 |
| 433.375 MHz | LoRaWAN EU channel 1 |
| 433.575 MHz | LoRaWAN EU channel 2 |
| 434.665 MHz | Radiosonde (RS41) |
| 435–438 MHz | Amateur satellite downlinks (CubeSats) |
| 440.000 MHz | Band edge beacon |

## HackRF Signal Analysis Tips

- **BW < 15 Hz, no modulation**: oscillator spurious or band edge beacon
- **BW ~50 kHz, SSB audio**: amateur SSB voice
- **Dominant tone ~2400 Hz after NFM demod**: POCSAG pager or AFSK data
- **Consistent −16 dBfs, zero audio**: FM broadcast harmonic (check 88 MHz × N)
- **Drifting frequency**: satellite pass (Doppler shift ~3 kHz/s at 437 MHz)
